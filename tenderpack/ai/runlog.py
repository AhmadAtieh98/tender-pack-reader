"""Run logs: every prompt, tool call (with a truncated result), raw response, usage, error, overwrite and validation
of a run, one JSON object per line, written to worklog/model_calls/<run_id>.jsonl and staging/ai/<run_id>/log.jsonl.

Secrets are redacted everywhere before anything is written: values under keys that name a credential
(authorization, x-api-key, api_key, *_api_key, secret, password, access/refresh tokens), strings that look like keys
(sk-..., sk-ant-..., 'Bearer ...'), and the current values of the credential environment variables named in
config/ai.yaml. Token COUNTS (input_tokens, output_tokens) are not secrets and are kept.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path

SECRET_ENV = ("ANTHROPIC_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_AUTH_TOKEN")
_SECRET_KEY = re.compile(r"^(authorization|proxy-authorization|x-api-key|api[-_]?key|.*_api_key|.*secret.*|password|"
                         r"access_token|refresh_token|bearer|cookie|set-cookie)$", re.I)
_SECRET_STR = re.compile(r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-or-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9_\-]{16,}|"
                         r"Bearer\s+[A-Za-z0-9._\-]{8,})")
REDACTED = "[REDACTED]"


def _env_secrets(extra: tuple[str, ...] = ()) -> list[str]:
    return [v for k in (*SECRET_ENV, *extra) if (v := os.environ.get(k)) and len(v) >= 8]


def redact(obj, extra_env: tuple[str, ...] = ()):
    secrets = _env_secrets(extra_env)

    def walk(x):
        if isinstance(x, dict):
            return {k: (REDACTED if isinstance(k, str) and _SECRET_KEY.match(k) else walk(v)) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [walk(v) for v in x]
        if isinstance(x, str):
            for s in secrets:
                if s in x:
                    x = x.replace(s, REDACTED)
            return _SECRET_STR.sub(REDACTED, x)
        return x
    return walk(obj)


def truncate(text: str, n: int) -> str:
    return text if len(text) <= n else text[:n] + f"... [truncated: {len(text) - n} more characters]"


def now_iso(clock=None) -> str:
    t = clock() if clock else dt.datetime.now(dt.timezone.utc)
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RunLog:
    """Append-only JSON-lines log written to several files at once (all redacted)."""

    def __init__(self, run_id: str, paths: list[Path], clock=None, extra_env: tuple[str, ...] = ()):
        self.run_id, self.paths, self.clock, self.extra_env = run_id, [Path(p) for p in paths], clock, extra_env
        for p in self.paths:
            p.parent.mkdir(parents=True, exist_ok=True)
        self.events: list[dict] = []

    def event(self, name: str, /, **data) -> dict:
        rec = redact({"ts": now_iso(self.clock), "run_id": self.run_id, **data, "event": name}, self.extra_env)
        line = json.dumps(rec, ensure_ascii=False, sort_keys=True, default=str)
        for p in self.paths:
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        self.events.append(rec)
        return rec

    def add_path(self, path: Path) -> None:
        """Start writing to another file too (e.g. the staging copy once the run directory exists); earlier events
        are copied so both files hold the whole run."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            for rec in self.events:
                fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, default=str) + "\n")
        self.paths.append(path)
