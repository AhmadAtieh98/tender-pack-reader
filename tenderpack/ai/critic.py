"""The independent critic (session 10, routes layer): a SECOND model pass over a SELECTED subset of a staged run's items.

It reads each selected item with its evidence INLINE (no tools), under its own system prompt and, where configured, on
another route or model than the proposer, and answers {agrees, concerns[], evidence_checked[]}. The answer is written
to the item's `review.critic` (contract.CriticReview) in staging/ai/<run_id>/proposals.yaml and shown in the review
request. It NEVER changes a verification status, a coverage figure or anything outside the run's staging folder:
agreement between models is not approval, and disagreement is a concern for a person, not a rejection.

Which items (config/ai.yaml `critic.select`; each reason is recorded on the review):
  removal                      an amendment op `set_status` deleted or revoked; a row reading or new row whose
                               interpretation records `removed` words
  conflicting                  the controller's status `conflicting`, or the proposer declares a conflict
  consequential_interpretation a row reading / new row whose interpretation states a consequence; an annotation that
                               interprets or adds an obligation; a `no_effect` disposition that rests on an
                               interpretation or an assumption statement
  uncertain_target             from the controller's validation records and the state before the addendum: the old
                               words were located in the target rather than quoted (record "interpretation": "located in
                               the target"); the target is a group (table, form, list) or resolved through one
                               (replace_unit / insert_unit, several annotate targets); the target is a heading; or the
                               target is not among the units the provision cites (its candidate targets)
  Items the controller found `invalid` are left out (nothing to second-guess: they never reach a person as changes).

Routes (config `critic.route`, or --route):
  host       a headless Claude Code call (`claude -p`, no tools, --system-prompt policy.compose("critic_item", "host")
             (session 13: the runtime policy, tenderpack/ai/policy.py), --json-schema for the
             answer, --output-format json, a timeout): the host's own plan pays; the model is the one the CLI reports
  recorded   a cassette (providers.recorded): offline tests only
  anthropic / openrouter / ollama   the same provider interface as propose (session 12: the model is config
             `models.critic` of the route; on ollama ONLY that one, no fallback, see config.critic_model) (Request with no tools and
             response_schema = the critic schema; native structured output where the adapter supports it), under the
             route's caps, with capabilities verified as for propose (base.unverified)
Every call is logged to the run's log files (worklog/model_calls/<run_id>.jsonl and staging/ai/<run_id>/log.jsonl,
redacted) as `critic_*` events.

Session 11, inside the workflow (tenderpack/ai/workflow.py): after each analysis batch is validated, and after the
downstream items are validated, the critic reviews the SELECTED items of that batch in ONE request (review_batch: the
shared context, i.e. the addendum, the stage and the units the items cite, is sent once; the answer is
{reviews: [{item, agrees, concerns, evidence_checked}]}), through the request layer (tenderpack/ai/requests.py: the
same capability check, size, failure classes and one bounded repair as every phase). Selection adds `conflicting`
for items whose evidence contradicts another item of the set (`contradictions`: the same target or row with different
new words, values or parameters), and `select_downstream` for downstream items (removals; consequential
interpretations, a row whose interpretation states a consequence or an issue for the A3 sheet; uncertain targets, a
reading of a row that is not its task's row; conflicts). `run()` (the `tenderpack ai critic` command) is unchanged: one
request per item.

Session 12, offline mode (tenderpack/ai/offline.py): the host critic is refused before any process ("offline mode: the
host critic is not available; configure routes.ollama.models.critic or accept a skipped review"); in the workflow the
critic then runs on the local critic model or is recorded SKIPPED with its reason ("independent review did not run").
"""
from __future__ import annotations

import datetime as dt
import json
import secrets
import shutil
import subprocess
import time
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

from . import budget as B
from . import config as C
from . import policy
from .runlog import RunLog, truncate

REASONS = ("removal", "conflicting", "consequential_interpretation", "uncertain_target")
NOT_APPROVAL = "agreement between models is not approval; the critic changes no status"

# Session 13: the critic's text lives in the runtime policy (tenderpack/ai/policy/40_critic.md with 41_critic_item.md,
# one item, or 42_critic_batch.md, several); these are the compositions the application routes send. The host critic
# (a plain `claude -p` session) sends policy.compose(..., "host").
CRITIC_SYSTEM = policy.compose("critic_item", "api")

CRITIC_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["agrees", "concerns", "evidence_checked"],
                 "properties": {"agrees": {"type": "boolean"},
                                "concerns": {"type": "array", "items": {"type": "string"}},
                                "evidence_checked": {"type": "array", "items": {"type": "string"}}}}


class CriticAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agrees: bool
    concerns: list[str]
    evidence_checked: list[str]


class CriticError(Exception):
    pass


def settings(cfg: dict) -> dict:
    s = dict(cfg.get("critic") or {})
    s.setdefault("route", "host")
    s.setdefault("model", None)
    s.setdefault("select", list(REASONS))
    s.setdefault("max_items", 25)
    s.setdefault("host", {})
    return s


# ---------------------------------------------------------------------------------------------- selection

def _payload(it) -> dict:
    return it.payload if isinstance(it.payload, dict) else {}


def _interps(it) -> list[dict]:
    p = _payload(it)
    if it.statement_type == "row_reading":
        return [p.get("interpretation") or {}]
    if it.statement_type == "row_new":
        return list((p.get("row") or {}).get("interpretations") or [])
    return []


def reasons_for(it, statements: dict, ws=None, packet_targets: dict | None = None) -> list[str]:
    """Why an item is sent to the critic (empty: it is not). See the module docstring."""
    out: list[str] = []
    p = _payload(it)
    st = it.statement_type
    if it.verification_status == "invalid":
        return []
    if (st == "amendment_op" and p.get("type") == "set_status" and p.get("status") in ("deleted", "revoked")) \
            or any(i.get("removed") for i in _interps(it)):
        out.append("removal")
    if it.verification_status == "conflicting" or it.conflicts:
        out.append("conflicting")
    deps = [statements.get(s) for s in it.statements]
    if any(i.get("consequence") not in (None, "none_stated", {}) for i in _interps(it)) \
            or (st == "amendment_op" and p.get("type") == "annotate" and p.get("effect") in ("interprets", "adds_obligation")) \
            or (st == "disposition" and p.get("disposition") == "no_effect"
                and any(d is not None and d.kind in ("interpretation", "assumption") for d in deps)):
        out.append("consequential_interpretation")
    if _uncertain_target(it, ws, packet_targets):
        out.append("uncertain_target")
    return out


def _uncertain_target(it, ws, packet_targets) -> list[str]:
    why = []
    if any(v.check == "interpretation" and v.ok and "located in the target" in v.detail for v in it.validation):
        why.append("old words located in the target")
    p = _payload(it)
    if p.get("type") in ("replace_unit", "insert_unit") or len(p.get("targets") or []) > 1:
        why.append("resolved through a group")
    tgt = it.target or p.get("target")
    if ws is not None and tgt:
        from .. import amend
        try:
            pst = ws.stage(ws.prev_stage(it.provision.split(":")[0])).state
        except Exception:                                        # noqa: BLE001 (no stage: nothing more to say)
            pst = {}
        u = pst.get(tgt)
        if u is None and amend.group_members(pst, tgt):
            why.append("target is a group")
        elif u is not None and u.kind == "heading":
            why.append("target is a heading")
        cands = (packet_targets or {}).get(it.provision)
        if cands is not None and tgt not in cands and not any(c in tgt or tgt in c for c in cands):
            why.append("target is not among the units the provision cites")
    return why


def _candidates(ws, ps) -> dict[str, list[str]]:
    from ..citations import citations, resolve
    from .. import amend
    try:
        pst = ws.stage(ws.prev_stage(ps.addendum)).state
        order = [u["unit_id"] for u in ws.r["units"]]
    except Exception:                                            # noqa: BLE001
        return {}
    out = {}
    for it in ps.items:
        u = pst.get(it.provision)
        if u is not None and it.provision not in out:
            head = amend.heading_of(order, pst, it.provision)
            out[it.provision] = list(dict.fromkeys(resolve(citations(u.text + " " + head), set(pst))))
    return out


def select(ps, ws=None, cfg_select=None) -> list[tuple[object, list[str]]]:
    want = set(cfg_select or REASONS)
    statements = {s.id: s for s in ps.statements}
    cands = _candidates(ws, ps) if ws is not None else None
    clash = contradictions(ps.items)
    out = []
    for it in ps.items:
        r = [x for x in reasons_for(it, statements, ws, cands) if x in want]
        if it.id in clash and "conflicting" in want and it.verification_status != "invalid":
            if "conflicting" not in r:
                r.append("conflicting")
            r.append(f"conflicting: its evidence contradicts {', '.join(clash[it.id])}")
        if r:
            detail = _uncertain_target(it, ws, cands) if "uncertain_target" in r else []
            out.append((it, r + [f"uncertain_target: {d}" for d in detail]))
    return out


def _target_of(it) -> list[str]:
    p = _payload(it)
    if it.statement_type in ("row_reading",):
        return [p.get("row")] if p.get("row") else []
    if it.statement_type == "row_new":
        return [(p.get("row") or {}).get("id")] if (p.get("row") or {}).get("id") else []
    t = [it.target or p.get("target")] + list(p.get("targets") or [])
    return [x for x in dict.fromkeys(t) if x]


def contradictions(items) -> dict[str, list[str]]:
    """Items whose evidence contradicts another item of the same set (conservative): two ops on the same target that
    replace the same old words (or the same previous value) with different new words (values); two interpretations of
    the same row giving one parameter different values; two new rows with the same id. {item id: [the other ids]}."""
    out: dict[str, list[str]] = {}
    xs = [it for it in items if getattr(it, "verification_status", "") != "invalid"]

    def clash(a, b):
        out.setdefault(a.id, []).append(b.id)
        out.setdefault(b.id, []).append(a.id)
    for i, a in enumerate(xs):
        for b in xs[i + 1:]:
            if not set(_target_of(a)) & set(_target_of(b)):
                continue
            pa, pb = _payload(a), _payload(b)
            if a.statement_type == b.statement_type == "amendment_op":
                if pa.get("old") and pa.get("old") == pb.get("old") and pa.get("new") != pb.get("new"):
                    clash(a, b)
                elif a.previous_value is not None and a.previous_value == b.previous_value \
                        and a.proposed_value is not None and b.proposed_value is not None \
                        and str(a.proposed_value) != str(b.proposed_value):
                    clash(a, b)
            elif a.statement_type == b.statement_type == "row_reading":
                ka = (pa.get("interpretation") or {}).get("parameters") or {}
                kb = (pb.get("interpretation") or {}).get("parameters") or {}
                if any(k in kb and str(ka[k]) != str(kb[k]) for k in ka):
                    clash(a, b)
            elif a.statement_type == b.statement_type == "row_new":
                clash(a, b)
    return {k: sorted(set(v)) for k, v in out.items()}


def select_downstream(ds, tasks: dict | None = None, cfg_select=None) -> list[tuple[object, list[str]]]:
    """The downstream items sent to the critic (see the module docstring); invalid items are left out."""
    want = set(cfg_select or REASONS)
    clash = contradictions(ds.items)
    out = []
    for it in ds.items:
        if it.verification_status == "invalid":
            continue
        p, r = _payload(it), []
        if any(i.get("removed") for i in _interps(it)):
            r.append("removal")
        if it.verification_status == "conflicting" or it.conflicts or it.id in clash:
            r.append("conflicting")
            if it.id in clash:
                r.append(f"conflicting: its evidence contradicts {', '.join(clash[it.id])}")
        if any(i.get("consequence") not in (None, "none_stated", {}) for i in _interps(it)) \
                or (it.statement_type == "issue" and (p.get("show_in_a3") or p.get("a3"))):
            r.append("consequential_interpretation")
        t = (tasks or {}).get(it.task) or {}
        if it.statement_type == "row_reading" and t.get("kind") == "row_reading" and p.get("row") != t.get("row"):
            r.append("uncertain_target")
            r.append(f"uncertain_target: reads row {p.get('row')} for the task of row {t.get('row')}")
        elif tasks is not None and it.task not in tasks:
            r.append("uncertain_target")
            r.append(f"uncertain_target: answers {it.task!r}, which is not a task of the run")
        keep = [x for x in r if x.split(":")[0] in want]
        if keep:
            out.append((it, keep))
    return out


# ---------------------------------------------------------------------------------------------- the request

def evidence_text(ws, ps, it, reasons: list[str]) -> str:
    """The item and its evidence, inline (the critic has no tools)."""
    prev = None
    pst = {}
    if ws is not None:
        try:
            prev = ws.prev_stage(ps.addendum)
            pst = ws.stage(prev).state
        except Exception:                                        # noqa: BLE001
            pst = {}
    def unit(uid):
        u = pst.get(uid)
        if u is None and ws is not None:
            iu = ws.units_by_id.get(uid)
            return None if iu is None else {"unit_id": uid, "text_as_issued": iu.get("text"), "pages": iu.get("pages")}
        return None if u is None else {"unit_id": uid, "doc": u.doc, "kind": u.kind, "status": u.status,
                                       "pages": u.pages, "text_before_addendum": u.text, "cells": u.cells or None}
    tgt = it.target or _payload(it).get("target")
    statements = {s.id: s for s in ps.statements}
    body = {"addendum": ps.addendum, "stage_before_addendum": prev, "why_selected": reasons,
            "item": {k: v for k, v in it.model_dump(mode="json").items()
                     if k not in ("state", "validation", "review", "verification_status")},
            "controller_status": it.verification_status,
            "controller_validation": [v.model_dump() for v in it.validation],
            "provision": unit(it.provision), "target": unit(tgt) if tgt else None,
            "statements_relied_on": [statements[s].model_dump(mode="json") for s in it.statements if s in statements],
            "reminder": NOT_APPROVAL}
    return "CRITIC REQUEST\n" + json.dumps(body, ensure_ascii=False, default=str)


def parse_answer(data) -> CriticAnswer:
    if isinstance(data, str):
        from .controller import ParseError, _extract_json
        try:
            data = _extract_json(data)
        except ParseError as e:
            raise CriticError(f"the critic's answer is not JSON: {e}") from None
    try:
        return CriticAnswer.model_validate(data)
    except ValidationError as e:
        raise CriticError(f"the critic's answer is not {{agrees, concerns, evidence_checked}}: {str(e)[:300]}") from None


# ---------------------------------------------------------------------------------------------- backends

class HostCritic:
    """A headless `claude -p` call: no tools, the critic system prompt, the answer constrained by --json-schema."""
    route = "host"

    def __init__(self, cfg: dict, model: str | None = None, runner=subprocess.run):
        from .offline import check_host_session
        check_host_session(cfg, "critic")                          # session 12: offline mode, before any process
        self.cfg = cfg
        h = dict(settings(cfg).get("host") or {})
        self.claude_bin = h.get("claude_bin") or (cfg.get("host_session") or {}).get("claude_bin") or "claude"
        self.timeout_s = float(h.get("timeout_s", 240))
        self.max_turns = int(h.get("max_turns", 3))
        self.model = model if model is not None else settings(cfg).get("model")
        self.runner = runner

    @property
    def system(self) -> str:
        return policy.compose("critic_item", "host", cfg=self.cfg)              # session 13: the runtime policy

    def command(self) -> list[str]:
        cmd = [self.claude_bin, "-p", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
               "--permission-prompts", "none", "--output-format", "json", "--max-turns", str(self.max_turns),
               "--system-prompt", self.system,
               "--json-schema", json.dumps(CRITIC_SCHEMA)]
        if self.model:
            cmd += ["--model", str(self.model)]
        return cmd

    def review(self, text: str, cwd: Path) -> tuple[CriticAnswer, dict]:
        if not shutil.which(self.claude_bin) and not Path(self.claude_bin).exists():
            raise CriticError(f"{self.claude_bin} not found: the host critic needs the Claude Code CLI")
        t0 = time.monotonic()
        try:
            p = self.runner(self.command(), input=text, capture_output=True, text=True, timeout=self.timeout_s,
                            cwd=str(cwd))
        except subprocess.TimeoutExpired:
            raise CriticError(f"the host critic timed out after {self.timeout_s:g} s") from None
        meta = {"elapsed_s": round(time.monotonic() - t0, 1), "exit_code": p.returncode}
        try:
            out = json.loads(p.stdout or "{}")
        except ValueError:
            raise CriticError(f"the host CLI printed no JSON (exit {p.returncode}): {(p.stdout or p.stderr)[:300]}") \
                from None
        meta.update({"num_turns": out.get("num_turns"), "usage": out.get("usage"),
                     "model_reported": ", ".join(out.get("modelUsage") or {}) or None,
                     "host_plan_cost_usd": out.get("total_cost_usd"), "is_error": out.get("is_error"),
                     "raw_result": truncate(str(out.get("result") or ""), 4000)})
        if out.get("is_error"):
            raise CriticError(f"the host critic ended with an error: {out.get('subtype')} {str(out.get('result'))[:200]}")
        return parse_answer(out.get("structured_output") if out.get("structured_output") is not None
                            else out.get("result") or ""), meta


class ProviderCritic:
    """The critic through the provider interface (recorded, anthropic, openrouter, ollama)."""

    def __init__(self, route: str, cfg: dict, model: str | None = None, cassette=None, provider=None, caps=None,
                 sleep=time.sleep):
        from .providers import make
        rcfg = C.route(cfg, route)
        self.route = route
        self.prov = provider or make(route, C.critic_model(rcfg, route, model), cfg, cassette)
        self.caps = C.caps(cfg, route, caps)
        self.price = B.price_for(cfg, self.prov.model)
        B.check_startable(route, rcfg, self.caps, self.price)
        self.budget = B.Budget(self.caps, self.price)
        self.sleep = sleep
        self.model = self.prov.model
        self.checked = False
        self.system = policy.compose("critic_item", route, cfg=cfg)          # session 13: the runtime policy

    def review(self, text: str, cwd: Path) -> tuple[CriticAnswer, dict]:
        from .providers.base import ProviderError, Request, complete_with_retries
        if not self.checked:
            if hasattr(self.prov, "check_ready"):
                self.prov.check_ready()
            self.prov.capabilities()                 # verified, or refused (base.unverified), as for propose
            self.checked = True
        req = Request(system=self.system, messages=[{"role": "user", "content": [{"type": "text", "text": text}]}],
                      tools=[], response_schema=CRITIC_SCHEMA, max_tokens=min(self.budget.max_tokens(), 4000),
                      timeout_s=self.budget.call_timeout())
        try:
            self.budget.next_turn()
            resp = complete_with_retries(self.prov, req, retries=int(self.caps.get("retries") or 0),
                                         backoff_s=float(self.caps.get("backoff_s") or 0), sleep=self.sleep,
                                         before_attempt=self.budget.before_call)
            self.budget.after_call(resp.usage.get("input_tokens", 0), resp.usage.get("output_tokens", 0))
        except (ProviderError, B.BudgetExhausted) as e:
            raise CriticError(f"the critic's provider call failed: {e}") from None
        return parse_answer(resp.text), {"usage": resp.usage, "model_reported": resp.model_reported,
                                         "stop_reason": resp.stop_reason}


def backend_for(route: str, cfg: dict, model=None, cassette=None, provider=None, caps=None, runner=subprocess.run):
    if route == "host":
        return HostCritic(cfg, model, runner)
    return ProviderCritic(route, cfg, model, cassette, provider, caps)


# ---------------------------------------------------------------------------------------------- the step

def critic_run_id(run_id: str) -> str:
    return f"critic-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(2)}"


def run(ws, run_id: str, route: str | None = None, model: str | None = None, cassette=None, cfg: dict | None = None,
        max_items: int | None = None, backend=None, provider=None, caps=None, runner=subprocess.run) -> dict:
    """Criticise the selected items of staged run `run_id`; write review.critic into its proposals.yaml and a section
    of its review_request.md. Returns a summary. Never changes a status (checked before writing)."""
    from .contract import CriticReview, ItemReview, ProposalSet
    from .controller import HEADER
    from .providers.base import ProviderError, collect_notices
    cfg = cfg or C.load(ws.ai_config)
    st = settings(cfg)
    route = route or st["route"]
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    d = staging / B.check_run_id(run_id)
    f = d / "proposals.yaml"
    if not f.exists():
        raise B.Refused(f"no staged run {run_id} ({f})")
    raw = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    ps = ProposalSet.model_validate(raw["proposal_set"])
    before = {it.id: it.verification_status for it in ps.items}
    ws.refresh()
    chosen = select(ps, ws, st.get("select"))
    limit = int(max_items or st.get("max_items") or 25)
    skipped = [it.id for it, _ in chosen[limit:]]
    chosen = chosen[:limit]
    crun = critic_run_id(run_id)
    log = RunLog(run_id, [Path(ws.worklog) / f"{run_id}.jsonl", d / "log.jsonl"])
    log.event("critic_start", critic_run=crun, route=route, model_requested=model or st.get("model"),
              selected=[{"item": it.id, "why": r} for it, r in chosen], not_reviewed_over_limit=skipped,
              select=st.get("select"), note=NOT_APPROVAL)
    results, errors = [], []
    with collect_notices() as notes:
        try:
            be = backend or backend_for(route, cfg, model, cassette, provider, caps, runner)
        except (B.Refused, C.ConfigError) as e:
            log.event("critic_refused", reason=str(e))
            raise
        for it, why in chosen:
            text = evidence_text(ws, ps, it, why)
            log.event("critic_request", critic_run=crun, item=it.id, prompt=text,
                      system=getattr(be, "system", None) or policy.compose("critic_item", route, cfg=cfg))
            try:
                ans, meta = be.review(text, d)
            except (CriticError, ProviderError, B.Refused) as e:
                msg = getattr(e, "message", None) or str(e)
                errors.append({"item": it.id, "error": msg})
                log.event("critic_error", critic_run=crun, item=it.id, error=msg)
                if isinstance(e, (B.Refused, ProviderError)) and "capabilities" in msg:
                    break                                   # refused before any call: the rest would be refused too
                continue
            reported = meta.get("model_reported")
            it.review = ItemReview(critic=CriticReview(
                agrees=ans.agrees, concerns=ans.concerns, evidence_checked=ans.evidence_checked,
                selected_because=why, route=route, model_requested=getattr(be, "model", None) or "the CLI's default",
                model_reported=reported, critic_run=crun,
                created=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
            results.append({"item": it.id, "agrees": ans.agrees, "concerns": len(ans.concerns)})
            log.event("critic_answer", critic_run=crun, item=it.id, answer=ans.model_dump(), **meta)
    after = {it.id: it.verification_status for it in ps.items}
    if after != before:                                          # a guard: the critic never changes a status
        raise CriticError("a status changed during the critic step; nothing written")
    raw["proposal_set"] = ps.model_dump(mode="json")
    ctl = dict(raw.get("controller") or {})
    ctl.setdefault("critic_runs", []).append({"critic_run": crun, "route": route, "items": results, "errors": errors,
                                              "not_reviewed_over_limit": skipped, "route_notices": list(notes),
                                              "note": NOT_APPROVAL})
    raw["controller"] = ctl
    f.write_text(HEADER + yaml.safe_dump(raw, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    rr = d / "review_request.md"
    md = rr.read_text(encoding="utf-8") if rr.exists() else f"# Review request: run {run_id}\n"
    rr.write_text(_with_section(md, critic_markdown(ps, crun, route, results, errors, skipped, notes)), encoding="utf-8")
    log.event("critic_end", critic_run=crun, reviewed=len(results), errors=errors, statuses_unchanged=True,
              route_notices=list(notes))
    return {"run_id": run_id, "critic_run": crun, "route": route, "selected": len(chosen), "reviewed": len(results),
            "agrees": sum(1 for r in results if r["agrees"]), "disagrees": sum(1 for r in results if not r["agrees"]),
            "errors": errors, "not_reviewed_over_limit": skipped, "items": results, "staging": str(d),
            "note": NOT_APPROVAL}


SECTION = "## Independent critic"


def critic_markdown(ps, crun, route, results, errors, skipped, notes) -> str:
    L = [f"{SECTION} (a second model; agreement is not approval, and no status was changed)", "",
         f"- critic run `{crun}`, route **{route}**; {len(results)} item(s) reviewed"
         + (f"; {len(errors)} failed" if errors else "") + (f"; {len(skipped)} not reviewed (over the limit)" if skipped
                                                          else ""), ""]
    by = {it.id: it for it in ps.items}
    for r in results:
        c = by[r["item"]].review.critic
        L.append(f"- **{r['item']}** ({by[r['item']].verification_status}): critic {'agrees' if c.agrees else 'DOES NOT agree'}"
                 f" — selected because {', '.join(c.selected_because)}; model {c.model_reported or c.model_requested}")
        L += [f"  - concern: {x}" for x in c.concerns]
        if c.evidence_checked:
            L.append(f"  - checked: {', '.join(c.evidence_checked)[:400]}")
    L += [f"- **{e['item']}**: critic failed: {e['error'][:300]}" for e in errors]
    L += [f"- route notice: {n.get('message')}" for n in notes]
    return "\n".join(L) + "\n"


def _with_section(md: str, section: str) -> str:
    i = md.find(SECTION)
    if i >= 0:
        j = md.find("\n## ", i + len(SECTION))
        md = md[:i] + (md[j + 1:] if j >= 0 else "")
    k = md.find("\n## Next")
    return (md[:k + 1] + section + "\n" + md[k + 1:]) if k >= 0 else (md.rstrip("\n") + "\n\n" + section)


# ---------------------------------------------------------------------------------------------- session 11: batched

CRITIC_TASK = "critic_review"
CRITIC_BATCH_SYSTEM = policy.compose("critic", "api")

_REVIEW = {"type": "object", "additionalProperties": False, "required": ["item", "agrees", "concerns", "evidence_checked"],
           "properties": {"item": {"type": "string"}, "agrees": {"type": "boolean"},
                          "concerns": {"type": "array", "items": {"type": "string"}},
                          "evidence_checked": {"type": "array", "items": {"type": "string"}}}}
CRITIC_BATCH_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["reviews"],
                       "properties": {"reviews": {"type": "array", "items": _REVIEW}}}


class ReviewEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item: str
    agrees: bool
    concerns: list[str]
    evidence_checked: list[str]


class CriticBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reviews: list[ReviewEntry]


def parse_batch(data, fields: dict | None = None, overwrites: list | None = None) -> CriticBatch:
    if not isinstance(data, dict):
        raise CriticError("the critic's answer must be a JSON object {reviews: [...]}")
    try:
        return CriticBatch.model_validate(data)
    except ValidationError as e:
        raise CriticError(f"the critic's answer is not {{reviews: [{{item, agrees, concerns, evidence_checked}}]}}: "
                          f"{str(e)[:600]}") from None


def batch_packet(ws, addendum: str, entries: list[tuple[str, object, list[str], dict]]) -> dict:
    """The request of one batched review: `entries` are (key, item, reasons, statements by id). The units the items cite
    (the provision, the target) are printed once under `units`; each item names them."""
    prev, pst = None, {}
    if ws is not None:
        try:
            prev = ws.prev_stage(addendum)
            pst = ws.stage(prev).state
        except Exception:                                        # noqa: BLE001 (a refused build: no stage)
            pst = {}

    def unit(uid):
        u = pst.get(uid)
        if u is None and ws is not None:
            iu = ws.units_by_id.get(uid)
            return None if iu is None else {"text_as_issued": iu.get("text"), "pages": iu.get("pages")}
        return None if u is None else {"doc": u.doc, "kind": u.kind, "status": u.status, "pages": u.pages,
                                       "text_before_addendum": u.text, "cells": u.cells or None}
    units: dict = {}
    items = []
    for key, it, why, statements in entries:
        p = _payload(it)
        tgt = getattr(it, "target", None) or p.get("target")
        for uid in (getattr(it, "provision", None), tgt):
            if uid and uid not in units:
                v = unit(uid)
                if v is not None:
                    units[uid] = v
        d = it.model_dump(mode="json", by_alias=True)
        items.append({"key": key, "why_selected": why,
                      "item": {k: v for k, v in d.items() if k not in ("state", "validation", "review",
                                                                     "verification_status")},
                      "controller_status": it.verification_status,
                      "controller_validation": [v.model_dump() for v in it.validation],
                      "provision": getattr(it, "provision", None), "target": tgt,
                      "statements_relied_on": [statements[s].model_dump(mode="json") for s in it.statements
                                               if s in statements]})
    return {"task": CRITIC_TASK, "addendum": addendum, "stage_before_addendum": prev, "reminder": NOT_APPROVAL,
            "note": "the units are printed once; each item names its provision and target", "units": units,
            "items": items}


def batch_prompt(packet: dict) -> str:
    return "CRITIC REQUEST\n" + json.dumps(packet, ensure_ascii=False, default=str)


def review_batch(packet: dict, *, route: str, cfg: dict, log, cwd: Path, policy, model: str | None = None,
                 provider=None, cassette=None, caps: dict | None = None, sleep=time.sleep, runner=subprocess.run,
                 staging: Path | None = None, run_id: str = "critic") -> dict:
    """ONE critic request for the items of `packet` (batch_packet), through the request layer. Returns {answers: {key:
    ReviewEntry}, missing: [keys], outcome: Outcome record, model_requested, model_reported}. Raises the request layer's
    errors (RateLimited, ProviderFailed, Malformed, CapabilityRefused, TooLarge)."""
    from . import requests as R
    sp = R.spec("critic", route=route, cfg=cfg)                     # session 13: the policy for this route's family
    fields = {"run_id": run_id, "created": "-", "route": route, "provider": route, "model_requested": model or "-",
              "model_reported": None, "task": CRITIC_TASK}
    prompt = batch_prompt(packet)
    if route == "host":
        from . import hostsession as HS
        from .offline import check_host_session
        check_host_session(cfg, "critic")                         # session 12: offline mode, before any process
        ps_ = HS.PlainSession(cfg, sp.system, schema=CRITIC_BATCH_SCHEMA,
                              model=model if model is not None else settings(cfg).get("model"),
                              timeout_s=float((settings(cfg).get("host") or {}).get("timeout_s", 240)),
                              max_turns=int((settings(cfg).get("host") or {}).get("max_turns", 3)),
                              claude_bin=(settings(cfg).get("host") or {}).get("claude_bin")
                              or (cfg.get("host_session") or {}).get("claude_bin"), runner=runner, label="critic")

        class _S:                       # the plain session in the shape ask_host expects
            model = ps_.model
            last = None

            def capabilities(self):
                return HS.declared_capabilities(cfg)

            def host_model_label(self):
                return ps_.host_model_label()

            def system_prompt(self):
                return sp.system

            def prompt(self, pk):
                return prompt

            def run_batch(self, pk):
                r = ps_.run(prompt, cwd, log)
                if r.structured_output is not None:
                    r.final_text = json.dumps(r.structured_output, ensure_ascii=False)
                self.last = r
                return {}
        out = R.ask_host(sp, _S(), packet, cfg=cfg, policy=policy, log=log, fields=fields, cwd=cwd, sleep=sleep,
                         settings=R.settings_for(cfg, "host"), runner=runner)
        mreq = ps_.host_model_label()
    else:
        from .providers import make
        rcfg = C.route(cfg, route)
        prov = provider or make(route, C.critic_model(rcfg, route, model), cfg, cassette)
        caps_ = C.caps(cfg, route, caps)
        price = B.price_for(cfg, prov.model)
        B.check_startable(route, rcfg, caps_, price)
        out = R.converse(sp, prov, packet, ws=None, route=route, caps_=caps_, price=price, policy=policy, log=log,
                         staging=Path(staging or cwd), run_id=run_id, fields={**fields, "model_requested": prov.model},
                         sleep=sleep, prompt_text=prompt, settings=R.settings_for(cfg, route))
        mreq = prov.model
    answers = {r.item: r for r in out.answer.reviews}
    keys = [x["key"] for x in packet["items"]]
    return {"answers": answers, "missing": [k for k in keys if k not in answers], "outcome": out.record(),
            "model_requested": mreq, "model_reported": out.model_reported}
