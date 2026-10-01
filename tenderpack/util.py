"""Small shared helpers: hashing, deterministic JSON/YAML IO, colours."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def hex_color(value: int) -> str:
    return f"#{value:06x}"


def load_yaml(path: Path) -> Any:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump_json(obj: Any, path: Path) -> None:
    """Deterministic JSON: sorted keys, fixed separators, trailing newline, UTF-8."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def relpath(path: Path, root: Path) -> str:
    """Path relative to root (posix) when inside it, else absolute (e.g. test temp dirs)."""
    p, r = Path(path).resolve(), Path(root).resolve()
    return p.relative_to(r).as_posix() if p.is_relative_to(r) else p.as_posix()


def r1(x: float) -> float:
    """Round coordinates to 0.1 pt so outputs are stable across platforms."""
    return round(float(x) + 0.0, 1)


def bbox_r(b) -> list[float]:
    return [r1(v) for v in b]
