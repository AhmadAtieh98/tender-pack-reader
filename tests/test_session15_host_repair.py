from types import SimpleNamespace
from tenderpack.ai import requests as R,hostsession as H


def test_host_repair_preserves_failure_policy_object(monkeypatch,tmp_path):
    policy=R.FailurePolicy(host_retries=1)
    monkeypatch.setattr(H,'PlainSession',lambda *a,**kw:SimpleNamespace(label='repair',run=lambda *a:None))
    def call(run, passed, **kw):
        assert passed is policy
        return SimpleNamespace(structured_output=None,final_text='{}',elapsed_s=0,model_reported=[],error=None,host_plan_cost_usd=None)
    monkeypatch.setattr(R,'call_host',call)
    R.host_repair(R.spec('downstream',route='host'),{},'{}',[],[],tmp_path,None,policy)
