import json,subprocess
from types import SimpleNamespace
from tenderpack.ai.checkpoint import code_identity


def test_portable_copy_does_not_inherit_parent_repository_commit(tmp_path,monkeypatch):
    folder=tmp_path/'portable';folder.mkdir()
    (folder/'INTERVIEW.json').write_text(json.dumps({'base':'509be48'}))
    def run(args,**kw):
        if '--show-toplevel' in args:return SimpleNamespace(returncode=0,stdout=str(tmp_path))
        return SimpleNamespace(returncode=0,stdout='unrelated-parent-commit' if 'HEAD' in args else '')
    monkeypatch.setattr(subprocess,'run',run)
    got=code_identity(folder)
    assert got['git_head'] is None
    assert got['package_base']=='509be48'


def test_repack_keeps_the_packages_base_when_inside_another_repo(tmp_path,monkeypatch):
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('interview_builder',Path(__file__).resolve().parents[1]/'scripts/make_interview_folder.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    (tmp_path/'INTERVIEW.json').write_text(json.dumps({'base':'509be48'}))
    monkeypatch.setattr(module,'_git',lambda repo,*args: str(tmp_path.parent) if '--show-toplevel' in args else 'wrong-parent')
    assert module.base_revision(tmp_path)=='509be48'
