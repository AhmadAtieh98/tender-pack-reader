"""Session 11 (D2): ONE request path for the AI phases (analysis, image reading, downstream, the critic), with the task
schema per phase, a capability check before any call, complete request and context accounting, bounded response repair,
three failure classes (rate limit, provider failure, malformed answer) with bounded backoff, resumable checkpoints and
the selective critic inside the workflow.

Every provider exchange here is RECORDED or MOCKED (cassettes, canned replies, a recorded stand-in for the `claude` CLI):
no live call is made and none is implied. Passing these tests shows how the request layer and the workflow behave
whatever a model or a host returns; it says nothing about how well any real model proposes or criticises."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT, workspace
from tenderpack.ai import budget as B
from tenderpack.ai import config as C
from tenderpack.ai import workflow as W
from tenderpack.ai.checkpoint import Checkpoint
from tenderpack.ai.contract import DOWNSTREAM_TASK, READING_TASK, downstream_fill_schema
from tenderpack.ai.providers.recorded import RecordedProvider

quiet = lambda *a, **k: None  # noqa: E731
PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s11-req"), evidence=request.getfixturevalue("blind02_build"))


def _ctx(tmp: Path, ws, route: str = "recorded", cfg: dict | None = None) -> W.Ctx:
    """A workflow context around the blind-02 workspace (no candidate is built: the request layer is under test)."""
    settings = {"addendum": "ADD-03", "route": route, "worklog": str(tmp / "worklog"), "staging": str(tmp / "staging"),
                "caps": {}, "ai_config": None, "model": None, "batch_size": 8, "downstream_batch_size": 12}
    cp = Checkpoint.new(tmp / "run" / "checkpoint.json", run_id="t11", addendum="ADD-03", settings=settings, inputs={},
                        candidate={})
    ctx = W.Ctx(cp, echo=quiet, sleep=lambda s: None)
    ctx._ws, ctx._cfg = ws, (cfg or C.load())
    return ctx


def _recorded(turns, images=True, tools=True, context=400000, structured=False) -> RecordedProvider:
    return RecordedProvider({"name": "s11", "model": "recorded-fixture-model", "turns": turns,
                             "capabilities": {"images": images, "tools": tools, "structured_output": structured,
                                              "context_tokens": context, "source": "cassette (recorded fixture)"}})


def _state(ws) -> dict:
    return ws.identity().model_dump()


# ---------------------------------------------------------------------------------------------- (1) one request path

def test_regression_a_reading_request_without_image_input_is_refused_before_any_call(ws, tmp_path):
    """REGRESSION (session 11): workflow._converse checked tool use and a rough packet size only. A reading request to a
    provider that does not report image input went ahead (the tool result said "images not attached" and the model
    answered anyway): a reading of an image made without the image. The reading phase REQUIRES image input."""
    ctx = _ctx(tmp_path, ws)
    reading = {"region_id": "ADD-03-p3-r1", "reading": {"region_id": "ADD-03-p3-r1"}, "model_rationale": "guessed"}
    prov = _recorded([{"response": {"text": json.dumps(reading)}}], images=False)
    packet = {"task": READING_TASK, "region_id": "ADD-03-p3-r1", "state": {"doc": "ADD-03", "page": 3}}
    from tenderpack.ai import regionread as RR
    with pytest.raises((W.BatchFailed, B.Refused), match="image input"):
        W._converse(ctx, prov, packet, "reading-ADD-03-p3-r1", system=RR.SYSTEM, parse=RR.parse, task=READING_TASK,
                    tool_names=["get_region", "validate_reading"], ws=ws)
    assert prov.requests == [], "a reading was asked of a model that cannot see the image"


def test_regression_every_request_carries_its_phase_schema(ws, tmp_path):
    """REGRESSION (session 11): the downstream and reading requests of workflow._converse carried no response schema,
    so no route could constrain the answer natively (only controller.propose did, for the analysis)."""
    ctx = _ctx(tmp_path, ws)
    st = _state(ws)
    answer = {"addendum": "ADD-03", "state": st, "statements": [], "items": []}
    prov = _recorded([{"response": {"text": json.dumps(answer)}}], images=False)
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks": [], "tasks_total": 0}
    ds = W._converse(ctx, prov, packet, "downstream-001")
    assert ds.items == [] and len(prov.requests) == 1
    assert prov.requests[0].response_schema == downstream_fill_schema()


def test_regression_an_oversize_packet_is_never_sent(ws, tmp_path):
    """REGRESSION (session 11): the size check of workflow._converse compared the packet alone (characters / 3.5) plus
    the output cap with the context window; the system prompt, the tool definitions, the images and the later turns
    were not counted, so a packet that cannot fit the conversation was sent. It is now refused before any call, with
    the sizes of every part (the workflow splits it by task, or escalates a single task with its size)."""
    ctx = _ctx(tmp_path, ws)
    st = _state(ws)
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 1,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading", "filler": "x" * 70000}]}
    from tenderpack.ai.providers.recorded import PACKET_MARK
    est_old = int(len(PACKET_MARK + json.dumps(packet, ensure_ascii=False, default=str)) / 3.5)
    context = est_old + 16000 + 200                         # fits the old check, not the conversation
    answer = {"addendum": "ADD-03", "state": st, "statements": [], "items": []}
    prov = _recorded([{"response": {"text": json.dumps(answer)}}], images=False, context=context)
    with pytest.raises((W.BatchFailed, B.Refused), match="does not fit"):
        W._converse(ctx, prov, packet, "downstream-001")
    assert prov.requests == [], "a packet that cannot fit the conversation was sent"


# ---------------------------------------------------------------------------------------------- (2) failure classes

def _s11_cassette(tmp: Path, rate_limited: str | None = None, times: int = 5) -> Path:
    """The session-10 recorded workflow (workflow_add03.yaml) with, optionally, HTTP 429 answers at the start of one
    analysis session ('7.x' = batch analysis-004), plus the critic's recorded sessions (s11_workflow_critic.yaml)."""
    data = yaml.safe_load((CASSETTES / "workflow_add03.yaml").read_text(encoding="utf-8"))
    extra = CASSETTES / "s11_workflow_critic.yaml"
    if extra.exists():
        data["sessions"] += yaml.safe_load(extra.read_text(encoding="utf-8"))["sessions"]
    if rate_limited:
        for s in data["sessions"]:
            if s["phase"] == "analysis" and rate_limited in (s.get("when") or {}).get("provisions_include", []):
                s["turns"] = [{"error": {"kind": "http_429", "status": 429, "retryable": True,
                                         "message": "rate_limit_error: Number of request tokens has exceeded your "
                                                    "per-minute rate limit (recorded)"}, "times": times}] + s["turns"]
    p = tmp / "s11_workflow.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


@pytest.fixture(scope="module")
def prev_build(tmp_path_factory):
    from tenderpack.cli import ingest
    out = tmp_path_factory.mktemp("s11-prev") / "build"
    res = ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)
    assert res["exit_code"] == 0
    return out


def test_regression_a_rate_limit_backs_off_then_defers_the_batch_and_stops_cleanly(prev_build, tmp_path):
    """REGRESSION (blind-04, session 10 E129): HTTP 429 from the plan killed analysis batches 8-9 and every downstream
    batch within seconds: a rate limit was retried like any failure (2 s, 4 s) and then the batch FAILED, and the run
    went on asking. A rate limit now backs off (30, 60, 120, 240 s with jitter, bounded by config), then the batch is
    DEFERRED (not failed) and the run stops cleanly with everything done so far checkpointed."""
    cas = _s11_cassette(tmp_path, rate_limited="ADD-03:7.1", times=10)
    slept: list[float] = []
    res = W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=tmp_path / "staging",
                  worklog=tmp_path / "worklog", run_id="rl", route="recorded", cassette=cas, batch_size=8,
                  background_before=False, stop_after="validation", echo=quiet, sleep=slept.append)
    cp = W.load("rl", tmp_path / "staging").data
    b = cp["batches"]
    assert b["analysis-001"]["status"] == "done" and b["analysis-002"]["status"] == "done"
    assert b["analysis-004"]["status"] == "deferred", b["analysis-004"]
    big = [s for s in slept if s >= 20]
    assert len(big) == 4 and 24 <= big[0] <= 36 and 192 <= big[-1] <= 288, slept      # 30, 60, 120, 240 (+/- 20 %)
    assert res["status"] == "deferred" and res["exit_code"] == 5, res
    assert "rate limit" in res["status_reason"] and "resume" in res["status_reason"]
    assert b["analysis-005"]["status"] == "pending"                 # nothing asked after the deferral (stop)


# ---------------------------------------------------------------------------------------------- (1) fixed behaviour

PLACEHOLDER = "placeholder-not-a-real-credential-0000"      # a test value, not a key: nothing is sent anywhere
CAPS = {"max_calls": 6, "max_input_tokens": 10 ** 6, "max_output_tokens": 10 ** 5}


def _ds_item(st, iid, task, statements=(), row="VOL-I-7.1-01"):
    return {"id": iid, "state": st, "statement_type": "row_reading", "task": task, "provision": "ADD-03:3.1",
            "target": row, "statements": list(statements),
            "payload": {"row": row, "interpretation": {"stage": "ADD-03", "quote": "one hundred and eighty (180) days"}},
            "evidence": [{"doc": "VOL-I", "unit_id": "VOL-I:7.1", "page": 4, "kind": "span",
                          "words": "one hundred and eighty (180) days"}]}


def test_downstream_native_structured_output_through_the_common_path(ws, tmp_path, monkeypatch):
    """RECORDED (HttpCassette): the downstream phase on the Messages API adapter, through the request layer: the
    request carries output_config.format with the DOWNSTREAM schema fitted to the limits (the payload a JSON-encoded
    string); the answer's string payload is decoded and parsed locally."""
    from tenderpack.ai.providers import anthropic as A
    from tenderpack.ai.providers.recorded import HttpCassette
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    st = _state(ws)
    item = _ds_item(st, "D1", "row:VOL-I-7.1-01")
    item["payload"] = json.dumps(item["payload"])                  # as a native schema makes the model send it
    answer = json.dumps({"addendum": "ADD-03", "state": st, "statements": [], "items": [item]})
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "GET", "path": "/v1/models/claude-opus-5-5"},
         "response": {"body": {"id": "claude-opus-5-5", "max_input_tokens": 1000000, "max_tokens": 128000,
                               "capabilities": {"structured_outputs": {"supported": True},
                                                "image_input": {"supported": True}}}}},
        {"request": {"method": "POST", "path": "/v1/messages", "body_has": ["output_config.format.schema", "tools"]},
         "response": {"body": {"model": "claude-opus-5-5", "stop_reason": "end_turn",
                               "usage": {"input_tokens": 50, "output_tokens": 40},
                               "content": [{"type": "text", "text": answer}]}}}]})
    monkeypatch.setattr(A, "http_json", cas)
    ctx = _ctx(tmp_path, ws, route="anthropic")
    ctx.s["caps"], ctx.s["model"] = CAPS, "claude-opus-5-5"
    prov = A.AnthropicProvider("claude-opus-5-5", ctx.cfg["routes"]["anthropic"],
                               ctx.cfg["routes"]["anthropic"]["models"]["propose"])
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 1,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading"}]}
    ds = W._converse(ctx, prov, packet, "downstream-001")
    assert cas.pos == len(cas.exchanges)
    body = cas.requests[1]["body"]
    sch = body["output_config"]["format"]["schema"]
    assert sch["$defs"]["DownstreamItem"]["properties"]["payload"]["type"] == "string"
    assert body["output_config"]["effort"] == "high"                # merged with the configured effort
    assert ds.items[0].payload["row"] == "VOL-I-7.1-01"             # decoded, then validated locally


def test_a_malformed_answer_is_repaired_once_then_only_its_bad_items_are_set_aside(ws, tmp_path):
    """The blind-03 downstream sessions wrote free text where statement ids were expected. One re-ask carries the
    errors. After it, an item that still fails its SCHEMA is set aside ITEM BY ITEM (the batch keeps its good items);
    an item whose only problem is a reference (free text where a statement id belongs) is kept for the controller,
    which rates an unknown statement insufficient_evidence with the reason; an answer that is not a set at all after
    the re-ask fails as malformed."""
    ctx = _ctx(tmp_path, ws)
    st = _state(ws)
    good = _ds_item(st, "D1", "row:VOL-I-7.1-01", ["S1"])
    bad = _ds_item(st, "D2", "row:VOL-I-6.1-01", ["the clause says the delivery time moved"], row="VOL-I-6.1-01")
    broken = dict(_ds_item(st, "D3", "row:VOL-I-6.1-01", row="VOL-I-6.1-01"), statement_type="row_rewrite")
    stmts = [{"id": "S1", "kind": "interpretation", "text": "180 days now", "evidence": []}]
    first = json.dumps({"addendum": "ADD-03", "state": st, "statements": stmts, "items": [good, bad, broken]})
    prov = _recorded([{"response": {"text": first}},
                      {"match": {"last_role": "user", "contains": ["REPAIR REQUEST", "not ids", "D2"]},
                       "response": {"text": first}}], images=False)
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 2,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading"}, {"id": "row:VOL-I-6.1-01", "kind": "row_reading"}]}
    ctx.cp.data["batches"]["downstream-001"] = {"phase": "downstream", "tasks": [t["id"] for t in packet["tasks"]],
                                                "status": "running", "attempts": 1}
    ds = W._converse(ctx, prov, packet, "downstream-001")
    assert [it.id for it in ds.items] == ["D1", "D2"] and len(prov.requests) == 2
    b = ctx.cp.batch("downstream-001")
    assert b["request"]["repaired"] is True
    assert [m["id"] for m in b["malformed_items"]] == ["D3"] and "row_rewrite" in b["malformed_items"][0]["errors"][0]
    ref = b["request"]["reference_problems"]
    assert [m["id"] for m in ref] == ["D2"] and "never free text" in ref[0]["errors"][0]
    md = "\n".join(W.requests_section(ctx.cp))
    assert "repaired once" in md and "malformed item 'D3'" in md and "item 'D2' kept with a reference problem" in md
    # not a set at all, twice: the batch fails as malformed (the item-level separation needs a set)
    prov2 = _recorded([{"response": {"text": "I could not finish."}}, {"response": {"text": "Still no JSON, sorry."}}],
                      images=False)
    with pytest.raises(W.BatchFailed, match="malformed"):
        W._converse(ctx, prov2, packet, "downstream-001")
    assert len(prov2.requests) == 2 and ctx.cp.batch("downstream-001")["failure_class"] == "malformed"


def test_a_batch_that_does_not_fit_is_split_by_task_and_a_single_one_escalated(ws, tmp_path):
    from tenderpack.ai import batching as BT
    from tenderpack.ai import requests as R
    ctx = _ctx(tmp_path, ws)
    cp = ctx.cp
    cp.data["downstream"]["tasks"] = {t: {"kind": "row_reading", "batch": "downstream-001"} for t in ("t1", "t2", "t3")}
    cp.data["batches"] = {"downstream-001": {"phase": "downstream", "tasks": ["t1", "t2", "t3"], "status": "running"},
                          "downstream-002": {"phase": "downstream", "tasks": ["t4"], "status": "pending"}}
    sz = BT.request_size("downstream", {"context_tokens": 1000, "source": "test"}, packet_text="x" * 40000)
    assert not sz.fits and "exceed the usable context" in sz.why
    W._split(ctx, "downstream-001", "tasks", ["t1", "t2", "t3"], R.TooLarge("does not fit", sz))
    assert list(cp.data["batches"]) == ["downstream-001", "downstream-001.1", "downstream-001.2", "downstream-002"]
    assert cp.batch("downstream-001")["status"] == "split" and cp.batch("downstream-001.1")["tasks"] == ["t1", "t2"]
    assert cp.data["downstream"]["tasks"]["t3"]["batch"] == "downstream-001.2"
    W._split(ctx, "downstream-001.2", "tasks", ["t3"], R.TooLarge("does not fit", sz))
    assert cp.batch("downstream-001.2")["status"] == "escalated" and cp.batch("downstream-001.2")["size"]["fits"] is False
    # the planner: consecutive groups, nothing dropped or reordered, a unit too large alone on its own
    units = [{"unit_id": f"u{i}", "n": n} for i, n in enumerate([3, 3, 9, 2, 2, 2])]
    groups = BT.plan_units(units, lambda g: sum(u["n"] for u in g) <= 6)
    assert [[u["unit_id"] for u in g] for g in groups] == [["u0", "u1"], ["u2"], ["u3", "u4", "u5"]]


def test_the_unverified_capabilities_notice_reaches_the_log_the_checkpoint_and_the_packet(ws, tmp_path, monkeypatch):
    """--allow-unverified-capabilities (the models endpoint unreachable): the request runs on the configured values and
    says so in the batch's run log, the checkpoint (the batch and the run's notices) and the review packet section."""
    from tenderpack.ai.providers import anthropic as A
    from tenderpack.ai.providers.base import ALLOW_UNVERIFIED_KEY
    from tenderpack.ai.providers.recorded import HttpCassette
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    st = _state(ws)
    answer = json.dumps({"addendum": "ADD-03", "state": st, "statements": [], "items": []})
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "GET"}, "error": {"kind": "network", "message": "blocked (recorded)", "retryable": True}},
        {"request": {"method": "POST", "path": "/v1/messages"},
         "response": {"body": {"model": "claude-opus-5-5", "stop_reason": "end_turn", "usage": {"input_tokens": 9,
                                                                                                 "output_tokens": 9},
                               "content": [{"type": "text", "text": answer}]}}}]})
    monkeypatch.setattr(A, "http_json", cas)
    cfg = C.load()
    cfg[ALLOW_UNVERIFIED_KEY] = True
    ctx = _ctx(tmp_path, ws, route="anthropic", cfg=cfg)
    ctx.s["caps"] = CAPS
    ctx.cp.data["batches"]["downstream-001"] = {"phase": "downstream", "tasks": [], "status": "running", "attempts": 1}
    prov = A.AnthropicProvider("claude-opus-5-5", cfg["routes"]["anthropic"], cfg["routes"]["anthropic"]["models"]["propose"],
                               allow_unverified=True)
    W._converse(ctx, prov, {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks": []}, "downstream-001")
    kinds = [n["kind"] for n in ctx.cp.data["notices"]]
    assert "capabilities_unverified" in kinds and ctx.cp.batch("downstream-001")["notices"]
    log = (Path(ws.staging) / "t11-downstream-001" / "log.jsonl").read_text(encoding="utf-8")
    assert "capabilities unverified" in log and "route_notice" in (ctx.dir / "log.jsonl").read_text(encoding="utf-8")
    md = "\n".join(W.requests_section(ctx.cp))
    assert "**capabilities unverified** (downstream-001)" in md


def test_openrouter_and_ollama_go_through_the_common_path(ws, tmp_path, monkeypatch):
    """RECORDED (HttpCassette): the downstream phase on the OpenRouter and Ollama adapters through the request layer:
    OpenRouter carries response_format json_schema (the listing names structured_outputs); Ollama withholds `format`
    on a turn that offers tools (with_tools false) and SAYS so (a route notice); both answers validated locally; the
    Ollama request is held to the route's own later-turn allowance (batching.prior_turns_tokens 8000)."""
    from tenderpack.ai.providers import ollama as O
    from tenderpack.ai.providers import openrouter as OR
    from tenderpack.ai.providers.recorded import HttpCassette
    st = _state(ws)
    answer = json.dumps({"addendum": "ADD-03", "state": st, "statements": [], "items": [_ds_item(st, "D1",
                                                                                                  "row:VOL-I-7.1-01")]})
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 1,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading"}]}
    listing = {"data": [{"id": "vendor/m", "context_length": 200000, "architecture": {"input_modalities": ["text"]},
                         "supported_parameters": ["tools", "structured_outputs"],
                         "top_provider": {"max_completion_tokens": 32000}}]}
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "POST", "path": "/chat/completions",
                     "body_has": ["response_format.json_schema.schema", "tools"]},
         "response": {"body": {"model": "vendor/m", "usage": {"prompt_tokens": 9, "completion_tokens": 9},
                               "choices": [{"finish_reason": "stop", "message": {"content": answer}}]}}}]})
    monkeypatch.setattr(OR, "http_json", cas)
    ctx = _ctx(tmp_path / "or", ws, route="openrouter")
    ctx.s["caps"] = CAPS
    orp = OR.OpenRouterProvider("vendor/m", ctx.cfg["routes"]["openrouter"], env={"OPENROUTER_API_KEY": PLACEHOLDER},
                                fetch=lambda *a, **k: (200, {}, listing))
    ds = W._converse(ctx, orp, packet, "downstream-001")
    assert cas.pos == 1 and [it.id for it in ds.items] == ["D1"]
    assert cas.requests[0]["body"]["response_format"]["json_schema"]["strict"] is True
    show = {"capabilities": ["completion", "tools"], "model_info": {"qwen3.context_length": 32768}}
    cas2 = HttpCassette({"exchanges": [
        {"request": {"method": "POST", "path": "/api/chat", "body_has": ["tools", "options.num_ctx"],
                     "body_lacks": ["format"]},
         "response": {"body": {"model": "qwen3:30b-a3b", "message": {"content": answer}, "prompt_eval_count": 9,
                               "eval_count": 9, "done_reason": "stop"}}}]})
    monkeypatch.setattr(O, "http_json", cas2)
    ctx2 = _ctx(tmp_path / "ol", ws, route="ollama")
    rcfg = ctx2.cfg["routes"]["ollama"]
    olp = O.OllamaProvider("qwen3:30b-a3b", rcfg, rcfg["models"]["text"], env={}, fetch=lambda *a, **k: (200, {}, show))
    ctx2.cp.data["batches"]["downstream-001"] = {"phase": "downstream", "tasks": [], "status": "running", "attempts": 1}
    ds2 = W._converse(ctx2, olp, packet, "downstream-001")
    assert cas2.pos == 1 and [it.id for it in ds2.items] == ["D1"]
    b = ctx2.cp.batch("downstream-001")
    assert b["request"]["size"]["prior_turns_tokens"] == 8000 and b["request"]["size"]["context_tokens"] == 32768
    assert [n["kind"] for n in b["notices"]] == ["structured_output_withheld"]


# ---------------------------------------------------------------------------------------------- (2) failure classes

class _Flaky:
    """A provider whose first calls fail with the given ProviderErrors, then answer."""
    name, model, paid = "flaky", "flaky-model", False

    def __init__(self, errors):
        self.errors, self.calls = list(errors), 0

    def complete(self, req):
        from tenderpack.ai.providers.base import Response
        self.calls += 1
        if self.errors:
            raise self.errors.pop(0)
        return Response(text="{}", tool_calls=[], usage={}, model_reported=None, raw={})


def test_the_three_failure_classes_are_handled_differently():
    import random
    from tenderpack.ai import hostsession as HS
    from tenderpack.ai import requests as R
    from tenderpack.ai.providers.base import ProviderError
    pol = R.FailurePolicy.from_cfg(C.load(), {"retries": 2, "backoff_s": 2.0})
    assert pol.backoff_s == (30.0, 60.0, 120.0, 240.0) and pol.max_tries == 4 and pol.on_deferred == "stop"
    rng = random.Random(1)
    # provider failure (5xx): bounded retries with a short backoff, then FAILED (never deferred)
    slept: list = []
    with pytest.raises(R.ProviderFailed) as e:
        R.call_provider(_Flaky([ProviderError("http_500", "boom", True, 500)] * 3), None, pol, sleep=slept.append, rng=rng)
    assert slept == [2.0, 4.0] and [a["class"] for a in e.value.attempts] == ["provider"] * 3
    slept.clear()
    assert R.call_provider(_Flaky([ProviderError("http_529", "overloaded", True, 529)]), None, pol, sleep=slept.append,
                           rng=rng).text == "{}" and slept == [2.0]
    # rate limit: the schedule with jitter, then DEFERRED
    slept.clear()
    with pytest.raises(R.RateLimited):
        R.call_provider(_Flaky([ProviderError("http_429", "rate_limit_error", True, 429)] * 9), None, pol,
                        sleep=slept.append, rng=rng)
    assert len(slept) == 4 and all(b * 0.8 <= s <= b * 1.2 for s, b in zip(slept, (30, 60, 120, 240)))
    # a reset named beyond the limit: deferred at once (no tries burnt)
    slept.clear()
    with pytest.raises(R.RateLimited, match="reset"):
        R.call_provider(_Flaky([ProviderError("http_429", "slow down", True, 429, retry_after=3600)]), None, pol,
                        sleep=slept.append, rng=rng)
    assert slept == []
    # after a deferral in the drive: one try, no backoff
    pol2 = R.FailurePolicy.from_cfg(C.load())
    pol2.after_deferral = True
    with pytest.raises(R.RateLimited, match="one try"):
        R.call_provider(_Flaky([ProviderError("http_429", "x", True, 429)]), None, pol2, sleep=slept.append, rng=rng)
    assert slept == []
    # a schema rejection is not a rate limit; a 4xx naming a quota with status 400 is not either
    assert R.classify(ProviderError("http_400", "output_config.format.schema: unsupported", False, 400)) == "provider"
    assert R.classify(ProviderError("api_error_429", "rate limited", True, 429)) == "rate_limit"
    # the host CLI's own rate-limit result (blind-04, verbatim shape) is a rate limit with the reset it names
    import datetime as dt
    res = HS.SessionResult(run_id="x", addendum="ADD-03", provisions=[], started="-", exit_code=1, api_error_status=429,
                           terminal_reason="api_error", error="the host ended with an error (success: 429)",
                           final_text="You've hit your session limit · resets 4:30pm (UTC)")
    assert HS.classify(res) == "rate_limit" and 0 < res.reset_in_s <= 86400
    assert HS.reset_seconds("resets 4:30pm (UTC)", dt.datetime(2026, 10, 4, 16, 8, tzinfo=dt.timezone.utc)) == 1320.0
    assert HS.classify(HS.SessionResult(run_id="y", addendum="A", provisions=[], started="-", exit_code=0,
                                        final_text='{"items": []}')) is None
    assert HS.classify(HS.SessionResult(run_id="z", addendum="A", provisions=[], started="-", timed_out=True,
                                        error="timed out after 900 s")) == "provider"
    # the host session under the policy: rate-limited twice, then a normal end
    seq = [HS.SessionResult(run_id=str(i), addendum="A", provisions=[], started="-", api_error_status=429,
                            error="the host ended with an error (success: 429)", final_text="Rate limit (recorded)")
           for i in range(2)] + [HS.SessionResult(run_id="ok", addendum="A", provisions=[], started="-", exit_code=0)]
    for r in seq:
        HS.classify(r)
    slept.clear()
    assert R.call_host(lambda: seq.pop(0), pol, sleep=slept.append, rng=rng).run_id == "ok" and len(slept) == 2
    with pytest.raises(C.ConfigError):
        R.FailurePolicy.from_cfg({"failures": {"malformed": {"repairs": 3}}})


@pytest.fixture(scope="module")
def critic_rl_run(prev_build, tmp_path_factory):
    """A recorded run where analysis-004 is rate limited (deferred; the run stops), then resumed to the end with the
    rate limit gone. Every provider lookup is recorded, so what each drive asked is known."""
    d = tmp_path_factory.mktemp("s11-rl")
    cas = _s11_cassette(d, rate_limited="ADD-03:7.1", times=10)
    asked: list[tuple[str, str, tuple]] = []
    real = W.WorkflowCassette.provider

    def spy(self, phase, keys, used, _tag=[]):
        asked.append((_tag[0] if _tag else "?", phase, tuple(keys)))
        return real(self, phase, keys, used)
    mp = pytest.MonkeyPatch()
    mp.setattr(W.WorkflowCassette, "provider", spy)
    tag = spy.__defaults__[0]
    try:
        tag[:] = ["first"]
        res1 = W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=d / "staging",
                       worklog=d / "worklog", run_id="rl2", route="recorded", cassette=cas, batch_size=8,
                       background_before=False, echo=quiet, sleep=lambda s: None)
        cp1 = copy.deepcopy(W.load("rl2", d / "staging").data)
        _s11_cassette(d)                                           # the rate limit is over (same file, no 429)
        tag[:] = ["resume"]
        res2 = W.resume("rl2", d / "staging", stop_after="critic", echo=quiet, sleep=lambda s: None)
    finally:
        mp.undo()
    md = W.review_markdown(W.Ctx(W.load("rl2", d / "staging"), quiet))     # the review packet as the review step writes it
    return {"res1": res1, "cp1": cp1, "res2": res2, "cp2": W.load("rl2", d / "staging").data, "asked": asked,
            "dir": Path(res2["run_dir"]), "md": md}


def test_a_resume_after_a_rate_limit_asks_only_what_was_not_done(critic_rl_run):
    r = critic_rl_run
    b1, b2 = r["cp1"]["batches"], r["cp2"]["batches"]
    assert r["res1"]["status"] == "deferred" and b1["analysis-004"]["status"] == "deferred"
    assert b1["analysis-004"]["failure_class"] == "rate_limit" and len(b1["analysis-004"]["failures"]) == 5
    assert [k for k, b in b1.items() if b["status"] == "done"] == ["analysis-001", "analysis-002"]
    resumed = [(p, k) for t, p, k in r["asked"] if t == "resume" and p == "analysis"]
    asked_provs = {x for _, k in resumed for x in k}
    assert not asked_provs & set(b1["analysis-001"]["provisions"] + b1["analysis-002"]["provisions"]), resumed
    assert "ADD-03:7.1" in asked_provs                              # the deferred batch is asked again
    for k in ("analysis-001", "analysis-002"):                      # never re-run: same staged run, one attempt
        assert b2[k]["staged_run"] == b1[k]["staged_run"] and b2[k]["attempts"] == 1
    assert b2["analysis-004"]["status"] == "done" and b2["analysis-004"]["attempts"] == 2
    assert r["res2"]["status"] == "stopped" and r["cp2"]["steps"]["critic"]["status"] == "done"
    assert any(e["event"] == "batch_deferred" and e["batch"] == "analysis-004" for e in r["cp2"]["events"])


def test_the_critic_runs_per_batch_on_the_selected_items_and_survives_the_resume(critic_rl_run):
    r = critic_rl_run
    crit1 = r["cp1"]["batches"]["analysis-002"]["critic"]
    assert crit1["status"] == "done" and crit1["selected"] == 1 and crit1["reviewed"] == 1 and crit1["agrees"] == 1
    critic_calls = [(t, k) for t, p, k in r["asked"] if p == "critic"]
    assert critic_calls == [("first", ("ADD-03/2.4",)), ("resume", ("D3",))]   # one request per batch; 2.4 not re-asked
    assert r["cp2"]["batches"]["analysis-002"]["critic"]["critic_run"] == crit1["critic_run"]
    d = r["dir"]
    comb = yaml.safe_load((d / "ai/rl2-combined/proposals.yaml").read_text(encoding="utf-8"))["proposal_set"]
    it = next(x for x in comb["items"] if x["id"] == "ADD-03/2.4")
    assert it["review"]["critic"]["agrees"] is True and it["verification_status"] == "evidence_verified"
    assert "uncertain_target" in it["review"]["critic"]["selected_because"]
    side = yaml.safe_load((d / "downstream/critic.yaml").read_text(encoding="utf-8"))
    assert side["items"]["D3"]["review"]["critic"]["agrees"] is False
    ds = yaml.safe_load((d / "downstream/proposals.yaml").read_text(encoding="utf-8"))["downstream_set"]
    assert next(x for x in ds["items"] if x["id"] == "D3")["verification_status"] == "interpretation_pending"   # unchanged
    md = r["md"]
    sec = md[md.index("## Critic"):]
    assert "**Agreement between the critic and the proposer is not approval**" in sec
    assert "**ADD-03/2.4** (analysis-002; controller status **evidence_verified**, unchanged)" in sec
    assert "DOES NOT agree" in sec and "class rejection is the reading of 6.6" in sec
    chain = md[md.index("### ADD-03:2.4 "):md.index("### ADD-03:3.1 ")]
    assert "critic (a second model; agreement is not approval): agrees" in chain
    req = md[md.index("## Requests: failures"):]
    line = next(x for x in req.splitlines() if x.startswith("- **analysis-004** (done)"))
    assert "5 failed call(s) (rate_limit)" in line and "DEFERRED" in line


# ---------------------------------------------------------------------------------------------- (3) the host route

FAKE = CASSETTES / "fake_claude_s11.py"


@pytest.fixture()
def fake_dir(tmp_path, monkeypatch):
    d = tmp_path / "fake"
    d.mkdir()
    monkeypatch.setenv("FAKE_S11_DIR", str(d))
    return d


def _host_cfg(images=True):
    cfg = copy.deepcopy(C.load())
    cfg["host_session"] = {**cfg["host_session"], "claude_bin": str(FAKE), "timeout_s": 120,
                           "capabilities": {**cfg["host_session"]["capabilities"], "images": images}}
    cfg["critic"] = {**cfg["critic"], "host": {**cfg["critic"]["host"], "claude_bin": str(FAKE)}}
    cfg["failures"] = {**cfg["failures"], "rate_limit": {**cfg["failures"]["rate_limit"], "seed": 7}}
    return cfg


def _calls(d: Path) -> list[dict]:
    p = d / "calls.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []


def test_host_answer_sessions_go_through_the_same_request_layer(ws, tmp_path, fake_dir):
    """RECORDED host (fake_claude_s11.py stands in for the CLI): a downstream answer with free text in `statements` is
    repaired once by a PLAIN session (no tools) given the answer and the errors; the host plan's rate-limit result backs
    off and then defers; the reading phase is refused before any session when the host's declared capabilities have no
    image input; the critic reviews several items in ONE plain session."""
    from tenderpack.ai import critic as CR
    from tenderpack.ai import hostsession as HS
    from tenderpack.ai import requests as R
    from tenderpack.ai.runlog import RunLog
    cfg = _host_cfg()
    st = _state(ws)
    good = _ds_item(st, "D1", "row:VOL-I-7.1-01", ["S1"])
    bad = dict(good, id="D2", statements=["because the clause changed"])
    stmts = [{"id": "S1", "kind": "interpretation", "text": "180 days now", "evidence": []}]
    (fake_dir / "answer.json").write_text(json.dumps({"addendum": "ADD-03", "state": "${state}", "statements": stmts,
                                                      "items": [good, bad]}).replace('"${state}"', "${state}"))
    (fake_dir / "repair.json").write_text(json.dumps({"addendum": "ADD-03", "state": st, "statements": stmts,
                                                      "items": [good, dict(bad, statements=["S1"])]}))
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 1,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading"}]}
    log = RunLog("t", [tmp_path / "log.jsonl"])
    pol = R.FailurePolicy.from_cfg(cfg)
    fields = {"run_id": "t", "created": "-", "route": "host", "provider": "host-session", "model_requested": "fake",
              "model_reported": None, "task": DOWNSTREAM_TASK}

    def session():
        return HS.AnswerSession(ws, cfg, system="SYSTEM", rules="rules")
    out = R.ask_host(R.spec("downstream"), session(), packet, cfg=cfg, policy=pol, log=log, fields=fields, cwd=tmp_path,
                     sleep=lambda s: None)
    assert [it.id for it in out.answer.items] == ["D1", "D2"] and out.repaired and not out.malformed_items
    assert [c["kind"] for c in _calls(fake_dir)] == ["tool", "repair"]
    rep = _calls(fake_dir)[1]
    assert rep["tools"] == "" and rep["allowed"] is None and "REPAIR REQUEST" in rep["prompt"]
    assert any(n["kind"] == "capabilities_declared" for n in out.notices)
    # the plan's rate limit, as the real CLI printed it (no reset time here): backoff, then deferred
    (fake_dir / "calls.jsonl").unlink()
    (fake_dir / "rate_limit_n").write_text("9")
    slept: list = []
    pol.honour_reset_up_to_s = 0                                   # the recorded message names a reset: defer at once
    with pytest.raises(R.RateLimited, match="reset"):
        R.ask_host(R.spec("downstream"), session(), packet, cfg=cfg, policy=pol, log=log, fields=fields, cwd=tmp_path,
                   sleep=slept.append)
    assert slept == [] and len(_calls(fake_dir)) == 1               # one session, no tries burnt
    pol.honour_reset_up_to_s = 10 ** 6                             # a reset within reach is waited for, bounded
    (fake_dir / "rate_limit_n").write_text("1")
    slept.clear()
    out2 = R.ask_host(R.spec("downstream"), session(), packet, cfg=cfg, policy=pol, log=log, fields=fields,
                      cwd=tmp_path, sleep=slept.append)
    assert len(slept) == 1 and slept[0] >= 24 and out2.attempts[0]["class"] == "rate_limit"
    # the reading phase REQUIRES image input: refused before any session when the host declares none
    (fake_dir / "calls.jsonl").unlink()
    cfg_noimg = _host_cfg(images=False)
    with pytest.raises(R.CapabilityRefused, match="REQUIRES image input"):
        R.ask_host(R.spec("reading"), HS.AnswerSession(ws, cfg_noimg, system="S"), {"task": READING_TASK},
                   cfg=cfg_noimg, policy=pol, log=log, fields=dict(fields, task=READING_TASK), cwd=tmp_path)
    assert _calls(fake_dir) == []
    # the critic: ONE plain session (no tools, --json-schema) for every selected item of a batch
    from tenderpack.ai.contract import DownstreamSet
    ds = DownstreamSet.model_validate({"run_id": "r", "created": "-", "route": "host", "provider": "p",
                                       "model_requested": "m", "addendum": "ADD-03", "state": st,
                                       "items": [good, dict(bad, statements=[])]})
    entries = [(it.id, it, ["consequential_interpretation"], {}) for it in ds.items]
    res = CR.review_batch(CR.batch_packet(ws, "ADD-03", entries), route="host", cfg=cfg, log=log, cwd=tmp_path,
                          policy=pol, sleep=lambda s: None)
    assert set(res["answers"]) == {"D1", "D2"} and not res["missing"]
    calls = _calls(fake_dir)
    assert [c["kind"] for c in calls] == ["critic"] and calls[0]["json_schema"] and calls[0]["tools"] == ""


def test_a_host_route_run_defers_on_the_plans_rate_limit_and_records_it(prev_build, tmp_path, fake_dir):
    """RECORDED host route end to end (fake_claude_s11.py): the analysis sessions start the real MCP server and submit
    through submit_proposals; the plan's rate limit on a later session is retried after a backoff, then deferred; the
    run stops cleanly; the host's declared capabilities are a visible notice."""
    cfg_path = tmp_path / "ai.yaml"
    cfg = _host_cfg()
    cfg["failures"]["rate_limit"].update(honour_reset_up_to_s=0)   # the recorded message names a reset: defer at once
    cfg_path.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (fake_dir / "rate_limit_n").write_text("0")
    slept: list = []
    calls_before = []

    real_run = None
    from tenderpack.ai import hostsession as HS
    real_run = HS.HostSession.run_batch

    def counting(self, packet):
        calls_before.append(packet.get("workflow", {}).get("batch"))
        if len(calls_before) == 2:                                  # the plan's limit from the second session on
            (fake_dir / "rate_limit_n").write_text("9")
        return real_run(self, packet)
    mp = pytest.MonkeyPatch()
    mp.setattr(HS.HostSession, "run_batch", counting)
    try:
        res = W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=tmp_path / "staging",
                      worklog=tmp_path / "worklog", ai_config=cfg_path, run_id="host-rl", route="host", batch_size=8,
                      background_before=False, stop_after="validation", echo=quiet, sleep=slept.append)
    finally:
        mp.undo()
    cp = W.load("host-rl", tmp_path / "staging").data
    b = cp["batches"]
    assert b["analysis-001"]["status"] == "done" and b["analysis-002"]["status"] == "deferred", b["analysis-002"]
    assert res["status"] == "deferred" and res["exit_code"] == 5 and "reset" in res["status_reason"]
    assert b["analysis-002"]["host_session"]["failure_class"] == "rate_limit" and slept == []
    assert b["analysis-003"]["status"] == "pending"
    assert any(n["kind"] == "capabilities_declared" for n in cp["notices"])
    assert [x["kind"] for x in cp["interventions"]] == ["host session (automatic)"] * 2


# ---------------------------------------------------------------------------------------------- (4) the other entry points

def test_ai_propose_defers_a_rate_limit_and_refuses_an_oversize_packet(ws):
    """FOLLOW-UP (session 11): the standalone `ai propose` (controller.propose) on the common request path. Before, its
    own loop retried a 429 at 2 s and 4 s and ended `provider_failed`, and a packet whose conversation cannot fit was
    sent. Now a rate limit backs off and the set is `deferred`; an oversize request is refused before any call."""
    from tenderpack.ai import controller
    slept: list = []
    prov = _recorded([{"error": {"kind": "http_429", "status": 429, "retryable": True,
                                 "message": "rate_limit_error (recorded)"}, "times": 9}], images=False, context=200000)
    ps = controller.propose(ws, "ADD-03", "recorded", C.load(), provider=prov, sleep=slept.append)
    assert ps.status == "deferred" and ps.items == [], ps.status
    assert len([s for s in slept if s >= 20]) == 4, slept
    pk = controller.task_packet(ws, "ADD-03")
    est_old = int(len(controller._packet_text(pk)) / 3.5)
    prov2 = _recorded([{"response": {"text": "{}"}}], images=False, context=est_old + 16000 + 100)
    with pytest.raises(B.Refused, match="does not fit"):
        controller.propose(ws, "ADD-03", "recorded", C.load(), provider=prov2, sleep=lambda s: None)
    assert prov2.requests == []


def test_the_host_session_command_goes_through_the_failure_policy(ws, tmp_path, fake_dir, capsys):
    """FOLLOW-UP (session 11): `tenderpack ai host-session` on the common path: the plan's rate-limit result is
    classified and the session deferred (no tries burnt when the reset it names is beyond the limit); exit code 1 as
    before for a session without a submission."""
    from argparse import Namespace
    from tenderpack.ai import cli_routes
    cfg = _host_cfg()
    cfg["failures"]["rate_limit"]["honour_reset_up_to_s"] = 0
    p = tmp_path / "ai.yaml"
    p.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (fake_dir / "rate_limit_n").write_text("9")
    a = Namespace(ai_cmd="host-session", addendum="ADD-03", provisions="ADD-03:2.1", model=None, max_turns=None,
                  timeout_s=60, claude_bin=str(FAKE), evidence=str(ws.evidence), pack=str(ws.pack), config=str(p),
                  out=str(ws.staging), worklog=str(ws.worklog))
    code = cli_routes.handle(a)
    out = json.loads(capsys.readouterr().out)
    assert code == 1 and out["failure_class"] == "rate_limit" and out["deferred"] is True, out
    assert len(_calls(fake_dir)) == 1
