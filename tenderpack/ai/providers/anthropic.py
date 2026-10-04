"""The direct Messages API route (an application making paid API calls), over the standard library (urllib).

  * The key comes from the environment only (`api_key_env`, default ANTHROPIC_API_KEY); it is never read from a file,
    never logged and never put into an error message. Without it the route refuses to start.
  * Requests: POST {base_url}/v1/messages with the `anthropic-version` header from config; tools as {name,
    description, input_schema}; images as base64 image blocks; tool results as tool_result blocks in one user
    message per assistant turn. The assistant's own content (including any thinking blocks) is replayed unchanged on
    the next request (append-only history). `request_extra` from the route config is merged into the body (e.g.
    output_config.effort for a model that supports it); nothing else is added.
  * No server-side model fallback is requested: a refusal (stop_reason "refusal") is a ProviderError, so the run ends
    `provider_failed` rather than being silently answered by another model.
  * Capabilities: GET {base_url}/v1/models/{model} when a key is present (max_input_tokens, max_tokens,
    capabilities.image_input / structured_outputs); tool use comes from config. If the models endpoint cannot be
    reached, the config values are used with source "config, unverified against the endpoint".
  * One attempt per complete(); retries, backoff on 408/409/429/5xx/529 and timeouts (honouring retry-after) are
    done by base.complete_with_retries, bounded by the run's caps.
"""
from __future__ import annotations

import os

from .base import Capabilities, ProviderError, Request, Response, ToolCall, http_json, image_b64


class AnthropicProvider:
    name = "anthropic"
    paid = True

    def __init__(self, model: str, rcfg: dict, model_cfg: dict | None = None, env=os.environ):
        self.model, self.rcfg, self.mcfg = model, rcfg, model_cfg or {}
        self.base_url = (rcfg.get("base_url") or "https://api.anthropic.com").rstrip("/")
        self.version = rcfg.get("api_version") or "2023-06-01"
        self.key_env = rcfg.get("api_key_env") or "ANTHROPIC_API_KEY"
        self._key = env.get(self.key_env)
        self._caps: Capabilities | None = None

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
        declared = dict(self.mcfg.get("capabilities") or {})
        retention = self.rcfg.get("retention", "provider policy; not verified by this tool")
        caps = Capabilities(images=declared.get("images"), tools=declared.get("tools", True),
                            structured_output=declared.get("structured_output"),
                            context_tokens=declared.get("context_tokens"), retention=retention,
                            source="config, unverified against the endpoint" + ("" if self._key else
                                                                                  f" (no {self.key_env} in the environment)"),
                            max_output_tokens=declared.get("max_output_tokens"))
        if self._key:
            try:
                _, _, m = http_json("GET", f"{self.base_url}/v1/models/{self.model}", self._headers(), None, 20)
                c = m.get("capabilities") or {}
                leaf = lambda k: (c.get(k) or {}).get("supported") if isinstance(c.get(k), dict) else None  # noqa: E731
                caps = Capabilities(images=leaf("image_input") if leaf("image_input") is not None else caps.images,
                                    tools=caps.tools,
                                    structured_output=leaf("structured_outputs") if leaf("structured_outputs") is not None
                                    else caps.structured_output,
                                    context_tokens=m.get("max_input_tokens") or caps.context_tokens, retention=retention,
                                    source=f"GET /v1/models/{self.model} (tool use from config)",
                                    max_output_tokens=m.get("max_tokens") or caps.max_output_tokens,
                                    details={"model_id_reported": m.get("id")})
            except ProviderError as e:
                caps.source = f"config, unverified against the endpoint (models endpoint: {e.kind})"
        self._caps = caps
        return caps

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
        return body

    def complete(self, request: Request) -> Response:
        _, _, data = http_json("POST", f"{self.base_url}/v1/messages", self._headers(), self.body(request),
                               request.timeout_s)
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
