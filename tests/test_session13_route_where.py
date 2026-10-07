"""Session 13, fixer F4 (reviewer R3's recheck N-3): a route recorded as tested says WHERE it was tested. The panel's
route label prints the status with config/routes_status.yaml's `where` for a tested route ("[tested in the cloud
container (sessions 10-12); not yet on the Mac]"), so on the owner's Mac it never reads as tested there. Nothing is
called; no key is read."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_a_tested_route_label_says_where_synthetic():
    from tenderpack.panel import views as V
    routes = {"offline": None, "routes": [
        {"route": "host", "available": True, "why": "", "status": {"status": "tested", "where": "place X; not yet on Y"}},
        {"route": "codex", "available": False, "why": "manual", "status": {"status": "built, unverified",
                                                                           "where": "an MCP test"}}]}
    by = {c["value"]: c for c in V.route_choices(routes, True, False)[0]}
    assert by["host"]["label"].endswith("[tested in place X; not yet on Y]"), by["host"]["label"]
    assert by["codex"]["label"].endswith("[built, unverified]"), by["codex"]["label"]      # untested: no place claimed


def test_the_recorded_host_status_names_the_cloud_container_and_the_mac():
    from tenderpack.ai.cli_routes import route_status
    from tenderpack.panel import views as V
    st = route_status(ROOT / "config/routes_status.yaml")
    assert st["host"]["status"] == "tested"
    assert st["host"]["where"].startswith("the cloud container (sessions 10") and "not yet on the Mac" in st["host"]["where"]
    routes = {"offline": None, "routes": [{"route": "host", "available": True, "why": "", "status": st["host"]}]}
    label = V.route_choices(routes, True, False)[0][0]["label"]
    assert "[tested in the cloud container (sessions 10" in label and "not yet on the Mac]" in label, label
