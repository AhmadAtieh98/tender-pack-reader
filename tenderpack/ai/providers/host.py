"""The coding-host route (Claude Code or Codex using ITS OWN model): the application makes NO API call and spends
nothing. The host reads the same tools through MCP (`tenderpack ai serve-mcp`) or the CLI (`tenderpack ai tool NAME
--json ...`), claims the addendum's lock with the task packet, and submits a proposal file:

    tenderpack ai submit FILE --route host --host-model NAME

The controller validates a submitted set exactly as it validates an API run (the same contract, checks and status
assignment). What model the host used is declared by the host (`--host-model`) and recorded as declared; this tool
cannot verify it. Capabilities are the host's and are recorded as unknown.
"""
from __future__ import annotations

from .base import Capabilities, ProviderError, Request, Response


class HostProvider:
    name = "host"
    paid = False

    def __init__(self, model: str | None = None):
        from ..offline import check_adapter
        check_adapter("host")                       # session 14 (W6): offline mode, also when built directly
        self.model = model or "undeclared"

    def capabilities(self) -> Capabilities:
        return Capabilities(images=None, tools=None, structured_output=None, context_tokens=None,
                            retention="the coding host's own policy; not verified by this tool",
                            source="declared by the host; not checked by this tool")

    def complete(self, request: Request) -> Response:
        raise ProviderError("host_route", "the host route makes no API call: the host drives the tools over MCP or the "
                                          "CLI and submits a ProposalSet with `tenderpack ai submit FILE --route host "
                                          "--host-model NAME`", False)
