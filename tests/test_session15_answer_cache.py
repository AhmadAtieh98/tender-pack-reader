from types import SimpleNamespace
from tenderpack.ai import hostsession as H


def test_answer_resume_reuses_bytes_but_changed_state_reasks(monkeypatch, tmp_path):
    state = {"hash": "one"}
    ws = SimpleNamespace(ai_config=None, staging=tmp_path / "staging", identity=lambda: SimpleNamespace(model_dump=lambda **kw: dict(state)))
    cfg = {"host_session": {"model": "fixture", "durable_answers": True}}
    calls = []
    def run(self, packet):
        calls.append(packet)
        self.last = H.SessionResult(run_id="fixture", addendum="ADD-03", provisions=[], started="now", exit_code=0,
                                    final_text='{"items":[]}', elapsed_s=10, usage={"output_tokens": 10})
        return {}
    monkeypatch.setattr(H.HostSession, "run_batch", run)
    packet = {"addendum": "ADD-03", "tasks": [{"id": "T1"}]}
    first = H.AnswerSession(ws, cfg, phase="downstream")
    first.run_batch(packet)
    resumed = H.AnswerSession(ws, cfg, phase="downstream")
    resumed.run_batch(packet)
    assert len(calls) == 1
    assert resumed.last.final_text == first.last.final_text
    assert resumed.last.elapsed_s == 0 and resumed.last.usage == {}
    state["hash"] = "two"
    H.AnswerSession(ws, cfg, phase="downstream").run_batch(packet)
    assert len(calls) == 2


def test_answer_cache_invalidates_when_runtime_code_changes(monkeypatch, tmp_path):
    identity={'content_sha256':'before'}
    from tenderpack.ai import checkpoint
    monkeypatch.setattr(checkpoint, 'code_identity', lambda root: dict(identity))
    ws=SimpleNamespace(ai_config=None,staging=tmp_path/'staging',identity=lambda: SimpleNamespace(model_dump=lambda **kw:{}))
    cfg={'host_session':{'model':'fixture','durable_answers':True}}
    calls=[]
    def run(self, packet):
        calls.append(packet)
        self.last=H.SessionResult(run_id='fixture',addendum='ADD-03',provisions=[],started='now',exit_code=0,final_text='{}')
        return {}
    monkeypatch.setattr(H.HostSession,'run_batch',run)
    packet={'addendum':'ADD-03','tasks':[]}
    H.AnswerSession(ws,cfg,phase='downstream').run_batch(packet)
    identity['content_sha256']='after'
    H.AnswerSession(ws,cfg,phase='downstream').run_batch(packet)
    assert len(calls)==2
