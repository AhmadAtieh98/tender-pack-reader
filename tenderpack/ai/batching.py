"""Bounded batches for an addendum too large for one request (session 10, routes layer).

    plan_batches(provisions, capabilities, overhead) -> list[Batch]

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
