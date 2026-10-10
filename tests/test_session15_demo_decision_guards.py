from tenderpack import review


def test_only_assumed_acceptances_are_excluded_from_human_override_guards():
    records=[
        {'kind':'row','item':'R1','decision':'accept','origin':'interview_demo'},
        {'kind':'row','item':'R2','decision':'reject','origin':'interview_demo'},
        {'kind':'row','item':'R3','decision':'accept','reviewer':'Operator'},
        {'kind':'row','item':'R1','decision':'reject','reviewer':'Operator'},
    ]
    assert review.ai_guard_decisions({'interview_demo':True},records)==records[1:]
    assert review.ai_guard_decisions({},records)==records
    assert len(records)==4


def test_demo_run_report_does_not_claim_the_workflow_approved_nothing(tmp_path):
    import yaml
    from types import SimpleNamespace
    from tenderpack.ai.workflow import approval
    dec=tmp_path/'decisions.yaml';dec.write_text(yaml.safe_dump({'decisions':[{
        'kind':'row','item':'R1','decision':'accept','origin':'interview_demo','reviewer':'Interview demo assumption'}]}))
    pack=tmp_path/'pack.yaml';pack.write_text(yaml.safe_dump({'interview_demo':True,'decisions':str(dec)}))
    result=approval(SimpleNamespace(data={'candidate':{'pack':str(pack)}}))
    assert result['status']=='simulated'
    assert result['assumed_reviews']==1
    assert 'nothing approved' not in result['by_the_workflow']
    assert 'R1' in result['decisions'][0]
