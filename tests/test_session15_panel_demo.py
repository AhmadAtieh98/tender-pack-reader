import json
from tenderpack.panel import views


def data():
    return {'stage':'ADD-02','items':[
        {'id':k,'kind':'row','fingerprint':'f','label':'ASSUMED APPROVED FOR DEMO',
         'value':{'owner':owner},'evidence':{},'history':[]}
        for k,owner in [('R1','Legal'),('R2','Engineering')]]}


def test_decision_search_works_without_javascript_and_preserves_candidate():
    html=views.interview_page('/t/token/',data(),{'run':'candidate'},query='legal')
    assert 'R1' in html and 'R2' not in html
    assert 'method="get"' in html and 'name="q"' in html
    assert 'name="run" value="candidate"' in html
    assert 'oninput=' not in html


def test_demo_checks_cannot_advertise_an_ordinary_release(tmp_path):
    from tenderpack.interview import mark_outputs
    p=tmp_path/'checks.json'
    p.write_text(json.dumps({'release':{'status':'RELEASABLE','blockers':[]}}))
    mark_outputs(tmp_path)
    checks=json.loads(p.read_text())
    assert 'INTERVIEW DEMO' in checks['release']['status']
    assert 'RELEASABLE' not in views.validated_state(checks)


def test_demo_home_labels_assumptions_and_candidate_behavior(tmp_path):
    from types import SimpleNamespace
    out=tmp_path/'out'; out.mkdir()
    (out/'checks.json').write_text(json.dumps({'_interview_demo':'INTERVIEW DEMO','release':{'status':'INTERVIEW DEMO'}}))
    cfg=SimpleNamespace(out=out,root=tmp_path,evidence=tmp_path/'build')
    html=views.home('/t/token/',cfg,[], 'every proposal stays PROPOSED and out/ is not touched.')
    assert '<h2>Human approval</h2>' not in html
    assert 'every proposal stays PROPOSED' not in html
    assert 'assumed' in html.lower()


def test_a5_deliverables_put_programme_and_marshalling_data_before_the_chart(tmp_path):
    from types import SimpleNamespace
    cfg=SimpleNamespace(root=tmp_path,out=tmp_path/'out')
    html=views.deliverables('/t/token/',cfg)
    a5=html[html.index('A5 Bid programme'):html.index('Review batches')]
    for name in ('programme.csv','programme.json','marshalling.csv','marshalling.json'):
        assert name in a5
        assert a5.index(name)<a5.index('gantt.html')
    assert 'backward' in a5 and 'diagnostic' in a5 and 'chart' in a5


def test_demo_decision_job_is_registered_as_a_build_with_clear_completion_status(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from tenderpack.panel import jobs
    monkeypatch.setattr(jobs.subprocess, 'Popen', lambda *a, **kw: SimpleNamespace(pid=12345, wait=lambda: 0))
    runner = jobs.Jobs(tmp_path, tmp_path / 'jobs')
    rec = runner.start('interview-decision', ['interview', 'apply', '--request', 'request.json'])
    assert rec['group'] == 'build'
    assert 'rebuilt' in jobs.meaning('interview-decision', 0)
