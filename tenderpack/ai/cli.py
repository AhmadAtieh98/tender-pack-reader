"""`tenderpack ai ...`: the AI layer's command line (the same functions as the MCP server).

  propose ADDENDUM --route recorded|anthropic|openrouter|ollama [--model M] [--cassette P] [caps] [--provisions ..]
          [--include-crop UNIT] [--reference OPFILE] [--break-lock --by NAME] [--evidence --pack --out --worklog]
          one controller run; writes staging/ai/<run_id>/ only. Exit 0 when the set is complete or partial, 1 when it
          is malformed, stale, budget_exhausted or provider_failed, 2 when the run is refused before any call.
  task ADDENDUM [--claim --host-model NAME] [--provisions ..]   the task packet for a coding host (JSON on stdout);
          --claim takes the addendum's lock for the host route
  submit FILE --route host --host-model NAME        validate a host's ProposalSet exactly as an API run; stage it
  validate FILE                                     the controller's statuses for a set, against the current state;
                                                    writes nothing
  tool NAME --json '{...}'                          run one tool (for a host without MCP); JSON on stdout
  serve-mcp                                         the MCP server on stdin/stdout
  capabilities --route R [--model M] [--cassette P] what the endpoint reports (a live, free call for openrouter, ollama
                                                    and, with a key, anthropic); prints the source of each value
  promote RUN_ID --by NAME                          a person copies verified items into curation as PROPOSED drafts
  locks [--break ADDENDUM --by NAME]                list (or break) orchestrator locks
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from ..util import ROOT


def add_parser(sub) -> None:
    ai = sub.add_parser("ai", help="AI proposals: propose, submit, validate, tools, MCP server, promote")
    s = ai.add_subparsers(dest="ai_cmd", required=True)

    def common(p, staging=True):
        p.add_argument("--evidence", default=str(ROOT / "build"))
        p.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
        p.add_argument("--config", default=str(ROOT / "config/ai.yaml"), help="AI configuration (routes, caps, prices)")
        if staging:
            p.add_argument("--out", default=str(ROOT / "staging/ai"), help="staging directory (never curation/)")
            p.add_argument("--worklog", default=str(ROOT / "worklog/model_calls"))

    p = s.add_parser("propose")
    p.add_argument("addendum")
    p.add_argument("--route", required=True, choices=["recorded", "anthropic", "openrouter", "ollama"])
    p.add_argument("--model")
    p.add_argument("--cassette", help="recorded route: the cassette to replay")
    for cap, t in (("max-usd", float), ("max-calls", int), ("max-input-tokens", int), ("max-output-tokens", int),
                   ("timeout-s", float), ("max-turns", int)):
        p.add_argument(f"--{cap}", type=t)
    p.add_argument("--provisions", help="comma-separated provision ids or prefixes (default: every provision)")
    p.add_argument("--include-crop", action="append", default=[], help="unit id whose image crop the task includes")
    p.add_argument("--reference", help="op file to compare the proposals with (report only)")
    p.add_argument("--break-lock", action="store_true")
    p.add_argument("--by", help="the person breaking a lock")
    common(p)
    t = s.add_parser("task")
    t.add_argument("addendum")
    t.add_argument("--claim", action="store_true", help="take the addendum's lock for the host route")
    t.add_argument("--host-model")
    t.add_argument("--provisions")
    common(t)
    u = s.add_parser("submit")
    u.add_argument("file")
    u.add_argument("--route", required=True, choices=["host"])
    u.add_argument("--host-model", required=True, help="the model the host used (recorded as declared)")
    common(u)
    v = s.add_parser("validate")
    v.add_argument("file")
    common(v)
    w = s.add_parser("tool")
    w.add_argument("name")
    w.add_argument("--json", default="{}", help="the tool's arguments as a JSON object")
    common(w)
    m = s.add_parser("serve-mcp")
    common(m)
    c = s.add_parser("capabilities")
    c.add_argument("--route", required=True, choices=["recorded", "anthropic", "openrouter", "ollama", "host"])
    c.add_argument("--model")
    c.add_argument("--cassette")
    c.add_argument("--config", default=str(ROOT / "config/ai.yaml"))
    pr = s.add_parser("promote")
    pr.add_argument("run_id")
    pr.add_argument("--by", required=True)
    pr.add_argument("--amendments-dir")
    pr.add_argument("--proposals-dir")
    common(pr)
    lk = s.add_parser("locks")
    lk.add_argument("--break", dest="brk")
    lk.add_argument("--by")
    common(lk)


def _ws(a):
    from .tools import Workspace
    return Workspace(Path(a.evidence), Path(a.pack), ROOT, Path(getattr(a, "out", ROOT / "staging/ai")),
                     Path(getattr(a, "worklog", ROOT / "worklog/model_calls")), Path(a.config))


def _print(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def run(a) -> int:
    from . import budget as B
    from . import config as C
    from . import controller
    from .tools import ToolError, call_tool
    try:
        if a.ai_cmd == "capabilities":
            from .providers import make
            from .providers.base import ProviderError
            cfg = C.load(Path(a.config))
            rcfg = C.route(cfg, a.route)
            prov = make(a.route, a.model or C.default_model(rcfg), cfg, a.cassette)
            try:
                _print({"route": a.route, "model": prov.model, **prov.capabilities().to_dict()})
            except ProviderError as e:
                print(f"REFUSED: {e.message}")
                return 2
            return 0
        ws = _ws(a)
        if a.ai_cmd == "propose":
            cfg = C.load(Path(a.config))
            caps = {"max_usd": a.max_usd, "max_calls": a.max_calls, "max_input_tokens": a.max_input_tokens,
                    "max_output_tokens": a.max_output_tokens, "timeout_s": a.timeout_s, "max_turns": a.max_turns}
            if a.break_lock and not a.by:
                print("refused: --break-lock needs --by \"Your Name\"")
                return 2
            ps = controller.propose(ws, a.addendum, a.route, cfg, model=a.model, cassette=a.cassette, caps=caps,
                                    include_crops=a.include_crop or None,
                                    provisions=[x.strip() for x in a.provisions.split(",")] if a.provisions else None,
                                    reference=a.reference, break_lock_by=a.by if a.break_lock else None)
            counts: dict[str, int] = {}
            for it in ps.items:
                counts[it.verification_status] = counts.get(it.verification_status, 0) + 1
            print(f"run {ps.run_id}: {ps.status}; items {counts or 'none'}; coverage {ps.coverage.accounted}/"
                  f"{ps.coverage.provisions_total}; usage {ps.usage.calls} calls, {ps.usage.input_tokens} in / "
                  f"{ps.usage.output_tokens} out; cost {ps.usage.cost_usd} ({ps.usage.cost_basis})")
            print(f"staging: {Path(a.out) / ps.run_id}/review_request.md")
            return 0 if ps.status in ("complete", "partial") else 1
        if a.ai_cmd == "task":
            _print(controller.host_task(ws, a.addendum, claim=a.claim, host_model=a.host_model,
                                        provisions=[x.strip() for x in a.provisions.split(",")] if a.provisions else None))
            return 0
        if a.ai_cmd == "submit":
            res = controller.submit(ws, Path(a.file), a.host_model, via="cli")
            _print(res)
            return 0 if res["status"] in ("complete", "partial") else 1
        if a.ai_cmd == "validate":
            data = controller._load_set_data(Path(a.file))
            _print(controller.validate_payload(ws, data))
            return 0
        if a.ai_cmd == "tool":
            try:
                args = json.loads(a.json)
            except ValueError as e:
                print(f"refused: --json is not JSON: {e}")
                return 2
            _print(call_tool(ws, a.name, args, caller="cli"))
            return 0
        if a.ai_cmd == "serve-mcp":
            from ..mcp_server import serve
            return serve(ws)
        if a.ai_cmd == "promote":
            code, msgs = controller.promote(ws, a.run_id, a.by, Path(a.amendments_dir) if a.amendments_dir else None,
                                            Path(a.proposals_dir) if a.proposals_dir else None)
            print("\n".join(msgs))
            return code
        if a.ai_cmd == "locks":
            cfg = C.load(Path(a.config))
            staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
            if a.brk:
                ok, msg = B.break_lock(staging, a.brk, a.by or "", cfg.get("lock_stale_after_min", 120))
                print(msg)
                return 0 if ok else 2
            for p in sorted(staging.glob(".lock-*")) if staging.is_dir() else []:
                info = B.read_lock(p) or {}
                stale, why = B.lock_state(info, cfg.get("lock_stale_after_min", 120))
                print(f"{p.name}: {'STALE' if stale else 'live'} — {why}")
            return 0
    except (B.Refused, C.ConfigError, ToolError) as e:
        print(f"REFUSED: {e}", file=sys.stdout)
        return 2
    return 2
