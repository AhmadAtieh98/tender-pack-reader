"""The panel's pages (session 12, part 5): plain HTML built from the engine's own records, every value escaped.

What a page shows comes from files the engine wrote (out/stages.json, out/checks.json, out/review/items.json, the A4
register, a run's checkpoint.json and review packet) or from a job's own output; the panel computes no status of its
own beyond reading them. Four records are kept apart on every page that has them:
  execution              did the command or the run's steps run, and how did they end (exit codes, steps, batches);
  completeness           what is accounted for and what is not (provisions, downstream tasks, coverage checks);
  structural validation  the engine's structural checks (E01, C16, ...; a candidate's own checks);
  human approval         what a named person decided; everything else is PROPOSED / HUMAN DECISION PENDING.
Model-produced text (a run's reasons, errors, review sections) is untrusted: html.escape everywhere, never markup.

The outputs are listed from the files that exist (os.walk), grouped A1-A5 by folder, never from a fixed list; a
missing key file is named with the command that builds it. A candidate's outputs use the same listing. A run's
candidate workspace is read where its checkpoint records it (`candidate`), as the engine reads it."""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import shlex
import socket
import urllib.parse
from collections import Counter
from pathlib import Path

from .jobs import AI_EXIT, meaning

TITLE = "tenderpack: operating panel"
CANDIDATE_BANNER = "CANDIDATE, not approved; the validated outputs are under out/"
DEMO_CANDIDATE_BANNER = "INTERVIEW DEMO — approvals are simulated and remain editable; unresolved evidence stays unresolved. Not a tender release."
NOTHING_ACCEPTED = "Nothing is accepted; decisions are recorded with tenderpack accept/reject."
CSS = ("body{font-family:system-ui,sans-serif;margin:12px auto;max-width:1200px;padding:0 14px;color:#111;"
       "background:#fff;line-height:1.4;font-size:15px}nav{padding:6px 0;border-bottom:1px solid #ccc}"
       "nav a{margin-right:16px;font-weight:600}h1{font-size:22px;margin:12px 0 6px}h2{font-size:18px;margin:22px 0 "
       "6px;border-bottom:1px solid #ccc}h3{font-size:15px;margin:14px 0 4px}table{border-collapse:collapse;margin:6px "
       "0;max-width:100%}td,th{border:1px solid #ccc;padding:3px 6px;font-size:13px;vertical-align:top;text-align:left;"
       "overflow-wrap:anywhere}th{background:#f3f3f3}pre,code{background:#f4f4f4;white-space:pre-wrap;"
       "overflow-wrap:anywhere}pre{padding:6px;font-size:12px;max-height:520px;overflow:auto}.banner{border:2px solid "
       "#b60;background:#fff3e0;padding:8px;font-weight:bold}.box{border:2px solid #357;background:#f2f6fb;padding:"
       "8px 14px;margin:12px 0}.box h2{border:0;margin-top:4px}.line{margin:3px 0}.note{color:#444;font-size:13px}"
       ".bad{color:#a00}.ok{color:#060}.lead{font-size:17px;font-weight:600}form.inline{display:inline}"
       "label{margin-right:12px}fieldset{border:1px solid #ccc;margin:6px 0}details{margin:4px 0}"
       "summary{cursor:pointer}.group{margin:10px 0 16px}.grouphead{font-weight:600;font-size:16px}"
       ".scroll{overflow-x:auto}")
# the folders of out/ as groups (a folder not named here is still listed, under "Other files")
# Session 13 (the owner: "the work log is A4"): A4 is the work log (the repository history, the prompts and model
# calls, the note of every error), under worklog/; out/a4 holds the clarification register, a supporting record.
A4_LABEL = "A4 Work log (the repository history, prompts, model calls, errors)"
REGISTER_LABEL = "Clarification register (supporting record, drafts not sent)"
CSS += ("th{white-space:nowrap}button{font:inherit;font-size:14px;padding:5px 12px;cursor:pointer}"
        ".box button,.primary{background:#246;color:#fff;border:1px solid #135;border-radius:4px;font-weight:600;"
        "text-decoration:none;padding:6px 14px}.deliv{border:2px solid #286;background:#f1faf4;padding:8px 14px;"
        "margin:12px 0}.deliv h2{border:0;margin-top:4px}.deliv .line{margin:5px 0;font-size:15px}.nw{white-space:nowrap}")
GROUPS = (
    ("a1", "A1 Compliance register", "every requirement, with its source, consequence and owner"),
    ("a2", "A2 Amendment reconciliation", "what each addendum changed, and the C28 check of each cover summary "
                                          "against its provisions"),
    ("a3", "A3 Bid-out consequences", "the one-page sheet of what puts the bid out, and its detail page"),
    ("_a4", A4_LABEL, ""),           # session 13: A4 is the work log (worklog/; not a folder of out/), linked here
    ("a4", REGISTER_LABEL, "draft questions to the Authority (NOT SENT): a supporting record of what the system "
                           "could not resolve, cited by A2 and A4; it is not the A4 deliverable"),
    ("a5", "A5 Bid programme", "the Gantt chart, programme, marshalling, documents, resources, drivers, replan deltas "
                               "and scenarios"),
    ("review", "Review batches (your decisions)", "the items waiting for a person's decision, in the order to review "
                                                  "them; start with index.html"),
    ("", "About these outputs", "the outputs README, the checks and the stages"),
)
KEY_FILES = {"a1": ("a1.xlsx",), "a2": ("a2.md",), "a3": ("a3.pdf",), "a4": ("clarification_register.md",),
             "a5": ("gantt.pdf", "programme.csv"), "review": ("index.html",)}
DESCRIBE = {"a1.xlsx": "the register (spreadsheet)", "a1.csv": "the register (CSV)", "a1.json": "the register (data)",
            "a2.md": "the reconciliation (read this)", "a2_cover_summary_check.csv": "C28: cover summary vs provisions",
            "a3.pdf": "the one-page sheet", "a3_detail.html": "the detail behind each line",
            "clarification_register.md": "draft questions (read this)", "gantt.pdf": "the Gantt chart (PDF)",
            "gantt.html": "the Gantt chart (browser)", "gantt.svg": "the Gantt chart (image)",
            "programme.csv": "the programme activities", "README.md": "how to read these files",
            "index.html": "start here", "checks.json": "every check and its result", "stages.json": "the stages applied",
            "requirements_not_carried.csv": "A1 rows the programme does not carry, with the reason",
            "marshalling.csv": "the marshalling plan", "documents.csv": "the bid documents",
            "resources.csv": "resources", "drivers.csv": "what drives the dates", "replan_deltas.csv": "what moved",
            "packet.html": "the evidence packet (crops beside the reading)", "CANDIDATE.md": "what this candidate is",
            "diff.md": "what changed (the diff)", "index.md": "the review packet as text"}
VIEWABLE = (".html", ".htm", ".md", ".csv", ".txt", ".pdf", ".svg", ".png", ".jpg", ".json", ".log")
STEP_WORDS = {"done": "done", "running": "running", "pending": "pending", "failed": "FAILED", "stopped": "stopped",
              "skipped": "skipped"}


def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def read_json(p: Path):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def page(base: str, heading: str, body: str, refresh: int | None = None) -> str:
    nav = " ".join(f'<a href="{base}{p}">{n}</a>' for p, n in (("", "Home: outputs and new addendum"),
                                                                ("runs", "Runs"), ("jobs", "Jobs"),
                                                                ("stages", "Stages and sources"),
                                                                ("decisions", "Decisions"),
                                                                ("interview", "All demo decisions"),
                                                                ("quickreview", "Quick reviews")))
    meta = f'<meta http-equiv="refresh" content="{int(refresh)}">' if refresh else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width, initial-scale=1">{meta}<title>{TITLE}</title><style>{CSS}</style></head>'
            f"<body><nav>{nav}</nav><h1>{esc(heading)}</h1>{body}</body></html>")


def table(head: list[str], rows: list[list[str]]) -> str:
    """`rows` cells are HTML already (callers escape)."""
    if not rows:
        return '<p class="note">none</p>'
    h = "".join(f"<th>{esc(x)}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table><tr>{h}</tr>{b}</table></div>'


def button(base: str, action: str, label: str, fields: dict | None = None) -> str:
    hidden = "".join(f'<input type="hidden" name="{esc(k)}" value="{esc(v)}">' for k, v in (fields or {}).items())
    return f'<form class="inline" method="post" action="{base}{action}">{hidden}<button>{esc(label)}</button></form>'


def _ts(t: float) -> str:
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _size(n: int) -> str:
    return f"{n / 1048576:.1f} MB" if n >= 1048576 else f"{max(1, round(n / 1024))} KB"


def _okcell(ok, text: str | None = None) -> str:
    if ok is None:
        return esc(text or "")
    return f'<span class="{"ok" if ok else "bad"}">{text or ("ok" if ok else "NOT OK")}</span>'


def _short(x, n: int) -> str:
    s = "" if x is None else str(x)
    return s if len(s) <= n else s[: n - 1] + "…"


def _read(p: Path) -> str:
    try:
        return Path(p).read_text(encoding="utf-8")
    except OSError:
        return ""


def _section(md: str, heading: str) -> str:
    i = md.find(heading)
    if i < 0:
        return ""
    j = md.find("\n## ", i + len(heading))
    return md[i: j if j > 0 else len(md)].strip()


# ---------------------------------------------------------------------------------------------- the file listing

def walk(root: Path) -> list[tuple[str, os.stat_result]]:
    """Every file under `root` (relative POSIX path, stat), sorted; symlinks are not followed."""
    out = []
    root = Path(root)
    if not root.is_dir():
        return out
    for d, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = Path(d) / f
            if p.is_symlink():
                continue
            try:
                st = p.stat()
            except OSError:
                continue
            out.append((p.relative_to(root).as_posix(), st))
    return out


def file_row(base: str, area: str, rel: str, st, name: str | None = None) -> list[str]:
    q = esc(urllib.parse.quote(rel))
    fname = name or rel.rsplit("/", 1)[-1]
    is_view = Path(rel).suffix.lower() in VIEWABLE
    label = f'<a href="{base}file/{area}/{q}">{esc(fname)}</a>'
    links = (f'<a href="{base}file/{area}/{q}">open</a> · ' if is_view else "") + \
        f'<a href="{base}download/{area}/{q}">download</a>'
    return [label, esc(DESCRIBE.get(fname.rsplit("/", 1)[-1], "")), esc(_size(st.st_size)), esc(_ts(st.st_mtime)),
            links]


FILE_HEAD = ["File", "What it is", "Size", "Built (modified)", "Open / download"]


def _group_of(rel: str) -> str:
    return rel.split("/", 1)[0] if "/" in rel else ""


def listing(base: str, area: str, root: Path, state: str, extra: dict | None = None) -> str:
    """The outputs under `root` grouped A1-A5 (then review, then the top-level files, then any other folder), one
    line per group (what it is, its state, when it was built), one row per file. Sub-folders fold away."""
    files = walk(root)
    by: dict[str, list] = {}
    for rel, st in files:
        by.setdefault(_group_of(rel), []).append((rel, st))
    known = [g[0] for g in GROUPS]
    order = list(GROUPS) + [(k, f"Other files: {k}/", "files in a folder this panel has no description for")
                            for k in sorted(by) if k not in known]
    L = []
    for key, heading, what in order:
        items = by.get(key, [])
        more = (extra or {}).get(key, "")
        if key.startswith("_"):                          # not a folder of out/ (the A4 work log): its block only
            if more:
                L.append(f'<section class="group"><div class="grouphead">{esc(heading)}</div>{more}</section>')
            continue
        if not items and not more and key not in KEY_FILES:
            continue
        newest = max((st.st_mtime for _, st in items), default=None)
        missing = [k for k in KEY_FILES.get(key, ()) if not any(r == f"{key}/{k}" for r, _ in items)]
        L.append(f'<section class="group"><div class="grouphead">{esc(heading)}</div>'
                 f'<div class="line">{esc(what)}. <b>{esc(state)}</b>'
                 + (f"; built {esc(_ts(newest))}" if newest else "") + f"; {len(items)} file(s).</div>")
        if missing:
            L.append(f'<div class="line bad">Missing: {esc(", ".join(missing))} (built by '
                     "<code>python -m tenderpack outputs</code>).</div>")
        depth = 1 if key else 0
        top = [(r, s) for r, s in items if r.count("/") <= depth]
        sub: dict[str, list] = {}
        for r, s in items:
            if r.count("/") > depth:
                sub.setdefault(r.rsplit("/", 1)[0], []).append((r, s))
        if top:
            L.append(table(FILE_HEAD, [file_row(base, area, r, s) for r, s in top]))
        for folder, fs in sub.items():
            L.append(f"<details><summary>{esc(folder)}/: {len(fs)} more file(s)</summary>"
                     + table(FILE_HEAD, [file_row(base, area, r, s, r[len(folder) + 1:]) for r, s in fs])
                     + "</details>")
        L.append(more + "</section>")
    return "".join(L)


def evidence_listing(base: str, review_dir: Path) -> str:
    files = walk(review_dir)
    if not files:
        return '<p class="note">No evidence packets (no image regions in the evidence build, or no build yet).</p>'
    by: dict[str, list] = {}
    for rel, st in files:
        by.setdefault(rel.split("/", 1)[0] if "/" in rel else "", []).append((rel, st))
    L = []
    for region, fs in by.items():
        top = [(r, s) for r, s in fs if r.count("/") <= 1]
        deep = [(r, s) for r, s in fs if r.count("/") > 1]
        L.append(f'<div class="line"><b>{esc(region or "review/")}</b>: the image region\'s evidence packet '
                 f"({len(fs)} files)</div>")
        L.append(table(FILE_HEAD, [file_row(base, "evidence-review", r, s, r.split("/", 1)[-1]) for r, s in top]))
        if deep:
            L.append(f"<details><summary>{esc(region)}: crops and renders, {len(deep)} file(s)</summary>"
                     + table(FILE_HEAD, [file_row(base, "evidence-review", r, s, r.split("/", 1)[1]) for r, s in deep])
                     + "</details>")
    return "".join(L)


def validated_state(checks: dict) -> str:
    rel = (checks or {}).get("release") or {}
    n = len(rel.get("blockers") or [])
    s = f"validated through {checks.get('validated_stage')}" if checks.get("validated_stage") else "not validated"
    return s + (f" · {rel.get('status')}" if rel.get("status") else "") + (f" · {n} release blocker(s)" if n else "")


# ---------------------------------------------------------------------------------------------- Home

def stage_line(stages: list[dict], checks: dict) -> str:
    parts = []
    for s in stages:
        bits = [x for x in ((s.get("status") if s.get("stage") != "BASE" else ""),
                            (f"issued {s.get('issued')}" if s.get("issued") else "")) if x]
        parts.append(esc(s.get("stage")) + (f" ({esc(', '.join(bits))})" if bits else ""))
    return (f'<div class="line"><b>Stage:</b> {" → ".join(parts)}. Validated through '
            f"<b>{esc(checks.get('validated_stage'))}</b>; working stage {esc(checks.get('working_stage') or 'none')}."
            "</div>")


DELIVERABLES = (
    ("A1 Compliance register", (("out", "a1/a1.xlsx", "download"), ("out", "a1/a1.csv", "open"))),
    ("A2 Amendment reconciliation", (("out", "a2/a2.md", "open"),)),
    ("A3 Bid-out consequences", (("out", "a3/a3.pdf", "open"), ("out", "a3/a3_detail.html", "open"))),
    (A4_LABEL, (("worklog", "README.md", "open"), ("worklog", "ERROR_INDEX.md", "open"),
                ("page", "worklog", "model calls and subagent briefs"), ("page", "history", "commit history"))),
    (REGISTER_LABEL, (("out", "a4/clarification_register.md", "open"), ("out", "a4/clarification_register.csv", "open"),
                      ("out", "a4/clarification_register.json", "open"))),
    ("A5 Bid programme and submission marshalling", (
                          ("out", "a5/programme.csv", "open"), ("out", "a5/programme.json", "open"),
                          ("out", "a5/marshalling.csv", "open"), ("out", "a5/marshalling.json", "open"),
                          ("out", "a5/gantt.html", "open"), ("out", "a5/gantt.pdf", "open"),
                          ("out", "a5/README.md", "open"))),
    ("Review batches (your decisions)", (("out", "review/index.html", "open"),)),
)


def deliverables(base: str, cfg) -> str:
    """The deliverables first: one line per A1-A5 (and the review batches) with the key file(s) that exist, each
    opening in the browser or downloading; a missing key file is named so. The full listing follows further down."""
    roots = {"out": Path(cfg.out), "worklog": Path(cfg.root) / "worklog"}
    L = ['<section class="deliv"><h2>Deliverables</h2>']
    for label, files in DELIVERABLES:
        parts = []
        for area, rel, how in files:
            if area == "page":                           # a panel page (the work log's listing, the history)
                parts.append(f'<a href="{base}{rel}">{esc(how)}</a>')
                continue
            path = roots[area] / rel
            name = rel.rsplit("/", 1)[-1]
            if not path.is_file():
                parts.append(f"<code>{esc(name)}</code> (missing)")
                continue
            if how == "download":
                parts.append(f'<a href="{base}download/{area}/{esc(rel)}">{esc(name)}</a> (download)')
            else:
                parts.append(f'<a href="{base}file/{area}/{esc(rel)}">{esc(name)}</a> '
                             f'(<a href="{base}download/{area}/{esc(rel)}">download</a>)')
        L.append(f'<div class="line"><b>{esc(label)}:</b> ' + " · ".join(parts) + "</div>")
        if label.startswith("A5 "):
            L.append('<div class="line note">The CSV/JSON programme and marshalling plan are the A5 deliverables; '
                     'the chart is a supporting view. Use latest_start/latest_finish and drop_dead_start for the '
                     'backward schedule. Earliest dates are feasibility diagnostics. Durations and resource '
                     'capacities are labelled assumptions; review infeasible work and overloads.</div>')
    L.append('<div class="line note">Every other file (CSV and JSON tables, the scenarios, the evidence packets) is '
             'listed under "Outputs" below.</div></section>')
    return "".join(L)


def home(base: str, cfg, jobs: list[dict], addendum_box: str) -> str:
    out = cfg.out
    checks = read_json(out / "checks.json") or {}
    stages = read_json(out / "stages.json") or []
    items = (read_json(out / "review" / "items.json") or {}).get("items") or []
    files = walk(out)
    demo = bool(checks.get("_interview_demo"))
    L = ['<p class="banner">INTERVIEW DEMO — approvals are simulated and remain editable. Not a tender release.</p>'] if demo else []
    if demo:
        addendum_box = addendum_box.replace("every proposal stays PROPOSED and out/ is not touched.",
            "eligible reviews are assumed approved for this demo; missing evidence stays unresolved. The ADD02 outputs remain available.")
    if stages:
        L.append(stage_line(stages, checks))
    for b in (checks.get("release") or {}).get("blockers") or []:
        L.append(f'<div class="line bad"><b>Blocker ({esc(b.get("kind"))}):</b> {esc(b.get("detail"))}</div>')
    if checks.get("release"):
        L.append(f'<div class="line note">{esc(checks["release"].get("note"))}. The decisions are yours: '
                 f'<a href="{base}decisions">Decisions</a>.</div>')
    if files:
        L.append(deliverables(base, cfg))
    L.append(addendum_box)
    L.append(f"<h2>Outputs in {esc(out)}</h2>")
    if not files:
        L.append(f'<p class="bad lead">No outputs yet in <code>{esc(out)}</code>.</p><p>Build them with '
                 "<code>python -m tenderpack outputs</code> (about 20 seconds; it needs the evidence build, made by "
                 "<code>python -m tenderpack ingest</code>): "
                 f"{button(base, 'jobs/start', 'Run outputs', {'action': 'outputs'})} "
                 f"{button(base, 'jobs/start', 'Run ingest', {'action': 'ingest'})}</p>")
    else:
        L.append('<p class="note">Every file that exists, grouped. The file name opens it in the browser (a '
                 'spreadsheet downloads); "download" saves it. A1-A5 here are the deliverables.</p>')
        L.append(listing(base, "out", out, validated_state(checks), {"_a4": worklog_block(base, cfg.root / "worklog"),
                                                                       "a4": f'<div class="line">The outputs README: '
                                                                             f'{_one(base, "out", "README.md", out)}.'
                                                                             "</div>"}))
    L.append(f"<h2>Evidence packets in {esc(cfg.evidence / 'review')}</h2>")
    L.append(evidence_listing(base, cfg.evidence / "review"))
    L.append("<h2>Execution: rebuild and check</h2>")
    L.append("<p>" + " ".join(button(base, "jobs/start", lab, {"action": a}) for a, lab in (
        ("ingest", "Run ingest (rebuild the evidence)"), ("outputs", "Run outputs (rebuild A1-A5)"),
        ("strict", "Run strict check (release)"), ("check-register", "Run check-register"))) + "</p>")
    last = {}
    for j in jobs:
        if j.get("group") == "build":
            last.setdefault(j["kind"], j)
    L.append(table(JOB_HEAD, [job_row(base, j) for j in last.values()]))
    L.append("<h2>Completeness</h2>")
    L.append(table(["Check", "Stage", "Result", "Detail"],
                   [[esc(c.get("id")), esc(c.get("stage") or ""),       # the engine's own wording: ok / REPORTED
                     esc("ok" if c.get("ok") else "REPORTED (report only)"), esc(c.get("detail"))]
                    for c in checks.get("reported") or []]))
    L.append("<h2>Structural validation</h2>")
    if checks:
        L.append(f"<p>Structural status: {_okcell(checks.get('status') == 'ok', esc(checks.get('status')))}</p>")
    L.append(table(["Check", "Result", "Detail"], [[esc(c.get("id")), _okcell(c.get("ok")), esc(c.get("detail"))]
                                                   for c in checks.get("structural") or []]))
    L.append("<h2>Demo approval status (assumed reviews)</h2>" if demo else "<h2>Human approval</h2>")
    cnt = Counter((i.get("kind"), i.get("status")) for i in items)
    L.append(table(["Kind", "Status", "Count"], [[esc(k), esc(s), esc(n)] for (k, s), n in sorted(cnt.items())]))
    return page(base, "Home: outputs and new addendum", "".join(L))


def worklog_block(base: str, wl: Path) -> str:
    """The A4 work log's lines on Home (session 13): the index, the error note, the model calls and briefs, the
    history."""
    n_calls = len(walk(Path(wl) / "model_calls"))
    n_briefs = len(walk(Path(wl) / "subagent_briefs"))
    return ('<div class="line">the brief\'s A4: the repository with its real commit history, the prompts and model '
            "calls, and the note of every place the system was wrong.</div>"
            f'<div class="line">{_one(base, "worklog", "README.md", wl)} (the index: every session, where each part '
            f'is) · {_one(base, "worklog", "ERROR_INDEX.md", wl)} (every error and how it was caught) · '
            f'<a href="{base}worklog">the session logs, {n_calls} model-call log(s) and {n_briefs} subagent brief(s)'
            f'</a> · <a href="{base}history">the commit history</a></div>')


def worklog_page(base: str, wl: Path) -> str:
    """The A4 work log, read-only: worklog/ grouped (index and errors, session logs, model_calls/, subagent_briefs/,
    anything else), each file opening in the browser or downloading."""
    files = walk(Path(wl))
    groups: dict[str, list] = {}
    for rel, st in files:
        top = rel.split("/", 1)[0] if "/" in rel else ""
        groups.setdefault(top, []).append((rel, st))
    L = ['<p class="note">A4, the work log: the repository with its real commit history '
         f'(<a href="{base}history">the commit history</a>), the prompts and model calls, and the note of every place '
         "the system was wrong. Read-only.</p>"]
    top = groups.pop("", [])
    first = [x for x in top if x[0] in ("README.md", "ERROR_INDEX.md")]
    rest = [x for x in top if x[0] not in ("README.md", "ERROR_INDEX.md")]
    L.append("<h2>The index and the error note</h2>" + table(FILE_HEAD, [file_row(base, "worklog", r, s)
                                                                          for r, s in first]))
    L.append("<h2>Session logs and the owner's prompts</h2>" + table(FILE_HEAD, [file_row(base, "worklog", r, s)
                                                                                for r, s in rest]))
    for folder in ("model_calls", "subagent_briefs", *sorted(k for k in groups if k not in ("model_calls",
                                                                                              "subagent_briefs"))):
        fs = groups.get(folder) or []
        L.append(f"<h2>{esc(folder)}/ ({len(fs)} file(s))</h2>")
        if fs:
            L.append(f"<details><summary>{esc(folder)}/: {len(fs)} file(s)</summary>"
                     + table(FILE_HEAD, [file_row(base, "worklog", r, s, r[len(folder) + 1:]) for r, s in fs])
                     + "</details>")
    return page(base, "A4 Work log", "".join(L))


def history_page(base: str, lines: list[str] | None, why_not: str | None) -> str:
    """The commit history (`git log`, read-only), or why it is not available here."""
    if lines is None:
        body = (f'<p class="bad">The commit history is not available here: {esc(why_not)}.</p><p class="note">An '
                "operating copy (the interview folder) holds no .git: the submitted repository is preserved "
                "separately and carries the history (<code>git log --stat</code> there).</p>")
    else:
        body = (f'<p class="note">git log, read-only ({len(lines)} commit(s), newest first). Nothing here can change '
                "the history.</p><pre>" + esc("\n".join(lines)) + "</pre>")
    return page(base, "A4 Work log: the commit history", body)


def _one(base: str, area: str, rel: str, root: Path) -> str:
    if not (Path(root) / rel).is_file():
        return f"<code>{esc(rel)}</code> (missing)"
    return f'<a href="{base}file/{area}/{esc(rel)}">{esc(area)}/{esc(rel)}</a>'


# ---------------------------------------------------------------------------------------------- new addendum

def route_choices(routes: dict | None, host_found: bool, cassette: bool) -> tuple[list[dict], str | None, str]:
    """[{value, label, available, why}], the default route, and the offline state (the engine's own reading of
    TENDERPACK_OFFLINE / config `offline`, from `tenderpack ai routes --json`). Session 13: every route is listed
    (host = Claude Code, codex, anthropic, openrouter, ollama) with its recorded status (config/routes_status.yaml:
    tested / built, unverified / untested / ...) in the label and, when it cannot be chosen now, why and what the owner
    must do (the engine's own `available` / `why`; a key is never shown, only whether one is configured)."""
    rows = {r.get("route"): r for r in (routes or {}).get("routes") or []}
    off = (routes or {}).get("offline")
    out = []

    def status(name):
        # session 13 (F4; audit R3 recheck N-3): a route recorded as tested says where (routes_status.yaml `where`), so
        # the panel on the owner's Mac never reads 'tested' as tested there
        rec = (rows.get(name) or {}).get("status") or {}
        st, where = rec.get("status"), rec.get("where")
        return (f" [{st} in {where}]" if st == "tested" and where and where != "-" else f" [{st}]") if st else ""
    host_name = "Codex" if (routes or {}).get("host_driver") == "codex" else "Claude Code"
    host_label = f"host: {host_name} on this machine (your signed-in account)" + status("host")
    if off:
        out.append({"value": "host", "label": host_label, "available": False,
                    "why": f"offline mode is on ({off}): only the local ollama route"})
    else:
        out.append({"value": "host", "label": host_label, "available": True, "why": "" if host_found else
                    "the configured host command is not found here: the run will stop and wait for each batch to be submitted "
                    "by hand (tenderpack ai submit-batch)"})
    if "codex" in rows:
        out.append({"value": "codex", "label": "codex: Codex over MCP (manual path)" + status("codex"),
                    "available": False, "why": rows["codex"].get("why") or "the workflow starts Claude Code only"})
    for name, label in (("anthropic", "anthropic: the Messages API with your key (paid)"),
                        ("openrouter", "openrouter: OpenRouter with your key (paid)")):
        if name not in rows:
            continue
        ok = bool(rows[name].get("available")) and not off
        why = "" if ok else (f"offline mode is on ({off}): only the local ollama route" if off else
                             rows[name].get("why") or "not configured")
        out.append({"value": name, "label": label + status(name), "available": ok, "why": why})
    oll = rows.get("ollama")
    usable = [m for m in (oll or {}).get("models") or [] if m.get("ok")]
    out.append({"value": "ollama", "label": "ollama: a local model on this machine (offline, free)" + status("ollama"),
                "available": bool(usable), "why": "" if usable else
                f"not usable now: {(oll or {}).get('error') or 'no configured model is installed and usable'}"
                " (tenderpack ai ollama-models lists the installed models; nothing is pulled)"})
    if cassette:
        out.append({"value": "recorded", "label": "test replay (a cassette; not a live model)", "available": True,
                    "why": "configured for tests only"})
    default = None
    if not off and host_found:
        default = "host"
    elif usable:
        default = "ollama"
    return out, default, off or ""


def addendum_box(base: str, routes: dict | None, routes_error: str | None, next_add: str, host_found: bool,
                 cassette: bool, limit_mb: int, base_run: dict | None = None) -> str:
    choices, default, off = route_choices(routes, host_found, cassette)
    radios = []
    for c in choices:
        dis = "" if c["available"] else " disabled"
        chk = " checked" if c["value"] == default else ""
        why = f' <span class="note">({esc(c["why"])})</span>' if c["why"] else ""
        radios.append(f'<div><label><input type="radio" name="route" value="{c["value"]}"{chk}{dis}> '
                      f"{esc(c['label'])}</label>{why}</div>")
    usable = [m for r in (routes or {}).get("routes") or [] if r.get("route") == "ollama"
              for m in r.get("models") or [] if m.get("ok")]
    models = ['<option value="">the configured model for each step (config/ai.yaml)</option>'] + [
        f'<option value="{esc(m.get("id"))}">{esc(m.get("id"))} (ollama, {esc(m.get("role"))})</option>'
        for m in usable]
    model_note = "" if usable else ' <span class="note">(no other choice here: each route uses its configured ' \
                                   "model)</span>"
    none_msg = "" if default else ('<div class="line bad">No route is ready by default: choose one that is available '
                                   "(the reason is beside each).</div>")
    adv = ""
    if base_run is not None:
        if base_run.get("available") and base_run.get("runs"):
            opts = '<option value="">none (start from the validated state)</option>' + "".join(
                f'<option value="{esc(r)}">{esc(r)}</option>' for r in base_run["runs"])
            adv = ("<details><summary>Advanced: start from another run's candidate (--base-run)</summary>"
                   f'<select name="base_run">{opts}</select></details>')
        else:
            adv = ('<details><summary>Advanced</summary><select name="base_run" disabled><option value="">'
                   f'{"no run to start from" if base_run.get("available") else "not in this build"}</option>'
                   "</select></details>")
    err = f'<div class="line bad">tenderpack ai routes --json did not answer: {esc(routes_error)}</div>' \
        if routes_error else ""
    return (f'<section class="box"><h2>New addendum</h2><div class="line note">Upload the addendum PDF and start: the '
            "run builds a CANDIDATE in its own folder under <code>staging/ai/runs/</code> (A1-A5, a review packet, "
            "the diff); every proposal stays PROPOSED and out/ is not touched. You land on the run's page, which "
            f"follows it.</div>{err}"
            f'<form method="post" action="{base}addendum/start" enctype="multipart/form-data">'
            f'<div class="line"><label>1. The PDF (at most {limit_mb} MB) <input type="file" name="pdf" '
            f'accept="application/pdf" required></label></div>'
            f'<div class="line"><label>2. Addendum id <input name="addendum" value="{esc(next_add)}" size="7" '
            f'pattern="ADD-[0-9]{{2}}"></label> <span class="note">(the next one after the pack\'s last)</span></div>'
            f'<div class="line">3. Route:{"".join(radios)}</div>{none_msg}'
            f'<div class="line"><label>4. Model <select name="model">{"".join(models)}</select></label>{model_note}'
            f'</div><div class="line"><label><input type="checkbox" name="offline" value="yes"'
            f'{" checked" if off else ""}> 5. Offline (only the local ollama route; '
            f'{"pre-set: " + esc(off) if off else "TENDERPACK_OFFLINE is not set"})</label></div>{adv}'
            f'<div class="line"><button>Start the run</button> <button formaction="{base}quickreview/start" '
            f'class="secondary">Start AI quick review (preliminary briefing)</button> <span class="note">(a separate, bounded AI reading of '
            "the same PDF on the route chosen above: ONE session, a short budget, lower priority than the run; it "
            "writes a PRELIMINARY AI BRIEFING, unverified, and changes nothing; the quick review itself has run on the "
            "test replay only so far: `tenderpack ai routes` says so per route)</span></div></form></section>")


def addendum_page(base: str, box: str, routes: dict | None) -> str:
    L = [box]
    if routes:
        L.append("<h2>Routes (tenderpack ai routes --json)</h2>")
        L.append(table(["Route", "Kind", "Checked", "Models"], [
            [esc(r.get("route")), esc(r.get("kind")), esc(r.get("checked")),
             "<br>".join(esc(f"{m.get('role')}: {m.get('id')}" + ("" if r.get("route") != "ollama" else
                                                                 (" (usable)" if m.get("ok") else
                                                                  f" (NOT USABLE: {m.get('problem')})")))
                         for m in r.get("models") or [])] for r in routes.get("routes") or []]))
    return page(base, "New addendum", "".join(L))


# ---------------------------------------------------------------------------------------------- Stages

def pack_docs(pack: Path) -> list[dict]:
    import yaml
    try:
        return (yaml.safe_load(Path(pack).read_text(encoding="utf-8")) or {}).get("documents") or []
    except (OSError, ValueError, yaml.YAMLError):
        return []


def candidate_runs(staging: Path) -> list[tuple[str, dict]]:
    out = []
    rd = Path(staging) / "runs"
    for d in sorted(rd.iterdir()) if rd.is_dir() else []:
        cp = read_json(d / "checkpoint.json")
        if isinstance(cp, dict) and cp.get("addendum"):
            out.append((d.name, cp))
    return out


def cand_paths(run_dir: Path, cp: dict) -> dict:
    """The candidate workspace where the run's checkpoint records it (`candidate`: dir, pack, build, out, pdf_copy, as
    the engine writes and reads it); the engine's default layout (candidate.paths) when the record is absent. A
    recorded path outside the run's own folder is not used."""
    run_dir = Path(run_dir)
    rec = (cp or {}).get("candidate") or {}
    d = run_dir / "candidate"

    def pick(key, default):
        v = rec.get(key)
        if v and Path(v).is_absolute():
            p = Path(v)
            try:
                if p.resolve().is_relative_to(run_dir.resolve()):
                    return p
            except OSError:
                pass
        return default
    out = {"dir": pick("dir", d), "pack": pick("pack", d / "pack.yaml"), "build": pick("build", d / "build"),
           "out": pick("out", d / "out"), "pdf": pick("pdf_copy", None)}
    if out["pdf"] is None:
        pdfs = sorted((Path(out["dir"]) / "input").glob("*.pdf"))
        out["pdf"] = pdfs[-1] if pdfs else None
    return out


def run_file_href(base: str, rid: str, run_dir: Path, p: Path | None) -> str | None:
    """The panel link for a file inside the run's folder (served only from the run's candidate/out, candidate/input
    and review parts, or where the checkpoint records the candidate)."""
    if p is None:
        return None
    try:
        rel = Path(p).resolve().relative_to(Path(run_dir).resolve()).as_posix()
    except (OSError, ValueError):
        return None
    return f"{base}file/runs/{esc(rid)}/{esc(urllib.parse.quote(rel))}"


def stages_page(base: str, cfg, runs: list[tuple[str, dict]], pre: dict, run_jobs: dict | None = None) -> str:
    stages = read_json(cfg.out / "stages.json") or []
    docs = {d.get("doc_id"): d for d in pack_docs(cfg.pack)}
    opts = [(s["stage"], f"{s['stage']} (validated state: {s.get('status')})") for s in stages] or \
        [("BASE", "BASE")] + [(k, k) for k in docs if str(k).startswith("ADD-")]
    cands = []
    for rid, cp in runs:
        cpath = cand_paths(Path(cfg.staging) / "runs" / rid, cp)
        if (Path(cpath["build"]) / "units.json").is_file():
            cands.append((f"run:{rid}:{cp['addendum']}", f"{cp['addendum']} @ run {rid} (CANDIDATE, {cp.get('status')})"))
    L = ['<p class="note">Compare two stages: the report is <code>tenderpack diff</code> run as a job. A comparison '
         "with a candidate stage runs in that run's candidate workspace (its earlier stages are copies of the "
         "validated state); two different candidate runs cannot be compared in one diff.</p>"]

    def sel(name, chosen):
        return f'<select name="{name}">' + "".join(
            f'<option value="{esc(v)}"{" selected" if v == chosen else ""}>{esc(t)}</option>' for v, t in opts + cands
        ) + "</select>"
    first = opts[-2][0] if len(opts) > 1 else opts[0][0]
    L.append(f'<form method="post" action="{base}stages/diff"><label>from {sel("frm", pre.get("frm") or first)}'
             f'</label><label>to {sel("to", pre.get("to") or opts[-1][0])}</label><button>Compare</button></form>')
    L.append("<h2>Stages and their sources</h2>")
    rows = []
    for s in stages or [{"stage": "BASE"}]:
        st = s["stage"]
        if st == "BASE":
            src = "<br>".join(_src_link(base, d) + f' · <a href="{base}units?doc={esc(k)}">units of {esc(k)}</a>'
                              for k, d in docs.items() if d.get("kind") == "volume")
        else:
            src = _src_link(base, docs.get(st)) + f' · <a href="{base}units?doc={esc(st)}">units of {esc(st)}</a>'
        rows.append([esc(st), esc(s.get("status", "")), esc(s.get("issued") or ""), src])
    for rid, cp in runs:
        rdir = Path(cfg.staging) / "runs" / rid
        cpath = cand_paths(rdir, cp)
        href = run_file_href(base, rid, rdir, cpath["pdf"])
        src = f'<a href="{href}">{esc(Path(cpath["pdf"]).name)}</a>' if href else ""
        if (Path(cpath["build"]) / "units.json").is_file():
            src += (f' · <a href="{base}units?doc={esc(cp["addendum"])}&amp;run={esc(rid)}">units of '
                    f'{esc(cp["addendum"])}</a>')
        syn = synthetic_label(cp, (run_jobs or {}).get(rid))        # session 13 (R3-6): as on the Runs page
        rows.append([esc(cp["addendum"]) + " <b>CANDIDATE</b>" + (f' <span class="note nw">{esc(syn)}</span>' if syn
                                                                  else ""),
                     esc(cp.get("status")) + f' (<a href="{base}runs/'
                     f'{esc(rid)}">run {esc(rid)}</a>)', "", src or '<span class="note">no candidate yet</span>'])
    L.append(table(["Stage", "Status", "Issued", "Sources"], rows))
    L.append(f"<h2>Image region renders ({esc(Path(cfg.evidence) / 'review')})</h2>")
    L.append(evidence_listing(base, Path(cfg.evidence) / "review"))
    return page(base, "Stages and sources", "".join(L))


def _src_link(base: str, d: dict | None) -> str:
    if not d or not str(d.get("path", "")).startswith("sources/"):
        return '<span class="note">no source</span>'
    rel = str(d["path"])[len("sources/"):]
    return f'<a href="{base}file/sources/{esc(rel)}">{esc(Path(rel).name)}</a>'


def units_page(base: str, doc: str, units: list[dict], pdf_href: str | None, candidate: str | None) -> str:
    L = []
    if candidate:
        L.append(f'<p class="banner">{CANDIDATE_BANNER} (run {esc(candidate)})</p>')
    rows = []
    for u in units:
        pages = u.get("pages") or []
        pl = " ".join((f'<a href="{pdf_href}#page={int(p)}">p{int(p)}</a>' if pdf_href else f"p{int(p)}")
                      for p in pages if isinstance(p, int))
        rows.append([f"<code>{esc(u.get('unit_id'))}</code>", esc(u.get("kind")), pl,
                     esc(_short(u.get("text"), 500))])
    L.append(table(["Unit", "Kind", "Pages (open the PDF there)", "Text (as printed)"], rows))
    return page(base, f"Units of {doc}", "".join(L))


# ---------------------------------------------------------------------------------------------- runs

def _lock_state(run_dir: Path) -> str | None:
    """'interrupted' when the checkpoint says running but no live process holds the run lock on this machine."""
    info = read_json(run_dir / "run.lock")
    if not isinstance(info, dict):
        return "interrupted"
    if info.get("host") != socket.gethostname():
        return None
    try:
        os.kill(int(info.get("pid")), 0)
    except (OSError, ValueError, TypeError):
        return "interrupted"
    return None


def run_state(run_dir: Path, cp: dict) -> str:
    st = str(cp.get("status"))
    if st == "running" and _lock_state(run_dir) == "interrupted":
        return "interrupted (no process is driving it: resume it)"
    return st


def synthetic_label(cp: dict, job: dict | None) -> str:
    pdf = str((cp.get("settings") or {}).get("pdf") or "")
    if "/rehearsals/" in pdf or (job and (job.get("meta") or {}).get("synthetic")):
        return "synthetic (rehearsal input)"
    return ""


def _parse(ts) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(str(ts), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def duration(start, end=None) -> str:
    a, b = _parse(start), (_parse(end) if end else dt.datetime.now(dt.timezone.utc))
    if not a or not b:
        return ""
    s = max(0, int((b - a).total_seconds()))
    return f"{s // 3600}h {s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m {s % 60:02d}s"


def _exit_code(cp: dict):
    st = cp.get("status")
    if st in ("complete", "partial"):
        return 1 if (cp.get("steps") or {}).get("outputs", {}).get("refused") else 0
    if st == "stopped":
        return cp.get("stop_code", 0) or 0
    return {"waiting_for_host": 4, "failed": 1, "refused": 2, "deferred": 5}.get(st)


def needs(cp: dict, state: str, running_job: dict | None) -> str:
    """One line: what the run needs from the person now."""
    st = cp.get("status")
    if running_job:
        return "Nothing yet: it is running (its page refreshes every 10 s)."
    if state.startswith("interrupted"):
        return "Press Resume: the run was interrupted; done batches are not asked again."
    if st == "deferred":
        return "Wait for the rate-limit reset named on its page, then press Resume."
    if st == "waiting_for_host":
        return "Submit the waiting batch (tenderpack ai submit-batch RUN FILE --by NAME), or press Resume."
    if st == "stopped" and cp.get("stop_code") == 6:
        return "Do what the reason says (" + _short(cp.get("status_reason"), 160) + "), then press Resume."
    if st == "stopped":
        return "Press Resume when ready (it stopped where it was asked to)."
    if st == "failed":
        return ("It failed (" + _short(cp.get("status_reason"), 140) + "): read the failure on its page; once fixed, "
                "press Resume (or Resume from the failed step).")
    if st == "refused":
        return "Fix the input named in the reason and start a new run."
    if st in ("complete", "partial"):
        unres = (cp.get("completeness") or {}).get("provisions") or {}
        n = len(unres.get("unresolved") or [])
        return ("Review the candidate: open its review packet first" + (f"; {n} provision(s) unresolved" if n else "")
                + (". Demo approvals are simulated and remain editable." if (cp.get("approval") or {}).get("status") == "simulated"
                   else ". Nothing is accepted until you decide."))
    return "Open the run to see where it stands."


def runs_page(base: str, runs: list[tuple[str, dict]], staging: Path, run_jobs: dict, running: dict) -> str:
    rows = []
    for rid, cp in sorted(runs, key=lambda x: str(x[1].get("created") or ""), reverse=True):
        j = run_jobs.get(rid)
        state = run_state(Path(staging) / "runs" / rid, cp)
        rj = running.get(rid)
        brun = (cp.get("settings") or {}).get("base_run")
        brun = brun.get("run_id") if isinstance(brun, dict) else brun
        rows.append([f'<a href="{base}runs/{esc(rid)}">{esc(rid)}</a>', esc(cp.get("addendum")),
                     esc((cp.get("settings") or {}).get("route")), esc("running" if rj else state),
                     esc(cp.get("created") or ""),
                     esc(duration(cp.get("created"), None if rj else cp.get("updated"))),
                     esc(brun or "none"), esc(needs(cp, state, rj)), esc(synthetic_label(cp, j))])
    return page(base, "Runs", '<p class="note">Every addendum run under <code>' + esc(Path(staging) / "runs") +
                "</code>, newest first. A run is a CANDIDATE until a person reviews it.</p>" +
                table(["Run", "Addendum", "Route", "Status", "Started", "Duration", "Base run",
                       "What it needs from you", "Data"], rows), refresh=10 if running else None)


def _secs(x) -> str:
    try:
        return f"{float(x):.1f}"
    except (TypeError, ValueError):
        return ""


def critic_disagreements(md: str) -> list[str]:
    """The items of the review packet's Critic section where the critic does not agree (its own words)."""
    sec = _section(md, "## Critic")
    out, cur = [], []
    for ln in sec.splitlines():
        if ln.startswith("- **"):
            if cur:
                out.append("\n".join(cur))
            cur = [ln]
        elif cur and ln.startswith("  "):
            cur.append(ln)
    if cur:
        out.append("\n".join(cur))
    return [b for b in out if re.search(r"critic[^\n]*: (disagrees|does not agree|not agree)", b, re.I)]


def run_detail(base: str, rid: str, run_dir: Path, cp: dict, job: dict | None, running_job: dict | None,
               steps: tuple, cand_listing: str) -> str:
    state = run_state(run_dir, cp)
    s = cp.get("settings") or {}
    st = cp.get("steps") or {}
    b = cp.get("batches") or {}
    code = _exit_code(cp)
    demo = (cp.get("approval") or {}).get("status") == "simulated"
    L = [f'<p class="banner">{DEMO_CANDIDATE_BANNER if demo else CANDIDATE_BANNER}</p>']
    syn = synthetic_label(cp, job)
    cur = next((k for k in steps if (st.get(k) or {}).get("status") == "running"), None)
    if running_job:
        lead = f"Running: step {cur or 'starting'}" + (f" ({list(steps).index(cur) + 1} of {len(steps)})" if cur else "")
    else:
        lead = {"partial": "Finished: partial (some provisions or tasks are not answered; see below)",
                "complete": "Finished: complete"}.get(cp.get("status"), f"Status: {state}")
    L.append(f'<p class="lead">{esc(lead)}</p>')
    L.append(f'<p><a href="{base}interview?run={esc(rid)}">Inspect or change all demo decisions for this run</a></p>')
    L.append(f"<p>Addendum {esc(cp.get('addendum'))} · route {esc(s.get('route'))} · started {esc(cp.get('created'))}"
             f" · duration {esc(duration(cp.get('created'), None if running_job else cp.get('updated')))}"
             + (f" · <b>{esc(syn)}</b>" if syn else "") + "</p>")
    L.append("<h2>What it needs from you</h2>")
    L.append(f"<p>{esc(needs(cp, state, running_job))}</p>")
    if (run_dir / "review" / "index.html").is_file():
        L.append(f'<p><a class="primary" href="{base}file/runs/{esc(rid)}/review/index.html">Open the review packet</a>'
                 + (f' &nbsp; <a href="{base}file/runs/{esc(rid)}/review/diff.md">the diff</a>'
                    if (run_dir / "review" / "diff.md").is_file() else "")
                 + ' &nbsp; <a href="#candidate">the candidate outputs on this page</a></p>')
    person = []
    for k, v in b.items():
        if v.get("status") in ("escalated", "deferred", "waiting_for_host"):
            extra = ""
            if v.get("reset_in_s"):
                extra = f"; the rate-limit reset was named in about {float(v['reset_in_s']) / 60:.0f} min"
            person.append(f"{k}: {v.get('status')}{extra}: {_short(v.get('error') or v.get('reason') or '', 300)}")
    rd = st.get("readings") or {}
    if rd.get("escalated"):
        person.append(f"readings escalated to a person: {_short(rd.get('reason') or rd.get('escalated'), 300)}")
    md = _read(run_dir / "review" / "index.md")
    hdp = [ln for ln in md.splitlines() if "HUMAN DECISION PENDING" in ln]
    if hdp:
        person.append(f"{len(hdp)} line(s) of the review packet are HUMAN DECISION PENDING (listed under Pending "
                      "questions below)")
    rsec = _section(md, "## Readings of the addendum's image regions")
    if "PENDING HUMAN REVIEW" in rsec:
        person.append("readings of the addendum's image regions are PENDING HUMAN REVIEW (see the review packet)")
    if person:
        L.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in person) + "</ul>")
    if running_job:
        L.append("<p>" + button(base, f"jobs/{running_job['id']}/stop", "Stop (interrupt; Resume later)")
                 + f' <a href="{base}jobs/{esc(running_job["id"])}">the job and its output</a></p>')
    else:
        opts = '<option value="">continue from the checkpoint</option>' + "".join(
            f'<option value="{esc(k)}">rerun from step {esc(k)}</option>' for k in steps)
        L.append(f'<form method="post" action="{base}runs/{esc(rid)}/resume"><select name="from_step">{opts}</select>'
                 f' <button>Resume</button> <span class="note">runs <code>tenderpack ai resume {esc(rid)}</code>; done '
                 "batches are never asked again</span></form>")
    L.append(quick_review_box(base, rid, run_dir, cp))               # session 13, part 4
    # ---- execution
    L.append("<h2>Execution</h2>")
    L.append(f"<p>Run status: <b>{esc('running' if running_job else state)}</b>"
             + (f"; exit {esc(code)}: {esc(AI_EXIT.get(code, ''))}" if code is not None and not running_job
                and cp.get("status") != "running" else "") + f"</p><p>Reason: {esc(cp.get('status_reason'))}</p>")
    L.append("<h3>Steps</h3>" + table(["#", "Step", "Status", "Seconds", "Reason recorded by the step"], [
        [f'<span class="nw">{i + 1}</span>', esc(k), esc(STEP_WORDS.get((st.get(k) or {}).get("status", "pending"),
                                                (st.get(k) or {}).get("status"))),
         _secs((st.get(k) or {}).get("seconds")), esc(_short((st.get(k) or {}).get("reason") or "", 300))]
        for i, k in enumerate(steps or list(st))]))
    L.append("<h3>Batches</h3>" + table(["Batch", "Status", "Attempts", "Failure class", "Error / reason"], [
        [esc(k), esc(v.get("status")), esc(v.get("attempts", "")), esc(v.get("failure_class") or ""),
         esc(_short(v.get("error") or v.get("reason") or "", 400))] for k, v in b.items()]))
    bad = [(k, v) for k, v in b.items() if v.get("status") in ("failed", "deferred", "escalated", "interrupted",
                                                                 "waiting_for_host")]
    L.append("<h3>Failures and deferrals</h3>")
    if bad or cp.get("status") in ("failed", "refused"):
        items = []
        if cp.get("status") in ("failed", "refused"):
            items.append(f"<li>The run {esc(cp.get('status'))}: {esc(cp.get('status_reason'))}"
                         + (f" (exit {esc(code)}: {esc(AI_EXIT.get(code, ''))})" if code is not None else "") + "</li>")
        for k, v in bad:
            t = f"{k}: {v.get('status')}"
            if v.get("status") == "deferred" or v.get("failure_class") == "rate_limit":
                r = v.get("reset_in_s")
                t += " (rate limit" + (f"; the reset was named in about {float(r) / 60:.0f} min" if r else "") + \
                    "; the run stops with exit 5 and resumes after the reset)"
            items.append(f"<li>{esc(t)}: {esc(_short(v.get('error') or '', 400))}</li>")
        L.append("<ul>" + "".join(items) + "</ul>")
    else:
        L.append('<p class="note">none</p>')
    L.append('<p class="note">Exit codes: ' + "; ".join(f"{k} {esc(v)}" for k, v in AI_EXIT.items()) + "</p>")
    L.append("<h3>Critic (a second model; agreement is not approval)</h3>")
    cs = st.get("critic") or {}
    if cs.get("status"):
        L.append(f"<p>Critic step: {esc(cs.get('status'))}; reviewed {esc(cs.get('reviewed', 0))}; does not agree "
                 f"{esc(cs.get('disagrees', 0))}. {esc(cs.get('note') or cs.get('reason') or '')}</p>")
    dis = critic_disagreements(md)
    L.append(("<pre>" + esc("\n\n".join(dis)) + "</pre>") if dis else
             ('<p class="note">Disagreements were recorded; open the review packet for the details.</p>'
              if cs.get("disagrees") else '<p class="note">no disagreement recorded so far</p>'))
    # ---- completeness
    L.append("<h2>Completeness</h2>")
    comp = cp.get("completeness") or {}
    prov = Counter(v.get("status") for v in (cp.get("provisions") or {}).values())
    L.append(f"<p>Completeness: <b>{esc(comp.get('status') or 'not computed')}</b>; provisions: "
             + esc(", ".join(f"{k} {n}" for k, n in sorted(prov.items())) or "none") + "</p>")
    L.append("<ul>" + "".join(f"<li>{esc(r)}</li>" for r in comp.get("reasons") or []) + "</ul>")
    ds = comp.get("downstream") or {}
    if ds:
        L.append(f"<p>Downstream tasks: {esc(ds.get('tasks'))}; answered {esc(ds.get('answered'))}; unanswered "
                 f"{esc(len(ds.get('unanswered') or []))}</p>")
    # ---- structural validation
    L.append("<h2>Structural validation</h2>")
    cpath = cand_paths(run_dir, cp)
    checks = read_json(Path(cpath["out"]) / "checks.json") or {}
    o = st.get("outputs") or {}
    L.append(f"<p>Candidate outputs build: {esc(o.get('status', 'pending'))}"
             + (f"; exit {esc(o.get('exit_code'))}" if o.get("exit_code") is not None else "")
             + (f"; REFUSED: {esc(o.get('reason'))}" if o.get("refused") else "") + "</p>")
    cr = st.get("check_register") or {}
    if cr:
        L.append(f"<p>check-register on the candidate: {esc(cr.get('status'))}"
                 + (f"; exit {esc(cr.get('exit_code'))}" if cr.get("exit_code") is not None else "") + "</p>")
    if checks:
        L.append(f"<p>Candidate structural status: {_okcell(checks.get('status') == 'ok', esc(checks.get('status')))}"
                 "</p>" + table(["Check", "Result", "Detail"], [[esc(c.get("id")), _okcell(c.get("ok")),
                                                                 esc(_short(c.get("detail"), 300))]
                                                                for c in checks.get("structural") or []]))
    else:
        L.append('<p class="note">no candidate checks yet (the outputs step has not built them)</p>')
    # ---- human approval
    L.append("<h2>Demo approval status (assumed reviews)</h2>" if demo else "<h2>Human approval</h2>")
    ap = cp.get("approval") or {}
    if demo:
        L.append(f"<p>{DEMO_CANDIDATE_BANNER} Inspect or change the decisions using this run's decisions link.</p>")
    else:
        L.append(f"<p>Approval: <b>{esc(ap.get('status') or 'none')}</b>. Everything the run proposed is PROPOSED; "
                 "nothing was approved, accepted, rejected or sent by the workflow or by this panel.</p>")
    for d in ap.get("decisions") or []:
        L.append(f"<p>{esc(json.dumps(d, ensure_ascii=False))}</p>")
    # ---- pending questions
    L.append("<h2>Pending questions</h2>")
    sec = _section(md, "## First: unresolved provisions and escalations")
    L.append(f"<pre>{esc(sec)}</pre>" if sec else '<p class="note">no review packet yet</p>')
    if hdp:
        L.append(f"<p>Lines marked HUMAN DECISION PENDING in the review packet: {len(hdp)}</p>"
                 "<pre>" + esc("\n".join(hdp[:60])) + ("\n…" if len(hdp) > 60 else "") + "</pre>")
    win = (read_json(run_dir / "review" / "diff.json") or {}).get("clarification_window") or {}
    if win.get("note"):
        L.append(f"<p>Clarification window: {esc(win.get('note'))}</p>")
    nxt = _section(md, "## Next (a person)")
    if nxt:
        L.append(f"<h3>Next (from the review packet)</h3><pre>{esc(nxt)}</pre>")
    # ---- candidate outputs (when the run is not running)
    if not running_job:
        L.append(cand_listing)
    L.append(f'<p class="note">Read from the run\'s checkpoint (<code>{esc(run_dir / "checkpoint.json")}</code>), the '
             f"record <code>tenderpack ai run-status {esc(rid)}</code> prints.</p>")
    return page(base, f"Run {rid}", "".join(L), refresh=10 if running_job else None)


def candidate_outputs(base: str, rid: str, run_dir: Path, cp: dict) -> str:
    """The candidate's outputs, listed exactly like HOME's, under a CANDIDATE heading: the review packet first, the
    diff next, then A1-A5."""
    cpath = cand_paths(run_dir, cp)
    out = Path(cpath["out"])
    demo = (cp.get("approval") or {}).get("status") == "simulated"
    L = (['<h2 id="candidate">Interview candidate outputs (simulated approvals; separate from ADD02)</h2>',
          f'<p class="banner">{DEMO_CANDIDATE_BANNER}</p>'] if demo else
         ['<h2 id="candidate">CANDIDATE outputs (not approved; apart from the validated outputs)</h2>',
          f'<p class="banner">{CANDIDATE_BANNER}</p>', f"<p><b>{NOTHING_ACCEPTED}</b></p>"])
    rev = run_dir / "review"
    rows = []
    for f in ("index.html", "diff.md", "index.md", "diff.json", "outputs-before-after.json"):
        if (rev / f).is_file():
            rows.append(file_row(base, f"runs/{rid}/review", f, (rev / f).stat()))
    L.append("<h3>The review packet first, then the diff</h3>")
    L.append(table(FILE_HEAD, rows) if rows else '<p class="note">no review packet yet</p>')
    try:
        rel = out.resolve().relative_to(run_dir.resolve()).as_posix()
    except (OSError, ValueError):
        rel = "candidate/out"
    L.append("<h3>Candidate A1-A5</h3>")
    if walk(out):
        L.append(listing(base, f"runs/{rid}/{rel}", out, "INTERVIEW DEMO (simulated approvals)" if demo else "CANDIDATE (not approved)"))
    else:
        L.append('<p class="note">no candidate outputs yet (the outputs step builds them)</p>')
    return "".join(L)


def candidate_page(base: str, rid: str, run_dir: Path, cp: dict) -> str:
    return page(base, f"Candidate review: {rid}", candidate_outputs(base, rid, run_dir, cp)
                + f'<p><a href="{base}runs/{esc(rid)}">the run</a> · <a href="{base}stages?to=run:{esc(rid)}:'
                f'{esc(cp.get("addendum") or "")}">compare stages with this candidate</a></p>')


def starting_page(base: str, rid: str, job: dict) -> str:
    return page(base, f"Run {rid}", f'<p class="banner">{CANDIDATE_BANNER}</p><p class="lead">Starting: the job is '
                f"running; the run's checkpoint appears when its first step starts.</p><p>"
                + button(base, f"jobs/{job['id']}/stop", "Stop") + f' <a href="{base}jobs/{esc(job["id"])}">the job and '
                "its output</a></p><h3>Steps</h3><p class=\"note\">ingest: pending</p>",
                refresh=10 if job.get("status") == "running" else None)


# ---------------------------------------------------------------------------------------------- Jobs

KIND_WORDS = {"ingest": "rebuild the evidence (ingest)", "outputs": "rebuild A1-A5 (outputs)",
              "strict": "strict release check", "check-register": "check the register", "ai-run": "addendum run",
              "ai-resume": "resume an addendum run", "diff": "compare stages (diff)", "decision": "a decision"}


def job_needs(j: dict) -> str:
    if j["status"] == "running":
        return "Nothing yet: wait (the page refreshes)."
    if j["status"] == "finished":
        return "Nothing."
    if j["status"] == "interrupted":
        return "It ended while the panel was closed; run it again if needed."
    if j["status"] == "stopped":
        return "Stopped on request; run it again (or Resume the run) when ready."
    code = j.get("exit_code")
    if j.get("kind") in ("ai-run", "ai-resume"):
        return "Open the run: " + (AI_EXIT.get(code) or "read the output")
    if j.get("kind") == "strict" and code == 3:
        return "Expected while approvals are pending: decide the items, then run it again."
    return "Read its output: " + (meaning(j.get("kind", ""), code) or "it failed")


def job_row(base: str, j: dict) -> list[str]:
    code = j.get("exit_code")
    return [f'<a href="{base}jobs/{esc(j["id"])}">{esc(j["id"])}</a>', esc(KIND_WORDS.get(j.get("kind"), j.get("kind"))),
            esc(j.get("status")), esc(j.get("started")),
            esc(duration(j.get("started"), j.get("finished") if j.get("status") != "running" else None)),
            esc("" if code is None else code) + (f' <span class="note">{esc(meaning(j.get("kind", ""), code))}</span>'
                                                 if code is not None else ""),
            esc(job_needs(j)), f"<code>{esc(j.get('command'))}</code>"]


JOB_HEAD = ["Job", "What", "Status", "Started", "Duration", "Exit code", "What it needs from you",
            "Command (repeat it in a terminal)"]


def jobs_page(base: str, jobs: list[dict]) -> str:
    running = any(j["status"] == "running" for j in jobs)
    return page(base, "Jobs", '<p class="note">Every command the panel ran, newest first. Each is the command shown, '
                "run in a subprocess; its log is under <code>staging/panel/jobs/&lt;job&gt;/</code>.</p>"
                + table(JOB_HEAD, [job_row(base, j) for j in jobs]), refresh=10 if running else None)


def job_page(base: str, j: dict, log: str, cut: bool) -> str:
    L = [f'<p class="lead">{esc(KIND_WORDS.get(j.get("kind"), j.get("kind")))}: {esc(j["status"])}'
         + (f"; exit code {esc(j['exit_code'])}: {esc(meaning(j['kind'], j['exit_code']))}"
            if j.get("exit_code") is not None else "") + "</p>",
         f"<p>What it needs from you: {esc(job_needs(j))}</p>",
         f"<p>Started {esc(j.get('started'))}; finished {esc(j.get('finished') or '-')}; duration "
         f"{esc(duration(j.get('started'), j.get('finished') if j['status'] != 'running' else None))}</p>",
         f"<p>Command (repeat it in a terminal):</p><pre>{esc(j['command'])}</pre>"]
    meta = j.get("meta") or {}
    if meta.get("run_id"):
        L.append(f'<p>Run id: <b>{esc(meta["run_id"])}</b> · <a href="{base}runs/{esc(meta["run_id"])}">the run</a> · '
                 f'<a href="{base}runs/{esc(meta["run_id"])}/candidate">candidate outputs</a></p>')
    for k in ("original_name", "upload_sha256", "synthetic", "item", "decision", "reviewer"):
        if meta.get(k):
            L.append(f"<p>{esc(k.replace('_', ' '))}: {esc(meta[k])}</p>")
    if j.get("note"):
        L.append(f"<p>{esc(j['note'])}</p>")
    if j["status"] == "running":
        L.append(button(base, f"jobs/{j['id']}/stop", "Stop (interrupt; resume later)"))
    L.append(f"<h2>Output{' (last lines)' if cut else ''}</h2><pre>{esc(log)}</pre>")
    L.append(f'<p><a href="{base}file/jobs/{esc(j["id"])}/output.log">output.log (the whole log)</a></p>')
    return page(base, f"Job {j['id']}", "".join(L), refresh=10 if j["status"] == "running" else None)


# ---------------------------------------------------------------------------------------------- Decisions

def decision_commands(item: str, kind: str) -> list[str]:
    if kind == "reading":
        return [f"python -m tenderpack approve {shlex.quote(item)} --reviewer \"Your Name\" --notes \"...\""]
    return [f"python -m tenderpack accept {shlex.quote(item)} --reviewer \"Your Name\" --note \"...\"",
            f"python -m tenderpack reject {shlex.quote(item)} --reviewer \"Your Name\" --note \"what is wrong\""]


def decisions_page(base: str, pending: list[dict], decided: Counter, latest: dict) -> str:
    L = ['<p class="note">Only a person decides. The panel lists the items and the exact commands; it runs one only '
         "when you choose the decision, type your name and a reason and confirm. The engine binds the decision to the "
         "item's current content; any later change voids it.</p>"]
    L.append("<p>Decided or closed items (per the outputs): " + (esc(", ".join(f"{k} {s}: {n}" for (k, s), n in
                                                                          sorted(decided.items()))) or "none") + "</p>")
    rows = []
    for it in pending:
        lt = latest.get(it["id"])
        rows.append([esc(it["kind"]), f"<code>{esc(it['id'])}</code>", f'<span class="nw">{esc(it.get("status"))}</span>',
                     esc(_short(it.get("prompt") or "", 300)),
                     "<br>".join(f"<code>{esc(c)}</code>" for c in decision_commands(it["id"], it["kind"])),
                     esc(f"{lt.get('decision')} by {lt.get('reviewer')} ({lt.get('date') or lt.get('at') or ''})"
                         if lt else "none recorded"),
                     f'<a class="nw" href="{base}decisions/form?item={esc(it["id"])}">decide…</a>'])
    L.append(table(["Kind", "Item", "Status", "What is decided", "Commands", "Latest recorded decision", ""], rows))
    return page(base, "Decisions", "".join(L))


def decision_form(base: str, it: dict, errors: list[str] | None = None, values: dict | None = None) -> str:
    v = values or {}
    choices = ["approve"] if it["kind"] == "reading" else ["accept", "reject"]
    radios = " ".join(f'<label><input type="radio" name="decision" value="{c}"'
                      f'{" checked" if v.get("decision") == c else ""}> {c}</label>' for c in choices)
    L = [f"<p>{esc(it['kind'])} <code>{esc(it['id'])}</code>: {esc(it.get('status'))}</p>",
         f"<p>{esc(it.get('prompt') or '')}</p>"]
    if errors:
        L.append("<ul>" + "".join(f'<li class="bad">refused: {esc(e)}</li>' for e in errors) + "</ul>")
    L.append(f'<form method="post" action="{base}decisions/confirm"><input type="hidden" name="item" '
             f'value="{esc(it["id"])}"><fieldset><legend>Decision (none is chosen for you)</legend>{radios}</fieldset>'
             f'<p><label>Your name <input name="name" value="{esc(v.get("name", ""))}" required></label></p>'
             f'<p><label>Reason <textarea name="reason" rows="3" cols="70" required>{esc(v.get("reason", ""))}'
             "</textarea></label></p><button>Show the exact command</button></form>")
    return page(base, "Decide", "".join(L))


def decision_confirm(base: str, it: dict, decision: str, name: str, reason: str, command: str) -> str:
    hidden = "".join(f'<input type="hidden" name="{k}" value="{esc(x)}">' for k, x in
                     (("item", it["id"]), ("decision", decision), ("name", name), ("reason", reason)))
    return page(base, "Confirm the decision", f"<p>This command will run as a job, exactly:</p><pre>{esc(command)}</pre>"
                f'<form method="post" action="{base}decisions/run">{hidden}<p><label><input type="checkbox" '
                f'name="confirm" value="yes"> I, {esc(name)}, make this decision ({esc(decision)} '
                f"{esc(it['id'])})</label></p><button>Run this command</button></form>"
                f'<p><a href="{base}decisions">back</a></p>')


def message(base: str, heading: str, text: str, status_class: str = "bad") -> str:
    return page(base, heading, f'<p class="{status_class}">{esc(text)}</p>')


# ---------------------------------------------------------------------------------------------- quick review (s13)
# Session 13, part 4: the AI quick review (tenderpack/ai/quick_review.py). Its pages show the briefing under its label,
# the questions as a form (each answer recorded by a job against the exact question and evidence), the comparison
# with a run when one was made (headed "model agreement is not proof"), and the two timings side by side. Nothing on
# them approves, accepts or edits anything.

QR_HEAD = ["Quick review", "Addendum", "Route", "Status", "Started", "First briefing after", "Beside run"]


def _qr_label() -> str:
    from ..ai.quick_review import LABEL
    return LABEL


def _qr_kind() -> str:
    """Session 14 (W5): what a briefing is, shown beside its label everywhere it is rendered."""
    from ..ai.quick_review import KIND
    return KIND


def quick_reviews(staging: Path) -> list[tuple[str, Path]]:
    d = Path(staging) / "quick-review"
    return [(p.name, p) for p in sorted(d.iterdir(), reverse=True) if p.is_dir() and not p.name.startswith(".")] \
        if d.is_dir() else []


def _qr_row(base: str, qid: str, d: Path) -> list[str]:
    req = read_json(d / "request.json") or {}
    stt = read_json(d / "status.json") or {}
    t = read_json(d / "timing.json") or {}
    s = t.get("seconds_to_first_briefing")
    return [f'<a href="{base}quickreview/{esc(qid)}">{esc(qid)}</a>', esc(req.get("addendum")), esc(req.get("route")),
            esc(stt.get("status") or "running"), esc(req.get("created")), esc(f"{s} s" if s is not None else "-"),
            esc(req.get("for_run") or "-")]


def quick_review_box(base: str, rid: str, run_dir: Path, cp: dict) -> str:
    """The run page's quick-review box: start one on the run's PDF; the quick reviews started beside this run."""
    staging = Path(run_dir).parent.parent
    mine = [(q, d) for q, d in quick_reviews(staging) if (read_json(d / "request.json") or {}).get("for_run") == rid]
    rows = table(QR_HEAD, [_qr_row(base, q, d) for q, d in mine]) if mine else ""
    notes = []
    for nf in sorted((Path(run_dir) / "owner_answers").glob("*.yaml")) if (Path(run_dir) / "owner_answers").is_dir() \
            else []:
        try:
            import yaml
            notes += (yaml.safe_load(nf.read_text(encoding="utf-8")) or {}).get("notes") or []
        except (OSError, ValueError):
            continue
    if notes:
        from ..ai.answers import state_line                     # session 14 (W5): what the run did with each answer
        rows += ("<h3>Your answers offered to this run (PROPOSED notes; never a decision)</h3>" + table(
            ["Note", "Question", "Answer (kind; by, when)", "Offered after step", "Revalidation", "Taken by the run"],
            [[esc(n.get("id")), esc(n.get("question")),
              esc(f"{n.get('answer')} ({n.get('answer_kind') or 'judgment'}; {n.get('by')}, {n.get('recorded')})"),
              esc(n.get("offered_after")), esc((n.get("revalidation") or {}).get("state")),
              esc(state_line({"handoff": n.get("handoff") or {"state": "offered"},
                              "offers": [{"run": rid, "result": "offered"}]}))] for n in notes]))
    return (f'<section class="box"><h2>AI quick review (preliminary, lower priority)</h2>'
            f'<p class="banner">{esc(_qr_kind())}</p><p class="note">A separate, '
            "bounded AI reading of this run's PDF (ONE session, the read-only retrieval tools on the published "
            "workspace, never this run's proposals): a PRELIMINARY AI BRIEFING, unverified, to compare with this run "
            f"later. It never changes the run.</p><form method=\"post\" action=\"{base}runs/{esc(rid)}/quickreview\">"
            "<button>Start AI quick review (preliminary briefing)</button></form>" + rows + "</section>")


def quickreview_list(base: str, staging: Path) -> str:
    rows = [_qr_row(base, q, d) for q, d in quick_reviews(staging)]
    return page(base, "Quick reviews", f'<p class="banner">{esc(_qr_label())}</p><p class="banner">{esc(_qr_kind())}'
                '</p><p class="note">Start one from the '
                "New addendum box (HOME) or from a run's page.</p>" + table(QR_HEAD, rows))


def _tim(s) -> str:
    return "-" if s is None else f"{float(s):.1f} s ({float(s) / 60:.1f} min)"


def quickreview_page(base: str, qid: str, d: Path, runs: list[tuple[str, dict]], running_job: dict | None) -> str:
    from ..ai.quick_review import NOT_PROOF, preserved, run_timing
    label = _qr_label()
    req = read_json(d / "request.json") or {}
    stt = read_json(d / "status.json") or {}
    t = read_json(d / "timing.json") or {}
    b = read_json(d / "briefing.json")
    cmp = read_json(d / "comparison.json")
    L = [f'<p class="banner">{esc(label)}</p>', f'<p class="banner">{esc(_qr_kind())}</p>']     # session 14 (W5)
    L.append(f"<p>Addendum {esc(req.get('addendum'))} · route {esc(req.get('route'))} · started "
             f"{esc(req.get('created'))} · status <b>{esc(stt.get('status') or ('running' if running_job else 'unknown'))}"
             f"</b>" + (f" · {esc(stt.get('error'))}" if stt.get("error") else "") + "</p>")
    if running_job:
        L.append(f'<p class="lead">Running (lower priority, under nice): <a href="{base}jobs/{esc(running_job["id"])}">'
                 "the job and its output</a></p>")
    # ---- the two timings side by side
    rid = (cmp or {}).get("run", {}).get("run_id") or req.get("for_run")
    rcp = next((cp for r, cp in runs if r == rid), None) if rid else None
    rt = run_timing(rcp) if rcp else (cmp or {}).get("timings") or {
        "run_updated_a1_a5_s": None, "note": "no run linked yet (start it from a run's page, or compare with a run)"}
    L.append("<h2>Timings (measured separately)</h2>" + table(
        ["Time to the first briefing (this quick review)", "Time to the run's updated A1-A5 candidate"
         + (f" ({rid})" if rid else "")],
        [[esc(_tim(t.get("seconds_to_first_briefing"))) + f'<div class="note">{esc(t.get("first_useful_briefing") or t.get("note") or "")}</div>',
          esc(_tim(rt.get("run_updated_a1_a5_s"))) + f'<div class="note">{esc(rt.get("note"))}</div>']]))
    tok = t.get("tokens") or {}
    if tok:
        L.append(f'<p class="note">Tokens: {esc(tok.get("input_tokens"))} in / {esc(tok.get("output_tokens"))} out in '
                 f"{esc(tok.get('calls'))} call(s); budget {esc((t.get('budget') or {}).get('minutes'))} min, "
                 f"{esc((t.get('budget') or {}).get('max_tokens'))} tokens.</p>")
    links = [f'<a href="{base}file/quick-review/{esc(qid)}/{f}">{f}</a>' for f in
             ("briefing.md", "briefing.json", "timing.json", "comparison.md", "answers.yaml", "log.jsonl")
             if (d / f).is_file()]
    L.append("<p>Files: " + " · ".join(links) + "</p>")
    if b is None:
        L.append('<p class="note">No briefing yet (or none was written: see the status above).</p>')
        return page(base, f"Quick review {qid}", "".join(L), refresh=10 if running_job else None)
    pres = preserved(d)
    L.append(f"<p>Initial findings preserved as written (briefing.sha256): "
             f"{_okcell(pres['ok'], 'yes' if pres['ok'] else 'NO: ' + pres['why'])}</p>")
    # ---- the briefing
    L.append("<h2>Predicted changes (preliminary, unverified)</h2>" + table(
        ["Id", "Provision (page)", "Quotation (check)", "Target guess (check)", "Kind", "Deliverables", "Confidence",
         "Uncertainty"],
        [[f'<span class="nw">{esc(i["id"])}</span>', esc(f"{i['provision']} (p{i['page']})"),
          esc(f"“{i['quotation']}”") + f'<div class="note">{esc((i.get("checks") or {}).get("quotation"))}</div>',
          esc(i.get("target_unit_guess") or "none") + f'<div class="note">{esc((i.get("checks") or {}).get("target"))}'
          "</div>", f'<span class="nw">{esc(i["kind"])}</span>', esc(", ".join(i.get("deliverables") or [])),
          esc(i["confidence"]),
          esc(i["uncertainty_class"] + (f": {i['uncertainty']}" if i.get("uncertainty") else ""))]
         for i in b.get("items") or []]))
    # ---- questions as a form
    ans = {}
    try:
        import yaml
        for a in (yaml.safe_load((d / "answers.yaml").read_text(encoding="utf-8")) or {}).get("answers") or []:
            ans.setdefault(a.get("question_id"), []).append(a)
    except (OSError, ValueError, AttributeError):
        pass
    L.append("<h2>Questions for you</h2><p class=\"note\">Your answer is recorded with your name and the time against "
             "the exact question and the evidence it cites (answers.yaml beside the briefing); it never changes "
             "curation/. It reaches a run only at a safe checkpoint (before analysis, downstream or promotion), as a "
             "PROPOSED item: a fact only with evidence the program finds (else it is refused, with the reason), a "
             "judgment as your proposed judgment; never an approval (approvals stay in accept/reject).</p>")
    from ..ai.answers import state_line                         # session 14 (W5): each answer's state
    for q in b.get("questions") or []:
        ev = "".join(f"<li>page {esc(e.get('page'))}" + (f", {esc(e.get('unit_id'))}" if e.get("unit_id") else "")
                     + f": “{esc(e.get('quotation'))}” <span class=\"note\">({esc(c)})</span></li>"
                     for e, c in zip(q.get("evidence") or [], q.get("checks") or [""] * 99))
        done = "".join(f"<li><b>{esc(a.get('by'))}</b> at {esc(a.get('recorded'))} ({esc(a.get('kind') or 'judgment')}"
                       f"{', ' + str(len(a.get('answer_evidence') or [])) + ' cite(s)' if a.get('answer_evidence') else ''}"
                       f"): {esc(a.get('answer'))} <span class=\"note\">({esc(a.get('id'))}: {esc(state_line(a))})"
                       "</span></li>" for a in ans.get(q["id"], []))
        L.append(f'<fieldset><legend><b>{esc(q["id"])}</b> {esc(q["question"])}'
                 + (f' <span class="note">(decision owner: {esc(q.get("decision_owner"))})</span>'
                    if q.get("decision_owner") else "") + f"</legend><ul>{ev}</ul>"
                 + (f"<p>Recorded answers:</p><ul>{done}</ul>" if done else "")
                 + f'<form method="post" action="{base}quickreview/{esc(qid)}/answer">'
                 f'<input type="hidden" name="question" value="{esc(q["id"])}">'
                 f'<div class="line"><label>Your answer <textarea name="answer" rows="3" cols="80" required>'
                 f'</textarea></label></div>'
                 '<div class="line"><label>It is <select name="kind"><option value="judgment">my judgment (a proposal; '
                 'never an approval)</option><option value="fact">a fact (cite its evidence below)</option></select>'
                 '</label></div><div class="line"><label>Evidence, one per line: <code>page 3: the words</code> '
                 '(this addendum) or <code>VOL-I:6.1: the words</code> (the pack) <textarea name="evidence" rows="2" '
                 'cols="80"></textarea></label></div>'
                 f'<div class="line"><label>Your name <input name="name" size="30" '
                 f'required></label> <button>Record my answer</button></div></form></fieldset>')
    if not b.get("questions"):
        L.append('<p class="note">no question in this briefing</p>')
    calcs = b.get("unverified_calculations") or []
    L.append("<h2>Unverified calculations</h2>" + table(["Id", "What", "The model's figure (UNVERIFIED)", "Why unverified"],
                                                        [[esc(c["id"]), esc(c["what"]),
                                                          esc(c.get("model_result_unverified") or "none"),
                                                          esc(c["why_unverified"])] for c in calcs]))
    L.append("<h2>Not read</h2>" + table(["What", "Page", "Class", "Reason"], [
        [esc(n["what"]), esc(n.get("page") or ""), esc(n["uncertainty_class"]), esc(n["reason"])]
        for n in b.get("not_read") or []]))
    # ---- comparison with a run
    opts = "".join(f'<option value="{esc(r)}"{" selected" if r == rid else ""}>{esc(r)}</option>' for r, _ in runs)
    L.append(f"<h2>Comparison with a run</h2><p class=\"lead\">{esc(NOT_PROOF)}</p>")
    if runs:
        L.append(f'<form method="post" action="{base}quickreview/{esc(qid)}/compare"><select name="run">{opts}</select>'
                 " <button>Compare with this run</button></form>"
                 f'<form method="post" action="{base}quickreview/{esc(qid)}/offer"><select name="run">{opts}</select>'
                 ' <button>Offer my answers to this run</button> <span class="note">(only between phases: while a step '
                 "or batch runs, the answers are held; each becomes a PROPOSED note that the run takes at its next safe "
                 "checkpoint after the evidence checks and the staleness guard, re-asking the batches it concerns; "
                 "never a decision)</span></form>")
    if cmp:
        c = cmp.get("counts") or {}
        L.append(f"<p>Compared with run <b>{esc(cmp['run']['run_id'])}</b> on {esc(cmp.get('created'))}: "
                 + esc(", ".join(f"{k.replace('_', ' ')} {v}" for k, v in c.items())) + "</p>")
        L.append("<h3>Disagreements (for you to investigate; nothing was edited)</h3>" + table(
            ["Briefing", "Run", "Differences"],
            [[esc(f"{x['briefing']['id']} {x['briefing']['provision']} p{x['briefing']['page']} "
                  f"{x['briefing']['kind']} → {x['briefing']['target_unit_guess']}: “{x['briefing']['quotation']}”"),
              esc(f"{x['run']['id']} {x['run']['kind']} → {x['run'].get('target')} ({x['run'].get('status')}): "
                  + "; ".join(f"“{e.get('words')}”" for e in x["run"].get("evidence") or [])),
              esc("; ".join(x["differences"]))] for x in cmp.get("disagreements") or []]))
        L.append("<h3>Agreements (not proof)</h3>" + table(["Briefing", "Run", "Matched by"], [
            [esc(x["briefing"]["id"]), esc(x["run"]["id"]), esc(", ".join(x["matched_by"]))]
            for x in cmp.get("agreements") or []]))
        L.append(f"<p>In the briefing only: {esc(', '.join(x['id'] for x in cmp.get('briefing_only') or []) or 'none')}"
                 f"; in the run only: {len(cmp.get('run_only') or [])} item(s) (see comparison.md).</p>")
    else:
        L.append('<p class="note">not compared yet</p>')
    return page(base, f"Quick review {qid}", "".join(L), refresh=10 if running_job else None)


def interview_page(base: str, data: dict, target: dict, busy: bool = False, query: str = "") -> str:
    """All current decisions, including approvals; every edit binds the viewed version."""
    import json
    hidden = ''.join(f'<input type="hidden" name="{esc(k)}" value="{esc(v)}">' for k, v in target.items())
    body = '<p class="banner">INTERVIEW DEMO — approvals may be assumed. This is not an actual human review or tender release.</p>'
    body += f'<p>Stage {esc(data["stage"])} · {len(data["items"])} decisions. Expand an item to inspect evidence, edit its proposal, or change its decision. Edits rebuild outputs and preserve history.</p>'
    if busy:
        body += '<p class="banner">A run or rebuild is active. Decisions can be inspected; changes become available when it finishes.</p>'
    body += (f'<form method="get" action="{base}interview">{hidden}'
             f'<input id="decision-filter" name="q" value="{esc(query)}" '
             'placeholder="Find by ID, owner, requirement or status" style="width:75%"> '
             '<button>Search decisions</button></form>')
    matches = [it for it in data['items'] if query.casefold() in json.dumps(it, ensure_ascii=False, default=str).casefold()]
    if query:
        body += f'<p>{len(matches)} matching decisions</p>'
    for it in matches:
        from ..interview import planning_fields
        pretty = lambda x: esc(json.dumps(x, ensure_ascii=False, indent=2, default=str))
        disabled = ' disabled' if busy else ''
        body += f'<details class="demo-item"><summary><strong>{esc(it["id"])}</strong> · {esc(it["kind"])} · {esc(it["label"])}</summary>'
        fields = planning_fields(it)
        if fields:
            body += (f'<form method="post" action="{base}interview/apply">{hidden}'
                     f'<input type="hidden" name="item" value="{esc(it["id"])}">'
                     f'<input type="hidden" name="fingerprint" value="{esc(it["fingerprint"])}">'
                     '<p>Adjust a provisional planning assumption. Dates and resource loads are recalculated; no AI call is needed.</p>'
                     '<p><label>Planning field <select name="planning_field">')
            for field in fields:
                body += f'<option value="{esc(field["path"])}">{esc(field["label"])} · current {esc(field["value"])}</option>'
            body += ('</select></label></p><p><label>New value <input type="number" name="planning_value" min="0" step="any" required></label></p>'
                     '<p><label>Reason / revised basis <input name="reason" required maxlength="2000" style="width:75%"></label></p>'
                     f'<button name="action" value="planning"{disabled}>Update planning assumption and rebuild</button></form>')
        body += '<details><summary>Advanced structured edit and approval</summary>'
        body += f'<form method="post" action="{base}interview/apply">{hidden}<input type="hidden" name="item" value="{esc(it["id"])}"><input type="hidden" name="fingerprint" value="{esc(it["fingerprint"])}">'
        body += f'<p>Proposal (editable structured fields)</p><textarea name="value" rows="14" style="width:98%">{pretty(it["value"])}</textarea>'
        body += '<p><label>Reason for this change <input name="reason" required maxlength="2000" style="width:75%"></label></p>'
        for action, label in (("edit", "Edit proposal and rebuild"), ("accept", "Approve current proposal"), ("reject", "Reject current proposal")):
            if action not in it.get("actions", ["edit", "accept", "reject"]):
                continue
            body += f'<button name="action" value="{action}"{disabled}>{label}</button> '
        body += '</form><p>Editing creates a new proposal; approve it separately after reviewing the rebuilt result.</p></details>'
        body += f'<details><summary>Evidence and dependencies</summary><pre>{pretty(it["evidence"])}</pre></details>'
        body += f'<details><summary>Decision history ({len(it["history"])})</summary><pre>{pretty(it["history"])}</pre></details></details>'
    return page(base, 'All interview decisions', body)
