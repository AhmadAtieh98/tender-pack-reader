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
          note, issues: [I-...]        what to review; open issues it links to (they are linked, never resolved).
                                       Session 13 (audit R1-1/R1-2): the issues travel with the link: every row the
                                       entry names in `to` lists them in A1 ('I-X (via REL-ID (status))', issue_links),
                                       and A2 shows them ('open: I-X[, human decision pending]') wherever the entry
                                       carries a change (signals.relationship_issue_notes)
          context: [{unit, page, words, note}]   session 13 (audit R1-4): words of the pack that bear on the link
                                       without stating it (a non-binding record such as the pre-bid minutes), quoted
                                       verbatim on their page and checked like evidence; shown beside the link
                                       ('context (not binding)'), never counted as its evidence or as a decision
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

Completeness and blockers (session 11). Session 10's traversal stopped after four links without saying so, so an
indirect chain could look complete when it was not; and a missing-document gap was reported only when its own `from`
or its blocked target changed directly, so a blocked target reached indirectly lost its blocker. Now:
  * the traversal is cycle-safe (a visited set per path: a link back to a node already on the path is recorded once,
    as `cyclic`, and never followed again) and bounded only by a configured bound (MAX_DEPTH links per path; the pack
    config's `relationships_max_depth` overrides it in impact) and a record budget (MAX_RECORDS). Every record says
    whether its chain is `complete`, `truncated` by a bound (the links not followed are named: reported, never silent)
    or `cyclic`; completeness(records) sums it up and label() prints "CHAIN INCOMPLETE" where it is;
  * every node of a path (the changed source included) that a missing_document entry blocks puts that entry on the
    record's `blockers` ("cannot be established: <document> not supplied (<conclusion>)"), so the blocker travels with
    the chain into impact, `diff`, A2 and the A5 review flags (label(), review_flag()).
Record fields for renderers (trace / impact_between records): target, entry_id, kind, status, class, path [entry ids],
nodes [source, each target in order], source, sources, lexical, via_target, completeness (complete | truncated |
cyclic), chain_complete (False only when truncated), unfollowed [entry ids not followed past the target], truncated_by
(depth | records | ''), bound (the depth bound used), cycle [nodes of the loop, first repeated], blockers [{entry_id,
document_id, document, blocks, node, status, text}], blocked (bool).

Discovery (session 11): discover(units, rows=None, existing=()) proposes `proposed` entries from the documents' own
cross-references ("as defined in Clause X", "calculated in accordance with", "in the form set out in", "the figure
stated in", "listed in Table", "subject to Clause", "referred to in" and a defined term used in another clause), each
with the verbatim words; it never writes `confirmed` and never writes the curated file (`tenderpack relationships
discover --to <file>` writes a separate file for a person).

API for other tools and agents:
  load(path) -> [entry]                                       entries as written ([] when the file does not exist)
  validate(entries, units, rows, activities, ...) -> [finding] 'REL-ID: what is wrong' (check-register, release gate)
  reach(entries, changed_rows_or_units, words=()) -> {target: [(entry, status)]}
  trace(entries, changed, words=(), max_depth=MAX_DEPTH) -> [record]   the same with paths, sources, completeness, blockers
  completeness(records) -> {complete, truncated, cyclic, bound} blocked(records) -> records carrying a blocker
  discover(units, rows=None, existing=()) -> {entries, unresolved, skipped_terms}   proposed links for a person
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
# Session 12 (audit R-6): one line printed wherever relationships are listed (A1, A2, a3_detail, diff), so that a link's
# "confirmed" (the documents state it) is not read as "confirmed by the owner", the words used for the image readings.
STATUS_LEGEND = ("Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not "
                 "confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a "
                 "weaker inference.")
_RANK = {s: i for i, s in enumerate(STATUSES)}
FIELDS = ("id", "from", "to", "kind", "status", "evidence", "basis", "origin", "note", "issues", "document",
          "document_id", "blocks", "confirmed_by", "review", "reviewer", "context")
REQUIRED = ("id", "from", "to", "kind", "status", "origin")
WORDS, CALC = "words:", "calc:"
MAX_DEPTH = 12            # links per path; a path cut here is `truncated` and says which links it did not follow
MAX_RECORDS = 20000       # records per trace; reaching it truncates the paths still to follow (reported, never silent)
COMPLETENESS = ("complete", "truncated", "cyclic")
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
        ctx = e.get("context") or []                    # session 13 (audit R1-4): checked like evidence
        if not isinstance(ctx, list):
            out.append(f"{rid}: context must be a list of {{unit, page, words, note}}")
            ctx = []
        for q in ctx:
            if not isinstance(q, dict) or any(_blank(q.get(k)) for k in ("unit", "page", "words")):
                out.append(f"{rid}: context needs a unit, a page and non-blank words; got {q!r}")
                continue
            u = by_unit.get(q["unit"])
            if u is None:
                out.append(f"{rid}: context unit {q['unit']} does not exist in the evidence build")
            elif not found(str(q["words"]), u.get("text", "")):
                out.append(f"{rid}: context not verbatim in {q['unit']}: '{str(q['words'])[:80]}'")
            elif q["page"] not in u.get("pages", []):
                out.append(f"{rid}: context unit {q['unit']} is on page(s) {u.get('pages')}, not p{q['page']}")
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


def _gap_index(good: list[dict]) -> dict[str, list[dict]]:
    """{node: [missing_document entries whose `to` names it]}: the nodes whose conclusion a document not supplied
    blocks."""
    out: dict[str, list[dict]] = {}
    for e in good:
        if e["kind"] == "missing_document":
            for t in ends(e, "to"):
                out.setdefault(t, []).append(e)
    return out


def blocker_text(e: dict) -> str:
    """'cannot be established: <document> not supplied (<the conclusion it blocks>)'."""
    blocks = str(e.get("blocks") or "").strip()
    return f"cannot be established: {e.get('document') or e.get('document_id')} not supplied" + (
        f" ({blocks})" if blocks else "")


def _blockers(nodes: list[str], gap_by_node: dict[str, list[dict]], skip: str | None = None) -> list[dict]:
    out, seen = [], set()
    for n in nodes:
        for g in gap_by_node.get(n, []):
            if g["id"] == skip or (g["id"], n) in seen:
                continue
            seen.add((g["id"], n))
            out.append({"entry_id": g["id"], "document_id": g.get("document_id"), "document": g.get("document"),
                        "blocks": g.get("blocks"), "node": n, "status": g.get("status"), "text": blocker_text(g)})
    return out


def trace(entries: list, changed, words=(), max_depth: int | None = MAX_DEPTH,
          max_records: int = MAX_RECORDS, inherit: dict | None = None) -> list[dict]:
    """Every target reached from `changed` (row and unit ids, calc: names), as records sorted by status, target and
    path: {target, entry_id (the last entry of the path), kind, status (the path's weakest link), class, path: [entry
    ids], nodes (the source, then each target along the path), source (the first changed id or `words:` phrase that
    started it), sources (all of them), lexical (started by a words: trigger), via_target (a missing_document entry
    whose blocked target changed), completeness / chain_complete / unfollowed / truncated_by / bound / cycle, blockers /
    blocked} (the module docstring says what each means). `words`: the words the stage's ops added or removed (a
    `words:` trigger matches a phrase inside them; such a path is at most a possible impact). Entries of unknown kind or
    status are skipped (validate reports them).

    Cycle-safe: a path never visits a node twice; a link back to a node already on it is recorded once as `cyclic`
    and not followed. Bounded only by `max_depth` links per path (None: no depth bound) and `max_records`; a path cut
    by either is `truncated` and names the links it did not follow. Missing-document entries are reported (gaps) and
    never followed; every node on a path that one blocks puts it on the record's `blockers`."""
    changed = set(changed or ())
    texts = [_norm(w) for w in words or () if w]
    good = [e for e in entries or [] if isinstance(e, dict) and e.get("kind") in KINDS and e.get("status") in STATUSES
            and e.get("id")]
    by_from: dict[str, list[dict]] = {}
    for e in good:
        for f in ends(e, "from"):
            if not f.startswith(WORDS):
                by_from.setdefault(f, []).append(e)
    gap_by_node = _gap_index(good)
    by_id = {e["id"]: e for e in good}
    inherit = inherit or {}
    bound = max_depth if max_depth and max_depth > 0 else None

    def inherited(path: list[str], nodes: list[str]) -> list[dict]:
        # session 11 audit (A2-5): a limit a blocked source sets is blocked where it is applied: a limit_applies link
        # from a node whose rows a document not supplied blocks (`inherit`, impact_between) carries that blocker on
        out = []
        for k, eid in enumerate(path):
            e = by_id.get(eid)
            if e is not None and e["kind"] == "limit_applies" and k < len(nodes):
                out += _blockers([nodes[k]], inherit)
        return out
    best: dict[tuple, dict] = {}

    def onward(node: str, path: list[str]) -> list[str]:
        return sorted({e["id"] for e in by_from.get(node, []) if e["kind"] != "missing_document" and e["id"] not in path})

    def add(target: str, e: dict, status: str, path: list[str], sources: list[str], lexical: bool,
            via_target: bool, nodes: list[str], cyclic: bool = False) -> dict | None:
        """Record one path to a target (its sources are those of the path's first entry); the record when new."""
        key = (target, tuple(path), lexical, via_target)
        if key in best:
            return None
        gap = e["kind"] == "missing_document"
        bl = [] if gap else _blockers(list(dict.fromkeys(sources + nodes[1:])), gap_by_node)
        if not gap:
            bl += [b for b in inherited(path, nodes) if b["entry_id"] not in {x["entry_id"] for x in bl}]
        rec = {"target": target, "entry_id": e["id"], "kind": e["kind"], "status": status, "class": CLASSES[status],
               "path": list(path), "nodes": list(nodes), "source": sources[0], "sources": list(sources),
               "lexical": lexical, "via_target": via_target, "completeness": "complete", "chain_complete": True,
               "unfollowed": [], "truncated_by": "", "bound": bound, "cycle": [], "blockers": bl, "blocked": bool(bl)}
        if cyclic:
            first = nodes.index(target) if target in nodes[:-1] else 0
            rec.update({"completeness": "cyclic", "cycle": nodes[first:]})
        best[key] = rec
        return rec

    def cut(rec: dict, path: list[str], why: str) -> None:
        rest = onward(rec["target"], path)
        if rest:
            rec.update({"completeness": "truncated", "chain_complete": False, "unfollowed": rest, "truncated_by": why})

    frontier = []                                       # (record, node, status, path, nodes, sources, lexical)
    for e in good:
        gap = e["kind"] == "missing_document"           # a blocked conclusion is reported, never followed further
        exact = sorted(f for f in ends(e, "from") if not f.startswith(WORDS) and f in changed)
        lexical = sorted(f for f in ends(e, "from") if f.startswith(WORDS) and _norm(f[len(WORDS):])
                         and any(_norm(f[len(WORDS):]) in t for t in texts))
        for srcs, lex in ((exact, False), (lexical, True)):
            if not srcs or (lex and exact):             # a lexical match adds nothing when the unit itself changed
                continue
            st = _weakest(e["status"], "possible") if lex else e["status"]
            for t in ends(e, "to"):
                loop = not gap and t in srcs
                rec = add(t, e, st, [e["id"]], srcs, lex, False, [srcs[0], t], cyclic=loop)
                if rec is not None and not gap and not loop:
                    frontier.append((rec, t, st, [e["id"]], [srcs[0], t], srcs, lex))
        if gap and not exact:
            for t in ends(e, "to"):
                if t in changed:
                    add(t, e, e["status"], [e["id"]], [t], False, True, [t, t])
    depth = 1
    while frontier:
        nxt = []
        for rec, node, status, path, nodes, sources, lexical in frontier:
            if bound is not None and depth >= bound:
                cut(rec, path, "depth")                 # the configured bound: reported on the record, never silent
                continue
            if len(best) >= max_records:
                cut(rec, path, "records")
                continue
            seen = set(sources) | set(nodes)
            for e in by_from.get(node, []):
                if e["id"] in path or e["kind"] == "missing_document":
                    continue
                st = _weakest(status, e["status"])
                p = path + [e["id"]]
                for t in ends(e, "to"):
                    loop = t in seen
                    new = add(t, e, st, p, sources, lexical, False, nodes + [t], cyclic=loop)
                    if new is not None and not loop:
                        nxt.append((new, t, st, p, nodes + [t], sources, lexical))
        frontier, depth = nxt, depth + 1
    return sorted(best.values(), key=lambda r: (_RANK[r["status"]], r["target"], r["path"], r["source"]))


def completeness(records: list[dict]) -> dict:
    """{complete: no record truncated, truncated: [targets], cyclic: [targets], bound, records: n}: whether every chain
    of a trace was followed to its end."""
    recs = list(records or [])
    tr = sorted({r["target"] for r in recs if r.get("completeness") == "truncated"})
    cy = sorted({r["target"] for r in recs if r.get("completeness") == "cyclic"})
    return {"complete": not tr, "truncated": tr, "cyclic": cy, "bound": recs[0].get("bound") if recs else None,
            "records": len(recs)}


def blocked(records: list[dict]) -> list[dict]:
    """The reached records (not the gap records themselves) whose chain passes a node a document not supplied blocks."""
    return [r for r in records or [] if r.get("blockers") and r["kind"] != "missing_document"]


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
    bound = (r.get("cfg") or {}).get("relationships_max_depth", MAX_DEPTH)     # the configured bound (pack config)
    # session 11 audit (A2-5): a document not supplied that blocks rows blocks the units they cite and those units'
    # tables or forms, for limit_applies links from them (trace `inherit`): the Environmental Permit blocks every Table
    # 2-4 row, so every row applying a Table 2-4 limit inherits the block
    inherit: dict[str, list[dict]] = {}
    for g in entries:
        if not isinstance(g, dict) or g.get("kind") != "missing_document" or not g.get("id"):
            continue
        for t in ends(g, "to"):
            for u in (rows[t]["row"].units if t in rows else []):
                n = u
                while n:
                    if g not in inherit.setdefault(n, []):
                        inherit[n].append(g)
                    n = getattr(s.state.get(n) or sp.state.get(n), "parent", None)
    recs = trace(entries, raw | parents | direct, words, max_depth=bound, inherit=inherit) if entries else []
    for rec in recs:
        t = rec["target"]
        rec["target_type"] = ("row" if t in rows else "calculation" if t.startswith(CALC) else
                              "unit" if t in s.state else "activity" if t in acts else
                              "evidence item" if t in evs else "date rule" if t in rules else "?")
        rec["target_status"] = rows[t]["stages"][to]["status"] if t in rows else (
            s.state[t].status.upper() if t in s.state else "")
        rec["direct"] = t in direct or t in raw
    return {"from": frm, "changed_units": sorted(raw), "direct_rows": sorted(direct), "records": recs,
            "completeness": completeness(recs), "blocked": sorted({x["target"] for x in blocked(recs)})}


def impact(r: dict) -> dict[str, dict]:
    """impact_between for each addendum stage of a stage2 run and the stage before it: {stage: {...}} (the first stage,
    BASE, reaches nothing)."""
    order = [s.stage for s in r["stages"]]
    out = {st: {"from": None, "changed_units": [], "direct_rows": [], "records": [], "completeness": completeness([]),
                "blocked": []} for st in order[:1]}
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
    if rec.get("completeness") == "truncated":                  # session 11: never silent
        line += (f"; CHAIN INCOMPLETE: stopped at the bound ({rec.get('truncated_by') or 'depth'}"
                 + (f", {rec['bound']} links" if rec.get("truncated_by") == "depth" and rec.get("bound") else "")
                 + f"); not followed: {', '.join(rec.get('unfollowed') or [])}")
    elif rec.get("completeness") == "cyclic":
        line += f"; cycle: {' > '.join(rec.get('cycle') or [])} (not followed again)"
    for b in rec.get("blockers") or []:                         # session 11: the blocker travels with the chain
        line += f"; BLOCKED: {b['text']}" + (f" [at {b['node']}, {b['entry_id']}]" if b["node"] != rec["target"]
                                             else f" [{b['entry_id']}]")
    e = next((x for x in entries or [] if isinstance(x, dict) and x.get("id") == rec["entry_id"]), None)
    if e is not None and rec["kind"] == "missing_document":
        line += f". NOT SUPPLIED: {e.get('document')}; cannot be established: {e.get('blocks')}"
        if e.get("context"):                                     # session 13 (audit R1-4)
            line += "; " + context_text(e)
    return line


def context_text(e: dict) -> str:
    """'context (not binding): <unit> p<page> '<words>' (<note>)' for an entry's `context` quotations; '' without."""
    ctx = [q for q in e.get("context") or [] if isinstance(q, dict)]
    return ("context (not binding): " + "; ".join(f"{q.get('unit')} p{q.get('page')} '{q.get('words')}'"
                                                  + (f" ({q['note']})" if q.get("note") else "") for q in ctx)) if ctx else ""


def issue_links(entries: list, rows) -> dict[str, list[dict]]:
    """Session 13 (audit R1-2): row id -> [{issue, via, status}] for every entry with `issues` and every row it names in
    `to` (`rows`: the register's row ids; a unit, activity or calculation target is not a row). One rule for every
    issue and every entry, whatever its kind or status (the status is shown, never used to drop a link)."""
    rows = set(rows or ())
    out: dict[str, list[dict]] = {}
    for e in entries or []:
        if not isinstance(e, dict) or not e.get("issues"):
            continue
        for t in ends(e, "to"):
            if t in rows:
                for i in e.get("issues") or []:
                    x = {"issue": i, "via": e.get("id"), "status": e.get("status")}
                    if x not in out.setdefault(t, []):
                        out[t].append(x)
    return out


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
    not work to redo, and are left out. [{class, status, targets, entries, sources}] strongest first; session 11 adds
    `blockers` (the texts of the documents not supplied that block a reached chain) and `incomplete` (a chain cut by
    the bound) only where there are some."""
    rows, evs = set(activity.get("req_ids") or []), set(activity.get("evidence_items") or [activity.get("evidence")])
    out = []
    for status in STATUSES:
        hit = [r for r in records or [] if r["status"] == status and r["kind"] != "missing_document"
               and (r["target"] == activity.get("id") or r["target"] in rows or r["target"] in evs)]
        if hit:
            rv = {"class": CLASSES[status], "status": status,
                  "targets": sorted({r["target"] for r in hit}),
                  "entries": sorted({e for r in hit for e in r["path"]}),
                  "sources": sorted({s for r in hit for s in r.get("sources") or [r["source"]]})}
            bl = sorted({b["text"] for r in hit for b in r.get("blockers") or []})
            if bl:
                rv["blockers"] = bl
            cut = sorted({r["target"] for r in hit if r.get("completeness") == "truncated"})
            if cut:
                rv["incomplete"] = cut
            out.append(rv)
    return out


def review_flag(rv: dict) -> str:
    return (f"REVIEW ({rv['class']}): {', '.join(rv['targets'])} reached from {', '.join(rv['sources'])} via "
            f"{', '.join(rv['entries'])}; dates unchanged (a relationship, not a direct citation)"
            + "".join(f"; BLOCKED: {b}" for b in rv.get("blockers") or [])
            + (f"; CHAIN INCOMPLETE at {', '.join(rv['incomplete'])}" if rv.get("incomplete") else ""))


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


# ---------------------------------------------------------------------------------------------- discovery (session 11)
# The documents' own cross-references, proposed for a person (never confirmed, never written into the curated file).
# Each phrase is followed by the clause, table, form or appendix it names (citations.citations; a bare "Clause N" or
# "Table N-N" takes the unit's own volume); the link runs FROM the unit named TO the unit whose words name it (a change
# to the named unit may change what the naming unit requires). Order matters: the first phrase that matches a span wins.
DISCOVERY_PHRASES = (
    (r"as defined in", "depends_on", "a definition the words rely on"),
    (r"has the meaning given in", "depends_on", "a definition given elsewhere"),
    (r"calculated (?:in accordance with|under)", "feeds_calculation", "a calculation the words rely on"),
    (r"(?:figure|amount|value|rate|sum|cost)s? (?:as )?(?:stated|specified|shown) (?:by the Bidder )?in",
     "feeds_calculation", "a figure stated elsewhere"),
    (r"in the form set out in", "cites", "a form the words require"),
    (r"(?:listed|set out|specified|identified) in", "cites", "a list, table or schedule the words rely on"),
    (r"subject to", "depends_on", "a provision the words are subject to"),
    (r"referred to in", "cites", "a provision the words refer to"),
    (r"required by", "depends_on", "a requirement stated elsewhere"),
    (r"in accordance with", "depends_on", "a provision the words follow"),
)
_DEF = re.compile(r"^\W*[\"“‘']?(?P<term>[A-Z][A-Za-z0-9\-]*(?:\s+(?:of\s+|the\s+)?[A-Z][A-Za-z0-9\-]*){0,5})[\"”’']?"
                  r"\s+(?:means|shall mean|has the meaning)\b")
_DOC_REF = re.compile(r"\b(?:Schedule|Appendix|Annex|Attachment|Exhibit)\s+[A-Z0-9][\w.-]*")
_ROMAN = {"VOL-I": "I", "VOL-II": "II", "VOL-III": "III", "VOL-IV": "IV", "VOL-V": "V"}
DISCOVER_ORIGIN = "discover"
MAX_TERM_USES = 10            # a defined term used in more units than this is reported, not proposed unit by unit


def _context(t: str, start: int, end: int, before: int = 6, after: int = 6) -> str:
    """The words around a span of `t` (a few words either side), sliced from `t` as printed, within the sentence."""
    s = start
    for _ in range(before):
        m = re.search(r"(\S+)\s*$", t[:s])
        if not m or re.search(r"[.;:]$", m.group(1)):          # never across a sentence end
            break
        s = m.start(1)
    e = end
    for _ in range(after):
        if re.match(r"[.;:]", t[e:e + 1]):
            break
        m = re.match(r"\s*(\S+)", t[e:])
        if not m:
            break
        e += m.end(1)
        if re.search(r"[.;:]$", m.group(1)):
            break
    return t[s:e].strip(" ,;:.")


def discover(units: list[dict], rows=None, existing=(), *, include_addenda: bool = False,
             max_term_uses: int = MAX_TERM_USES) -> dict:
    """Proposed relationships read from the documents' own words (session 11), for a person to review:
    {"entries": [entry (status proposed, origin discover, review proposed, basis, verbatim evidence)],
     "unresolved": [{unit, page, words, reference}] (a reference to a document the evidence does not contain: a
     candidate missing_document for a person), "skipped_terms": {term: number of units using it} (defined terms used
     in more than `max_term_uses` units: listed, not proposed one by one), "already_curated": [entries found that an
     existing entry already links]}.
    `units`: the evidence build's units as issued (the quotes are checked against them, as check-register does);
    `rows`: Row objects (or {id, units}) so each entry also reaches the rows citing the naming unit; `existing`: the
    curated entries (an entry linking the same from and to is not proposed again). Addendum units are left out unless
    `include_addenda` (an addendum's references are amendment targets, which the engine handles). Nothing is
    written; nothing is confirmed."""
    from .citations import citations, resolve
    from .textnorm import normalize_latin
    ids = {u["unit_id"] for u in units}
    by_id = {u["unit_id"]: u for u in units}
    cites_unit: dict[str, list[str]] = {}
    for row in rows or []:
        rid, runits = (row.get("id"), row.get("units")) if isinstance(row, dict) else (row.id, row.units)
        for uid in runits or []:
            cites_unit.setdefault(uid, []).append(rid)
    pool = [u for u in units if (include_addenda or not u["doc"].startswith("ADD-")) and u.get("kind") != "heading"
            and ":cover/" not in u["unit_id"] and (u.get("text") or "").strip()]
    found_links: dict[tuple, dict] = {}
    unresolved: list[dict] = []

    def page(u: dict) -> int | None:
        return (u.get("pages") or [None])[0]

    def targets_of(window: str, doc: str) -> tuple[list[str], str]:
        """The units the first reference in `window` names, and that reference's words as printed ('' when none). A
        bare 'Clause N' or 'Table N-N' (no volume before it, no 'of Volume' after it) takes the unit's own volume."""
        roman = _ROMAN.get(doc)

        def own(m):
            if re.search(r"Volume (?:I{1,3}|IV|V)\s*$", window[:m.start()]) or \
                    re.match(r"\s+of Volume", window[m.end():]):
                return m.group(0)
            return f"Volume {roman} {m.group(0)}"
        local = re.sub(r"\b(?:Clause \d+(?:\.\d+)*|Table \d+-\d+)", own, window) if roman else window
        cs = citations(local)
        first = min(cs, key=lambda c: local.find(c.text)) if cs else None
        if first is None or local.find(first.text) > 60:
            return [], ""
        words = first.text
        if words not in window and roman and words.startswith(f"Volume {roman} "):
            words = words[len(f"Volume {roman} "):]
        got = []
        for g in resolve([first], ids):
            if g in ids:
                got.append(g)
                continue
            # a form or table group with no unit of its own (VOL-IV:F4-D): its top-level members stand for it (a
            # table among them stands for its rows through their `parent`, as impact_between reads changes)
            members = [k for k in ids if k.startswith(g + "/")]
            got += sorted(k for k in members if by_id[k].get("parent") not in members)
        return got, words

    for u in pool:
        t = normalize_latin(u["text"])
        taken: list[tuple[int, int]] = []
        for rx, kind, why in DISCOVERY_PHRASES:
            for m in re.finditer(r"\b" + rx + r"\b", t, re.I):
                if any(a <= m.start() < b for a, b in taken):
                    continue
                rest = t[m.end():]
                stop = re.search(r"[.;](?:\s|$)", rest)
                window = rest[: stop.start() if stop else 200][:200]
                if re.match(r"\s*this (?:Clause|Agreement|Volume|Form|Section)\b", window):
                    continue                                    # a reference to itself
                got, cite_words = targets_of(window, u["doc"])
                got = [g for g in got if g != u["unit_id"] and not u["unit_id"].startswith(g + "/")
                       and g != (u.get("parent") or "") and not g.startswith(u["unit_id"] + "/")]
                if not got:
                    d = _DOC_REF.match(window.strip())
                    if d and not cite_words:
                        end = m.end() + window.find(d.group(0)) + len(d.group(0))
                        unresolved.append({"unit": u["unit_id"], "page": page(u), "words": t[m.start():end],
                                           "reference": d.group(0)})
                        taken.append((m.start(), end))
                    continue
                k = window.find(cite_words)
                end = m.end() + (k + len(cite_words) if k >= 0 else 0)
                words = t[m.start():end].strip()
                if not found(words, u["text"]):
                    words = m.group(0)
                taken.append((m.start(), end))
                frm = tuple(got)
                key = (frm, u["unit_id"])
                e = found_links.setdefault(key, {"from": list(frm), "to": [u["unit_id"]] + sorted(cites_unit.get(u["unit_id"], [])),
                                                 "kind": kind, "status": "proposed", "evidence": [],
                                                 "basis": "", "_why": why})
                q = {"unit": u["unit_id"], "page": page(u), "words": words}
                if q not in e["evidence"]:
                    e["evidence"].append(q)
    # definitions: the term defined in one clause and used by its name in others
    defs: dict[str, list[dict]] = {}
    for u in pool:
        m = _DEF.match(normalize_latin(u["text"]))
        if m and u.get("kind") in ("clause", "paragraph", "list_item", "numbered_paragraph"):
            defs.setdefault(m.group("term").strip(), []).append(u)
    skipped: dict[str, int] = {}
    for term, dus in sorted(defs.items()):
        rx = re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])")
        uses = [u for u in pool if u["unit_id"] not in {d["unit_id"] for d in dus} and rx.search(normalize_latin(u["text"]))]
        if len(uses) > max_term_uses:
            skipped[term] = len(uses)
            continue
        for use in uses:
            same = [d for d in dus if d["doc"] == use["doc"]] or dus        # a volume's own definition first
            frm = tuple(sorted(d["unit_id"] for d in same))
            t = normalize_latin(use["text"])
            hit = rx.search(t)
            key = (frm, use["unit_id"])
            if key in found_links:
                continue
            found_links[key] = {"from": list(frm), "to": [use["unit_id"]] + sorted(cites_unit.get(use["unit_id"], [])),
                                "kind": "depends_on", "status": "proposed", "_why": f"the defined term '{term}'",
                                "evidence": [{"unit": use["unit_id"], "page": page(use),
                                              "words": _context(t, hit.start(), hit.end())}]
                                + [{"unit": d["unit_id"], "page": page(d), "words": f"{term} " + re.search(
                                    r"(means|shall mean|has the meaning)", normalize_latin(d["text"])).group(1)} for d in same]}
    have = [(set(ends(e, "from")), set(ends(e, "to"))) for e in existing or [] if isinstance(e, dict)]
    out, dup = [], []
    for (frm, to), e in sorted(found_links.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        e["evidence"] = [q for q in e["evidence"] if q["words"] and found(q["words"], by_id[q["unit"]]["text"])]
        if not e["evidence"]:
            continue
        why = e.pop("_why")
        e["basis"] = (f"{to} names {', '.join(frm)} ({why}): '{e['evidence'][0]['words']}'. A change to "
                      f"{', '.join(frm)} may change what {to} requires. Found by tenderpack.relationships.discover in "
                      "the documents' own words; not checked by a person")
        e.update({"origin": DISCOVER_ORIGIN, "review": "proposed"})
        if any(set(e["from"]) & f and set(e["to"]) & t2 for f, t2 in have):
            dup.append(e)
            continue
        out.append(e)
    for i, e in enumerate(out, 1):
        out[i - 1] = {"id": f"REL-DISC-{i:03d}", **e}
    return {"entries": out, "unresolved": unresolved, "skipped_terms": skipped, "already_curated": dup}


def write_discovered(path, result: dict, source: str) -> Path:
    """Write discover()'s result to a NEW file for a person (never over an existing file; never the curated file):
    a relationships file whose every entry is `proposed`, plus the unresolved references and skipped terms as data."""
    p = Path(path)
    if p.exists():
        raise FileExistsError(f"{p} exists: discovery writes a new file for a person and never overwrites one")
    head = (HEADER + "# PROPOSED by `tenderpack relationships discover` from the documents' own cross-references "
            f"({source}).\n# Nothing here is confirmed or reviewed; a person copies what holds into the curated file.\n")
    body = {"prepared_by": "tenderpack relationships discover (program; not reviewed)", "method": source,
            "relationships": result["entries"], "unresolved_references": result["unresolved"],
            "skipped_terms": result["skipped_terms"],
            "already_curated": [{"from": e["from"], "to": e["to"], "kind": e["kind"]} for e in result["already_curated"]]}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(head + yaml.safe_dump(body, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    return p


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
