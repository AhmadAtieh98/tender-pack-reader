"""Explicit, local interview demo: frozen inputs, reversible decisions, native validation.

Assumptions never invent an answer or bypass evidence/quote/staleness checks. The
owner has authorised simulated approvals for this profile, not real tender release.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

import yaml

from . import review, stage2
from .util import load_yaml

DEMO_REVIEWER = "Interview demo assumption"
DEMO_NOTE = "Assumed approved for an interview demonstration on the owner's instruction; no observed human review."
DEMO_BANNER = "INTERVIEW DEMO: approvals assumed for demonstration; not an actual human review or tender release."
TREES = ("config", "curation", "sources", "build", "out")


class InterviewError(ValueError):
    pass


def confined(root: Path, path: Path) -> Path:
    root = Path(root).resolve()
    p = (root / path).resolve()
    if not p.is_relative_to(root) or p == root:
        raise InterviewError(f"path is outside the operating copy: {path}")
    return p


def require_demo(pack: Path) -> dict:
    cfg = load_yaml(pack) or {}
    if cfg.get("interview_demo") is not True:
        raise InterviewError("this operation requires an explicitly enabled interview demo copy")
    return cfg


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]


def require_idle(root: Path) -> None:
    from .ai.candidate import lock_live
    for p in (root / "staging").glob("**/run.lock"):
        if lock_live(p.parent):
            raise InterviewError("an AI run is active; inspect decisions now and apply changes after it finishes")


def atomic_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str) + "\n")
    tmp.replace(path)


def mark_outputs(out: Path) -> None:
    """Mark human-facing exports before the atomic publication, including PDFs and A1."""
    import re
    import pymupdf
    a1p = out / "a1/a1.json"
    if a1p.exists():
        from .render import write_a1
        a1 = json.loads(a1p.read_text())
        a1["title"] = "INTERVIEW DEMO — " + a1["title"]
        a1["notice"] = DEMO_BANNER + " " + a1.get("notice", "")
        write_a1(a1, out / "a1")
    for p in out.rglob("*"):
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.suffix == ".html":
            text = p.read_text()
            banner = f'<p style="background:#fff2ce;border:2px solid #a60;padding:8px">{DEMO_BANNER}</p>'
            m = re.search(r"<body[^>]*>", text, re.I)
            p.write_text(text[:m.end()] + banner + text[m.end():] if m else banner + text)
        elif p.suffix == ".md":
            p.write_text("> **" + DEMO_BANNER + "**\n\n" + p.read_text())
        elif p.suffix == ".json":
            data = json.loads(p.read_text())
            if isinstance(data, dict):
                data["_interview_demo"] = DEMO_BANNER
                if p.name == "checks.json" and isinstance(data.get("release"), dict):
                    data["release"]["status"] = "INTERVIEW DEMO (assumed approvals; not a tender release)"
                    data["release"]["note"] = DEMO_BANNER
                atomic_json(p, data)
        elif p.suffix == ".pdf":
            with pymupdf.open(p) as doc:
                for page in doc:
                    page.insert_text((24, 11), DEMO_BANNER, fontsize=7, color=(0.65, 0.2, 0))
                tmp = p.with_suffix(".demo-marked")
                doc.save(tmp)
            tmp.replace(p)
    (out / "INTERVIEW_DEMO.txt").write_text(DEMO_BANNER + "\n" + DEMO_NOTE + "\n")


@contextmanager
def locked(root: Path):
    p = confined(root, Path("staging/interview/edit.lock"))
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e:
            raise InterviewError("another interview change is rebuilding outputs; retry when it finishes") from e
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def manifest(folder: Path) -> dict:
    out = {}
    for p in sorted(folder.rglob("*")):
        if p.is_symlink():
            raise InterviewError(f"baseline cannot contain a symbolic link: {p}")
        if p.is_file():
            out[str(p.relative_to(folder))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def freeze(root: Path) -> dict:
    root = Path(root).resolve()
    cfg = require_demo(root / "config/pack.yaml")
    if any(d.get("doc_id", "").startswith("ADD-") and int(d["doc_id"].split("-")[1]) > 2
           for d in cfg.get("documents", [])):
        raise InterviewError("freeze expects the baseline to stop at ADD02")
    with locked(root):
        dest = confined(root, Path("baseline/ADD02"))
        if dest.exists():
            raise InterviewError("ADD02 is already frozen; refusing to overwrite the baseline")
        tmp = dest.with_name(".preparing-" + stamp())
        for name in TREES:
            src = confined(root, Path(name))
            if src.exists():
                manifest(src)  # reject links before copying, including dangling links
                shutil.copytree(src, tmp / "files" / name)
        info = {"version": 1, "stage": "ADD-02", "demo": True, "created": stamp(),
                "files": manifest(tmp / "files")}
        atomic_json(tmp / "manifest.json", info)
        tmp.rename(dest)
        return info


def verify_frozen(root: Path) -> list[str]:
    d = confined(root, Path("baseline/ADD02"))
    try:
        wanted = json.loads((d / "manifest.json").read_text())["files"]
        got = manifest(d / "files")
    except (OSError, ValueError, KeyError) as e:
        return [f"cannot verify frozen ADD02: {e}"]
    return [p for p in sorted(set(wanted) | set(got)) if wanted.get(p) != got.get(p)]


def restore(root: Path) -> dict:
    root = Path(root).resolve()
    require_demo(root / "config/pack.yaml")
    with locked(root):
        require_idle(root)
        bad = verify_frozen(root)
        if bad:
            raise InterviewError(f"frozen baseline failed its hash check: {bad[:8]}")
        backup = confined(root, Path("staging/interview/history") / stamp())
        backup.mkdir(parents=True)
        replaced = []
        try:
            for name in TREES:
                src = root / "baseline/ADD02/files" / name
                dest = confined(root, Path(name))
                if dest.exists():
                    dest.rename(backup / name)
                replaced.append(name)
                if src.exists():
                    shutil.copytree(src, dest)
        except Exception:
            for name in reversed(replaced):
                dest = root / name
                if dest.exists():
                    shutil.rmtree(dest)
                if (backup / name).exists():
                    (backup / name).rename(dest)
            raise
        info = {"action": "restore", "baseline": "ADD-02", "previous_files": str(backup)}
        atomic_json(backup / "action.json", info)
        return info


def assumption_candidates(r: dict, decisions: list[dict]) -> list[str]:
    # Preserve all operator decisions, including a rejection whose binding changed.
    manual = {(d.get("kind"), d.get("item")) for d in decisions if d.get("origin") != "interview_demo"}
    rejected = {(d.get("kind"), d.get("item")) for d in decisions if d.get("decision") == "reject"}
    return sorted(item for (kind, item), st in r["reviews"].items()
                  if st["status"] in ("proposed", "changed") and (kind, item) not in manual | rejected)


def assume_reviews(root: Path, pack: Path, evidence: Path) -> dict:
    cfg = require_demo(pack)
    path = confined(root, review.decisions_path(cfg, root))
    r = stage2.run(evidence, pack, root)
    decisions = review.load_decisions(path)
    accepted, skipped = [], {}
    # Native decide validates each item. Its output is collected in an isolated ledger
    # so provenance can be added before the single append to the actual ledger.
    temp = confined(root, Path("staging/interview") / (stamp() + ".yaml"))
    temp.parent.mkdir(parents=True, exist_ok=True)
    try:
        for item in assumption_candidates(r, decisions):
            code, msgs = review.decide(r, [item], "accept", DEMO_REVIEWER, DEMO_NOTE, temp)
            if code:
                skipped[item] = msgs
            else:
                accepted.append(item)
        entries = review.load_decisions(temp)
        for entry in entries:
            entry["origin"] = "interview_demo"
        if entries:
            review.record(path, entries)
    finally:
        temp.unlink(missing_ok=True)
    return {"assumed": accepted, "skipped": skipped, "label": DEMO_NOTE}


def assume_reading(root: Path, pack: Path, region_id: str) -> None:
    from .cli import approve
    cfg = require_demo(pack)
    path = confined(root, Path(cfg.get("approvals", "curation/approvals.yaml")))
    code = approve(region_id, DEMO_REVIEWER, DEMO_NOTE, root=root, pack_path=pack,
                   approvals_path=path, confirm_changes=True)
    if code:
        raise InterviewError(f"reading {region_id} failed native approval checks (exit {code})")
    data = load_yaml(path)
    data["approvals"][-1]["origin"] = "interview_demo"
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def catalog(root: Path, pack: Path, evidence: Path) -> dict:
    require_demo(pack)
    r = stage2.run(evidence, pack, root)
    history = r["decisions"]
    items = []
    for (kind, item), st in sorted(r["reviews"].items()):
        binding = st["binding"]
        value = binding.get("row", binding.get("op", binding.get("entry")))
        items.append({"id": item, "kind": kind, "fingerprint": st["fingerprint"],
                      "status": st["status"], "label": review.label(st), "value": value,
                      "evidence": binding, "history": [d for d in history if d.get("kind") == kind and d.get("item") == item]})
    from .readings import load_readings
    cfg = r["cfg"]
    approvals_path = confined(root, Path(cfg.get("approvals", "curation/approvals.yaml")))
    approvals = (load_yaml(approvals_path) or {}).get("approvals", []) if approvals_path.exists() else []
    for rid, (reading, _) in sorted(load_readings(root / cfg.get("readings_dir", "curation/readings")).items()):
        value = reading.model_dump(mode="json")
        statuses = [u["reading"] for u in r["units"] if (u.get("reading") or {}).get("region") == rid]
        subject = statuses[0] if statuses else {}
        records = [a for a in approvals if a.get("region_id") == rid]
        assumed = any(a.get("origin") == "interview_demo" and a.get("subject_sha256") == subject.get("subject_sha256") for a in records)
        binding = {"reading": value, "subject": subject}
        items.append({"id": rid, "kind": "reading", "fingerprint": review.fingerprint(binding),
                      "status": subject.get("status", "pending"),
                      "label": "ASSUMED APPROVED FOR DEMO" if assumed else subject.get("status", "pending"),
                      "value": value, "evidence": binding, "history": records,
                      "actions": ["edit", "accept"]})
    for key, value in r["assumptions"].items():
        if not isinstance(value, dict):
            continue
        items.append({"id": f"assumption:{key}", "kind": "assumption", "fingerprint": review.fingerprint(value),
                      "status": "assumption", "label": "PLANNING ASSUMPTION — not a tender fact", "value": value,
                      "evidence": {"basis": "config/assumptions.yaml", "group": key}, "history": [], "actions": ["edit"]})
    # Include edits as well as decisions; an edited proposal may not yet be approved.
    by_id = {x["id"]: x for x in items}
    for path in sorted((root / "staging/interview/history").glob("*/action.json")):
        rec = json.loads(path.read_text())
        iid = (rec.get("request") or {}).get("item")
        if iid in by_id and rec.get("pack") == str(pack) and rec.get("status") == "current":
            by_id[iid]["history"].append({"action": rec["request"], "previous_value": rec["before"]["value"],
                                         "revision": path.parent.name})
    return {"items": items, "stage": r["order"][-1], "demo": True,
            "findings": stage2.register_findings(r)}


def _item_file(root: Path, cfg: dict, kind: str, item: str) -> tuple[Path, str]:
    from .ai.downstream import find_row
    if kind == "row":
        candidates = find_row(confined(root, Path(cfg.get("register", "curation/register/rows.yaml"))), item)
        key = "rows"
    elif kind == "op":
        candidates = [confined(root, Path(cfg.get("amendments_dir", "curation/amendments"))) / (item.split("/")[0] + ".yaml")]
        key = "ops"
    elif kind == "issue":
        p = confined(root, Path(cfg.get("issues", "curation/register/issues.yaml")))
        candidates = [p, *sorted((p.parent / "issues").glob("*.yaml"))]
        candidates = [f for f in candidates if item in (load_yaml(f) or {}).get("issues", {})]
        key = "issues"
    elif kind == "clarification":
        candidates = [confined(root, Path(cfg.get("clarifications", "curation/clarifications/register.yaml")))]
        key = "clarifications"
    elif kind == "assumption":
        candidates = [confined(root, Path(cfg.get("assumptions", "config/assumptions.yaml")))]
        key = item.split(":", 1)[1]
    elif kind == "reading":
        from .readings import load_readings
        candidates = [load_readings(root / cfg.get("readings_dir", "curation/readings"))[item][1]]
        key = "reading"
    else:
        raise InterviewError(f"unsupported decision kind {kind}")
    if len(candidates) != 1:
        raise InterviewError(f"expected one curated source for {item}; found {len(candidates)}")
    return confined(root, candidates[0]), key


def planning_fields(item: dict) -> list[dict]:
    """Only provisional durations, staff effort and capacity have quick controls."""
    group = item.get("id", "").removeprefix("assumption:")
    allowed = {"lead_times": {"value": "Duration (Working Days)", "effort_wd": "Effort (person-days)"},
               "resources": {"capacity": "Capacity (staff per Working Day)"}}.get(group, {})
    if item.get("kind") != "assumption":
        return []
    return [{"path": f"{key}.{field}", "label": f"{key.replace('_', ' ')} — {label}", "value": value[field]}
            for key, value in item["value"].items() if isinstance(value, dict)
            for field, label in allowed.items()
            if isinstance(value.get(field), (int, float)) and not isinstance(value[field], bool)]


def planning_edit(item: dict, field: str, raw: str, reason: str) -> dict:
    """Patch a whitelisted numeric field of the current, fingerprint-bound value."""
    if field not in {f["path"] for f in planning_fields(item)}:
        raise InterviewError("choose an existing duration, effort or resource capacity")
    if not reason.strip():
        raise InterviewError("a reason is required for a planning assumption")
    try:
        number = float(raw)
    except (TypeError, ValueError):
        raise InterviewError("enter a finite non-negative number") from None
    key, leaf = field.rsplit(".", 1)
    if not math.isfinite(number) or number < 0 or (leaf == "capacity" and number == 0):
        raise InterviewError("enter a finite non-negative number; capacity must be positive")
    if leaf == "value" and not number.is_integer():
        raise InterviewError("duration must be a whole number of Working Days")
    result = copy.deepcopy(item["value"])
    previous = result[key][leaf]
    result[key][leaf] = int(number) if number.is_integer() else number
    basis = "effort_basis" if leaf == "effort_wd" else "basis"
    result[key][basis] = (f"PROVISIONAL ASSUMPTION: {reason.strip()} "
                          f"(interview edit: {leaf} {previous} → {result[key][leaf]}). "
                          f"Previous basis: {result[key].get(basis, 'not recorded')}")
    return result


def apply(root: Path, pack: Path, evidence: Path, out: Path, request: dict) -> dict:
    """Compare-and-swap an item; keep its prior bytes and rebuild before publication."""
    cfg = require_demo(pack)
    pack, evidence, out = (confined(root, Path(p)) for p in (pack, evidence, out))
    if not str(request.get("reason", "")).strip():
        raise InterviewError("a reason is required so the decision history remains understandable")
    action = "edit" if request.get("action") == "planning" else request.get("action")
    if action not in ("accept", "reject", "edit"):
        raise InterviewError("choose accept, reject, or edit")
    with locked(root):
        require_idle(root)
        current = catalog(root, pack, evidence)
        item = next((x for x in current["items"] if x["id"] == request.get("item")), None)
        if item is None or item["fingerprint"] != request.get("fingerprint"):
            raise InterviewError("this item changed since it was viewed; reload it before deciding")
        dpath = confined(root, review.decisions_path(cfg, root))
        snapshots = {dpath: dpath.read_bytes() if dpath.exists() else None}
        if action not in item.get("actions", ["accept", "reject", "edit"]):
            raise InterviewError("this item supports " + ", ".join(item["actions"]))
        journal = confined(root, Path("staging/interview/history") / stamp())
        journal.mkdir(parents=True)
        entry = {"request": request, "before": item, "status": "rebuilding", "pack": str(pack)}
        atomic_json(journal / "action.json", entry)
        rebuild_evidence = item["kind"] == "reading"
        if rebuild_evidence:
            # A new reading changes derived units and approval bindings. Keep the entire
            # prior evidence build so a failed edit cannot leave outputs on mixed inputs.
            shutil.copytree(evidence, journal / "evidence-before")
            ap = confined(root, Path(cfg.get("approvals", "curation/approvals.yaml")))
            snapshots[ap] = ap.read_bytes() if ap.exists() else None
        try:
            if action == "edit":
                value = (planning_edit(item, request.get("planning_field", ""),
                                       request.get("planning_value", ""), request["reason"])
                         if request.get("action") == "planning" else request.get("value"))
                if not isinstance(value, dict):
                    raise InterviewError("the edited value must be an object")
                if item["kind"] in ("row", "op", "clarification") and value.get("id") != item["id"]:
                    raise InterviewError("an edit cannot change the item's identity")
                if item["kind"] == "row":
                    from .register import Row
                    Row.model_validate(value)
                if item["kind"] == "op":
                    from .amend import Op
                    Op.model_validate(value)
                if item["kind"] == "reading":
                    from .readings import Reading
                    Reading.model_validate(value)
                    if value.get("region_id") != item["id"] or value.get("unit_id") != item["value"].get("unit_id"):
                        raise InterviewError("an edit cannot change the reading's identity")
                path, key = _item_file(root, cfg, item["kind"], item["id"])
                snapshots[path] = path.read_bytes()
                data = load_yaml(path)
                if item["kind"] == "assumption":
                    data[key] = value
                elif item["kind"] == "reading":
                    data = value
                elif key == "issues":
                    data[key][item["id"]] = value
                else:
                    matches = [i for i, x in enumerate(data[key]) if x.get("id") == item["id"]]
                    if len(matches) != 1:
                        raise InterviewError("item source is ambiguous")
                    data[key][matches[0]] = value
                path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
            if rebuild_evidence:
                from .cli import approve, ingest
                if action == "accept":
                    code = approve(item["id"], "Interview operator", request["reason"], root=root,
                                   pack_path=pack, confirm_changes=True)
                    if code:
                        raise InterviewError(f"reading approval failed (exit {code})")
                result = ingest(pack, evidence, root=root, quiet=True)
                if result["exit_code"]:
                    raise InterviewError("reading failed the evidence checks")
            r = stage2.run(evidence, pack, root)
            new_findings = stage2.register_findings(r)
            old = {json.dumps(x, sort_keys=True, default=str) for x in current["findings"]}
            added = [x for x in new_findings if json.dumps(x, sort_keys=True, default=str) not in old]
            if added:
                raise InterviewError(f"change creates validation findings: {added[:5]}")
            # An edit creates a new proposal; approval is a separate, visible decision.
            if action != "edit" and item["kind"] != "reading":
                code, msgs = review.decide(r, [item["id"]], action, "Interview operator", request["reason"], dpath)
                if code:
                    raise InterviewError("; ".join(msgs))
            result = stage2.build(evidence, out, pack, root, quiet=True, strict=False)
            if result["exit_code"] != 0:
                raise InterviewError(f"outputs failed validation (exit {result['exit_code']}); inputs restored")
            entry.update(status="current", output=str(out), blockers=result.get("blockers", []))
        except Exception as e:
            for path, content in snapshots.items():
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(content)
            if rebuild_evidence:
                if evidence.exists():
                    shutil.rmtree(evidence)
                shutil.copytree(journal / "evidence-before", evidence)
            entry.update(status="rolled_back", error=str(e))
            raise
        finally:
            for i, (path, content) in enumerate(snapshots.items()):
                if content is not None:
                    (journal / f"before-{i}.yaml").write_bytes(content)
            entry["previous_files"] = [str(p) for p in snapshots]
            atomic_json(journal / "action.json", entry)
        return entry


def timed_args(command: list[str], cfg: dict) -> list[str]:
    profile = cfg.get("interview") or {}
    args = list(command)
    if args[:2] == ["ai", "run"]:
        args += ["--batch-size", str(profile.get("analysis_batch_size", 6)),
                 "--downstream-batch-size", str(profile.get("downstream_batch_size", 6))]
    return ["interview", "timed", "--seconds", str(profile.get("time_budget_s", 2700)), "--", *args]


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "timed":
        parser = argparse.ArgumentParser(prog="tenderpack interview timed")
        parser.add_argument("--seconds", type=float, default=2700)
        parser.add_argument("command", nargs=argparse.REMAINDER)
        a = parser.parse_args(argv[1:])
        command = a.command[1:] if a.command[:1] == ["--"] else a.command
        if command[:2] not in (["ai", "run"], ["ai", "resume"]) or not 0 < a.seconds <= 7200:
            parser.error("expected --seconds 1..7200 -- ai run|resume ...")
        root = Path(__file__).resolve().parent.parent
        require_demo(root / "config/pack.yaml")
        result = run_timed([sys.executable, "-m", "tenderpack", *command], root, a.seconds)
        atomic_json(root / "staging/interview/timing" / (stamp() + ".json"), result)
        print(json.dumps(result, indent=2))
        return result["exit_code"]
    p = argparse.ArgumentParser(prog="tenderpack interview")
    p.add_argument("action", choices=("freeze", "verify", "restore", "assume", "catalog", "apply"))
    p.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    p.add_argument("--pack", default="config/pack.yaml")
    p.add_argument("--evidence", default="build")
    p.add_argument("--out", default="out")
    p.add_argument("--request", type=Path)
    a = p.parse_args(argv)
    root = Path(a.root).resolve()
    pack, evidence, out = (confined(root, Path(x)) for x in (a.pack, a.evidence, a.out))
    try:
        if a.action in ("freeze", "restore"):
            result = globals()[a.action](root)
        elif a.action == "verify":
            result = {"problems": verify_frozen(root)}
            print(json.dumps(result, indent=2))
            return int(bool(result["problems"]))
        elif a.action == "catalog":
            result = catalog(root, pack, evidence)
        elif a.action == "apply":
            result = apply(root, pack, evidence, out, json.loads(a.request.read_text()))
        else:
            with locked(root):
                result = assume_reviews(root, pack, evidence)
                built = stage2.build(evidence, out, pack, root, quiet=True, strict=False)
                result["outputs_exit_code"] = built["exit_code"]
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return int(bool(result.get("outputs_exit_code")))
    except (InterviewError, OSError, ValueError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2


def run_timed(command: list[str], root: Path, seconds: float) -> dict:
    """Stop the existing resumable controller via SIGTERM when the demo budget ends."""
    t0 = time.monotonic()
    wall0 = time.time()
    proc = subprocess.Popen(command, cwd=root)
    awake = None
    if sys.platform == "darwin" and Path("/usr/bin/caffeinate").is_file():
        awake = subprocess.Popen(["/usr/bin/caffeinate", "-i", "-w", str(proc.pid)])
    timed_out = False
    try:
        code = proc.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        print("Interview time budget reached; saving the checkpoint. Resume this run to continue.", flush=True)
        proc.terminate()
        try:
            proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        code = 130
    except BaseException:
        proc.terminate()
        try:
            proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        raise
    active = time.monotonic() - t0
    calendar = time.time() - wall0
    if awake is not None:
        awake.wait(timeout=5)
    return {"command": command, "elapsed_s": round(active, 3), "calendar_elapsed_s": round(calendar, 3),
            "unaccounted_wall_s": round(max(0, calendar - active), 3), "kept_awake": awake is not None,
            "budget_s": seconds, "budget_reached": timed_out, "exit_code": code,
            "completion": "stopped; resume required" if timed_out else "consult the workflow checkpoint"}
