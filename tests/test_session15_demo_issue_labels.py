from tenderpack import human_owned as H, stage2
from tenderpack.util import ROOT


def test_assumed_issue_review_does_not_claim_a_real_decision_or_close_the_issue():
    issue = {"id": "I-X", "text": "Which clause governs remains unknown", "owner": "Legal"}
    decision = {"kind": "issue", "item": "I-X", "decision": "accept", "origin": "interview_demo",
                "reviewer": "Interview demo assumption", "date": "2026-10-08",
                "fingerprint": H.entry_fingerprint("issue", issue)}
    label = H.issue_label("I-X", issue, [decision])
    assert "DEMO" in label and "ASSUMED" in label and "OPEN" in label
    assert "DECIDED" not in label and "decision recorded" not in label
    assert issue.get("status", "open") == "open"
    real = dict(decision, origin="operator", reviewer="Owner")
    assert H.issue_label("I-X", issue, [real]).startswith("DECIDED (decision recorded: Owner")


def test_demo_a3_banner_does_not_claim_owner_confirmation_or_all_proposed():
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    r["cfg"]["interview_demo"] = True
    page = stage2.a3(r, stage2.collect_issues(r, None), None)
    assert "DEMO" in page["banner"] and "assumed" in page["banner"]
    assert "confirmed by the owner" not in page["banner"]
    assert "every register row and amendment op is PROPOSED" not in page["banner"]
