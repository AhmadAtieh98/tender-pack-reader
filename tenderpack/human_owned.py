"""Judgments a person owns (session 12, the owner's part 1; the brief's section 6: "Letting the tool decide a commercial
or legal question that a person has to own" is a failure; surfacing it to a human is the job).

Extraction and calculation run automatically; a legal or commercial judgment is never made or settled by the program.
A verbatim quotation proves that the words are in the pack, not that a conclusion drawn from them is right: valid
evidence never validates the conclusion. This module is the ONE place that says which proposals are human-owned, used
by both AI phases (tenderpack.ai.controller for the analysis phase, tenderpack.ai.downstream for the downstream phase)
and by every renderer (clarify, programme, stage2, the workflow's review packet).

Human-owned (decided by the item's TYPE and its CONTENT, never by the model's own label or status):
  by type      an issue (issues are matters kept open for people: "Issues are never resolved by the program"); a
               clarification entry that re-reads an EXISTING question (a person compares the two), or that carries a
               response status other than the one the register holds, or an answer (declaring a question answered or
               withdrawn is a person's decision; recording that an addendum responds to it is not); an annotation op
               whose effect interprets, confirms or changes nothing when its words raise a trigger below (a precedence
               answer, a waiver, an ambiguity closed).
  by content   the model's own prose (never the verbatim quotations, which are checked as evidence) uses a word of
               TRIGGERS: resolved/settled/closed, prevails/governs/precedence, waived/no longer required,
               answered/withdrawn, "means"/"is to be read as", deemed/taken as accepted, "no conflict".
               The list is deliberately conservative: a false positive costs a person one look; a false negative
               would let a model's conclusion pass as verified.
A human-owned item is never `evidence_verified`: its status is `interpretation_pending` (promotable as a PROPOSAL,
nothing applied as settled), and its validation records say "evidence verified; conclusion is a human decision" with
the reasons. Deterministic facts stay `evidence_verified`: a verbatim quotation of a fact, a computed date, an
evidence item whose own words raise no trigger.

Settled only by a recorded decision: a clarification entry whose response status closes the question ("answered by
addendum", "withdrawn (not sent)") or an issue that carries a `status`/`resolution` is presented as settled only when
a person's decision (`tenderpack accept CQ-... | I-...`, tenderpack.review) is bound to the entry exactly as it now
reads; otherwise every output shows HUMAN_DECISION_PENDING and the question stays open (A5's gates included). A curated
issue whose own words (quotations aside: own_words) assert a judgment, i.e. use a topic word of TRIGGERS (which document
prevails, which clause governs, what a term means), is labelled HUMAN_DECISION_PENDING the same way until a person's
decision is bound to it (session 12, F1; audit A1-1/A2-1/A3-1: the concession term). Session 12
(F5; audit A3-5, R-a, R1-1): so is a curated issue that a pending decision of the clarification register links
(pending_links: the register says such a point is shown as HUMAN DECISION PENDING), and one whose decision owner (else
owner) is Legal or Commercial (owner_judgment). pending_reasons is the one rule: A1's Issues sheet, the A3 page (⚑)
and a3_detail.html, A4's pending section, and A2/A5's NOT SETTLED for the rows such an issue is linked to
(signals.attach_pending) all read it. An answer
the AI workflow recorded from an addendum (`recorded_answer`) is shown as "answer recorded ... whether it resolves the
question is a human decision". The workflow never records a decision; only a person running `accept` does."""
from __future__ import annotations

import hashlib
import json
import re

HUMAN_DECISION_PENDING = "HUMAN DECISION PENDING"
EVIDENCE_NOT_CONCLUSION = "evidence verified; conclusion is a human decision"
CHECK = "human-owned"                         # the ValidationRecord.check that marks a human-owned item
MARKER = "human_decision"                     # the field promotion writes on a human-owned issue or clarification entry
PROPOSED_STATUS = "proposed_response_status"  # a response status a proposal asked for, kept beside the entry, never applied
DRAFT = "draft, not sent"
CLOSING_STATES = ("answered by addendum", "withdrawn (not sent)")   # clarify.RESPONSE_STATES that close a question

# The trigger words, each with what it signals and its kind. Matched case-insensitively on the model's own prose only
# (quotations are evidence, checked verbatim elsewhere). Conservative on purpose: see the module docstring.
#   closure  the words declare a matter decided, closed, waived, answered or withdrawn
#   topic    the words put a legal or commercial judgment in play (precedence, which clause governs, what a term means)
TRIGGERS: tuple[tuple[str, str, str], ...] = (
    (r"\bresolv(?:e|es|ed|ing)\b|\bresolution\b", "declares a matter resolved", "closure"),
    (r"\bsettl(?:e|es|ed|ing)\b", "declares a matter settled", "closure"),
    (r"\b(?:is|are|now|be|been|considered|treated as|remains?)\s+closed\b|\bclos(?:e|es|ed|ing) (?:the|this|that) "
     r"(?:question|issue|ambiguity|matter|conflict|gap)\b", "declares a matter closed", "closure"),
    (r"\bwaiv(?:e|es|ed|er|ing)\b", "a waiver", "closure"),
    (r"\bno longer (?:required|applies|apply|applicable|needed|relevant|necessary|an issue|open)\b",
     "declares an obligation or a question ended", "closure"),
    (r"\banswered\b", "declares a question answered", "closure"),
    (r"\bwithdraw(?:n|s|al)?\b", "withdraws a question", "closure"),
    (r"\bno (?:further |remaining )?(?:conflict|ambiguity|discrepancy|inconsistency)\b|"
     r"\b(?:conflicts?|ambiguit(?:y|ies)|discrepanc(?:y|ies)|inconsistenc(?:y|ies))\s+(?:is|are|has been|have been)\s+"
     r"(?:removed|eliminated|cured|cleared|addressed|reconciled)\b", "declares a conflict or an ambiguity gone", "closure"),
    (r"\bprevail(?:s|ed|ing)?\b|\btakes? (?:precedence|priority)\b", "decides which document prevails (precedence)",
     "topic"),
    (r"\bprecedence\b", "a precedence question", "topic"),
    (r"\bgovern(?:s|ed|ing)?\b", "decides which clause governs", "topic"),
    (r"\b(?:is|are) to be (?:read|construed|understood|interpreted)\b|\bshall be (?:read|construed|interpreted)\b|"
     r"\bmeans\b|\bmust be read\b", "interprets a term (legal or commercial interpretation)", "topic"),
    (r"\bdeemed\b|\btaken as accepted\b", "a deemed acceptance (legal effect)", "topic"),
)
_TRIGGERS = tuple((re.compile(p, re.I), why, kind) for p, why, kind in TRIGGERS)
# fields whose text is a verbatim quotation (evidence), never the model's own conclusion
QUOTE_KEYS = ("words", "quote", "sources", "evidence", "answer", "recorded_answer", "referenced_in", "source")


# session 14 (W4; blind-07 COMPARISON section 8 item 14): a closure word under a negation in its own clause ("unit not
# resolved", "has not been settled", "whether it resolves") declares nothing closed. NEGATION: the words that negate or
# make conditional what follows them; the window is the clause before the match (cut at . ; : ! ? , | or a line break)
# and at most NEGATION_WINDOW words. Topic words are not affected: a negated precedence statement ("Volume I does not
# prevail") still puts the judgment in play.
NEGATION = re.compile(r"^(?:not|never|no|nor|neither|without|cannot|whether|if|until|unless|yet|\w+n't)$", re.I)
NEGATION_WINDOW = 5
_CLAUSE_CUT = re.compile(r"[.;:!?,|\n]")


def negated(text: str, start: int, window: int = NEGATION_WINDOW) -> bool:
    """Whether the word at `start` in `text` stands under a negation (NEGATION) among the `window` words before it in
    its own clause. Session 14 (W4)."""
    head = str(text or "")[:start]
    cuts = [m.end() for m in _CLAUSE_CUT.finditer(head)]
    clause = head[cuts[-1]:] if cuts else head
    return any(NEGATION.match(w) for w in re.findall(r"[A-Za-z']+", clause)[-window:])


def triggers(text: str, kinds: tuple[str, ...] = ("closure", "topic")) -> list[str]:
    """What the words signal ([] when nothing). `text` is the model's own prose; `kinds` limits the triggers. Session 14
    (W4): a closure word counts only where it is asserted (the first occurrence not negated: negated())."""
    out = []
    t = str(text or "")
    for rx, why, kind in _TRIGGERS:
        if kind not in kinds:
            continue
        m = next((x for x in rx.finditer(t) if kind != "closure" or not negated(t, x.start())), None)
        if m:
            out.append(f"{why} ('{m.group(0)}')")
    return out


def prose(obj, skip=QUOTE_KEYS) -> str:
    """Every string in a payload except the verbatim quotations (keys in `skip`), joined."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " \n".join(prose(v, skip) for k, v in obj.items() if k not in skip)
    if isinstance(obj, (list, tuple)):
        return " \n".join(prose(v, skip) for v in obj)
    return ""


def downstream_reasons(statement_type: str, payload: dict, existing: dict | None = None) -> list[str]:
    """Why a downstream item (tenderpack.ai.contract.DownstreamItem) is human-owned; [] when it is not. `existing` is the
    register's entry with the same id (a clarification entry re-read), or None. Called on the proposer's payload
    BEFORE any field is reset, so what the model tried to set counts."""
    t = statement_type
    out: list[str] = []
    if t == "issue":
        out.append("an issue is a matter kept open for people: its framing and conclusion are a person's")
    if t == "clarification_item":
        e = dict((payload or {}).get("entry") or {})
        status = e.get(PROPOSED_STATUS) or e.get("response_status")
        kept = (existing or {}).get("response_status") or DRAFT
        if existing is not None:
            out.append(f"re-reads the existing question {e.get('id')}: a person compares the two")
        if status not in (None, kept):
            out.append(f"sets the response status to {status!r} (the register holds {kept!r}): whether a question is "
                       "answered or withdrawn is a human decision")
        if e.get("answer") or e.get("recorded_answer"):
            out.append("records an answer: recording that an addendum responds is not declaring that the answer "
                       "resolves the question")
    if t != "escalation":
        out += [f"its own words {x}" for x in triggers(prose(payload))]
    return list(dict.fromkeys(out))


def analysis_reasons(statement_type: str, payload: dict, provision_text: str = "") -> list[str]:
    """Why an analysis-phase item (tenderpack.ai.contract.ChangeProposal) is human-owned; [] when it is not. An
    annotation op that confirms, interprets or changes nothing is a reading of what an answer means: human-owned when
    its own words or the provision's words raise a trigger (a precedence answer, a waiver, an ambiguity closed). An
    amendment op that applies printed words (substitute, delete, insert, ...) is a deterministic edit and is left to the
    engine's checks. A no_effect disposition whose reason declares a matter closed (a closure trigger) is human-owned;
    issues and clarification questions are human-owned by type."""
    p = payload or {}
    out: list[str] = []
    if statement_type == "amendment_op":
        if p.get("type") == "annotate" and p.get("effect") in (None, "none", "confirms", "interprets"):
            own = triggers(prose({k: p.get(k) for k in ("note", "issue")}))
            pro = triggers(provision_text)
            out += [f"its own words {x}" for x in own]
            out += [f"the provision it reads {x}: what that answer settles is a person's decision" for x in pro]
            if out:
                out.insert(0, f"an annotation that {p.get('effect') or 'changes nothing'} reads a legal or commercial "
                              "question")
    elif statement_type == "disposition":
        # a 'no effect' answer is a person's judgment when its reason declares a matter closed (closure words only: a
        # recital that names precedence changes nothing by itself)
        out += [f"its reason {x}" for x in triggers(prose({k: p.get(k) for k in ("reason",)}), ("closure",))]
    elif statement_type in ("issue", "clarification"):
        out.append(f"a{'n' if statement_type == 'issue' else ''} {statement_type} is a matter kept open for people")
        out += [f"its own words {x}" for x in triggers(prose(p))]
    return list(dict.fromkeys(out))


def record_detail(reasons: list[str]) -> str:
    return (f"{EVIDENCE_NOT_CONCLUSION} ({HUMAN_DECISION_PENDING}): " + "; ".join(reasons))[:600]


def is_human_owned(item) -> bool:
    """A validated item (ChangeProposal or DownstreamItem) the controller marked human-owned."""
    return any(getattr(v, "check", None) == CHECK for v in getattr(item, "validation", None) or [])


# ---------------------------------------------------------------------------------------------- recorded decisions

def entry_binding(kind: str, entry: dict) -> dict:
    """What a person's decision on a clarification entry or an issue is bound to: the entry exactly as it reads (every
    field; the promotion marker and drafting provenance included), so any later change voids the decision."""
    return {"kind": kind, "entry": entry}


def entry_fingerprint(kind: str, entry: dict) -> str:
    return hashlib.sha256(json.dumps(entry_binding(kind, entry), sort_keys=True, ensure_ascii=False,
                                     default=str).encode("utf-8")).hexdigest()


def decision(decisions: list[dict] | None, kind: str, item: str, entry: dict) -> dict | None:
    """The latest named ACCEPT decision on `item` when it is bound to the entry as it now reads; else None (no decision,
    a rejection, or a decision on an earlier wording)."""
    from .review import _latest
    d = _latest(list(decisions or []), kind, item)
    if d is None or d.get("decision") != "accept" or d.get("fingerprint") != entry_fingerprint(kind, entry):
        return None
    return d


def _ref(q) -> str:
    q = q or {}
    return f"{q.get('unit')} p{q.get('page')}"


def clarification_closed(entry: dict, decisions: list[dict] | None) -> bool:
    """True only when the entry's response status closes the question AND a person's decision is bound to it."""
    return (str(entry.get("response_status") or "") in CLOSING_STATES
            and decision(decisions, "clarification", str(entry.get("id")), entry) is not None)


def clarification_status(entry: dict, decisions: list[dict] | None) -> str:
    """The response status as every output presents it. Never 'answered' or 'withdrawn' without a recorded decision."""
    s = str(entry.get("response_status") or "")
    d = decision(decisions, "clarification", str(entry.get("id")), entry)
    parts = []
    if s in CLOSING_STATES:
        if d is not None:
            parts.append(f"{s} (decision recorded: {d.get('reviewer')}, {d.get('date')})")
        else:
            what = "closing the question by an addendum answer" if s.startswith("answered") else "withdrawing the question"
            parts.append(f"{HUMAN_DECISION_PENDING}: the entry proposes {what}"
                         + (f" ({_ref(entry.get('answer'))})" if entry.get("answer") else "")
                         + "; no person's decision is recorded, so the question stays open (draft, not sent)")
    else:
        parts.append(s)
    ra = entry.get("recorded_answer")
    if isinstance(ra, dict) and ra:
        parts.append(f"{HUMAN_DECISION_PENDING}: answer recorded from {_ref(ra)}"
                     + (" (candidate)" if entry.get(MARKER) else "")
                     + "; whether it resolves the question is a human decision")
    elif entry.get(MARKER) and d is None and s not in CLOSING_STATES:
        parts.append(f"{HUMAN_DECISION_PENDING}: proposed by the AI workflow (candidate); a person decides it")
    if entry.get(PROPOSED_STATUS) and d is None:
        parts.append("a change of the response status was proposed by the AI workflow and not applied")
    return " — ".join(p for p in parts if p)


# quotations inside running text are evidence, not the curator's own words (the rule of QUOTE_KEYS, for prose)
_QUOTED = re.compile(r"(?<![A-Za-z])'[^'\n]*?'(?![A-Za-z])|\"[^\"\n]*\"|‘[^’]*’|“[^”]*”")
_NOUN_MEANS = re.compile(r"\bmeans of\b", re.I)          # 'by means of', 'its means of decryption': a noun
ISSUE_TEXT_KEYS = ("text", "a3", "short")


def own_words(text) -> str:
    """The curator's own words in a running text: quotations removed ('...', "...", ‘...’, “...”)."""
    return _NOUN_MEANS.sub(" ", _QUOTED.sub(" ", str(text or "")))


def asserted_judgment(issue: dict) -> list[str]:
    """What an issue's own wording (text, a3, short; quotations aside) asserts that is a person's judgment: the topic
    words of TRIGGERS (which document prevails, which clause governs, what a term means, a deemed acceptance). []
    when none. Session 12 (F1; audit A1-1/A2-1/A3-1): a curated issue that states 'Volume I prevails' is a conclusion,
    not an open question, and is labelled until a person decides it."""
    return list(dict.fromkeys(x for k in ISSUE_TEXT_KEYS for x in triggers(own_words(issue.get(k)), ("topic",))))


# session 13 (audit R1-3): words that settle a limb of a question (a conclusion stated as the reading); in an issue
# that is a person's decision not yet recorded they are reported for a person (stage2.pending_wording_findings)
SETTLING = re.compile(r"\b(?:is|are) not treated as\b|\b(?:is|are) treated as\b|\b(?:is|are) (?:to be )?read as\b|"
                      r"\bmeans\b|\btherefore\b|\bso it follows\b|\bit follows that\b", re.I)


def settled_wording(issue: dict) -> list[str]:
    """The settling words in an issue's own words (text, a3, short; quotations removed: own_words), each quoted once;
    [] when none."""
    out = []
    for k in ISSUE_TEXT_KEYS:
        for m in SETTLING.finditer(own_words((issue or {}).get(k))):
            w = f"'{m.group(0)}'"
            if w not in out:
                out.append(w)
    return out


# session 12 (F5; audit A3-5, R-a, R1-1): an issue whose owner is Legal or Commercial (the lead, counsel) is a legal or
# commercial judgment by its owner; the issue file's `decision_owner` (when given) counts before `owner`
JUDGMENT_OWNERS = re.compile(r"^\s*(?:legal|commercial)\b", re.I)


def owner_judgment(issue: dict) -> str | None:
    """'a legal or commercial judgment by its owner (Legal)' when the issue's decision owner (else owner) is Legal or
    Commercial (lead, counsel); else None."""
    o = str((issue or {}).get("decision_owner") or (issue or {}).get("owner") or "")
    return f"a legal or commercial judgment by its owner ({o})" if JUDGMENT_OWNERS.match(o) else None


def pending_links(register: dict | None) -> dict[str, list[str]]:
    """Issue id -> the topics of the clarification register's `pending_decision` entries that link it (an issue linked
    from a pending decision is pending: the register says such a point is shown as HUMAN DECISION PENDING)."""
    out: dict[str, list[str]] = {}
    for c in (register or {}).get("pending_decision") or []:
        for i in c.get("linked_issues") or []:
            out.setdefault(str(i), []).append(str(c.get("topic") or ""))
    return out


# session 14 (W4; report section 9 L27, blind-07 COMPARISON section 5): an issue whose point an explicit and unambiguous
# document rule settles (the controller's re_present_issue writes `applied_rule` and `confirm`: "applied rule: <clause
# words>; a person confirms the application") is a PROPOSED basis for a person to confirm, with its owner kept; it is
# not shown as HUMAN DECISION PENDING unless a genuine judgment remains: a proposed status or resolution, a pending
# decision of the clarification register naming it, or its own remaining words asserting a judgment. Its rows stay NOT
# SETTLED ("applied rule awaiting a person's confirmation", signals.awaiting_note) until a person accepts the issue.
PROPOSED_BASIS = "PROPOSED BASIS (applied rule; a person confirms the application)"


def applied_basis(issue: dict | None) -> list[str]:
    """The confirmation lines of an issue the controller re-presented as an applied rule ([] when it is not one)."""
    issue = issue or {}
    return [str(x) for x in issue.get("confirm") or []] if issue.get("applied_rule") and issue.get("confirm") else []


def awaiting_confirmation(iid: str, issue: dict, decisions: list[dict] | None,
                          linked: list[str] | None = None) -> list[str]:
    """The applied-rule confirmation lines of an issue no person has decided and that holds no genuine judgment
    (pending_reasons is empty); [] otherwise. Session 14 (W4)."""
    basis = applied_basis(issue)
    if not basis or decision(decisions, "issue", iid, issue or {}) is not None:
        return []
    return [] if pending_reasons(iid, issue, decisions, linked) else basis


def pending_reasons(iid: str, issue: dict, decisions: list[dict] | None, linked: list[str] | None = None) -> list[str]:
    """Why an open issue is a person's decision not yet recorded ([] when it is not, or when a person's decision is bound
    to it as it now reads). The ONE rule every output uses (A1's Issues sheet, the A3 page's marker and a3_detail.html,
    A4's pending section, and A2/A5's NOT SETTLED for the rows it is linked to: signals.attach_pending): proposed by the
    AI workflow (MARKER); a proposed status or resolution; its own words assert a judgment (asserted_judgment); a
    pending decision of the clarification register links it (`linked`, pending_links); its owner is Legal or Commercial
    (owner_judgment). Session 12, F5 (audit A3-5, R-a, R1-1)."""
    issue = issue or {}
    if decision(decisions, "issue", iid, issue) is not None:
        return []
    out = []
    basis = applied_basis(issue)                 # session 14 (W4): an applied rule is a basis to confirm, not a judgment
    if issue.get(MARKER) and not basis:
        out.append("proposed by the AI workflow")
    if issue.get("status") not in (None, "", "open") or issue.get("resolution"):
        out.append(f"a proposed {'resolution' if issue.get('resolution') else 'status'}")
    out += [f"its own words {x}" for x in asserted_judgment(issue)]
    if linked:
        out.append("a pending decision of the clarification register names it (" + "; ".join(linked) + ")")
    ow = owner_judgment(issue)
    if ow and not basis:
        out.append(ow)
    return out


def issue_label(iid: str, issue: dict, decisions: list[dict] | None, linked: list[str] | None = None) -> str | None:
    """The prefix an output puts before an issue's text: None for an open issue as curated (it is open by
    construction), HUMAN_DECISION_PENDING for one the AI workflow proposed (MARKER), one that carries a status or a
    resolution, or (session 12, F1) a curated issue whose own words assert a judgment (asserted_judgment), or (F5) one
    a pending decision of the clarification register links (`linked`) or whose owner is Legal or Commercial
    (owner_judgment), without a person's decision bound to it; and the decision when one is."""
    closing = issue.get("status") not in (None, "", "open") or bool(issue.get("resolution"))
    basis = applied_basis(issue)                 # session 14 (W4): an applied rule's owner confirms; not a judgment
    judged = bool(asserted_judgment(issue)) or bool(linked) or (bool(owner_judgment(issue)) and not basis)
    d = decision(decisions, "issue", iid, issue) if (closing or issue.get(MARKER) or judged or basis) else None
    if closing and d is not None:
        return f"{str(issue.get('status') or 'resolved').upper()} (decision recorded: {d.get('reviewer')}, {d.get('date')})"
    if closing:
        return (f"{HUMAN_DECISION_PENDING} (a proposed {'resolution' if issue.get('resolution') else 'status'}; the "
                "issue stays open)")
    if basis and not judged:
        return (f"APPLIED RULE CONFIRMED (decision recorded: {d.get('reviewer')}, {d.get('date')})" if d is not None
                else PROPOSED_BASIS)
    if issue.get(MARKER) and d is None:
        return f"{HUMAN_DECISION_PENDING} (proposed by the AI workflow)"
    if judged and d is not None:
        return f"DECIDED (decision recorded: {d.get('reviewer')}, {d.get('date')})"
    if judged:
        return HUMAN_DECISION_PENDING          # short: it prefixes the A3 line too (the reason is the issue's own text)
    return None


# ---------------------------------------------------------------------------------------------- one owner per judgment
# session 13 (F2; audit R2-5): a judgment has one owner in A1, A3 and A4. The owner comes from the issue the judgment is
# about (a register entry's FIRST linked issue: the issue it asks about; later links are context, e.g. a reading's
# precision) and the register entry inherits it. Roles compare on their function word ('Legal' = 'Legal counsel',
# 'Commercial' = 'Commercial lead'); 'Technical' and 'Process engineer' are different owners.

def _role(o) -> str:
    w = str(o or "").strip().split()
    return w[0].lower() if w else ""


def same_owner(a, b) -> bool:
    """Whether two owner labels name the same function ('Legal' and 'Legal counsel'; not 'Technical' and 'Process
    engineer')."""
    return bool(_role(a)) and _role(a) == _role(b)


def judgment_owner(entry: dict, issues: dict | None) -> str:
    """The owner of a clarification-register entry (a question or a pending decision) as every output shows it: the
    owner of its first linked issue that exists in `issues` (id -> issue: the issue's decision_owner, else owner), else
    the entry's own decision_owner. The ONE function A4 uses, so A1/A3 (the issue) and A4 (the entry) agree."""
    for i in (entry or {}).get("linked_issues") or []:
        it = (issues or {}).get(i)
        if it:
            return str(it.get("decision_owner") or it.get("owner") or "")
    return str((entry or {}).get("decision_owner") or "")


def owner_findings(register: dict | None, issues: dict | None) -> list[str]:
    """Register entries whose curated decision_owner is not the owner of the issue they are about (judgment_owner):
    one judgment, two owners. A regression for the curated register (tests/test_session13_audit_fixes_a3.py), not a
    release gate: the sealed rehearsal registers were written before the rule (as clarify.judgment_findings); the outputs
    already show judgment_owner, so they never disagree."""
    out = []
    for kind, key in (("clarifications", "id"), ("pending_decision", "topic")):
        for c in (register or {}).get(kind) or []:
            own = judgment_owner(c, issues)
            if c.get("decision_owner") and own and not same_owner(c.get("decision_owner"), own):
                first = next(i for i in c.get("linked_issues") or [] if (issues or {}).get(i))
                out.append(f"{kind}[{c.get(key)}]: decision owner {c.get('decision_owner')!r} is not the owner of its "
                           f"issue {first} ({own!r}): one judgment has one owner (the entry inherits the issue's)")
    return out
