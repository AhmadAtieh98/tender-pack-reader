"""The recorded route: replays a cassette (YAML) of canned provider turns. Used by every offline test. It records
nothing live, sends nothing anywhere and is never presented as a working live integration.

Cassette:
    name: <label>
    model: <the model name the recording claims>          (reported back as model_reported unless a turn says otherwise)
    capabilities: {images, tools, structured_output, context_tokens, retention, source}
    turns:                                                 consumed in order, one per provider call
      - match: {last_role: user|tool, contains: [..], tool_results: [tool names], tool_error: bool}   (optional)
        response: {text, tool_calls: [{id, name, arguments}], usage: {input_tokens, output_tokens},
                   model_reported, stop_reason}
      - error: {kind: timeout | http_500 | ..., retryable: true, message: ..}
        times: N                                           (an error turn is raised N times before it is consumed)

In `text` and in string tool arguments, the placeholder ${state} is replaced with the JSON of the state identity
from the task packet in the first user message (what a model is asked to copy), so a recording stays valid for the
evidence build it is replayed against; a cassette that hard-codes another state tests the stale path.
A request that does not satisfy a turn's matcher raises ProviderError("cassette_mismatch") (not retryable).

HttpCassette (session 10) replays recorded HTTP exchanges for the LIVE adapters (anthropic, openrouter, ollama), so
their real request bodies and response parsing run offline. It stands in for base.http_json; every request is kept
(`requests`) so a test can check the exact body an adapter would send. Cassette:
    name: <label>
    exchanges:                                  consumed in order (an exchange with `repeat: true` is not consumed)
      - request: {method: GET|POST, path: <url suffix>, body_has: [dotted.key, ...], body_lacks: [dotted.key, ...],
                  contains: [text in the JSON body, ...]}
        response: {status: 200, body: {...}}    (`${state}` in any string is replaced as above, from the task packet
                                                 in the request's first user message)
      - request: {...}
        error: {status: 400, message: ..., retryable: false}      (raised as base.ProviderError, like http_json does)
A request that does not match the next exchange raises ProviderError("cassette_mismatch"). Hand-written: NOT a live
model's or endpoint's output.
"""
from __future__ import annotations

import json
from pathlib import Path

from ...util import load_yaml
from .base import Capabilities, ProviderError, Request, Response, ToolCall, text_of

PACKET_MARK = "TASK PACKET\n"


class RecordedProvider:
    paid = False

    def __init__(self, cassette: Path | dict, model: str | None = None):
        data = cassette if isinstance(cassette, dict) else (load_yaml(Path(cassette)) or {})
        self.cassette_path = None if isinstance(cassette, dict) else str(cassette)
        self.name = "recorded"
        self.model = model or data.get("model") or "recorded"
        self.data = data
        self.turns = list(data.get("turns") or [])
        self.pos = 0
        self.raised = 0
        self.requests: list[Request] = []

    def capabilities(self) -> Capabilities:
        c = dict(self.data.get("capabilities") or {})
        return Capabilities(images=c.get("images"), tools=c.get("tools", True),
                            structured_output=c.get("structured_output"), context_tokens=c.get("context_tokens"),
                            retention=c.get("retention", "recorded fixture: nothing leaves the process"),
                            source=c.get("source", f"cassette {self.cassette_path or '(inline)'}; not a live endpoint"),
                            max_output_tokens=c.get("max_output_tokens"))

    # ------------------------------------------------------------------ matching
    @staticmethod
    def _state(request: Request) -> dict | None:
        for m in request.messages:
            if m["role"] == "user":
                t = text_of(m["content"])
                if t.startswith(PACKET_MARK):
                    try:
                        return json.loads(t[len(PACKET_MARK):]).get("state")
                    except ValueError:
                        return None
        return None

    @staticmethod
    def _matches(match: dict, request: Request) -> tuple[bool, str]:
        if not match:
            return True, ""
        last = request.messages[-1] if request.messages else {}
        if match.get("last_role") and last.get("role") != match["last_role"]:
            return False, f"last message role {last.get('role')!r}, expected {match['last_role']!r}"
        if last.get("role") == "tool":
            text = "\n".join(r["content"] for r in last["results"])
            names = [r["name"] for r in last["results"]]
            errors = [r.get("is_error", False) for r in last["results"]]
        else:
            text = text_of(last.get("content") or [])
            names, errors = [], []
        missing = [s for s in match.get("contains") or [] if s not in text]
        if missing:
            return False, f"last message does not contain {missing}"
        want = [n for n in match.get("tool_results") or [] if n not in names]
        if want:
            return False, f"no result for tool(s) {want} in the last message (got {names})"
        if "tool_error" in match and any(errors) != bool(match["tool_error"]):
            return False, f"tool_error {any(errors)}, expected {match['tool_error']}"
        return True, ""

    def _fill(self, s: str, state: dict | None) -> str:
        if state is not None and "${state}" in s:
            s = s.replace("${state}", json.dumps(state, ensure_ascii=False))
        return s

    def complete(self, request: Request) -> Response:
        self.requests.append(request)
        if self.pos >= len(self.turns):
            raise ProviderError("cassette_exhausted", f"no recorded turn left (used {self.pos})")
        turn = self.turns[self.pos]
        ok, why = self._matches(turn.get("match") or {}, request)
        if not ok:
            raise ProviderError("cassette_mismatch", f"turn {self.pos}: {why}")
        if "error" in turn:
            err = turn["error"] or {}
            self.raised += 1
            if self.raised >= int(turn.get("times", 1)):
                self.pos, self.raised = self.pos + 1, 0
            if err.get("kind") == "timeout":
                raise TimeoutError(err.get("message", "recorded timeout"))
            raise ProviderError(err.get("kind", "http_500"), err.get("message", "recorded failure"),
                                bool(err.get("retryable", True)), err.get("status"))
        self.pos += 1
        r = turn.get("response") or {}
        state = self._state(request)
        calls = []
        for i, c in enumerate(r.get("tool_calls") or []):
            args = {k: (self._fill(v, state) if isinstance(v, str) else v) for k, v in (c.get("arguments") or {}).items()}
            calls.append(ToolCall(id=c.get("id") or f"rec_{self.pos}_{i}", name=c["name"], arguments=args))
        text = self._fill(r.get("text") or "", state)
        usage = {"input_tokens": int((r.get("usage") or {}).get("input_tokens", 0)),
                 "output_tokens": int((r.get("usage") or {}).get("output_tokens", 0))}
        return Response(text=text, tool_calls=calls, usage=usage,
                        model_reported=r.get("model_reported", self.data.get("model")),
                        raw={"recorded_turn": self.pos - 1, "cassette": self.cassette_path},
                        stop_reason=r.get("stop_reason") or ("tool_use" if calls else "end_turn"))


# ---------------------------------------------------------------------------------------------- HTTP cassettes (s10)

def _dotted(obj, key: str):
    cur = obj
    for part in key.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return _MISSING
    return cur


_MISSING = object()


def _state_in_body(body) -> dict | None:
    """The task packet's state from a request body's first user message (any adapter's message shape)."""
    text = json.dumps(body or {}, ensure_ascii=False)
    i = text.find(json.dumps(PACKET_MARK)[1:-1])
    if i < 0:
        return None
    for m in (body or {}).get("messages") or []:
        content = m.get("content")
        parts = content if isinstance(content, list) else [{"type": "text", "text": content}]
        for p in parts:
            t = p.get("text") if isinstance(p, dict) else None
            if isinstance(t, str) and t.startswith(PACKET_MARK):
                try:
                    return json.loads(t[len(PACKET_MARK):]).get("state")
                except ValueError:
                    return None
    return None


class HttpCassette:
    """A replay of recorded HTTP exchanges with the signature of base.http_json (see the module docstring)."""

    def __init__(self, cassette: Path | dict):
        data = cassette if isinstance(cassette, dict) else (load_yaml(Path(cassette)) or {})
        self.path = None if isinstance(cassette, dict) else str(cassette)
        self.exchanges = list(data.get("exchanges") or [])
        self.pos = 0
        self.requests: list[dict] = []
        self.state: dict | None = None

    def _fill(self, obj):
        if isinstance(obj, str):
            return obj.replace("${state}", json.dumps(self.state, ensure_ascii=False)) if self.state is not None else obj
        if isinstance(obj, dict):
            return {k: self._fill(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._fill(v) for v in obj]
        return obj

    def __call__(self, method: str, url: str, headers: dict, body, timeout: float):
        self.requests.append({"method": method, "url": url, "body": body})
        self.state = _state_in_body(body) or self.state
        if self.pos >= len(self.exchanges):
            raise ProviderError("cassette_exhausted", f"no recorded HTTP exchange left for {method} {url}")
        ex = self.exchanges[self.pos]
        rq = ex.get("request") or {}
        why = None
        if rq.get("method") and rq["method"] != method:
            why = f"method {method}, expected {rq['method']}"
        elif rq.get("path") and not url.endswith(rq["path"]):
            why = f"url {url} does not end with {rq['path']}"
        else:
            missing = [k for k in rq.get("body_has") or [] if _dotted(body, k) is _MISSING]
            present = [k for k in rq.get("body_lacks") or [] if _dotted(body, k) is not _MISSING]
            text = json.dumps(body or {}, ensure_ascii=False)
            absent = [s for s in rq.get("contains") or [] if s not in text]
            if missing or present or absent:
                why = f"body lacks {missing}, has {present}, does not contain {absent}"
        if why:
            raise ProviderError("cassette_mismatch", f"exchange {self.pos}: {why}")
        if not ex.get("repeat"):
            self.pos += 1
        if "error" in ex:
            e = ex["error"] or {}
            st = e.get("status")
            raise ProviderError(e.get("kind") or (f"http_{st}" if st else "network"), str(e.get("message", "recorded")),
                                bool(e.get("retryable", False)), st)
        resp = ex.get("response") or {}
        return int(resp.get("status", 200)), {}, self._fill(resp.get("body") or {})
