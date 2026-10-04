"""`tenderpack ai ...` subcommands of the routes layer (session 10). Wired into tenderpack/ai/cli.py by:

    from . import cli_routes
    cli_routes.add_subcommands(s)                    # in add_parser, `s` = the `ai` subparsers
    if a.ai_cmd in cli_routes.COMMANDS:              # at the top of run()
        return cli_routes.handle(a)

  critic RUN_ID [--route host|recorded|anthropic|openrouter|ollama] [--model M] [--cassette P] [--max-items N]
          [--allow-unverified-capabilities] [--max-calls N --max-input-tokens N --max-output-tokens N]
          a second, independent model pass over the run's selected items (removals, conflicts, interpretations with
          a consequence, uncertain targets); writes review.critic into staging/ai/RUN_ID only; changes no status.
  host-session ADDENDUM [--provisions ID,..] [--model M] [--max-turns N] [--timeout-s S] [--claude-bin PATH]
          an actual headless Claude Code session over the tenderpack MCP tools (no file or shell tools): it reads the
          crops it needs, submits through submit_proposals; prints the run ids, the elapsed time, the tool calls, the
          crops read and the statuses. The host's own plan pays.
  plan-batches ADDENDUM [--route R --model M --cassette P | --context-tokens N --max-output-tokens N]
          [--provisions ID,..] [--count-tokens] [--allow-unverified-capabilities]
          the bounded batches for the addendum (JSON): every provision in exactly one batch; a provision too large
          alone is flagged "too large: needs a person to split". Capabilities come from the endpoint (or a cassette);
          numbers given on the command line are labelled as such.
Exit codes: 0 done, 1 done with failures (an item the critic could not review; a host session without a submission;
a provision too large), 2 refused before anything ran.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from ..util import ROOT

COMMANDS = ("critic", "host-session", "plan-batches")


def _common(p) -> None:
    p.add_argument("--evidence", default=str(ROOT / "build"))
    p.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    p.add_argument("--config", default=str(ROOT / "config/ai.yaml"), help="AI configuration (routes, caps, prices)")
    p.add_argument("--out", default=str(ROOT / "staging/ai"), help="staging directory (never curation/)")
    p.add_argument("--worklog", default=str(ROOT / "worklog/model_calls"))


def _caps(p) -> None:
    for cap, t in (("max-calls", int), ("max-input-tokens", int), ("max-output-tokens", int), ("max-usd", float)):
        p.add_argument(f"--{cap}", type=t)


def add_subcommands(sub) -> None:
    c = sub.add_parser("critic", help="independent critic over a staged run's selected items (changes no status)")
    c.add_argument("run_id")
    c.add_argument("--route", choices=["host", "recorded", "anthropic", "openrouter", "ollama"])
    c.add_argument("--model")
    c.add_argument("--cassette", help="recorded route: the cassette to replay")
    c.add_argument("--max-items", type=int)
    c.add_argument("--allow-unverified-capabilities", action="store_true",
                   help="a person's choice: run on the configured capabilities when the endpoint does not verify them "
                        "(logged; shown in the review request)")
    _caps(c)
    _common(c)
    h = sub.add_parser("host-session", help="an actual headless Claude Code session over the MCP tools")
    h.add_argument("addendum")
    h.add_argument("--provisions", help="comma-separated provision ids or prefixes (default: every provision)")
    h.add_argument("--model", help="the host model (default: config host_session.model, else the CLI's default)")
    h.add_argument("--max-turns", type=int)
    h.add_argument("--timeout-s", type=float)
    h.add_argument("--claude-bin")
    _common(h)
    b = sub.add_parser("plan-batches", help="bounded batches for an addendum (every provision in exactly one)")
    b.add_argument("addendum")
    b.add_argument("--route", choices=["recorded", "anthropic", "openrouter", "ollama"])
    b.add_argument("--model")
    b.add_argument("--cassette")
    b.add_argument("--context-tokens", type=int, help="a person's figure when no endpoint is consulted (labelled so)")
    b.add_argument("--max-output-tokens", type=int)
    b.add_argument("--provisions")
    b.add_argument("--count-tokens", action="store_true", help="calibrate sizes with the route's token-count endpoint")
    b.add_argument("--allow-unverified-capabilities", action="store_true")
    _common(b)


def _ws(a):
    from .tools import Workspace
    return Workspace(Path(a.evidence), Path(a.pack), ROOT, Path(a.out), Path(a.worklog), Path(a.config))


def _print(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def _cfg(a) -> dict:
    from . import config as C
    from .providers.base import ALLOW_UNVERIFIED_KEY
    cfg = C.load(Path(a.config))
    if getattr(a, "allow_unverified_capabilities", False):
        cfg[ALLOW_UNVERIFIED_KEY] = True
    return cfg


def handle(a) -> int:
    from . import budget as B
    from . import config as C
    from .providers.base import ProviderError
    from .tools import ToolError
    try:
        if a.ai_cmd == "critic":
            return _critic(a)
        if a.ai_cmd == "host-session":
            return _host_session(a)
        if a.ai_cmd == "plan-batches":
            return _plan(a)
    except (B.Refused, C.ConfigError, ToolError) as e:
        print(f"REFUSED: {e}", file=sys.stdout)
        return 2
    except ProviderError as e:
        print(f"REFUSED: {e.message}", file=sys.stdout)
        return 2
    return 2


def _critic(a) -> int:
    from . import critic
    caps = {"max_calls": a.max_calls, "max_input_tokens": a.max_input_tokens, "max_output_tokens": a.max_output_tokens,
            "max_usd": a.max_usd}
    res = critic.run(_ws(a), a.run_id, route=a.route, model=a.model, cassette=a.cassette, cfg=_cfg(a),
                     max_items=a.max_items, caps={k: v for k, v in caps.items() if v is not None})
    _print(res)
    return 1 if res["errors"] else 0


def _host_session(a) -> int:
    from .hostsession import HostSession, host_packet
    ws = _ws(a)
    provs = [x.strip() for x in a.provisions.split(",")] if a.provisions else None
    pk = host_packet(ws, a.addendum, provs)
    hs = HostSession(ws, _cfg(a), model=a.model, max_turns=a.max_turns, timeout_s=a.timeout_s, claude_bin=a.claude_bin)
    ps = hs.run_batch(pk)
    r = hs.last
    _print({"session_run": r.run_id, "elapsed_s": r.elapsed_s, "exit_code": r.exit_code, "error": r.error,
            "model_requested": r.model_requested or "the CLI's default", "model_reported": r.model_reported,
            "num_turns": r.num_turns, "tool_calls": len(r.tool_calls),
            "tool_call_names": [c["name"] for c in r.tool_calls], "crops_read": r.crops_read,
            "images_received": sum(len(x["received"]) for x in r.images_received),
            "submission_run": (r.submission or {}).get("run_id"), "set_status": ps.get("status"),
            "statuses": r.statuses, "host_plan_cost_usd": r.host_plan_cost_usd,
            "note": "host_plan_cost_usd is the host's own plan usage, not the application's spend",
            "session_folder": r.run_dir})
    return 0 if r.submission else 1


def _plan(a) -> int:
    from . import batching as BT
    from . import config as C
    from .controller import SYSTEM, task_packet
    from .tools import MODEL_TOOLS, TOOLS
    ws = _ws(a)
    cfg = _cfg(a)
    ws.refresh()
    provs = [x.strip() for x in a.provisions.split(",")] if a.provisions else None
    pk = task_packet(ws, a.addendum, provs)
    tools = [TOOLS[n].spec() for n in MODEL_TOOLS]
    prov = None
    if a.route:
        from .providers import make
        prov = make(a.route, a.model or C.default_model(C.route(cfg, a.route)), cfg, a.cassette)
        if hasattr(prov, "check_ready") and a.route != "ollama":
            prov.check_ready()
        caps = prov.capabilities().to_dict()
    elif a.context_tokens:
        caps = {"context_tokens": a.context_tokens, "max_output_tokens": a.max_output_tokens,
                "source": "given on the command line by a person (not checked against an endpoint)"}
    else:
        print("REFUSED: name a --route whose endpoint (or cassette) reports the limits, or give --context-tokens "
              "(labelled as a person's figure)")
        return 2
    ratio, source = None, None
    if a.count_tokens:
        if prov is None:
            print("REFUSED: --count-tokens needs a --route with a token-count endpoint")
            return 2
        from .controller import _packet_text
        ratio, source = BT.calibrate(prov, _packet_text(pk), SYSTEM, tools)
    per_call = C.caps(cfg, a.route or "recorded").get("max_tokens_per_call")
    settings = {**(cfg.get("batching") or {}), **((C.route(cfg, a.route).get("batching") or {}) if a.route else {})}
    ov = BT.overhead_for(pk, SYSTEM, tools, max_output_tokens=a.max_output_tokens or per_call,
                         settings=settings, chars_per_token=ratio, size_source=source)
    batches = BT.plan_batches(BT.packet_provisions(pk), caps, ov)
    out = BT.summary(batches)
    out.update({"addendum": a.addendum, "capabilities": {k: caps.get(k) for k in ("context_tokens", "max_output_tokens",
                                                                                    "source")},
                "overhead": ov.__dict__, "provisions_in_packet": len(pk["provisions"]),
                "provisions_total": pk["provisions_total"]})
    _print(out)
    return 1 if out["too_large"] else 0


def main(argv=None) -> int:
    """`python -m tenderpack.ai.cli_routes COMMAND ...` (the same commands, before they are wired into `tenderpack ai`)."""
    import argparse
    ap = argparse.ArgumentParser(prog="tenderpack.ai.cli_routes")
    add_subcommands(ap.add_subparsers(dest="ai_cmd", required=True))
    return handle(ap.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
