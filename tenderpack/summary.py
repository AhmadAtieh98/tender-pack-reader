"""C28: each addendum's cover summary compared with its actual provisions (session 07). Report only.

The summary is the sentence in an addendum's cover that begins "This Addendum <verb> ...". It is the Authority's
description of the addendum and is never applied: ops come only from the provisions (curated op files, or
tenderpack.draft, which never drafts a change from cover text). C28 reads the engine's result afterwards and
reports what a person should look at:

  omitted                    an op that changes the documents or adds an obligation and that no claim covers; also an
                             interpretation in a section no claim reaches
  understated                a claim covers the provision, but the provision does more than the claim says: an answer
                             that adds an obligation or changes text under "responds to"; a clause reinstated in an
                             amended form under "reinstates"
  consequence not mentioned  the provision states a consequence (rejection, disqualification, non-responsive,
                             returned unopened) and the claim does not mention one
  contradicted               the claim's verb does not fit what the provision does (it says "deletes", the provision
                             reinstates), or a stated range or count differs from the provisions
  not found                  a claim no provision supports
  claimed, not applied       the provision a claim describes has an op that is invalid or rejected, so nothing applied
  unchecked                  a provision still unresolved (no op yet), so its effect cannot be compared
  no summary                 the cover has no "This Addendum ..." sentence

"Unchanged" claims (session 09, blind rehearsal 02): any other cover sentence of the form "<X> is unchanged | is not
changed | is not extended | remains unchanged" is a claim of kind `unchanged` (an answer saying the same is an
answer, not a cover claim, and is left alone). X resolves through the register's date anchors (the anchor's
defining clause and, where the volume defines the name, its definition clause and the clauses that definition cites:
"Proposal Due Date means the date and time stated in Clause 6.1" -> VOL-I 2.6 and 6.1), through clause, table or form
citations, or through a table row named by its key. The claim is contradicted when an op applied at that stage
changes one of those units (text, cells or status), and the finding says what changed; supported when none does.
A subject such as "All other terms of the RFP Documents" names nothing that can change, and is not a claim.

"No date affected" claims (session 09, blind rehearsal 03): a cover sentence of the form "<X> does not affect any
deadline | the Proposal Due Date | ..." is a claim of kind `no_date_effect`. It is judged by the register's computed
dates, not by the ops: it is contradicted when a date rule in force at this stage and the one before has a different
planning date (a change inside the Working Day definition moves the clarification cut-off, which no sentence states),
and the finding names the rule, its row and the two dates. A scope naming one anchor or one rule is judged by that one.
An insert_unit at an anchor that a set_status deleted removes at the same stage counts as a substitution ("replaces").

Matching is deterministic. A claim's object is split into the things it names ("the Proposal Due Date, the
clarification period and the number of copies"); each must be found. Cited targets ("Volume II Clauses 4.4 and Table 2-4", "Form 4-G", footnotes; the names of
the register's date anchors, e.g. "the Proposal Due Date", resolve to their defining clause) match ops on that target
or inside it. "Clarification requests a to b" match the answers Qa..Qb. A claim whose words name one of the
register's date rules ("the Proposal validity period" names PROPOSAL-VALIDITY, VOL-I 7.1; it does not name
BID-BOND-VALIDITY, whose clause also mentions "the period of Proposal validity") matches the ops on that rule's source
clause first (session 09). Any other claim is matched by its words against each op's provision text, target text and
target heading. Only ops of a kind the verb allows are candidates, and the best-scoring ones are taken, so one
descriptive claim names one subject. A deletion of words with nothing put in their place is a deletion
("removes ..."), not an amendment. Claims are split at every ", <verb>" and " and <verb>" ("removes ..., re-letters
Volume I Clause 9.1").
"""
from __future__ import annotations

import math
import re

from .amend import group_members, heading_of
from .citations import citations
from .textnorm import normalize_latin

# verb -> claim kind. The kind decides which ops a claim may describe (ALLOWS).
VERBS = {
    "amends": "change", "corrects": "change", "extends": "change", "reduces": "change", "increases": "change",
    "modifies": "change", "revises": "change", "varies": "change", "updates": "change",
    # session 10 (blind rehearsal 04): verbs a cover uses for a changed limit, a split clause or a conditional change
    "relaxes": "change", "tightens": "change", "divides": "change", "splits": "change",
    "makes a conditional amendment to": "change", "makes conditional amendments to": "change",
    "deletes": "delete", "removes": "delete",
    "reinstates": "reinstate", "restores": "reinstate",
    "revokes": "revoke", "withdraws": "revoke", "cancels": "revoke",
    "adds": "add", "inserts": "add", "introduces": "add", "creates": "add", "requires": "add",
    "reissues": "replace", "re-issues": "replace", "replaces": "replace", "substitutes": "replace",
    "renumbers": "renumber", "re-numbers": "renumber", "re-letters": "renumber", "reletters": "renumber",
    "responds to": "answers", "answers": "answers",
    "publishes": "info", "confirms": "info", "clarifies": "info", "notes": "info", "records": "info", "explains": "info",
}
ALLOWS = {
    "change": {"change", "add", "replace", "delete", "reinstate", "revoke", "renumber", "obligation", "interpretation"},
    "delete": {"delete", "revoke"},
    "reinstate": {"reinstate"},
    "revoke": {"revoke", "delete"},
    "add": {"add", "obligation"},
    "replace": {"replace", "change"},
    "renumber": {"renumber"},
    "answers": {"interpretation", "none"},
    "info": {"interpretation", "none"},
}
CHANGES = {"change", "add", "replace", "delete", "reinstate", "revoke", "renumber"}
_VERB_RE = "|".join(sorted((re.escape(v) for v in VERBS), key=len, reverse=True))
# a sentence ends at a full stop followed by a capitalised word, or at the end ("Clause 5.3" does not end it)
SUMMARY_RE = re.compile(r"\bThis Addendum (?:" + _VERB_RE + r")\b.*?(?:\.(?=\s+[A-Z(‘'\"])|\.?\s*$)", re.I | re.S)
CONSEQUENCE = re.compile(r"\b(?:reject\w*|disqualif\w*|non-responsive|returned unopened|excluded from (?:the )?"
                         r"(?:evaluation|tender)|shall not be evaluated)\b", re.I)
_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
_STOP = {"the", "a", "an", "of", "to", "and", "or", "in", "on", "for", "at", "by", "with", "its", "their", "this",
         "that", "these", "those", "which", "who", "be", "is", "are", "was", "were", "been", "being", "has", "have",
         "had", "will", "shall", "may", "must", "not", "no", "than", "more", "less", "only", "also", "such", "under",
         "from", "into", "as", "it", "if", "per", "volume", "clause", "clauses", "addendum", "rfp", "documents",
         "document", "certain", "various", "all", "each", "any", "new", "existing"}
# "clarification request(s) N" names the Q&A, not a subject such as the clarification period: dropped before matching
_QA_REF = re.compile(r"\bclarification requests?\b(?:\s+\d+(?:\s*(?:to|and|,|-|–)\s*\d+)*)?", re.I)


def _stem(w: str) -> str:
    w = w.lower()
    return w[:6] if len(w) > 6 else w.rstrip("s")


def _words(s: str) -> list[str]:
    return [_stem(w) for w in re.findall(r"[A-Za-z][A-Za-z\-]+", _QA_REF.sub(" ", normalize_latin(s)))
            if w.lower() not in _STOP and w.lower() not in _NUM and w.lower() not in VERBS]


def summary_sentences(units: list[dict], addendum: str) -> list[tuple[str, str]]:
    """[(cover unit, sentence)] for every "This Addendum <verb> ..." sentence in the addendum's cover."""
    out = []
    for u in units:
        if u["doc"] == addendum and ":cover/" in u["unit_id"]:
            for m in SUMMARY_RE.finditer(normalize_latin(u.get("text") or "")):
                out.append((u["unit_id"], m.group(0).strip()))
    return out


# "<X> is unchanged | is not changed | is not extended | remains unchanged" (session 09)
UNCHANGED_RE = re.compile(r"^(?P<x>.+?)\s+(?P<verb>(?:is|are)\s+(?:unchanged|not\s+(?:changed|extended|amended|altered))|"
                          r"remains?\s+unchanged)\s*\.?$", re.I | re.S)
# a subject that names only what the addendum does not change ("All other terms of the RFP Documents") cannot be
# contradicted by any op, so it is not a claim
_TAUTOLOGY = re.compile(r"^(?:(?:all|every|any)\s+other|(?:the\s+)?(?:other|remaining))\b", re.I)


def unchanged_claims(text: str) -> list[dict]:
    """Cover sentences stating that something did not change ('The Proposal Due Date is unchanged.'). A 'This Addendum
    ...' sentence is the summary, never one of these."""
    out = []
    for sent in re.split(r"(?<=[.;])\s+(?=[A-Z(‘'\"])", normalize_latin(text or "")):
        sent = sent.strip()
        m = UNCHANGED_RE.match(sent)
        if not m or re.match(r"This Addendum\b", sent, re.I) or _TAUTOLOGY.match(m.group("x").strip()):
            continue
        out.append({"verb": " ".join(m.group("verb").split()).lower(), "kind": "unchanged",
                    "object": m.group("x").strip(), "text": sent.rstrip(".").strip()})
    return out


# "<X> does not affect any deadline | the Proposal Due Date | ..." (session 09, blind rehearsal 03): a claim that no
# computed date moves. It is judged by the register's date rules, never by the ops: a change inside a definition
# ("Working Day") moves a deadline that no sentence of the addendum states
NO_DATE_EFFECT_RE = re.compile(r"^(?P<x>.+?)\s+(?P<verb>(?:does|do)\s+not\s+affect|affects?\s+no|(?:has|have)\s+no\s+"
                               r"effect\s+on)\s+(?P<scope>.+?)\s*\.?$", re.I | re.S)
_DATE_WORDS = re.compile(r"\b(?:deadlines?|dates?|periods?|cut-?offs?|time\s*limits?|timetable|programme)\b", re.I)


def no_date_effect_claims(text: str) -> list[dict]:
    """Cover sentences stating that no date is affected ('The closure of the Authority's offices does not affect any
    deadline under the RFP Documents.'). The scope must speak of dates, deadlines or periods."""
    out = []
    for sent in re.split(r"(?<=[.;])\s+(?=[A-Z(‘'\"])", normalize_latin(text or "")):
        sent = sent.strip()
        m = NO_DATE_EFFECT_RE.match(sent)
        if not m or re.match(r"This Addendum\b", sent, re.I) or not _DATE_WORDS.search(m.group("scope")):
            continue
        out.append({"verb": " ".join(m.group("verb").split()).lower(), "kind": "no_date_effect",
                    "object": m.group("x").strip(), "scope": m.group("scope").strip(), "text": sent.rstrip(".").strip()})
    return out


def date_changes_by_stage(evals: list[dict], order: list[str]) -> dict[str, list[dict]]:
    """{stage: [{row, rule_id, old, new, anchor, source_unit}]}: every date rule in force at a stage and at the one
    before whose planning date differs, from the register's evaluations (Register.all()). Event-dependent rules
    without a date are left out."""
    out: dict[str, list[dict]] = {}
    for e in evals:
        for a, b in zip(order, order[1:]):
            sa, sb = e["stages"].get(a), e["stages"].get(b)
            if not (sa and sb and sa.get("active") and sb.get("active")):
                continue
            was = {d["rule_id"]: d for d in sa.get("dates", [])}
            for d in sb.get("dates", []):
                p = was.get(d["rule_id"])
                old, new = (p or {}).get("planning", {}).get("value"), d.get("planning", {}).get("value")
                if p and old and new and old != new:
                    out.setdefault(b, []).append({"row": e["row"].id, "rule_id": d["rule_id"], "old": old, "new": new,
                                                  "anchor": d.get("anchor"),
                                                  "source_unit": d.get("source_unit") or d.get("unit") or ""})
    return out


def _check_no_date_effect(rec: dict, stage: str, cover_units: list[dict], date_changes: dict | None, anchors: dict,
                          rules: dict | None) -> None:
    """Add the addendum's '<X> does not affect any deadline' claims to `rec`. A scope that names one anchor ('the
    Proposal Due Date') is judged by that anchor's own rule; one that names a date rule by that rule; 'any deadline'
    by every rule whose planning date moved at this stage. Without `date_changes` (an older caller) the claim is
    reported unchecked."""
    for u in cover_units:
        for c in no_date_effect_claims(u.get("text") or ""):
            c["n"] = len(rec["claims"]) + 1
            changes = None if date_changes is None else list(date_changes.get(stage, []))
            named_anchor = [k for k, a in (anchors or {}).items()
                            if a.get("name") and re.search(r"\b" + re.escape(a["name"]) + r"\b", c["scope"], re.I)]
            named_rules = [] if named_anchor else _named_rules(set(_words(c["scope"])), rules)
            if changes is not None and (named_anchor or named_rules):
                changes = [d for d in changes if d["rule_id"] in (named_anchor or named_rules)]
            c.update({"targets": named_anchor or named_rules, "matched": [d["rule_id"] for d in changes or []],
                      "matched_provisions": [],
                      "status": "not checked" if changes is None else "contradicted" if changes else "supported"})
            rec["claims"].append(c)
            rec["sentence"] = (rec["sentence"] + " " + c["text"] + ".").strip()
            if changes is None:
                rec["findings"].append({"kind": "unchecked", "claim": c["n"], "detail":
                                        f"'{c['text']}': the computed dates were not available to compare"})
            for d in changes or []:
                rec["findings"].append({"kind": "contradicted", "claim": c["n"], "detail":
                                        f"'{c['text']}', but {d['rule_id']} (row {d['row']}"
                                        + (f", {_ref(d['source_unit'])}" if d.get("source_unit") else "")
                                        + f") moves from {d['old']} to {d['new']}"})


def rule_index(rows) -> dict:
    """The register's date rules as summary_check reads them: {rule_id: {source_unit, text, purpose}}."""
    return {d.rule_id: {"source_unit": d.source_unit, "text": d.text, "purpose": d.purpose} for r in rows
            for d in r.date_rules}


def _named_rules(words: set[str], rules: dict | None) -> list[str]:
    """Source units of the date rules a claim names: every word of the rule's id (or of a purpose of two or more words)
    is among the claim's words ('the Proposal validity period' names PROPOSAL-VALIDITY, not BID-BOND-VALIDITY or
    PROPOSAL-VALIDITY-F4A). The rules naming the most words win."""
    best, out = 0, []
    for rid, r in sorted((rules or {}).items()):
        for name in (rid, r.get("purpose") or ""):
            toks = {_stem(t) for t in re.split(r"[-_\s]+", name) if t and t.lower() not in _STOP}
            if len(toks) < 2 or not toks <= words:
                continue
            if len(toks) > best:
                best, out = len(toks), []
            if len(toks) == best and r["source_unit"] not in out:
                out.append(r["source_unit"])
    return out


def _definition(state, doc: str, name: str) -> str | None:
    """The clause of `doc` that defines `name` ('Proposal Due Date means the date and time stated in Clause 6.1 ...')."""
    rx = re.compile(r"^\W*" + re.escape(name) + r"\W*\s+(?:means|shall mean|has the meaning)\b", re.I)
    return next((k for k, u in state.items() if u.doc == doc and u.status == "active" and u.kind != "heading"
                 and rx.match(normalize_latin(u.text or ""))), None)


def _subject_units(obj: str, anchors: dict, state) -> tuple[list[str], list[str]]:
    """What an 'X is unchanged' claim is about: (units, definition units). X is a cited clause, table or form; the name
    of a register date anchor (its defining clause, the volume's definition of the name and the clauses that definition
    cites); or the key of a table row ('BOD5')."""
    t = _expand(obj)
    cites = citations(t)
    units = [c.target for c in cites]
    rest = t
    for c in cites:
        rest = rest.replace(c.text, " ")
    defs: list[str] = []
    for a in (anchors or {}).values():
        name = a.get("name")
        if not name or not re.search(r"\b" + re.escape(name) + r"\b", rest, re.I):
            continue
        units.append(a["defined_in"])
        doc = a["defined_in"].split(":")[0]
        d = _definition(state, doc, name)
        if d:
            defs.append(d)
            units += [d] + [f"{doc}:{n}" for n in re.findall(r"\bClause (\d+(?:\.\d+)*)", state[d].text)]
    if not units:
        key = re.sub(r"^(?:the|a|an)\s+", "", normalize_latin(obj), flags=re.I).strip().lower()
        units = [k for k, u in state.items() if key and u.kind == "table_row" and u.status == "active"
                 and not u.doc.startswith("ADD-") and key in ((u.label or "").lower(),
                                                              str(next(iter((u.cells or {}).values()), "")).lower())]
    return list(dict.fromkeys(units)), defs


def _ref(uid: str) -> str:
    doc, _, local = (uid or "").partition(":")
    return f"{doc} {local}" if local else uid


def _change_words(o) -> str:
    """What an op did to a unit, in the provision's own words where it quotes them."""
    if o.type == "replace_text" and o.old is not None:
        return (f"{o.id} replaces '{_short(o.old, 90)}' with '{_short(o.new, 90)}' in {_ref(o.target)}" if o.new else
                f"{o.id} deletes '{_short(o.old, 120)}' from {_ref(o.target)}")
    return f"{o.id} {_does(o)}"


def _check_unchanged(rec: dict, s, prev, cover_units: list[dict], anchors: dict) -> None:
    """Add the addendum's 'X is unchanged' claims to `rec`: contradicted when an op applied at this stage changes one
    of X's units (text, cells or status), supported when none does, not checked when X resolves to nothing."""
    for u in cover_units:
        for c in unchanged_claims(u.get("text") or ""):
            c["n"] = len(rec["claims"]) + 1
            targets, defs = _subject_units(c["object"], anchors, prev)
            targets = [t for t in targets if t in prev or group_members(prev, t)]      # only what exists can be checked
            members = {k for t in targets for k in ([t] if t in prev else []) + group_members(prev, t)}
            hit = [x for x in s.ops if x.applied and set(x.changed) & members]
            c.update({"targets": targets, "matched": [x.op.id for x in hit], "matched_provisions": [],
                      "status": "contradicted" if hit else "supported" if targets else "not checked"})
            rec["claims"].append(c)
            rec["sentence"] = (rec["sentence"] + " " + c["text"] + ".").strip()
            if not targets:
                rec["findings"].append({"kind": "unchecked", "claim": c["n"], "detail":
                                        f"'{c['text']}': the subject is not a clause, table, form, row key or date "
                                        "anchor the program can resolve; a person compares it with the provisions"})
            defined = "".join(f"; {_ref(d)}: '{_short(prev[d].text, 160)}'" for d in defs)
            for x in hit:
                rec["findings"].append({"kind": "contradicted", "claim": c["n"], "op": x.op.id, "provision": x.op.provision,
                                        "detail": f"'{c['text']}', but {_change_words(x.op)}{defined}"})


def _expand(obj: str) -> str:
    """'Volume II Clauses 4.4 and Table 2-4' -> 'Volume II Clause 4.4 and Volume II Table 2-4' (citations() reads the
    singular forms); a bare 'Clause N' or 'Table N-N' after a volume takes that volume."""
    obj = re.sub(r"\b(Volume (?:I{1,3}|IV|V)) Clauses ((?:\d+(?:\.\d+)*)(?:(?:, | and )\d+(?:\.\d+)*)*)",
                 lambda m: " and ".join(f"{m.group(1)} Clause {n}" for n in re.split(r", | and ", m.group(2))), obj)
    obj = re.sub(r"\b(Volume (?:I{1,3}|IV|V)) Tables (\d+-\d+(?:(?:, | and )\d+-\d+)*)",
                 lambda m: " and ".join(f"{m.group(1)} Table {n}" for n in re.split(r", | and ", m.group(2))), obj)
    vol = None
    out = []
    for tok in re.split(r"(\bVolume (?:I{1,3}|IV|V)\b|\b(?:Clause|Table) \d[\d.\-]*)", obj):
        m = re.fullmatch(r"Volume (I{1,3}|IV|V)", tok or "")
        if m:
            vol = tok
        elif tok and re.fullmatch(r"(?:Clause|Table) \d[\d.\-]*", tok) and vol and not "".join(out).endswith(vol + " "):
            tok = f"{vol} {tok}"
        out.append(tok or "")
    return "".join(out)


def parse_claims(sentence: str) -> list[dict]:
    body = re.sub(r"^This Addendum\s+", "", sentence.strip().rstrip("."), flags=re.I)
    verb_at = re.compile(r"(?:and\s+)?(" + _VERB_RE + r")\b\s*(.*)", re.I)
    claims: list[dict] = []
    for piece in re.split(r",\s*|\s+and\s+(?=(?:" + _VERB_RE + r")\b)", body):
        piece = piece.strip()
        if not piece:
            continue
        m = verb_at.fullmatch(piece)
        if m:
            verb = m.group(1).lower()
            claims.append({"verb": verb, "kind": VERBS[verb], "object": m.group(2).strip()})
        elif claims:
            claims[-1]["object"] += ", " + re.sub(r"^and\s+", "", piece)
    for i, c in enumerate(claims, 1):
        c["n"] = i
        c["text"] = f"{c['verb']} {c['object']}"
    return claims


def _items(obj: str) -> list[str]:
    """A claim's object split into the things it names: at commas, and at 'and' when a new item starts there
    ('the Bid Bond amount and the number of copies'; 'Volume II Table 2-4 and Volume II Table 2-6'), never inside
    one descriptive phrase ('terms and conditions')."""
    t = _expand(obj)
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+(?=(?:the|a|an|Volume|Form|Table|Clause|footnote|Footnote|Appendix)\b)", t)
    return [x.strip() for x in parts if x.strip()]


def _claim_targets(obj: str, anchors: dict) -> tuple[list[str], str]:
    """Targets cited by a claim, and the words left for descriptive matching."""
    t = _expand(obj)
    cites = citations(t)
    targets = [c.target for c in cites]
    rest = t
    for c in cites:
        rest = rest.replace(c.text, " ")
    for a in (anchors or {}).values():
        if a.get("name") and re.search(r"\b" + re.escape(a["name"]) + r"\b", rest, re.I):
            targets.append(a["defined_in"])
            rest = re.sub(re.escape(a["name"]), " ", rest, flags=re.I)
    return targets, rest


def _answers(obj: str) -> set[int] | None:
    m = re.search(r"clarification requests? (\d+)(?:\s*(?:to|-|–)\s*(\d+)|((?:\s*(?:,|and)\s*\d+)+))?", obj, re.I)
    if not m:
        return None
    a = int(m.group(1))
    if m.group(2):
        return set(range(a, int(m.group(2)) + 1))
    return {a} | {int(x) for x in re.findall(r"\d+", m.group(3) or "")}


def _count(obj: str) -> int | None:
    m = re.search(r"\b(" + "|".join(_NUM) + r"|\d+)\s+(?:[a-z\-]+\s+){0,3}?(?:requirements?|clauses?|provisions?|"
                  r"forms?|tables?|items?|criteria|obligations?)\b", obj, re.I)
    if not m:
        return None
    return _NUM.get(m.group(1).lower()) or int(m.group(1))


def _op_class(o) -> str:
    if o.type == "set_status":
        return {"deleted": "delete", "reinstated": "reinstate", "revoked": "revoke"}[o.status]
    if o.type == "replace_text" and o.old is not None and not (o.new or "").strip():
        return "delete"                                # words deleted, nothing put in their place ("removes ...")
    if o.type in ("replace_text", "set_value"):
        return "change"
    if o.type == "append_text":
        return "add"
    if o.type == "replace_unit":
        return "replace"
    if o.type in ("insert_unit", "insert_row"):
        return "add"
    return {"adds_obligation": "obligation", "renumbers": "renumber"}.get(o.effect or "", "interpretation")


def _op_keys(o, ptext: str = "") -> list[str]:
    keys = [k for k in [o.target, o.new_group, o.anchor, *o.targets] if k]
    m = re.search(r"\bnew Clause (\d+(?:\.\d+)*)", ptext or "")
    if o.type == "insert_unit" and o.anchor and m:          # the number the inserted clause is given
        keys.append(f"{o.anchor.split(':')[0]}:{m.group(1)}")
    return keys


def _hits(claim_target: str, key: str) -> bool:
    if key == claim_target or key.startswith((claim_target + "/", claim_target + "#", claim_target + "(")):
        return True
    m1, m2 = re.search(r":F(\d-[A-Z])$", claim_target), re.search(r":F(\d-[A-Z])(?:$|/)", key)
    return bool(m1 and m2 and m1.group(1) == m2.group(1))          # Form 4-G in VOL-IV or added by an addendum


def _target_text(state, order, key: str) -> str:
    u = state.get(key)
    if u is None and ":" in key:
        doc, local = key.split(":", 1)
        u = state.get(f"{doc}:H:{local.split('/')[0]}")
    if u is None:
        return ""
    try:
        head = heading_of(order, state, u.unit_id)
    except ValueError:                                  # a unit an op inserted: not in the printed order
        head = ""
    return f"{u.text[:400]} {head}"


def summary_check(stages: list, units: list[dict], anchors: dict | None = None, rules: dict | None = None,
                  date_changes: dict | None = None) -> list[dict]:
    """One record per addendum: its summary claims, what each matched, and the findings. Reads the engine's result
    only; changes nothing. `anchors` are the register's date anchors ({PDD: {name, defined_in}}); `rules` its date rules
    ({rule_id: {source_unit, text, purpose}}, rule_index); `date_changes` the computed dates that moved at each stage
    (date_changes_by_stage), for the 'does not affect any deadline' claims."""
    order = [u["unit_id"] for u in units]
    by_id = {u["unit_id"]: u for u in units}
    out = []
    for i, s in enumerate(stages[1:], 1):
        prev = stages[i - 1].state
        add = s.addendum
        sents = summary_sentences(units, add)
        covers = [u for u in units if u["doc"] == add and ":cover/" in u["unit_id"]]
        rec = {"addendum": add, "stage": s.stage, "cover": sents[0][0] if sents else None,
               "page": (by_id.get(sents[0][0], {}).get("pages") or [None])[0] if sents else None,
               "sentence": " ".join(x[1] for x in sents), "claims": [], "findings": []}
        out.append(rec)
        if not sents:
            rec["findings"].append({"kind": "no summary", "detail": f"{add}'s cover has no 'This Addendum ...' sentence; "
                                    "nothing to compare"})
            _check_unchanged(rec, s, prev, covers, anchors or {})
            _check_no_date_effect(rec, s.stage, covers, date_changes, anchors or {}, rules)
            continue
        ops = [x for x in s.ops if ":cover/" not in x.op.provision]
        # an insert_unit at an anchor that a set_status deleted removes at the same stage is a substitution (the
        # replacement of the Form 4-C declaration in blind rehearsal 03): both ops are of class "replace"
        subst = ({x.op.target for x in s.ops if x.op.type == "set_status" and x.op.status == "deleted"}
                 & {x.op.anchor for x in s.ops if x.op.type == "insert_unit" and x.op.anchor})

        def cls(x) -> str:
            o = x.op
            if (o.type == "insert_unit" and o.anchor in subst) or \
                    (o.type == "set_status" and o.status == "deleted" and o.target in subst):
                return "replace"
            return _op_class(o)
        no_effect = [c for c in s.coverage if c["disposition"] == "no_effect" and ":cover/" not in c["provision"]]
        unresolved = [c for c in s.coverage if c["disposition"] in ("unresolved", "UNACCOUNTED")
                      and ":cover/" not in c["provision"]]
        answers_here = {int(m.group(1)): c["provision"] for c in s.coverage
                        if (m := re.search(r":Q(\d+)$", c["provision"]))}

        def section(prov: str) -> str:
            try:
                return heading_of(order, s.state, prov)
            except (KeyError, ValueError):
                return ""

        def ptext_of(o) -> str:
            return s.state[o.provision].text if o.provision in s.state else ""

        def keys(x) -> list[str]:
            return _op_keys(x.op, ptext_of(x.op))

        def haystack(x) -> set[str]:
            o = x.op
            text = " ".join([ptext_of(o)] + [_target_text(prev if k in prev else s.state, order, k) for k in keys(x)])
            return set(_words(text))

        matched_by: dict[str, list[int]] = {}
        covered_sections: set[str] = set()
        for c in (cl for _, sent in sents for cl in parse_claims(sent)):
            c["n"] = len(rec["claims"]) + 1
            rng = _answers(c["object"]) if c["kind"] == "answers" else None
            allowed = ALLOWS[c["kind"]]
            hit: list = []
            hit_prov: list[str] = []
            all_targets: list[str] = []
            missing: list[str] = []
            cnt = None
            if rng is not None:
                hit_prov = [answers_here[q] for q in sorted(rng) if q in answers_here]
                hit = [x for x in ops if x.op.provision in hit_prov]
                if rng != set(answers_here):
                    rec["findings"].append({"kind": "contradicted", "claim": c["n"], "detail":
                                            f"'{c['text']}': the summary names requests {_rangetext(rng)}; the "
                                            f"addendum answers {', '.join(map(str, sorted(answers_here))) or 'none'}"})
            else:
                for item in _items(c["object"]):
                    targets, rest = _claim_targets(item, anchors or {})
                    all_targets += targets
                    ih, ip = [], []
                    # an answer is described by "responds to clarification requests ...", never by another claim
                    cand = [x for x in ops if not re.search(r":Q\d+$", x.op.provision)]
                    if targets:
                        ih = [x for x in cand if any(_hits(t, k) for t in targets for k in keys(x))]
                    else:
                        cnt = _count(rest) if cnt is None else cnt
                        words = set(_words(rest))
                        named = _named_rules(words, rules)        # a date rule the claim names: its clause first
                        if named:
                            ih = [x for x in cand if cls(x) in allowed
                                  and any(_hits(t, k) for t in named for k in keys(x))]
                            all_targets += named if ih else []
                        if words and not ih:
                            need =len(words) if len(words) <= 2 else math.ceil(2 * len(words) / 3)
                            # best subject: most words found (provision, target, target heading); ties go to the
                            # provision whose own text names more of them
                            scored = [((len(words & haystack(x)), len(words & set(_words(ptext_of(x.op))))), x)
                                      for x in cand if cls(x) in allowed]
                            best = max((n for n, _ in scored), default=(0, 0))
                            ih = [x for n, x in scored if n[0] >= need and n == best]
                            if "none" in allowed:
                                ip = [p["provision"] for p in no_effect
                                      if len(words & set(_words(f"{p['text']} {section(p['provision'])}"))) >= need]
                    if not ih and not ip:
                        missing.append(item)
                    hit += [x for x in ih if x not in hit]
                    hit_prov += [q for q in ip if q not in hit_prov]
            c.update({"targets": all_targets, "matched": [x.op.id for x in hit], "matched_provisions": hit_prov})
            if not hit and not hit_prov:
                c["status"] = "not found"
                rec["findings"].append({"kind": "not found", "claim": c["n"], "detail":
                                        f"'{c['text']}': no provision of {add} does this"})
                rec["claims"].append(c)
                continue
            for item in missing:
                rec["findings"].append({"kind": "not found", "claim": c["n"], "detail":
                                        f"'{c['text']}': no provision of {add} matches '{item}'"})
            fit = [x for x in hit if cls(x) in allowed]
            if not fit and not hit_prov:
                c["status"] = "contradicted"
                for x in hit:
                    rec["findings"].append({"kind": "contradicted", "claim": c["n"], "op": x.op.id,
                                            "provision": x.op.provision, "detail":
                                            f"'{c['text']}', but {x.op.id} {_does(x.op)}"})
            else:
                c["status"] = "supported"
                if c["kind"] not in ("answers", "info"):
                    # an op on the same target that the verb does not describe (a renumbering under "inserts") is not
                    # covered by this claim, so it can still be reported as omitted. Answers keep every op: one that
                    # changes or adds something is reported as understated below
                    hit = [x for x in hit if cls(x) in allowed or cls(x) == "interpretation"]
                    c["matched"] = [x.op.id for x in hit]
            if cnt is not None and c["kind"] in ("delete", "reinstate", "revoke", "add", "replace"):
                n_ok = len({x.op.provision for x in fit})
                if n_ok != cnt:
                    rec["findings"].append({"kind": "contradicted", "claim": c["n"], "detail":
                                            f"'{c['text']}': the summary counts {cnt}; the provisions do it {n_ok} "
                                            f"time(s) ({', '.join(x.op.id for x in fit) or 'none'})"})
            if any(f.get("claim") == c["n"] and f["kind"] == "contradicted" for f in rec["findings"]):
                c["status"] = "contradicted"
            elif missing:
                c["status"] = "partly found"
            for x in hit:
                matched_by.setdefault(x.op.id, []).append(c["n"])
                covered_sections.add(section(x.op.provision))
                o, kind = x.op, cls(x)
                if not x.applied:
                    rec["findings"].append({"kind": "claimed, not applied", "claim": c["n"], "op": o.id,
                                            "provision": o.provision, "detail":
                                            f"'{c['text']}' describes {o.id}, which is "
                                            f"{'rejected by a person (withheld)' if x.withdrawn else 'INVALID'} and was "
                                            "not applied" + (f" ({_failed(x)})" if not x.valid else "")})
                if c["kind"] in ("answers", "info") and kind in CHANGES | {"obligation"}:
                    rec["findings"].append({"kind": "understated", "claim": c["n"], "op": o.id, "provision": o.provision,
                                            "detail": f"'{c['text']}', but {o.id} {_does(o)}: "
                                                      f"'{_gist(s.state[o.provision].text if o.provision in s.state else '')}'"})
                if kind == "reinstate" and o.new_text and o.target in stages[0].state:
                    before = _norm(stages[0].state[o.target].text)
                    if _norm(o.new_text) != before:
                        rec["findings"].append({"kind": "understated", "claim": c["n"], "op": o.id,
                                                "provision": o.provision, "detail":
                                                f"'{c['text']}', but {o.id} reinstates it in an amended form: "
                                                f"'{_short(o.new_text, 200)}' (as issued: '{_short(stages[0].state[o.target].text, 160)}')"})
                cons = _consequence(ptext_of(o))
                done = {(f["kind"], f.get("provision"), f.get("claim")) for f in rec["findings"]}
                if cons and not CONSEQUENCE.search(c["text"]) and \
                        ("consequence not mentioned", o.provision, c["n"]) not in done:
                    rec["findings"].append({"kind": "consequence not mentioned", "claim": c["n"], "op": o.id,
                                            "provision": o.provision, "detail":
                                            f"{o.provision} states '{cons}'; the summary says only '{c['text']}'"})
            for p in hit_prov:
                covered_sections.add(section(p))
            rec["claims"].append(c)
        for x in ops:
            o, kind = x.op, cls(x)
            if o.id in matched_by:
                continue
            if kind in CHANGES or kind == "obligation" or section(o.provision) not in covered_sections:
                ptext = ptext_of(o)
                cons = _consequence(ptext)
                rec["findings"].append({"kind": "omitted", "op": o.id, "provision": o.provision, "detail":
                                        f"{o.id} {_does(o)}; the summary does not mention it: '{_gist(ptext)}'"
                                        + (f" (it states a consequence: '{cons}')" if cons else "")
                                        + ("" if x.applied else " [op withheld after a rejection: not applied]"
                                           if x.valid else " [op INVALID: not applied]")})
        with_op = {x.op.provision for x in s.ops}
        for c in unresolved:
            if c["provision"] in with_op:              # it has an op that failed: reported with that op, not here
                continue
            rec["findings"].append({"kind": "unchecked", "provision": c["provision"], "detail":
                                    f"{c['provision']} is unresolved (no op yet), so its effect cannot be compared with "
                                    "the summary"})
        _check_unchanged(rec, s, prev, covers, anchors or {})
        _check_no_date_effect(rec, s.stage, covers, date_changes, anchors or {}, rules)
    return out


def _rangetext(rng: set[int]) -> str:
    r = sorted(rng)
    return f"{r[0]} to {r[-1]}" if len(r) > 2 and r == list(range(r[0], r[-1] + 1)) else ", ".join(map(str, r))


def _does(o) -> str:
    tgt = o.target or o.new_group or ", ".join(o.targets)
    return {"replace_text": f"amends {tgt}" if o.new or o.old is None else f"deletes words from {tgt}", "set_value": f"changes a value in {tgt}", "append_text": f"adds text to {tgt}",
            "replace_unit": f"replaces {tgt}",
            "insert_row": f"adds a row to {tgt}" + (f" after {o.after}" if o.after else ""),
            "insert_unit":f"inserts {o.new_group or 'new text'}" + (f" after {o.anchor}" if o.anchor else "")}.get(o.type) or (
        f"{ {'deleted': 'deletes', 'reinstated': 'reinstates', 'revoked': 'ends the effect of'}[o.status]} {tgt}"
        if o.type == "set_status" else
        {"adds_obligation": f"adds an obligation ({tgt})", "renumbers": f"renumbers {tgt}"}.get(o.effect or "",
                                                                                           f"{o.effect or 'annotates'} {tgt}"))


def _failed(x) -> str:
    return "; ".join(f"{c['id']}: {c['detail'][:100]}" for c in x.checks if not c["ok"])


def _norm(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"^\s*\d+(?:\.\d+)*\s+", "", normalize_latin(t or ""))).strip().lower()


def _short(t: str, n: int) -> str:
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def _consequence(t: str) -> str:
    """The first sentence stating a consequence, not counting one that says the consequence is unchanged."""
    for sent in re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", t or "")):
        if CONSEQUENCE.search(sent) and not re.search(r"\b(?:unchanged|remains?|continues? to apply)\b", sent, re.I):
            return _short(sent.strip("’'\" "), 200)
    return ""


def _gist(t: str) -> str:
    """The words a person needs: an answer's response rather than the question; up to 240 characters."""
    m = re.search(r"Authority response:\s*(.*)", t or "", re.S)
    return _short(m.group(1) if m else t, 240)
