"""The OpenRouter route (an application making paid API calls through an OpenAI-compatible endpoint), over urllib.

  * The key comes from the environment only (`api_key_env`, default OPENROUTER_API_KEY).
  * Capabilities come from the endpoint, not from config: GET {base_url}/models is fetched once per run (cached on
    the adapter) and the model's entry gives input modalities (images), supported parameters (tools,
    structured_outputs / response_format) and the context length. If the listing cannot be reached, or does not list
    the model, live use is REFUSED with a clear message; there is no fallback to declared values or to another
    model. (This cloud environment's network policy blocks openrouter.ai, so the route is untested live here.)
  * Requests: POST {base_url}/chat/completions with tools as functions; images as data: URLs in user content (a tool
    result's image is sent in a user message after the tool messages, as the chat format has no image tool results).
  * Retention and provider routing are OpenRouter's and the upstream provider's policies; they are not verified here.
  * Listing prices are reported as data but never used for cost: cost comes only from config/ai.yaml `prices`.
"""
from __future__ import annotations

import json
import os

from .base import Capabilities, ProviderError, Request, Response, ToolCall, http_json, image_b64, text_of


class OpenRouterProvider:
    name = "openrouter"
    paid = True

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ, fetch=http_json):
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        self.base_url = (rcfg.get("base_url") or "https://openrouter.ai/api/v1").rstrip("/")
        self.key_env = rcfg.get("api_key_env") or "OPENROUTER_API_KEY"
        self._key = env.get(self.key_env)
        self._fetch = fetch
        self._listing: dict | None = None

    def _headers(self) -> dict:
        if not self._key:
            raise ProviderError("no_credentials", f"set {self.key_env} in the environment to use this route", False)
        h = {"authorization": f"Bearer {self._key}"}
        if self.rcfg.get("app_title"):
            h["x-title"] = self.rcfg["app_title"]
        return h

    def check_ready(self) -> None:
        """Refuse before any call when the credential is not in the environment."""
        self._headers()

    def capabilities(self) -> Capabilities:
        if self._listing is None:
            try:
                _, _, data = self._fetch("GET", f"{self.base_url}/models", {}, None, 20)
            except ProviderError as e:
                raise ProviderError("capabilities_unavailable",
                                    f"the OpenRouter model listing ({self.base_url}/models) could not be reached "
                                    f"({e.kind}); live use is refused until it can be checked (no fallback)", False) from None
            self._listing = {m.get("id"): m for m in data.get("data") or []}
        m = self._listing.get(self.model)
        if m is None:
            raise ProviderError("model_not_listed", f"{self.model} is not in the OpenRouter model listing; check the "
                                                    "slug in config/ai.yaml (no fallback)", False)
        arch = m.get("architecture") or {}
        params = set(m.get("supported_parameters") or [])
        return Capabilities(images="image" in (arch.get("input_modalities") or []), tools="tools" in params,
                            structured_output=bool(params & {"structured_outputs", "response_format"}),
                            context_tokens=m.get("context_length"),
                            retention=self.rcfg.get("retention", "OpenRouter and upstream provider policy; not verified "
                                                                 "by this tool"),
                            source=f"GET {self.base_url}/models (fetched this run)",
                            max_output_tokens=(m.get("top_provider") or {}).get("max_completion_tokens"),
                            details={"listing_pricing_not_used_for_cost": m.get("pricing")})

    def body(self, request: Request) -> dict:
        msgs = [{"role": "system", "content": request.system}]
        for m in request.messages:
            if m["role"] == "user":
                parts = []
                for p in m["content"]:
                    if p["type"] == "text":
                        parts.append({"type": "text", "text": p["text"]})
                    elif p["type"] == "image":
                        parts.append({"type": "image_url", "image_url": {
                            "url": f"data:{p.get('media_type', 'image/png')};base64,{image_b64(p)}"}})
                msgs.append({"role": "user", "content": parts})
            elif m["role"] == "assistant":
                msg = {"role": "assistant", "content": text_of(m["content"]) or None}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [{"id": c["id"], "type": "function",
                                          "function": {"name": c["name"], "arguments": json.dumps(c["arguments"])}}
                                         for c in m["tool_calls"]]
                msgs.append(msg)
            elif m["role"] == "tool":
                images = []
                for r in m["results"]:
                    msgs.append({"role": "tool", "tool_call_id": r["tool_call_id"], "content": r["content"]})
                    images += [(r["tool_call_id"], im) for im in r.get("images") or []]
                if images:
                    msgs.append({"role": "user", "content": [
                        x for cid, im in images for x in (
                            {"type": "text", "text": f"image returned by tool call {cid} (sha256 {im.get('sha256')})"},
                            {"type": "image_url", "image_url": {"url": f"data:{im.get('media_type', 'image/png')};base64,"
                                                                       f"{image_b64(im)}"}})]})
        body = {"model": self.model, "messages": msgs, "max_tokens": request.max_tokens}
        if request.tools:
            body["tools"] = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                               "parameters": t["input_schema"]}} for t in request.tools]
        for k, v in (self.mcfg.get("request_extra") or {}).items():
            body.setdefault(k, v)
        return body

    def complete(self, request: Request) -> Response:
        _, _, data = http_json("POST", f"{self.base_url}/chat/completions", self._headers(), self.body(request),
                               request.timeout_s)
        if data.get("error"):
            err = data["error"]
            code = err.get("code") if isinstance(err, dict) else None
            raise ProviderError(f"api_error_{code}", str(err)[:300], isinstance(code, int) and (code == 429 or code >= 500))
        ch = (data.get("choices") or [{}])[0]
        msg = ch.get("message") or {}
        calls = []
        for i, c in enumerate(msg.get("tool_calls") or []):
            fn = c.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except ValueError:
                args = {"__unparseable_arguments__": (fn.get("arguments") or "")[:2000]}
            calls.append(ToolCall(c.get("id") or f"call_{i}", fn.get("name", ""), args if isinstance(args, dict) else
                                  {"__not_an_object__": args}))
        u = data.get("usage") or {}
        return Response(text=msg.get("content") or "", tool_calls=calls,
                        usage={"input_tokens": int(u.get("prompt_tokens") or 0),
                               "output_tokens": int(u.get("completion_tokens") or 0), "detail": u},
                        model_reported=data.get("model"), raw=data, stop_reason=ch.get("finish_reason"))
