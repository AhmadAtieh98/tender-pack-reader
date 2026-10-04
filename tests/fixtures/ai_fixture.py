"""Session 09 AI-layer test helpers: blind rehearsal 02 as a FRESH addendum (ADD-03 arrived, no curated op file yet),
in disposable directories. The rehearsal's own files are read, never written. Its evidence build is the test
session's disposable ingest of rehearsals/blind-02/work/pack.yaml (tests/conftest.py, fixture `blind02_build`), never
the uncommitted rehearsals/blind-02/build."""
from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
BLIND = ROOT / "rehearsals/blind-02"
CASSETTES = ROOT / "tests/fixtures/ai_cassettes"
CURATED_ADD03 = BLIND / "work/amendments/ADD-03.yaml"
BUILDS = None          # the test session's rehearsal builds (tests/conftest.py registers its RehearsalBuilds here)


def session_evidence() -> Path:
    """The session's disposable blind-02 evidence build (the `blind02_build` fixture), ingested on first use."""
    if BUILDS is None:
        raise RuntimeError("the blind-02 evidence build is made by the pytest session (tests/conftest.py); "
                           "outside it, pass evidence= explicitly")
    return BUILDS.build("blind-02")


class _SessionEvidence(os.PathLike):
    """EVIDENCE, kept for callers written before session 10 (new tests take the `blind02_build` fixture): stands for
    session_evidence() wherever it is used as a path."""

    def __fspath__(self) -> str:
        return os.fspath(session_evidence())

    __str__ = __fspath__

    def __truediv__(self, other) -> Path:
        return session_evidence() / other

    def __getattr__(self, name):
        return getattr(session_evidence(), name)

    def __repr__(self) -> str:
        return "EVIDENCE(the test session's disposable blind-02 build)"


EVIDENCE = _SessionEvidence()


def fresh_pack(d: Path, decisions: list[dict] | None = None) -> Path:
    """A copy of the blind-02 pack whose amendments directory holds ADD-01 and ADD-02 only (ADD-03 is drafted by the
    pattern drafter, so it is PARTIAL and the validated state is ADD-02) and whose decisions file is disposable."""
    d = Path(d)
    (d / "amendments").mkdir(parents=True, exist_ok=True)
    for a in ("ADD-01", "ADD-02"):
        shutil.copy(BLIND / "work/amendments" / f"{a}.yaml", d / "amendments" / f"{a}.yaml")
    cfg = yaml.safe_load((BLIND / "work/pack.yaml").read_text(encoding="utf-8"))
    cfg["amendments_dir"] = str(d / "amendments")
    cfg["decisions"] = str(d / "decisions.yaml")
    if decisions:
        (d / "decisions.yaml").write_text(yaml.safe_dump({"decisions": decisions}, sort_keys=False), encoding="utf-8")
    (d / "pack.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return d / "pack.yaml"


def workspace(d: Path, decisions: list[dict] | None = None, evidence: Path | None = None):
    """`evidence` defaults to the session's disposable blind-02 build (the `blind02_build` fixture)."""
    from tenderpack.ai.tools import Workspace
    pack = fresh_pack(Path(d) / "pack", decisions)
    return Workspace(evidence or session_evidence(), pack, ROOT, Path(d) / "staging", Path(d) / "worklog",
                     ROOT / "config/ai.yaml")


def tree_hash(*dirs: Path) -> str:
    h = hashlib.sha256()
    for base in dirs:
        base = Path(base)
        if not base.exists():
            h.update(f"absent {base}".encode())
            continue
        h.update(f"tree {base}".encode())
        for p in sorted(base.rglob("*")):
            if p.is_file():
                h.update(p.relative_to(base).as_posix().encode())
                h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def hard() -> list[Path]:
    """Nothing else writes here during a test run: build/ and, once this session has made it, the blind-02 build."""
    built = BUILDS.built("blind-02") if BUILDS is not None else None
    return [ROOT / "build"] + ([built] if built else [])


SOFT = [ROOT / "curation", BLIND / "work"]            # other engineers may edit these concurrently


def tree_files(*dirs: Path) -> dict[str, str]:
    out = {}
    for base in dirs:
        for p in sorted(Path(base).rglob("*")) if Path(base).exists() else []:
            if p.is_file():
                out[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


class WriteAudit:
    """Records every path this process opens for writing, creates, renames or removes while active (builtins.open,
    io.open, os.open, os.remove/unlink/rename/replace/mkdir). Other engineers may edit curation/ at the same time, so a
    tree hash alone cannot attribute a change; this can."""

    def __init__(self):
        self.paths: list[str] = []

    def __enter__(self):
        import builtins
        import io
        import os
        self._saved = []

        def wrap(mod, name, is_write):
            orig = getattr(mod, name)

            def f(path, *a, **k):
                if is_write(a, k):
                    self.paths.append(os.path.abspath(os.fspath(path)) if isinstance(path, (str, bytes, os.PathLike)) else str(path))
                return orig(path, *a, **k)
            self._saved.append((mod, name, orig))
            setattr(mod, name, f)

        def mode_w(a, k):
            m = (a[0] if a else k.get("mode", "r"))
            return isinstance(m, str) and any(c in m for c in "wax+")

        def flags_w(a, k):
            fl = a[0] if a else k.get("flags", 0)
            return bool(fl & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        always = lambda a, k: True  # noqa: E731
        wrap(builtins, "open", mode_w)
        wrap(io, "open", mode_w)
        wrap(os, "open", flags_w)
        for name in ("remove", "unlink", "rename", "replace", "mkdir"):
            wrap(os, name, always)
        return self

    def __exit__(self, *exc):
        for mod, name, orig in reversed(self._saved):
            setattr(mod, name, orig)
        return False

    def under(self, base: Path) -> list[str]:
        b = str(Path(base).resolve())
        return [p for p in self.paths if p == b or p.startswith(b + "/")]


class Untouched:
    """`with Untouched() as u:` around a run: build/ and the evidence build are byte-identical before and after; this
    process wrote nothing anywhere in the repository (WriteAudit); curation/ and the rehearsal's curated work are
    byte-identical too, unless another process changed them during the run (then only that process is to blame, which
    the audit establishes, and the files are reported)."""

    def __enter__(self):
        self.hard_dirs = hard()                          # the evidence build lives outside the repository now
        self.hard, self.soft = tree_hash(*self.hard_dirs), tree_files(*SOFT)
        self.audit = WriteAudit().__enter__()
        return self

    def __exit__(self, *exc):
        self.audit.__exit__(*exc)
        if exc[0] is not None:
            return False
        assert tree_hash(*self.hard_dirs) == self.hard, "build/ or the evidence build changed"
        assert self.audit.under(ROOT) == [], f"this process wrote inside the repository: {self.audit.under(ROOT)}"
        wrote = [p for d in self.hard_dirs for p in self.audit.under(d)]
        assert wrote == [], f"this process wrote inside the evidence build: {wrote}"
        after = tree_files(*SOFT)
        changed = sorted(k for k in set(self.soft) | set(after) if self.soft.get(k) != after.get(k))
        if changed:
            import warnings
            warnings.warn(f"changed by ANOTHER process during the run (this one wrote nothing there): {changed}")
        return False
