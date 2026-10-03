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

Matching is deterministic. A claim's object is split into the things it names ("the Proposal Due Date, the
clarification period and the number of copies"); each must be found. Cited targets ("Volume II Clauses 4.4 and Table 2-4", "Form 4-G", footnotes; the names of
the register's date anchors, e.g. "the Proposal Due Date", resolve to their defining clause) match ops on that target
or inside it. "Clarification requests a to b" match the answers Qa..Qb. Any other claim is matched by its words
against each op's provision text, target text and target heading. Only ops of a kind the verb allows are candidates,
and the best-scoring ones are taken, so one descriptive claim names one subject.
"""
from __future__ import annotations

import math
import re

from .amend import heading_of
from .citations import citations
from .textnorm import normalize_latin

# verb -> claim kind. The kind decides which ops a claim may describe (ALLOWS).
VERBS = {
    "amends": "change", "corrects": "change", "extends": "change", "reduces": "change", "increases": "change",
    "modifies": "change", "revises": "change", "varies": "change", "updates": "change",
    "deletes": "delete", "removes": "delete",
    "reinstates": "reinstate", "restores": "reinstate",
    "revokes": "revoke", "withdraws": "revoke", "cancels": "revoke",
    "adds": "add", "inserts": "add", "introduces": "add", "creates": "add", "requires": "add",
    "reissues": "replace", "replaces": "replace", "substitutes": "replace",
    "renumbers": "renumber",
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
    if o.type in ("replace_text", "set_value"):
        return "change"
    if o.type == "append_text":
        return "add"
    if o.type == "replace_unit":
        return "replace"
    if o.type == "insert_unit":
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


def summary_check(stages: list, units: list[dict], anchors: dict | None = None) -> list[dict]:
    """One record per addendum: its summary claims, what each matched, and the findings. Reads the engine's result
    only; changes nothing."""
    order = [u["unit_id"] for u in units]
    by_id = {u["unit_id"]: u for u in units}
    out = []
    for i, s in enumerate(stages[1:], 1):
        prev = stages[i - 1].state
        add = s.addendum
        sents = summary_sentences(units, add)
        rec = {"addendum": add, "stage": s.stage, "cover": sents[0][0] if sents else None,
               "page": (by_id.get(sents[0][0], {}).get("pages") or [None])[0] if sents else None,
               "sentence": " ".join(x[1] for x in sents), "claims": [], "findings": []}
        out.append(rec)
        if not sents:
            rec["findings"].append({"kind": "no summary", "detail": f"{add}'s cover has no 'This Addendum ...' sentence; "
                                    "nothing to compare"})
            continue
        ops = [x for x in s.ops if ":cover/" not in x.op.provision]
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
                        if words:
                            need = len(words) if len(words) <= 2 else math.ceil(2 * len(words) / 3)
                            # best subject: most words found (provision, target, target heading); ties go to the
                            # provision whose own text names more of them
                            scored = [((len(words & haystack(x)), len(words & set(_words(ptext_of(x.op))))), x)
                                      for x in cand if _op_class(x.op) in allowed]
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
            fit = [x for x in hit if _op_class(x.op) in allowed]
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
                    hit = [x for x in hit if _op_class(x.op) in allowed or _op_class(x.op) == "interpretation"]
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
                o, cls = x.op, _op_class(x.op)
                if not x.valid or o.review == "rejected":
                    rec["findings"].append({"kind": "claimed, not applied", "claim": c["n"], "op": o.id,
                                            "provision": o.provision, "detail":
                                            f"'{c['text']}' describes {o.id}, which is "
                                            f"{'rejected by a person' if o.review == 'rejected' else 'INVALID'} and was "
                                            "not applied" + (f" ({_failed(x)})" if not x.valid else "")})
                if c["kind"] in ("answers", "info") and cls in CHANGES | {"obligation"}:
                    rec["findings"].append({"kind": "understated", "claim": c["n"], "op": o.id, "provision": o.provision,
                                            "detail": f"'{c['text']}', but {o.id} {_does(o)}: "
                                                      f"'{_gist(s.state[o.provision].text if o.provision in s.state else '')}'"})
                if cls == "reinstate" and o.new_text and o.target in stages[0].state:
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
            o, cls = x.op, _op_class(x.op)
            if o.id in matched_by:
                continue
            if cls in CHANGES or cls == "obligation" or section(o.provision) not in covered_sections:
                ptext = ptext_of(o)
                cons = _consequence(ptext)
                rec["findings"].append({"kind": "omitted", "op": o.id, "provision": o.provision, "detail":
                                        f"{o.id} {_does(o)}; the summary does not mention it: '{_gist(ptext)}'"
                                        + (f" (it states a consequence: '{cons}')" if cons else "")
                                        + ("" if x.valid else " [op INVALID: not applied]")})
        with_op = {x.op.provision for x in s.ops}
        for c in unresolved:
            if c["provision"] in with_op:              # it has an op that failed: reported with that op, not here
                continue
            rec["findings"].append({"kind": "unchecked", "provision": c["provision"], "detail":
                                    f"{c['provision']} is unresolved (no op yet), so its effect cannot be compared with "
                                    "the summary"})
    return out


def _rangetext(rng: set[int]) -> str:
    r = sorted(rng)
    return f"{r[0]} to {r[-1]}" if len(r) > 2 and r == list(range(r[0], r[-1] + 1)) else ", ".join(map(str, r))


def _does(o) -> str:
    tgt = o.target or o.new_group or ", ".join(o.targets)
    return {"replace_text": f"amends {tgt}", "set_value": f"changes a value in {tgt}", "append_text": f"adds text to {tgt}",
            "replace_unit": f"replaces {tgt}",
            "insert_unit": f"inserts {o.new_group or 'new text'}" + (f" after {o.anchor}" if o.anchor else "")}.get(o.type) or (
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
