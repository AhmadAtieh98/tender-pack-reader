import importlib.util,json,sys
from pathlib import Path


def test_export_metadata_matches_clean_contents_and_excludes_runtime_history(tmp_path,monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    spec=importlib.util.spec_from_file_location('prepare_demo',root/'scripts/prepare_interview_demo.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    folder=tmp_path/'operating';folder.mkdir()
    (folder/'INTERVIEW.json').write_text(json.dumps({'files':1,'label':'test'}))
    (folder/'DEMO_GUIDE.txt').write_text('guide')
    runtime=folder/'staging/interview/timing';runtime.mkdir(parents=True)
    (runtime/'private.json').write_text('{}')
    calls=folder/'worklog/model_calls';calls.mkdir(parents=True)
    (calls/'old-add03.jsonl').write_text('old rehearsal answer')
    out=mod.export(folder,tmp_path/'demo.zip')
    import zipfile
    with zipfile.ZipFile(tmp_path/'demo.zip') as archive:
        assert not any('old-add03' in name for name in archive.namelist())
    data=json.loads((folder/'INTERVIEW.json').read_text())
    assert data['files']==out['files']==3
    assert data['interview_demo'] is True


def test_demo_export_names_a_demo_suite_and_preserves_the_source_suite(tmp_path,monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    spec=importlib.util.spec_from_file_location('prepare_demo',root/'scripts/prepare_interview_demo.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    folder=tmp_path/'operating';folder.mkdir()
    source_args=['-m','pytest','tests/test_session13_ordinary_approvals.py']
    (folder/'INTERVIEW.json').write_text(json.dumps({'quick_tests_argv':source_args}))
    (folder/'tests').mkdir()
    (folder/'tests/test_session15_interview.py').write_text('')
    (folder/'tests/test_session16_downstream_context.py').write_text('')
    (folder/'tests/test_session17_audit.py').write_text('')
    (folder/'tests/test_session18_pdf_view.py').write_text('')
    mod.export(folder,tmp_path/'demo.zip')
    data=json.loads((folder/'INTERVIEW.json').read_text())
    assert data['source_quick_tests_argv']==source_args
    assert data['quick_tests_argv']==['-m','pytest','-q','--durations=10','tests/test_session15_interview.py',
                                      'tests/test_session16_downstream_context.py', 'tests/test_session17_audit.py', 'tests/test_session18_pdf_view.py']
    assert 'source checkout' in data['verification_scope']


def test_interview_package_includes_current_context_regressions(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    from make_interview_folder import focused_tests
    assert 'tests/test_session16_downstream_context.py' in focused_tests(root)


def test_interview_package_includes_pdf_viewer_regressions(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    from make_interview_folder import focused_tests
    assert 'tests/test_session18_pdf_view.py' in focused_tests(root)
