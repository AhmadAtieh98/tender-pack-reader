"""The direct Messages API route (an application making paid API calls), over the standard library (urllib).

  * The key comes from the environment (`api_key_env`, default ANTHROPIC_API_KEY) or, session 13, a chmod-600 key file
    OUTSIDE the folder (tenderpack/ai/keys.py); it is never read from a file inside the folder,
    never logged and never put into an error message. Without it the route refuses to start.
  * Requests: POST {base_url}/v1/messages with the `anthropic-version` header from config; tools as {name,
    description, input_schema}; images as base64 image blocks; tool results as tool_result blocks in one user
    message per assistant turn. The assistant's own content (including any thinking blocks) is replayed unchanged on
    the next request (append-only history). `request_extra` from the route config is merged into the body (e.g.
    output_config.effort for a model that supports it); nothing else is added.
  * No server-side model fallback is requested: a refusal (stop_reason "refusal") is a ProviderError, so the run ends
    `provider_failed` rather than being silently answered by another model.
  * Capabilities (session 10: no silent fallback): GET {base_url}/v1/models/{model} (shape from the bundled claude-api
    skill, shared/models.md "Programmatic Model Discovery" -> "Raw HTTP": `max_input_tokens` is the context window,
    `max_tokens` the output cap, `capabilities.<leaf>.supported` per feature: image_input, structured_outputs). Without
    a key, when the endpoint cannot be reached or does not list the model, or when it omits max_input_tokens or
    max_tokens, live use is REFUSED ("capabilities unverified"); the configured `capabilities:` block is used only with
    --allow-unverified-capabilities (base.unverified: marked, logged, shown in the review request). A leaf the endpoint
    omits is unknown (None), never filled from config. Tool use is a Messages API feature for every listed model (the
    documented models response has no tool-use leaf); a model that rejected `tools` would fail its first call visibly.
  * Native structured outputs (session 10): when a request carries `response_schema` (the controller's proposal-set
    schema), the endpoint reports `structured_outputs`, and the route's `structured_output.mode` is `native`, the body
    gets `output_config.format = {type: "json_schema", schema}` (merged with any `output_config` from request_extra,
    e.g. effort), sent with the tools on every turn; see structured.py for the schema and its limits. A 400 that rejects
    the schema switches this provider to the plain path for the rest of the run, with a route notice, and the attempt is
    retried (counted as a call) without the format. The controller parses and validates the answer locally either way.
  * Token counting: count_tokens(request) -> POST {base_url}/v1/messages/count_tokens with model, system, messages and
    tools (shared/token-counting.md; it samples nothing). Used by the batch planner when a key is set.
  * One attempt per complete(); retries, backoff on 408/409/429/5xx/529 and timeouts (honouring retry-after) are
    done by base.complete_with_retries, bounded by the run's caps.
"""
from __future__ import annotations

import os

from . import structured as SO
from .base import (ALLOW_UNVERIFIED_KEY, Capabilities, ProviderError, Request, Response, ToolCall, configured_capabilities,
                   http_json, image_b64, notice, unverified)


class AnthropicProvider:
    name = "anthropic"
    paid = True

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ,
                 allow_unverified: bool = False, fetch=None):
        from ..offline import check_adapter
        check_adapter("anthropic")                  # session 14 (W6): offline mode, before anything (also when built directly)
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        self.base_url = (rcfg.get("base_url") or "https://api.anthropic.com").rstrip("/")
        self.version = rcfg.get("api_version") or "2023-06-01"
        self.key_env = rcfg.get("api_key_env") or "ANTHROPIC_API_KEY"
        from .. import keys                       # session 13: the environment, else a chmod-600 file outside
        self._key, self._key_source = keys.lookup(self.key_env, env)   # the folder; never logged or shown
        self._caps: Capabilities | None = None
        self.allow_unverified = bool(allow_unverified or rcfg.get(ALLOW_UNVERIFIED_KEY))
        self._fetch = fetch                     # None: base.http_json, looked up at call time (tests patch the module)
        self.structured_mode = str((rcfg.get("structured_output") or {}).get("mode", "native"))
        self._plain_reason: str | None = None   # set when native structured output is not (or no longer) used
        self.format_sent = False                # the last request body carried output_config.format

    def key_source(self) -> str | None:
        """Where the key comes from (never its value)."""
        return self._key_source

    def _http(self, *a):
        return (self._fetch or http_json)(*a)

    def _headers(self) -> dict:
        if not self._key:
            raise ProviderError("no_credentials", f"set {self.key_env} in the environment (never in a file, chat or "
                                                  "log) to use this route", retryable=False)
        return {"x-api-key": self._key, "anthropic-version": self.version}

    def check_ready(self) -> None:
        """Refuse before any call when the credential is not in the environment."""
        self._headers()

    def capabilities(self) -> Capabilities:
        if self._caps is not None:
            return self._caps
        retention = self.rcfg.get("retention", "provider policy; not verified by this tool")
        endpoint = f"GET /v1/models/{self.model}"
        configured = (configured_capabilities(self.mcfg, retention, "config/ai.yaml capabilities")
                      if self.mcfg.get("capabilities") else None)
        if not self._key:
            self._caps = unverified("anthropic", self.model, f"no {self.key_env} in the environment, so {endpoint} "
                                    "cannot be called", configured, self.allow_unverified)
            return self._caps
        try:
            _, _, m = self._http("GET", f"{self.base_url}/v1/models/{self.model}", self._headers(), None, 20)
        except ProviderError as e:
            what = "does not list the model" if e.status == 404 else "could not be reached"
            self._caps = unverified("anthropic", self.model, f"the models endpoint {what} ({endpoint}: {e.kind})",
                                    configured, self.allow_unverified)
            return self._caps
        missing = [k for k in ("max_input_tokens", "max_tokens") if not isinstance(m.get(k), int)]
        if missing:
            self._caps = unverified("anthropic", self.model, f"{endpoint} does not report {' or '.join(missing)}",
                                    configured, self.allow_unverified)
            return self._caps
        c = m.get("capabilities") if isinstance(m.get("capabilities"), dict) else {}
        leaf = lambda k: (c.get(k) or {}).get("supported") if isinstance(c.get(k), dict) else None  # noqa: E731
        self._caps = Capabilities(images=leaf("image_input"), tools=True, structured_output=leaf("structured_outputs"),
                                  context_tokens=m["max_input_tokens"], retention=retention,
                                  source=f"{endpoint} (context, output cap, image input, structured outputs; tool use "
                                         "is a Messages API feature of every listed model)",
                                  max_output_tokens=m["max_tokens"],
                                  details={"model_id_reported": m.get("id"),
                                           "leaves_not_reported": [k for k in ("image_input", "structured_outputs")
                                                                   if leaf(k) is None]})
        return self._caps

    # ------------------------------------------------------------------ structured outputs
    def native_format(self, request: Request) -> dict | None:
        """output_config.format for this request, or None (plain path: the answer is parsed locally as text)."""
        if request.response_schema is None:
            return None
        why = self._plain_reason
        if why is None and self.structured_mode != "native":
            why = f"routes.anthropic.structured_output.mode is {self.structured_mode!r}"
        if why is None:
            caps = self._caps
            if caps is None or caps.structured_output is not True:
                why = (f"the endpoint does not report structured outputs for {self.model} "
                       f"(structured_output={None if caps is None else caps.structured_output})")
        if why is None:
            try:
                return {"type": "json_schema", "schema": SO.for_provider(request.response_schema, "anthropic")}
            except SO.SchemaUnsupported as e:
                why = f"the proposal-set schema cannot be expressed within the structured-output limits ({e})"
        if self._plain_reason is None:
            self._plain_reason = why
            notice("structured_output_not_used", f"native structured output not used ({why}); the final answer is "
                                                 "parsed and validated locally from text", route="anthropic",
                   model=self.model)
        return None

    # ------------------------------------------------------------------ translation
    @staticmethod
    def _content(parts: list[dict]) -> list[dict]:
        out = []
        for p in parts:
            if p["type"] == "text":
                out.append({"type": "text", "text": p["text"]})
            elif p["type"] == "image":
                out.append({"type": "image", "source": {"type": "base64", "media_type": p.get("media_type", "image/png"),
                                                        "data": image_b64(p)}})
        return out

    def body(self, request: Request) -> dict:
        msgs = []
        for m in request.messages:
            if m["role"] == "user":
                msgs.append({"role": "user", "content": self._content(m["content"])})
            elif m["role"] == "assistant":
                content = m.get("provider_raw") if m.get("provider_raw") is not None else (
                    [{"type": "text", "text": p["text"]} for p in m["content"] if p.get("text")]
                    + [{"type": "tool_use", "id": c["id"], "name": c["name"], "input": c["arguments"]}
                       for c in m.get("tool_calls") or []])
                msgs.append({"role": "assistant", "content": content})
            elif m["role"] == "tool":
                blocks = []
                for r in m["results"]:
                    inner = [{"type": "text", "text": r["content"]}] + self._content(r.get("images") or [])
                    blocks.append({"type": "tool_result", "tool_use_id": r["tool_call_id"], "content": inner,
                                   "is_error": bool(r.get("is_error"))})
                msgs.append({"role": "user", "content": blocks})
        body = {"model": self.model, "max_tokens": request.max_tokens, "system": request.system, "messages": msgs}
        if request.tools:
            body["tools"] = [{"name": t["name"], "description": t["description"], "input_schema": t["input_schema"]}
                             for t in request.tools]
        for k, v in (self.mcfg.get("request_extra") or {}).items():
            body.setdefault(k, v)
        fmt = self.native_format(request)
        self.format_sent = fmt is not None
        if fmt is not None:                     # merged with request_extra's output_config (e.g. effort), never replacing it
            body["output_config"] = {**(body.get("output_config") or {}), "format": fmt}
        return body

    def count_tokens(self, request: Request) -> int:
        """POST /v1/messages/count_tokens (free; samples nothing): the input tokens of this request as the endpoint
        counts them for this model."""
        b = self.body(request)
        body = {k: b[k] for k in ("model", "system", "messages", "tools") if k in b}
        _, _, data = self._http("POST", f"{self.base_url}/v1/messages/count_tokens", self._headers(), body,
                                request.timeout_s)
        if not isinstance(data.get("input_tokens"), int):
            raise ProviderError("count_tokens", f"no input_tokens in the reply ({str(data)[:200]})", False)
        return data["input_tokens"]

    def complete(self, request: Request) -> Response:
        body = self.body(request)
        try:
            _, _, data = self._http("POST", f"{self.base_url}/v1/messages", self._headers(), body, request.timeout_s)
        except ProviderError as e:
            if self.format_sent and SO.is_schema_rejection(e):
                self._plain_reason = f"the endpoint rejected the structured-output schema ({e.kind}: {e.message[:200]})"
                notice("structured_output_rejected", f"{self._plain_reason}; the run continued on the plain tool-use "
                                                     "path (final answer parsed and validated locally)",
                       route="anthropic", model=self.model)
                raise ProviderError("structured_output_rejected", self._plain_reason, True, e.status, 0.0) from None
            raise
        if data.get("type") == "error":
            raise ProviderError("api_error", str(data.get("error"))[:300], False)
        if data.get("stop_reason") == "refusal":
            raise ProviderError("refusal", str(data.get("stop_details"))[:300], False)
        content = data.get("content") or []
        text = "\n".join(b.get("text", "") for b in content if b.get("type") == "text")
        calls = [ToolCall(b["id"], b["name"], b.get("input") or {}) for b in content if b.get("type") == "tool_use"]
        u = data.get("usage") or {}
        usage = {"input_tokens": int(u.get("input_tokens") or 0) + int(u.get("cache_read_input_tokens") or 0)
                 + int(u.get("cache_creation_input_tokens") or 0),
                 "output_tokens": int(u.get("output_tokens") or 0), "detail": u}
        return Response(text=text, tool_calls=calls, usage=usage, model_reported=data.get("model"), raw=data,
                        stop_reason=data.get("stop_reason"), provider_raw=content)
