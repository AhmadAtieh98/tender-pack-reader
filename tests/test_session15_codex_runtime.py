import base64
import json
from pathlib import Path
from types import SimpleNamespace

from tenderpack.ai import hostsession as HS, policy


def cfg():
    return {"host_session": {"driver": "codex", "codex_bin": "/bin/echo", "model": "configured-test-model",
                             "reasoning_effort": "high", "max_mcp_calls": 120, "timeout_s": 420}}


def test_codex_driver_is_selected_for_tools_and_plain_critic(tmp_path):
    ws = SimpleNamespace(ai_config=None)
    host = HS.HostSession(ws, cfg())
    cmd = host.command(tmp_path / "mcp.json")
    assert "tenderpack.ai.codex" in cmd
    assert "codex" in host.host_model_label()
    plain = HS.PlainSession(cfg(), policy.compose("critic", "host"), label="critic")
    assert "tenderpack.ai.codex" in plain.command()
    assert "codex" in plain.host_model_label()


def test_bad_logged_image_does_not_discard_valid_native_image_or_tool_text():
    from tenderpack.ai import codex
    good = {"type": "image", "mimeType": "image/png", "data": base64.b64encode(b"pixels").decode()}
    out = codex.normalize_mcp_result({"content": [good, {"type": "image", "data": "bad truncated %"},
                                                 {"type": "text", "text": '{"ok":true}'}]})
    assert good in out["content"]
    assert len(out["_codex_image_transport_diagnostics"]) == 1
    assert json.loads(next(b["text"] for b in out["content"] if b["type"] == "text"))["ok"]


def test_event_translation_does_not_fabricate_model_or_usage_and_keeps_final_answer():
    from tenderpack.ai import codex
    events = [None, "malformed", {"type": "item.completed", "item": "broken"},
              {"type": "item.completed", "item": {"type": "agent_message", "text": '{"items":[]}'}},
              {"type": "turn.completed"}]
    converted, final, usage, turns, models, errors = codex.event_adapter(events, "", [], "configured")
    assert final == '{"items":[]}'
    assert models == [] and usage == {} and turns == 1
    assert converted == []


def test_codex_tool_call_limit_is_independent_of_model_turn_limit(tmp_path):
    host = HS.HostSession(SimpleNamespace(ai_config=None), cfg(), max_turns=1)
    cmd = host.command(tmp_path / "mcp.json")
    settings = json.loads(cmd[cmd.index("--codex-settings") + 1])
    assert settings["max_mcp_calls"] == 120
    assert settings["reasoning_effort"] == "high"


def test_codex_critic_ignores_legacy_claude_binary_override():
    plain = HS.PlainSession(cfg(), policy.compose("critic", "host"), claude_bin="missing-claude")
    host = HS.HostSession(SimpleNamespace(ai_config=None), cfg(), claude_bin="missing-claude")
    assert plain.claude_bin == host.claude_bin == "/bin/echo"


def test_malformed_native_content_and_error_are_reported_without_crashing():
    from tenderpack.ai import codex
    assert codex.normalize_mcp_result({"content": [None]})["content"] == []
    result = codex.event_adapter([{"type": "error", "error": "transport interrupted"}], "", [], "configured")
    assert "transport interrupted" in result[-1][0]


def test_host_model_slots_include_plain_critic_and_tool_sessions():
    import threading, time
    from concurrent.futures import ThreadPoolExecutor
    cfg2 = cfg()
    cfg2["concurrency"] = {"max_total_host_sessions": 2}
    guard = threading.Lock()
    active = peak = 0
    def work():
        nonlocal active, peak
        with HS.model_slot(cfg2):
            with guard:
                active += 1
                peak = max(peak, active)
            time.sleep(0.03)
            with guard:
                active -= 1
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(lambda _: work(), range(5)))
    assert peak == 2


def test_region_image_delivery_is_recorded_with_hashes(tmp_path):
    import base64
    host = HS.AnswerSession(SimpleNamespace(ai_config=None), cfg(), phase='reading')
    res = HS.SessionResult(run_id='test', addendum='ADD-03', provisions=[], started='now')
    call = {'name':'get_region', 'arguments':{'region_id':'IMG1'}}
    payload = {'content':[{'type':'image','mimeType':'image/png','data':base64.b64encode(b'pixels').decode()},
                          {'type':'text','text':'{}'}]}
    host._tool_result(payload,call,res,SimpleNamespace(event=lambda *a,**kw:None))
    assert res.images_received[0]['region_id']=='IMG1'
    assert res.images_received[0]['received'][0]['bytes']==6


def test_codex_transport_refuses_offline_before_a_process(monkeypatch):
    import io
    from tenderpack.ai import codex
    from tenderpack.ai.offline import OfflineError
    monkeypatch.setenv('TENDERPACK_OFFLINE','1')
    monkeypatch.setattr('sys.stdin',io.StringIO('test'))
    monkeypatch.setattr(codex.subprocess,'Popen',lambda *a,**kw: (_ for _ in ()).throw(AssertionError('process started')))
    with __import__('pytest').raises(OfflineError):
        codex.main(['--codex-settings',json.dumps({'model':'fixture','timeout_s':1})])


def test_panel_and_routes_detect_the_selected_codex_driver(tmp_path):
    import yaml
    from tenderpack.panel.server import Panel
    from tenderpack.panel.views import route_choices
    from tenderpack.ai.cli_routes import availability
    p=tmp_path/'ai.yaml';p.write_text(yaml.safe_dump(cfg()))
    panel=object.__new__(Panel);panel.cfg=SimpleNamespace(ai_config=p)
    assert panel.host_found()
    ok,why=availability({'route':'host'},cfg(),False)
    assert ok and 'Codex' in why
    choices,_,_=route_choices({'host_driver':'codex','routes':[{'route':'host'}]},True,False)
    assert 'Codex' in choices[0]['label'] and 'Claude' not in choices[0]['label']
