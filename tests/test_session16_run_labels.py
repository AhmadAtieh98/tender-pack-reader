from tenderpack.panel import views


def test_run_page_displays_uppercase_critic_disagreements():
    md='''## Critic (a second model)

- **R-1** (controller status pending)
  - critic (a second model; agreement is not approval): DOES NOT agree
    - concern: The consequence's trigger is missing.
- **R-2** (controller status pending)
  - critic (a second model; agreement is not approval): agrees
'''
    found=views.critic_disagreements(md)
    assert len(found)==1
    assert 'R-1' in found[0] and 'trigger is missing' in found[0]


def test_simulated_run_labels_do_not_claim_no_decisions_exist(tmp_path):
    cp={'status':'partial','addendum':'ADD-03','approval':{'status':'simulated'},
        'completeness':{'status':'partial','provisions':{'unresolved':['ADD-03:6.1']}}}
    listing=views.candidate_outputs('/t/token/','demo',tmp_path,cp)
    html=views.run_detail('/t/token/','demo',tmp_path,cp,None,None,(),listing)
    assert 'Everything the run proposed is PROPOSED' not in html
    assert 'Nothing is accepted' not in html
    assert 'approvals are simulated' in html
    assert 'remain editable' in html
    assert '1 provision(s) unresolved' in html
