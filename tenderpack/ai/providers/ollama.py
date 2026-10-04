"""The local Ollama route: the owner's Mac only (M5 Pro, 48 GB unified memory). Its endpoint is localhost on that Mac
and is never assumed to be reachable from a cloud session.

  * Base URL: config `base_url` (default http://127.0.0.1:11434), overridden by the environment variable named in
    `base_url_env` (default TENDERPACK_OLLAMA_URL). No key.
  * Capabilities come from the endpoint: POST /api/show {model} reports `capabilities` (e.g. completion, vision,
    tools) and the model's context length (model_info "<arch>.context_length"). A task that needs images with a model
    that does not report `vision`, or tool use without `tools`, is REFUSED (never silently degraded). If /api/show
    cannot be reached, live use is refused.
  * Context: `num_ctx` is the configured bound for the model (config models.<role>.num_ctx), never more than the
    model's reported context length; the task packet must fit it or the run is refused before any call.
  * Requests: POST /api/chat with stream false, tools as functions, images as base64 in `images`, tool results as
    role "tool" messages. Usage from prompt_eval_count / eval_count.
  * Candidates in config/ai.yaml are marked "candidate, unmeasured": no performance is claimed until measured on
    the Mac (docs/AI_ROUTES.md gives the measurement protocol).
"""
from __future__ import annotations

import os

from .base import Capabilities, ProviderError, Request, Response, ToolCall, http_json, image_b64, text_of


class OllamaProvider:
    name = "ollama"
    paid = False

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ, fetch=http_json):
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        url_env = rcfg.get("base_url_env") or "TENDERPACK_OLLAMA_URL"
        self.base_url = (env.get(url_env) or rcfg.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
        self._fetch = fetch
        self._caps: Capabilities | None = None
        self.num_ctx: int | None = self.mcfg.get("num_ctx") or rcfg.get("num_ctx")

    def capabilities(self) -> Capabilities:
        if self._caps is not None:
            return self._caps
        try:
            _, _, data = self._fetch("POST", f"{self.base_url}/api/show", {}, {"model": self.model}, 20)
        except ProviderError as e:
            raise ProviderError("capabilities_unavailable",
                                f"Ollama at {self.base_url} could not be reached ({e.kind}): this route runs on the "
                                "owner's Mac only; live use is refused", False) from None
        caps = set(data.get("capabilities") or [])
        info = data.get("model_info") or {}
        ctx = next((int(v) for k, v in info.items() if k.endswith(".context_length") and isinstance(v, (int, float))), None)
        bound = min(x for x in (self.num_ctx, ctx) if x) if (self.num_ctx or ctx) else None
        self.num_ctx = bound
        self._caps = Capabilities(images="vision" in caps, tools="tools" in caps,
                                  structured_output=None, context_tokens=bound,
                                  retention="local: the prompt stays on the machine running Ollama",
                                  source=f"POST {self.base_url}/api/show (capabilities {sorted(caps)}; context "
                                         f"{ctx}; bounded by config num_ctx {self.mcfg.get('num_ctx')})",
                                  details={"reported_context_length": ctx, "details": data.get("details")})
        return self._caps

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
        return body

    def complete(self, request: Request) -> Response:
        _, _, data = http_json("POST", f"{self.base_url}/api/chat", {}, self.body(request), request.timeout_s)
        if data.get("error"):
            raise ProviderError("api_error", str(data["error"])[:300], False)
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
