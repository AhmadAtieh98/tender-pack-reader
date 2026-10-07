"""The AI QUICK REVIEW (session 13, part 4): a separate, bounded, lower-priority AI reading of a new addendum, started
beside the main workflow run, for a PRELIMINARY AI BRIEFING. The owner: "give it ADD-03 and the relevant original
pack/ADD-02 context. it should independently predict changes, cite pages and quotations, identify affected deliverables,
explain uncertainties and ask focused questions ... it must not edit authoritative data, approve items or mark pipeline
work complete ... model agreement is not proof ... keep this pass short and lower priority so it doesn't starve the main
run. measure time to the first useful briefing separately from time to updated A1-A5."

    tenderpack ai quick-review ADD-NN --pdf PATH [--route host|anthropic|openrouter|ollama|recorded]
                                      [--budget-minutes N] [--max-tokens N] [--model M] [--cassette P] [--qr-id ID]
    tenderpack ai quick-review compare QR_ID RUN_ID|RUN_DIR
    tenderpack ai quick-review answer QR_ID --question Q1 --answer TEXT --by NAME
    tenderpack ai quick-review offer QR_ID RUN_ID|RUN_DIR
    tenderpack ai quick-review revalidate RUN_ID|RUN_DIR

run(): ONE bounded session (no batches, no critic) through the one request path (requests.converse on the recorded and
API routes, with offline.check_route through providers.make; requests.ask_host in ONE hostsession.AnswerSession on the
host route). Its system prompt is policy.compose("quick_review", route) (tenderpack/ai/policy/70_quick_review.md after the
shared sections); its tools are policy.tools("quick_review"): search_evidence, get_unit, get_group, get_crop and
compare_state only (no simulate_amendment, no calculate, no validation, no submission tool), over the PUBLISHED
workspace (the validated evidence build and pack: the ADD-02 stage today), never a run's staging: an evidence build or
pack under the staging folder is refused, and nothing of a run (proposals, candidate, packet) is read or given. The
packet carries the addendum's text page by page (PyMuPDF) and, on a route that reports image input, the rendered images
of the pages that carry image regions (or no text layer); a page image not attached is listed under `not_read` as a
software limitation (the host route receives its packet as text, so the images are never attached there).

Lower priority: one quick review at a time (SessionLock), a short budget (--budget-minutes: the session's wall clock;
default 10), a token cap (--max-tokens: input, with output capped at a quarter of it), at most MAX_TURNS calls, a rate
limit never waited out (deferred, exit 5: start it again later), no addendum lock (the main run holds it; the quick
review writes nothing it protects), and the process niced (`--nice`, default 10; the panel starts it under `nice`).

Output: <staging>/quick-review/<qr id>/
    request.json      what was given: the PDF (sha256), the workspace (evidence, pack, stage, state identity), the tools,
                      the budget, the page images attached, and `main_run_inputs_read: []`
    briefing.json     LABEL; predicted changes [provision, page, quotation, target unit guess, kind, deliverables
                      affected, rows, confidence, uncertainty class], questions [id, question, evidence], unverified
                      calculations, what was not read; beside each, the program's CHECKS (is the quotation verbatim on
                      that page of the addendum's text layer; is the target guess a unit of the published workspace),
                      labelled as checks, never as a validation of the reading
    briefing.md       the same, headed "# " + LABEL
    briefing.sha256   the initial findings preserved: sha256 of briefing.json and briefing.md (both made read-only);
                      later steps never edit them, and preserved() says whether they still match
    timing.json       start, first_useful_briefing (the moment a briefing with at least one item or question was
                      written), end, the seconds, the tokens; the run's own time to its updated A1-A5 candidate is read
                      from its checkpoint by compare() and the panel, never mixed with this one
    log.jsonl         the request log (also worklog/model_calls/<qr id>.jsonl)
    comparison.json/.md   compare(): headed NOT_PROOF
    answers.yaml      record_answer(): the owner's answers against the exact question text and evidence

compare(): the briefing's predicted changes matched one to one with the run's analysis items (the combined set) by
provision, target unit and quoted words; agreements, disagreements (with the differences and the evidence of each side)
and one-sided items. A disagreement is a list for a person, never an edit: nothing of the run or of curation/ changes.

Answers and safe checkpoints: record_answer() stores the owner's answer (name, time) against the exact question and its
evidence; it never changes curation/. offer_answers() offers the recorded answers to a run ONLY between phases: while a
step or a batch of the run is running, every answer is HELD (the reason recorded); between steps each becomes a PROPOSED
note in <run>/owner_answers/<qr id>.yaml (review pending a person), its evidence checked verbatim against the run's
addendum PDF and its staleness fingerprint recorded (the run's combined set, downstream set and candidate curation);
revalidate_offers() marks a note STALE when the run changed after it was offered. A note is never a decision; the
workflow does not read these notes by itself (a person carries one into the review).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import secrets
import socket
import time
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..util import ROOT

PHASE = "quick_review"
TASK = "quick_review_briefing"
SUBDIR = "quick-review"
LABEL = ("PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations "
         "unchecked")
NOT_PROOF = "model agreement is not proof: every item is verified only by the validators and a person"
ROUTES = ("recorded", "host", "anthropic", "openrouter", "ollama")
DEFAULT_BUDGET_MIN = 10.0
DEFAULT_MAX_TOKENS = 60000
MAX_TURNS = 12
NICE = 10
QR_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")
ADDENDUM = re.compile(r"^ADD-\d{2}$")
EXIT = {"briefed": 0, "failed": 1, "refused": 2, "deferred": 5}
# honest status per route (`tenderpack ai routes`): where the quick review has been exercised
ROUTE_STATUS = {
    "recorded": "tested (tests only: hand-written cassettes; not a live model)",
    "host": "built, untested live: one Claude Code answer session with the retrieval tools; only a fake host CLI has "
            "run it (tests)",
    "anthropic": "built, untested live: the same request path as the workflow (requests.converse); recorded responses "
                 "only",
    "openrouter": "built, untested live: the same request path as the workflow (requests.converse); recorded responses "
                  "only",
    "ollama": "built, untested live: the same request path (local); no real local model has run it",
    "codex": "not offered: the quick review starts no Codex session",
}


class QuickReviewError(ValueError):
    """Refused before any call (bad input, a run's staging as the workspace, another quick review running), or a
    briefing that cannot be used as it stands."""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _secs(a: str | None, b: str | None) -> float | None:
    try:
        f = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")          # noqa: E731
        return round((f(b) - f(a)).total_seconds(), 1)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------------------------- the answer schema

class _M(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Cite(_M):
    page: int = Field(ge=1, description="the addendum page the words are on")
    quotation: str = Field(min_length=1, description="the words, copied verbatim")
    unit_id: str | None = Field(None, description="the unit id when the words are quoted from the pack (a tool result)")


class PredictedChange(_M):
    id: str = Field(min_length=1, max_length=80)
    provision: str = Field(min_length=1, description="the provision as printed: its number or heading")
    page: int = Field(ge=1)
    quotation: str = Field(min_length=1, description="verbatim from that page of the addendum")
    target_unit_guess: str | None = Field(None, description="a unit id at previous_stage (a guess), or null")
    target_quotation: str | None = Field(None, description="the target's words at previous_stage, from a tool result")
    kind: Literal["replace", "insert", "delete", "annotate", "status", "no_effect", "unclear"]
    deliverables: list[Literal["A1", "A2", "A3", "A4", "A5"]] = Field(default_factory=list)
    rows: list[str] = Field(default_factory=list, description="A1 rows, A5 activities or units it would touch")
    confidence: Literal["low", "medium", "high"]
    uncertainty_class: Literal["none", "software limitation", "missing evidence", "genuine ambiguity"] = "none"
    uncertainty: str | None = None
    propagation: list[str] = Field(default_factory=list, description="what depends on the target")

    @model_validator(mode="after")
    def _reason(self):
        if self.uncertainty_class != "none" and not (self.uncertainty or "").strip():
            raise ValueError("an uncertainty class other than none needs its reason in `uncertainty`")
        return self


class Question(_M):
    id: str = Field(min_length=1, max_length=40)
    question: str = Field(min_length=1)
    evidence: list[Cite] = Field(min_length=1)
    decision_owner: str | None = None
    why: str | None = None


class Calculation(_M):
    id: str = Field(min_length=1, max_length=40)
    what: str = Field(min_length=1)
    inputs: list[Cite] = Field(min_length=1)
    model_result_unverified: str | None = None
    why_unverified: str = Field(min_length=1)


class NotRead(_M):
    what: str = Field(min_length=1)
    page: int | None = None
    uncertainty_class: Literal["software limitation", "missing evidence"]
    reason: str = Field(min_length=1)


class Briefing(_M):
    addendum: str
    items: list[PredictedChange] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)
    unverified_calculations: list[Calculation] = Field(default_factory=list)
    not_read: list[NotRead] = Field(default_factory=list)
    model_rationale: str | None = None


def answer_schema() -> dict:
    return Briefing.model_json_schema()


def parse(data: dict, fields: dict | None = None, overwrites: list | None = None) -> dict:
    """The strict parse of an answer (the request layer's TaskSpec.parse): the briefing as data. A pydantic
    ValidationError goes back to the request layer (one bounded re-ask; an item still failing its schema is set aside)."""
    if not isinstance(data, dict):
        raise QuickReviewError("the quick-review answer must be a JSON object")
    return Briefing.model_validate(data).model_dump(mode="json")


# ---------------------------------------------------------------------------------------------- the addendum

def read_pdf(pdf: Path, out_dir: Path | None = None, dpi: int = 110) -> dict:
    """The addendum page by page: its text layer, the image regions (their rectangles), and, in `out_dir`, a PNG of
    every page with an image region or no usable text layer (the page images a route with image input receives)."""
    import pymupdf
    pdf = Path(pdf)
    doc = pymupdf.open(pdf)
    pages, images = [], []
    for p in doc:
        n = p.number + 1
        text = p.get_text("text") or ""
        rects = []
        for img in p.get_images(full=True):
            for r in p.get_image_rects(img[0]):
                if r.width * r.height >= 0.01 * p.rect.width * p.rect.height:   # a logo or a dot is not a region
                    rects.append([round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1)])
        why = "an image region" if rects else ("no usable text layer" if len(text.strip()) < 40 else None)
        pages.append({"page": n, "text": text.strip(), "characters": len(text.strip()), "image_regions": rects})
        if why and out_dir is not None:
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            f = Path(out_dir) / f"page-{n}.png"
            p.get_pixmap(dpi=dpi).save(str(f))
            images.append({"page": n, "path": str(f), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                           "media_type": "image/png", "why": why})
    return {"pages": pages, "images": images, "page_count": len(pages),
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()}


_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def _norm(s: str) -> str:
    return " ".join(str(s or "").translate(_QUOTES).split())


def _words(s: str) -> list[str]:
    return re.findall(r"\w+", _norm(s).lower())


def quote_check(quote: str, pages: list[dict], page: int | None) -> str:
    """Whether a quotation's words are on the page named, in the addendum's text layer (a CHECK, not a validation)."""
    def on(p):
        t = _norm(p["text"])
        q = _norm(quote)
        if q and q in t:
            return "verbatim"
        qw, tw = _words(quote), _norm(p["text"]).split()
        # the words in order, allowing short interleaved marks of the page (a watermark's letters) between them
        toks = [re.sub(r"\W", "", w).lower() for w in tw]
        i = 0
        for tok, raw in zip(toks, tw):
            if i < len(qw) and tok == qw[i]:
                i += 1
            elif i and not (len(raw) <= 3 and raw.isupper()) and tok:
                i = 1 if qw and tok == qw[0] else 0
        return "verbatim apart from interleaved page marks" if qw and i == len(qw) else None
    by = {p["page"]: p for p in pages}
    if page in by:
        r = on(by[page])
        if r:
            return f"{r} on page {page} of the addendum's text layer"
        if by[page]["image_regions"] and by[page]["characters"] < 200:
            return f"page {page} is an image page: not checkable against the text layer (unchecked)"
    other = [n for n, p in by.items() if n != page and on(p)]
    if other:
        return f"NOT on page {page}; found on page {other[0]} of the addendum's text layer"
    return f"NOT FOUND on page {page} of the addendum's text layer: treat the quotation as unverified"


# ---------------------------------------------------------------------------------------------- locks and files

class SessionLock:
    """One quick review at a time (lower priority than the main run): <staging>/quick-review/.session.lock."""

    def __init__(self, staging: Path):
        self.path = Path(staging) / SUBDIR / ".session.lock"
        self.token = secrets.token_hex(8)

    def acquire(self) -> "SessionLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        info = {"pid": os.getpid(), "host": socket.gethostname(), "created": _now(), "token": self.token}
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                cur = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cur = {}
            alive = True
            if cur.get("host") == socket.gethostname() and cur.get("pid"):
                try:
                    os.kill(int(cur["pid"]), 0)
                except ProcessLookupError:
                    alive = False
                except (PermissionError, ValueError):
                    pass
            if not cur or not alive:
                self.path.unlink(missing_ok=True)
                return self.acquire()
            raise QuickReviewError(f"one quick review at a time: process {cur.get('pid')} started one at "
                                   f"{cur.get('created')}; wait for it (it is bounded) or stop it") from None
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(info, fh)
        return self

    def release(self) -> None:
        try:
            if json.loads(self.path.read_text(encoding="utf-8")).get("token") == self.token:
                self.path.unlink(missing_ok=True)
        except (OSError, ValueError):
            pass


def _write(p: Path, text: str) -> None:
    tmp = p.with_name(f".{p.name}.{secrets.token_hex(3)}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def _jdump(x) -> str:
    return json.dumps(x, ensure_ascii=False, indent=1, default=str) + "\n"


PRESERVED = ("briefing.json", "briefing.md")


def preserved(d: Path) -> dict:
    """Whether the initial findings are as written (briefing.sha256): {ok, files: {name: (recorded, now)}, why}."""
    d = Path(d)
    rec = {}
    try:
        for line in (d / "briefing.sha256").read_text(encoding="utf-8").splitlines():
            if "  " in line:
                sha, name = line.split("  ", 1)
                rec[name.strip()] = sha.strip()
    except OSError:
        return {"ok": False, "files": {}, "why": "no briefing.sha256 (no briefing was written)"}
    files = {}
    for name in PRESERVED:
        try:
            now = hashlib.sha256((d / name).read_bytes()).hexdigest()
        except OSError:
            now = None
        files[name] = (rec.get(name), now)
    bad = [n for n, (a, b) in files.items() if not a or a != b]
    return {"ok": not bad, "files": files,
            "why": "" if not bad else f"{', '.join(bad)} changed after the briefing was written (or is missing)"}


def qr_dir(staging: Path, qr_id: str) -> Path:
    if not QR_ID.match(qr_id or "") or ".." in qr_id:
        raise QuickReviewError(f"invalid quick-review id {qr_id!r}")
    return Path(staging) / SUBDIR / qr_id


def load(d: Path) -> dict:
    return json.loads((Path(d) / "briefing.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------------- run

def _published(p: Path, staging: Path) -> None:
    p = Path(p).resolve()
    parts = p.parts
    if p.is_relative_to(staging) or any(parts[i] == "runs" and i + 2 < len(parts) and parts[i + 2] == "candidate"
                                        for i in range(len(parts))):
        raise QuickReviewError(f"the quick review reads the published workspace (the validated evidence build and "
                               f"pack), never a run's staging: {p}")


def _program_checks(b: dict, pages: list[dict], ws, stage: str) -> dict:
    units = ws.units_by_id
    for it in b["items"]:
        t = it.get("target_unit_guess")
        it["checks"] = {
            "quotation": quote_check(it["quotation"], pages, it["page"]),
            "target": ("no target guessed" if not t else
                       f"a unit of the {stage} workspace (the guess itself is unchecked)" if t in units else
                       f"NOT a unit of the {stage} workspace: the guess names nothing the pack holds"),
            "note": "the program's checks of the words and the id; the reading itself is unverified"}
    for q in b["questions"]:
        q["checks"] = [quote_check(e["quotation"], pages, e["page"]) if not e.get("unit_id") else
                       (f"quoted from {e['unit_id']} (a unit of the {stage} workspace; words unchecked)"
                        if e["unit_id"] in units else f"NOT a unit of the {stage} workspace: {e['unit_id']}")
                       for e in q["evidence"]]
    for c in b["unverified_calculations"]:
        c["checks"] = [quote_check(e["quotation"], pages, e["page"]) for e in c["inputs"]]
        c["status"] = "unverified: no calculation was run or checked"
    return b


def render_md(b: dict) -> str:
    L = [f"# {LABEL}", "",
         f"Quick review `{b['qr_id']}` of {b['addendum']} (PDF sha256 `{b['pdf']['sha256'][:16]}…`), read against the "
         f"published {b['workspace']['stage']} workspace; route {b['route']}, model {b.get('model_reported') or b.get('model_requested') or 'as the route reports'}; "
         f"written {b['created']}.",
         "", "Nothing here edits curation/, approves an item or marks the main workflow's work complete. Each item "
         "is a prediction by a model; the program checked only whether the quoted words are on the page named and "
         "whether a target id exists. Compare it with a run: `tenderpack ai quick-review compare "
         f"{b['qr_id']} <run id>` (model agreement is not proof).", "", "## Predicted changes", ""]
    for it in b["items"]:
        L += [f"### {it['id']}: provision {it['provision']} (page {it['page']}): {it['kind']}, confidence "
              f"{it['confidence']}",
              f"- quotation: “{it['quotation']}” ({it['checks']['quotation']})",
              f"- target guess: {it.get('target_unit_guess') or 'none'} ({it['checks']['target']})"
              + (f"; its words at the previous stage: “{it['target_quotation']}”" if it.get("target_quotation") else ""),
              f"- deliverables affected: {', '.join(it['deliverables']) or 'none named'}"
              + (f"; rows/activities: {', '.join(it['rows'])}" if it.get("rows") else ""),
              f"- uncertainty: {it['uncertainty_class']}" + (f": {it['uncertainty']}" if it.get("uncertainty") else "")]
        if it.get("propagation"):
            L.append(f"- what depends on it: {'; '.join(it['propagation'])}")
        L.append("")
    if not b["items"]:
        L += ["(none predicted)", ""]
    L += ["## Questions for a person (answer them on the panel's Quick review page)", ""]
    for q in b["questions"]:
        L.append(f"- **{q['id']}** {q['question']}" + (f" (decision owner: {q['decision_owner']})"
                                                       if q.get("decision_owner") else ""))
        for e, c in zip(q["evidence"], q.get("checks") or []):
            L.append(f"  - page {e['page']}" + (f", {e['unit_id']}" if e.get("unit_id") else "")
                     + f": “{e['quotation']}” ({c})")
    if not b["questions"]:
        L.append("(none)")
    L += ["", "## Unverified calculations (unchecked until the workflow's tools and a person check them)", ""]
    for c in b["unverified_calculations"]:
        L.append(f"- **{c['id']}** {c['what']}: the model's figure (UNVERIFIED): "
                 f"{c.get('model_result_unverified') or 'none given'}; why unverified: {c['why_unverified']}")
        for e, ch in zip(c["inputs"], c.get("checks") or []):
            L.append(f"  - input, page {e['page']}: “{e['quotation']}” ({ch})")
    if not b["unverified_calculations"]:
        L.append("(none)")
    L += ["", "## Not read", ""]
    for n in b["not_read"]:
        L.append(f"- {n['what']}" + (f" (page {n['page']})" if n.get("page") else "")
                 + f": {n['uncertainty_class']}: {n['reason']}")
    if not b["not_read"]:
        L.append("(nothing reported)")
    if b.get("model_rationale"):
        L += ["", "## The model's own account of what it read", "", b["model_rationale"]]
    return "\n".join(L).rstrip() + "\n"


def run(addendum: str, pdf: Path, *, route: str = "host", evidence: Path | None = None, pack: Path | None = None,
        staging: Path | None = None, worklog: Path | None = None, ai_config: Path | None = None,
        model: str | None = None, cassette: Path | None = None, budget_minutes: float = DEFAULT_BUDGET_MIN,
        max_tokens: int = DEFAULT_MAX_TOKENS, qr_id: str | None = None, offline: bool = False, runner=None,
        claude_bin: str | None = None, for_run: str | None = None, echo=None) -> dict:
    """One quick review (see the module docstring). Returns {status, exit_code, qr_id, dir, ...}. Raises
    QuickReviewError / offline.OfflineError / budget.Refused when refused before anything is written."""
    from . import budget as B
    from . import config as C
    from . import offline as OFF
    from . import requests as R
    from .runlog import RunLog
    from .tools import Workspace
    say = echo or (lambda *a: None)
    if not ADDENDUM.match(addendum or ""):
        raise QuickReviewError(f"the addendum id must look like ADD-NN, not {addendum!r}")
    if route not in ROUTES:
        raise QuickReviewError(f"no route {route!r} ({', '.join(ROUTES)})")
    cfg = C.load(Path(ai_config) if ai_config else None)
    OFF.activate(cfg, OFF.requested(cfg, offline))
    OFF.check_route(cfg, route, "the quick review")               # offline mode: before any file, process or call
    pdf = Path(pdf)
    if not pdf.is_file() or pdf.read_bytes()[:5] != b"%PDF-":
        raise QuickReviewError(f"{pdf}: not a PDF")
    budget_minutes, max_tokens = float(budget_minutes), int(max_tokens)
    if not (0 < budget_minutes <= 60) or not (1000 <= max_tokens <= 400000):
        raise QuickReviewError("a quick review is short: --budget-minutes in (0, 60], --max-tokens in [1000, 400000]")
    evidence = Path(evidence or ROOT / "build").resolve()
    pack = Path(pack or ROOT / "config/pack.yaml").resolve()
    st0 = Path(staging or ROOT / "staging/ai").absolute().resolve()
    _published(evidence, st0)                                     # first: a run's staging is named as such
    _published(pack, st0)
    st = B.safe_staging(st0, ROOT, evidence)
    lock = SessionLock(st).acquire()
    try:
        qr_id = qr_id or f"{addendum}-qr-{route}-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(2)}"
        d = qr_dir(st, qr_id)
        if d.exists():
            raise QuickReviewError(f"quick review {qr_id} exists already ({d}); a briefing is never rewritten")
        d.mkdir(parents=True)
        return _run(addendum, pdf, route, cfg, d, qr_id, evidence, pack, st, Path(worklog or ROOT / "worklog/model_calls"),
                    ai_config, model, cassette, budget_minutes, max_tokens, runner, claude_bin, for_run, say, B, C, R,
                    RunLog, Workspace)
    finally:
        lock.release()


def _run(addendum, pdf, route, cfg, d, qr_id, evidence, pack, st, worklog, ai_config, model, cassette, budget_minutes,
         max_tokens, runner, claude_bin, for_run, say, B, C, R, RunLog, Workspace) -> dict:
    from . import policy as P
    start, t0 = _now(), time.monotonic()
    ws = Workspace(evidence, pack, ROOT, d, worklog, Path(ai_config) if ai_config else None)
    ws.refresh()
    ident = ws.identity()
    stage = ident.validated_stage
    rd = read_pdf(pdf, d / "pages")
    tools = list(P.tools(PHASE, "api"))
    host = route == "host"
    rcfg = C.route(cfg, route)
    model_req = None if host else C.phase_model(rcfg, route, PHASE, model)
    prov = None
    images_ok = False
    if not host:
        from .providers import make
        from .providers.base import ProviderError
        prov = make(route, model_req, cfg, cassette)               # offline.check_route again, inside make
        try:
            images_ok = prov.capabilities().images is True
        except ProviderError:
            images_ok = False                                       # the request layer refuses it with the reason
    attached = rd["images"] if images_ok else []
    not_attached = [] if images_ok else [
        {"page": i["page"], "reason": ("software limitation: the host route receives its packet as text; the page "
                                       "images of a new addendum are not attached there" if host else
                                       "software limitation: the route does not report image input")}
        for i in rd["images"]]
    budget = {"minutes": budget_minutes, "max_tokens": max_tokens, "max_turns": MAX_TURNS, "sessions": 1,
              "nice": "the panel starts the command under `nice -n 10`; the command lowers its own priority (--nice)"}
    packet = {"task": TASK, "label": LABEL, "addendum": addendum, "previous_stage": stage,
              "note": ("A separate, bounded quick review beside the main workflow: the workflow's proposals, candidate "
                       "and packets are not given here and are not to be asked for. The tools read the published "
                       f"workspace at {stage}."),
              "pages": [{"page": p["page"], "text": p["text"], "image_regions": p["image_regions"]} for p in rd["pages"]],
              "images_attached": [i["page"] for i in attached], "images_not_attached": not_attached,
              "tools": tools, "budget": {k: budget[k] for k in ("minutes", "max_tokens", "max_turns")},
              "state": ident.model_dump(mode="json"), "schema": answer_schema()}
    request = {"qr_id": qr_id, "addendum": addendum, "route": route, "model_requested": model_req, "created": start,
               "label": LABEL, "for_run": for_run,
               "pdf": {"path": str(pdf), "sha256": rd["sha256"], "pages": rd["page_count"]},
               "workspace": {"evidence": str(evidence), "pack": str(pack), "stage": stage,
                             "identity": ident.model_dump(mode="json"),
                             "note": "the published workspace (the validated state); never a run's staging"},
               "tools": tools, "budget": budget,
               "images": [{k: i[k] for k in ("page", "sha256", "why")} for i in attached],
               "images_not_attached": not_attached, "main_run_inputs_read": [],
               "session": {"sessions": 1, "batches": 0, "critic": False}}
    _write(d / "request.json", _jdump(request))
    log = RunLog(qr_id, [Path(worklog) / f"{qr_id}.jsonl", d / "log.jsonl"])
    log.event("start", phase=PHASE, route=route, model_requested=model_req, addendum=addendum, label=LABEL,
              workspace=request["workspace"]["evidence"], stage=stage, tools=tools, budget=budget,
              note="ONE bounded session; no batches, no critic; nothing approved, nothing written outside this folder")
    say(f"quick review {qr_id}: {addendum} on the {route} route, {budget_minutes:g} min, {max_tokens} tokens at most")
    pol = R.FailurePolicy.from_cfg(cfg)
    pol.max_tries, pol.honour_reset_up_to_s = 0, 0.0              # lower priority: a rate limit is never waited out
    pol.provider_retries, pol.host_retries = min(pol.provider_retries, 1), 0
    fields = {"run_id": qr_id, "created": start, "route": route, "provider": route, "model_requested": model_req,
              "model_reported": None, "task": TASK}
    status, error, out, exc = "briefed", None, None, None
    try:
        if host:
            from . import hostsession as HS
            kw = {"runner": runner} if runner is not None else {}
            # no addendum lock (run_lock=True: never taken here): the main run holds it, and the quick review writes
            # nothing it protects; the session's MCP server offers exactly the retrieval tools over the published build
            sess = HS.AnswerSession(ws, cfg, phase=PHASE, model=model, max_turns=MAX_TURNS,
                                    timeout_s=budget_minutes * 60, claude_bin=claude_bin, run_lock=True, **kw)
            pol.repairs = 0                                         # one session at most: no repair session
            sp = R.spec(PHASE, system=sess.system_prompt(), cfg=cfg)
            out = R.ask_host(sp, sess, packet, cfg=cfg, policy=pol, log=log, fields=fields, cwd=d,
                             settings=R.settings_for(cfg, route), runner=runner)
        else:
            sp = R.spec(PHASE, route="api", cfg=cfg)
            caps = dict(C.caps(cfg, route, {}))
            price = B.price_for(cfg, prov.model)
            B.check_startable(route, rcfg, caps, price)            # a paid route needs the OWNER's caps first
            caps["max_calls"] = min(int(caps.get("max_calls") or MAX_TURNS), MAX_TURNS)
            caps["max_input_tokens"] = min(int(caps.get("max_input_tokens") or max_tokens), max_tokens)
            out_cap = max(1000, max_tokens // 4)
            caps["max_output_tokens"] = min(int(caps.get("max_output_tokens") or out_cap), out_cap)
            caps["max_tokens_per_call"] = min(int(caps.get("max_tokens_per_call") or 8000), caps["max_output_tokens"])
            caps["timeout_s"] = min(float(caps.get("timeout_s") or budget_minutes * 60), budget_minutes * 60)
            out = R.converse(sp, prov, packet, ws=ws, route=route, caps_=caps, price=price, policy=pol, log=log,
                             staging=st, run_id=qr_id, fields={**fields, "provider": prov.name}, images=[
                                 {"type": "image", "path": i["path"], "sha256": i["sha256"],
                                  "media_type": i["media_type"]} for i in attached],
                             settings=R.settings_for(cfg, route), enforce_output_estimate=False)
    except (R.CapabilityRefused, R.TooLarge, B.Refused) as e:
        status, error, exc = "refused", str(e), e
    except R.RateLimited as e:
        status, error, exc = "deferred", f"{e.message}; the quick review is lower priority: start it again later", e
    except (R.ProviderFailed, R.Malformed, R.ContextExhausted) as e:
        status, error, exc = "failed", e.message, e
    except B.BudgetExhausted as e:
        status, error, exc = "failed", f"budget exhausted: {e}", e
    usage = (getattr(out, "usage", None) or getattr(getattr(exc, "outcome", None), "usage", None) or {})
    first, t_first = None, None
    if status == "briefed":
        b = dict(out.answer)
        b["not_read"] = list(b.get("not_read") or []) + [
            {"what": f"the image of page {x['page']}", "page": x["page"], "uncertainty_class": "software limitation",
             "reason": x["reason"]} for x in not_attached]
        b = _program_checks(b, rd["pages"], ws, stage)
        hs = (out.host_sessions or [{}])[0] if host else {}
        rec = {"label": LABEL, "qr_id": qr_id, "created": _now(), "addendum": addendum, "route": route,
               "model_requested": model_req if not host else (model or "the host CLI's default"),
               "model_reported": out.model_reported, "pdf": request["pdf"],
               "workspace": {k: request["workspace"][k] for k in ("evidence", "pack", "stage")},
               "tools_offered": tools, "main_run_inputs_read": [], "session": request["session"],
               "malformed_items_set_aside": out.malformed_items, "notices": out.notices,
               "host_session": hs or None, **b,
               "status_of_everything_here": "PRELIMINARY: unverified; nothing approved, accepted, validated or complete"}
        _write(d / "briefing.json", _jdump(rec))
        if rec["items"] or rec["questions"]:
            first, t_first = _now(), time.monotonic()
        _write(d / "briefing.md", render_md(rec))
        _write(d / "briefing.sha256", "".join(f"{hashlib.sha256((d / n).read_bytes()).hexdigest()}  {n}\n"
                                              for n in PRESERVED))
        for n in PRESERVED:
            os.chmod(d / n, 0o444)                                 # the initial findings: never edited later
    end = _now()
    tok = {"calls": int(usage.get("calls") or 0), "input_tokens": int(usage.get("input_tokens") or 0),
           "output_tokens": int(usage.get("output_tokens") or 0), "cost_usd": usage.get("cost_usd"),
           "cost_basis": usage.get("cost_basis") or ("the host's own plan" if host else None)}
    timing = {"qr_id": qr_id, "status": status, "start": start, "first_useful_briefing": first, "end": end,
              "seconds_to_first_briefing": round(t_first - t0, 1) if t_first is not None else None,
              "seconds_total": round(time.monotonic() - t0, 1), "tokens": tok, "budget": budget,
              "measures": "the time from the start of this quick review to its first useful briefing (a briefing with "
                          "at least one predicted change or question); the main run's time to its updated A1-A5 "
                          "candidate is measured separately, from its own checkpoint",
              "note": None if first else ("no useful briefing: " + (error or "the briefing has no item and no question"))}
    _write(d / "timing.json", _jdump(timing))
    _write(d / "status.json", _jdump({"qr_id": qr_id, "status": status, "error": error, "label": LABEL,
                                      "for_run": for_run}))
    log.event("end", phase=PHASE, status=status, error=error, timing=timing)
    return {"status": status, "exit_code": EXIT[status], "qr_id": qr_id, "dir": str(d), "error": error,
            "timing": timing, "label": LABEL}


# ---------------------------------------------------------------------------------------------- compare

STEPS_ORDER = ("ingest", "readings", "analysis", "validation", "downstream", "downstream_validation", "critic",
               "promotion", "pin", "check_register", "outputs", "diff", "review")


def run_dir(ref: str, staging: Path) -> Path:
    """A run's folder: <staging>/runs/<id>, or a folder holding a run's checkpoint.json (a recorded rehearsal)."""
    if RUN_ID.match(ref or "") and (Path(staging) / "runs" / ref / "checkpoint.json").is_file():
        return Path(staging) / "runs" / ref
    p = Path(ref)
    if p.is_dir() and (p / "checkpoint.json").is_file():
        return p
    raise QuickReviewError(f"no run {ref!r} (neither {Path(staging) / 'runs' / str(ref)} nor a folder with a "
                           "checkpoint.json)")


def _checkpoint(rd: Path) -> dict:
    return json.loads((Path(rd) / "checkpoint.json").read_text(encoding="utf-8"))


def _combined_path(rd: Path, cp: dict) -> Path | None:
    rid = cp.get("run_id") or Path(rd).name
    for p in (Path(rd) / "ai" / f"{rid}-combined" / "proposals.yaml",
              Path(rd) / "proposals" / f"{rid}-combined" / "proposals.yaml"):
        if p.is_file():
            return p
    return None


def _run_kind(it: dict) -> str:
    st, p = it.get("statement_type"), it.get("payload") or {}
    if st == "amendment_op":
        t = str(p.get("type") or "")
        for pre, k in (("replace", "replace"), ("insert", "insert"), ("append", "insert"), ("add", "insert"),
                       ("delete", "delete"), ("remove", "delete"), ("annotate", "annotate"), ("set_status", "status")):
            if t.startswith(pre):
                return k
        return t or "op"
    if st == "disposition":
        return str(p.get("disposition") or "disposition")
    if st == "escalation":
        return "unclear"
    return str(st or "item")


def run_items(rd: Path) -> tuple[list[dict], dict]:
    """The run's analysis items (its combined set), each as {id, provision, target, kind, words, evidence, status}."""
    cp = _checkpoint(rd)
    p = _combined_path(rd, cp)
    if p is None:
        return [], cp
    ps = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("proposal_set") or {}
    out = []
    for it in ps.get("items") or []:
        ev = [{"page": e.get("page"), "unit_id": e.get("unit_id"), "words": e.get("words")}
              for e in it.get("evidence") or [] if isinstance(e, dict)]
        out.append({"id": it.get("id"), "provision": it.get("provision"), "target": it.get("target"),
                    "kind": _run_kind(it), "statement_type": it.get("statement_type"),
                    "status": it.get("verification_status"), "evidence": ev})
    return out, cp


def _prov(x) -> str:
    s = re.sub(r"^[A-Z]+-\d+:", "", str(x or "").strip())
    s = re.sub(r"^(clause|section|paragraph|para\.?|item|no\.?)\s+", "", s, flags=re.I)
    return s.strip().rstrip(".").lower()


def _overlap(a: str, words: list[str]) -> float:
    aw = set(_words(a))
    best = 0.0
    for w in words:
        bw = set(_words(w))
        if len(aw) >= 3 and len(bw) >= 3:
            best = max(best, len(aw & bw) / min(len(aw), len(bw)))
    return round(best, 2)


def _kinds_agree(b: str, r: str) -> bool:
    return b == r or (b == "unclear" and r in ("unclear", "issue", "clarification"))


def match(items: list[dict], ritems: list[dict]) -> tuple[list, list, list, list]:
    """One-to-one matches by provision, target unit and quoted words (greedy by score); then agreements,
    disagreements (with the differences), briefing-only and run-only items."""
    cands = []
    for bi, b in enumerate(items):
        for ri, r in enumerate(ritems):
            prov = bool(_prov(b["provision"])) and _prov(b["provision"]) == _prov(r["provision"])
            tgt = bool(b.get("target_unit_guess")) and b.get("target_unit_guess") == r.get("target")
            w = _overlap(b["quotation"], [e.get("words") or "" for e in r["evidence"]])
            if not (prov or tgt or w >= 0.8):
                continue
            basis = [x for x, ok in (("provision", prov), ("target unit", tgt), (f"quoted words ({w:.0%} shared)",
                                                                                   w >= 0.6)) if ok]
            score = 3 * prov + 2 * tgt + w + (0.5 if _kinds_agree(b["kind"], r["kind"]) else 0)
            cands.append((score, bi, ri, basis))
    used_b, used_r, pairs = set(), set(), []
    for score, bi, ri, basis in sorted(cands, key=lambda c: (-c[0], c[1], c[2])):
        if bi in used_b or ri in used_r:
            continue
        used_b.add(bi)
        used_r.add(ri)
        pairs.append((bi, ri, basis))
    agree, disagree = [], []
    for bi, ri, basis in sorted(pairs):
        b, r = items[bi], ritems[ri]
        diffs = []
        bt, rt = b.get("target_unit_guess"), r.get("target")
        if bt and rt and bt != rt:
            diffs.append(f"target unit: briefing {bt}, run {rt}")
        if not _kinds_agree(b["kind"], r["kind"]):
            diffs.append(f"kind: briefing {b['kind']}, run {r['kind']}")
        side_b = {k: b.get(k) for k in ("id", "provision", "page", "quotation", "target_unit_guess", "kind",
                                        "deliverables", "confidence", "uncertainty_class", "uncertainty")}
        side_b["checks"] = b.get("checks")
        entry = {"briefing": side_b, "run": r, "matched_by": basis}
        if not (bt and rt):
            entry["note"] = "a target unit is named on one side only"
        if diffs:
            disagree.append({**entry, "differences": diffs, "for_a_person": True,
                             "what_to_do": "investigate: read both quotations against the addendum; the run's "
                                           "validators and a person decide; nothing is changed by this list"})
        else:
            agree.append({**entry, "note_on_agreement": NOT_PROOF})
    b_only = [{k: items[i].get(k) for k in ("id", "provision", "page", "quotation", "target_unit_guess", "kind")}
              for i in range(len(items)) if i not in used_b]
    r_only = [ritems[i] for i in range(len(ritems)) if i not in used_r]
    return agree, disagree, b_only, r_only


def run_timing(cp: dict) -> dict:
    o = (cp.get("steps") or {}).get("outputs") or {}
    done = o.get("status") == "done" and o.get("finished")
    s = _secs(cp.get("created"), o.get("finished")) if done else None
    return {"run_updated_a1_a5_s": s, "run_started": cp.get("created"), "run_outputs_finished": o.get("finished"),
            "note": ("from the run's start to the end of its outputs step (the candidate A1-A5)" if s is not None
                     else "the run has not built its updated A1-A5 candidate yet")}


def compare(qr_id: str, run_ref: str, *, staging: Path | None = None) -> dict:
    """See the module docstring; writes comparison.json and comparison.md beside the briefing (and nothing else)."""
    st = Path(staging or ROOT / "staging/ai")
    d = qr_dir(st, qr_id)
    pres = preserved(d)
    if not pres["ok"]:
        raise QuickReviewError(f"quick review {qr_id}: {pres['why']}: the initial findings changed after they were "
                               "written; a comparison is made only with the briefing as written")
    b = load(d)
    rd = run_dir(run_ref, st)
    ritems, cp = run_items(rd)
    agree, disagree, b_only, r_only = match(b["items"], ritems)
    qt = json.loads((d / "timing.json").read_text(encoding="utf-8")) if (d / "timing.json").is_file() else {}
    timings = {"quick_review_first_briefing_s": qt.get("seconds_to_first_briefing"),
               "quick_review_first_briefing": qt.get("first_useful_briefing"), **run_timing(cp)}
    out = {"header": NOT_PROOF, "label": LABEL, "qr_id": qr_id, "created": _now(),
           "run": {"run_id": cp.get("run_id"), "dir": str(rd), "status": cp.get("status"),
                   "combined_set": str(_combined_path(rd, cp) or "none (the run has no combined set yet)")},
           "briefing_preserved": pres["ok"],
           "counts": {"briefing_items": len(b["items"]), "run_items": len(ritems), "agreements": len(agree),
                      "disagreements": len(disagree), "briefing_only": len(b_only), "run_only": len(r_only)},
           "agreements": agree, "disagreements": disagree, "briefing_only": b_only, "run_only": r_only,
           "timings": timings,
           "note": ("Disagreements are a list for a person, never an edit: nothing of the run, of the briefing or of "
                    "curation/ was changed. Matching is by provision, target unit and quoted words; a match is not "
                    "a judgement that either side is right.")}
    _write(d / "comparison.json", _jdump(out))
    _write(d / "comparison.md", render_comparison(out))
    return out


def _side(r: dict) -> str:
    ev = "; ".join(f"p{e.get('page')} {e.get('unit_id') or ''}: “{e.get('words')}”" for e in r.get("evidence") or [])
    return f"{r.get('id')} ({r.get('kind')}, target {r.get('target')}, status {r.get('status')}): {ev or 'no evidence'}"


def render_comparison(c: dict) -> str:
    t = c["timings"]
    L = [f"# {NOT_PROOF}", "", f"{LABEL}", "",
         f"Quick review `{c['qr_id']}` compared with run `{c['run']['run_id']}` ({c['run']['status']}) on "
         f"{c['created']}. Briefing preserved as written: {'yes' if c['briefing_preserved'] else 'NO'}.", "",
         "Counts: " + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in c["counts"].items()), "",
         "## Timings (measured separately)", "",
         f"- time to the quick review's first useful briefing: "
         f"{t['quick_review_first_briefing_s'] if t['quick_review_first_briefing_s'] is not None else 'none'} s",
         f"- time to the run's updated A1-A5 candidate: "
         f"{t['run_updated_a1_a5_s'] if t['run_updated_a1_a5_s'] is not None else 'not yet'} s ({t['note']})", "",
         "## Disagreements (for a person to investigate; nothing is edited)", ""]
    for x in c["disagreements"]:
        b = x["briefing"]
        L += [f"- briefing {b['id']} (provision {b['provision']}, p{b['page']}, {b['kind']}, target "
              f"{b['target_unit_guess']}): “{b['quotation']}”", f"  - run {_side(x['run'])}",
              f"  - differences: {'; '.join(x['differences'])}; matched by {', '.join(x['matched_by'])}"]
    L += ["" if c["disagreements"] else "(none)", "", "## Agreements (not proof)", ""]
    for x in c["agreements"]:
        b = x["briefing"]
        L.append(f"- briefing {b['id']} ~ run {x['run']['id']} (matched by {', '.join(x['matched_by'])})")
    L += ["" if c["agreements"] else "(none)", "", "## In the briefing only", ""]
    L += [f"- {b['id']}: provision {b['provision']} p{b['page']} ({b['kind']}, target {b['target_unit_guess']}): "
          f"“{b['quotation']}”" for b in c["briefing_only"]] or ["(none)"]
    L += ["", "## In the run only", ""]
    L += [f"- {_side(r)}" for r in c["run_only"]] or ["(none)"]
    L += ["", c["note"]]
    return "\n".join(L).rstrip() + "\n"


# ---------------------------------------------------------------------------------------------- answers

def _answers(d: Path) -> dict:
    p = Path(d) / "answers.yaml"
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.is_file() else {}


def _save_answers(d: Path, data: dict) -> None:
    data.setdefault("note", "the owner's answers to the questions of a PRELIMINARY AI BRIEFING, against the exact "
                            "question and evidence; recorded here only (never in curation/)")
    _write(Path(d) / "answers.yaml", yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))


def record_answer(d: Path, question_id: str, answer: str, by: str, *, now: str | None = None) -> dict:
    """The owner's answer (name, time) against the exact question text and the evidence it cites. Never touches
    curation/ and never edits the briefing."""
    d = Path(d)
    pres = preserved(d)
    if not pres["ok"]:
        raise QuickReviewError(f"{pres['why']}: an answer is recorded only against the briefing as written")
    by = " ".join(str(by or "").split())
    answer = str(answer or "").strip()
    if not by or len(by) > 100:
        raise QuickReviewError("type your name (the person answering)")
    if not answer or len(answer) > 4000:
        raise QuickReviewError("type the answer (at most 4000 characters)")
    b = load(d)
    q = next((q for q in b.get("questions") or [] if q.get("id") == question_id), None)
    if q is None:
        raise QuickReviewError(f"no question {question_id!r} in this briefing "
                               f"({', '.join(x.get('id') for x in b.get('questions') or []) or 'none'})")
    data = _answers(d)
    rows = data.setdefault("answers", [])
    e = {"id": f"A{len(rows) + 1}", "question_id": question_id, "question": q["question"],
         "evidence": q["evidence"], "answer": answer, "by": by, "recorded": now or _now(),
         "briefing_sha256": hashlib.sha256((d / "briefing.json").read_bytes()).hexdigest(),
         "status": "recorded (not incorporated)", "offers": []}
    rows.append(e)
    _save_answers(d, data)
    return e


def fingerprint(rd: Path) -> str:
    """The staleness guard's fingerprint of a run: its combined set, its downstream set and its candidate's curation
    and pack (whatever of them exists)."""
    rd = Path(rd)
    cp = _checkpoint(rd)
    files = [p for p in (_combined_path(rd, cp), rd / "downstream" / "proposals.yaml",
                         rd / "candidate" / "pack.yaml") if p is not None and p.is_file()]
    cur = rd / "candidate" / "curation"
    files += sorted(cur.glob("**/*.yaml")) if cur.is_dir() else []
    h = hashlib.sha256()
    for f in files:
        h.update(f.relative_to(rd).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def safe_checkpoint(cp: dict) -> tuple[bool, str, str | None, str | None]:
    """(between phases?, why not, the last step done, the next step) from a run's checkpoint: never while a step or a
    batch is running."""
    steps = cp.get("steps") or {}
    running = [s for s in STEPS_ORDER if (steps.get(s) or {}).get("status") == "running"]
    batches = [k for k, v in (cp.get("batches") or {}).items() if (v or {}).get("status") == "running"]
    done = [s for s in STEPS_ORDER if (steps.get(s) or {}).get("status") in ("done", "skipped")]
    nxt = next((s for s in STEPS_ORDER if (steps.get(s) or {}).get("status") in (None, "pending")), None)
    if running or batches:
        what = (f"the run's {running[0]} step is running" if running else "a batch of the run is running") + \
            (f" (batches running: {', '.join(batches[:5])})" if batches else "")
        return False, (f"{what}: an owner's answer is offered only between phases, never under a running batch; it "
                       "is held and offered when the step ends"), done[-1] if done else None, nxt
    return True, "", done[-1] if done else None, nxt


def offer_answers(d: Path, rd: Path) -> dict:
    """Offer the recorded answers of quick review `d` to run `rd` at a safe checkpoint (see the module docstring)."""
    d, rd = Path(d), Path(rd)
    cp = _checkpoint(rd)
    data = _answers(d)
    rows = data.get("answers") or []
    ok, why, last, nxt = safe_checkpoint(cp)
    out = {"offered": [], "held": [], "already": []}
    nf = rd / "owner_answers" / f"{d.name}.yaml"
    notes = (yaml.safe_load(nf.read_text(encoding="utf-8")) or {}).get("notes", []) if nf.is_file() else []
    have = {n.get("answer_id") for n in notes}
    pdf = ((cp.get("inputs") or {}).get("pdf") or {}).get("path")
    pages = read_pdf(Path(pdf))["pages"] if pdf and Path(pdf).is_file() else []
    now = _now()
    for a in rows:
        if a["id"] in have:
            out["already"].append(a["id"])
            continue
        if not ok:
            a.setdefault("offers", []).append({"run": cp.get("run_id"), "at": now, "result": "held", "reason": why})
            out["held"].append({"answer": a["id"], "reason": why})
            continue
        checks = [quote_check(e["quotation"], pages, e["page"]) if pages else
                  "not checked: the run's addendum PDF is not readable here" for e in a["evidence"]]
        n = {"id": f"{d.name}/{a['id']}", "answer_id": a["id"], "status": "PROPOSED", "review": "pending a person",
             "kind": "an owner's answer to a question of a PRELIMINARY AI BRIEFING",
             "question_id": a["question_id"], "question": a["question"], "evidence": a["evidence"],
             "answer": a["answer"], "by": a["by"], "recorded": a["recorded"], "offered": now,
             "offered_after": last, "before": nxt, "evidence_checks": checks,
             "revalidation": {"state": "current", "fingerprint": fingerprint(rd), "checked": now,
                              "guard": "the run's combined set, downstream set and candidate curation; a change "
                                       "after this offer makes the note STALE until it is offered again"},
             "what_it_is": "a note for the run's review, never a decision: a person still decides every item"}
        notes.append(n)
        a.setdefault("offers", []).append({"run": cp.get("run_id"), "at": now, "result": "offered as a PROPOSED note",
                                           "between": [last, nxt]})
        a["status"] = f"offered to run {cp.get('run_id')} as a PROPOSED note (not incorporated as a decision)"
        out["offered"].append(n["id"])
    if out["offered"]:
        nf.parent.mkdir(parents=True, exist_ok=True)
        _write(nf, yaml.safe_dump({"label": LABEL, "notes": notes}, allow_unicode=True, sort_keys=False, width=110))
    if rows:
        _save_answers(d, data)
    return out


def revalidate_offers(rd: Path) -> dict:
    """The staleness guard: every offered note whose run changed since its offer is marked STALE."""
    rd = Path(rd)
    fp, now = fingerprint(rd), _now()
    out = {"current": [], "stale": []}
    for nf in sorted((rd / "owner_answers").glob("*.yaml")) if (rd / "owner_answers").is_dir() else []:
        data = yaml.safe_load(nf.read_text(encoding="utf-8")) or {}
        for n in data.get("notes") or []:
            rv = n.setdefault("revalidation", {})
            if rv.get("fingerprint") == fp:
                out["current"].append(n["id"])
                continue
            rv["state"] = (f"STALE since {now}: the run's proposals or candidate changed after the note was offered; "
                           "offer it again so its evidence is checked against the new state")
            out["stale"].append(n["id"])
        _write(nf, yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))
    return out


# ---------------------------------------------------------------------------------------------- the command line

def add_parser(s, common) -> None:
    q = s.add_parser("quick-review", help="a separate, bounded AI quick review of a new addendum (a PRELIMINARY AI "
                                          "BRIEFING); compare | answer | offer | revalidate")
    q.add_argument("what", help="ADD-NN to start one; or compare QR RUN | answer QR | offer QR RUN | revalidate RUN")
    q.add_argument("rest", nargs="*")
    q.add_argument("--pdf")
    q.add_argument("--route", choices=list(ROUTES), help="default: host, or ollama in offline mode")
    q.add_argument("--model")
    q.add_argument("--cassette", help="recorded route: the cassette to replay (tests)")
    q.add_argument("--budget-minutes", type=float, default=DEFAULT_BUDGET_MIN)
    q.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    q.add_argument("--qr-id")
    q.add_argument("--for-run", help="the run this quick review was started beside (recorded only)")
    q.add_argument("--offline", action="store_true")
    q.add_argument("--nice", type=int, default=NICE, help="lower this process's priority to at least this niceness")
    q.add_argument("--question")
    q.add_argument("--answer")
    q.add_argument("--by")
    common(q)


def cli(a) -> int:
    from . import budget as B
    from . import config as C
    st = Path(a.out)
    try:
        if a.what == "compare":
            if len(a.rest) != 2:
                raise QuickReviewError("usage: tenderpack ai quick-review compare QR_ID RUN_ID|RUN_DIR")
            c = compare(a.rest[0], a.rest[1], staging=st)
            print(NOT_PROOF)
            print(f"{LABEL}\nquick review {c['qr_id']} vs run {c['run']['run_id']}: " + ", ".join(
                f"{k.replace('_', ' ')} {v}" for k, v in c["counts"].items()))
            t = c["timings"]
            print(f"time to the first useful briefing: {t['quick_review_first_briefing_s']} s; time to the run's "
                  f"updated A1-A5 candidate: {t['run_updated_a1_a5_s']} s")
            print(f"written: {qr_dir(st, c['qr_id']) / 'comparison.md'} (disagreements are for a person; nothing "
                  "was edited)")
            return 0
        if a.what == "answer":
            if len(a.rest) != 1 or not a.question:
                raise QuickReviewError("usage: tenderpack ai quick-review answer QR_ID --question ID --answer TEXT --by "
                                       "NAME")
            e = record_answer(qr_dir(st, a.rest[0]), a.question, a.answer, a.by)
            print(f"recorded {e['id']} by {e['by']} at {e['recorded']} against question {e['question_id']} "
                  f"(“{e['question']}”); curation/ is not changed")
            return 0
        if a.what == "offer":
            if len(a.rest) != 2:
                raise QuickReviewError("usage: tenderpack ai quick-review offer QR_ID RUN_ID|RUN_DIR")
            print(json.dumps(offer_answers(qr_dir(st, a.rest[0]), run_dir(a.rest[1], st)), indent=1))
            return 0
        if a.what == "revalidate":
            if len(a.rest) != 1:
                raise QuickReviewError("usage: tenderpack ai quick-review revalidate RUN_ID|RUN_DIR")
            print(json.dumps(revalidate_offers(run_dir(a.rest[0], st)), indent=1))
            return 0
        if not ADDENDUM.match(a.what):
            raise QuickReviewError(f"{a.what!r}: give ADD-NN (with --pdf), or compare | answer | offer | revalidate")
        if not a.pdf:
            raise QuickReviewError("--pdf is required")
        if a.route is None:
            from .offline import requested
            a.route = "ollama" if requested(C.load(Path(a.config)), a.offline) else "host"
        try:
            if os.nice(0) < a.nice:
                os.nice(a.nice - os.nice(0))                    # lower priority than the main run
        except OSError:
            pass
        print(LABEL, flush=True)
        res = run(a.what, Path(a.pdf), route=a.route, evidence=Path(a.evidence), pack=Path(a.pack), staging=st,
                  worklog=Path(a.worklog), ai_config=Path(a.config), model=a.model,
                  cassette=Path(a.cassette) if a.cassette else None, budget_minutes=a.budget_minutes,
                  max_tokens=a.max_tokens, qr_id=a.qr_id, offline=a.offline, for_run=a.for_run,
                  echo=lambda m: print(m, flush=True))
        t = res["timing"]
        print(f"quick review {res['qr_id']}: {res['status']}" + (f" ({res['error']})" if res["error"] else ""))
        print(f"first useful briefing: {t['first_useful_briefing'] or 'none'}"
              + (f" ({t['seconds_to_first_briefing']} s after the start)" if t["seconds_to_first_briefing"] is not None
                 else "") + f"; tokens {t['tokens']['input_tokens']} in / {t['tokens']['output_tokens']} out in "
              f"{t['tokens']['calls']} call(s)")
        print(f"folder: {res['dir']} (briefing.md, briefing.json, timing.json, briefing.sha256)")
        return res["exit_code"]
    except (QuickReviewError, B.Refused, C.ConfigError) as e:
        print(f"REFUSED: {e}")
        return 2
