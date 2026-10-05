"""Configuration of the AI layer: config/ai.yaml (routes, model choices, capabilities as declared, caps, prices,
retention notes). Model identifiers appear only there, as configuration values.

What is checked on load: the file has `routes` and every route named on the command line exists; a cap is a
non-negative number or null; prices are {model: {input_per_mtok, output_per_mtok}} numbers. A failure raises
ConfigError (the CLI prints it and exits 2); nothing falls back to a default model or route silently.

Caps are merged in this order (later wins): `defaults.caps`, the route's `caps`, then caps given on the command
line. A cap left null is unset; a paid route refuses to start while its call and token caps are unset (budget.py).
"""
from __future__ import annotations

from pathlib import Path

from ..util import ROOT, load_yaml

DEFAULT_PATH = ROOT / "config/ai.yaml"
CAP_KEYS = ("max_calls", "max_input_tokens", "max_output_tokens", "max_usd", "timeout_s", "max_turns", "concurrency",
            "max_tokens_per_call", "call_timeout_s", "retries", "backoff_s", "max_tool_result_chars")


class ConfigError(Exception):
    pass


def load(path: Path | None = None) -> dict:
    p = Path(path or DEFAULT_PATH)
    if not p.exists():
        raise ConfigError(f"no AI configuration at {p}")
    cfg = load_yaml(p) or {}
    if not isinstance(cfg.get("routes"), dict) or not cfg["routes"]:
        raise ConfigError(f"{p}: `routes` is missing or empty")
    for model, pr in (cfg.get("prices") or {}).items():
        if not isinstance(pr, dict) or not all(isinstance(pr.get(k), (int, float)) for k in ("input_per_mtok", "output_per_mtok")):
            raise ConfigError(f"{p}: prices.{model} needs numeric input_per_mtok and output_per_mtok")
    for where, caps in [("defaults", (cfg.get("defaults") or {}).get("caps") or {})] + \
            [(f"routes.{k}", (v or {}).get("caps") or {}) for k, v in cfg["routes"].items()]:
        for k, v in caps.items():
            if k not in CAP_KEYS:
                raise ConfigError(f"{p}: {where}.caps.{k} is not a known cap ({', '.join(CAP_KEYS)})")
            if v is not None and (not isinstance(v, (int, float)) or v < 0):
                raise ConfigError(f"{p}: {where}.caps.{k} must be a non-negative number or null, got {v!r}")
    cfg["_path"] = str(p)
    return cfg


def route(cfg: dict, name: str) -> dict:
    if name not in cfg["routes"]:
        raise ConfigError(f"unknown route {name!r}; configured routes: {', '.join(cfg['routes'])}")
    return cfg["routes"][name] or {}


def caps(cfg: dict, route_name: str, overrides: dict | None = None) -> dict:
    out = {k: None for k in CAP_KEYS}
    out.update({k: v for k, v in ((cfg.get("defaults") or {}).get("caps") or {}).items()})
    out.update({k: v for k, v in (route(cfg, route_name).get("caps") or {}).items()})
    out.update({k: v for k, v in (overrides or {}).items() if v is not None})
    return out


def model_entry(rcfg: dict, model: str) -> dict:
    """The configured entry for a model id on a route (capabilities, num_ctx, status), or {}."""
    for v in (rcfg.get("models") or {}).values():
        if isinstance(v, dict) and v.get("id") == model:
            return v
        if v == model:
            return {"id": v}
    return {}


def default_model(rcfg: dict, role: str = "propose") -> str | None:
    v = (rcfg.get("models") or {}).get(role)
    return v.get("id") if isinstance(v, dict) else v


def phase_model(rcfg: dict, route_name: str, phase: str, explicit: str | None = None) -> str | None:
    """Session 12: the model of a workflow phase on a route. `explicit` (--model) wins for the text phases. On the
    ollama route (local models, one per role in config/ai.yaml): the reading phase takes `models.vision` when
    configured (it needs image input; the capability check still decides), the text phases `propose`, else `text`.
    Other routes: --model, else `models.propose` (unchanged)."""
    if route_name == "ollama":
        if phase == "reading":
            return default_model(rcfg, "vision") or explicit or default_model(rcfg) or default_model(rcfg, "text")
        return explicit or default_model(rcfg) or default_model(rcfg, "text")
    return explicit or default_model(rcfg)


def critic_model(rcfg: dict, route_name: str, explicit: str | None = None) -> str | None:
    """The critic's model on a route: `explicit`, else `models.critic`; on the API routes also `check`, then `propose`
    (session 10). On the ollama route ONLY `models.critic` (it may name the same model as `propose`): no implicit
    fallback, so a missing local critic is recorded as a skipped review, never silently replaced."""
    if explicit:
        return explicit
    if route_name == "ollama":
        return default_model(rcfg, "critic")
    return default_model(rcfg, "critic") or default_model(rcfg, "check") or default_model(rcfg)
