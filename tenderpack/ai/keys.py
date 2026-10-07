"""API keys through the secure configuration only (session 13). Never in chat, in a file inside the folder, or in a log.

Where a key may come from, in this order:
  1. the environment variable the route names (`api_key_env` in config/ai.yaml: ANTHROPIC_API_KEY, OPENROUTER_API_KEY);
  2. a private key file OUTSIDE the tenderpack folder: $TENDERPACK_KEYS_FILE, else ~/.config/tenderpack/keys.env,
     with lines `NAME=value` (blank lines and # comments ignored). It is used only when it is a regular file owned by
     the person running tenderpack, with no group or other permission (chmod 600), and outside the folder (a key file
     inside it would travel with every zip and copy). A file that fails these is REFUSED with the command that fixes
     it; nothing is read from it.

The value is never printed, logged or put in an error message: `source()` says where a key comes from ("environment
ANTHROPIC_API_KEY" / "file <path>") without the value, and every value read from the file is registered with
runlog.redact (the environment's values already are), so a log line that contained it is written with [REDACTED].
Creating the file is the owner's step (docs/AI_ROUTES.md "Keys"):
    mkdir -p ~/.config/tenderpack && touch ~/.config/tenderpack/keys.env && chmod 600 ~/.config/tenderpack/keys.env
    then add the line ANTHROPIC_API_KEY=... with a text editor (not with echo: the shell history would keep it)."""
from __future__ import annotations

import os
import stat
from pathlib import Path

from ..util import ROOT
from .config import ConfigError

ENV_FILE = "TENDERPACK_KEYS_FILE"
LOADED: set[str] = set()                 # values read from a key file this process (runlog.redact removes them)


class KeyFileError(ConfigError):
    """The key file exists but may not be used (permissions, owner, location)."""


def default_path(env=None) -> Path:
    env = os.environ if env is None else env
    p = env.get(ENV_FILE)
    return Path(p).expanduser() if p else Path.home() / ".config" / "tenderpack" / "keys.env"


def check_location(path: Path, root: Path = ROOT) -> None:
    p = Path(path).expanduser().resolve()
    r = Path(root).resolve()
    if p == r or r in p.parents:
        raise KeyFileError(f"the key file {p} is inside the tenderpack folder {r}: keys must live outside it (it would "
                           f"travel with every copy and zip); move it: mv \"{p}\" ~/.config/tenderpack/keys.env")


def _check_file(path: Path) -> None:
    check_location(path)
    st = path.stat()
    if not stat.S_ISREG(st.st_mode):
        raise KeyFileError(f"the key file {path} is not a regular file")
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        raise KeyFileError(f"the key file {path} is not owned by you; nothing was read from it")
    if st.st_mode & 0o077:
        raise KeyFileError(f"the key file {path} can be read by others (mode {stat.S_IMODE(st.st_mode):03o}); nothing "
                           f"was read from it. Fix: chmod 600 \"{path}\"")


def _from_file(name: str, path: Path) -> str | None:
    if not path.exists():
        return None
    _check_file(path)
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        if k.strip().removeprefix("export ").strip() == name:
            v = v.strip().strip("'\"")
            if v:
                LOADED.add(v)
                return v
    return None


def lookup(name: str, env=None, path: Path | None = None) -> tuple[str | None, str | None]:
    """(value, where) for the key `name`; (None, None) when it is configured nowhere. Raises KeyFileError when the
    file exists but may not be used (never a silent fallback)."""
    env = os.environ if env is None else env
    if env.get(name):
        return env[name], f"environment {name}"
    p = Path(path) if path else default_path(env)
    v = _from_file(name, p)
    return (v, f"file {p}") if v else (None, None)


def get(name: str, env=None, path: Path | None = None) -> str | None:
    return lookup(name, env, path)[0]


def source(name: str, env=None, path: Path | None = None) -> str | None:
    """Where the key comes from, without its value ("environment NAME" / "file PATH"), or None."""
    try:
        return lookup(name, env, path)[1]
    except KeyFileError:
        return None


def status(name: str, env=None, path: Path | None = None) -> tuple[bool, str]:
    """(configured, explanation) for the routes listing; never the value."""
    try:
        v, where = lookup(name, env, path)
    except KeyFileError as e:
        return False, str(e)
    if v:
        return True, f"key configured ({where}; the value is never shown)"
    return False, (f"no key: set {name} in the environment, or put {name}=... in {default_path(env)} (chmod 600, "
                   "outside the folder); never in chat or a log")
