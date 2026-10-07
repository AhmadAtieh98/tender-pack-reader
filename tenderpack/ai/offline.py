"""Offline mode (session 12): every AI phase on the local Ollama route, and NOTHING hosted.

How it is switched on (any one is enough; the source is recorded in the run's settings and log):
    the command-line flag `--offline` (`tenderpack ai run|resume|critic|propose|capabilities|plan-batches|routes`)
    `offline: true` in config/ai.yaml
    the environment variable TENDERPACK_OFFLINE=1

What it forces:
  * the route of every phase is `ollama` (readings, analysis, downstream, the critic, the bounded repair, the
    capability checks). `--route` defaults to ollama; `--route host|anthropic|openrouter` is REFUSED (ConfigError)
    before any process or network call. The recorded route stays what it is: a test replay (no network), never a
    fallback for anything.
  * every code path that would start a host session (`claude -p`: HostSession, AnswerSession, PlainSession, the host
    critic, the host repair) or build an anthropic / openrouter adapter raises OfflineError (a ConfigError) BEFORE
    the process or the connection: `check_route` is called by providers.make, the host sessions' constructors and the
    workflow. Session 14: also by each hosted adapter's own constructor (`check_adapter`), and the HTTP layer refuses
    any non-loopback address in an offline process (`check_http`), so an adapter built directly cannot reach a hosted
    endpoint either. There is no silent fallback anywhere: a phase that cannot run locally is refused, escalated or recorded
    as skipped with its reason.
  * session 14 (F4; R4-6): ONE resolver, `is_offline`, answers "is this process offline" for every guard (check_route,
    check_host_session, check_adapter, check_http, the Ollama adapter): the flag, the config key and the variable each
    switch the whole PROCESS offline. `activate` (every command that loads its configuration) and the `ai` command
    line itself (before any command runs) latch the process (`switch_process`; it also sets TENDERPACK_OFFLINE=1 for
    the process's children); a process never switches back.
  * the Ollama base URL must be a loopback address (127.0.0.1, ::1, localhost); another host is refused.
  * the critic uses `routes.ollama.models.critic` (it may be the same model as `propose`); when none is configured,
    or the model is not installed or cannot hold the request, the review is recorded SKIPPED with the reason ("independent
    review did not run: <reason>") in the run log, the checkpoint, the review packet and the candidate README; never as
    agreement.

What it does not do: it never downloads a model (`ollama pull` is never run; a missing model is reported with the
command a person may run) and it never claims that a local model is good at the task (nothing is measured here).
"""
from __future__ import annotations

import ipaddress
import os
from urllib.parse import urlparse

from .config import ConfigError

OFFLINE_KEY = "_offline"                 # set in a loaded config dict when offline mode is active (its source)
ENV = "TENDERPACK_OFFLINE"
LOCAL_ROUTES = ("ollama",)
TEST_ROUTES = ("recorded",)
HOSTED_ROUTES = ("host", "anthropic", "openrouter")
KINDS = {"host": "connected coding host", "anthropic": "hosted API", "openrouter": "hosted API",
         "ollama": "local inference", "recorded": "recorded (tests only; not a live integration)"}
CRITIC_REFUSAL = ("offline mode: the host critic is not available; configure routes.ollama.models.critic or accept a "
                  "skipped review")


class OfflineError(ConfigError):
    """A hosted route, process or address was asked for in offline mode (raised before any call)."""


def _truthy(v) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def requested(cfg: dict | None = None, flag: bool = False, env=None) -> str | None:
    """The source of offline mode, or None: the flag, the config key, the environment variable (first that holds)."""
    env = os.environ if env is None else env
    if flag:
        return "--offline"
    if cfg and cfg.get(OFFLINE_KEY):
        return str(cfg[OFFLINE_KEY])
    if cfg and cfg.get("offline") is True:
        return "config/ai.yaml offline: true"
    if _truthy(env.get(ENV, "")):
        return f"{ENV}={env.get(ENV)}"
    return None


# session 14 (F4; R4-6): the source that switched THIS process offline (the flag, the config key or the variable), or
# None. Set once by switch_process (activate, the `ai` command line); never cleared in a running process.
_PROCESS: str | None = None


def switch_process(source: str | None) -> str | None:
    """Session 14 (F4; R4-6): switch this whole process offline (and its children: TENDERPACK_OFFLINE=1), whatever the
    switch was, so the last-line guards (check_adapter, check_http) hold under each one. Returns the process's source."""
    global _PROCESS
    if source:
        _PROCESS = _PROCESS or str(source)
        os.environ[ENV] = "1"
    return _PROCESS


def is_offline(cfg: dict | None = None, env=None) -> str | None:
    """Session 14 (F4; R4-6): THE resolver of offline mode, used by every guard: the source when offline mode holds for
    this config or this process, else None. A config marked by activate, or with ai.yaml's `offline: true`; this
    process switched offline (by --offline, the config key or the variable: switch_process); TENDERPACK_OFFLINE."""
    env = os.environ if env is None else env
    c = cfg or {}
    if c.get(OFFLINE_KEY):
        return str(c[OFFLINE_KEY])
    if c.get("offline") is True:
        return "config/ai.yaml offline: true"
    if _PROCESS:
        return _PROCESS
    if _truthy(env.get(ENV, "")):
        return f"{ENV}={env.get(ENV)}"
    return None


def activate(cfg: dict, source: str | None) -> dict:
    """Mark a loaded config dict as offline (returns it). Checks the Ollama URL is local. Session 14 (F4; R4-6): the
    whole process is switched offline too (switch_process), before the URL check (a refused URL leaves it offline)."""
    if source:
        cfg[OFFLINE_KEY] = source
        switch_process(source)
        check_local_url(ollama_url(cfg))
    return cfg


def active(cfg: dict | None) -> bool:
    return is_offline(cfg) is not None                  # session 14 (F4; R4-6): the one resolver


def ollama_url(cfg: dict, env=None) -> str:
    env = os.environ if env is None else env
    rc = ((cfg or {}).get("routes") or {}).get("ollama") or {}
    return (env.get(rc.get("base_url_env") or "TENDERPACK_OLLAMA_URL") or rc.get("base_url")
            or "http://127.0.0.1:11434").rstrip("/")


def is_loopback(url: str) -> bool:
    host = (urlparse(url).hostname or "").strip("[]").lower()
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def check_local_url(url: str) -> None:
    if not is_loopback(url):
        raise OfflineError(f"offline mode: the Ollama URL {url} is not a loopback address (127.0.0.1, ::1, localhost); "
                           "an offline run talks to the local Ollama only")


def check_route(cfg: dict | None, route: str, what: str = "this step") -> None:
    """Raise OfflineError when offline mode is active and `route` is hosted (before any process or network call)."""
    src = is_offline(cfg)                               # session 14 (F4; R4-6): the one resolver
    if not src or route not in HOSTED_ROUTES:
        return
    raise OfflineError(f"offline mode ({src}): {what} would use the {route} route "
                       f"({KINDS[route]}); no hosted call is made. Use the ollama route (local inference) or leave "
                       "offline mode")


def check_host_session(cfg: dict | None, what: str) -> None:
    """The guard of every `claude -p` session (host sessions, the host critic, the host repair)."""
    src = is_offline(cfg)                               # session 14 (F4; R4-6): the one resolver
    if not src:
        return
    if what == "critic":
        raise OfflineError(CRITIC_REFUSAL)
    raise OfflineError(f"offline mode ({src}): {what} would start a host session "
                       "(claude -p, a connected coding host); no host process is started")


def check_adapter(route: str) -> None:
    """Session 14 (W6): the guard in every hosted adapter's constructor (AnthropicProvider, OpenRouterProvider,
    HostProvider). providers.make checks the loaded config first; this one holds when an adapter is built directly in
    a process switched offline. Session 14 (F4; R4-6): by any switch (is_offline: --offline, the config key, the
    variable), not by TENDERPACK_OFFLINE alone."""
    check_route(None, route, f"building a {route} adapter")


def check_http(url: str) -> None:
    """Session 14 (W6): the last line, in the HTTP layer every adapter shares (providers.base.http_json): in an offline
    process a request to anything but a loopback address is refused BEFORE the name is resolved or a connection made.
    Session 14 (F4; R4-6): an offline process by any switch (is_offline), not by TENDERPACK_OFFLINE alone."""
    src = is_offline(None)
    if src and not is_loopback(url):
        raise OfflineError(f"offline mode ({src}): {urlparse(url).scheme}://"
                           f"{urlparse(url).hostname} is not a loopback address; no request leaves this machine")


def check_run_route(cfg: dict, route: str) -> None:
    """The workflow's start/resume check: offline accepts ollama (and the recorded test replay) only."""
    if route in HOSTED_ROUTES:
        check_route(cfg, route, "the run")
    if route == "ollama":
        check_local_url(ollama_url(cfg))
