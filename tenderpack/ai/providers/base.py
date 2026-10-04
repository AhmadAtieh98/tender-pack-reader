"""The provider protocol shared by every route, the neutral message format, HTTP over the standard library and the
bounded retry wrapper.

    Provider: name, model, capabilities() -> Capabilities, complete(Request) -> Response
    Capabilities{images, tools, structured_output, context_tokens, retention, source}: `source` says where each value
        came from (the endpoint's own report, or "config, unverified against the endpoint"); None means unknown.
    Request{system, messages, tools, response_schema, max_tokens, timeout_s}
    Response{text, tool_calls, usage, model_reported, raw, stop_reason}

Neutral messages (each adapter translates them; nothing provider-specific leaks into the controller):
    {"role": "user", "content": [{"type": "text", "text"} | {"type": "image", "path", "sha256", "media_type"}]}
    {"role": "assistant", "content": [{"type": "text", "text"}], "tool_calls": [{"id", "name", "arguments"}],
     "provider_raw": <the provider's own content, replayed unchanged on the next request when the provider needs it>}
    {"role": "tool", "results": [{"tool_call_id", "name", "content": str, "is_error": bool, "images": [...]}]}

Failures raise ProviderError(kind, retryable, status, retry_after). complete_with_retries retries a retryable failure
(timeouts, connection errors, 408/409/429/5xx/529) up to `retries` times with exponential backoff (or the server's
retry-after), charging each attempt to the budget; then the error propagates and the controller records
`provider_failed` with the partial log kept. No adapter falls back to another model or endpoint.
"""
from __future__ import annotations

import base64
import json
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}


@dataclass
class Capabilities:
    images: bool | None
    tools: bool | None
    structured_output: bool | None
    context_tokens: int | None
    retention: str
    source: str
    max_output_tokens: int | None = None
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"images": self.images, "tools": self.tools, "structured_output": self.structured_output,
                "context_tokens": self.context_tokens, "max_output_tokens": self.max_output_tokens,
                "retention": self.retention, "source": self.source, "details": self.details}


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass
class Request:
    system: str
    messages: list[dict]
    tools: list[dict]                       # [{"name", "description", "input_schema"}]
    response_schema: dict | None = None
    max_tokens: int = 8000
    timeout_s: float = 120.0


@dataclass
class Response:
    text: str
    tool_calls: list[ToolCall]
    usage: dict                             # {"input_tokens", "output_tokens", ...}
    model_reported: str | None
    raw: dict
    stop_reason: str | None = None
    provider_raw: object = None             # assistant content to replay unchanged (e.g. thinking blocks)


class ProviderError(Exception):
    def __init__(self, kind: str, message: str, retryable: bool = False, status: int | None = None,
                 retry_after: float | None = None):
        super().__init__(f"{kind}: {message}")
        self.kind, self.message, self.retryable, self.status, self.retry_after = kind, message, retryable, status, retry_after


class Provider(Protocol):
    name: str
    model: str
    paid: bool

    def capabilities(self) -> Capabilities: ...

    def complete(self, request: Request) -> Response: ...


# ---------------------------------------------------------------------------------------------- helpers

def image_b64(part: dict) -> str:
    return base64.standard_b64encode(Path(part["path"]).read_bytes()).decode("ascii")


def text_of(content: list[dict]) -> str:
    return "\n".join(p["text"] for p in content if p.get("type") == "text")


def http_json(method: str, url: str, headers: dict, body: dict | None, timeout: float) -> tuple[int, dict, dict]:
    """One HTTP exchange with a JSON body. Returns (status, headers, parsed body). Network failures and retryable
    statuses raise ProviderError(retryable=True); other 4xx raise ProviderError(retryable=False). Headers (which hold
    the credential) are never included in an error or a log."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.status, dict(resp.headers), (json.loads(raw.decode("utf-8")) if raw else {})
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8") or "{}")
        except (ValueError, OSError):
            payload = {}
        ra = e.headers.get("retry-after") if e.headers else None
        try:
            ra = float(ra) if ra is not None else None
        except ValueError:
            ra = None
        msg = json.dumps(payload.get("error", payload))[:500]
        raise ProviderError(f"http_{e.code}", msg, e.code in RETRYABLE_STATUS, e.code, ra) from None
    except (socket.timeout, TimeoutError) as e:
        raise ProviderError("timeout", str(e) or "timed out", True) from None
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, (socket.timeout, TimeoutError)):
            raise ProviderError("timeout", str(reason), True) from None
        raise ProviderError("network", str(reason)[:300], True) from None
    except (ConnectionError, OSError) as e:
        raise ProviderError("network", str(e)[:300], True) from None


def complete_with_retries(provider: Provider, request: Request, retries: int = 2, backoff_s: float = 2.0,
                          sleep=time.sleep, before_attempt=None, on_error=None) -> Response:
    """Bounded retries for retryable failures. `before_attempt()` is the budget gate (it may raise BudgetExhausted);
    `on_error(attempt, error)` logs every failed attempt."""
    attempt = 0
    while True:
        if before_attempt:
            before_attempt()
        try:
            return provider.complete(request)
        except ProviderError as e:
            err = e
        except (socket.timeout, TimeoutError) as e:
            err = ProviderError("timeout", str(e) or "timed out", True)
        except (ConnectionError, urllib.error.URLError) as e:
            err = ProviderError("network", str(e)[:300], True)
        if on_error:
            on_error(attempt, err)
        if not err.retryable or attempt >= retries:
            raise err
        sleep(min(err.retry_after if err.retry_after is not None else backoff_s * (2 ** attempt), 60.0))
        attempt += 1
