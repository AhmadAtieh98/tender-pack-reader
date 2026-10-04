"""Provider adapters (see base.py for the protocol). `make(route, model, cfg, cassette)` builds one from
config/ai.yaml; an unknown route raises ConfigError. No adapter is a fallback for another."""
from __future__ import annotations

from ..config import ConfigError, model_entry, route
from .base import Capabilities, Provider, ProviderError, Request, Response, ToolCall, complete_with_retries  # noqa: F401


def make(route_name: str, model: str | None, cfg: dict, cassette=None) -> Provider:
    rcfg = route(cfg, route_name)
    if route_name == "recorded":
        if cassette is None:
            raise ConfigError("the recorded route needs --cassette (a recorded fixture; it is not a live integration)")
        from .recorded import RecordedProvider
        return RecordedProvider(cassette, model)
    if route_name == "host":
        from .host import HostProvider
        return HostProvider(model)
    if not model:
        raise ConfigError(f"route {route_name} needs --model (configured choices: "
                          f"{', '.join(str(v.get('id') if isinstance(v, dict) else v) for v in (rcfg.get('models') or {}).values())})")
    mcfg = model_entry(rcfg, model)
    if route_name == "anthropic":
        from .anthropic import AnthropicProvider
        return AnthropicProvider(model, rcfg, mcfg)
    if route_name == "openrouter":
        from .openrouter import OpenRouterProvider
        return OpenRouterProvider(model, rcfg, mcfg)
    if route_name == "ollama":
        from .ollama import OllamaProvider
        return OllamaProvider(model, rcfg, mcfg)
    raise ConfigError(f"route {route_name!r} has no adapter")
