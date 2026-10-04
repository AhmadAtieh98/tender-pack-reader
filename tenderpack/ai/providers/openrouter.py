"""The OpenRouter route (an application making paid API calls through an OpenAI-compatible endpoint), over urllib.

  * The key comes from the environment only (`api_key_env`, default OPENROUTER_API_KEY).
  * Capabilities come from the endpoint, not from config: GET {base_url}/models is fetched once per run (cached on
    the adapter) and the model's entry gives input modalities (images), supported parameters (tools,
    structured_outputs / response_format) and the context length. If the listing cannot be reached, or does not list
    the model, live use is REFUSED with a clear message; there is no fallback to declared values or to another
    model. (This cloud environment's network policy blocks openrouter.ai, so the route is untested live here.)
    Session 10: an entry without `context_length` is refused too ("capabilities unverified"; the controller's fit
    check would otherwise be skipped); --allow-unverified-capabilities can use a configured `capabilities:` block
    (marked unverified, logged and shown in the review request); none is configured for OpenRouter by default.
  * Native structured outputs (session 10): only when the listing's supported_parameters name `structured_outputs`
    (`response_format` alone is recorded but not taken as JSON-schema support), the request carries `response_schema`
    and routes.openrouter.structured_output.mode is `native`: `response_format: {type: "json_schema", json_schema:
    {name, strict: true, schema}}` with the schema fitted as for the Messages API (structured.py). This request shape is
    the OpenAI-compatible convention OpenRouter documents; it is NOT verified from this environment (openrouter.ai is
    blocked here). A rejected schema switches the run to the plain path with a route notice (never silently).
  * Requests: POST {base_url}/chat/completions with tools as functions; images as data: URLs in user content (a tool
    result's image is sent in a user message after the tool messages, as the chat format has no image tool results).
  * Retention and provider routing are OpenRouter's and the upstream provider's policies; they are not verified here.
  * Listing prices are reported as data but never used for cost: cost comes only from config/ai.yaml `prices`.
"""
from __future__ import annotations

import json
import os

from . import structured as SO
from .base import (ALLOW_UNVERIFIED_KEY, Capabilities, ProviderError, Request, Response, ToolCall,
                   configured_capabilities, http_json, image_b64, notice, text_of, unverified)


class OpenRouterProvider:
    name = "openrouter"
    paid = True

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ, fetch=http_json,
                 allow_unverified: bool = False):
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        self.base_url = (rcfg.get("base_url") or "https://openrouter.ai/api/v1").rstrip("/")
        self.key_env = rcfg.get("api_key_env") or "OPENROUTER_API_KEY"
        self._key = env.get(self.key_env)
        self._fetch = fetch
        self._listing: dict | None = None
        self._caps: Capabilities | None = None
        self.allow_unverified = bool(allow_unverified or rcfg.get(ALLOW_UNVERIFIED_KEY))
        self.structured_mode = str((rcfg.get("structured_output") or {}).get("mode", "native"))
        self._plain_reason: str | None = None
        self.format_sent = False

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
        if self._caps is not None:
            return self._caps
        retention = self.rcfg.get("retention", "OpenRouter and upstream provider policy; not verified by this tool")
        configured = (configured_capabilities(self.mcfg, retention, "config/ai.yaml capabilities")
                      if self.mcfg.get("capabilities") else None)
        if self._listing is None:
            try:
                _, _, data = self._fetch("GET", f"{self.base_url}/models", {}, None, 20)
            except ProviderError as e:
                if self.allow_unverified and configured is not None:
                    self._caps = unverified("openrouter", self.model, f"the model listing could not be reached ({e.kind})",
                                            configured, True)
                    return self._caps
                raise ProviderError("capabilities_unavailable",
                                    f"the OpenRouter model listing ({self.base_url}/models) could not be reached "
                                    f"({e.kind}); live use is refused until it can be checked (no fallback; capabilities "
                                    "unverified)", False) from None
            self._listing = {m.get("id"): m for m in data.get("data") or []}
        m = self._listing.get(self.model)
        if m is None:
            if self.allow_unverified and configured is not None:
                self._caps = unverified("openrouter", self.model, "the model listing does not list the model",
                                        configured, True)
                return self._caps
            raise ProviderError("model_not_listed", f"{self.model} is not in the OpenRouter model listing; check the "
                                                    "slug in config/ai.yaml (no fallback; capabilities unverified)", False)
        if not isinstance(m.get("context_length"), int):
            self._caps = unverified("openrouter", self.model, "the listing entry does not report a context_length",
                                    configured, self.allow_unverified)
            return self._caps
        arch = m.get("architecture") or {}
        params = set(m.get("supported_parameters") or [])
        self._caps = Capabilities(images="image" in (arch.get("input_modalities") or []), tools="tools" in params,
                                  structured_output="structured_outputs" in params,
                                  context_tokens=m["context_length"], retention=retention,
                                  source=f"GET {self.base_url}/models (fetched this run)",
                                  max_output_tokens=(m.get("top_provider") or {}).get("max_completion_tokens"),
                                  details={"listing_pricing_not_used_for_cost": m.get("pricing"),
                                           "supported_parameters": sorted(params)})
        return self._caps

    def native_format(self, request: Request) -> dict | None:
        """response_format for this request, or None (plain path; see the module docstring)."""
        if request.response_schema is None:
            return None
        why = self._plain_reason
        if why is None and self.structured_mode != "native":
            why = f"routes.openrouter.structured_output.mode is {self.structured_mode!r}"
        if why is None and (self._caps is None or self._caps.structured_output is not True):
            params = (self._caps.details.get("supported_parameters") if self._caps else None) or []
            why = ("the listing names response_format but not structured_outputs" if "response_format" in params
                   else "the listing does not name structured_outputs for this model")
        if why is None:
            try:
                return {"type": "json_schema", "json_schema": {"name": SO.SCHEMA_NAME, "strict": True,
                                                               "schema": SO.for_provider(request.response_schema)}}
            except SO.SchemaUnsupported as e:
                why = f"the proposal-set schema cannot be expressed within the structured-output limits ({e})"
        if self._plain_reason is None:
            self._plain_reason = why
            notice("structured_output_not_used", f"native structured output not used ({why}); the final answer is "
                                                 "parsed and validated locally from text", route="openrouter",
                   model=self.model)
        return None

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
        fmt = self.native_format(request)
        self.format_sent = fmt is not None
        if fmt is not None:
            body["response_format"] = fmt
        return body

    def _rejected(self, e: ProviderError) -> ProviderError:
        self._plain_reason = f"the endpoint rejected the structured-output schema ({e.kind}: {e.message[:200]})"
        notice("structured_output_rejected", f"{self._plain_reason}; the run continued on the plain tool-use path "
                                             "(final answer parsed and validated locally)", route="openrouter",
               model=self.model)
        return ProviderError("structured_output_rejected", self._plain_reason, True, e.status, 0.0)

    def complete(self, request: Request) -> Response:
        try:
            _, _, data = http_json("POST", f"{self.base_url}/chat/completions", self._headers(), self.body(request),
                                   request.timeout_s)
        except ProviderError as e:
            if self.format_sent and SO.is_schema_rejection(e):
                raise self._rejected(e) from None
            raise
        if data.get("error"):
            err = data["error"]
            code = err.get("code") if isinstance(err, dict) else None
            pe = ProviderError(f"api_error_{code}", str(err)[:300], isinstance(code, int) and (code == 429 or code >= 500),
                               code if isinstance(code, int) else None)
            if self.format_sent and SO.is_schema_rejection(pe):
                raise self._rejected(pe)
            raise pe
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
