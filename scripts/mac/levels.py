"""The three levels of an AI check (session 14, W6): an exit code of 0 is never read as "validated".

    python scripts/mac/levels.py connectivity REPORT.json      level 1: the local Ollama answers /api/tags, the model the
                                                              one-batch request will use is installed, and /api/show
                                                              reports its vision, tool use and context
    python scripts/mac/levels.py pick-model REPORT.json        the model for the one-batch request (the configured text
                                                              model when it can serve the analysis, else the first
                                                              installed one that can); exit 1 when none can
    python scripts/mac/levels.py content STAGING [PROVISION..] level 2: the one-batch request returned a proposal set that
                                                              PASSED the controller's validation, read from the run's
                                                              own record (proposals.yaml: the set status and every
                                                              item's verification_status), never from the exit code
    python scripts/mac/levels.py workflow RUN_DIR [EXIT_CODE]  level 3: a whole `ai run` reached the candidate outputs
                                                              and the review packet, read from the checkpoint (status,
                                                              completeness, outputs published, review/index.md)

REPORT.json is `tenderpack ai ollama-models --json`. Each command prints ONE summary line, then indented details, and
exits with its verdict:
    0 PASS      the level is reached
    1 FAIL      the level is not reached (the record says why)
    3 PENDING   the level could not be examined here (Ollama not answering; nothing to read yet)
    4 PARTIAL   level 2/3: the record shows part of it (a partial run that exited 0 is PARTIAL, never success)
    5 PENDING   level 3: the run stopped or waits for a person, a host submission or a rate-limit reset
Used by scripts/mac/checks.sh (checks 6 and 7) and scripts/mac/launch.command (option 6). Reads files only: no model
call, no network, nothing written."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PASS, FAIL, PENDING, PARTIAL, WAITING = 0, 1, 3, 4, 5
# controller-written verification statuses (tenderpack/ai/contract.py): the ones that passed the validation, the ones
# that did not, and the escalation (a valid answer that hands the provision to a person: no proposal was validated)
PASSED = ("evidence_verified", "interpretation_pending")
NOT_PASSED = ("invalid", "insufficient_evidence", "unverified", "conflicting")
SET_FAILED = ("malformed", "provider_failed", "budget_exhausted", "stale", "deferred")
PHASES = ("reading", "analysis", "downstream", "critic")
ROLE_OF = {"reading": "vision", "analysis": "text", "downstream": "text", "critic": "critic"}


def _say(code: int, line: str, details=()) -> int:
    print(line)
    for d in details:
        if d:
            print(f"  {d}")
    return code


def _load_json(p: Path):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------------------------------------- level 1

def _model_line(m: dict) -> str:
    caps = set(m.get("capabilities") or [])
    roles = f" (configured as {', '.join(m['roles'])})" if m.get("roles") else ""
    if m.get("problem") and not caps:
        return f"{m.get('id')}{roles}: {m['problem']}"
    return (f"{m.get('id')}{roles}: /api/show reports vision={'yes' if 'vision' in caps else 'no'}, "
            f"tools={'yes' if 'tools' in caps else 'no'}, context={m.get('context_tokens') or 'not reported'}")


def pick_model(rep: dict) -> str | None:
    """The model for the one-batch analysis request: the configured text model when it can serve the analysis, else the
    first installed model that can (the request names it with --model; nothing is pulled)."""
    can = list((rep.get("phases") or {}).get("analysis") or [])
    want = (rep.get("configured") or {}).get("text") or (rep.get("configured") or {}).get("propose")
    if want in can:
        return want
    return can[0] if can else None


def connectivity(report: Path) -> int:
    rep = _load_json(report)
    if not isinstance(rep, dict):
        return _say(FAIL, f"level 1 (connectivity) FAIL: no readable `ai ollama-models --json` report at {report}")
    url = rep.get("base_url") or "the configured Ollama URL"
    if not rep.get("reachable"):
        return _say(PENDING, f"level 1 (connectivity) PENDING: Ollama does not answer /api/tags at {url}",
                    [rep.get("error"), "start the Ollama app (or `ollama serve`) and run again; nothing is downloaded"])
    models = rep.get("models") or []
    details = [f"Ollama answers /api/tags at {url}: {len(models)} model(s) installed"]
    details += [_model_line(m) for m in models]
    conf = rep.get("configured") or {}
    installed = {m.get("id") for m in models}
    for role, mid in sorted(conf.items()):
        if mid and mid not in installed:
            details.append(f"configured {role} model {mid} is NOT installed (`ollama pull {mid}` is your choice; "
                           "tenderpack never pulls)")
    missing = [p for p in PHASES if not (rep.get("phases") or {}).get(p)]
    chosen = pick_model(rep)
    if chosen:
        details.append(f"the one-batch request (level 2) will use {chosen}")
    if not models:
        return _say(PENDING, "level 1 (connectivity) PENDING: Ollama answers but no model is installed", details)
    if missing:
        details.append("no installed model can serve: " + ", ".join(missing) + " (see the per-model reasons in "
                       "`tenderpack ai ollama-models`)")
        return _say(PENDING, f"level 1 (connectivity) PENDING: Ollama answers; {len(missing)} phase(s) without an "
                             "installed model that can serve them", details)
    return _say(PASS, "level 1 (connectivity) PASS: Ollama answers, the models are installed and /api/show reports "
                      "their capabilities and context for every phase", details)


# ---------------------------------------------------------------------------------------------- level 2

def _newest_set(staging: Path) -> Path | None:
    sets = sorted(Path(staging).glob("*/proposals.yaml"), key=lambda p: p.stat().st_mtime)
    return sets[-1] if sets else None


def content(staging: Path, provisions: list[str]) -> int:
    import yaml
    f = Path(staging) if Path(staging).is_file() else _newest_set(Path(staging))
    if f is None:
        return _say(FAIL, f"level 2 (valid content) FAIL: no proposal set was staged under {staging} (the request "
                          "produced no record to validate)")
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        return _say(FAIL, f"level 2 (valid content) FAIL: {f} cannot be read ({type(e).__name__})")
    ps = data.get("proposal_set") or {}
    items = ps.get("items") or []
    status = ps.get("status")
    counts: dict[str, int] = {}
    for it in items:
        counts[it.get("verification_status") or "?"] = counts.get(it.get("verification_status") or "?", 0) + 1
    unacc = set((ps.get("coverage") or {}).get("unaccounted") or [])
    asked_unacc = [p for p in provisions if any(u == p or u.startswith(p + ".") for u in unacc)]
    ok = sum(counts.get(s, 0) for s in PASSED)
    bad = sum(counts.get(s, 0) for s in NOT_PASSED)
    esc = counts.get("escalated", 0)
    details = [f"record: {f}", f"set {ps.get('run_id')}: status {status}; items by validation status: "
               + (", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "none")]
    for it in items:
        if it.get("verification_status") in NOT_PASSED:
            why = "; ".join(str(c.get("detail") or c.get("check") or "") for c in (it.get("validation") or [])
                            if isinstance(c, dict) and c.get("ok") is False)[:300]
            details.append(f"{it.get('id')}: {it.get('verification_status')}" + (f" ({why})" if why else ""))
    if asked_unacc:
        details.append("asked but not accounted for: " + ", ".join(asked_unacc))
    if status in SET_FAILED:
        return _say(FAIL, f"level 2 (valid content) FAIL: the proposal set is {status} (the exit code is not the "
                          "result)", details)
    if not items:
        return _say(FAIL, "level 2 (valid content) FAIL: the proposal set holds no item", details)
    if ok and not bad and not asked_unacc:
        return _say(PASS, f"level 2 (valid content) PASS: {ok} item(s) passed the controller's validation, none "
                          "failed" + (f" ({esc} escalated to a person)" if esc else ""), details)
    if ok or esc:
        return _say(PARTIAL, f"level 2 (valid content) PARTIAL: {ok} item(s) passed the validation, {bad} did not, "
                             f"{esc} escalated to a person" + (", a provision asked was not answered"
                                                               if asked_unacc else ""), details)
    return _say(FAIL, f"level 2 (valid content) FAIL: none of the {len(items)} item(s) passed the controller's "
                      "validation", details)


# ---------------------------------------------------------------------------------------------- level 3

def workflow(run_dir: Path, exit_code: str | None = None) -> int:
    run_dir = Path(run_dir)
    cp = _load_json(run_dir / "checkpoint.json")
    ex = f"exit {exit_code}; " if exit_code not in (None, "") else ""
    if not isinstance(cp, dict):
        return _say(FAIL, f"level 3 (complete workflow) FAIL: {ex}no checkpoint at {run_dir / 'checkpoint.json'} "
                          "(the run was refused before it started, or the folder is wrong)")
    status, reason = cp.get("status"), cp.get("status_reason")
    comp = cp.get("completeness") or {}
    outs = comp.get("outputs") or {}
    review = run_dir / "review" / "index.md"
    steps = cp.get("steps") or {}
    details = [f"run {cp.get('run_id')}: status {status}" + (f" ({reason})" if reason else ""),
               f"completeness: {comp.get('status') or 'not recorded'}",
               f"candidate outputs published: {'yes' if outs.get('published') else 'no'}; review packet: "
               + (str(review) if review.is_file() else "not written")]
    details += [f"incomplete: {r}" for r in (comp.get("reasons") or [])[:6]]
    if len(comp.get("reasons") or []) > 6:
        details.append(f"... {len(comp['reasons']) - 6} more reason(s) in the review packet")
    rid = cp.get("run_id") or run_dir.name
    if status == "complete":
        if comp.get("status") == "complete" and outs.get("published") and review.is_file():
            return _say(PASS, f"level 3 (complete workflow) PASS: {ex}run {rid} complete: every provision answered, "
                              "the candidate outputs published and the review packet written (nothing approved)",
                        details)
        return _say(FAIL, f"level 3 (complete workflow) FAIL: {ex}run {rid} says complete but its record disagrees "
                          "(completeness, outputs or review packet missing)", details)
    if status == "partial":
        return _say(PARTIAL, f"level 3 (complete workflow) PARTIAL: {ex}run {rid} ended PARTIAL, not a success: "
                             f"{(comp.get('reasons') or [reason or 'see the review packet'])[0]}", details)
    if status in ("stopped", "waiting_for_host", "deferred"):
        last = next((s for s, v in steps.items() if (v or {}).get("status") not in ("done", "skipped")), None)
        return _say(WAITING, f"level 3 (complete workflow) PENDING: {ex}run {rid} {status}"
                             + (f" at {last}" if last else "") + f": not finished; `tenderpack ai run-status {rid}` "
                             "says what it needs", details)
    return _say(FAIL, f"level 3 (complete workflow) FAIL: {ex}run {rid} {status or 'has no status'}"
                      + (f": {reason}" if reason else ""), details)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ("connectivity", "pick-model", "content", "workflow"):
        print(__doc__)
        return 2
    cmd, arg = argv[0], Path(argv[1])
    if cmd == "connectivity":
        return connectivity(arg)
    if cmd == "pick-model":
        rep = _load_json(arg)
        m = pick_model(rep) if isinstance(rep, dict) else None
        if m:
            print(m)
        return 0 if m else 1
    if cmd == "content":
        return content(arg, argv[2:])
    return workflow(arg, argv[2] if len(argv) > 2 else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
