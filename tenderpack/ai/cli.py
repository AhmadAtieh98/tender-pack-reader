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

The workflow (session 10; tenderpack/ai/workflow.py): from a new addendum PDF and the preceding state to isolated
candidate A1-A5 outputs and a review packet, checkpointed and resumable (staging/ai/runs/<run_id>/):
  run ADD-NN --pdf PATH [--route recorded|host|anthropic|openrouter|ollama] [--pack config/pack.yaml]
          [--evidence build] [--run-id ID] [--batch-size N] [--downstream-batch-size N] [--model M] [--cassette P]
          [--host-model M] [--host-manual] [--stop-after STEP] [--no-background] [--no-cache] [caps]
          Exit 0 when the run finished (complete or partial) or stopped where asked, 1 when a step failed or the
          candidate outputs build was refused, 2 when refused before anything ran (or ingest failed structurally),
          4 when it waits for a host submission, 5 when a batch was deferred for a rate limit, 6 (session 12) when
          it stopped because it cannot go on until a person acts (no usable reading of an image region, readings
          escalated to a person, inputs changed before promotion); the reason says what to do, then `resume`.
  resume RUN_ID [--stop-after STEP] [--no-retry] [--from STEP] [--base-run RUN_ID]
                                 continue from the checkpoint (a failed batch is asked again; --from reruns a
                                 done step and the later ones after a code change; done batches are never asked again)
  (session 12) run ADD-04 --pdf PATH --base-run RUN_ID: consecutive addenda; the candidate starts from that run's
          candidate (its curation as promoted, its pack with its addendum and its evidence build); the base must have
          reached promotion and must not be running; --pack and --evidence are then the base's. resume --base-run
          names the run's recorded base (another one is refused). run-status names the base.
  submit-batch RUN_ID FILE --by NAME [--host-model M] [--batch ID] [--no-continue]
          the manual host path: the set answering a waiting batch's packet (batches/<id>.packet.json); recorded
          (who, when, the file's sha256) and validated as an API run's; the run then continues
  run-status RUN_ID                                 the checkpoint summary and the timings
Routes layer (tenderpack/ai/cli_routes.py, when present): critic, host-session, plan-batches, routes.
Session 12: --offline on run, resume, propose, capabilities, critic, plan-batches and routes (offline mode,
tenderpack/ai/offline.py): only the local ollama route (the recorded test replay aside); a hosted route is refused
before any call.
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
    p.add_argument("--allow-unverified-capabilities", action="store_true",
                   help="a person's choice: run on the configured capabilities when the endpoint does not verify them "
                        "(logged; shown in the review request)")
    p.add_argument("--by", help="the person breaking a lock")
    p.add_argument("--offline", action="store_true", help="offline mode: only the ollama (or recorded) route")
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
    c.add_argument("--allow-unverified-capabilities", action="store_true")
    c.add_argument("--offline", action="store_true", help="offline mode: only the ollama (or recorded) route")
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
    _add_workflow(s, common)
    routes = _routes()
    if routes is not None:
        routes.add_subcommands(s)


def _routes():
    try:
        from . import cli_routes
    except ImportError:
        return None
    return cli_routes if hasattr(cli_routes, "add_subcommands") and hasattr(cli_routes, "handle") else None


def _add_workflow(s, common) -> None:
    from .checkpoint import STEPS
    r = s.add_parser("run", help="the workflow: a new addendum PDF -> candidate A1-A5 outputs and a review packet")
    r.add_argument("addendum")
    r.add_argument("--pdf", required=True)
    r.add_argument("--route", default=None, choices=["recorded", "host", "anthropic", "openrouter", "ollama"],
                   help="default: host, or ollama in offline mode")
    r.add_argument("--offline", action="store_true",
                   help="offline mode: every phase on the local ollama route, no hosted call (also config offline: "
                        "true or TENDERPACK_OFFLINE=1)")
    r.add_argument("--run-id")
    r.add_argument("--batch-size", type=int, default=8, help="provisions per analysis batch (at most)")
    r.add_argument("--downstream-batch-size", type=int, default=12, help="downstream tasks per batch (at most)")
    r.add_argument("--model")
    r.add_argument("--cassette", help="recorded route: the recorded workflow to replay")
    r.add_argument("--host-model", help="host route: the model the host uses (recorded as declared)")
    r.add_argument("--host-manual", action="store_true", help="host route: always write the packets and wait for "
                                                              "submit-batch, even when a host session could run")
    r.add_argument("--host-model-alias", help="host route: the model the headless host session is started with "
                                              "(claude --model; default: config host_session.model, else the CLI's)")
    r.add_argument("--allow-unverified-capabilities", action="store_true",
                   help="API routes: a person's choice to run on configured capabilities the endpoint does not verify")
    r.add_argument("--stop-after", choices=list(STEPS))
    r.add_argument("--no-background", action="store_true", help="build the pre-addendum outputs at the outputs step")
    r.add_argument("--no-cache", action="store_true", help="do not reuse cached pre-addendum outputs")
    r.add_argument("--base-run", help="consecutive addenda (session 12): start from this run's candidate (its "
                                      "addendum is then the previous stage); it must have reached promotion")
    for cap, t in (("max-usd", float), ("max-calls", int), ("max-input-tokens", int), ("max-output-tokens", int),
                   ("timeout-s", float), ("max-turns", int)):
        r.add_argument(f"--{cap}", type=t)
    common(r)
    rs = s.add_parser("resume", help="continue a workflow run from its checkpoint")
    rs.add_argument("run_id")
    rs.add_argument("--stop-after", choices=list(STEPS))
    rs.add_argument("--no-retry", action="store_true", help="do not ask failed batches again")
    rs.add_argument("--offline", action="store_true", help="offline mode for this run from now on (ollama runs only)")
    rs.add_argument("--base-run", help="the run's base run, as recorded when it started (checked; another is refused)")
    rs.add_argument("--from", dest="from_step", choices=list(STEPS),
                    help="rerun this step and the later ones even when done (after a code change); "
                         "batches that succeeded are never asked again")
    common(rs)
    sb = s.add_parser("submit-batch", help="the manual host path: submit the set answering a waiting batch")
    sb.add_argument("run_id")
    sb.add_argument("file")
    sb.add_argument("--by", required=True, help="who submits (a person, or the host session); recorded")
    sb.add_argument("--host-model", help="the model the host used (analysis batches: required unless the run has it)")
    sb.add_argument("--batch", help="the batch answered (default: the one waiting)")
    sb.add_argument("--no-continue", action="store_true", help="record the submission without continuing the run")
    common(sb)
    st = s.add_parser("run-status", help="a workflow run's checkpoint summary and timings")
    st.add_argument("run_id")
    common(st)


def _run_workflow(a) -> int:
    from . import workflow as W
    if a.ai_cmd == "run":
        if a.route is None:
            from . import config as C
            from .offline import requested
            a.route = "ollama" if requested(C.load(Path(a.config)), a.offline) else "host"
        caps = {"max_usd": a.max_usd, "max_calls": a.max_calls, "max_input_tokens": a.max_input_tokens,
                "max_output_tokens": a.max_output_tokens, "timeout_s": a.timeout_s, "max_turns": a.max_turns}
        dflt = {"pack": str(ROOT / "config/pack.yaml"), "evidence": str(ROOT / "build")}
        own = {k: (None if a.base_run and getattr(a, k) == v else Path(getattr(a, k))) for k, v in dflt.items()}
        res = W.start(a.addendum, Path(a.pdf), route=a.route, pack=own["pack"], evidence=own["evidence"],
                      staging=Path(a.out), worklog=Path(a.worklog), ai_config=Path(a.config), run_id=a.run_id,
                      batch_size=a.batch_size, downstream_batch_size=a.downstream_batch_size, model=a.model,
                      cassette=Path(a.cassette) if a.cassette else None, caps=caps, host_model=a.host_model,
                      host_mode="manual" if a.host_manual else "auto", host_session_model=a.host_model_alias,
                      allow_unverified_capabilities=a.allow_unverified_capabilities, stop_after=a.stop_after,
                      background_before=not a.no_background, cache=not a.no_cache, offline=a.offline,
                      base_run=a.base_run)
    elif a.ai_cmd == "resume":
        res = W.resume(a.run_id, Path(a.out), stop_after=a.stop_after, retry_failed=not a.no_retry,
                       from_step=a.from_step, offline=a.offline, base_run=a.base_run)
    elif a.ai_cmd == "submit-batch":
        res = W.submit_batch(a.run_id, Path(a.file), a.by, a.host_model, a.batch, Path(a.out), cont=not a.no_continue)
    else:
        cp = W.load(a.run_id, Path(a.out))
        res = W.summary(cp)
        print("\n".join(W.timing_lines(cp)))
    _print(res)
    return int(res.get("exit_code", 1))


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
    routes = _routes()
    if routes is not None and a.ai_cmd in getattr(routes, "COMMANDS", ()):
        return routes.handle(a)
    try:
        if a.ai_cmd in ("run", "resume", "submit-batch", "run-status"):
            from .candidate import CandidateError
            try:
                return _run_workflow(a)
            except CandidateError as e:
                print(f"REFUSED: {e}")
                return 2
        if a.ai_cmd == "capabilities":
            from .providers import make
            from .providers.base import ProviderError
            cfg = C.load(Path(a.config))
            from .offline import activate, requested
            activate(cfg, requested(cfg, a.offline))
            rcfg = C.route(cfg, a.route)
            if getattr(a, "allow_unverified_capabilities", False):
                cfg["_allow_unverified_capabilities"] = True
            prov = make(a.route, C.phase_model(rcfg, a.route, "analysis", a.model), cfg, a.cassette)
            try:
                _print({"route": a.route, "model": prov.model, **prov.capabilities().to_dict()})
            except ProviderError as e:
                print(f"REFUSED: {e.message}")
                return 2
            return 0
        ws = _ws(a)
        if a.ai_cmd == "propose":
            cfg = C.load(Path(a.config))
            from .offline import activate, requested
            activate(cfg, requested(cfg, a.offline))
            caps = {"max_usd": a.max_usd, "max_calls": a.max_calls, "max_input_tokens": a.max_input_tokens,
                    "max_output_tokens": a.max_output_tokens, "timeout_s": a.timeout_s, "max_turns": a.max_turns}
            if a.break_lock and not a.by:
                print("refused: --break-lock needs --by \"Your Name\"")
                return 2
            ps = controller.propose(ws, a.addendum, a.route, cfg, model=a.model, cassette=a.cassette, caps=caps,
                                    include_crops=a.include_crop or None,
                                    provisions=[x.strip() for x in a.provisions.split(",")] if a.provisions else None,
                                    reference=a.reference, break_lock_by=a.by if a.break_lock else None,
                                    allow_unverified_capabilities=a.allow_unverified_capabilities)
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
