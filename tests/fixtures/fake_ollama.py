"""A FAKE Ollama server for offline tests (session 12): a real HTTP server on 127.0.0.1 (a random port) that speaks the
three endpoints tenderpack uses, so the real Ollama adapter (urllib, JSON bodies) runs end to end with no Ollama and
no network:

    GET  /api/tags   the "installed" models
    POST /api/show   a model's capabilities, model_info (context length, layers, KV heads) and details (parameter size,
                     quantisation); 404 {"error": "model 'x' not found"} for a model that is not "installed"
    POST /api/chat   the answer: the recorded workflow's turns (a WorkflowCassette, hand-written; NOT a live model's
                     output) replayed through providers.recorded.RecordedProvider, the session chosen from the packet in
                     the first user message exactly as WorkflowCassette.provider chooses it (provisions, tasks, items,
                     regions), the turn from the conversation; or `chat(body)` given by the test
    POST /api/pull   recorded and answered 403: tenderpack must never call it

Every request is kept in `requests` (method, path, body). Nothing here is a live integration: passing a test that uses
it shows how tenderpack talks to an Ollama-shaped endpoint, never how a real local model behaves."""
from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PACKET_MARK = "TASK PACKET\n"
CRITIC_MARK = "CRITIC REQUEST\n"


def show(caps=("completion", "tools"), context=262144, params="8.0B", quant="Q4_K_M", layers=8, kv_heads=2, head=64,
         family="fakearch") -> dict:
    """An /api/show reply (the fields tenderpack reads)."""
    info = {f"{family}.context_length": context, f"{family}.block_count": layers,
            f"{family}.attention.head_count_kv": kv_heads, f"{family}.attention.key_length": head,
            f"{family}.attention.value_length": head, "general.architecture": family}
    return {"capabilities": list(caps), "model_info": info,
            "details": {"family": family, "parameter_size": params, "quantization_level": quant, "format": "gguf"}}


def _neutral(body: dict):
    """The Ollama messages of a /api/chat body back in tenderpack's neutral form (providers/base.py)."""
    from tenderpack.ai.providers.base import Request
    system, msgs = "", []
    for m in body.get("messages") or []:
        r = m.get("role")
        if r == "system":
            system = m.get("content") or ""
        elif r == "user":
            msgs.append({"role": "user", "content": [{"type": "text", "text": m.get("content") or ""}]})
        elif r == "assistant":
            msgs.append({"role": "assistant", "content": [{"type": "text", "text": m.get("content") or ""}],
                         "tool_calls": [{"id": f"c{i}", "name": (c.get("function") or {}).get("name"),
                                         "arguments": (c.get("function") or {}).get("arguments") or {}}
                                        for i, c in enumerate(m.get("tool_calls") or [])]})
        elif r == "tool":
            res = {"tool_call_id": "", "name": m.get("tool_name"), "content": m.get("content") or "",
                   "is_error": str(m.get("content") or "").startswith('{"error"')}
            if msgs and msgs[-1]["role"] == "tool":
                msgs[-1]["results"].append(res)
            else:
                msgs.append({"role": "tool", "results": [res]})
    return Request(system=system, messages=msgs, tools=[], response_schema=None)


class FakeOllama:
    def __init__(self, models: dict[str, dict], cassette: Path | None = None, chat=None, delay_s: float = 0.0):
        self.models = dict(models)
        self.cassette_path = cassette
        self.chat = chat
        self.delay_s = delay_s
        self.requests: list[tuple[str, str, dict]] = []
        self._conv: dict[str, object] = {}
        self._used: set[int] = set()
        self._lock = threading.Lock()
        self.server = None
        self.url = None

    # ------------------------------------------------------------------ the replay
    def _provider(self, body: dict):
        from tenderpack.ai import requests as R
        from tenderpack.ai.workflow import WorkflowCassette
        first = next((m.get("content") or "" for m in body.get("messages") or [] if m.get("role") == "user"), "")
        key = hashlib.sha256((body.get("model", "") + first).encode()).hexdigest()
        if key in self._conv:
            return self._conv[key]
        if first.startswith(CRITIC_MARK):
            pk = json.loads(first[len(CRITIC_MARK):])
            phase, keys = "critic", [x["key"] for x in pk.get("items") or []]
        else:
            pk = json.loads(first[len(PACKET_MARK):]) if first.startswith(PACKET_MARK) else {}
            phase = R.phase_of_task(pk.get("task") or "")
            keys = ([p["unit_id"] for p in pk.get("provisions") or []] + [t["id"] for t in pk.get("tasks") or []]
                    + ([pk["region_id"]] if pk.get("region_id") else []))
        prov, i = WorkflowCassette(self.cassette_path).provider(phase, keys, self._used)
        if prov is None:
            return None
        self._used.add(i)
        self._conv[key] = prov
        return prov

    def answer(self, body: dict) -> tuple[int, dict]:
        if body.get("model") not in self.models:
            return 404, {"error": f"model '{body.get('model')}' not found"}
        if self.chat is not None:
            return 200, self.chat(body)
        with self._lock:
            prov = self._provider(body)
        if prov is None:
            return 500, {"error": "fake ollama: no recorded session covers this request"}
        from tenderpack.ai.providers.base import ProviderError
        try:
            resp = prov.complete(_neutral(body))
        except ProviderError as e:
            return (e.status or 500), {"error": e.message}
        return 200, {"model": body.get("model"), "done": True, "done_reason": "stop",
                     "message": {"role": "assistant", "content": resp.text,
                                 "tool_calls": [{"function": {"name": c.name, "arguments": c.arguments}}
                                                for c in resp.tool_calls]},
                     "prompt_eval_count": resp.usage.get("input_tokens", 0),
                     "eval_count": resp.usage.get("output_tokens", 0)}

    # ------------------------------------------------------------------ the server
    def start(self) -> str:
        fake = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, status, obj):
                data = json.dumps(obj).encode()
                self.send_response(status)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                fake.requests.append(("GET", self.path, {}))
                if self.path == "/api/tags":
                    return self._send(200, {"models": [{"name": n, "model": n, "details": (s.get("details") or {})}
                                                       for n, s in fake.models.items()]})
                return self._send(404, {"error": "not found"})

            def do_POST(self):
                n = int(self.headers.get("content-length") or 0)
                body = json.loads(self.rfile.read(n) or b"{}")
                fake.requests.append(("POST", self.path, body))
                if self.path == "/api/show":
                    m = body.get("model") or body.get("name")
                    if m not in fake.models:
                        return self._send(404, {"error": f"model '{m}' not found"})
                    return self._send(200, fake.models[m])
                if self.path == "/api/chat":
                    if fake.delay_s:
                        import time
                        time.sleep(fake.delay_s)
                    return self._send(*fake.answer(body))
                if self.path == "/api/pull":
                    return self._send(403, {"error": "the fake refuses pulls; tenderpack must never pull"})
                return self._send(404, {"error": "not found"})

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        return self.url

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def paths(self) -> list[str]:
        return [f"{m} {p}" for m, p, _ in self.requests]


class NetGuard:
    """Records every outgoing socket connection and every subprocess; refuses a connection to anything but the allowed
    loopback port, and refuses any host CLI (`claude`, `codex`) process."""

    def __init__(self, monkeypatch, allow_port: int):
        import socket
        import subprocess
        self.connects: list = []
        self.processes: list = []
        self.refused: list = []
        real_connect = socket.socket.connect
        real_popen_init = subprocess.Popen.__init__
        guard = self

        def connect(sock, address):
            guard.connects.append(address)
            host = address[0] if isinstance(address, tuple) else address
            port = address[1] if isinstance(address, tuple) and len(address) > 1 else None
            if host not in ("127.0.0.1", "::1", "localhost") or port != allow_port:
                guard.refused.append(address)
                raise ConnectionRefusedError(f"NetGuard: connection to {address} refused in an offline test")
            return real_connect(sock, address)

        def popen_init(self_, args, *a, **k):
            argv = [args] if isinstance(args, (str, bytes)) else list(args)
            guard.processes.append([str(x) for x in argv][:3])
            name = Path(str(argv[0])).name if argv else ""
            if name in ("claude", "codex") or "fake_claude" in name:
                guard.refused.append(argv[:2])
                raise PermissionError(f"NetGuard: a host process ({name}) was started in an offline test")
            return real_popen_init(self_, args, *a, **k)
        monkeypatch.setattr(socket.socket, "connect", connect)
        monkeypatch.setattr(subprocess.Popen, "__init__", popen_init)

    def non_local(self) -> list:
        return [a for a in self.connects if not (isinstance(a, tuple) and a[0] in ("127.0.0.1", "::1", "localhost"))]
