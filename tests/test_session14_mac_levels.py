"""Session 14 (W6, part 7, item 1): an exit-zero Ollama answer is never "validated". Three levels, each printed:

  level 1  connectivity: the local Ollama answers /api/tags, the model is installed, /api/show reports vision, tools and
           context (scripts/mac/levels.py connectivity, from `tenderpack ai ollama-models --json`)
  level 2  valid content: the one-batch request returned a proposal set that PASSED the controller's validation, read
           from the run's own record (proposals.yaml), never from the exit code (`ai propose` exits 0 for a partial set)
  level 3  complete workflow: a whole `ai run --offline` to the candidate outputs and the review packet, its status and
           completeness read from the checkpoint; a partial run that exits 0 is PARTIAL, never success

Before session 14, checks.sh check 7 printed "answered and validated" for any exit 0 of `ai propose`, and launcher
option 6 printed "(exit 0: done)" for a partial run. The levels are tested here against the FAKE local Ollama of the
tests (tests/fixtures/fake_ollama.py: a real HTTP server on 127.0.0.1 replaying hand-written recorded answers): what
tenderpack reads and reports, never how a real local model behaves (PENDING ON THE MAC). checks.sh and the launcher
are driven by a bash harness with a stand-in interpreter (TENDERPACK_PY) and a stand-in `ollama` on PATH."""
from __future__ import annotations

import copy
import json
import os
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT, workspace
from fake_ollama import FakeOllama, NetGuard, _neutral, show

MAC = ROOT / "scripts/mac"
PY = sys.executable
TEXT, VISION, CRITIC = "fake-text:8b", "fake-vl:8b", "fake-critic:8b"
PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
quiet = lambda *a, **k: None  # noqa: E731


def _levels():
    import importlib.util
    spec = importlib.util.spec_from_file_location("s14_levels", MAC / "levels.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _levels_cli(*args) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(MAC / "levels.py"), *map(str, args)], capture_output=True, text=True, timeout=60)


def _cfg(url: str, models: dict) -> dict:
    from tenderpack.ai import config as C
    cfg = copy.deepcopy(C.load())
    ol = cfg["routes"]["ollama"]
    ol["base_url"], ol["base_url_env"] = url, "TENDERPACK_TEST_OLLAMA_URL_UNSET"
    ol["models"] = models
    ol["machine"] = {"unified_memory_gb": 48, "usable_fraction": 0.75}
    cfg["concurrency"]["max_parallel_sessions"] = 1
    return cfg


def _cfg_file(tmp: Path, cfg: dict) -> Path:
    p = tmp / "ai.yaml"
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    return p


def _port(url: str) -> int:
    return int(url.rsplit(":", 1)[1])


# ---------------------------------------------------------------------------------------------- level 1

def _ollama_models_json(tmp: Path, cfgp: Path, capsys) -> Path:
    from tenderpack.cli import main
    main(["ai", "ollama-models", "--offline", "--json", "--config", str(cfgp)])
    out = tmp / "ollama-models.json"
    out.write_text(capsys.readouterr().out, encoding="utf-8")
    return out


def test_level1_connectivity_reads_tags_and_show_from_the_fake_ollama(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("TENDERPACK_OLLAMA_URL", raising=False)
    f = FakeOllama({TEXT: show(context=65536), VISION: show(caps=("completion", "vision", "tools"), context=65536),
                    CRITIC: show(caps=("completion",), context=65536)})
    f.start()
    try:
        guard = NetGuard(monkeypatch, allow_port=_port(f.url))
        cfgp = _cfg_file(tmp_path, _cfg(f.url, {"text": {"id": TEXT}, "vision": {"id": VISION},
                                                "critic": {"id": CRITIC}}))
        rep = _ollama_models_json(tmp_path, cfgp, capsys)
        r = _levels_cli("connectivity", rep)
        assert r.returncode == 0, r.stdout
        first = r.stdout.splitlines()[0]
        assert first.startswith("level 1 (connectivity) PASS"), r.stdout
        assert f"{VISION} (configured as vision): /api/show reports vision=yes, tools=yes, context=65536" in r.stdout
        assert f"{CRITIC} (configured as critic): /api/show reports vision=no, tools=no" in r.stdout
        assert f"the one-batch request (level 2) will use {TEXT}" in r.stdout
        assert _levels_cli("pick-model", rep).stdout.strip() == TEXT
        assert "GET /api/tags" in f.paths() and "POST /api/show" in f.paths()
        assert "POST /api/pull" not in f.paths() and guard.non_local() == []
        assert not any(Path(p[0]).name in ("claude", "codex", "ollama") for p in guard.processes)
        # the reading phase without a vision model: Ollama answers, level 1 is PENDING (not PASS), the reason named
        del f.models[VISION]
        rep = _ollama_models_json(tmp_path, cfgp, capsys)
        r = _levels_cli("connectivity", rep)
        assert r.returncode == 3 and r.stdout.startswith("level 1 (connectivity) PENDING"), r.stdout
        assert f"configured vision model {VISION} is NOT installed" in r.stdout and "reading" in r.stdout
        assert "ollama pull" in r.stdout and "never pulls" in r.stdout
    finally:
        f.stop()


def test_level1_unreachable_ollama_is_pending_with_the_next_step(tmp_path, monkeypatch, capsys):
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    url = f"http://127.0.0.1:{s.getsockname()[1]}"
    s.close()
    monkeypatch.delenv("TENDERPACK_OLLAMA_URL", raising=False)
    rep = _ollama_models_json(tmp_path, _cfg_file(tmp_path, _cfg(url, {"text": {"id": TEXT}})), capsys)
    r = _levels_cli("connectivity", rep)
    assert r.returncode == 3 and "does not answer /api/tags" in r.stdout and "ollama serve" in r.stdout, r.stdout
    assert _levels_cli("pick-model", rep).returncode == 1


# ---------------------------------------------------------------------------------------------- level 2

def _replay(cassette: dict | Path):
    """A FakeOllama /api/chat answer that replays a recorded proposal run (providers.recorded) turn by turn."""
    from tenderpack.ai.providers.recorded import RecordedProvider
    rp = RecordedProvider(cassette, TEXT)

    def chat(body):
        resp = rp.complete(_neutral(body))
        return {"model": TEXT, "done": True, "done_reason": "stop",
                "message": {"role": "assistant", "content": resp.text,
                            "tool_calls": [{"function": {"name": c.name, "arguments": c.arguments}}
                                           for c in resp.tool_calls]},
                "prompt_eval_count": resp.usage.get("input_tokens", 0), "eval_count": resp.usage.get("output_tokens", 0)}
    return chat


def _propose_offline(tmp: Path, ws, chat, monkeypatch, capsys) -> tuple[int, str, Path]:
    """`tenderpack ai propose ADD-03 --route ollama --offline` (the CLI, in process) against the fake local Ollama."""
    from tenderpack.cli import main
    f = FakeOllama({TEXT: show(context=262144)}, chat=chat)
    f.start()
    try:
        guard = NetGuard(monkeypatch, allow_port=_port(f.url))
        cfgp = _cfg_file(tmp, _cfg(f.url, {"text": {"id": TEXT, "num_ctx": 262144}}))
        out = tmp / "staging-propose"
        code = main(["ai", "propose", "ADD-03", "--route", "ollama", "--offline", "--model", TEXT,
                     "--evidence", str(ws.evidence), "--pack", str(ws.pack), "--config", str(cfgp),
                     "--out", str(out), "--worklog", str(tmp / "worklog")])
        text = capsys.readouterr().out
    finally:
        f.stop()
    assert guard.non_local() == [] and not any(Path(p[0]).name in ("claude", "codex") for p in guard.processes)
    assert any(p == "/api/chat" for _, p, _ in f.requests)
    return code, text, out


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-levels"), evidence=request.getfixturevalue("blind02_build"))


def test_level2_an_exit_zero_answer_with_failed_items_is_not_validated(ws, tmp_path, monkeypatch, capsys):
    """The recorded run answers 2.1, 3.1 and the cover line correctly, 5.1 with a FABRICATED quotation and 7.2 by an
    escalation: `ai propose` exits 0 (a partial set), and level 2 reads the record: PARTIAL, the failed item named."""
    code, text, out = _propose_offline(tmp_path, ws, _replay(CASSETTES / "add03_propose.yaml"), monkeypatch, capsys)
    assert code == 0, text                                    # what check 7 used to read as "validated"
    r = _levels_cli("content", out)
    assert r.returncode == 4, r.stdout
    assert r.stdout.startswith("level 2 (valid content) PARTIAL: 3 item(s) passed the validation, 1 did not, "
                               "1 escalated to a person"), r.stdout
    assert "ADD-03/5.1: insufficient_evidence" in r.stdout
    # the same record asked about a provision the set did not answer: not a PASS either
    r = _levels_cli("content", out, "ADD-03:4")
    assert r.returncode == 4 and "asked but not accounted for: ADD-03:4" in r.stdout, r.stdout


def test_level2_passes_only_when_every_item_passed_the_controller(ws, tmp_path, monkeypatch, capsys):
    data = yaml.safe_load((CASSETTES / "add03_propose.yaml").read_text(encoding="utf-8"))
    last = data["turns"][-1]["response"]
    t = last["text"]
    a, b = t.index('{"id": "ADD-03/5.1"'), t.index('{"id": "ADD-03/cover/para1"')
    last["text"] = t[:a] + t[b:]                               # only the three correct items
    code, text, out = _propose_offline(tmp_path, ws, _replay(data), monkeypatch, capsys)
    assert code == 0, text
    r = _levels_cli("content", out, "ADD-03:2.1")
    assert r.returncode == 0, r.stdout
    assert r.stdout.startswith("level 2 (valid content) PASS: 3 item(s) passed the controller's validation, none "
                               "failed"), r.stdout


def test_level2_an_answer_that_is_not_a_proposal_set_fails(ws, tmp_path, monkeypatch, capsys):
    chat = lambda body: {"model": TEXT, "done": True, "done_reason": "stop",               # noqa: E731
                         "message": {"role": "assistant", "content": "I am not able to help with this."},
                         "prompt_eval_count": 5, "eval_count": 5}
    code, text, out = _propose_offline(tmp_path, ws, chat, monkeypatch, capsys)
    r = _levels_cli("content", out)
    assert r.returncode == 1 and r.stdout.startswith("level 2 (valid content) FAIL"), (code, r.stdout)
    assert _levels_cli("content", tmp_path / "nothing-here").returncode == 1


# ---------------------------------------------------------------------------------------------- level 3

@pytest.fixture(scope="module")
def offline_full_run(tmp_path_factory, pack):
    """A WHOLE workflow run on the ollama route in offline mode against the fake local Ollama (the recorded workflow:
    three analysis batches answered, the others not, so the run ends PARTIAL with exit code 0)."""
    from tenderpack.ai import workflow as W
    d = tmp_path_factory.mktemp("s14-offline-full")
    data = yaml.safe_load((CASSETTES / "workflow_add03.yaml").read_text(encoding="utf-8"))
    data["sessions"] += yaml.safe_load((CASSETTES / "s11_workflow_critic.yaml").read_text(encoding="utf-8"))["sessions"]
    cas = d / "cassette.yaml"
    cas.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    f = FakeOllama({TEXT: show(context=400000), CRITIC: show(caps=("completion",), context=400000)}, cassette=cas)
    f.start()
    mp = pytest.MonkeyPatch()
    guard = NetGuard(mp, allow_port=_port(f.url))
    try:
        cfgp = _cfg_file(d, _cfg(f.url, {"text": {"id": TEXT, "num_ctx": 400000},
                                         "critic": {"id": CRITIC, "num_ctx": 400000}}))
        res = W.start("ADD-03", PDF, route="ollama", offline=True, ai_config=cfgp, evidence=pack["out"],
                      staging=d / "staging", worklog=d / "worklog", run_id="off-full", batch_size=8,
                      background_before=False, echo=quiet, sleep=lambda s: None)
    finally:
        mp.undo()
        f.stop()
    return {"res": res, "dir": d / "staging/runs/off-full", "guard": guard}


def test_level3_a_partial_offline_run_that_exits_zero_is_partial_never_success(offline_full_run):
    res, run = offline_full_run["res"], offline_full_run["dir"]
    assert res["exit_code"] == 0 and res["status"] == "partial", res
    assert offline_full_run["guard"].non_local() == []
    r = _levels_cli("workflow", run, res["exit_code"])
    assert r.returncode == 4, r.stdout
    assert r.stdout.startswith("level 3 (complete workflow) PARTIAL: exit 0; run off-full ended PARTIAL, not a success"), \
        r.stdout
    assert "completeness: partial" in r.stdout and "incomplete: " in r.stdout
    assert "review packet: " + str(run / "review" / "index.md") in r.stdout          # read from the run, not assumed


def test_level3_complete_only_when_the_checkpoint_the_outputs_and_the_packet_agree(offline_full_run, tmp_path):
    src = offline_full_run["dir"]
    run = tmp_path / "off-full"
    (run / "review").mkdir(parents=True)
    cp = json.loads((src / "checkpoint.json").read_text(encoding="utf-8"))
    cp["status"], cp["status_reason"] = "complete", None
    cp["completeness"] = {**cp["completeness"], "status": "complete", "reasons": [],
                          "outputs": {"published": True, "refused": False, "exit_code": 0}}
    (run / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    r = _levels_cli("workflow", run, 0)
    assert r.returncode == 1 and "says complete but its record disagrees" in r.stdout, r.stdout   # no review packet
    (run / "review/index.md").write_text("# review\n", encoding="utf-8")
    r = _levels_cli("workflow", run, 0)
    assert r.returncode == 0 and r.stdout.startswith("level 3 (complete workflow) PASS"), r.stdout
    for status, code, word in (("stopped", 5, "PENDING"), ("waiting_for_host", 5, "PENDING"),
                               ("deferred", 5, "PENDING"), ("failed", 1, "FAIL")):
        cp["status"] = status
        (run / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
        r = _levels_cli("workflow", run, 0)
        assert r.returncode == code and f"level 3 (complete workflow) {word}" in r.stdout, (status, r.stdout)
    assert _levels_cli("workflow", tmp_path / "no-run", 2).returncode == 1


# ---------------------------------------------------------------------------------------------- checks.sh

STANDIN = r'''#!/usr/bin/env bash
# a stand-in interpreter for checks.sh (session 14 tests): `-m tenderpack ai ...` answers per FAKE_CASE with the
# records a run would leave; every other command (scripts/mac/levels.py) runs on the real interpreter
REAL="__REAL__"
if [ "$1" = "-m" ] && [ "$2" = "tenderpack" ] && [ "$3" = "ai" ]; then
  shift 3
  cmd="$1"; shift
  arg() { local want="$1"; shift; while [ $# -gt 0 ]; do [ "$1" = "$want" ] && { echo "$2"; return; }; shift; done; }
  case "$cmd" in
    ollama-models)
      for a in "$@"; do [ "$a" = "--json" ] && { cat "$FAKE_DIR/models.json"; exit 0; }; done
      echo "Ollama at http://127.0.0.1:11434: answers"; exit 0 ;;
    run)
      out="$(arg --out "$@")"; rid="$(arg --run-id "$@")"; mkdir -p "$out/runs/$rid/candidate"
      for a in "$@"; do [ "$a" = "--stop-after" ] && exit 0; done
      mkdir -p "$out/runs/$rid/review"; echo "# review" > "$out/runs/$rid/review/index.md"
      cp "$FAKE_DIR/checkpoint.json" "$out/runs/$rid/checkpoint.json"
      echo "run $rid: partial"; exit 0 ;;
    propose)
      out="$(arg --out "$@")"; mkdir -p "$out/s14run"; cp "$FAKE_DIR/proposals.yaml" "$out/s14run/proposals.yaml"
      echo "run s14run: partial; items ..."; exit 0 ;;
  esac
  exit 0
fi
exec "$REAL" "$@"
'''


def _items(*statuses):
    return [{"id": f"ADD-03/2.{i}", "provision": "ADD-03:2.1", "verification_status": s,
             "validation": [{"check": "evidence", "ok": s == "evidence_verified", "detail": "quotation not found"}]}
            for i, s in enumerate(statuses, 1)]


def _checks_case(tmp: Path, items: list, run_status: str, comp: str = "partial") -> subprocess.CompletedProcess:
    d = tmp / "fake"
    d.mkdir(parents=True, exist_ok=True)
    (d / "models.json").write_text(json.dumps({
        "base_url": "http://127.0.0.1:11434", "reachable": True, "configured": {"text": TEXT},
        "models": [{"id": TEXT, "roles": ["text"], "capabilities": ["completion", "tools", "vision"],
                    "context_tokens": 65536}],
        "phases": {p: [TEXT] for p in ("reading", "analysis", "downstream", "critic")}}), encoding="utf-8")
    (d / "proposals.yaml").write_text(yaml.safe_dump({"proposal_set": {
        "run_id": "s14run", "status": "partial", "items": items,
        "coverage": {"provisions_total": 12, "accounted": 1, "unaccounted": ["ADD-03:1.1"]}}}), encoding="utf-8")
    (d / "checkpoint.json").write_text(json.dumps({
        "run_id": "r", "status": run_status, "status_reason": "2 provision(s) unresolved" if comp != "complete" else None,
        "completeness": {"status": comp, "reasons": [] if comp == "complete" else ["2 provision(s) unresolved"],
                         "outputs": {"published": True}}, "steps": {}}), encoding="utf-8")
    std = tmp / "standin"
    std.write_text(STANDIN.replace("__REAL__", PY), encoding="utf-8")
    std.chmod(0o755)
    bin_ = tmp / "bin"
    bin_.mkdir(exist_ok=True)
    (bin_ / "ollama").write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    (bin_ / "ollama").chmod(0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    env.update(TENDERPACK_PY=str(std), FAKE_DIR=str(d), TMPDIR=str(tmp), PATH=f"{bin_}:{env.get('PATH', '')}")
    return subprocess.run(["bash", str(MAC / "checks.sh"), "--only", "6,7"], capture_output=True, text=True,
                          env=env, timeout=300)


def _lines(out: str, n: int) -> list[str]:
    return [ln for ln in out.splitlines() if re.match(rf"^(PASS|FAIL|PENDING|PARTIAL) +{n} ", ln)]


def test_checks_never_reads_an_exit_zero_request_as_validated(tmp_path):
    r = _checks_case(tmp_path, _items("insufficient_evidence", "invalid"), "partial")
    seven = _lines(r.stdout, 7)
    assert seven and seven[0].startswith("FAIL     7 level 2 (valid content) FAIL"), r.stdout
    assert "the request's exit 0" in seven[0]                       # the exit code is printed, not believed
    assert not any(x.startswith("PASS") for x in seven), r.stdout
    assert "PENDING  7 level 3 (complete workflow) not run: level 1 and level 2 must PASS first" in r.stdout
    assert _lines(r.stdout, 6)[0].startswith("PASS     6 level 1 (connectivity) PASS"), r.stdout
    assert r.returncode != 0 and "0 PARTIAL" in r.stdout and "1 FAIL" in r.stdout
    assert not [ln for ln in _lines(r.stdout, 1) + _lines(r.stdout, 2)]          # --only 6,7


def test_checks_reports_each_level_and_a_partial_run_as_partial(tmp_path):
    r = _checks_case(tmp_path, _items("evidence_verified"), "partial")
    seven = _lines(r.stdout, 7)
    assert seven[0].startswith("PASS     7 level 2 (valid content) PASS: 1 item(s) passed"), r.stdout
    assert seven[1].startswith("PARTIAL  7 level 3 (complete workflow) PARTIAL: exit 0;"), r.stdout
    assert "not a success" in seven[1] and r.returncode == 0                  # partial is not a FAIL, nor a PASS
    assert "2 PASS, 1 PARTIAL, 0 PENDING, 0 FAIL" in r.stdout
    r = _checks_case(tmp_path / "c", _items("evidence_verified", "interpretation_pending"), "complete", "complete")
    seven = _lines(r.stdout, 7)
    assert seven[1].startswith("PASS     7 level 3 (complete workflow) PASS"), r.stdout
    assert "3 PASS, 0 PARTIAL, 0 PENDING, 0 FAIL" in r.stdout


def test_checks_no_workflow_skips_level_3_visibly(tmp_path):
    d = tmp_path
    r = _checks_case(d, _items("evidence_verified"), "partial")
    env_args = r.args[:2] + ["--only", "7", "--no-workflow"]
    env = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    env.update(TENDERPACK_PY=str(d / "standin"), FAKE_DIR=str(d / "fake"), TMPDIR=str(d),
               PATH=f"{d / 'bin'}:{env.get('PATH', '')}")
    r2 = subprocess.run(env_args, capture_output=True, text=True, env=env, timeout=300)
    assert "PENDING  7 level 3 (complete workflow) skipped (--no-workflow)" in r2.stdout, r2.stdout


# ---------------------------------------------------------------------------------------------- launcher option 6

LAUNCH_STANDIN = r'''#!/usr/bin/env bash
# a stand-in interpreter for launch.command option 6: `ai run` leaves a PARTIAL checkpoint and exits 0
REAL="__REAL__"
if [ "$1" = "-m" ] && [ "$2" = "tenderpack" ]; then
  case "$3" in
    ai)
      if [ "$4" = "run" ]; then
        rid=""; prev=""; for a in "$@"; do [ "$prev" = "--run-id" ] && rid="$a"; prev="$a"; done
        [ -n "$rid" ] || { echo "no --run-id given"; exit 0; }
        mkdir -p "staging/ai/runs/$rid/review"
        printf '{"run_id": "%s", "status": "partial", "status_reason": "3 provision(s) unresolved", "completeness": {"status": "partial", "reasons": ["3 provision(s) unresolved in the candidate"], "outputs": {"published": true}}, "steps": {}}' "$rid" > "staging/ai/runs/$rid/checkpoint.json"
        echo "# review" > "staging/ai/runs/$rid/review/index.md"
        echo "run $rid: partial"; exit 0
      fi
      echo "AI routes (stand-in)"; exit 0 ;;
    panel) exit 0 ;;
  esac
  exit 0
fi
exec "$REAL" "$@"
'''


def test_launcher_option_6_reads_the_checkpoint_not_the_exit_code(tmp_path):
    f = tmp_path / "tp"
    (f / "scripts/mac").mkdir(parents=True)
    for n in ("launch.command", "levels.py"):
        shutil.copy(MAC / n, f / "scripts/mac" / n)
    (f / "pyproject.toml").write_text('[project]\nname = "tenderpack"\n', encoding="utf-8")
    (f / "tenderpack").mkdir()
    (f / "staging/ai").mkdir(parents=True)
    std = tmp_path / "standin"
    std.write_text(LAUNCH_STANDIN.replace("__REAL__", PY), encoding="utf-8")
    std.chmod(0o755)
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    env = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    env["TENDERPACK_PY"] = str(std)
    r = subprocess.run(["bash", str(f / "scripts/mac/launch.command")], input=f"2\n6\nADD-03\n{pdf}\nq\n",
                       capture_output=True, text=True, env=env, timeout=120)
    assert "level 3 (complete workflow) PARTIAL: exit 0; run ADD-03-run-offline-" in r.stdout, r.stdout
    assert "not a success" in r.stdout and "(exit 0: done)" not in r.stdout
