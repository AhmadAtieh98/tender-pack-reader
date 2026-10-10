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
  routes [--json] [--offline]    (session 12) every route: its kind (connected coding host | hosted API | local
          inference | recorded), what is verified here and what is PENDING ON THE MAC, the configured models and, for
          ollama only, their capabilities checked now against the LOCAL endpoint (installed, vision, tools, context,
          estimated memory). It never calls a hosted endpoint, never starts a host process and never pulls a model.
Session 12: --offline on critic and plan-batches (offline mode, tenderpack/ai/offline.py): a hosted route is refused.
Session 13: `routes` also prints, for each route (host = Claude Code, codex, anthropic, openrouter, ollama), the record of
          where and when it was last exercised and with what result (config/routes_status.yaml) beside its LIVE
          availability here (a command on PATH, a key configured through tenderpack/ai/keys.py, the paid caps set, the
          local Ollama answering) and why it is not usable; `--brief` gives one line per route (the launcher's menu).
          Nothing is called: no hosted endpoint, no host process, no key value shown.
          Session 13, part 4: each row also says where the AI quick review (`ai quick-review`) has been exercised on
          that route (`quick_review`, from tenderpack/ai/quick_review.py ROUTE_STATUS).
  ollama-models [--json] [--offline]   (session 13) the INSTALLED Ollama models (/api/tags), each one's reported
          capabilities and context (/api/show) and its estimated memory against this machine's, and which phase
          (reading, analysis, downstream, critic) each can serve. Never pulls. Exit 0 every phase has a model, 1 Ollama
          answers but some phase has none, 3 Ollama does not answer (checks.sh checks 6 and 7 read these).
Exit codes: 0 done, 1 done with failures (an item the critic could not review; a host session without a submission;
a provision too large), 2 refused before anything ran.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from ..util import ROOT

COMMANDS = ("critic", "host-session", "plan-batches", "routes", "ollama-models")


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
    c.add_argument("--offline", action="store_true", help="offline mode: the local critic (ollama) only")
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
    b.add_argument("--offline", action="store_true", help="offline mode: only the ollama (or recorded) route")
    _common(b)
    r = sub.add_parser("routes", help="every route: kind, what is verified vs pending on the Mac, models, local checks")
    r.add_argument("--json", action="store_true")
    r.add_argument("--brief", action="store_true", help="one line per route: usable now or why not, and its status")
    r.add_argument("--offline", action="store_true")
    r.add_argument("--config", default=str(ROOT / "config/ai.yaml"))
    o = sub.add_parser("ollama-models", help="the installed Ollama models and which phase each can serve (no pull)")
    o.add_argument("--json", action="store_true")
    o.add_argument("--offline", action="store_true")
    o.add_argument("--config", default=str(ROOT / "config/ai.yaml"))


def _ws(a):
    from .tools import Workspace
    return Workspace(Path(a.evidence), Path(a.pack), ROOT, Path(a.out), Path(a.worklog), Path(a.config))


def _print(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def _cfg(a) -> dict:
    from . import config as C
    from .providers.base import ALLOW_UNVERIFIED_KEY
    from .offline import activate, requested
    cfg = C.load(Path(a.config))
    activate(cfg, requested(cfg, getattr(a, "offline", False)))          # session 12
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
        if a.ai_cmd == "routes":
            return _routes(a)
        if a.ai_cmd == "ollama-models":
            return _ollama_models(a)
    except (B.Refused, C.ConfigError, ToolError) as e:
        print(f"REFUSED: {e}", file=sys.stdout)
        return 2
    except ProviderError as e:
        print(f"REFUSED: {e.message}", file=sys.stdout)
        return 2
    return 2


def _critic(a) -> int:
    from . import critic
    from .offline import active
    cfg = _cfg(a)
    if active(cfg) and a.route is None:
        a.route = "ollama"                                           # session 12: offline: the local critic
    caps = {"max_calls": a.max_calls, "max_input_tokens": a.max_input_tokens, "max_output_tokens": a.max_output_tokens,
            "max_usd": a.max_usd}
    res = critic.run(_ws(a), a.run_id, route=a.route, model=a.model, cassette=a.cassette, cfg=cfg,
                     max_items=a.max_items, caps={k: v for k, v in caps.items() if v is not None})
    _print(res)
    return 1 if res["errors"] else 0


def _host_session(a) -> int:
    """One headless host session on the common request path (session 11; tenderpack/ai/requests.py): the host's
    declared capabilities checked (image input when the packet names image targets) and the complete size of the
    prompt (the context bound enforced; the output estimate a notice) before the session starts; the failure classes
    applied to the session (a rate limit backs off and is then reported `deferred`; a CLI failure is retried once). Exit
    codes as before: 0 a submission, 1 none, 2 refused."""
    import time
    from . import requests as R
    from .hostsession import HostSession, host_packet
    from .providers.base import collect_notices
    ws, cfg = _ws(a), _cfg(a)
    provs = [x.strip() for x in a.provisions.split(",")] if a.provisions else None
    pk = R.compact_analysis(host_packet(ws, a.addendum, provs))
    hs = HostSession(ws, cfg, model=a.model, max_turns=a.max_turns, timeout_s=a.timeout_s, claude_bin=a.claude_bin)
    sp = R.spec("analysis", system=hs.system_prompt())
    box, attempts, deferred, failure = {}, [], False, None
    with collect_notices() as notes:
        caps = hs.capabilities()
        n_img = R.packet_images(pk)
        R.require(sp, caps, n_img, "host", hs.host_model_label())
        from .tools import TOOLS
        sz = R.size(sp, caps, hs.prompt(pk), system=hs.system_prompt(), tools_spec=[TOOLS[n].spec() for n in sp.tools],
                    images=n_img, units=len(pk.get("provisions") or []), settings=R.settings_for(cfg, "host"))
        if not R.context_fits(sz):
            R.check_size(sp, sz)                         # the output estimate alone is reported (request_size.why)

        def run():
            box["ps"] = hs.run_batch(pk)
            return hs.last
        try:
            R.call_host(run, R.FailurePolicy.from_cfg(cfg), sleep=time.sleep, record=attempts.append)
        except R.RateLimited as e:
            deferred, failure = True, e.message
        except R.ProviderFailed as e:
            failure = e.message
    ps = box.get("ps") or {}
    r = hs.last
    _print({"session_run": r.run_id, "elapsed_s": r.elapsed_s, "exit_code": r.exit_code, "error": r.error,
            "failure_class": r.failure_class, "deferred": deferred, "failure": failure, "failures": attempts,
            "request_size": sz.to_dict(), "route_notices": list(notes),
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
        prov = make(a.route, C.phase_model(C.route(cfg, a.route), a.route, "analysis", a.model), cfg, a.cassette)
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


VERIFIED = {   # session 14 (W6): the same facts as config/routes_status.yaml (tests/test_session14_routes_status.py)
    "host": ("Claude Code headless sessions (claude -p over the MCP tools) have run for real on the host's own plan in "
             "the cloud container (sessions 10-13, blind rehearsals 03-07; the sealed blind-07 run from a twin of the "
             "interview folder); PENDING ON THE MAC. The MCP server is tested (stdio JSON-RPC); MCP interface "
             "tested; automated Codex execution unverified (no Codex session has run; the workflow starts Claude "
             "Code only, Codex is the manual MCP / submit-batch path)"),
    "anthropic": "untested: recorded responses only (tests); no API-key call has been made from this project's "
                 "environment",
    "openrouter": "blocked here, unverified: recorded responses only (tests); openrouter.ai is blocked from the cloud "
                  "environment; keys later",
    "ollama": ("prepared for local use; tested here with a fake local server and recorded answers "
               "(tests/test_session12_offline.py, tests/test_session14_mac_levels.py); a real local model: PENDING ON "
               "THE MAC (docs/MAC_CHECKLIST.md, scripts/mac/checks.sh)"),
    "recorded": "test replay of hand-written cassettes; not a live integration",
}


def _routes(a) -> int:
    """`tenderpack ai routes` (session 12): see the module docstring."""
    from . import config as C
    from .hostsession import declared_capabilities
    from .offline import KINDS, active
    cfg = _cfg(a)
    off = active(cfg)
    rows = []
    for name in ("host", "anthropic", "openrouter", "ollama", "recorded"):
        if name not in cfg["routes"]:
            continue
        rc = C.route(cfg, name)
        row = {"route": name, "kind": KINDS[name], "paid": rc.get("paid"), "verified": VERIFIED[name]}
        if name == "host":
            hs = cfg.get("host_session") or {}
            row["models"] = [{"role": "host_session", "id": hs.get("model") or "the CLI's default (as it reports it)"}]
            row["capabilities"] = {k: v for k, v in declared_capabilities(cfg).to_dict().items()
                                   if k in ("images", "tools", "context_tokens", "max_output_tokens", "source")}
        elif name != "recorded":
            row["models"] = [{"role": r, "id": v.get("id") if isinstance(v, dict) else v,
                              "status": v.get("status") if isinstance(v, dict) else None}
                             for r, v in (rc.get("models") or {}).items()]
        if off and name in ("host", "anthropic", "openrouter"):
            row["checked"] = "disabled in offline mode (refused before any call)"
        elif name == "host":
            row["checked"] = "not checked by this command (it would start a host process); capabilities are declared"
        elif name in ("anthropic", "openrouter"):
            row["checked"] = (f"not checked by this command (it would call a hosted endpoint); `tenderpack ai "
                              f"capabilities --route {name} --model M` checks it live")
        elif name == "ollama":
            from .providers.ollama import check_models
            rep = check_models(cfg)
            row.update(checked=f"checked now against {rep['base_url']} (local; nothing pulled)",
                       reachable=rep["reachable"], installed=rep["installed"], models=rep["models"],
                       machine=rc.get("machine"))
            if rep.get("error"):
                row["error"] = rep["error"] + " (expected in the cloud: the owner's Mac only)"
        else:
            row["checked"] = "nothing to check (a cassette per test)"
        rows.append(row)
    rows.insert(1, {"route": "codex", "kind": "connected coding host (manual path over MCP)", "paid": False,
                    "verified": "MCP interface tested; no Codex session has run (docs/AI_ROUTES.md section 3)",
                    "checked": "not checked by this command (it would start a process); `codex` looked up on PATH"})
    status = route_status(Path(a.config).parent / "routes_status.yaml")
    from .quick_review import ROUTE_STATUS as QR_STATUS     # session 13, part 4: where the quick review has run
    for row in rows:
        row["status"] = status.get(row["route"]) or {"status": "no record", "where": "-", "when": "-",
                                                     "result": "config/routes_status.yaml has no entry", "next": "-"}
        row["available"], row["why"] = availability(row, cfg, off)
        row["quick_review"] = QR_STATUS.get(row["route"], "no record")
        for k in ("works", "never_run", "ready"):              # session 14 (W6): what works, what never ran, what
            if row["status"].get(k):                           # is ready to try (config/routes_status.yaml)
                row[k] = row["status"][k]
    driver = (cfg.get("host_session") or {}).get("driver", "claude")
    if driver == "codex":
        for row in rows:
            if row["route"] == "host":
                row.update(kind="connected coding host (Codex exec)",
                           verified="Codex driver configured; current run results and local smoke records are separate evidence")
                row["status"] = {"status": "configured", "where": "this operating copy"}
            elif row["route"] == "codex":
                row.update(verified="Automated Codex is selected through the host route in this configuration",
                           why="Choose host: Codex; this legacy manual route is not a separate workflow route")
    out = {"offline": cfg.get("_offline") if off else None, "routes": rows, "host_driver": driver,
           "note": "kinds: connected coding host (Claude Code / Codex with their own model, over MCP or the CLI) | "
                   "hosted API (the application's paid calls) | local inference (Ollama on this machine) | recorded "
                   "(tests). Every route goes through the same request layer and the controller's validation."}
    if a.json:
        _print(out)
        return 0
    if getattr(a, "brief", False):
        print(f"AI routes ({'offline mode: only the local ollama route' if off else 'connected: Claude Code first'}):")
        for r in rows:
            if r["route"] == "recorded":
                continue
            st = r["status"]
            print(f"  {r['route']:<11} {'usable now' if r['available'] else 'not usable now: ' + r['why']}")
            print(f"  {'':<11} [{st.get('status')}; last exercised: {st.get('where')}, {st.get('when')}]")
        return 0
    print(f"AI routes ({'offline mode: ' + str(out['offline']) if off else 'offline mode off'})")
    for r in rows:
        st = r["status"]
        print(f"\n{r['route']}: {r['kind']}{' (paid)' if r.get('paid') else ''}")
        print(f"  usable now: {'yes' if r['available'] else 'no: ' + r['why']}")
        print(f"  status:   {st.get('status')} (last exercised: {st.get('where')}, {st.get('when')}: "
              f"{' '.join(str(st.get('result')).split())})")
        if not r["available"] and st.get("next") not in (None, "-"):
            print(f"  next:     {' '.join(str(st.get('next')).split())}")
        if r.get("works"):                                     # session 14 (W6)
            print(f"  works:    {r['works']}")
        if r.get("never_run"):
            print(f"  never run: {r['never_run']}")
        if r.get("ready"):
            print(f"  ready:    {r['ready']}")
        print(f"  verified: {r['verified']}")
        print(f"  quick review: {r['quick_review']}")
        print(f"  checked:  {r['checked']}")
        if r.get("error"):
            print(f"  error:    {r['error']}")
        if r.get("installed") is not None:
            print(f"  installed: {', '.join(r['installed']) or 'none'}")
        for m in r.get("models") or []:
            bits = [f"{m.get('role')}: {m.get('id')}"]
            if r["route"] == "ollama":
                if m.get("ok"):
                    mem = m.get("memory") or {}
                    bits.append(f"vision={m.get('images')} tools={m.get('tools')} context={m.get('context_tokens')} "
                                f"memory~{mem.get('total_gb')} GB of ~{mem.get('budget_gb')} GB")
                else:
                    bits.append(f"NOT USABLE: {m.get('problem')}")
            elif m.get("status"):
                bits.append(str(m["status"]))
            print("  - " + "; ".join(bits))
        if r.get("capabilities"):
            c = r["capabilities"]
            print(f"  declared capabilities: images={c.get('images')} tools={c.get('tools')} "
                  f"context={c.get('context_tokens')}")
    print("\n" + out["note"])
    return 0


def route_status(path: Path) -> dict:
    """config/routes_status.yaml (session 13): {route: {status, where, when, result, next, label}}; {} when absent."""
    import yaml
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    return {k: {kk: (" ".join(str(vv).split()) if isinstance(vv, str) else vv) for kk, vv in (v or {}).items()}
            for k, v in (data.get("routes") or {}).items()}


def availability(row: dict, cfg: dict, offline: bool) -> tuple[bool, str]:
    """(usable now, why not) for a routes row, from local facts only: offline mode, a command on PATH, a key configured
    (tenderpack/ai/keys.py, never its value), the paid caps set, the local Ollama's answer. Nothing is called."""
    import shutil
    from . import config as C
    from . import keys
    name = row["route"]
    if name == "recorded":
        return False, "tests only (a cassette replay, not a live model)"
    if offline and name in ("host", "codex", "anthropic", "openrouter"):
        return False, "offline mode is on: only the local ollama route (switch to connected to use it)"
    if name == "host":
        hs = cfg.get("host_session") or {}
        if hs.get("driver") == "codex":
            from .codex import discover
            try:
                return True, f"Codex CLI found at {discover(hs.get('codex_bin'))}; uses the signed-in account"
            except FileNotFoundError as e:
                return False, str(e)
        binary = (cfg.get("host_session") or {}).get("claude_bin") or "claude"
        found = shutil.which(binary)
        return (True, f"{binary} found at {found}") if found else (
            False, f"the {binary} command is not on PATH: install Claude Code and sign in (or use the manual path, "
                   "tenderpack ai submit-batch)")
    if name == "codex":
        found = shutil.which("codex")
        return False, ("the workflow starts Claude Code only; Codex is used by hand over the MCP server "
                       "(docs/AI_ROUTES.md section 3) and has never run here" + (f"; codex found at {found}" if found
                                                                                 else "; codex is not on PATH"))
    if name in ("anthropic", "openrouter"):
        rc = C.route(cfg, name)
        ok, why = keys.status(rc.get("api_key_env") or ("ANTHROPIC_API_KEY" if name == "anthropic"
                                                        else "OPENROUTER_API_KEY"))
        if not ok:
            return False, why
        caps = rc.get("caps") or {}
        unset = [k for k in ("max_calls", "max_input_tokens", "max_output_tokens", "max_usd") if caps.get(k) is None]
        if rc.get("paid") and unset:
            return False, (f"{why}; but the paid caps routes.{name}.caps {', '.join(unset)} are not set in "
                           "config/ai.yaml (a paid route refuses to start until the owner sets them)")
        return True, why
    if name == "ollama":
        usable = [m.get("id") for m in row.get("models") or [] if m.get("ok")]
        if usable:
            return True, f"usable configured model(s): {', '.join(usable)}"
        return False, (row.get("error") or "no configured model is installed and usable") + \
            " (tenderpack ai ollama-models lists what is installed; nothing is pulled)"
    return False, "unknown route"


def _ollama_models(a) -> int:
    """`tenderpack ai ollama-models` (session 13): see the module docstring."""
    from .providers.ollama import PHASE_NEEDS, discover
    cfg = _cfg(a)
    rep = discover(cfg)
    code = 3 if not rep["reachable"] else (0 if all(rep["phases"][p] for p in PHASE_NEEDS) else 1)
    rep["exit_code"] = code
    if a.json:
        _print(rep)
        return code
    m = rep["machine"]
    print(f"Ollama at {rep['base_url']}: {'answers' if rep['reachable'] else 'does not answer'}; machine memory "
          f"{m.get('memory_gb')} GB x {m.get('usable_fraction')} usable = {m.get('budget_gb')} GB ({m.get('source')})")
    if not rep["reachable"]:
        print(f"  {rep['error']}")
        print("  start the Ollama app (or `ollama serve`) and run again; nothing is downloaded by tenderpack")
        return code
    if not rep["models"]:
        print("  no model is installed (tenderpack never pulls one; `ollama pull <model>` is your decision)")
    for x in rep["models"]:
        roles = f" (configured as {', '.join(x['roles'])})" if x.get("roles") else ""
        mem = x.get("memory") or {}
        print(f"\n{x['id']}{roles}: {x.get('size_gb')} GB on disk; capabilities {', '.join(x.get('capabilities') or [])}"
              f"; context {x.get('context_tokens')}; memory ~{mem.get('total_gb')} GB "
              f"({'fits' if mem.get('fits') else 'does NOT fit' if mem.get('fits') is False else 'not estimated'})")
        if x.get("problem"):
            print(f"  {x['problem']}")
        for ph, v in (x.get("phases") or {}).items():
            print(f"  {ph:<11} {'can serve' if v['ok'] else 'cannot'}: {v['why']}")
    print("\nper phase: " + "; ".join(f"{p}: {', '.join(v) or 'NO installed model'}" for p, v in rep["phases"].items()))
    print("configured (config/ai.yaml routes.ollama.models): " +
          ", ".join(f"{r} = {i}" for r, i in rep["configured"].items()))
    print(rep["note"])
    return code


def main(argv=None) -> int:
    """`python -m tenderpack.ai.cli_routes COMMAND ...` (the same commands, before they are wired into `tenderpack ai`)."""
    import argparse
    ap = argparse.ArgumentParser(prog="tenderpack.ai.cli_routes")
    add_subcommands(ap.add_subparsers(dest="ai_cmd", required=True))
    return handle(ap.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
