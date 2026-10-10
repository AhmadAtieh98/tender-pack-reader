"""Session 13 (part 2, item 6): critical rules enforced in code and tool permissions, not only in prompt text.

Promotion wrote each curated input where the candidate's pack.yaml said, defaulting to the repository's path when a key
was missing: candidate isolation rested on the paths candidate.create wrote. downstream.candidate_path now refuses any
write that does not resolve inside the run's candidate. The host sessions' tool permissions (no built-in tools, only
the tenderpack MCP tools, the writers an answer session must not call disallowed) are pinned here as regressions."""
from __future__ import annotations

from pathlib import Path

import pytest

from tenderpack.ai import downstream as DS
from tenderpack.ai import hostsession as hs


def test_promotion_refuses_a_write_outside_the_candidate(tmp_path):
    cdir = tmp_path / "candidate"
    (cdir / "curation").mkdir(parents=True)
    inside = DS.candidate_path(cdir, {"register": str(cdir / "curation/register/rows.yaml")}, "register",
                               "curation/register/rows.yaml")
    assert inside.is_relative_to(cdir)
    with pytest.raises(ValueError, match="only inside the candidate"):
        DS.candidate_path(cdir, {}, "register", "curation/register/rows.yaml")       # the default: the REAL curation
    with pytest.raises(ValueError, match="only inside the candidate"):
        DS.candidate_path(cdir, {"issues": str(cdir / ".." / "elsewhere.yaml")}, "issues", "x")


class _WS:
    evidence, pack, staging, worklog, ai_config, root = Path("/e"), Path("/p"), Path("/s"), Path("/w"), None, Path("/r")


def _session(cls, **kw):
    s = object.__new__(cls)
    s.cfg = {}
    s.ws, s.claude_bin, s.output_format, s.max_turns, s.model, s.python = _WS(), "claude", "stream-json", 5, None, "py"
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def test_host_sessions_have_no_built_in_tools_and_only_the_tenderpack_mcp_tools():
    cmd = _session(hs.HostSession).command(Path("/m.json"))
    assert cmd[cmd.index("--tools") + 1] == "" and "--strict-mcp-config" in cmd
    # session 13 (implementer C, deliberate): deny-by-default. The allow list is no longer the wildcard
    # "mcp__tenderpack__*" but exactly the phase's tools (tenderpack.ai.policy.tools), every other tool disallowed by
    # name; tests/test_session13_policy.py::test_host_sessions_allow_exactly_the_phase_tools pins the exact lists.
    allowed = cmd[cmd.index("--allowedTools") + 1].split(",")
    assert hs.TOOL_PREFIX + "*" not in allowed and hs.TOOL_PREFIX + "submit_proposals" in allowed
    dis = cmd[cmd.index("--disallowedTools") + 1].split(",")
    assert {hs.TOOL_PREFIX + t for t in ("get_task_packet", "request_review")} <= set(dis)
    ans = _session(hs.AnswerSession, _system="S", _rules="R", _tools=None).command(Path("/m.json"))
    assert hs.TOOL_PREFIX + "submit_proposals" in ans[ans.index("--disallowedTools") + 1].split(",")
