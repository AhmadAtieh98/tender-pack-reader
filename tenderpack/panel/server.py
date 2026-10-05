"""The owner's local operating panel: `tenderpack panel [--port N] [--open]` (session 12, part 5).

A plain localhost page over the existing engine and workflow; A1-A5 under out/ remain the deliverables. Python's
standard library only (http.server, threading, subprocess): nothing to install on the Mac.

Access. The server binds 127.0.0.1 only (never another interface), on the port given or a free one, and every page
lives under /t/<token>/ where <token> is random per start and printed once on the terminal; a request without it, or
whose Host header is not 127.0.0.1/localhost on this port (DNS rebinding), is refused (403). The access log written to
the terminal never shows the token. Panel pages carry no script and load nothing external (CSP default-src 'none').

Files. /t/<token>/file/<area>/<path> opens and /t/<token>/download/<path> downloads (Content-Disposition) a file from
one of these areas only: out (the outputs), evidence-review (<evidence>/review: the image region renders), runs
(<staging>/runs/<run>/candidate/out, <run>/candidate/input and <run>/review only), jobs (<panel_dir>/jobs) and sources
(the repository's sources/). The path is checked part by part (no '', '.', '..', backslash or NUL), resolved, and must
stay inside its area after resolution, so a symlink out of the area (or of the repository) is refused. HTML from the
engine is served with a CSP that runs no script; a candidate's HTML and text get the CANDIDATE banner on top (the
download is the file exactly as written).

Actions. Every button starts a real job (tenderpack/panel/jobs.py): `<python> -m tenderpack ingest|outputs|outputs
--strict|check-register|diff|ai run|ai resume|accept|reject|approve ...` with the configured paths. Uploads (at most
50 MB, `%PDF-` magic) are stored as <panel_dir>/uploads/<sha256>.pdf; the sanitised original name is kept only in the
job record. A decision runs only from a form a person filled (decision chosen, name and reason typed, confirmation
ticked); the panel never pre-fills or pre-selects one. The panel writes only under <panel_dir> itself; out/ is written
only by the outputs job (which keeps the previous build on a structural failure, as the command always does),
candidate outputs stay in their run folders, rehearsals/ is never written. The panel reads no key and echoes no
environment variable; the jobs inherit the environment (the routes read their own keys) and their records hold the
argv only."""
from __future__ import annotations

import argparse
import email.parser
import email.policy
import hashlib
import hmac
import json
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
from collections import Counter
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ..util import ROOT
from . import views as V
from .jobs import JobError, Jobs

MAX_UPLOAD = 50 * 1024 * 1024
MAX_FORM = 256 * 1024
ADDENDUM = re.compile(r"^ADD-\d{2}$")
ITEM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/()+@-]{0,160}$")
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")
PANEL_CSP = ("default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; form-action 'self'; "
             "frame-ancestors 'none'; base-uri 'none'")
FILE_CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'self'; form-action 'none'"
TYPES = {".html": "text/html; charset=utf-8", ".htm": "text/html; charset=utf-8", ".md": "text/plain; charset=utf-8",
         ".txt": "text/plain; charset=utf-8", ".log": "text/plain; charset=utf-8", ".jsonl": "text/plain; charset=utf-8",
         ".csv": "text/plain; charset=utf-8", ".json": "application/json; charset=utf-8",
         ".yaml": "text/plain; charset=utf-8", ".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg",
         ".svg": "image/svg+xml",
         ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
RUN_SUBAREAS = (("candidate", "out"), ("candidate", "input"), ("review",))


@dataclass
class PanelConfig:
    """The paths the panel's jobs use. Every default is the repository's own; tests point them at tmp folders."""
    root: Path = ROOT
    pack: Path | None = None
    evidence: Path | None = None
    out: Path | None = None
    staging: Path | None = None                 # the AI staging folder (runs under <staging>/runs)
    worklog: Path | None = None
    panel_dir: Path | None = None
    ai_config: Path | None = None
    cassette: Path | None = None                # the recorded route's cassette (tests only)
    decisions: Path | None = None               # accept/reject --decisions (default: the pack's)
    approvals: Path | None = None               # approve --approvals (default: the pack's)
    python: str = field(default_factory=lambda: sys.executable)

    def __post_init__(self):
        r = Path(self.root).absolute()
        self.root = r
        defaults = {"pack": r / "config/pack.yaml", "evidence": r / "build", "out": r / "out",
                    "staging": r / "staging/ai", "worklog": r / "worklog/model_calls", "panel_dir": r / "staging/panel",
                    "ai_config": r / "config/ai.yaml"}
        self._default = {}
        for k, d in defaults.items():
            v = getattr(self, k)
            setattr(self, k, Path(v).absolute() if v else d)
            self._default[k] = getattr(self, k) == d
        for k in ("cassette", "decisions", "approvals"):
            if getattr(self, k):
                setattr(self, k, Path(getattr(self, k)).absolute())

    def flag(self, name: str, opt: str) -> list[str]:
        """`[opt, path]` when the path is not the command's own default (the command line stays the one to repeat)."""
        return [] if self._default.get(name) else [opt, str(getattr(self, name))]


# ---------------------------------------------------------------------------------------------- the panel

class Panel:
    def __init__(self, cfg: PanelConfig, port: int = 0, log=None):
        self.cfg = cfg
        self.log = log if log is not None else sys.stderr      # the access log (never the token)
        self.token = secrets.token_urlsafe(24)
        self.base = f"/t/{self.token}/"
        (cfg.panel_dir / "uploads").mkdir(parents=True, exist_ok=True)
        self.jobs = Jobs(cfg.root, cfg.panel_dir / "jobs", cfg.python)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", int(port)), _handler(self))
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}{self.base}"
        self._thread = None
        self._base_run = None
        self._routes = (0.0, None, None)

    def start(self) -> None:
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True, name="panel")
        self._thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()

    # ------------------------------------------------------------------ engine commands (argv after `-m tenderpack`)
    def cmd(self, action: str) -> list[str]:
        c = self.cfg
        if action == "ingest":
            return ["ingest", *c.flag("pack", "--pack"), *c.flag("evidence", "--out")]
        base = ["outputs", *c.flag("evidence", "--evidence"), *c.flag("out", "--out"), *c.flag("pack", "--pack")]
        if action == "outputs":
            return base
        if action == "strict":
            return base + ["--strict"]
        if action == "check-register":
            return ["check-register", *c.flag("evidence", "--evidence"), *c.flag("pack", "--pack")]
        raise JobError(f"unknown action {action!r}")

    def ai_common(self) -> list[str]:
        c = self.cfg
        return [*c.flag("evidence", "--evidence"), *c.flag("pack", "--pack"), *c.flag("ai_config", "--config"),
                *c.flag("staging", "--out"), *c.flag("worklog", "--worklog")]

    def decision_argv(self, it: dict, decision: str, name: str, reason: str) -> list[str]:
        c = self.cfg
        if decision == "approve":
            a = ["approve", it["id"], "--reviewer", name, "--notes", reason, "--pack", str(c.pack)]
            return a + (["--approvals", str(c.approvals)] if c.approvals else [])
        a = [decision, it["id"], "--reviewer", name, "--note", reason, "--evidence", str(c.evidence), "--pack",
             str(c.pack)]
        return a + (["--decisions", str(c.decisions)] if c.decisions else [])

    # ------------------------------------------------------------------ what the engine reports
    def routes(self) -> tuple[dict | None, str | None]:
        """`tenderpack ai routes --json` (read only: it checks the LOCAL Ollama endpoint, never a hosted one), kept for
        30 s so HOME stays quick."""
        t, val, err = self._routes
        if val is not None and time.time() - t < 30:
            return val, err
        val, err = self._routes_now()
        self._routes = (time.time(), val, err)
        return val, err

    def _routes_now(self) -> tuple[dict | None, str | None]:
        argv = [self.cfg.python, "-m", "tenderpack", "ai", "routes", "--json", *self.cfg.flag("ai_config", "--config")]
        try:
            res = subprocess.run(argv, cwd=self.cfg.root, capture_output=True, text=True, timeout=90,
                                 stdin=subprocess.DEVNULL)
            return json.loads(res.stdout), None
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            return None, f"{type(e).__name__}"

    def base_run_support(self) -> dict:
        """Whether this build's `ai run` has --base-run (read from its own --help), and the runs it could name."""
        if self._base_run is None:
            try:
                res = subprocess.run([self.cfg.python, "-m", "tenderpack", "ai", "run", "--help"], cwd=self.cfg.root,
                                     capture_output=True, text=True, timeout=90, stdin=subprocess.DEVNULL)
                self._base_run = "--base-run" in res.stdout
            except (OSError, subprocess.SubprocessError):
                self._base_run = False
        runs = [rid for rid, cp in V.candidate_runs(self.cfg.staging)
                if ((cp.get("steps") or {}).get("promotion") or {}).get("status") == "done"]
        return {"available": self._base_run, "runs": runs}

    def host_found(self) -> bool:
        """Whether the host route's command (config host_session.claude_bin, default `claude`) is on this machine."""
        import yaml
        try:
            hs = (yaml.safe_load(self.cfg.ai_config.read_text(encoding="utf-8")) or {}).get("host_session") or {}
        except (OSError, yaml.YAMLError):
            hs = {}
        return bool(shutil.which(str(hs.get("claude_bin") or "claude")))

    def addendum_box(self, advanced: bool = False) -> str:
        routes, err = self.routes()
        return V.addendum_box(self.base, routes, err, self.next_addendum(), self.host_found(), bool(self.cfg.cassette),
                              MAX_UPLOAD // (1024 * 1024), self.base_run_support() if advanced else None)

    def next_addendum(self) -> str:
        nums = [int(m.group(1)) for d in V.pack_docs(self.cfg.pack)
                if (m := re.match(r"^ADD-(\d{2})$", str(d.get("doc_id"))))]
        return f"ADD-{(max(nums) if nums else 0) + 1:02d}"

    def run_jobs(self) -> dict:
        out = {}
        for j in reversed(self.jobs.list()):
            rid = (j.get("meta") or {}).get("run_id")
            if rid:
                out.setdefault(rid, j)
        return out

    def running_runs(self) -> dict:
        return {(j.get("meta") or {}).get("run_id"): j for j in self.jobs.list()
                if j["status"] == "running" and (j.get("meta") or {}).get("run_id")}

    def running_for(self, rid: str) -> dict | None:
        for j in self.jobs.list():
            if (j.get("meta") or {}).get("run_id") == rid and j["status"] == "running":
                return j
        return None

    def pending_items(self) -> tuple[list[dict], Counter]:
        out = self.cfg.out
        items = (V.read_json(out / "review" / "items.json") or {}).get("items") or []
        done = ("accepted", "approved", "applied", "superseded", "rejected")
        pending = [{"kind": i.get("kind"), "id": i.get("id"), "status": i.get("status"), "prompt": i.get("decision")}
                   for i in items if i.get("kind") in ("row", "op", "reading") and i.get("status") not in done]
        decided = Counter((i.get("kind"), i.get("status")) for i in items if i.get("status") in done)
        a4 = V.read_json(out / "a4" / "clarification_register.json") or {}
        for r in a4.get("rows") or []:
            pending.append({"kind": "clarification", "id": r.get("id"), "status": r.get("response_status"),
                            "prompt": r.get("proposed_question") or r.get("gap")})
        import yaml
        try:
            pk = yaml.safe_load(self.cfg.pack.read_text(encoding="utf-8")) or {}
            ip = Path(pk.get("issues", "curation/register/issues.yaml"))
            ip = ip if ip.is_absolute() else self.cfg.root / ip
            files = [ip] + sorted((ip.parent / "issues").glob("*.yaml"))
            for f in files:
                for k, v in ((yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("issues") or {}).items():
                    pending.append({"kind": "issue", "id": k, "status": (v or {}).get("status") or "open",
                                    "prompt": (v or {}).get("short") or (v or {}).get("text")})
        except (OSError, ValueError, yaml.YAMLError, AttributeError):
            pass
        return [p for p in pending if p.get("id")], decided

    def latest_decisions(self) -> dict:
        import yaml
        p = self.cfg.decisions
        if p is None:
            try:
                pk = yaml.safe_load(self.cfg.pack.read_text(encoding="utf-8")) or {}
                p = Path(pk.get("decisions", "curation/reviews/decisions.yaml"))
                p = p if p.is_absolute() else self.cfg.root / p
            except (OSError, yaml.YAMLError):
                return {}
        try:
            data = yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            return {}
        out = {}
        for d in (data.get("decisions") if isinstance(data, dict) else data) or []:
            if isinstance(d, dict) and d.get("item"):
                out[d["item"]] = d
        return out

    def find_item(self, item: str) -> dict | None:
        if not ITEM.match(item or ""):
            return None
        for it in self.pending_items()[0]:
            if it["id"] == item:
                return it
        return None

    # ------------------------------------------------------------------ files
    def areas(self) -> dict:
        c = self.cfg
        return {"out": c.out, "evidence-review": c.evidence / "review", "runs": c.staging / "runs",
                "jobs": c.panel_dir / "jobs", "sources": c.root / "sources", "worklog": c.root / "worklog"}

    def safe_file(self, area: str, rel: str) -> Path | None:
        base = self.areas().get(area)
        if base is None or not rel or "\x00" in rel or "\\" in rel:
            return None
        parts = rel.split("/")
        if any(p in ("", ".", "..") for p in parts):
            return None
        if area == "worklog" and (len(parts) != 1 or not parts[0].endswith(".md")):
            return None                                       # the work log's top-level records only
        allowed = None
        if area == "runs":                                    # only a run's candidate outputs, input and review
            if not RUN_ID.match(parts[0]) or len(parts) < 2:
                return None
            rd = base / parts[0]
            cp = V.read_json(rd / "checkpoint.json")
            cand = V.cand_paths(rd, cp if isinstance(cp, dict) else {})
            allowed = [rd / "review", Path(cand["out"]), Path(cand["dir"]) / "input"] + \
                [rd.joinpath(*s) for s in RUN_SUBAREAS]
        try:
            real_base = base.resolve()
            target = base.joinpath(*parts).resolve()
            if allowed is not None:
                real_base = (base / parts[0]).resolve()
                if not any(target.is_relative_to(a.resolve()) for a in allowed):
                    return None
        except (OSError, RuntimeError):
            return None
        if not target.is_relative_to(real_base) or not target.is_file():
            return None
        return target


# ---------------------------------------------------------------------------------------------- the handler

def _clean_name(name: str) -> str:
    base = Path(str(name or "").replace("\\", "/")).name
    return (re.sub(r"[^A-Za-z0-9._ -]", "", base).strip()[:100]) or "upload.pdf"


def _rehearsal_match(root: Path, sha: str) -> str:
    for p in sorted((root / "rehearsals").glob("*/input/*.pdf")):
        try:
            if hashlib.sha256(p.read_bytes()).hexdigest() == sha:
                return p.relative_to(root).as_posix()
        except OSError:
            continue
    return ""


def _handler(panel: Panel):
    class H(BaseHTTPRequestHandler):
        server_version = "tenderpack-panel"
        sys_version = ""
        protocol_version = "HTTP/1.1"

        # ---- plumbing
        def log_message(self, fmt, *args):                    # never the token
            msg = (fmt % args).replace(panel.token, "<token>")
            panel.log.write(f"panel: {msg}\n")
            panel.log.flush()

        def _send(self, status: int, body: bytes, ctype: str = "text/html; charset=utf-8", headers: dict | None = None,
                  csp: str = PANEL_CSP):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", csp)
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _html(self, status: int, text: str):
            self._send(status, text.encode("utf-8"))

        def _refuse(self, status: int, text: str):
            self.close_connection = True
            self._html(status, V.message(panel.base if status != 403 else "/", "Refused", text))

        def _redirect(self, path: str):
            self._send(303, b"", headers={"Location": panel.base + path})

        def _authorised(self) -> str | None:
            """The sub-path after /t/<token>/, or None (refused)."""
            host = (self.headers.get("Host") or "").strip().lower()
            if host not in (f"127.0.0.1:{panel.port}", f"localhost:{panel.port}"):
                return None
            path = urllib.parse.urlsplit(self.path).path
            m = re.match(r"^/t/([^/]+)(/.*)?$", path)
            if not m or not hmac.compare_digest(m.group(1).encode(), panel.token.encode()):
                return None
            return (m.group(2) or "/")[1:]

        def _query(self) -> dict:
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query, keep_blank_values=True)
            return {k: v[0] for k, v in q.items()}

        def _form(self) -> dict | None:
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_FORM:
                return None
            data = self.rfile.read(n).decode("utf-8", "replace") if n else ""
            return {k: v[0] for k, v in urllib.parse.parse_qs(data, keep_blank_values=True).items()}

        # ---- verbs
        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            sub = self._authorised()
            if sub is None:
                return self._refuse(403, "refused: open the address the panel printed when it started "
                                         "(http://127.0.0.1:<port>/t/<token>/)")
            try:
                self._get(sub)
            except BrokenPipeError:
                pass

        def do_POST(self):
            sub = self._authorised()
            if sub is None:
                return self._refuse(403, "refused: open the address the panel printed when it started")
            try:
                self._post(sub)
            except JobError as e:
                self._html(409, V.message(panel.base, "Not started", str(e)))
            except BrokenPipeError:
                pass

        # ---- GET routes
        def _get(self, sub: str):
            base, cfg = panel.base, panel.cfg
            raw = urllib.parse.unquote(sub)
            if sub.startswith(("file/", "download/")):
                return self._file(sub)
            if raw == "":
                return self._html(200, V.home(base, cfg, panel.jobs.list(), panel.addendum_box()))
            if raw == "stages":
                q = self._query()
                return self._html(200, V.stages_page(base, cfg, V.candidate_runs(cfg.staging),
                                                     {"frm": q.get("frm"), "to": q.get("to")}))
            if raw == "units":
                return self._units(self._query())
            if raw == "addendum":
                return self._html(200, V.addendum_page(base, panel.addendum_box(advanced=True), panel.routes()[0]))
            if raw == "runs":
                return self._html(200, V.runs_page(base, V.candidate_runs(cfg.staging), cfg.staging,
                                                   panel.run_jobs(), panel.running_runs()))
            m = re.match(r"^runs/([^/]+)(/candidate)?$", raw)
            if m:
                rid = m.group(1)
                rd = cfg.staging / "runs" / rid
                cp = V.read_json(rd / "checkpoint.json") if RUN_ID.match(rid) else None
                if not isinstance(cp, dict):
                    j = panel.run_jobs().get(rid) if RUN_ID.match(rid) else None
                    if j and not m.group(2):                  # just started: no checkpoint yet
                        return self._html(200, V.starting_page(base, rid, j))
                    return self._refuse(404, f"no run {rid}")
                if m.group(2):
                    return self._html(200, V.candidate_page(base, rid, rd, cp))
                from ..ai.checkpoint import STEPS
                return self._html(200, V.run_detail(base, rid, rd, cp, panel.run_jobs().get(rid),
                                                    panel.running_for(rid), tuple(STEPS),
                                                    V.candidate_outputs(base, rid, rd, cp)))
            if raw == "jobs":
                return self._html(200, V.jobs_page(base, panel.jobs.list()))
            m = re.match(r"^jobs/([^/]+)$", raw)
            if m:
                j = panel.jobs.get(m.group(1))
                if not j:
                    return self._refuse(404, "no such job")
                log, cut = panel.jobs.log_text(j)
                return self._html(200, V.job_page(base, j, log, cut))
            if raw == "decisions":
                pending, decided = panel.pending_items()
                return self._html(200, V.decisions_page(base, pending, decided, panel.latest_decisions()))
            if raw == "decisions/form":
                it = panel.find_item(self._query().get("item", ""))
                if not it:
                    return self._refuse(404, "no such pending item")
                return self._html(200, V.decision_form(base, it))
            return self._refuse(404, "no such page")

        def _units(self, q: dict):
            cfg, base = panel.cfg, panel.base
            doc, rid = q.get("doc", ""), q.get("run", "")
            if not re.match(r"^[A-Z0-9-]{2,12}$", doc) or (rid and not RUN_ID.match(rid)):
                return self._refuse(400, "refused: bad document or run")
            cand = None
            if rid:
                rd = cfg.staging / "runs" / rid
                cp = V.read_json(rd / "checkpoint.json")
                cand = V.cand_paths(rd, cp if isinstance(cp, dict) else {})
            build = Path(cand["build"]) if cand else cfg.evidence
            units = [u for u in (V.read_json(build / "units.json") or {}).get("units") or [] if u.get("doc") == doc]
            pdf = None
            if rid:
                if doc == (cp or {}).get("addendum"):
                    pdf = V.run_file_href(base, rid, rd, cand["pdf"])
            if not rid or pdf is None:
                d = next((d for d in V.pack_docs(cfg.pack) if d.get("doc_id") == doc), None)
                if d and str(d.get("path", "")).startswith("sources/"):
                    pdf = f"{base}file/sources/{urllib.parse.quote(str(d['path'])[len('sources/'):])}"
            return self._html(200, V.units_page(base, doc, units, pdf, rid or None))

        def _file(self, sub: str):
            kind, _, rest = sub.partition("/")
            area, _, rel = rest.partition("/")
            rel = urllib.parse.unquote(rel)
            p = panel.safe_file(area, rel)
            if p is None:
                return self._refuse(404, "refused: not a file this panel serves (out/, the evidence build's review "
                                         "renders, a run's candidate outputs, input and review, the panel's jobs, "
                                         "sources/)")
            data = p.read_bytes()
            ctype = TYPES.get(p.suffix.lower(), "application/octet-stream")
            fname = urllib.parse.quote(p.name)
            if kind == "download" or ctype == "application/octet-stream" or ctype.startswith(TYPES[".xlsx"]):
                return self._send(200, data, ctype, {"Content-Disposition": f"attachment; filename*=UTF-8''{fname}"},
                                  csp=FILE_CSP)
            if area == "runs":                                  # a candidate's file: the panel's banner on top
                if ctype.startswith("text/html"):
                    data = _inject_banner(data)
                elif ctype.startswith(("text/plain", "application/json")):
                    data = f"{V.CANDIDATE_BANNER}\n\n".encode() + data
                    ctype = "text/plain; charset=utf-8"
            return self._send(200, data, ctype, {"Content-Disposition": f"inline; filename*=UTF-8''{fname}"},
                              csp=FILE_CSP)

        # ---- POST routes
        def _post(self, sub: str):
            raw = urllib.parse.unquote(sub)
            if raw == "addendum/start":
                return self._upload()
            f = self._form()
            if f is None:
                return self._refuse(413, "refused: the form is too large")
            if raw == "jobs/start":
                a = f.get("action", "")
                if a not in ("ingest", "outputs", "strict", "check-register"):
                    return self._refuse(400, "refused: unknown action")
                j = panel.jobs.start(a, panel.cmd(a))
                return self._redirect(f"jobs/{j['id']}")
            m = re.match(r"^jobs/([^/]+)/stop$", raw)
            if m:
                j = panel.jobs.stop(m.group(1))
                return self._redirect(f"jobs/{j['id']}")
            if raw == "stages/diff":
                return self._diff(f)
            m = re.match(r"^runs/([^/]+)/resume$", raw)
            if m:
                rid = m.group(1)
                if not RUN_ID.match(rid) or not (panel.cfg.staging / "runs" / rid / "checkpoint.json").is_file():
                    return self._refuse(404, "no such run")
                frm = f.get("from_step", "")
                from ..ai.checkpoint import STEPS
                if frm and frm not in STEPS:
                    return self._refuse(400, "refused: unknown step")
                args = ["ai", "resume", rid, *(["--from", frm] if frm else []), *panel.cfg.flag("staging", "--out"),
                        *panel.cfg.flag("worklog", "--worklog")]
                j = panel.jobs.start("ai-resume", args, {"run_id": rid})
                return self._redirect(f"jobs/{j['id']}")
            if raw in ("decisions/confirm", "decisions/run"):
                return self._decision(f, run=(raw == "decisions/run"))
            return self._refuse(404, "no such action")

        def _diff(self, f: dict):
            cfg = panel.cfg
            frm, to = f.get("frm", ""), f.get("to", "")
            runs, stages = set(), []
            for s in (frm, to):
                m = re.match(r"^run:([^:]+):(ADD-\d{2})$", s)
                if m:
                    runs.add(m.group(1))
                    stages.append(m.group(2))
                elif re.match(r"^(BASE|ADD-\d{2})$", s):
                    stages.append(s)
                else:
                    return self._refuse(400, "refused: choose two stages")
            if len(runs) > 1:
                return self._refuse(400, "refused: two different candidate runs cannot be compared in one diff")
            if stages[0] == stages[1]:
                return self._refuse(400, "refused: choose two different stages")
            if runs:
                rid = runs.pop()
                if not RUN_ID.match(rid):
                    return self._refuse(400, "refused: bad run id")
                rd = cfg.staging / "runs" / rid
                cp = V.read_json(rd / "checkpoint.json")
                cand = V.cand_paths(rd, cp if isinstance(cp, dict) else {})   # where the checkpoint records it
                if not (Path(cand["build"]) / "units.json").is_file():
                    return self._refuse(404, "that run has no candidate build yet")
                args = ["diff", "--from", stages[0], "--to", stages[1], "--evidence", str(cand["build"]), "--pack",
                        str(cand["pack"])]
                meta = {"run_id": rid}
            else:
                args = ["diff", "--from", stages[0], "--to", stages[1], *cfg.flag("evidence", "--evidence"),
                        *cfg.flag("pack", "--pack")]
                meta = {}
            j = panel.jobs.start("diff", args, meta)
            return self._redirect(f"jobs/{j['id']}")

        def _upload(self):
            cfg = panel.cfg
            ctype = self.headers.get("Content-Type") or ""
            try:
                n = int(self.headers.get("Content-Length") or -1)
            except ValueError:
                n = -1
            if n < 0:
                return self._refuse(411, "refused: no Content-Length")
            if n > MAX_UPLOAD + MAX_FORM:
                return self._refuse(413, f"refused: the upload is larger than {MAX_UPLOAD // (1024 * 1024)} MB")
            if not ctype.lower().startswith("multipart/form-data"):
                return self._refuse(400, "refused: expected a form upload")
            body = self.rfile.read(n)
            msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
                b"Content-Type: " + ctype.encode("latin-1", "replace") + b"\r\nMIME-Version: 1.0\r\n\r\n" + body)
            fields, pdf, name = {}, None, ""
            for part in msg.iter_parts() if msg.is_multipart() else []:
                key = part.get_param("name", header="content-disposition")
                payload = part.get_payload(decode=True) or b""
                if key == "pdf":
                    pdf, name = payload, part.get_filename() or ""
                elif key:
                    fields[key] = payload.decode("utf-8", "replace").strip()
            errors = []
            add = fields.get("addendum", "")
            if not ADDENDUM.match(add):
                errors.append("the addendum id must look like ADD-NN (e.g. ADD-03)")
            route = fields.get("route", "")
            allowed = ["host", "ollama"] + (["recorded"] if cfg.cassette else [])
            if route not in allowed:
                errors.append(f"choose a route the panel offers ({', '.join(allowed)})")
            offline = fields.get("offline") == "yes"
            if offline and route == "host":
                errors.append("offline mode allows only the local ollama route (host is refused)")
            model = fields.get("model", "")
            if model and (route != "ollama" or not re.match(r"^[A-Za-z0-9._:/-]{1,120}$", model)):
                errors.append("a model is chosen only for the ollama route, from the models it lists as usable")
            base_run = fields.get("base_run", "")
            if base_run:
                sup = panel.base_run_support()
                if not sup["available"]:
                    errors.append("--base-run is not in this build")
                elif base_run not in sup["runs"]:
                    errors.append("--base-run must name a run whose promotion is done")
            if not pdf:
                errors.append("no PDF was uploaded")
            elif len(pdf) > MAX_UPLOAD:
                errors.append(f"the PDF is larger than {MAX_UPLOAD // (1024 * 1024)} MB")
            elif not pdf.startswith(b"%PDF-"):
                errors.append("the file is not a PDF (it does not start with %PDF-)")
            if errors:
                return self._html(400, V.page(panel.base, "Not started", "<ul>" + "".join(
                    f'<li class="bad">refused: {V.esc(e)}</li>' for e in errors) + "</ul>"))
            if model and route == "ollama":
                routes, _ = panel.routes()
                ok = {m.get("id") for r in (routes or {}).get("routes") or [] if r.get("route") == "ollama"
                      for m in r.get("models") or [] if m.get("ok")}
                if model not in ok:
                    return self._html(400, V.message(panel.base, "Not started",
                                                     "refused: that model is not usable on the ollama route now"))
            sha = hashlib.sha256(pdf).hexdigest()
            dest = cfg.panel_dir / "uploads" / f"{sha}.pdf"
            if not dest.exists():
                tmp = dest.with_name(f".{sha}.{secrets.token_hex(4)}.tmp")
                tmp.write_bytes(pdf)
                os.replace(tmp, dest)
            from ..ai.workflow import new_run_id
            rid = new_run_id(add, route)
            args = ["ai", "run", add, "--pdf", str(dest), "--route", route, "--run-id", rid, *panel.ai_common()]
            if offline:
                args.append("--offline")
            if model:
                args += ["--model", model]
            if route == "recorded":
                args += ["--cassette", str(cfg.cassette)]
            if base_run:
                args += ["--base-run", base_run]
            meta = {"run_id": rid, "upload_sha256": sha, "original_name": _clean_name(name), "bytes": len(pdf)}
            syn = _rehearsal_match(cfg.root, sha)
            if syn:
                meta["synthetic"] = syn
            panel.jobs.start("ai-run", args, meta)
            return self._redirect(f"runs/{rid}")                # the run's page follows it

        def _decision(self, f: dict, run: bool):
            item_id = f.get("item", "")
            it = panel.find_item(item_id)
            if not it:
                return self._refuse(400, "refused: no such pending item")
            decision = (f.get("decision") or "").strip()
            name = " ".join((f.get("name") or "").split())
            reason = (f.get("reason") or "").strip()
            errors = []
            allowed = ("approve",) if it["kind"] == "reading" else ("accept", "reject")
            if decision not in allowed:
                errors.append(f"choose the decision yourself ({' or '.join(allowed)}); none is chosen for you")
            if not name or len(name) > 100:
                errors.append("type your name (the person deciding)")
            if not reason or len(reason) > 2000:
                errors.append("type the reason for the decision")
            if errors:
                return self._html(400, V.decision_form(panel.base, it, errors,
                                                       {"decision": decision, "name": name, "reason": reason}))
            argv = panel.decision_argv(it, decision, name, reason)
            if not run:
                shown = shlex.join([panel.cfg.python, "-m", "tenderpack", *argv])
                return self._html(200, V.decision_confirm(panel.base, it, decision, name, reason, shown))
            if f.get("confirm") != "yes":
                return self._html(400, V.message(panel.base, "Not run", "refused: tick the confirmation that you "
                                                                        "make this decision; nothing was run"))
            j = panel.jobs.start("decision", argv, {"item": it["id"], "decision": decision, "reviewer": name})
            return self._redirect(f"jobs/{j['id']}")

    return H


def _inject_banner(data: bytes) -> bytes:
    banner = (f'<div style="border:2px solid #b60;background:#fff3e0;padding:8px;font-weight:bold;'
              f'font-family:system-ui,sans-serif">{V.CANDIDATE_BANNER}</div>').encode()
    m = re.search(rb"<body[^>]*>", data, re.I)
    return data[:m.end()] + banner + data[m.end():] if m else banner + data


# ---------------------------------------------------------------------------------------------- the command

def add_parser(sub) -> None:
    p = sub.add_parser("panel", help="the owner's local operating panel (127.0.0.1 only; a token per start)")
    p.add_argument("--port", type=int, default=0, help="the port (default: a free one)")
    p.add_argument("--open", action="store_true", help="open the panel in the default browser")
    p.add_argument("--pack", help="the pack configuration (default config/pack.yaml)")
    p.add_argument("--evidence", help="the evidence build (default build/)")
    p.add_argument("--out", help="the outputs folder (default out/)")
    p.add_argument("--staging", help="the AI staging folder (default staging/ai)")
    p.add_argument("--worklog", help="the AI work log folder (default worklog/model_calls)")
    p.add_argument("--panel-dir", help="the panel's jobs and uploads (default staging/panel)")


def main(a) -> int:
    cfg = PanelConfig(pack=a.pack, evidence=a.evidence, out=a.out, staging=a.staging, worklog=a.worklog,
                      panel_dir=a.panel_dir)
    try:
        p = Panel(cfg, a.port)
    except OSError as e:
        print(f"REFUSED: cannot listen on 127.0.0.1:{a.port}: {e}")
        return 2
    print(f"tenderpack: operating panel at {p.url}\n  (127.0.0.1 only; this address works while this process runs; "
          f"jobs and uploads under {cfg.panel_dir}; Ctrl-C stops the panel, not the jobs)", flush=True)
    if a.open:
        import webbrowser
        webbrowser.open(p.url)
    try:
        p.httpd.serve_forever()
    except KeyboardInterrupt:
        print("\npanel stopped")
    finally:
        p.httpd.server_close()
    return 0
