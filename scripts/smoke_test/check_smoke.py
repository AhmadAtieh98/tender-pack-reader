"""SMOKE TEST: synthetic, not tender content. Compares a smoke run with smoke-test/expected.yaml.

Usage: python smoke-test/check_smoke.py RUN_DIR EXPECTED_YAML EXIT_CODE RUN_LOG

PASS only when: the run exited 0; its checkpoint says `stopped` after ingest with every later step pending; its
provisions are exactly the expected ones and every one is `pending` (nothing proposed, nothing accepted: approval
`none`); the candidate stayed inside the run folder; and the run's log holds no model, host-session or network event.
Prints one PASS / FAIL line per check and exits 0 (all pass) or 1."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


def main(run_dir: str, expected: str, rc: str, run_log: str) -> int:
    rd, exp = Path(run_dir), yaml.safe_load(Path(expected).read_text(encoding="utf-8"))
    res = []

    def check(ok: bool, what: str) -> None:
        res.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {what}")
    check(rc == "0", f"the run exited {rc} (expected 0)")
    cp_path = rd / "checkpoint.json"
    if not cp_path.is_file():
        check(False, f"no checkpoint at {cp_path}; the run log says:\n" + Path(run_log).read_text(encoding="utf-8")[-2000:])
        return 1
    cp = json.loads(cp_path.read_text(encoding="utf-8"))
    steps = cp.get("steps") or {}
    check(cp.get("status") == "stopped", f"status {cp.get('status')!r} (expected 'stopped' after ingest)")
    check((steps.get("ingest") or {}).get("status") == "done", "the ingest step is done")
    later = {k: (v or {}).get("status") for k, v in steps.items() if k != "ingest"}
    check(all(s == "pending" for s in later.values()), f"every later step is pending ({later})")
    got, want = sorted((cp.get("provisions") or {})), sorted(exp.get("provisions") or [])
    check(got == want, f"{len(got)} provisions of {exp.get('doc_id')} found, {len(want)} expected"
          + ("" if got == want else f" (missing {sorted(set(want) - set(got))}, extra {sorted(set(got) - set(want))})"))
    states = sorted({(v or {}).get("status") for v in (cp.get("provisions") or {}).values()})
    check(states == ["pending"], f"every provision is pending (states: {states}); nothing proposed or accepted")
    ap = cp.get("approval")
    ap_status, decisions = (ap.get("status"), ap.get("decisions")) if isinstance(ap, dict) else (ap, [])
    check(str(ap_status) == "none" and not decisions,
          f"approval {ap_status!r} with {len(decisions or [])} decision(s) (expected 'none' and no decision recorded)")
    log = rd / "log.jsonl"
    events = [json.loads(x).get("event") for x in log.read_text(encoding="utf-8").splitlines()] if log.is_file() else []
    calls = [e for e in events if re.search(r"request|response|session|call|prompt|capabilit", str(e))]
    check(not calls and not (rd / "ai").exists(), f"no model, host-session or network event in the run log "
          f"({len(events)} event(s): {sorted(set(map(str, events)))})")
    cand = Path((cp.get("candidate") or {}).get("dir") or rd / "candidate")
    check(cand.resolve().is_relative_to(rd.resolve()), f"the candidate stayed inside the run folder ({cand})")
    print(f"\nsmoke test: {'PASS' if all(res) else 'FAIL'} ({sum(res)} of {len(res)} checks; the run is in {rd})")
    return 0 if all(res) else 1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(*sys.argv[1:]))
