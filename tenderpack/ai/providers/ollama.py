"""The local Ollama route: the owner's Mac only (M5 Pro, 48 GB unified memory). Its endpoint is localhost on that Mac
and is never assumed to be reachable from a cloud session.

  * Base URL: config `base_url` (default http://127.0.0.1:11434), overridden by the environment variable named in
    `base_url_env` (default TENDERPACK_OLLAMA_URL). No key.
  * Capabilities come from the endpoint: POST /api/show {model} reports `capabilities` (e.g. completion, vision,
    tools) and the model's context length (model_info "<arch>.context_length"). A task that needs images with a model
    that does not report `vision`, or tool use without `tools`, is REFUSED (never silently degraded). If /api/show
    cannot be reached, live use is refused.
  * Context: `num_ctx` is the configured bound for the model (config models.<role>.num_ctx), never more than the
    model's reported context length; the task packet must fit it or the run is refused before any call. Session 10:
    when /api/show reports no context length, the bound cannot be checked and live use is REFUSED ("capabilities
    unverified"); --allow-unverified-capabilities uses the configured num_ctx, marked unverified, logged and shown in
    the review request.
  * Native structured outputs (session 10): `format: <JSON schema>` on /api/chat (Ollama's structured-output request
    field; a server feature, not reported by /api/show, so it is used as configured and NOT verified from this
    environment). Sent when a request carries `response_schema` and routes.ollama.structured_output.mode is `native`,
    and, on a request that also offers tools, only when `with_tools` is true: a format grammar may stop a model from
    emitting tool calls, which is to be checked on the Mac before turning it on. A rejected schema switches the run to
    the plain path with a route notice. The controller parses and validates the answer locally either way.
  * Requests: POST /api/chat with stream false, tools as functions, images as base64 in `images`, tool results as
    role "tool" messages. Usage from prompt_eval_count / eval_count.
  * Candidates in config/ai.yaml are marked "candidate, unmeasured": no performance is claimed until measured on
    the Mac (docs/AI_ROUTES.md gives the measurement protocol).
  * Session 12 (offline mode, tenderpack/ai/offline.py): a model /api/show does not know (404) is NOT INSTALLED: the
    error names the model, the command a person may run (`ollama pull X`; tenderpack never pulls) and the installed
    models (GET /api/tags). Image input and tool use are taken ONLY from the reported `capabilities` (never assumed).
    The memory a model needs at its context bound is ESTIMATED from /api/show (parameter size x the quantisation's
    bits per weight, plus the KV cache: layers x KV heads x (key + value length) x 2 bytes x num_ctx, plus 1 GB) and
    compared with `routes.ollama.machine` (unified_memory_gb x usable_fraction, an assumption about macOS's GPU
    working-set limit, not measured): a model that cannot hold its context is REFUSED with the numbers; without a
    parameter size or a quantisation the estimate is "unknown" (recorded with the capabilities, not a refusal). `check_models(cfg)`
    reports every configured model this way (`tenderpack ai routes`, the workflow's preflight). A loopback base URL is
    always reached directly, never through an HTTP proxy.
"""
from __future__ import annotations

import os
import re

from . import structured as SO
from .base import (ALLOW_UNVERIFIED_KEY, Capabilities, ProviderError, Request, Response, ToolCall, http_json, image_b64,
                   notice, text_of, unverified)


class OllamaProvider:
    name = "ollama"
    paid = False

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ, fetch=http_json,
                 allow_unverified: bool = False):
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        url_env = rcfg.get("base_url_env") or "TENDERPACK_OLLAMA_URL"
        self.base_url = (env.get(url_env) or rcfg.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
        self._fetch = fetch
        self._caps: Capabilities | None = None
        self.num_ctx: int | None = self.mcfg.get("num_ctx") or rcfg.get("num_ctx")
        self.allow_unverified = bool(allow_unverified or rcfg.get(ALLOW_UNVERIFIED_KEY))
        so = rcfg.get("structured_output") or {}
        self.structured_mode = str(so.get("mode", "native"))
        self.structured_with_tools = bool(so.get("with_tools", False))
        self._plain_reason: str | None = None
        self.format_sent = False

    def capabilities(self) -> Capabilities:
        if self._caps is not None:
            return self._caps
        try:
            _, _, data = self._fetch("POST", f"{self.base_url}/api/show", {}, {"model": self.model}, 20)
        except ProviderError as e:
            if e.status == 404 or "not found" in str(e.message).lower():
                raise ProviderError("model_not_installed", not_installed_message(self.model, self._installed()),
                                    False, 404) from None
            raise ProviderError("capabilities_unavailable",
                                f"Ollama at {self.base_url} could not be reached ({e.kind}): this route runs on the "
                                "owner's Mac only; live use is refused", False) from None
        caps = set(data.get("capabilities") or [])
        info = data.get("model_info") or {}
        ctx = next((int(v) for k, v in info.items() if k.endswith(".context_length") and isinstance(v, (int, float))), None)
        retention = "local: the prompt stays on the machine running Ollama"
        if ctx is None:
            conf = Capabilities(images="vision" in caps, tools="tools" in caps, structured_output=None,
                                context_tokens=self.num_ctx, retention=retention, source="config num_ctx",
                                details={"reported_context_length": None, "details": data.get("details")})
            self._caps = unverified("ollama", self.model, "/api/show reports no context length, so the configured "
                                    f"num_ctx {self.num_ctx} cannot be checked against the model",
                                    conf if self.num_ctx else None, self.allow_unverified)
            return self._caps
        bound = min(x for x in (self.num_ctx, ctx) if x)
        self.num_ctx = bound
        mem = memory_estimate(data, bound, self.rcfg.get("machine"))
        if mem.get("fits") is False:
            raise ProviderError("memory", f"ollama {self.model}: {mem['why']}; refused before any request (lower "
                                          "num_ctx in config/ai.yaml or choose a smaller model)", False)
        self._caps = Capabilities(images="vision" in caps, tools="tools" in caps,
                                  structured_output=None, context_tokens=bound,
                                  retention=retention,
                                  source=f"POST {self.base_url}/api/show (capabilities {sorted(caps)}; context "
                                         f"{ctx}; bounded by config num_ctx {self.mcfg.get('num_ctx')})",
                                  details={"reported_context_length": ctx, "details": data.get("details"),
                                           "reported_capabilities": sorted(caps), "memory": mem})
        return self._caps

    def _installed(self) -> list[str] | None:
        try:
            _, _, tags = self._fetch("GET", f"{self.base_url}/api/tags", {}, None, 20)
        except ProviderError:
            return None
        return sorted(m.get("name") or m.get("model") for m in (tags or {}).get("models") or [])

    def native_format(self, request: Request) -> dict | None:
        if request.response_schema is None:
            return None
        why = self._plain_reason
        if why is None and self.structured_mode != "native":
            why = f"routes.ollama.structured_output.mode is {self.structured_mode!r}"
        if why is None and request.tools and not self.structured_with_tools:
            # a tool-use turn: `format` is withheld (with_tools false; see the module docstring). Session 11: said, once
            notice("structured_output_withheld", "native structured output withheld on turns that offer tools "
                                                 "(routes.ollama.structured_output.with_tools is false until checked on "
                                                 "the Mac); the answer is parsed and validated locally from text",
                   route="ollama", model=self.model)
            return None
        if why is None:
            try:
                return SO.for_provider(request.response_schema, "ollama")
            except SO.SchemaUnsupported as e:
                why = f"the proposal-set schema cannot be expressed ({e})"
        if self._plain_reason is None:
            self._plain_reason = why
            notice("structured_output_not_used", f"native structured output not used ({why}); the answer is parsed and "
                                                 "validated locally from text", route="ollama", model=self.model)
        return None

    def body(self, request: Request) -> dict:
        msgs = [{"role": "system", "content": request.system}]
        for m in request.messages:
            if m["role"] == "user":
                msg = {"role": "user", "content": text_of(m["content"])}
                imgs = [image_b64(p) for p in m["content"] if p["type"] == "image"]
                if imgs:
                    msg["images"] = imgs
                msgs.append(msg)
            elif m["role"] == "assistant":
                msg = {"role": "assistant", "content": text_of(m["content"])}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [{"function": {"name": c["name"], "arguments": c["arguments"]}}
                                         for c in m["tool_calls"]]
                msgs.append(msg)
            elif m["role"] == "tool":
                imgs = []
                for r in m["results"]:
                    msgs.append({"role": "tool", "content": r["content"], "tool_name": r["name"]})
                    imgs += [image_b64(im) for im in r.get("images") or []]
                if imgs:
                    msgs.append({"role": "user", "content": "images returned by the tool calls above", "images": imgs})
        options = {"num_predict": request.max_tokens}
        if self.num_ctx:
            options["num_ctx"] = int(self.num_ctx)
        body = {"model": self.model, "messages": msgs, "stream": False, "options": options}
        if request.tools:
            body["tools"] = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                               "parameters": t["input_schema"]}} for t in request.tools]
        fmt = self.native_format(request)
        self.format_sent = fmt is not None
        if fmt is not None:
            body["format"] = fmt
        return body

    def _rejected(self, e: ProviderError) -> ProviderError:
        self._plain_reason = f"the endpoint rejected the structured-output schema ({e.kind}: {e.message[:200]})"
        notice("structured_output_rejected", f"{self._plain_reason}; the run continued on the plain tool-use path "
                                             "(answer parsed and validated locally)", route="ollama", model=self.model)
        return ProviderError("structured_output_rejected", self._plain_reason, True, e.status, 0.0)

    def complete(self, request: Request) -> Response:
        try:
            _, _, data = http_json("POST", f"{self.base_url}/api/chat", {}, self.body(request), request.timeout_s)
        except ProviderError as e:
            if self.format_sent and SO.is_schema_rejection(e):
                raise self._rejected(e) from None
            raise
        if data.get("error"):
            pe = ProviderError("api_error", str(data["error"])[:300], False)
            if self.format_sent and SO.is_schema_rejection(pe):
                raise self._rejected(pe)
            raise pe
        msg = data.get("message") or {}
        calls = [ToolCall(f"call_{i}", (c.get("function") or {}).get("name", ""),
                          (c.get("function") or {}).get("arguments") or {}) for i, c in enumerate(msg.get("tool_calls") or [])]
        return Response(text=msg.get("content") or "", tool_calls=calls,
                        usage={"input_tokens": int(data.get("prompt_eval_count") or 0),
                               "output_tokens": int(data.get("eval_count") or 0),
                               "detail": {k: data.get(k) for k in ("total_duration", "load_duration", "prompt_eval_duration",
                                                                   "eval_duration") if k in data}},
                        model_reported=data.get("model"), raw={k: v for k, v in data.items() if k != "context"},
                        stop_reason=data.get("done_reason"))


# ---------------------------------------------------------------------------------------------- session 12: local checks

BITS_PER_WEIGHT = {"Q2_K": 3.35, "Q3_K_S": 3.5, "Q3_K_M": 3.9, "Q3_K_L": 4.3, "Q4_0": 4.55, "Q4_1": 5.0,
                   "Q4_K_S": 4.6, "Q4_K_M": 4.85, "Q5_0": 5.5, "Q5_1": 6.0, "Q5_K_S": 5.55, "Q5_K_M": 5.7,
                   "Q6_K": 6.6, "Q8_0": 8.5, "F16": 16.0, "BF16": 16.0, "F32": 32.0, "MXFP4": 4.25}
OVERHEAD_GB = 1.0
GB = 1024 ** 3


def not_installed_message(model: str, installed: list[str] | None) -> str:
    have = ", ".join(installed) if installed else ("none" if installed is not None else "the list could not be read")
    return (f"model {model} is not installed; install it yourself with `ollama pull {model}` if you want it "
            f"(installed: {have}); tenderpack never downloads a model")


def _params(s) -> float | None:
    m = re.match(r"^\s*([\d.]+)\s*([KMBT]?)", str(s or ""), re.I)
    if not m:
        return None
    return float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[m.group(2).upper()]


def _info(info: dict, suffix: str):
    v = next((v for k, v in info.items() if k.endswith("." + suffix)), None)
    if isinstance(v, list):
        v = max((x for x in v if isinstance(x, (int, float))), default=None)
    return v if isinstance(v, (int, float)) else None


def machine_budget_gb(machine: dict | None) -> tuple[float | None, str]:
    m = machine or {}
    if not m.get("unified_memory_gb"):
        return None, "no routes.ollama.machine.unified_memory_gb configured"
    frac = float(m.get("usable_fraction", 0.75))
    return float(m["unified_memory_gb"]) * frac, (f"{m['unified_memory_gb']:g} GB unified memory x {frac:g} usable "
                                                  "(an assumption about macOS's GPU working-set limit; not measured)")


def memory_estimate(show: dict, num_ctx: int | None, machine: dict | None = None) -> dict:
    """An ESTIMATE of the memory a model needs at `num_ctx` from its /api/show reply (see the module docstring), and
    whether it fits the configured machine: {weights_gb, kv_cache_gb, overhead_gb, total_gb, budget_gb, fits, why,
    max_ctx_that_fits}. fits None: not estimated (and why)."""
    det = (show or {}).get("details") or {}
    info = (show or {}).get("model_info") or {}
    params, quant = _params(det.get("parameter_size")), str(det.get("quantization_level") or "").upper()
    bits = BITS_PER_WEIGHT.get(quant)
    budget, basis = machine_budget_gb(machine)
    out = {"parameter_size": det.get("parameter_size"), "quantization": det.get("quantization_level"),
           "num_ctx": num_ctx, "budget_gb": round(budget, 1) if budget else None, "budget_basis": basis,
           "basis": "an estimate from /api/show (weights + f16 KV cache + 1 GB overhead), not a measurement"}
    if params is None or bits is None:
        return {**out, "fits": None, "why": f"memory need not estimated (parameter size {det.get('parameter_size')!r}, "
                                            f"quantisation {det.get('quantization_level')!r} not both known)"}
    weights = params * bits / 8 / GB
    layers, kvh = _info(info, "block_count"), _info(info, "attention.head_count_kv")
    kl, vl = _info(info, "attention.key_length"), _info(info, "attention.value_length")
    if kl is None and _info(info, "embedding_length") and _info(info, "attention.head_count"):
        kl = vl = _info(info, "embedding_length") / _info(info, "attention.head_count")
    per_token = (layers * (kvh or 1) * ((kl or 0) + (vl or kl or 0)) * 2) if layers and kl else None
    kv = per_token * (num_ctx or 0) / GB if per_token else None
    total = weights + (kv or 0) + OVERHEAD_GB
    out.update(weights_gb=round(weights, 1), kv_cache_gb=round(kv, 1) if kv is not None else None,
               overhead_gb=OVERHEAD_GB, total_gb=round(total, 1))
    if budget is None:
        return {**out, "fits": None, "why": f"about {total:.1f} GB at num_ctx {num_ctx} (estimate); {basis}"}
    if per_token:
        out["max_ctx_that_fits"] = max(0, int((budget - weights - OVERHEAD_GB) * GB / per_token))
    kvs = f"KV cache {kv:.1f} GB" if kv is not None else "KV cache not estimated (no layer/head figures)"
    if total > budget:
        return {**out, "fits": False,
                "why": f"estimated memory {total:.1f} GB at num_ctx {num_ctx} (weights {weights:.1f} GB at "
                       f"{det.get('quantization_level')}, {kvs}, overhead {OVERHEAD_GB:g} GB) exceeds about "
                       f"{budget:.1f} GB ({basis})"}
    return {**out, "fits": True, "why": f"estimated {total:.1f} GB of about {budget:.1f} GB ({kvs})"}


def check_models(cfg: dict, roles: list[str] | None = None, env=os.environ, fetch=None) -> dict:
    """Every configured Ollama model (or `roles`), checked against the local endpoint: installed (/api/tags),
    capabilities as REPORTED (vision, tools), context bound, estimated memory. Never pulls. Returns {base_url,
    reachable, installed, models: [{role, id, installed, images, tools, context_tokens, memory, ok, problem}]}."""
    from .. import config as C
    rcfg = C.route(cfg, "ollama")
    url_env = rcfg.get("base_url_env") or "TENDERPACK_OLLAMA_URL"
    base = (env.get(url_env) or rcfg.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
    fetch = fetch or http_json
    out = {"base_url": base, "reachable": False, "installed": None, "models": []}
    try:
        _, _, tags = fetch("GET", f"{base}/api/tags", {}, None, 20)
        out["reachable"] = True
        out["installed"] = sorted(m.get("name") or m.get("model") for m in (tags or {}).get("models") or [])
    except ProviderError as e:
        out["error"] = f"Ollama at {base} could not be reached ({e.kind}: {str(e.message)[:200]})"
    for role, v in (rcfg.get("models") or {}).items():
        if roles and role not in roles:
            continue
        mid = v.get("id") if isinstance(v, dict) else v
        rec = {"role": role, "id": mid, "status": v.get("status") if isinstance(v, dict) else None}
        if not out["reachable"]:
            rec.update(ok=False, installed=None, problem=out["error"])
        elif mid not in (out["installed"] or []):
            rec.update(ok=False, installed=False, problem=not_installed_message(mid, out["installed"]))
        else:
            prov = OllamaProvider(mid, rcfg, v if isinstance(v, dict) else {}, env=env, fetch=fetch)
            try:
                caps = prov.capabilities()
                rec.update(ok=True, installed=True, images=caps.images, tools=caps.tools,
                           context_tokens=caps.context_tokens,
                           reported_context=caps.details.get("reported_context_length"),
                           capabilities=caps.details.get("reported_capabilities"), memory=caps.details.get("memory"))
            except ProviderError as e:
                rec.update(ok=False, installed=True, problem=e.message)
                try:
                    _, _, data = fetch("POST", f"{base}/api/show", {}, {"model": mid}, 20)
                    caps_ = set(data.get("capabilities") or [])
                    rec.update(images="vision" in caps_, tools="tools" in caps_, capabilities=sorted(caps_),
                               memory=memory_estimate(data, prov.num_ctx, rcfg.get("machine")))
                except ProviderError:
                    pass
        out["models"].append(rec)
    return out


# ---------------------------------------------------------------------------------------------- session 13: discovery

# What each workflow phase asks of a local model (tenderpack/ai/requests.py spec(): the tools it offers, image input)
PHASE_NEEDS = {"reading": {"vision": True, "tools": True, "role": "vision"},
               "analysis": {"vision": False, "tools": True, "role": "text"},
               "downstream": {"vision": False, "tools": True, "role": "text"},
               "critic": {"vision": False, "tools": False, "role": "critic"}}
DEFAULT_NUM_CTX = 32768


def machine_memory_bytes() -> int | None:
    """This machine's physical memory (macOS and Linux: sysconf), or None."""
    try:
        return int(os.sysconf("SC_PAGE_SIZE")) * int(os.sysconf("SC_PHYS_PAGES"))
    except (ValueError, OSError, AttributeError):
        return None


def _role_ctx(rcfg: dict, role: str) -> int:
    v = (rcfg.get("models") or {}).get(role)
    if role == "text" and not v:
        v = (rcfg.get("models") or {}).get("propose")
    return int((v.get("num_ctx") if isinstance(v, dict) else None) or rcfg.get("num_ctx") or DEFAULT_NUM_CTX)


def discover(cfg: dict, env=os.environ, fetch=None, memory_bytes: int | None = None) -> dict:
    """Every INSTALLED Ollama model (GET /api/tags), each one's reported capabilities and context (POST /api/show), its
    estimated memory at the phase's configured context bound compared with this machine's memory, and which phase it
    can serve. Never pulls, never chats. Returns {base_url, reachable, error, machine, models: [{id, size_gb,
    capabilities, context_tokens, memory, phases: {phase: {ok, why}}}], phases: {phase: [model ids that can serve it]},
    configured: {role: id}}."""
    from .. import config as C
    rcfg = C.route(cfg, "ollama")
    url_env = rcfg.get("base_url_env") or "TENDERPACK_OLLAMA_URL"
    base = (env.get(url_env) or rcfg.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
    fetch = fetch or http_json
    mach = dict(rcfg.get("machine") or {})
    frac = float(mach.get("usable_fraction", 0.75))
    mem = memory_bytes if memory_bytes is not None else machine_memory_bytes()
    if mem:
        gb = round(mem / GB, 1)
        machine = {"memory_gb": gb, "usable_fraction": frac, "budget_gb": round(gb * frac, 1),
                   "source": "detected on this machine (sysconf)" if memory_bytes is None else
                   "detected (given by the caller)"}
        mach_for_est = {"unified_memory_gb": gb, "usable_fraction": frac}
    else:
        machine = {"memory_gb": mach.get("unified_memory_gb"), "usable_fraction": frac,
                   "budget_gb": round(float(mach["unified_memory_gb"]) * frac, 1) if mach.get("unified_memory_gb") else None,
                   "source": "config routes.ollama.machine (this machine's memory could not be read)"}
        mach_for_est = mach
    configured = {r: (v.get("id") if isinstance(v, dict) else v) for r, v in (rcfg.get("models") or {}).items()}
    out = {"base_url": base, "reachable": False, "error": None, "machine": machine, "models": [],
           "phases": {p: [] for p in PHASE_NEEDS}, "configured": configured,
           "note": "installed models only; nothing is pulled. Memory is an ESTIMATE from /api/show, not a measurement"}
    try:
        _, _, tags = fetch("GET", f"{base}/api/tags", {}, None, 20)
    except ProviderError as e:
        out["error"] = f"Ollama at {base} could not be reached ({e.kind}: {str(e.message)[:200]})"
        return out
    out["reachable"] = True
    for t in sorted((tags or {}).get("models") or [], key=lambda m: m.get("name") or m.get("model") or ""):
        mid = t.get("name") or t.get("model")
        rec = {"id": mid, "size_gb": round(t["size"] / GB, 1) if isinstance(t.get("size"), (int, float)) else None,
               "roles": sorted(r for r, v in configured.items() if v == mid)}
        try:
            _, _, show = fetch("POST", f"{base}/api/show", {}, {"model": mid}, 20)
        except ProviderError as e:
            rec.update(problem=f"/api/show failed ({e.kind}): {str(e.message)[:200]}",
                       phases={p: {"ok": False, "why": "capabilities could not be read"} for p in PHASE_NEEDS})
            out["models"].append(rec)
            continue
        caps = set(show.get("capabilities") or [])
        info = show.get("model_info") or {}
        ctx = next((int(v) for k, v in info.items() if k.endswith(".context_length") and isinstance(v, (int, float))),
                   None)
        rec.update(capabilities=sorted(caps), context_tokens=ctx, details=show.get("details"))
        phases, mems = {}, {}
        for phase, need in PHASE_NEEDS.items():
            want = _role_ctx(rcfg, need["role"])
            bound = min(x for x in (want, ctx) if x) if ctx else want
            if bound not in mems:
                mems[bound] = memory_estimate(show, bound, mach_for_est)
            m = mems[bound]
            why = []
            if need["vision"] and "vision" not in caps:
                why.append("no vision (image input) reported; the reading phase reads images")
            if need["tools"] and "tools" not in caps:
                why.append(f"no tool use reported; the {phase} phase offers tools")
            if ctx is None:
                why.append("no context length reported (capabilities unverified)")
            elif ctx < want:
                why.append(f"context {ctx} < the configured num_ctx {want} for this phase (config/ai.yaml)")
            if m.get("fits") is False:
                why.append(f"memory: {m['why']}")
            ok = not why
            phases[phase] = {"ok": ok, "why": "; ".join(why) if why else
                             f"vision={'vision' in caps} tools={'tools' in caps} context {ctx}, num_ctx {bound}; "
                             f"{m.get('why')}"}
            if ok:
                out["phases"][phase].append(mid)
        rec["memory"] = mems.get(_role_ctx(rcfg, "text")) or next(iter(mems.values()))
        rec["phases"] = phases
        out["models"].append(rec)
    return out
