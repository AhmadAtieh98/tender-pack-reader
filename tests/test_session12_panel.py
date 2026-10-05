"""Session 12, part 5: the owner's local operating panel (`tenderpack panel`; tenderpack/panel/).

The panel is a plain localhost page over the existing engine: every action is a real `python -m tenderpack ...` job in a
subprocess with its own log under <panel_dir>/jobs/<id>/. These tests start the panel on a free port with every path
pointed at a disposable folder (the evidence build is ingested afresh; staging, outputs, the work log, the panel's jobs
and uploads all live under tmp), so the real out/, staging/, curation/ and config/ are never written; they are
fingerprinted around the run to show it.

What is NOT tested here (pending on the Mac, docs/PANEL.md): a browser click-through, `--open`, and the Mac launcher's
item 7. The recorded route replays a hand-written cassette: it shows the plumbing from upload to results, not how well
any real model proposes."""
from __future__ import annotations

import io
import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

from ai_fixture import CASSETTES, ROOT, tree_files

PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"      # synthetic (a rehearsal input), matches the cassette
CASSETTE = CASSETTES / "workflow_add03.yaml"
REAL = [ROOT / "curation", ROOT / "config", ROOT / "out", ROOT / "staging"]
PY = sys.executable


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def _req(url: str, data: bytes | None = None, headers: dict | None = None, method: str | None = None):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with _opener.open(r, timeout=120) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def _get(panel, path: str = ""):
    return _req(panel.url + path)


def _post(panel, path: str, fields: dict):
    return _req(panel.url + path, urllib.parse.urlencode(fields).encode(),
                {"Content-Type": "application/x-www-form-urlencoded"})


def _multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    b = "----panelboundary7d1f"
    out = b""
    for k, v in fields.items():
        out += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, (name, data) in files.items():
        out += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{name}\"\r\n"
                f"Content-Type: application/pdf\r\n\r\n").encode() + data + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return out, f"multipart/form-data; boundary={b}"


def _upload(panel, fields: dict, name: str, data: bytes):
    body, ctype = _multipart(fields, {"pdf": (name, data)})
    return _req(panel.url + "addendum/start", body, {"Content-Type": ctype})


def _job_id(headers: dict) -> str:
    loc = headers.get("Location") or headers.get("location") or ""
    m = re.search(r"/jobs/([A-Za-z0-9._-]+)$", loc)
    assert m, f"no job in the redirect: {loc!r}"
    return m.group(1)


def _job(panel, jid: str) -> dict:
    return json.loads((panel.cfg.panel_dir / "jobs" / jid / "job.json").read_text(encoding="utf-8"))


def _wait(panel, jid: str, timeout: float = 400) -> dict:
    t0 = time.time()
    while time.time() - t0 < timeout:
        j = _job(panel, jid)
        if j["status"] != "running":
            return j
        time.sleep(0.3)
    raise AssertionError(f"job {jid} still running after {timeout}s")


def _checkpoint(staging: Path, run_id: str) -> dict | None:
    try:
        return json.loads((staging / "runs" / run_id / "checkpoint.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


@pytest.fixture(scope="module")
def real_before():
    return tree_files(*REAL)


@pytest.fixture(scope="module")
def panel(pack, tmp_path_factory, real_before):
    """A panel on a free port over a disposable workspace (the real pack configuration is only read)."""
    from tenderpack.panel.server import Panel, PanelConfig
    d = tmp_path_factory.mktemp("panel")
    cfg = PanelConfig(root=ROOT, pack=ROOT / "config/pack.yaml", evidence=pack["out"], out=d / "out",
                      staging=d / "staging" / "ai", worklog=d / "worklog", panel_dir=d / "panel",
                      cassette=CASSETTE, decisions=d / "decisions.yaml", approvals=d / "approvals.yaml")
    p = Panel(cfg, port=0, log=io.StringIO())                    # follow-up: the access log is captured to check it
    p.start()
    p.tmp = d
    yield p
    p.stop()


def _run_location(headers: dict) -> str:
    """Starting a run lands on the run's page (follow-up): the run id from the redirect."""
    loc = headers.get("Location") or headers.get("location") or ""
    m = re.search(r"/runs/([A-Za-z0-9._-]+)$", loc)
    assert m, f"not a run page: {loc!r}"
    return m.group(1)


def _job_for_run(panel, run_id: str) -> str:
    for d in sorted((panel.cfg.panel_dir / "jobs").iterdir()):
        j = json.loads((d / "job.json").read_text(encoding="utf-8"))
        if j.get("meta", {}).get("run_id") == run_id and j["kind"] == "ai-run":
            return j["id"]
    raise AssertionError(f"no job for run {run_id}")


REFRESH10 = '<meta http-equiv="refresh" content="10">'


# ---------------------------------------------------------------------------------------------- binding and access

def test_the_panel_binds_to_loopback_only_on_a_free_port(panel):
    host, port = panel.httpd.server_address[:2]
    assert host == "127.0.0.1" and port > 0
    assert panel.url == f"http://127.0.0.1:{port}/t/{panel.token}/"
    assert len(panel.token) >= 24
    other = None
    try:
        other = socket.gethostbyname(socket.gethostname())
    except OSError:
        pass
    if other and not other.startswith("127."):                  # not reachable on another interface
        with pytest.raises(OSError):
            socket.create_connection((other, port), timeout=2).close()
    st, _, body = _get(panel)
    assert st == 200
    html_ = body.decode()
    assert "<title>tenderpack: operating panel</title>" in html_
    assert "<script" not in html_.lower()
    # nothing external is loaded or linked (changed in the follow-up: HOME now quotes the routes' own reason text,
    # which names the local Ollama address as text, so the check looks at link and resource attributes only)
    assert not re.search(r'(?:href|src|action)="(?:https?:)?//', html_)


def test_a_request_without_the_token_or_from_another_host_name_is_refused(panel):
    root = f"http://127.0.0.1:{panel.port}/"
    for url in (root, root + "jobs", root + "t/wrong-token/", root + f"t/{panel.token[:-1]}/",
                root + "file/out/a1/a1.csv"):
        st, _, body = _req(url)
        assert st == 403, url
        assert panel.token not in body.decode("utf-8", "replace")
    st, _, _ = _req(panel.url, headers={"Host": f"evil.example:{panel.port}"})   # DNS rebinding
    assert st == 403
    st, _, _ = _req(panel.url, headers={"Host": f"localhost:{panel.port}"})
    assert st == 200


def test_path_traversal_and_symlinks_out_of_the_areas_are_refused(panel):
    out = panel.cfg.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "ok.txt").write_text("fine", encoding="utf-8")
    (out / "link.txt").symlink_to(ROOT / "config" / "pack.yaml")
    (out / "dirlink").symlink_to(ROOT / "curation")
    st, _, body = _get(panel, "file/out/ok.txt")
    assert st == 200 and body == b"fine"
    for bad in ("file/out/../../config/pack.yaml", "file/out/..%2f..%2fconfig%2fpack.yaml",
                "file/out/%2e%2e/%2e%2e/etc/passwd", "file/out/link.txt", "file/out/dirlink/approvals.yaml",
                "file/curation/approvals.yaml", "file/out//etc/passwd", "file/out/a1/..", "download/out/../x",
                "file/runs/x/candidate/curation/approvals.yaml", "file/sources/../config/ai.yaml",
                "file/out/ok.txt%00.pdf", "file/out\\..\\x"):
        st, _, body = _get(panel, bad)
        assert st in (400, 403, 404), (bad, st)
        assert b"pack_id" not in body and b"approvals" not in body.lower() or st == 404, bad
    (out / "ok.txt").unlink()
    (out / "link.txt").unlink()
    (out / "dirlink").unlink()


def test_an_upload_that_is_not_a_pdf_or_too_large_is_refused(panel):
    jobs_before = set(os.listdir(panel.cfg.panel_dir / "jobs"))
    st, _, body = _upload(panel, {"addendum": "ADD-03", "route": "recorded"}, "x.pdf", b"<html>not a pdf</html>")
    assert st == 400 and b"not a PDF" in body
    _, ctype = _multipart({"addendum": "ADD-03", "route": "recorded"}, {"pdf": ("big.pdf", b"%PDF-1.4\n")})
    st, _, _ = _raw_post_with_length(panel, "addendum/start", ctype, 60 * 1024 * 1024)
    assert st == 413
    st, _, body = _upload(panel, {"addendum": "ADD-3; rm -rf /", "route": "recorded"}, "a.pdf", PDF.read_bytes())
    assert st == 400 and b"ADD-NN" in body
    st, _, body = _upload(panel, {"addendum": "ADD-03", "route": "anthropic"}, "a.pdf", PDF.read_bytes())
    assert st == 400 and b"route" in body
    assert set(os.listdir(panel.cfg.panel_dir / "jobs")) == jobs_before        # nothing started


def _raw_post_with_length(panel, path: str, ctype: str, length: int):
    """A request announcing a body larger than the limit: refused from the header, before the body is read."""
    s = socket.create_connection(("127.0.0.1", panel.port), timeout=30)
    try:
        s.sendall((f"POST /t/{panel.token}/{path} HTTP/1.1\r\nHost: 127.0.0.1:{panel.port}\r\n"
                   f"Content-Type: {ctype}\r\nContent-Length: {length}\r\nConnection: close\r\n\r\n").encode())
        data = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            data += chunk
    finally:
        s.close()
    st = int(data.split(b" ", 2)[1])
    return st, {}, data


# ---------------------------------------------------------------------------------------------- output parity

@pytest.fixture(scope="module")
def built_out(panel):
    """`outputs` run once through the panel (a real job) into the panel's disposable out folder."""
    st, h, _ = _post(panel, "jobs/start", {"action": "outputs"})
    assert st == 303
    jid = _job_id(h)
    return jid, _wait(panel, jid)


def test_outputs_through_the_panel_are_byte_identical_to_a_direct_run(panel, built_out, pack, tmp_path):
    jid, j = built_out
    assert j["exit_code"] == 0 and j["status"] == "finished", j
    assert j["argv"][:3] == [PY, "-m", "tenderpack"] and j["argv"][3] == "outputs"
    st, _, body = _get(panel, f"jobs/{jid}")
    assert st == 200 and "OUTPUTS PUBLISHED" in body.decode()
    direct = tmp_path / "out-direct"
    res = subprocess.run([PY, "-m", "tenderpack", "outputs", "--evidence", str(pack["out"]), "--out", str(direct),
                          "--pack", str(ROOT / "config/pack.yaml")], cwd=ROOT, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout[-2000:]
    a = {p.relative_to(panel.cfg.out).as_posix(): p.read_bytes() for p in panel.cfg.out.rglob("*") if p.is_file()}
    b = {p.relative_to(direct).as_posix(): p.read_bytes() for p in direct.rglob("*") if p.is_file()}
    assert sorted(a) == sorted(b) and len(a) > 50
    differ = [k for k in a if a[k] != b[k]]
    assert differ == [], differ                                  # the guide names no timestamp line: none excluded
    # the home page now shows the validated state, the four separate records and the deliverables
    st, _, body = _get(panel)
    t = body.decode()
    for s in ("Execution", "Completeness", "Structural validation", "Human approval", "BASE", "ADD-01", "ADD-02",
              "file/out/a1/a1.xlsx", "download/out/a1/a1.xlsx", "file/out/a3/a3.pdf", "file/out/a5/gantt.pdf",
              "file/out/a4/clarification_register.md", "file/out/review/index.html", "proposed"):
        assert s in t, s
    st, h, body = _get(panel, "download/out/a1/a1.xlsx")
    assert st == 200 and "attachment" in h["Content-Disposition"] and body == (panel.cfg.out / "a1/a1.xlsx").read_bytes()


# ---------------------------------------------------------------------------------------------- upload to results

@pytest.fixture(scope="module")
def full_run(panel):
    st, _, page = _get(panel, "addendum")
    assert st == 200
    t = page.decode()
    assert 'name="route"' in t and "recorded" in t and "ollama" in t and 'name="offline"' in t
    assert "base_run" in t                                       # offered, or disabled with "not in this build"
    home = _get(panel)[2].decode()                               # follow-up: the new-addendum box is on HOME
    box = home[home.index("New addendum"):]
    assert f'action="/t/{panel.token}/addendum/start"' in box and 'enctype="multipart/form-data"' in box
    assert 'value="ADD-03"' in box and 'type="file" name="pdf"' in box and 'name="offline"' in box
    assert home.index("New addendum") < home.index("Outputs in")  # at the top, above the full listing (the
    # deliverables strip sits above it: the coordinator's usability change of 19:02)
    st, h, body = _upload(panel, {"addendum": "ADD-03", "route": "recorded", "model": ""}, "ADD-03 <b>No 3<b>.pdf",
                          PDF.read_bytes())
    assert st == 303, body[:500]
    run_id = _run_location(h)                                    # starting lands on the run page
    jid = _job_for_run(panel, run_id)
    st, _, during = _get(panel, f"runs/{run_id}")
    j = _wait(panel, jid)
    st2, _, after = _get(panel, f"runs/{run_id}")
    return {"job": j, "jid": jid, "during": (st, during.decode()), "after": (st2, after.decode())}


def test_the_run_page_follows_the_run_and_then_lists_the_candidate_outputs(panel, full_run):
    st, during = full_run["during"]
    assert st == 200 and REFRESH10 in during                     # refreshes itself while the job runs (no script)
    assert "<script" not in during.lower() and "Stop" in during
    steps = during[during.index("Steps"):]
    assert "ingest" in steps and ("running" in steps or "pending" in steps)
    st, after = full_run["after"]
    assert st == 200 and 'http-equiv="refresh"' not in after       # ... and only while it runs
    for s in ("Steps", "ingest", "review", "done", "Batches", "Critic", "What it needs from you", "Resume",
              "CANDIDATE outputs", "Nothing is accepted; decisions are recorded with tenderpack accept/reject"):
        assert s in after, s
    cand = after[after.index("CANDIDATE outputs"):]
    i_review, i_diff = cand.index("review/index.html"), cand.index("review/diff.md")
    i_a1 = cand.index("candidate/out/a1/a1.xlsx")
    assert i_review < i_diff < i_a1                              # the review packet first, the diff next, then A1-A5
    for g in ("A1 ", "A2 ", "A3 ", "A4 ", "A5 "):
        assert g in cand, g
    run_id = full_run["job"]["meta"]["run_id"]
    out = panel.cfg.staging / "runs" / run_id / "candidate" / "out"
    for root, _, files in os.walk(out):                          # the same listing as HOME: every candidate file
        for f in files:
            rel = (Path(root) / f).relative_to(out).as_posix()
            assert f"runs/{run_id}/candidate/out/{urllib.parse.quote(rel)}" in cand, rel


def test_upload_to_results_runs_a_real_ai_run_job_to_completion(panel, full_run):
    j = full_run["job"]
    run_id = j["meta"]["run_id"]
    assert j["kind"] == "ai-run" and j["exit_code"] == 0, j
    assert j["argv"][3:6] == ["ai", "run", "ADD-03"] and "--route" in j["argv"] and "recorded" in j["argv"]
    sha = j["meta"]["upload_sha256"]
    stored = panel.cfg.panel_dir / "uploads" / f"{sha}.pdf"
    assert stored.read_bytes() == PDF.read_bytes() and j["argv"][j["argv"].index("--pdf") + 1] == str(stored)
    assert j["meta"]["original_name"] == "ADD-03 bNo 3b.pdf"        # sanitised, kept only in the job record
    assert j["meta"]["synthetic"].startswith("rehearsals/")        # a rehearsal input is labelled synthetic
    cp = _checkpoint(panel.cfg.staging, run_id)
    assert cp["status"] == "partial"
    st, _, body = _get(panel, f"jobs/{full_run['jid']}")
    t = body.decode()
    assert run_id in t and "&lt;b&gt;" not in t and "<b>No 3" not in t
    assert "python" in t and "-m tenderpack ai run ADD-03" in t      # the exact command, to repeat in a terminal
    st, _, body = _get(panel, "runs")
    assert st == 200 and run_id in body.decode()
    st, _, body = _get(panel, f"runs/{run_id}")
    t = body.decode()
    for s in ("Execution", "Completeness", "Structural validation", "Human approval", "partial", "Pending questions",
              "PROPOSED", "Resume", "unresolved", "synthetic"):
        assert s in t, s
    assert t.index("Execution") < t.index("Completeness") < t.index("Structural validation") < t.index("Human approval")


def test_the_candidate_review_is_labelled_and_never_writes_out(panel, full_run, real_before):
    run_id = full_run["job"]["meta"]["run_id"]
    before = {p: p.read_bytes() for p in panel.cfg.out.rglob("*") if p.is_file()}
    st, _, body = _get(panel, f"runs/{run_id}/candidate")
    t = body.decode()
    assert st == 200 and "CANDIDATE, not approved; the validated outputs are under out/" in t
    links = sorted(set(re.findall(r'href="(/t/[^"]+/(?:file|download)/runs/[^"]+)"', t)))
    assert any(x.endswith("candidate/out/a1/a1.xlsx") for x in links) and any(x.endswith("review/index.html") for x in links)
    for x in links:
        st, h, b = _req(f"http://127.0.0.1:{panel.port}{x}")
        assert st == 200, x
        if x.endswith(".html") and "/file/" in x:
            assert b"CANDIDATE, not approved; the validated outputs are under out/" in b
            assert "default-src 'none'" in h["Content-Security-Policy"]
    after = {p: p.read_bytes() for p in panel.cfg.out.rglob("*") if p.is_file()}
    assert after == before                                       # nothing copied into the validated outputs
    cand = panel.cfg.staging / "runs" / run_id / "candidate" / "out"
    assert (cand / "a1/a1.xlsx").is_file() and not (panel.cfg.out / "CANDIDATE.md").exists()
    # the stage comparison: the candidate stage is listed and a diff job runs in the candidate workspace
    st, _, body = _get(panel, "stages")
    t = body.decode()
    assert f"run:{run_id}:ADD-03" in t and "file/sources/candidate_pack/ADD-01_Addendum_No_1.pdf" in t
    st, h, _ = _post(panel, "stages/diff", {"frm": "ADD-02", "to": f"run:{run_id}:ADD-03"})
    assert st == 303
    j = _wait(panel, _job_id(h))
    assert j["exit_code"] == 0 and "candidate/build" in " ".join(j["argv"])
    st, _, body = _get(panel, f"jobs/{j['id']}")
    assert "What changed from ADD-02 to ADD-03" in body.decode()
    st, _, body = _get(panel, "units?doc=ADD-01")
    assert st == 200 and "ADD-01:cover/para1" in body.decode()
    assert tree_files(*REAL) == real_before                      # the real state untouched by everything above


def test_an_interrupted_run_is_resumed_from_the_panel(panel, full_run):
    st, h, body = _upload(panel, {"addendum": "ADD-03", "route": "recorded"}, "add03.pdf", PDF.read_bytes())
    assert st == 303, body[:400]
    run_id = _run_location(h)
    jid = _job_for_run(panel, run_id)
    t0 = time.time()
    while time.time() - t0 < 300:                                # kill the job's process mid-way (a crash)
        cp = _checkpoint(panel.cfg.staging, run_id)
        if cp and (cp["batches"].get("analysis-001") or {}).get("status") == "done":
            break
        assert _job(panel, jid)["status"] == "running", "the run ended before it could be interrupted"
        time.sleep(0.1)
    os.killpg(_job(panel, jid)["pid"], signal.SIGKILL)
    j = _wait(panel, jid, 60)
    assert j["status"] == "failed" and j["exit_code"] == -9
    cp = _checkpoint(panel.cfg.staging, run_id)
    assert cp["status"] == "running" and cp["steps"]["review"]["status"] != "done"
    st, _, body = _get(panel, f"runs/{run_id}")
    t = body.decode()
    assert "interrupted" in t and f"runs/{run_id}/resume" in t
    st, h, _ = _post(panel, f"runs/{run_id}/resume", {"from_step": ""})
    assert st == 303
    j2 = _wait(panel, _job_id(h))
    assert j2["kind"] == "ai-resume" and j2["argv"][3:6] == ["ai", "resume", run_id] and j2["exit_code"] == 0, j2
    cp = _checkpoint(panel.cfg.staging, run_id)
    assert cp["status"] == "partial" and cp["steps"]["review"]["status"] == "done"
    assert cp["batches"]["analysis-001"]["attempts"] == 1           # a done batch is never asked again
    assert any(e["event"] == "stale_run_lock_taken_over" for e in cp["events"])


# ---------------------------------------------------------------------------------------------- decisions

def test_the_decisions_form_refuses_without_a_name_and_a_reason_and_never_runs_on_its_own(panel, built_out,
                                                                                         monkeypatch):
    from tenderpack.panel import jobs as J
    jobs_dir = panel.cfg.panel_dir / "jobs"
    decision_jobs = lambda: [p for p in jobs_dir.iterdir() if "-decision-" in p.name]   # noqa: E731
    for page in ("", "stages", "addendum", "runs", "jobs", "decisions"):         # rendering pages starts nothing
        assert _get(panel, page)[0] == 200
    assert decision_jobs() == []
    st, _, body = _get(panel, "decisions")
    t = body.decode()
    assert "python -m tenderpack accept VOL-I-6.1-01 --reviewer" in t and "decisions/form?item=VOL-I-6.1-01" in t
    st, _, body = _get(panel, "decisions/form?item=VOL-I-6.1-01")
    t = body.decode()
    assert st == 200 and " checked" not in t and 'value="Your Name"' not in t
    assert re.search(r'name="name"[^>]*value=""|name="name"(?![^>]*value=)', t)
    base = {"item": "VOL-I-6.1-01", "decision": "accept", "name": "Ahmad", "reason": "checked against VOL-I 6.1"}
    for missing in ("name", "reason", "decision"):
        f = dict(base)
        f[missing] = "  "
        st, _, body = _post(panel, "decisions/confirm", f)
        assert st == 400 and b"refused" in body, missing
        st, _, body = _post(panel, "decisions/run", {**f, "confirm": "yes"})
        assert st == 400, missing
    st, _, body = _post(panel, "decisions/confirm", base)          # shows the exact command; runs nothing yet
    t = body.decode()
    assert st == 200 and "accept VOL-I-6.1-01 --reviewer Ahmad --note" in t and 'name="confirm"' in t
    assert " checked" not in t
    st, _, body = _post(panel, "decisions/run", base)                # no confirmation ticked
    assert st == 400 and b"confirm" in body
    assert decision_jobs() == []
    started = []

    class FakePopen:                                              # the engine command is captured, NOT executed here
        def __init__(self, argv, **kw):
            started.append(argv)
            self.pid, self.returncode = 999999, 0

        def wait(self, timeout=None):
            return 0

        def poll(self):
            return 0
    monkeypatch.setattr(J.subprocess, "Popen", FakePopen)
    st, h, _ = _post(panel, "decisions/run", {**base, "confirm": "yes"})
    assert st == 303 and len(started) == 1
    assert started[0] == [PY, "-m", "tenderpack", "accept", "VOL-I-6.1-01", "--reviewer", "Ahmad", "--note",
                          "checked against VOL-I 6.1", "--evidence", str(panel.cfg.evidence), "--pack",
                          str(panel.cfg.pack), "--decisions", str(panel.cfg.decisions)]
    st, _, _ = _post(panel, "decisions/run", {**base, "item": "--decisions=/etc/x", "confirm": "yes"})
    assert st == 400 and len(started) == 1                        # an option smuggled as an item is refused


# ---------------------------------------------------------------------------------------------- escaping

def test_model_produced_text_is_escaped_everywhere(panel):
    rd = panel.cfg.staging / "runs" / "ADD-09-run-recorded-x"
    (rd / "review").mkdir(parents=True)
    evil = '<script>alert(1)</script><img src=x onerror=alert(2)>'
    cp = {"format": 1, "run_id": rd.name, "addendum": "ADD-09", "settings": {"route": "recorded", "pdf": "/x.pdf"},
          "status": "failed", "status_reason": evil, "steps": {"ingest": {"status": "failed", "reason": evil}},
          "batches": {"analysis-001": {"status": "deferred", "failure_class": "rate_limit", "error": evil,
                                       "reset_in_s": 600}},
          "provisions": {"ADD-09:1.1": {"status": "pending", "history": []}}, "events": [],
          "completeness": {"status": "partial", "reasons": [evil]}, "approval": {"status": "none"}}
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    (rd / "review" / "index.md").write_text("## First: unresolved provisions and escalations\n\n- **ESCALATED** "
                                             + evil + "\n\n## Per provision\n", encoding="utf-8")
    for page in ("runs", f"runs/{rd.name}", f"runs/{rd.name}/candidate"):
        st, _, body = _get(panel, page)
        assert st == 200, page
        t = body.decode()
        assert "<script>" not in t and "<img src=x" not in t, page
        assert "&lt;script&gt;" in t or page.endswith("/candidate"), page   # shown, as text
    t = _get(panel, f"runs/{rd.name}")[2].decode()
    assert "rate limit" in t and "10 min" in t and "exit 5" in t


def test_the_cli_entry_point_lists_panel(tmp_path):
    res = subprocess.run([PY, "-m", "tenderpack", "panel", "--help"], cwd=ROOT, capture_output=True, text=True)
    assert res.returncode == 0 and "--port" in res.stdout and "--open" in res.stdout
    launch = (ROOT / "scripts/mac/launch.command").read_text(encoding="utf-8")
    assert "-m tenderpack panel --open" in launch


# ---------------------------------------------------------------------------------------------- follow-up: HOME

def test_home_lists_every_output_and_evidence_file_that_exists(panel, built_out):
    st, _, body = _get(panel)
    t = body.decode()
    assert st == 200
    top = t[:t.index("New addendum")]
    assert re.search(r"BASE\s*→\s*ADD-01.*→\s*ADD-02", top)              # the stage, in one line, at the top
    assert "205 of 205 register rows not accepted" in top and "37 of 37 amendment op(s) not accepted" in top
    listed = 0
    for area, base in (("out", panel.cfg.out), ("evidence-review", panel.cfg.evidence / "review")):
        for root, _, files in os.walk(base):
            for f in files:
                rel = (Path(root) / f).relative_to(base).as_posix()
                q = urllib.parse.quote(rel)                                   # hrefs are percent-encoded
                assert f"/t/{panel.token}/download/{area}/{q}\"" in t, (area, rel)      # every file that exists
                listed += 1
    assert listed > 100
    for g, words in (("A1 ", "a1.xlsx"), ("A2 ", "a2_cover_summary_check.csv"), ("A3 ", "a3_detail.html"),
                     ("A4 ", "clarification_register.md"), ("A5 ", "gantt.svg")):
        assert g in t and words in t, g
    full = t.index("Outputs in")                                      # the full listing (the deliverables strip above it
    a4 = t[t.index("A4 Clarification register and work log", full):t.index("A5 Bid programme", full)]
    assert f"/t/{panel.token}/file/worklog/README.md" in a4 and f"/t/{panel.token}/file/out/README.md" in a4
    assert _get(panel, "file/worklog/README.md")[0] == 200
    assert _get(panel, "file/worklog/../config/ai.yaml")[0] == 404
    assert f'href="/t/{panel.token}/file/out/a3/a3.pdf">a3.pdf</a>' in t   # the link is the file's name
    assert "WORKING DRAFT" in t and "validated through ADD-02" in t


def test_a_missing_out_shows_the_command_that_builds_it(pack, tmp_path):
    from tenderpack.panel.server import Panel, PanelConfig
    cfg = PanelConfig(root=ROOT, pack=ROOT / "config/pack.yaml", evidence=pack["out"], out=tmp_path / "no-out",
                      staging=tmp_path / "staging" / "ai", worklog=tmp_path / "wl", panel_dir=tmp_path / "panel")
    p = Panel(cfg, port=0, log=io.StringIO())
    p.start()
    try:
        t = _get(p)[2].decode()
    finally:
        p.stop()
    assert "No outputs yet" in t and "python -m tenderpack outputs" in t
    assert 'name="action" value="outputs"' in t                          # and the button that runs it
    assert "/file/out/" not in t
    assert "recorded" not in t[t.index("New addendum"):]                  # the test replay is never offered to the owner


def test_runs_and_jobs_pages_say_what_each_needs(panel, full_run):
    t = _get(panel, "runs")[2].decode()
    for s in ("Status", "Started", "Duration", "Base run", "What it needs from you"):
        assert s in t, s
    rows = re.findall(r'href="/t/[^/]+/runs/([^"/]+)"', t)
    created = [(_checkpoint(panel.cfg.staging, r) or {}).get("created") or "" for r in rows]
    assert created == sorted(created, reverse=True)                      # newest first
    t = _get(panel, "jobs")[2].decode()
    for s in ("Duration", "What it needs from you", "Command"):
        assert s in t, s


def test_the_token_appears_only_under_its_own_prefix_and_never_in_logs(panel, full_run):
    pages = ["", "stages", "addendum", "runs", "jobs", "decisions", f"runs/{full_run['job']['meta']['run_id']}",
             f"runs/{full_run['job']['meta']['run_id']}/candidate", f"jobs/{full_run['jid']}"]
    for page in pages:
        t = _get(panel, page)[2].decode()
        for url in re.findall(r'(?:href|action|src)="([^"]*)"', t):
            if panel.token in url:
                assert url.startswith(f"/t/{panel.token}/"), (page, url)
            assert not url.startswith(("http:", "https:", "//")), (page, url)
        assert t.count(panel.token) == len(re.findall(rf'="/t/{re.escape(panel.token)}/', t)), page
    log = panel.log.getvalue()
    assert "GET /t/<token>/" in log and panel.token not in log
    for p in panel.cfg.panel_dir.rglob("*"):                             # job records and logs: never the token
        if p.is_file() and p.suffix in (".json", ".log"):
            assert panel.token not in p.read_text(encoding="utf-8", errors="replace"), p


def test_the_stages_page_reads_the_candidate_where_the_checkpoint_records_it(panel, pack):
    """Coordinator, after W5 (consecutive addenda): the candidate workspace is read where the run's checkpoint records
    it (`candidate.build`, `candidate.pack`, `candidate.pdf_copy`), the way the engine reads it, not from a guessed
    layout. Here the record points to a folder that is not the default `candidate/`."""
    import shutil
    rd = panel.cfg.staging / "runs" / "ADD-07-run-recorded-layout"
    cand = rd / "cand-elsewhere"
    (cand / "build").mkdir(parents=True)
    (cand / "input").mkdir()
    shutil.copy(pack["out"] / "units.json", cand / "build" / "units.json")
    (cand / "input" / "ADD-07.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
    (cand / "pack.yaml").write_text((ROOT / "config/pack.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    cp = {"format": 1, "run_id": rd.name, "addendum": "ADD-07", "settings": {"route": "recorded"}, "status": "partial",
          "status_reason": "test layout", "created": "2000-01-01T00:00:00Z", "updated": "2000-01-01T00:01:00Z",
          "steps": {}, "batches": {}, "provisions": {}, "events": [],
          "candidate": {"dir": str(cand), "build": str(cand / "build"), "pack": str(cand / "pack.yaml"),
                        "pdf_copy": str(cand / "input" / "ADD-07.pdf")}}
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    t = _get(panel, "stages")[2].decode()
    assert f"run:{rd.name}:ADD-07" in t and f"units?doc=ADD-07&amp;run={rd.name}" in t
    u = _get(panel, f"units?doc=ADD-01&run={rd.name}")[2].decode()
    assert "ADD-01:cover/para1" in u                                     # read from the recorded build
    st, h, _ = _post(panel, "stages/diff", {"frm": "ADD-02", "to": f"run:{rd.name}:ADD-07"})
    assert st == 303
    j = _wait(panel, _job_id(h))
    assert j["argv"][j["argv"].index("--evidence") + 1] == str(cand / "build")
    assert j["argv"][j["argv"].index("--pack") + 1] == str(cand / "pack.yaml")
    shutil.rmtree(rd)


def test_home_puts_the_deliverables_first_with_open_and_download_links(panel, built_out):
    """The owner's ask: every necessary output easy to see. The first thing under the blockers is a Deliverables strip
    (A1-A5 and the review batches, the key file of each), then the new-addendum box, then the full listing."""
    st, _, body = _get(panel)
    t = body.decode()
    assert st == 200
    i = t.index("Deliverables")
    assert i < t.index("New addendum") < t.index("Outputs in")
    strip = t[i:t.index("New addendum")]
    for label, rel in (("A1 Compliance register", "a1/a1.xlsx"), ("A2 Amendment reconciliation", "a2/a2.md"),
                       ("A3 Bid-out consequences", "a3/a3.pdf"), ("A4 Clarification register and work log",
                                                                   "a4/clarification_register.md"),
                       ("A5 Bid programme", "a5/gantt.html"), ("Review batches", "review/index.html")):
        assert label in strip, label
        if (panel.cfg.out / rel).is_file():
            assert f"/t/{panel.token}/download/out/{rel}" in strip, rel          # every key file: download ...
            if not rel.endswith(".xlsx"):
                assert f"/t/{panel.token}/file/out/{rel}" in strip, rel          # ... and open, where a browser can
    assert f"/t/{panel.token}/file/worklog/README.md" in strip                    # A4 proper: the work log index
    assert "(missing)" not in strip or not (panel.cfg.out / "a5/gantt.html").is_file()


def test_the_run_page_offers_the_review_packet_first_when_the_run_is_finished(panel, full_run):
    """The owner's ask: follow the work easily. A finished run's page puts "Open the review packet" right under
    "What it needs from you", with the diff and a jump to the candidate outputs on the same page."""
    st, after = full_run["after"]
    assert st == 200
    needs_sec = after[after.index("What it needs from you"):after.index("<h2>Execution")]
    run_id = full_run["job"]["meta"]["run_id"]
    assert "Open the review packet" in needs_sec
    assert f"/t/{panel.token}/file/runs/{run_id}/review/index.html" in needs_sec
    assert 'href="#candidate"' in needs_sec and 'id="candidate"' in after
