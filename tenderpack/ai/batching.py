"""Bounded batches for an addendum too large for one request (session 10, routes layer).

    plan_batches(provisions, capabilities, overhead) -> list[Batch]
    plan_structured(provisions, size, units, fits) -> list[list[str]]     (session 13: by structure, see below)

splits an addendum's provisions, in their order, into batches whose request fits the model's VERIFIED context window and
output cap, accounting for everything else the request carries:

    input   = system prompt + tool definitions + the packet without its provisions (instructions, schema, payload
              schemas, the pattern drafter's reference, the tool list) + the batch's provisions (+ their image crops)
              + an allowance for the conversation's later turns (tool calls and tool results)
    output  = the set's envelope + an expected size per provision
    a batch fits when  output <= the output cap  and  input + output <= context x (1 - margin)

Nothing is dropped. A provision that cannot fit even alone becomes its own batch with `fits: false` and the note "too
large: needs a person to split", with its size; every provision appears in exactly one batch (`assignment`). The
workflow (tenderpack/ai/workflow.py) runs one propose per batch with a checkpoint; this module only plans.

Sizes are ESTIMATES unless calibrated:
  * characters per token: 3.5 (the controller's own estimate, controller._conv_tokens; a ratio, not a tokenizer).
    With a key, `calibrate()` asks the Messages API's free token-count endpoint (AnthropicProvider.count_tokens: POST
    /v1/messages/count_tokens, per the bundled claude-api skill, shared/token-counting.md) for the whole packet and
    uses the measured ratio for this packet; the source is recorded on every batch.
  * an image crop: 4,800 tokens, an upper estimate (the bundled claude-api skill, shared/model-migration.md: a
    full-resolution image uses "up to ~4784 tokens" on current models).
  * output per provision: 700 tokens, from the blind-03 host run's proposal set (68,854 characters for 35 provisions,
    about 562 tokens per provision at 3.5 characters per token) with about 25% headroom; plus 1,500 for the envelope.
  * later turns: `prior_turns_tokens` (config/ai.yaml batching), since a model reads with tools before it answers.
The capabilities must come from the endpoint (or a cassette): a plan is refused when the context window is unknown.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field

CHARS_PER_TOKEN = 3.5
IMAGE_TOKENS = 4800
OUTPUT_TOKENS_PER_PROVISION = 700
OUTPUT_TOKENS_FIXED = 1500
PRIOR_TURNS_TOKENS = 30000
MARGIN = 0.10
TOO_LARGE = "too large: needs a person to split"


class BatchPlanError(Exception):
    pass


@dataclass
class Overhead:
    """What every batch's request carries besides its provisions (tokens), and the expected output sizes."""
    system_tokens: int = 0
    tools_tokens: int = 0
    packet_fixed_tokens: int = 0
    prior_turns_tokens: int = PRIOR_TURNS_TOKENS
    output_tokens_fixed: int = OUTPUT_TOKENS_FIXED
    output_tokens_per_provision: int = OUTPUT_TOKENS_PER_PROVISION
    max_output_tokens: int | None = None          # what one call may request (the run's max_tokens_per_call)
    margin: float = MARGIN
    chars_per_token: float = CHARS_PER_TOKEN
    image_tokens: int = IMAGE_TOKENS
    size_source: str = "estimate: 3.5 characters per token (not a tokenizer count)"

    def input_fixed(self) -> int:
        return self.system_tokens + self.tools_tokens + self.packet_fixed_tokens + self.prior_turns_tokens

    def output_for(self, n: int) -> int:
        return self.output_tokens_fixed + self.output_tokens_per_provision * n


@dataclass
class Batch:
    index: int
    provisions: list[str]
    input_tokens: int
    output_tokens: int
    fits: bool
    note: str = ""
    sizes: dict[str, int] = field(default_factory=dict)
    size_source: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def tokens_of(text: str, overhead: Overhead) -> int:
    return int(len(text) / overhead.chars_per_token) + 1


def provision_tokens(p, overhead: Overhead) -> int:
    """A provision's share of the packet: its packet entry as JSON, plus its image crops when it carries any."""
    if isinstance(p, dict) and isinstance(p.get("tokens"), int):
        return p["tokens"]
    if not isinstance(p, dict) or "unit_id" not in p:
        raise BatchPlanError(f"a provision must be a task-packet entry with a unit_id, got {str(p)[:80]!r}")
    entry = {k: v for k, v in p.items() if k not in ("crops", "tokens")}
    return tokens_of(json.dumps(entry, ensure_ascii=False), overhead) + overhead.image_tokens * len(p.get("crops") or [])


def _limits(capabilities) -> tuple[int, int | None, str]:
    c = capabilities.to_dict() if hasattr(capabilities, "to_dict") else dict(capabilities or {})
    ctx = c.get("context_tokens")
    if not isinstance(ctx, int) or ctx <= 0:
        raise BatchPlanError(f"no verified context window (context_tokens={ctx!r}; source: {c.get('source')}): a batch "
                             "plan needs the endpoint's limits (capabilities unverified)")
    out = c.get("max_output_tokens")
    return ctx, out if isinstance(out, int) and out > 0 else None, str(c.get("source") or "")


def plan_batches(provisions: list, capabilities, overhead: Overhead | None = None) -> list[Batch]:
    """Split `provisions` (task-packet entries, in addendum order) into batches that fit (see the module docstring)."""
    ov = overhead or Overhead()
    ctx, out_cap_model, _ = _limits(capabilities)
    caps_out = [x for x in (out_cap_model, ov.max_output_tokens) if x]
    out_cap = min(caps_out) if caps_out else None
    usable = int(ctx * (1 - ov.margin))
    sizes = [(p["unit_id"] if isinstance(p, dict) else str(p), provision_tokens(p, ov)) for p in provisions]

    def fits(group: list[tuple[str, int]]) -> tuple[bool, int, int]:
        inp = ov.input_fixed() + sum(s for _, s in group)
        out = ov.output_for(len(group))
        ok = inp + out <= usable and (out_cap is None or out <= out_cap)
        return ok, inp, out

    batches: list[Batch] = []
    cur: list[tuple[str, int]] = []

    overhead_only = ov.input_fixed() + ov.output_for(0)

    def close(group, ok_override=None):
        ok, inp, out = fits(group)
        ok = ok if ok_override is None else ok_override
        note = "" if ok else (f"{TOO_LARGE}: about {inp} input + {out} output tokens against a usable context of "
                              f"{usable} (context {ctx}, margin {ov.margin:g})"
                              + (f" and an output cap of {out_cap}" if out_cap else ""))
        if not ok and overhead_only >= usable:
            note += (f"; the request overhead alone (system, tools, packet, later-turn allowance and the set's envelope: "
                     f"about {overhead_only} tokens) leaves no room: a larger context, a smaller "
                     "batching.prior_turns_tokens, or a person's split is needed")
        batches.append(Batch(index=len(batches) + 1, provisions=[u for u, _ in group], input_tokens=inp,
                             output_tokens=out, fits=ok, note=note, sizes=dict(group), size_source=ov.size_source))
    for uid, size in sizes:
        if not fits([(uid, size)])[0]:                       # never dropped: alone, flagged for a person
            if cur:
                close(cur)
                cur = []
            close([(uid, size)], ok_override=False)
            continue
        if cur and not fits([*cur, (uid, size)])[0]:
            close(cur)
            cur = []
        cur.append((uid, size))
    if cur:
        close(cur)
    planned = [u for b in batches for u in b.provisions]
    if planned != [u for u, _ in sizes]:                     # a guard: every provision once, in order
        raise BatchPlanError("the plan lost or reordered a provision")
    return batches


def assignment(batches: list[Batch]) -> dict[str, int]:
    """provision -> batch index (every provision of the plan)."""
    return {u: b.index for b in batches for u in b.provisions}


def overhead_for(packet: dict, system: str = "", tools: list | None = None, max_output_tokens: int | None = None,
                 settings: dict | None = None, chars_per_token: float | None = None,
                 size_source: str | None = None) -> Overhead:
    """An Overhead from a task packet (controller.task_packet): everything in the packet except the provisions and the
    crops, the system prompt and the tool definitions; `settings` is config/ai.yaml `batching` (defaults above)."""
    st = settings or {}
    ov = Overhead(prior_turns_tokens=int(st.get("prior_turns_tokens", PRIOR_TURNS_TOKENS)),
                  output_tokens_fixed=int(st.get("output_tokens_fixed", OUTPUT_TOKENS_FIXED)),
                  output_tokens_per_provision=int(st.get("output_tokens_per_provision", OUTPUT_TOKENS_PER_PROVISION)),
                  margin=float(st.get("context_margin", MARGIN)), image_tokens=int(st.get("image_tokens", IMAGE_TOKENS)),
                  chars_per_token=float(chars_per_token or st.get("chars_per_token", CHARS_PER_TOKEN)),
                  max_output_tokens=max_output_tokens)
    if size_source:
        ov.size_source = size_source
    fixed = {k: v for k, v in packet.items() if k not in ("provisions", "crops")}
    ov.packet_fixed_tokens = tokens_of(json.dumps(fixed, ensure_ascii=False, default=str), ov)
    ov.system_tokens = tokens_of(system or "", ov)
    ov.tools_tokens = tokens_of(json.dumps(tools or [], ensure_ascii=False), ov)
    return ov


def packet_provisions(packet: dict) -> list[dict]:
    """The packet's provisions with the crops the packet attaches to each (by unit id)."""
    by_unit: dict[str, list] = {}
    for c in packet.get("crops") or []:
        by_unit.setdefault(c.get("unit_id"), []).append(c.get("sha256"))
    return [{**p, "crops": by_unit.get(p["unit_id"], [])} for p in packet.get("provisions") or []]


def calibrate(provider, packet_text: str, system: str = "", tools: list | None = None) -> tuple[float, str]:
    """Characters per token of THIS packet as the provider's token-count endpoint measures it (Anthropic:
    count_tokens). Returns (ratio, source). Raises the provider's error when it cannot count (no key, no endpoint)."""
    from .providers.base import Request
    if not hasattr(provider, "count_tokens"):
        raise BatchPlanError(f"{getattr(provider, 'name', provider)} has no token-count endpoint")
    req = Request(system=system, messages=[{"role": "user", "content": [{"type": "text", "text": packet_text}]}],
                  tools=list(tools or []), max_tokens=1, timeout_s=60)
    n = provider.count_tokens(req)
    total = len(packet_text) + len(system or "") + len(json.dumps(tools or [], ensure_ascii=False))
    if n <= 0:
        raise BatchPlanError("the token-count endpoint returned no tokens")
    ratio = total / n
    return ratio, (f"{getattr(provider, 'name', 'provider')} token-count endpoint on this packet: {n} tokens for {total} "
                   f"characters ({ratio:.2f} characters per token)")


def summary(batches: list[Batch]) -> dict:
    return {"batches": [b.to_dict() for b in batches], "assignment": assignment(batches),
            "too_large": [{"provision": u, "batch": b.index, "note": b.note} for b in batches if not b.fits
                          for u in b.provisions],
            "provisions": sum(len(b.provisions) for b in batches)}


# ---------------------------------------------------------------------------------------------- session 11: one request
# The request layer (tenderpack/ai/requests.py) checks EVERY request of every phase before it is sent, with the same
# rule as the planner: input = system + tool definitions + the packet (its JSON as sent) + the images attached + the
# allowance for later turns (tool phases only); output = what the phase is expected to write (`expected_output`);
# fits when output <= the output cap and input + output <= context x (1 - margin). A request that does not fit is
# never truncated: the workflow splits its batch by provision or task, and a single provision or task that does not
# fit alone is escalated with its size.

EXPECTED_OUTPUT = {                         # per phase: (fixed, per unit); config/ai.yaml batching.expected_output
    "analysis": (OUTPUT_TOKENS_FIXED, OUTPUT_TOKENS_PER_PROVISION),
    "downstream": (1500, 900),              # per task: a re-made reading, a row or an escalation with its quotations
    "reading": (8000, 0),                   # one Reading of an image region (a form or a table, every line)
    "critic": (300, 350),                   # per item reviewed
    "repair": (1500, 700),
}


@dataclass
class RequestSize:
    phase: str
    system_tokens: int
    tools_tokens: int
    packet_tokens: int
    image_tokens: int
    prior_turns_tokens: int
    output_tokens: int
    context_tokens: int | None
    usable_tokens: int | None
    output_cap: int | None
    fits: bool
    why: str = ""
    size_source: str = ""
    capability_source: str = ""
    units: int = 0

    @property
    def input_tokens(self) -> int:
        return (self.system_tokens + self.tools_tokens + self.packet_tokens + self.image_tokens
                + self.prior_turns_tokens)

    def to_dict(self) -> dict:
        return {**asdict(self), "input_tokens": self.input_tokens}

    def line(self) -> str:
        return (f"about {self.input_tokens} input tokens (system {self.system_tokens}, tools {self.tools_tokens}, packet "
                f"{self.packet_tokens}, images {self.image_tokens}, later turns {self.prior_turns_tokens}) + "
                f"{self.output_tokens} output tokens against a usable context of {self.usable_tokens} (context "
                f"{self.context_tokens}) and an output cap of {self.output_cap}")


def expected_output(phase: str, units: int, settings: dict | None = None) -> int:
    st = ((settings or {}).get("expected_output") or {}).get(phase)
    fixed, per = (st if isinstance(st, (list, tuple)) and len(st) == 2 else EXPECTED_OUTPUT.get(phase, (1500, 700)))
    if phase == "analysis" and settings:
        fixed = int(settings.get("output_tokens_fixed", fixed))
        per = int(settings.get("output_tokens_per_provision", per))
    return int(fixed) + int(per) * max(0, int(units))


def request_size(phase: str, capabilities, *, system: str = "", tools: list | None = None, packet_text: str = "",
                 images: int = 0, prior_turns: bool = True, units: int = 0, max_output_tokens: int | None = None,
                 settings: dict | None = None, output_tokens: int | None = None,
                 packet_tokens: int | None = None) -> RequestSize:
    """The complete size of one request (see the comment above). `capabilities` must carry a context window (verified
    by the endpoint, a cassette's, or the host's declared one); without one the size is computed and `fits` is False
    with the reason (capabilities unverified)."""
    st = settings or {}
    cpt = float(st.get("chars_per_token", CHARS_PER_TOKEN))
    ov = Overhead(chars_per_token=cpt)
    c = capabilities.to_dict() if hasattr(capabilities, "to_dict") else dict(capabilities or {})
    ctx = c.get("context_tokens") if isinstance(c.get("context_tokens"), int) and c.get("context_tokens") > 0 else None
    caps_out = [x for x in (c.get("max_output_tokens"), max_output_tokens) if isinstance(x, int) and x > 0]
    out_cap = min(caps_out) if caps_out else None
    margin = float(st.get("context_margin", MARGIN))
    usable = int(ctx * (1 - margin)) if ctx else None
    out = int(output_tokens if output_tokens is not None else expected_output(phase, units, st))
    size = RequestSize(phase=phase, system_tokens=tokens_of(system or "", ov),
                       tools_tokens=tokens_of(json.dumps(tools or [], ensure_ascii=False), ov) if tools else 0,
                       packet_tokens=int(packet_tokens) if packet_tokens is not None else tokens_of(packet_text or "", ov),
                       image_tokens=int(st.get("image_tokens", IMAGE_TOKENS)) * int(images or 0),
                       prior_turns_tokens=int(st.get("prior_turns_tokens", PRIOR_TURNS_TOKENS)) if prior_turns else 0,
                       output_tokens=out, context_tokens=ctx, usable_tokens=usable, output_cap=out_cap, fits=True,
                       size_source=f"estimate: {cpt:g} characters per token (not a tokenizer count)",
                       capability_source=str(c.get("source") or ""), units=int(units or 0))
    why = []
    if ctx is None:
        why.append(f"no context window is known for this route (source: {c.get('source')}): the request cannot be "
                   "accounted (capabilities unverified)")
    elif size.input_tokens + out > usable:
        why.append(f"{size.input_tokens} input + {out} output tokens exceed the usable context of {usable}")
    if out_cap is not None and out > out_cap:
        why.append(f"the expected output of {out} tokens exceeds the output cap of {out_cap}")
    if why:
        size.fits, size.why = False, "; ".join(why)
    return size


def plan_units(units: list[dict], fits) -> list[list[dict]]:
    """Split `units` (provisions or tasks, in order) into consecutive groups that each `fits(group) -> bool`, greedily;
    a unit that does not fit alone is its own group (the caller escalates it with its size). Nothing is dropped or
    reordered."""
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for u in units:
        if cur and fits(cur + [u]):
            cur.append(u)
            continue
        if cur:
            groups.append(cur)
        cur = [u]
    if cur:
        groups.append(cur)
    if [id(u) for g in groups for u in g] != [id(u) for u in units]:
        raise BatchPlanError("the plan lost or reordered a unit")
    return groups


# ---------------------------------------------------------------------------------------------- session 13: structure

_TABLE_REF = re.compile(r"\bTable\s+([0-9]+(?:[.\-][0-9]+)*)", re.I)


def structure_key(pid: str, unit: dict | None = None) -> str:
    """The structure a provision is printed in, from its id (session 13, implementer D): the part before '/' (an image
    region's elements `p4-image/...`, a table's rows and notes `T1-3/...`, the cover lines, an appendix's paragraphs),
    the clause number for a clause and its lettered items (`3.3`, `3.3(b)` -> `3`), and for numbered answers (`Q15`)
    their letters with the heading they are printed under (the answers of one subject)."""
    local = pid.split(":", 1)[1] if ":" in pid else pid
    if "/" in local:
        return local.split("/")[0]
    m = re.match(r"^(\d+)[.(]", local)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Za-z]+)\d+$", local)
    if m:
        head = str((unit or {}).get("heading") or "").strip()
        return m.group(1) + (f"|{head}" if head else "")
    return local


def structure_keys(provisions: list[str], units: dict | None = None) -> dict[str, str]:
    """structure_key for every provision, with a section's own paragraphs attached to the structure printed under the
    same heading (an appendix's "The table below ..." paragraphs belong to the image region or table it introduces);
    the cover lines stay the cover's."""
    units = units or {}
    keys = {p: structure_key(p, units.get(p)) for p in provisions}
    heads: dict[str, str] = {}
    for p in provisions:
        u = units.get(p) or {}
        h = str(u.get("heading") or "").strip()
        if h and u.get("kind") != "paragraph" and not _is_cover(p):
            heads.setdefault(h, keys[p])
    for p in provisions:
        u = units.get(p) or {}
        h = str(u.get("heading") or "").strip()
        if h in heads and u.get("kind") == "paragraph" and not _is_cover(p):
            keys[p] = heads[h]
    return keys


def _is_cover(pid: str) -> bool:
    return pid.split(":", 1)[-1].startswith("cover/")


def structure_links(provisions: list[str], units: dict | None = None) -> list[tuple[str, str, str]]:
    """Links between structures that belong next to each other (session 13): provisions printed under the same heading
    (an appendix's paragraphs and the image region they introduce), and an operative provision whose own words or
    heading name a table this addendum itself prints (`Table 1-3` -> the structure `T1-3`: a translation and the table
    it renders, an answer that amends the table). The cover is the addendum's summary of itself, never an operative
    provision (VOL-I 3.2), so its words link nothing. Returns (key, key, why) triples, read from the evidence only."""
    units = units or {}
    keys = structure_keys(provisions, units)
    present = set(keys.values())
    out: list[tuple[str, str, str]] = []
    by_head: dict[str, str] = {}
    for p in provisions:
        u = units.get(p) or {}
        head = str(u.get("heading") or "").strip()
        k = keys[p]
        if _is_cover(p):
            continue
        if head:
            if head in by_head and by_head[head] != k and (by_head[head], k) not in {(x[0], x[1]) for x in out}:
                out.append((by_head[head], k, f"the same heading: {head[:80]}"))
            by_head.setdefault(head, k)
        for n in _TABLE_REF.findall(f"{head}\n{u.get('text') or ''}"):
            t = "T" + n.replace(".", "-")
            if t in present and t != k and (k, t) not in {(x[0], x[1]) for x in out}:
                out.append((k, t, f"names Table {n}, which this addendum prints"))
    return out


def plan_structured(provisions: list[str], size: int, units: dict | None = None, fits=None,
                    links: bool = True) -> list[list[str]]:
    """Session 13 (implementer D; the owner: "grouping related provisions"): batches planned by STRUCTURE, not by
    count.
      * a structure (structure_keys: an image region's elements, a table's rows and notes, a clause and its lettered
        items, the answers under one heading, the cover lines; a section's paragraphs with the structure printed
        under the same heading) goes into ONE batch whenever it fits the token budget
        `fits(ids) -> bool` (the request accounting's estimate for the route), even beyond `size`;
      * linked structures (structure_links) are placed next to each other, so they share a batch when the batch stays
        within `size` provisions and the budget (a link never makes a batch larger than `size`: a chain of references
        must not become one long session);
      * a structure that does not fit is split in document order at the budget;
      * without `fits` the count bounds every batch, as before.
    Deterministic (a function of the ids, the units and the budget); every provision in exactly one batch; groups in
    the order of their first provision."""
    units = units or {}
    size = max(1, int(size))
    budget = fits or (lambda ids: len(ids) <= size)
    pos = {p: i for i, p in enumerate(provisions)}
    keys = structure_keys(provisions, units)
    parent: dict[str, str] = {k: k for k in keys.values()}
    first: dict[str, int] = {}
    for p in provisions:
        first.setdefault(keys[p], pos[p])

    def root(k: str) -> str:
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k
    if links:
        for a, b, _ in structure_links(provisions, units):
            ra, rb = root(a), root(b)
            if ra != rb:                                       # the earlier structure names the group
                if first[ra] <= first[rb]:
                    parent[rb] = ra
                else:
                    parent[ra] = rb
    groups: dict[str, dict[str, list[str]]] = {}
    for p in provisions:
        groups.setdefault(root(keys[p]), {}).setdefault(keys[p], []).append(p)
    out: list[list[str]] = []
    cur: list[str] = []
    for g in groups.values():
        for sub in g.values():
            if cur and len(cur) + len(sub) <= size and budget(cur + sub):
                cur += sub
                continue
            if cur:
                out.append(cur)
                cur = []
            if budget(sub):
                cur = list(sub)                                # a whole structure, beyond `size` when it fits
                continue
            for p in sub:                                      # split at the budget, in document order
                if cur and budget(cur + [p]):
                    cur.append(p)
                else:
                    if cur:
                        out.append(cur)
                    cur = [p]                                  # alone; the request layer escalates it if too large
    if cur:
        out.append(cur)
    flat = [p for b in out for p in b]
    if sorted(flat, key=pos.__getitem__) != list(provisions) or len(flat) != len(set(flat)):
        raise BatchPlanError("the structured plan lost or repeated a provision")
    return out
