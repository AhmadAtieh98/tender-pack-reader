"""Indirect effects through reusable, evidence-backed relationships (session 10).

A register row cites the units its own words are in; `diff`, A2 and A5 used to report only rows that cite a changed
unit. Many effects run through other provisions: a change to who is a member reaches every per-member obligation, an
effluent limit reaches the reliability run and the contract's Unavailability Event, the payment mechanism reaches the
Financial Model and Form 4-F, and a document the pack references but does not supply blocks conclusions elsewhere.
Those links are curated here, once, as data, and followed by the program; nothing is inferred at run time.

    curation/relationships.yaml   (a rehearsal pack keeps its own copy beside its register: <work>/relationships.yaml;
                                   `relationships:` in the pack config overrides the path)
      relationships:
        - id: REL-...                  unique
          from: <id> | [<id>, ...]     a row id, a unit id (a table or form id also stands for its members), a
                                       calculation `calc:<name>`, or `words:<phrase>` (a lexical trigger: an op of
                                       the stage adds or removes words containing the phrase)
          to: <id> | [<id>, ...]       a row id, a unit id, an A5 activity id, an evidence item id (EV-...), a date
                                       rule id, or a calculation `calc:<name>` (which can be the `from` of other entries)
          kind: one of KINDS
          status: confirmed | proposed | possible
          evidence: [{unit, page, words}]   verbatim, on that page (check-register); REQUIRED for confirmed
          basis: why the link is believed  REQUIRED for proposed and possible
          origin: who drafted it ("curator", "ai:<run or route>" for a model's proposal)
          note, issues: [I-...]        what to review; open issues it links to (they are linked, never resolved)
          document, document_id, blocks   missing_document only: the document not supplied, a short id, and the
                                       conclusion that cannot be established without it
          confirmed_by                 a person, when a model-proposed link (origin ai:...) is marked confirmed
          review: proposed             a drafting flag like a row's; never counts as a decision

Statuses (never merged):
  confirmed  the documents themselves state the link; the entry quotes the cross-reference verbatim
  proposed   inferred by a curator or a model, with its basis; a person decides. The program never promotes a proposed
             link to confirmed (append_proposed always writes proposed; a model's link marked confirmed needs a
             person's name in confirmed_by)
  possible   a weaker inference; also the ceiling of anything reached through a `words:` trigger
Traversal follows entries transitively from what changed (an entry's targets are the `from` of others; a path is as
strong as its weakest link) and reports three labelled classes, never merged with the direct-citation changes:
"confirmed dependency", "proposed relationship", "possible impact". A missing_document entry is also reported when one
of its targets changes (the blocked conclusion is in play again). Reached A5 activities are marked
"REVIEW (<class>)" with their dates unchanged.

API for other tools and agents:
  load(path) -> [entry]                                       entries as written ([] when the file does not exist)
  validate(entries, units, rows, activities, ...) -> [finding] 'REL-ID: what is wrong' (check-register, release gate)
  reach(entries, changed_rows_or_units, words=()) -> {target: [(entry, status)]}
  trace(entries, changed, words=()) -> [record]               the same with paths and sources
  append_proposed(path, entries, origin) -> {appended, skipped}   lands a model's dependency proposals as PROPOSED
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from .register import found
from .util import load_yaml

KINDS = {
    "cites": "the target's words refer to the source (a clause, table, form or schedule)",
    "depends_on": "the target's content or work depends on the source",
    "feeds_calculation": "the source is an input to a calculation or a figure the target states",
    "member_scope": "the target applies per member of the Bidder, so who is a member changes it",
    "limit_applies": "a limit the source sets is applied by the target",
    "missing_document": "the source references a document the pack does not supply; the target's conclusion is blocked",
}
STATUSES = ("confirmed", "proposed", "possible")
CLASSES = {"confirmed": "confirmed dependency", "proposed": "proposed relationship", "possible": "possible impact"}
_RANK = {s: i for i, s in enumerate(STATUSES)}
FIELDS = ("id", "from", "to", "kind", "status", "evidence", "basis", "origin", "note", "issues", "document",
          "document_id", "blocks", "confirmed_by", "review", "reviewer")
REQUIRED = ("id", "from", "to", "kind", "status", "origin")
WORDS, CALC = "words:", "calc:"
MAX_DEPTH = 4
DEFAULT_NAME = "relationships.yaml"
HEADER = ("# Relationships between rows, units, calculations, evidence and A5 activities (tenderpack.relationships).\n"
          "# confirmed = the documents state the link (verbatim evidence, checked by check-register); proposed = inferred,\n"
          "# with its basis; possible = weaker. `review:` is a drafting flag and never counts as a decision.\n")


# ---------------------------------------------------------------------------------------------- files

def default_path(cfg: dict, root: Path) -> Path:
    """`relationships:` in the pack config, else relationships.yaml beside the register's folder (curation/ for the
    real pack, <rehearsal>/work/ for a rehearsal pack): a pack without one has no relationships."""
    root = Path(root)
    if cfg.get("relationships"):
        p = Path(cfg["relationships"])
        return p if p.is_absolute() else root / p
    reg = Path(cfg.get("register", "curation/register/rows.yaml"))
    reg = reg if reg.is_absolute() else root / reg
    return reg.parent.parent / DEFAULT_NAME


def load(path) -> list[dict]:
    """The entries of a relationships file as written (plain dicts; validate() checks them). [] when the file does not
    exist. A file that is not a mapping with a `relationships` list raises ValueError."""
    p = Path(path)
    if not p.exists():
        return []
    data = load_yaml(p) or {}
    if not isinstance(data, dict) or not isinstance(data.get("relationships") or [], list):
        raise ValueError(f"{p}: expected a mapping with a `relationships:` list")
    return [dict(e) if isinstance(e, dict) else e for e in data.get("relationships") or []]


def ends(entry: dict, key: str) -> list[str]:
    """`from` or `to` of an entry as a list of ids."""
    v = entry.get(key)
    if isinstance(v, str):
        return [v]
    return [x for x in (v or []) if isinstance(x, str)] if isinstance(v, list) else []


def _blank(v) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def _norm(t: str) -> str:
    return " ".join(str(t or "").lower().replace("’", "'").split())


def model_origin(origin) -> bool:
    """True for an entry a model proposed: origin 'ai' or 'ai:<run or route>' (as append_proposed writes it)."""
    return bool(re.match(r"ai(?::|$)", str(origin or "").strip().lower()))


# ---------------------------------------------------------------------------------------------- validation

def _activity_ids(activities) -> set[str]:
    if isinstance(activities, dict):                    # an activity-templates mapping
        return {t["id"] for k, ts in activities.items() if not str(k).startswith("_") for t in (ts or [])
                if isinstance(t, dict) and "id" in t}
    return {a if isinstance(a, str) else a.get("id") for a in (activities or [])} - {None}


def validate(entries: list, units: list[dict], rows, activities, *, evidence_items=(), date_rules=(),
             issues=None, known_units=()) -> list[str]:
    """Findings ('REL-ID: what'), empty when every entry is well formed and evidenced. `units`: the evidence build's
    units (dicts with unit_id, pages, text); `rows`: Row objects or row ids; `activities`: activity ids or the
    activity-templates mapping; `evidence_items`, `date_rules`: known ids (date rules are also read from Row objects);
    `issues`: known issue ids (None: not checked); `known_units`: further unit ids that exist (e.g. made by an op).
    Every quote is checked the way check-register checks quotes: non-blank, verbatim in the unit's text, on that page."""
    by_unit = {u["unit_id"]: u for u in units}
    unit_ids = set(by_unit) | set(known_units)
    row_list = list(rows or [])
    row_ids = {getattr(r, "id", r) for r in row_list}
    rule_ids = set(date_rules) | {d.rule_id for r in row_list for d in getattr(r, "date_rules", []) or []}
    act_ids, ev_ids = _activity_ids(activities), set(evidence_items or ())
    calc_targets = {t for e in entries if isinstance(e, dict) for t in ends(e, "to") if t.startswith(CALC)}
    out, seen = [], set()

    def node(x: str, side: str) -> str | None:
        """None when `x` names something that exists; otherwise why not."""
        if x.startswith(WORDS):
            return None if side == "from" and len(_norm(x[len(WORDS):]).split()) >= 2 else \
                ("a `words:` trigger is allowed in `from` only" if side == "to" else "a `words:` phrase needs two words or more")
        if x.startswith(CALC):
            if not re.fullmatch(r"calc:[a-z0-9][a-z0-9-]*", x):
                return "a calculation is named calc:<lower-case-name>"
            if side == "from" and x not in calc_targets:
                return f"{x} is reached by no entry (no `to: {x}`)"
            return None
        if x in row_ids or x in unit_ids:
            return None
        if side == "to" and (x in act_ids or x in ev_ids or x in rule_ids):
            return None
        return ("no row or unit with that id" if side == "from"
                else "no row, unit, activity, evidence item, date rule or calc: with that id")

    for i, e in enumerate(entries or []):
        if not isinstance(e, dict):
            out.append(f"relationships[{i}]: not a mapping")
            continue
        rid = str(e.get("id") or "").strip() or f"relationships[{i}]"
        if rid in seen:
            out.append(f"{rid}: duplicate id")
        seen.add(rid)
        extra = sorted(set(e) - set(FIELDS))
        if extra:
            out.append(f"{rid}: unknown field(s) {extra} (known: {', '.join(FIELDS)})")
        missing = [k for k in REQUIRED if _blank(e.get(k)) or e.get(k) == []]
        if missing:
            out.append(f"{rid}: missing {missing}")
        kind, status = e.get("kind"), e.get("status")
        if kind is not None and kind not in KINDS:
            out.append(f"{rid}: unknown kind {kind!r} (one of {', '.join(KINDS)})")
        if status is not None and status not in STATUSES:
            out.append(f"{rid}: unknown status {status!r} (one of {', '.join(STATUSES)})")
        if e.get("review", "proposed") not in ("proposed", "accepted"):
            out.append(f"{rid}: review must be 'proposed' or 'accepted' (a drafting flag), not {e.get('review')!r}")
        for key in ("from", "to"):
            if e.get(key) is not None and not isinstance(e.get(key), (str, list)):
                out.append(f"{rid}: `{key}` must be an id or a list of ids")
            for x in ends(e, key):
                why = node(x, key)
                if why:
                    out.append(f"{rid}: {key} {x}: {why}")
        if kind == "missing_document":
            bad = [x for x in ends(e, "to") if x not in row_ids and x not in unit_ids]
            if bad:
                out.append(f"{rid}: a missing_document entry blocks rows or units only; not: {bad}")
            for k in ("document", "document_id", "blocks"):
                if _blank(e.get(k)):
                    out.append(f"{rid}: missing_document needs `{k}` (the document, a short id, the conclusion it blocks)")
        ev = e.get("evidence") or []
        if not isinstance(ev, list):
            out.append(f"{rid}: evidence must be a list of {{unit, page, words}}")
            ev = []
        for q in ev:
            if not isinstance(q, dict) or any(_blank(q.get(k)) for k in ("unit", "page", "words")):
                out.append(f"{rid}: evidence needs a unit, a page and non-blank words; got {q!r}")
                continue
            u = by_unit.get(q["unit"])
            if u is None:
                out.append(f"{rid}: evidence unit {q['unit']} does not exist in the evidence build")
            elif not found(str(q["words"]), u.get("text", "")):
                out.append(f"{rid}: evidence not verbatim in {q['unit']}: '{str(q['words'])[:80]}'")
            elif q["page"] not in u.get("pages", []):
                out.append(f"{rid}: evidence unit {q['unit']} is on page(s) {u.get('pages')}, not p{q['page']}")
        if status == "confirmed":
            if not ev:
                out.append(f"{rid}: status confirmed needs evidence quoting the documents' own cross-reference; "
                           "an inferred link is `proposed` with its basis")
            if model_origin(e.get("origin")):
                from .readings import is_assistant, valid_reviewer
                who = e.get("confirmed_by")
                if not valid_reviewer(who) or is_assistant(who):
                    out.append(f"{rid}: a link a model proposed (origin {e.get('origin')!r}) is confirmed only by a person "
                               "named in `confirmed_by`; the program never promotes a proposed link")
        elif status in ("proposed", "possible") and _blank(e.get("basis")):
            out.append(f"{rid}: status {status} needs a `basis` (why the link is believed)")
        if issues is not None:
            bad = [x for x in e.get("issues") or [] if x not in issues]
            if bad:
                out.append(f"{rid}: linked issues that do not exist: {bad}")
    return out


# ---------------------------------------------------------------------------------------------- traversal

def _weakest(a: str, b: str) -> str:
    return a if _RANK.get(a, 2) >= _RANK.get(b, 2) else b


def trace(entries: list, changed, words=(), max_depth: int = MAX_DEPTH) -> list[dict]:
    """Every target reached from `changed` (row and unit ids, calc: names), as records sorted by status, target and
    path: {target, entry_id (the last entry of the path), kind, status (the path's weakest link), class, path: [entry
    ids], source (the first changed id or `words:` phrase that started it), sources (all of them), lexical (started by a
    words: trigger), via_target (a missing_document entry whose blocked target changed)}. `words`: the words the
    stage's ops added or removed (a `words:` trigger matches a phrase inside them; such a path is at most a possible
    impact). Entries of unknown kind or status are skipped (validate reports them)."""
    changed = set(changed or ())
    texts = [_norm(w) for w in words or () if w]
    good = [e for e in entries or [] if isinstance(e, dict) and e.get("kind") in KINDS and e.get("status") in STATUSES
            and e.get("id")]
    by_from: dict[str, list[dict]] = {}
    for e in good:
        for f in ends(e, "from"):
            if not f.startswith(WORDS):
                by_from.setdefault(f, []).append(e)
    best: dict[tuple, dict] = {}

    def add(target: str, e: dict, status: str, path: list[str], sources: list[str], lexical: bool,
            via_target: bool) -> bool:
        """Record one path to a target (its sources are those of the path's first entry); True when it is new."""
        key = (target, tuple(path), lexical, via_target)
        if key in best:
            return False
        best[key] = {"target": target, "entry_id": e["id"], "kind": e["kind"], "status": status, "class": CLASSES[status],
                     "path": list(path), "source": sources[0], "sources": list(sources), "lexical": lexical,
                     "via_target": via_target}
        return True

    frontier = []                                       # (node, status, path, sources, lexical) to follow further
    for e in good:
        gap = e["kind"] == "missing_document"           # a blocked conclusion is reported, never followed further
        exact = sorted(f for f in ends(e, "from") if not f.startswith(WORDS) and f in changed)
        lexical = sorted(f for f in ends(e, "from") if f.startswith(WORDS) and _norm(f[len(WORDS):])
                         and any(_norm(f[len(WORDS):]) in t for t in texts))
        for srcs, lex in ((exact, False), (lexical, True)):
            if not srcs or (lex and exact):             # a lexical match adds nothing when the unit itself changed
                continue
            st = _weakest(e["status"], "possible") if lex else e["status"]
            frontier += [(t, st, [e["id"]], srcs, lex) for t in ends(e, "to")
                         if add(t, e, st, [e["id"]], srcs, lex, False) and not gap]
        if gap and not exact:
            for t in ends(e, "to"):
                if t in changed:
                    add(t, e, e["status"], [e["id"]], [t], False, True)
    depth = 1
    while frontier and depth < max_depth:
        nxt = []
        for node, status, path, sources, lexical in frontier:
            for e in by_from.get(node, []):
                if e["id"] in path or e["kind"] == "missing_document":
                    continue
                st = _weakest(status, e["status"])
                p = path + [e["id"]]
                nxt += [(t, st, p, sources, lexical) for t in ends(e, "to") if add(t, e, st, p, sources, lexical, False)]
        frontier, depth = nxt, depth + 1
    return sorted(best.values(), key=lambda r: (_RANK[r["status"]], r["target"], r["path"], r["source"]))


def reach(entries: list, changed_rows_or_units, words=()) -> dict[str, list[tuple[dict, str]]]:
    """{target: [(entry, status), ...]} for every target reached from the changed ids (trace() without the paths):
    `entry` is the last entry on the path, `status` the path's (its weakest link); strongest first."""
    by_id = {e["id"]: e for e in entries or [] if isinstance(e, dict) and e.get("id")}
    out: dict[str, list[tuple[dict, str]]] = {}
    for r in trace(entries, changed_rows_or_units, words):
        pair = (by_id[r["entry_id"]], r["status"])
        if pair not in out.setdefault(r["target"], []):
            out[r["target"]].append(pair)
    return out


# ---------------------------------------------------------------------------------------------- what changed at a stage

def changed_units(prev_state: dict, state: dict, ignore_annotations=()) -> set[str]:
    """Units whose status, text, cells, annotations, replacement or number differ between two stage states (an
    addendum's own units count: they are issued at its stage). Annotations by the ops in `ignore_annotations` (an
    answer that only confirms a clause) are not a change."""
    ign = set(ignore_annotations)
    out = set()
    for k in set(prev_state) | set(state):
        a, b = prev_state.get(k), state.get(k)
        if a is None or b is None:
            out.add(k)
            continue
        if (a.status, a.text, a.cells, [x for x in a.annotations if x not in ign], a.superseded_by, a.number) != \
                (b.status, b.text, b.cells, [x for x in b.annotations if x not in ign], b.superseded_by, b.number):
            out.add(k)
    return out


def changed_words(stage) -> list[str]:
    """The words the applied ops of a stage add or remove: old and new words, inserted or replacing content, and the
    provision of an annotation that adds or interprets an obligation (for `words:` triggers)."""
    out = []
    for x in stage.ops:
        if not x.applied:
            continue
        o = x.op
        out += [w for w in (o.old, o.new, o.new_text) if w]
        out += [stage.state[k].text for k in x.details.get("content", []) if k in stage.state]
        if o.type == "annotate" and o.effect in ("adds_obligation", "interprets") and o.provision in stage.state:
            out.append(stage.state[o.provision].text)
    return out


def impact_between(r: dict, frm: str, to: str) -> dict:
    """What changed from stage `frm` to stage `to` of a stage2 run and what the relationships reach from it:
    {"from", "changed_units": [...], "direct_rows": [...] (rows citing a changed unit, changed by an op of the stages
    after `frm`, entering or leaving force, or re-read), "records": [trace record + target_type, target_status (a
    row's status at `to`), direct (the target is itself directly changed)]}. Annotations that only confirm a clause are
    not changes; the words of every op after `frm` up to `to` feed the `words:` triggers."""
    entries = r.get("relationships") or []
    stages, evals = r["stages"], r["evals"]
    order = [s.stage for s in stages]
    sp, s = stages[order.index(frm)], stages[order.index(to)]
    between = set(order[order.index(frm) + 1: order.index(to) + 1])
    op_stage = r["register"].op_stage if r.get("register") is not None else {}
    rows = {e["row"].id: e for e in evals}
    acts = _activity_ids(r.get("templates") or {})
    evs = set(r.get("evidence_items") or {})
    rules = {d.rule_id for e in evals for d in e["row"].date_rules}
    confirms = {x.op.id for st in stages for x in st.ops if x.op.type == "annotate" and x.op.effect == "confirms"}
    raw = changed_units(sp.state, s.state, confirms)
    parents = {getattr(s.state.get(k) or sp.state.get(k), "parent", None) for k in raw} - {None}
    direct = set()
    for rid, e in rows.items():
        a, b = e["stages"][frm], e["stages"][to]
        cites = set(e["row"].units) | ({b.get("effective_unit")} - {None})
        here = [h for h in b.get("ops") or [] if op_stage.get(h) in between]
        if cites & raw or here or bool(a["active"]) != bool(b["active"]) or (
                b.get("interpretation_stage") in between and a.get("interpretation") != b.get("interpretation")):
            direct.add(rid)
    words = [w for st in stages if st.stage in between for w in changed_words(st)]
    recs = trace(entries, raw | parents | direct, words) if entries else []
    for rec in recs:
        t = rec["target"]
        rec["target_type"] = ("row" if t in rows else "calculation" if t.startswith(CALC) else
                              "unit" if t in s.state else "activity" if t in acts else
                              "evidence item" if t in evs else "date rule" if t in rules else "?")
        rec["target_status"] = rows[t]["stages"][to]["status"] if t in rows else (
            s.state[t].status.upper() if t in s.state else "")
        rec["direct"] = t in direct or t in raw
    return {"from": frm, "changed_units": sorted(raw), "direct_rows": sorted(direct), "records": recs}


def impact(r: dict) -> dict[str, dict]:
    """impact_between for each addendum stage of a stage2 run and the stage before it: {stage: {...}} (the first stage,
    BASE, reaches nothing)."""
    order = [s.stage for s in r["stages"]]
    out = {st: {"from": None, "changed_units": [], "direct_rows": [], "records": []} for st in order[:1]}
    for prev, st in zip(order, order[1:]):
        out[st] = impact_between(r, prev, st)
    return out


# ---------------------------------------------------------------------------------------------- presentation helpers

def label(rec: dict, entries: list | None = None) -> str:
    """One line for a reached target: 'VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:29.3 via REL-A > REL-B [feeds_calculation]'.
    With `entries`, a missing_document record also says what is not supplied and which conclusion it blocks."""
    what = rec.get("target_type") or ""
    st = rec.get("target_status") or ""
    head = f"{rec['target']}" + (f" ({what}{'; ' + st if st else ''})" if what else "")
    trig = "target changed" if rec.get("via_target") else ", ".join(rec.get("sources") or [rec["source"]])
    line = (f"{head} <- {trig} via {' > '.join(rec['path'])} [{rec['kind']}; link {rec['status']}]"
            + ("; also changed directly" if rec.get("direct") else ""))
    e = next((x for x in entries or [] if isinstance(x, dict) and x.get("id") == rec["entry_id"]), None)
    if e is not None and rec["kind"] == "missing_document":
        line += f". NOT SUPPLIED: {e.get('document')}; cannot be established: {e.get('blocks')}"
    return line


def by_class(records: list[dict]) -> list[tuple[str, list[dict]]]:
    """Dependency records grouped in the fixed class order (confirmed dependency, proposed relationship, possible
    impact); missing-document records are listed apart (gaps)."""
    return [(CLASSES[s], [r for r in records if r["status"] == s and r["kind"] != "missing_document"]) for s in STATUSES]


def gaps(records: list[dict]) -> list[dict]:
    """The missing-document records: a conclusion in play at the stage that a document not supplied blocks."""
    return [r for r in records if r["kind"] == "missing_document"]


def activity_review(records: list[dict], activity: dict) -> list[dict]:
    """The relationship reviews an A5 activity carries at a stage: one per class, for records whose target is the
    activity, one of the rows it serves (req_ids) or one of its evidence items. Missing-document records are gaps,
    not work to redo, and are left out. [{class, status, targets, entries, sources}] strongest first."""
    rows, evs = set(activity.get("req_ids") or []), set(activity.get("evidence_items") or [activity.get("evidence")])
    out = []
    for status in STATUSES:
        hit = [r for r in records or [] if r["status"] == status and r["kind"] != "missing_document"
               and (r["target"] == activity.get("id") or r["target"] in rows or r["target"] in evs)]
        if hit:
            out.append({"class": CLASSES[status], "status": status,
                        "targets": sorted({r["target"] for r in hit}),
                        "entries": sorted({e for r in hit for e in r["path"]}),
                        "sources": sorted({s for r in hit for s in r.get("sources") or [r["source"]]})})
    return out


def review_flag(rv: dict) -> str:
    return (f"REVIEW ({rv['class']}): {', '.join(rv['targets'])} reached from {', '.join(rv['sources'])} via "
            f"{', '.join(rv['entries'])}; dates unchanged (a relationship, not a direct citation)")


def links_of(entries: list, target: str) -> list[dict]:
    """Entries naming `target` in `from` or `to`."""
    return [e for e in entries or [] if isinstance(e, dict) and (target in ends(e, "to") or target in ends(e, "from"))]


def missing_documents(entries: list) -> dict[str, dict]:
    """{document_id: {document, entries: [entry], targets: [ids], sources: [ids]}} over the missing_document entries."""
    out: dict[str, dict] = {}
    for e in entries or []:
        if not isinstance(e, dict) or e.get("kind") != "missing_document" or _blank(e.get("document_id")):
            continue
        d = out.setdefault(e["document_id"], {"document": e.get("document"), "entries": [], "targets": [], "sources": []})
        d["entries"].append(e)
        d["targets"] += [t for t in ends(e, "to") if t not in d["targets"]]
        d["sources"] += [f for f in ends(e, "from") if f not in d["sources"]]
    return dict(sorted(out.items()))


def evidence_text(e: dict) -> str:
    return "; ".join(f"{q.get('unit')} p{q.get('page')}: “{q.get('words')}”" for q in e.get("evidence") or [])


# ---------------------------------------------------------------------------------------------- landing proposals

def append_proposed(path, entries: list[dict], origin: str) -> dict:
    """Land relationship proposals (e.g. a model's `dependency` proposals) in a relationships file as PROPOSED entries.
    Each entry needs from, to, kind (KINDS) and basis; it may carry id, evidence [{unit, page, words}], note, issues,
    and, for missing_document, document, document_id and blocks. Its status is written as `proposed` (or `possible`
    when the proposer said so): a claim that the documents confirm the link is recorded in the note, never as the
    status; a person who checks the evidence may change it and names themselves in `confirmed_by`. `origin` names
    the proposer (written as 'ai:<origin>'); `review: proposed`. An entry with the same from, to and kind as an existing
    one is skipped. Nothing else in the file changes: the entries are appended as text after the last one, and the
    result is read back before it replaces the file. Returns {"appended": [ids], "skipped": [{"entry", "why"}]}.
    Raises ValueError (writing nothing) when an entry is malformed. Quotes are checked by check-register, not here."""
    if _blank(origin):
        raise ValueError("append_proposed: `origin` must name the proposer (a run id or route)")
    origin = origin.strip() if model_origin(origin) else f"ai:{origin.strip()}"
    p = Path(path)
    existing = load(p)
    ids = {e.get("id") for e in existing if isinstance(e, dict)}
    keys = {(tuple(ends(e, "from")), tuple(ends(e, "to")), e.get("kind")) for e in existing if isinstance(e, dict)}
    n = 1 + max([int(m.group(1)) for i in ids if isinstance(i, str) and (m := re.fullmatch(r"REL-AI-(\d+)", i))] or [0])
    new, skipped = [], []
    allowed = {"id", "from", "to", "kind", "basis", "evidence", "note", "issues", "document", "document_id", "blocks",
               "status"}
    for raw in entries or []:
        if not isinstance(raw, dict):
            raise ValueError(f"append_proposed: not a mapping: {raw!r}")
        extra = sorted(set(raw) - allowed)
        if extra:
            raise ValueError(f"append_proposed: unknown field(s) {extra} in {raw.get('id') or raw}")
        if any(not ends(raw, k) for k in ("from", "to")) or raw.get("kind") not in KINDS or _blank(raw.get("basis")):
            raise ValueError(f"append_proposed: each entry needs from, to, a kind ({', '.join(KINDS)}) and a basis: {raw!r}")
        key = (tuple(ends(raw, "from")), tuple(ends(raw, "to")), raw["kind"])
        if key in keys:
            skipped.append({"entry": raw.get("id") or f"{key}", "why": "an entry with the same from, to and kind exists"})
            continue
        claimed = str(raw.get("status") or "proposed")
        e = {"id": raw.get("id") or f"REL-AI-{n:03d}", "from": raw["from"], "to": raw["to"], "kind": raw["kind"],
             "status": "possible" if claimed == "possible" else "proposed", "basis": str(raw["basis"]).strip()}
        if not raw.get("id"):
            n += 1
        if e["id"] in ids:
            raise ValueError(f"append_proposed: id {e['id']} exists already")
        for k in ("evidence", "issues", "document", "document_id", "blocks"):
            if raw.get(k):
                e[k] = raw[k]
        note = str(raw.get("note") or "").strip()
        if claimed == "confirmed":
            note = (note + " " if note else "") + ("[The proposer said the documents state this link; it is recorded as "
                                                   "proposed until a person checks the evidence and confirms it.]")
        if note:
            e["note"] = note
        e.update({"origin": origin, "review": "proposed"})
        ids.add(e["id"])
        keys.add(key)
        new.append(e)
    if not new:
        return {"appended": [], "skipped": skipped}
    text = p.read_text(encoding="utf-8") if p.exists() else HEADER + "relationships:\n"
    if not re.search(r"(?m)^relationships:\s*(\[\])?\s*$", text):
        raise ValueError(f"{p}: no top-level `relationships:` list to append to")
    text = re.sub(r"(?m)^relationships:\s*\[\]\s*$", "relationships:", text)
    block = yaml.safe_dump(new, allow_unicode=True, sort_keys=False, width=110)
    block = "".join("  " + ln if ln.strip() else ln for ln in block.splitlines(keepends=True))
    candidate = text.rstrip("\n") + "\n" + block
    check = (yaml.safe_load(candidate) or {}).get("relationships") or []
    if len(check) != len(existing) + len(new) or check[-len(new):] != new:
        raise ValueError(f"{p}: the relationships list is not the last top-level key; nothing written")
    tmp = p.with_name(f".{p.name}.{os.getpid()}.tmp")
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(candidate, encoding="utf-8")
    tmp.replace(p)
    return {"appended": [e["id"] for e in new], "skipped": skipped}
