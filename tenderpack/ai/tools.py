"""Narrow tools over the existing modules, for models (application routes), coding hosts (MCP and the CLI) and the
controller itself. Each tool has a name, a JSON input schema and a JSON-serialisable result.

Read-only (they compute from the published evidence build and the curated inputs and write nothing):
  search_evidence(query, docs, kinds, limit)  deterministic token-overlap ranking (idf-weighted, phrase bonus) over
                                              the units' printed text (Latin normalised for matching; Arabic matched
                                              with textnorm.normalize_arabic, source kept); no embeddings
  get_unit(unit_id, stage)                    text as issued and effective text at a stage (engine state), cells,
                                              pages, anchors, status, history (op ids), annotations; for an image
                                              reading the Arabic/English SOURCE text, the translation and the match
                                              text as separate fields (only the source text is evidence)
  get_group(group_id, stage)                  members of a table, form or list with cells, the heading and notes
  get_crop(unit_id)                           path and sha256 of the native image / crops in the evidence build
                                              (refused for text-layer units, and for any path outside the build); each
                                              file is checked against the sha256 the build recorded: a file replaced
                                              after the build is an integrity failure (ToolError), never served
  compare_state(from_stage, to_stage)         live.diff plus every unit whose status, text, cells or annotations differ
  calculate(kind, args)                       approved date calculations only (dates.py): relative periods with every
                                              counting reading, working days between, adding working days, a working
                                              day test, and the date printed in a named unit; no arithmetic on free text.
                                              Each result carries `inputs_fingerprint` (StateIdentity.fingerprint(): the
                                              assumptions, amendment files, evidence build, ... it was computed under)
  simulate_amendment(addendum, ops, dispositions)   engine dry run (amend.Engine through stage2.evaluate on a copy;
                                              nothing persisted): per-op validity with the C21-C27 check records,
                                              coverage, unevidenced additions (C47), scope leak, changed units, C46
  simulate_programme(stage)                   the programme (programme.stage_planner) read-only: milestones and the
                                              infeasible chains, bounded
  validate_proposal(proposal)                 the controller's validation of one item or a whole set (statuses are the
                                              controller's), without writing anything
  get_state()                                 the state identity, stages and addenda statuses
Writers (staging only, never curation/):
  get_task_packet(addendum, claim)            the task packet; with claim=true it takes the addendum's orchestrator lock
  request_review(proposal_set) / submit_proposals(proposal_set, host_model)   validate a set and write
                                              staging/ai/<run_id>/{proposals.yaml, review_request.md, log.jsonl}

Every evidence read runs on a verified version (session 10): the Workspace's inputs are those it loaded (otherwise
"workspace stale: reload"; a tool call reloads first) and the evidence build verified against its manifest (otherwise
"integrity failure").

The tool layer never executes model text: arguments are checked against each tool's schema (unknown keys, types,
enums) and used as data. Unit and stage ids are looked up, never used as paths; the only file paths a tool returns
are crops inside the evidence build, checked after resolution.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable

from pydantic import ValidationError

from .. import amend, stage2
from ..dates import DateRule, interpretations, long_date, parse_date, planning_value
from ..textnorm import has_arabic, normalize_arabic, normalize_latin
from ..util import ROOT, load_yaml, sha256_file
from .budget import Refused
from .contract import StateIdentity


class ToolError(Exception):
    pass


# ---------------------------------------------------------------------------------------------- workspace

class Workspace:
    """One evidence build + pack, evaluated lazily with stage2.run.

    Loading (session 10). `refresh()` loads, and reloads when any input changed since the last load: the pack, the
    curated inputs (decisions, approvals, readings, clarifications, assumptions, activity templates, amendment files,
    register, dispositions, evidence items), BUILD_MANIFEST.json and every file it records (units.json, the crops,
    ...). A tool call refreshes first (a long-lived MCP server sees a decision recorded after it started), and so does
    every controller step. Between loads, nothing is served from a version whose inputs changed: `check_fresh()` (run
    by every evidence read and by `identity()`) refuses with "workspace stale: reload". The state identity is computed
    from the bytes of the inputs at load time (contract.StateIdentity), and a crop is served only when its bytes are the
    ones the evidence build recorded ("integrity failure" otherwise, never silently)."""

    def __init__(self, evidence: Path | None = None, pack: Path | None = None, root: Path = ROOT,
                 staging: Path | None = None, worklog: Path | None = None, ai_config: Path | None = None):
        self.root = Path(root).resolve()
        self.evidence = Path(evidence or self.root / "build").resolve()
        self.pack = Path(pack or self.root / "config/pack.yaml").resolve()
        self.staging = Path(staging) if staging else self.root / "staging/ai"
        self.worklog = Path(worklog) if worklog else self.root / "worklog/model_calls"
        self.ai_config = ai_config
        self._r = self._key = self._index = self._by_id = None
        self._identity: StateIdentity | None = None
        self._recorded: dict[str, str] = {}        # evidence-build path -> sha256 the build recorded (or, for a crop
        self._unrecorded: dict[str, str] = {}      # the manifest does not record, the sha256 read when loading)
        self._cache: dict = {}

    def _p(self, p) -> Path:
        p = Path(p)
        return p if p.is_absolute() else self.root / p

    def _curated(self, cfg: dict) -> dict:
        """The curated input files and directories the pack names (defaults relative to the repository root)."""
        return {k: self._p(cfg.get(k, d)) for k, d in (
            ("decisions", "curation/reviews/decisions.yaml"), ("approvals", "curation/approvals.yaml"),
            ("clarifications", "curation/clarifications/register.yaml"), ("assumptions", "config/assumptions.yaml"),
            ("activity_templates", "curation/activity_templates.yaml"), ("amendments_dir", "curation/amendments"),
            ("dispositions_dir", "curation/register/dispositions"), ("evidence_items_dir", "curation/evidence_items"),
            ("readings_dir", "curation/readings"), ("register", "curation/register/rows.yaml"))}

    def _input_files(self) -> list[Path]:
        cfg = load_yaml(self.pack) or {}
        c = self._curated(cfg)
        man = self.evidence / "BUILD_MANIFEST.json"
        files = [self.pack, man] + [c[k] for k in ("decisions", "approvals", "clarifications", "assumptions",
                                                  "activity_templates")]
        for k in ("amendments_dir", "dispositions_dir", "evidence_items_dir", "readings_dir"):
            files += sorted(c[k].glob("**/*.yaml")) if c[k].is_dir() else []
        reg = c["register"].parent
        files += sorted(reg.glob("**/*.yaml")) if reg.is_dir() else []
        try:                                       # session 10: the curated relationships stage2.run reads, if any
            from .. import relationships
            files.append(relationships.default_path(cfg, self.root))
        except (ImportError, AttributeError):
            pass
        try:
            outputs = json.loads(man.read_text(encoding="utf-8")).get("outputs") or {}
        except (OSError, ValueError):
            outputs = {}
        files += [self.evidence / p for p in sorted(outputs)]
        return files

    def _inputs_key(self) -> tuple:
        out = []
        for f in self._input_files():
            try:
                st = f.stat()
                out.append((str(f), st.st_mtime_ns, st.st_size, st.st_ino))
            except OSError:
                out.append((str(f), None, None, None))
        return tuple(out)

    def refresh(self) -> dict:
        """Load, or reload when any input changed since the last load (see the class docstring). The inputs are keyed
        before and after loading; a change while loading is loaded again once, then refused."""
        key = self._inputs_key()
        if self._r is not None and key == self._key:
            return self._r
        for _ in range(2):
            r = stage2.run(self.evidence, self.pack, self.root)
            identity, recorded, unrecorded = self._identity_of(r)
            after = self._inputs_key()
            if after == key:
                self._r, self._key, self._identity = r, key, identity
                self._recorded, self._unrecorded = recorded, unrecorded
                self._index = self._by_id = None
                self._cache = {}
                return r
            key = after
        raise ToolError("workspace stale: reload (its inputs kept changing while they were being loaded)")

    def _identity_of(self, r: dict) -> tuple[StateIdentity, dict, dict]:
        """The state identity from the bytes of the inputs as loaded, the sha256 the evidence build recorded for each
        file it wrote, and the sha256 (read now) of any crop the units name that the build did not record."""
        cfg, c = r["cfg"], self._curated(r["cfg"])
        man = self.evidence / "BUILD_MANIFEST.json"
        recorded = dict(json.loads(man.read_text(encoding="utf-8")).get("outputs") or {})
        unrecorded = {}
        for rel in sorted({rel for u in r["units"] for _, rel, _ in _crop_paths(u)} - set(recorded)):
            p = (self.evidence / rel).resolve()
            if p.is_relative_to(self.evidence) and p.is_file():
                unrecorded[rel] = sha256_file(p)
        order = r["order"]
        upto = order.index(r["working"].stage) if r["working"] else len(order)
        amend_dir = c["amendments_dir"]
        amendments = [amend_dir / f"{a}.yaml" for a in order[1:upto]]
        readings = [c["approvals"]] + (sorted(c["readings_dir"].glob("*.yaml")) if c["readings_dir"].is_dir() else [])
        dec = Path(r["decisions_file"])
        ident = StateIdentity(pack_id=str(cfg.get("pack_id") or self.pack.stem), evidence_build_id=sha256_file(man),
                              validated_stage=r["validated"].stage,
                              working_stage=r["working"].stage if r["working"] else None,
                              decisions_sha256=sha256_file(dec) if dec.exists() else None,
                              assumptions_sha256=_sha_or_none(c["assumptions"]),
                              activity_templates_sha256=_sha_or_none(c["activity_templates"]),
                              readings_sha256=_files_sha(readings), amendments_sha256=_files_sha(amendments),
                              unrecorded_crops_sha256=_files_sha([], unrecorded) if unrecorded else None)
        return ident, recorded, unrecorded

    def check_fresh(self) -> None:
        """Refuse ("workspace stale: reload") when any input changed since the workspace was loaded: nothing is served
        from a version whose inputs changed (refresh() reloads; a tool call does that first)."""
        if self._r is None:
            return
        key = self._inputs_key()
        if key == self._key:
            return
        old, new = {k[0]: k[1:] for k in self._key}, {k[0]: k[1:] for k in key}
        changed = [self._rel(f) for f in sorted(set(old) | set(new)) if old.get(f) != new.get(f)]
        raise ToolError(f"workspace stale: reload (changed since it was loaded: {', '.join(changed[:4])}"
                        f"{f' and {len(changed) - 4} more' if len(changed) > 4 else ''})")

    def verified(self) -> dict:
        """The loaded run, for an evidence read: the inputs are those loaded (check_fresh) and the evidence build
        verified against its BUILD_MANIFEST.json when it was loaded (E01), else an integrity failure."""
        self.check_fresh()
        r = self.r
        if r["problems"]:
            raise ToolError("integrity failure: the evidence build does not verify against its BUILD_MANIFEST.json "
                            "(E01): " + "; ".join(r["problems"])[:600])
        return r

    def check_file(self, rel: str) -> str:
        """sha256 of an evidence-build file, after checking it is the file the build recorded (or, for a crop the
        manifest does not record, the file read when loading). ToolError otherwise: never served silently."""
        self.r
        p = (self.evidence / rel).resolve()
        if not p.is_relative_to(self.evidence) or not p.is_file():
            raise ToolError(f"integrity failure: {rel} is not a file of the evidence build")
        actual = sha256_file(p)
        expected = self._recorded.get(rel) or self._unrecorded.get(rel)
        if expected is None:
            raise ToolError(f"integrity failure: {rel} is neither recorded in BUILD_MANIFEST.json nor read when the "
                            "workspace was loaded")
        if actual != expected:
            try:
                now = (json.loads((self.evidence / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
                       .get("outputs") or {}).get(rel)
            except (OSError, ValueError):
                now = None
            if now == actual:
                raise ToolError(f"workspace stale: reload (the evidence build was rebuilt since it was loaded: {rel})")
            raise ToolError(f"integrity failure: {rel} (sha256 {actual[:16]}…) is not the file the evidence build "
                            f"recorded (sha256 {expected[:16]}…): it was replaced or edited after the build; nothing "
                            "served")
        return actual

    def memo(self, key, fn):
        """A value computed once per loaded version (cleared on reload)."""
        self.r
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    def _rel(self, f: str) -> str:
        p = Path(f)
        for base, tag in ((self.evidence, "evidence build: "), (self.root, "")):
            if p.is_relative_to(base):
                return tag + p.relative_to(base).as_posix()
        return p.name

    @property
    def r(self) -> dict:
        return self._r if self._r is not None else self.refresh()

    def require_ok(self) -> dict:
        r = self.r
        if r["problems"]:
            raise Refused("E01: the evidence build is not usable: " + "; ".join(r["problems"])[:600])
        return r

    @property
    def units_by_id(self) -> dict:
        r = self.r
        if self._by_id is None:
            self._by_id = {u["unit_id"]: u for u in r["units"]}
        return self._by_id

    def identity(self) -> StateIdentity:
        """The state identity of the loaded inputs; refused ("workspace stale: reload") when they changed since."""
        self.r
        self.check_fresh()
        return self._identity.model_copy()

    def stage_name(self, stage: str | None) -> str:
        r = self.r
        if stage in (None, "", "validated"):
            return r["validated"].stage
        if stage in ("working", "latest"):
            return r["order"][-1]
        if stage not in r["order"]:
            raise ToolError(f"unknown stage {stage!r}; stages: {r['order']} (or 'validated', 'latest')")
        return stage

    def stage(self, name: str):
        return next(s for s in self.r["stages"] if s.stage == self.stage_name(name))

    def prev_stage(self, addendum: str) -> str:
        order = self.r["order"]
        if addendum not in order:
            raise ToolError(f"{addendum} is not a stage of this pack ({order})")
        return order[order.index(addendum) - 1]

    def order_index(self) -> dict[str, int]:
        return {u["unit_id"]: i for i, u in enumerate(self.r["units"])}

    def addenda(self) -> list[str]:
        return [s for s in self.r["order"] if s != amend.BASE]


def _sha_or_none(p: Path) -> str | None:
    return sha256_file(p) if Path(p).is_file() else None


def _files_sha(paths: list[Path], named: dict[str, str] | None = None) -> str:
    """One sha256 over files, by name and content (a disposable copy with the same files has the same value); an
    absent file counts as absent. `named` adds {name: sha256} pairs already computed."""
    h = hashlib.sha256()
    pairs = [(Path(p).name, sha256_file(p) if Path(p).is_file() else "absent") for p in paths]
    for name, sha in sorted(pairs) + sorted((named or {}).items()):
        h.update(f"{name}\0{sha}\n".encode("utf-8"))
    return h.hexdigest()


def _crop_paths(u: dict) -> list[tuple[str, str, str | None]]:
    """(kind, path in the evidence build, column) of every image file a unit names."""
    found: list[tuple[str, str, str | None]] = []
    region = u.get("region")
    if region:
        found += [("native", f"regions/{region}/native.png", None), ("region_crop", f"regions/{region}/crop.png", None)]
    for a in u.get("anchors", []):
        if a.get("crop"):
            found.append(("unit", a["crop"], None))
        for col, c in (a.get("cell_crops") or {}).items():
            if c:
                found.append(("cell", c, col))
    return list(dict.fromkeys(found))


def _num(addendum: str) -> int:
    return int(addendum.split("-")[1])


def _short(t: str | None, n: int = 400) -> str:
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


# ---------------------------------------------------------------------------------------------- search

_TOKEN = re.compile(r"\d+(?:[.:,/-]\d+)*|[^\W\d_]+")


def match_form(text: str) -> str:
    """The form used for MATCHING only (never shown as evidence): Arabic via normalize_arabic, Latin via
    normalize_latin, lower case."""
    return (normalize_arabic(text) if has_arabic(text) else normalize_latin(text)).lower()


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(match_form(text or ""))


def _index(ws: Workspace) -> dict:
    r = ws.r
    if ws._index is not None:
        return ws._index
    docs = []
    df: Counter = Counter()
    for i, u in enumerate(r["units"]):
        text, tr = u.get("text") or "", u.get("translation") or ""
        toks, ttoks = set(_tokens(text)), set(_tokens(tr))
        df.update(toks | ttoks)
        docs.append((i, u, toks, ttoks, match_form(text), match_form(tr)))
    ws._index = {"docs": docs, "df": df, "n": len(docs)}
    return ws._index


def search_evidence(ws: Workspace, query: str, docs: list[str] | None = None, kinds: list[str] | None = None,
                    limit: int = 20) -> dict:
    q = query.strip()
    if not q:
        raise ToolError("empty query")
    ws.verified()
    limit = max(1, min(int(limit), 50))
    idx = _index(ws)
    qt = list(dict.fromkeys(_tokens(q)))
    qform = match_form(q)
    idf = {t: math.log((idx["n"] + 1) / (idx["df"].get(t, 0) + 1)) + 1 for t in qt}
    hits = []
    for i, u, toks, ttoks, form, tform in idx["docs"]:
        if docs and u["doc"] not in docs or kinds and u["kind"] not in kinds:
            continue
        common = [t for t in qt if t in toks]
        score = sum(idf[t] for t in common)
        phrase = bool(qform) and qform in form
        if phrase:
            score += sum(idf.values()) * 2
        where = "text"
        if not common and not phrase:
            tcommon = [t for t in qt if t in ttoks]
            if not tcommon:
                continue
            score, where = sum(idf[t] for t in tcommon) * 0.5, "translation"
        hits.append((-round(score, 6), i, u, where, phrase, common))
    hits.sort(key=lambda h: (h[0], h[1]))
    out = []
    for neg, i, u, where, phrase, common in hits[:limit]:
        src = (u.get("text") or "") if where == "text" else (u.get("translation") or "")
        form = match_form(src)
        pos = form.find(qform) if phrase else (form.find(common[0]) if common else 0)
        a = max(0, pos - 100)
        out.append({"unit_id": u["unit_id"], "doc": u["doc"], "pages": u.get("pages", []), "kind": u["kind"],
                    "score": -neg, "matched_in": where, "phrase": phrase,
                    "snippet": ("…" if a else "") + src[a:a + 260] + ("…" if a + 260 < len(src) else "")})
    return {"query": q, "results": out, "total_hits": len(hits),
            "note": "matched_in 'translation' is a proposed translation, not evidence; quote the unit's source text"}


# ---------------------------------------------------------------------------------------------- units and groups

def _ops_info(ws: Workspace, op_ids: list[str]) -> list[dict]:
    reg, reviews = ws.r["register"], ws.r.get("reviews") or {}
    return [{"op": h, "stage": reg.op_stage.get(h), "provision": reg.op_provision.get(h),
             "review": (reviews.get(("op", h)) or {}).get("status")} for h in op_ids]


def get_unit(ws: Workspace, unit_id: str, stage: str | None = None) -> dict:
    ws.verified()                    # never cached text of a version whose inputs changed, or of an unverified build
    s = ws.stage(stage)
    u = ws.units_by_id.get(unit_id)
    us = s.state.get(unit_id)
    if u is None and us is None:
        raise ToolError(f"no unit {unit_id!r} (search_evidence finds unit ids)")
    out = {"unit_id": unit_id, "stage": s.stage, "doc": (u or {}).get("doc") or us.doc,
           "kind": (u or {}).get("kind") or us.kind, "label": (u or {}).get("label") or (us.label if us else None),
           "parent": (u or {}).get("parent") or (us.parent if us else None),
           "pages": (u or {}).get("pages") or (us.pages if us else []),
           "origin": (u or {}).get("origin") or (us.origin if us else None),
           "text_as_issued": (u or {}).get("text"), "cells_as_issued": (u or {}).get("cells")}
    if us is not None:
        out.update({"status": us.status, "effective_text": us.text if us.status != "not_issued" else None,
                    "effective_cells": us.cells, "number": us.number, "superseded_by": us.superseded_by,
                    "issued_by": us.issued_by, "history": _ops_info(ws, us.history),
                    "annotations": _ops_info(ws, us.annotations)})
    else:
        out.update({"status": "absent at this stage"})
    if u is not None:
        out["anchors"] = [{"page": a.get("page"), "bbox": a.get("bbox"), "has_crop": bool(a.get("crop"))}
                          for a in u.get("anchors", [])]
        try:
            out["heading"] = amend.heading_of([x["unit_id"] for x in ws.r["units"]], s.state, unit_id)
        except (ValueError, KeyError):
            out["heading"] = None
        if u.get("origin") == "image_reading":
            rd = u.get("reading") or {}
            out["reading"] = {"region": rd.get("region"), "status": rd.get("status"), "lang": u.get("lang"),
                              "source_text": u.get("text"), "translation": u.get("translation"),
                              "match_text": u.get("normalized"), "uncertain": u.get("uncertain"),
                              "numerals": u.get("numerals"), "context": u.get("context"),
                              "note": "source_text is what the image prints (Arabic in logical order) and is the only "
                                      "evidence; translation is proposed and match_text is for matching only"}
    return out


def _sorted_members(ws: Workspace, ids) -> list[str]:
    pos = ws.order_index()

    def key(k):
        base = k.split("+")[0]
        return (pos.get(k, pos.get(base, 10 ** 9) + 0.5), k)
    return sorted(ids, key=key)


def get_group(ws: Workspace, group_id: str, stage: str | None = None) -> dict:
    ws.verified()
    s = ws.stage(stage)
    members = _sorted_members(ws, amend.group_members(s.state, group_id))
    if not members:
        raise ToolError(f"no group {group_id!r} at {s.stage} (a table, form, list or section id such as VOL-II:T2-2)")
    doc, _, local = group_id.partition(":")
    head = s.state.get(f"{doc}:H:{local}")
    rows, context = [], None
    for k in members[:200]:
        x = s.state[k]
        u = ws.units_by_id.get(k) or {}
        context = context or u.get("context")
        rows.append({"unit_id": k, "kind": x.kind, "label": x.label, "status": x.status,
                     "text": x.text if x.status != "not_issued" else _short(x.text, 300) + " [not issued at this stage]",
                     "cells": x.cells, "pages": x.pages})
    return {"group_id": group_id, "stage": s.stage, "heading": {"unit_id": f"{doc}:H:{local}", "text": head.text} if head else None,
            "title": amend._group_title(s.state, group_id), "members": rows, "count": len(members),
            "notes": [k for k in members if s.state[k].kind in ("note", "note_intro") or "/note" in k],
            "image_table_context": context}


def get_crop(ws: Workspace, unit_id: str) -> dict:
    """The unit's image files, each checked against the sha256 the evidence build recorded (Workspace.check_file): a
    file replaced or edited after the build is an integrity failure (ToolError), never served; then the workspace must
    be fresh and the build verified (Workspace.verified)."""
    u = ws.units_by_id.get(unit_id)
    if u is None:
        raise ToolError(f"no unit {unit_id!r} in the evidence build")
    region = u.get("region")
    base = ws.evidence
    crops = []
    for kind, rel, col in _crop_paths(u):
        p = (base / rel).resolve()
        if not p.is_relative_to(base) or not p.is_file():
            continue                                         # outside the evidence build, or missing: never returned
        sha = ws.check_file(p.relative_to(base).as_posix())
        crops.append({"kind": kind, "path": str(p), "path_in_build": p.relative_to(base).as_posix(),
                      "sha256": sha, "column": col, "media_type": "image/png"})
    ws.verified()
    if not crops:
        raise ToolError(f"no image crop for {unit_id}: it is a text-layer unit (its words are in get_unit) or its crop "
                        "is not in the evidence build")
    return {"unit_id": unit_id, "region": region, "page": (u.get("pages") or [None])[0], "crops": crops}


# ---------------------------------------------------------------------------------------------- state comparison

def compare_state(ws: Workspace, from_stage: str, to_stage: str) -> dict:
    from .. import live
    r = ws.verified()
    a, b = ws.stage(from_stage), ws.stage(to_stage)
    md, data = live.diff(r, a.stage, b.stage)
    units = []
    for k in _sorted_members(ws, set(a.state) | set(b.state)):
        x, y = a.state.get(k), b.state.get(k)
        if x is not None and y is not None and x.sha() == y.sha() and x.annotations == y.annotations and x.number == y.number:
            continue
        rec = {"unit": k, "status": f"{x.status if x else 'absent'} -> {y.status if y else 'absent'}"}
        if (x.text if x else "") != (y.text if y else ""):
            rec["text_before"], rec["text_after"] = _short(x.text if x else "", 300), _short(y.text if y else "", 300)
        if (x.cells if x else None) != (y.cells if y else None):
            rec["cells"] = {c: [(x.cells or {}).get(c) if x else None, (y.cells or {}).get(c)]
                            for c in set((x.cells or {}) if x else {}) | set(y.cells or {} if y else {})
                            if ((x.cells or {}).get(c) if x else None) != ((y.cells or {}).get(c) if y else None)}
        if y is not None:
            rec["ops"] = [h for h in y.history if not x or h not in x.history]
            rec["annotations_added"] = [h for h in y.annotations if not x or h not in x.annotations]
            if y.number != (x.number if x else None):
                rec["number"] = y.number
        units.append(rec)
    if isinstance(data.get("programme"), list):
        data["programme"] = data["programme"][:100]
    return {"from": a.stage, "to": b.stage, "diff": data, "markdown": md[:20000], "units": units[:300],
            "units_total": len(units)}


# ---------------------------------------------------------------------------------------------- calculations

CALC_KINDS = ("relative_date", "working_days_between", "add_working_days", "is_working_day", "printed_date")


def _iso(v, what: str) -> date:
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        raise ToolError(f"{what} must be an ISO date (YYYY-MM-DD), got {v!r}") from None


def computed_under(ws: Workspace) -> dict:
    """What a calculation or a simulation states it was computed under: the fingerprint of the state identity (it
    binds the assumptions: calendar, holidays, counting policy; the amendment files; the evidence build; ...) and the
    parts of it a date depends on. A result whose fingerprint differs from the current state's was made under other
    inputs."""
    ident = ws.identity()
    return {"inputs_fingerprint": ident.fingerprint(),
            "computed_under": {k: getattr(ident, k) for k in ("evidence_build_id", "assumptions_sha256",
                                                              "amendments_sha256", "validated_stage", "working_stage")}}


def calculate(ws: Workspace, kind: str, args: dict) -> dict:
    r = ws.verified()
    return {**_calculate(ws, r, kind, args), **computed_under(ws)}


def _calculate(ws: Workspace, r: dict, kind: str, args: dict) -> dict:
    last = r["order"][-1]
    cal = r["register"].cal_by_stage.get(last, r["cal"])
    calinfo = {"weekend": sorted(cal.weekend), "holidays": sorted(h.isoformat() for h in cal.holidays),
               "notified_by_addenda": sorted((r.get("non_working_days") or {}).get(last) or []),
               "basis": f"VOL-I 2.4 Working Days (Sunday to Thursday); holidays from the pack's assumptions and the days notified by the addenda applied at {last}"}
    allowed = {"relative_date": {"anchor_date", "offset", "unit", "direction", "purpose"},
               "working_days_between": {"from", "to"}, "add_working_days": {"date", "n"},
               "is_working_day": {"date"}, "printed_date": {"unit_id", "stage"}}
    if kind not in allowed:
        raise ToolError(f"calculate kind must be one of {CALC_KINDS}; free-text arithmetic is not offered")
    extra = set(args) - allowed[kind]
    if extra:
        raise ToolError(f"unknown arguments for {kind}: {sorted(extra)}")
    if kind == "relative_date":
        x = _iso(args.get("anchor_date"), "anchor_date")
        n = args.get("offset")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ToolError("offset must be a positive integer (the direction gives the sign)")
        try:
            rule = DateRule(rule_id="CALC", kind="relative", purpose=args.get("purpose", "deadline"), anchor="X",
                            offset=n, unit=args.get("unit", "calendar_day"), direction=args.get("direction", "after"))
        except ValueError as e:
            raise ToolError(str(e)) from None
        ins = interpretations(rule, {"X": x}, cal)
        plan = planning_value(rule, ins, r["policy"])
        return {"kind": kind, "inputs": args, "readings": [{"key": i.key, "label": i.label, "value": i.value.isoformat()
                                                            if i.value else None, "basis": i.basis} for i in ins],
                "planning": {"key": plan.key, "value": plan.value.isoformat() if plan.value else None,
                             "policy": r["policy"]},
                "readings_differ": len({i.value for i in ins}) > 1, "calendar": calinfo}
    if kind == "working_days_between":
        a, b = _iso(args.get("from"), "from"), _iso(args.get("to"), "to")
        return {"kind": kind, "inputs": args, "result": cal.working_days_between(a, b),
                "convention": "Working Days in (from, to]: from not counted, to counted", "calendar": calinfo}
    if kind == "add_working_days":
        d, n = _iso(args.get("date"), "date"), args.get("n")
        if not isinstance(n, int) or isinstance(n, bool):
            raise ToolError("n must be an integer")
        v = cal.add_working_days(d, n)
        return {"kind": kind, "inputs": args, "result": v.isoformat(), "long": long_date(v),
                "convention": "the |n|-th Working Day after (n>0) or before (n<0); the date itself is never counted",
                "calendar": calinfo}
    if kind == "is_working_day":
        d = _iso(args.get("date"), "date")
        return {"kind": kind, "inputs": args, "result": cal.is_working_day(d), "long": long_date(d), "calendar": calinfo}
    s = ws.stage(args.get("stage"))
    u = s.state.get(args.get("unit_id"))
    if u is None:
        raise ToolError(f"no unit {args.get('unit_id')!r} at {s.stage}")
    try:
        p = parse_date(u.text)
    except ValueError as e:
        return {"kind": kind, "inputs": args, "result": None, "problem": str(e)}
    return {"kind": kind, "inputs": args, "stage": s.stage, "result": p[0].isoformat() if p else None,
            "time": p[1] if p else None, "long": long_date(p[0]) if p else None,
            "note": "the first date printed in the unit's effective text, and the first HH:MM time in it"}


# ---------------------------------------------------------------------------------------------- simulation

def _issued_from(ws: Workspace, addendum: str) -> str:
    f = next((f for f in ws.r["opfiles"] if f.addendum == addendum), None)
    if f is not None:
        return f.issued_from
    from ..draft import draft
    return draft(ws.r["units"], addendum).issued_from


def simulate(ws: Workspace, addendum: str, ops: list[dict], dispositions: list[dict]) -> tuple[dict, dict | None]:
    """Dry run of an addendum's proposed ops over the state before it (earlier addenda as the pack has them).
    Returns (summary, the evaluated copy of the run) — the copy is the controller's input for impact; nothing is
    written anywhere."""
    from ..amend import Disposition, Op, OpFile, unevidenced_additions
    ws.check_fresh()
    r = ws.require_ok()
    if addendum not in r["order"] or addendum == amend.BASE:
        raise ToolError(f"{addendum} is not an addendum of this pack ({r['order'][1:]})")
    parsed, disps, errors = [], [], []
    for i, o in enumerate(ops or []):
        o = dict(o)
        o["review"], o["reviewer"] = "proposed", None              # a simulation never carries a review flag
        o.setdefault("origin", "assistant")
        try:
            parsed.append(Op.model_validate(o))
        except ValidationError as e:
            errors.append({"index": i, "id": o.get("id"), "error": _short(str(e), 600)})
    for i, d in enumerate(dispositions or []):
        d = dict(d)
        d.setdefault("origin", "assistant")
        try:
            disps.append(Disposition.model_validate(d))
        except ValidationError as e:
            errors.append({"index": i, "disposition": d.get("provision"), "error": _short(str(e), 600)})
    f = OpFile(addendum=addendum, issued_from=_issued_from(ws, addendum),
               prepared_by="AI proposal dry run (tenderpack.ai.tools.simulate; nothing persisted)",
               method="simulate_amendment", ops=parsed, dispositions=disps)
    r2 = dict(r)
    r2.pop("_unit_evidence", None)
    r2["opfiles"] = [x for x in r["opfiles"] if _num(x.addendum) < _num(addendum)] + [f]
    try:
        stage2.evaluate(r2)
    except Exception as e:                                       # noqa: BLE001 (reported, never retried with changes)
        raise ToolError(f"the engine dry run failed: {type(e).__name__}: {_short(str(e), 400)}") from None
    i = r2["order"].index(addendum)
    s, prev = r2["stages"][i], r2["stages"][i - 1]
    c47 = unevidenced_additions(prev.state, s.state, addendum)
    by_unit: dict[str, list[str]] = {}
    for x in c47:
        by_unit.setdefault(x.split(": '", 1)[0], []).append(x)
    out_ops = []
    for x in s.ops:
        out_ops.append({"id": x.op.id, "provision": x.op.provision, "type": x.op.type,
                        "target": x.op.target or x.op.anchor or x.op.new_group or (x.op.targets or [None])[0],
                        "valid": x.valid, "withdrawn": x.withdrawn, "applied": x.applied, "checks": x.checks,
                        "failed": [c for c in x.checks if not c["ok"]], "changed": list(x.changed),
                        "content": list(x.details.get("content") or []),
                        "c47": [f for k in x.changed for f in by_unit.get(k, [])],
                        "details": {k: v for k, v in x.details.items() if k in ("old_value", "cell", "also_in", "cited",
                                                                              "renumbered", "evidence", "mentions")}})
    changed = sorted({k for x in s.ops if x.applied for k in x.changed})
    cov = [{"provision": c["provision"], "disposition": c["disposition"], "accounted_by": c["accounted_by"]}
           for c in s.coverage]
    return ({"addendum": addendum, "from_stage": prev.stage, "status": s.status, "ops": out_ops,
             "parse_errors": errors, "coverage": cov,
             "unaccounted": [c["provision"] for c in s.coverage if c["disposition"] == "UNACCOUNTED"],
             "c47_unevidenced_additions": c47, "scope_leak": list(s.scope_leak), "problems": list(s.problems),
             "changed_units": changed,
             "c46_needs": [{"op": t["op"], "output": t["output"], "rows": t.get("rows", []), "detail": _short(t["detail"], 300)}
                           for t in r2.get("trace", []) if t["stage"] == addendum],
             "note": "dry run: nothing persisted; validity is structural (C21-C27, C47), not acceptance",
             **computed_under(ws)}, r2)


def simulate_amendment(ws: Workspace, addendum: str, ops: list[dict] | None = None,
                       dispositions: list[dict] | None = None) -> dict:
    return simulate(ws, addendum, ops or [], dispositions or [])[0]


def simulate_programme(ws: Workspace, stage: str | None = None) -> dict:
    from .. import programme
    ws.check_fresh()
    r = ws.require_ok()
    st = ws.stage_name(stage)
    try:
        p = programme.stage_planner(r, st, extended=True)(r["assumptions"])
    except Exception as e:                                       # noqa: BLE001
        raise ToolError(f"the programme cannot be planned at {st}: {type(e).__name__}: {_short(str(e), 300)}") from None
    acts = p["activities"]
    return {"stage": st, "status_date": p.get("status_date"), "planning_basis": p.get("planning_basis"),
            "milestones": [{k: m.get(k) for k in ("id", "date", "time", "short", "source", "reading", "readings_differ",
                                                 "conditional")} for m in (p.get("milestones") or [])][:60],
            "infeasible": [{k: d.get(k) for k in ("activity", "status", "shortfall_wd", "chain", "deadline", "req_ids")}
                           | {"would_make_feasible": (d.get("would_make_feasible") or [])[:3]}
                           for d in (p.get("drivers") or [])][:30],
            "activity_status_counts": dict(Counter(a["status"].split(" ")[0] for a in acts)),
            "activities": len(acts), "problems": (p.get("problems") or [])[:20],
            "note": "every lead time is a PROVISIONAL ASSUMPTION (config/assumptions.yaml); negative float is INFEASIBLE",
            **computed_under(ws)}


def get_state(ws: Workspace) -> dict:
    r = ws.r
    ident = ws.identity()
    return {"state": ident.model_dump(), "inputs_fingerprint": ident.fingerprint(),
            "stages": [{"stage": s.stage, "status": s.status, "issued": s.issued, "ops": len(s.ops),
                        "opfile": s.prepared_by} for s in r["stages"]],
            "evidence_problems": r["problems"],
            "drafted_addenda": sorted(r.get("drafted") or {}),
            "note": "copy `state` into every proposal; a proposal made against another state is stale"}


# ---------------------------------------------------------------------------------------------- controller-backed tools

def validate_proposal(ws: Workspace, proposal: dict) -> dict:
    from . import controller
    return controller.validate_payload(ws, proposal)


def get_task_packet(ws: Workspace, addendum: str, claim: bool = False, provisions: list[str] | None = None,
                    host_model: str | None = None, _caller: str = "cli") -> dict:
    from . import controller
    return controller.host_task(ws, addendum, claim=claim, provisions=provisions, host_model=host_model,
                                pid=os.getpid() if _caller == "mcp" else None)


def request_review(ws: Workspace, proposal_set: dict, host_model: str | None = None, _caller: str = "cli") -> dict:
    from . import controller
    return controller.submit(ws, proposal_set, host_model=host_model or proposal_set.get("model_requested") or "undeclared",
                             via=_caller)


def submit_proposals(ws: Workspace, proposal_set: dict, host_model: str, _caller: str = "cli") -> dict:
    from . import controller
    return controller.submit(ws, proposal_set, host_model=host_model, via=_caller)


# ---------------------------------------------------------------------------------------------- registry

def _obj(props: dict, required: list[str] = ()) -> dict:
    return {"type": "object", "properties": props, "required": list(required), "additionalProperties": False}


S, I, B = {"type": "string"}, {"type": "integer"}, {"type": "boolean"}
SA = {"type": "array", "items": {"type": "string"}}
STAGE = {"type": ["string", "null"], "description": "a stage name (BASE, ADD-01, ...), 'validated' (default) or 'latest'"}


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    fn: Callable
    writes: bool = False          # writes to staging only
    model: bool = True            # offered to application-route models

    def spec(self) -> dict:
        return {"name": self.name, "description": self.description, "input_schema": self.input_schema}


TOOLS: dict[str, Tool] = {t.name: t for t in [
    Tool("search_evidence", "Rank units by token overlap with the query (deterministic; no embeddings). Returns unit ids, "
         "document, pages, kind and a snippet. Use get_unit for the full text.",
         _obj({"query": S, "docs": SA, "kinds": SA, "limit": I}, ["query"]), search_evidence),
    Tool("get_unit", "One unit: text as issued and effective text at a stage, cells, pages, status, the ops that "
         "changed or annotate it; for an image reading the source text, translation and match text separately.",
         _obj({"unit_id": S, "stage": STAGE}, ["unit_id"]), get_unit),
    Tool("get_group", "Members of a table, form, list or section (e.g. VOL-II:T2-2) with cells, heading and notes.",
         _obj({"group_id": S, "stage": STAGE}, ["group_id"]), get_group),
    Tool("get_crop", "Path and sha256 of the native image and crops of an image-read unit (refused for text-layer "
         "units). A vision-capable provider is shown the image.", _obj({"unit_id": S}, ["unit_id"]), get_crop),
    Tool("compare_state", "What changed between two stages: requirements, stale rows, A3, programme, and every unit "
         "whose status, text, cells or annotations differ.", _obj({"from_stage": S, "to_stage": S},
                                                                  ["from_stage", "to_stage"]), compare_state),
    Tool("calculate", "Approved date calculations only (VOL-I 2.4 calendar): kind relative_date {anchor_date, offset, "
         "unit, direction, purpose} gives every counting reading; working_days_between {from, to}; add_working_days "
         "{date, n}; is_working_day {date}; printed_date {unit_id, stage}.",
         _obj({"kind": {"type": "string", "enum": list(CALC_KINDS)}, "args": {"type": "object"}}, ["kind", "args"]),
         calculate),
    Tool("simulate_amendment", "Dry-run proposed ops (amend.Op objects) and dispositions for an addendum through the "
         "amendment engine over the state before it. Returns per-op validity with check records (C21-C27), C47, "
         "scope leak, coverage, changed units and C46 needs. Nothing is persisted.",
         _obj({"addendum": S, "ops": {"type": "array", "items": {"type": "object"}},
               "dispositions": {"type": "array", "items": {"type": "object"}}}, ["addendum"]), simulate_amendment),
    Tool("simulate_programme", "The A5 programme at a stage, read-only: milestones and infeasible chains.",
         _obj({"stage": STAGE}), simulate_programme),
    Tool("validate_proposal", "The controller's validation of one ChangeProposal (or a whole ProposalSet) against the "
         "current state; returns the controller's verification statuses. Writes nothing.",
         _obj({"proposal": {"type": "object"}}, ["proposal"]), validate_proposal),
    Tool("get_state", "The state identity to copy into proposals, the stages and the addenda statuses.",
         _obj({}), get_state, model=False),
    Tool("get_task_packet", "The task packet for an addendum (provisions, candidate targets, the pattern drafter's "
         "unverified output, the schema). claim=true takes the addendum's orchestrator lock for the host route "
         "(written in staging only).",
         _obj({"addendum": S, "claim": B, "provisions": SA, "host_model": S}, ["addendum"]), get_task_packet,
         writes=True, model=False),
    Tool("request_review", "Validate a ProposalSet and write it to staging/ai/<run_id>/ for a person's review "
         "(never curation/). Releases the host lock on the addendum.",
         _obj({"proposal_set": {"type": "object"}, "host_model": S}, ["proposal_set"]), request_review,
         writes=True, model=False),
    Tool("submit_proposals", "The host route's submission: the same as request_review with the host model declared.",
         _obj({"proposal_set": {"type": "object"}, "host_model": S}, ["proposal_set", "host_model"]), submit_proposals,
         writes=True, model=False),
]}
MODEL_TOOLS = [n for n, t in TOOLS.items() if t.model]

_PY = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict,
       "null": type(None)}


def check_args(schema: dict, args) -> None:
    if not isinstance(args, dict):
        raise ToolError("arguments must be a JSON object")
    props = schema.get("properties", {})
    unknown = sorted(set(args) - set(props))
    if unknown:
        raise ToolError(f"unknown argument(s) {unknown}; allowed: {sorted(props)}")
    missing = [k for k in schema.get("required", []) if k not in args]
    if missing:
        raise ToolError(f"missing argument(s) {missing}")
    for k, v in args.items():
        types = props[k].get("type")
        types = types if isinstance(types, list) else [types] if types else []
        if types and not any(isinstance(v, _PY[t]) and not (t in ("integer", "number") and isinstance(v, bool))
                             for t in types):
            raise ToolError(f"argument {k} must be {' or '.join(types)}")
        if "enum" in props[k] and v not in props[k]["enum"]:
            raise ToolError(f"argument {k} must be one of {props[k]['enum']}")
        item_t = (props[k].get("items") or {}).get("type")
        if isinstance(v, list) and item_t and not all(isinstance(x, _PY[item_t]) for x in v):
            raise ToolError(f"every item of {k} must be {item_t}")


def call_tool(ws: Workspace, name: str, args: dict | None, caller: str = "model") -> dict:
    """Run one tool. `caller` is model | mcp | cli | controller; a model may call only MODEL_TOOLS."""
    t = TOOLS.get(name)
    if t is None or (caller == "model" and not t.model):
        raise ToolError(f"no tool {name!r} is available to this caller; tools: "
                        f"{MODEL_TOOLS if caller == 'model' else list(TOOLS)}")
    args = dict(args or {})
    check_args(t.input_schema, args)
    if name not in STATELESS:                    # the region tools read a (possibly refused) build's files only
        ws.refresh()
    if name in ("get_task_packet", "request_review", "submit_proposals"):
        args["_caller"] = caller
    try:
        return t.fn(ws, **args)
    except (ToolError, Refused):
        raise
    except KeyError as e:
        raise ToolError(f"{name}: not found: {e}") from None


# ---------------------------------------------------------------------------------------------- region tools (s10)
# The workflow's readings step (tenderpack/ai/regionread.py): an addendum image region with no reading stops ingest
# (C05); these read the refused build's region evidence (and nothing of the stage 2 state, which such a build does not
# have) so a host can propose a reading. Offered over MCP and to the readings step; not to the amendment proposer.

def _get_region(ws: Workspace, region_id: str, bands: list[int] | None = None, cells: bool = False) -> dict:
    from .regionread import tool_get_region
    return tool_get_region(ws, region_id, bands, cells)


def _validate_reading(ws: Workspace, reading: dict) -> dict:
    from .regionread import tool_validate_reading
    return tool_validate_reading(ws, reading)


STATELESS = {"get_region", "validate_reading"}
TOOLS["get_region"] = Tool(
    "get_region", "An image region of the evidence build (also a refused one): doc, page, bbox, native image sha256 and "
    "size, the text and rule bands measured from pixels with their crops, the ruled grid if any, a content-type guess, "
    "and its images (the native image and the page context; or the band crops asked for with `bands`, at most three "
    "images per call, and the cell crops with `cells`). Every file is checked against BUILD_MANIFEST.json.",
    _obj({"region_id": S, "bands": {"type": "array", "items": {"type": "integer"}}, "cells": B}, ["region_id"]),
    _get_region, model=False)
TOOLS["validate_reading"] = Tool(
    "validate_reading", "Check a draft reading of an image region (a tenderpack Reading: the shape of the pack's own "
    "readings) with readings.check_reading: the region and native image, the ruled grid, every text band read, Arabic "
    "stored in logical order with a separate translation, numerals in their visual order, table structure. Returns "
    "the findings; writes nothing; nothing is approved.",
    _obj({"reading": {"type": "object"}}, ["reading"]), _validate_reading, model=False)

