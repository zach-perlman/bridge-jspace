"""x47_edges (batch 47, test 47.6; jobs/c3/batch47.yaml, design and rules fixed in advance; Q47.6 in
predictions/2026-10-28_dan.md): where is the pointer formed? Exact edge knock-outs (bridge_jspace.knockout, the code
scripts/attn_knockout.py runs) on the routes test's scenes (scripts/x6_routes.py). Part (c), the dereference block, was
dropped by Dan (amendment 1, 28 Oct ~02:30: blocking the question's reads of the locker sentences kills the lookup
under every hypothesis, so it discriminates nothing); its code stays behind `run --with-c`, unexercised and not in
any rule.

Scenes. The routes test's C2 scenes (x6_routes.scenes, seed 2510; locker-first: three locker sentences, then three pick
sentences): O = the original prompt (Iris picked A), S = the changed one (Iris picked B; B's and C's locker sentences
swapped, B's digit new). The lookup's answer on O after the patch: identity (B's digit in O), position (C's: the slot
B's sentence holds in S), value (B's new digit), original (A's), other. Gate and eligibility as x6_routes / x8_write:
O's read accuracy >= 0.80 per reader (else the model is "not tested"); both readers say and read O's and S's answers
right; the first 300 in scene order. Part (a) uses these scenes as they are. Parts (b) and (c) need a neutral filler
sentence for their control: FILLER (27 tokens on both tokenizers, the three locker sentences' total) is put before the
first locker sentence, identical in O and S, and the gate and eligibility are rerun on those prompts. Reads: X0's chat
read (the prompt with a digit's space token appended; the top token). L = the layer fixed in advance (x0_necessity.
PREDICTED: 9B 12, Muse 26); h = block L's output at the bridge word; the whole change Delta = h_S - h_O, added at the
bridge word at L on O (x6_routes' patch).

Edges. An edge is (layer, source token, destination token): at that layer the destination cannot read the source
directly (knockout.knock_out, mode "value": full attention, the pair's logits at -inf in every head; Gated DeltaNet, the
source's value and its conv taps in the value channels removed from the destination's output, every weight kept).
Indirect routes stay open by design. Every source here precedes every destination, so each pair is a real causal edge;
a control blocks exactly as many edges as its arm (same destinations and layers, the filler's 27 tokens as sources;
asserted per item). Layer sets: "all" = every block in the range (on the 9B, DeltaNet and full attention; on Muse
every layer is softmax attention, its sliding windows of 2048 longer than any prompt here, as attn_knockout treats
them); "attn" (9B only) = its full-attention blocks in the range. The decisive arms use "all"; "attn" is reported beside.

(a) measurement (descriptive; lookup): on O, at the bridge word at L, the arms none / whole (Delta) / no_U (Delta minus
its part in the pointer directions U, x0_massmean's Alf, not refit) / no_U_rand (Delta minus a random part of the same
share: X0's random subspace, seed 888 + L) / write1, write2 (h + 2 (mu_k - mu_j): x8_write's write at s = 2, j the
bridge's locker slot in O, k the two other slots) / rand1, rand2 (a random direction of the write's norm, seed 4761,
drawn on the CPU in item order). In the same forward, each attention layer's (9B: full attention; Muse: every layer)
softmax from the last token (the appended space, where the answer is read) to each locker sentence, per query head,
summed over the sentence's tokens: attention.npz. The answered locker = the O locker sentence stating the top token's
digit.
(b) formation (rule): Delta formed under a block: the asked pick sentence's tokens (dests "sentence"; or the bridge
token alone, "bridge") cannot read the locker sentences at layers 0..L, in both forwards that form the change (O's and
S's, the same positions); then that change is added at the bridge word at L on O, read unblocked, as in the routes
test. Arms: none (Delta, no block), block/<dests>/<layers>, control/<dests>/<layers> (the filler as sources); the
unedited read beside. The routes classification (lookup) and the recall's switch.
(c) dereference (DROPPED; `--with-c` only, descriptive): no patch; on O, the question tokens (from the question's first
word, "Which" / "How", to the last token, the appended space) cannot read the locker sentences at layers L..end;
control: the filler. Lookup and recall accuracy (top token = O's answer). Never in the rule.

Rule (stage verdict; point estimates, EPS 1e-9 at the bars; cluster-bootstrap CIs over the bridge items, 10,000
resamples, seed 0, beside them): formation, per model, decisive arms block/sentence/all and control/sentence/all:
position share <= 0.10, |identity - identity(none)| <= 0.10, |recall switch - recall switch(none)| <= 0.10, and the
control within 0.10 of none on each of the three. Holds for the test if it holds on Muse and on the 9B.
SEALED: the run writes per-item files only and prints counts. verdict, view (the verify-pack view: 10 random items,
seed 0, the prompt as the model reads it with the patch, sources and destinations marked, every arm's answer) and
figures ((a), one per model) refuse until predictions/2026-10-28_dan.md holds Dan's committed answer to Q47.6.

uv run python scripts/x47_edges.py plan                                                  # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_edges.py run --part b --name qwen35_9b_x47_6_b     # GPU (sealed)
uv run python scripts/x47_edges.py verdict                                               # CPU, after Dan's Q47.6
uv run python scripts/x47_edges.py view --name qwen35_9b_x47_6_b                         # CPU, after Dan's Q47.6
uv run python scripts/x47_edges.py figures --name qwen35_9b_x47_6_a                      # CPU, after Dan's Q47.6
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.knockout import FULL, LINEAR
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W

EXP = "x47_edges"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.6"
LK, RC = X.LOOKUP, X.RECALL
READER_NAME = {LK: "lookup", RC: "recall"}
COND = "C2"
# One neutral sentence (no entity, digit, locker or pick): 27 tokens where it stands (first in the user's message) on
# Qwen3.5's and Muse's tokenizers, the three locker sentences' total; checked per item (plan, run).
FILLER = (
    "A light rain began to fall just after the doors were closed, and the old radio in the corner played softly "
    "through the whole day."
)
WRITE_S, RAND_SEED = 2.0, 4761  # (a): x8_write's write at s = 2; the random directions' seed (CPU, item order)
A_ARMS = ("none", "whole", "no_U", "no_U_rand", "write1", "write2", "rand1", "rand2")
ROUTES = R.ROUTES
FALL_TO, NEAR = 0.10, 0.10  # formation: position share at most 0.10; identity, recall switch, control within 0.10
EPS = 1e-9  # a value exactly at a bar counts as at the bar
DECISIVE_B, CONTROL_B = "block/sentence/all", "control/sentence/all"
C_ARMS = ("block/all", "control/all")  # (c), dropped: descriptive arms of a --with-c run, never in a rule
POSITION_REF = {"qwen3.5-9b": 0.51, "muse-glimmer-30b": 0.54}  # the routes runs' C2 whole-change position share
POSITION_REF["qwen3.6-27b"] = 0.34  # batch 52 C: x6_routes_27b's C2 whole-change position share (reported beside)
MODELS = ("muse-glimmer-30b", "qwen3.5-9b")
RUNS = {"qwen3.5-9b": {"a": "qwen35_9b_x47_6_a", "b": "qwen35_9b_x47_6_b"},
        "muse-glimmer-30b": {"a": "muse30_x47_6_a", "b": "muse30_x47_6_b"}}  # fmt: skip
# batch 52 C coverage (amendment 2: the 27B fills every gap): run-stage targets beyond the design's; the
# verdict's own model list is unchanged (the 27B's run is read by passing it to the verdict)
COVERAGE_RUNS = {"qwen3.6-27b": {"a": "x47_6_a_27b", "b": "x47_6_b_27b"}}
N_EXAMPLES = 10


# ---- scenes and positions (tokenizer only) ---------------------------------------------------------------------------


def tokenizer():
    """The target's tokenizer as a run loads it (on the Mac: its cached files with the chat-template edits)."""
    from scripts import x45m

    return x45m.tokenizer()


def plain_cases(tok, n_gen: int = R.N_GEN) -> list[dict]:
    """The routes test's C2 cases (x6_routes.scenes, its seed), in scene order."""
    cases, _ = R.scenes(tok, n_gen)
    return [c for c in cases if c["condition"] == COND]


def filler_cases(tok, base: list[dict], filler: str = FILLER) -> tuple[list[dict], collections.Counter]:
    """Each base case with the filler before O's and S's first sentence (x6_routes.encode: the bridge one token at one
    index shared by O and S, else dropped and counted); everything else as the base."""
    legs, _, _ = R.pools(tok)
    out, dropped = [], collections.Counter()
    for c in base:
        case, why = R.encode(tok, f"{filler} {c['context']}", f"{filler} {c['cf_context']}", R.asked_of(c), c["bridge"],
                             c["cf_bridge"], legs, c["expect"], c["condition"], c["scene"], c["rendering"])  # fmt: skip
        if case is None:
            dropped[why] += 1
            continue
        out.append({**case, "filler": filler})
    return out, dropped


def rendered(tok, case: dict, reader: str, variant: str) -> str:
    """The reader's prompt text for O (org) or S (alt), as x6_routes.encode renders it."""
    rd = case["readers"][reader]
    ctx = case["context"] if variant == "org" else case["cf_context"]
    item = {"format": "prose", "kind": "digit", "context": ctx, "question": rd["question"]}
    return X.render(tok, item, case["rendering"], ctx)


def spans(tok, case: dict) -> dict:
    """Token positions in the prompts as read (the digit's space token appended): the three locker sentences in slot
    order, the filler ([] without one), the asked pick sentence, the bridge word, and per reader the question (its first
    word to the last token). The same in O and S and, but for the question, in both readers (asserted); the sentences
    are disjoint, the filler and lockers come before the pick sentence and the pick sentence before the question."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    per: dict[str, dict] = {}
    for w in X.READERS:
        rd = case["readers"][w]
        got = {}
        for v in ("org", "alt"):
            text = rendered(tok, case, w, v)
            enc = raw_encoding(tok, text, offsets=True)
            assert enc["input_ids"] == rd["ids"][v], f"{case['scene']} {w} {v}: the rendered prompt's ids differ"
            off = enc["offset_mapping"]
            ctx = case["context"] if v == "org" else case["cf_context"]
            assert text.count(ctx) == 1, f"{case['scene']}: the context is not once in the prompt"
            base = text.index(ctx)
            lockers = [SP.tokens_in(off, base + m.start(), base + m.end()) for m in W.LOCKER.finditer(ctx)]
            assert len(lockers) == 3, f"{case['scene']}: {len(lockers)} locker sentences"
            assert all(lockers), f"{case['scene']}: a locker sentence without tokens"
            filler = case.get("filler")
            if filler:
                assert ctx.startswith(filler + " "), f"{case['scene']}: the filler is not O's / S's first sentence"
            fill = SP.tokens_in(off, base, base + len(filler)) if filler else []
            item = case["bridge"] if v == "org" else case["cf_bridge"]
            sent = f"{R.asked_of(case)} picked the {item}."
            assert ctx.count(sent) == 1, f"{case['scene']}: the asked pick sentence is not once in the context"
            a = base + ctx.index(sent)
            pick = SP.tokens_in(off, a, a + len(sent))
            q = text.index(rd["question"], base + len(ctx))
            first = SP.tokens_in(off, q, q + 1)[0]
            n = len(enc["input_ids"]) + len(case["space"])
            got[v] = {"lockers": lockers, "filler": fill, "pick": pick, "question": list(range(first, n))}
        assert got["org"] == got["alt"], f"{case['scene']} {w}: positions differ between O and S"
        per[w] = got["org"]
    for key in ("lockers", "filler", "pick"):
        assert per[LK][key] == per[RC][key], f"{case['scene']}: the readers' {key} positions differ"
    p = {"lockers": per[LK]["lockers"], "filler": per[LK]["filler"], "pick": per[LK]["pick"], "bridge": [case["pos"]],
         "question": {w: per[w]["question"] for w in X.READERS}}  # fmt: skip
    assert case["pos"] in p["pick"], f"{case['scene']}: the bridge is not in the asked pick sentence"
    flat = [t for s in p["lockers"] for t in s]
    assert len(set(flat)) == len(flat), f"{case['scene']}: locker sentences overlap"
    assert not set(flat) & set(p["filler"]), f"{case['scene']}: the filler overlaps a locker sentence"
    assert max(flat + p["filler"]) < min(p["pick"]), f"{case['scene']}: a locker or filler token after the pick"
    for w in X.READERS:
        assert max(p["pick"]) < min(p["question"][w]), f"{case['scene']}: the question starts inside the pick sentence"
    assert 0 not in flat + p["filler"], "the first token (attention sink) is never a source"
    return p


def layer_sets(kinds: list[str], layer: int) -> dict[str, dict[str, list[int]]]:
    """Per layer set ("all"; "attn" on a hybrid model: its full-attention blocks), the blocks 0..L ("pre", formation)
    and L..end ("post", dereference), L included in both."""
    n = len(kinds)
    assert 0 <= layer < n, f"layer {layer} outside 0..{n - 1}"
    out = {"all": {"pre": list(range(layer + 1)), "post": list(range(layer, n))}}
    if LINEAR in kinds:
        out["attn"] = {k: [la for la in v if kinds[la] == FULL] for k, v in out["all"].items()}
    return out


def edge_count(src: list[int], dst: list[int], layers: list[int], kinds: list[str]) -> dict[str, int]:
    """Edges (layer, source, destination) with the source before the destination (a pair the other way round is no
    edge: nothing reads ahead), split by the layer's kind."""
    pairs = sum(1 for d in dst for s in src if s < d)
    full = sum(kinds[la] == FULL for la in layers)
    return {"pairs": pairs, "n_layers": len(layers), "edges": pairs * len(layers), "edges_full_attention": pairs * full,
            "edges_deltanet": pairs * (len(layers) - full)}  # fmt: skip


def _arm(src: list[int], dst: list[int], layers: list[int], kinds: list[str]) -> dict:
    counts = edge_count(src, dst, layers, kinds)
    assert not {"src", "dst", "layers"} & set(counts), "a count would overwrite the arm's positions"
    return {"src": sorted(src), "dst": sorted(dst), "layers": list(layers), **counts}


def formation_arms(p: dict, sets: dict, kinds: list[str]) -> dict[str, dict]:
    """(b)'s blocks: block/<dests>/<layers> (sources the locker sentences) and control/<dests>/<layers> (the filler),
    dests the asked pick sentence ("sentence") or the bridge word ("bridge"), layers 0..L of the set. A control blocks
    exactly its block's number of edges (asserted)."""
    lockers = sorted(t for s in p["lockers"] for t in s)
    assert len(p["filler"]) == len(lockers), f"filler {len(p['filler'])} tokens, lockers {len(lockers)}"
    out = {}
    for dname, dst in (("sentence", p["pick"]), ("bridge", p["bridge"])):
        for lname, ls in sets.items():
            for kind, src in (("block", lockers), ("control", p["filler"])):
                out[f"{kind}/{dname}/{lname}"] = _arm(src, dst, ls["pre"], kinds)
            b, c = out[f"block/{dname}/{lname}"], out[f"control/{dname}/{lname}"]
            assert b["edges"] == c["edges"] == len(lockers) * len(dst) * len(ls["pre"]) > 0, (dname, lname)
    return out


def dereference_arms(p: dict, sets: dict, kinds: list[str], reader: str) -> dict[str, dict]:
    """(c)'s blocks for one reader (dropped; --with-c only): block/<layers> (sources the locker sentences) and
    control/<layers> (the filler), dests the reader's question to the last token, layers L..end of the set; counts
    matched (asserted)."""
    lockers = sorted(t for s in p["lockers"] for t in s)
    assert len(p["filler"]) == len(lockers), f"filler {len(p['filler'])} tokens, lockers {len(lockers)}"
    dst = p["question"][reader]
    out = {}
    for lname, ls in sets.items():
        out[f"block/{lname}"] = _arm(lockers, dst, ls["post"], kinds)
        out[f"control/{lname}"] = _arm(p["filler"], dst, ls["post"], kinds)
        assert out[f"block/{lname}"]["edges"] == out[f"control/{lname}"]["edges"] > 0, lname
    return out


def edge_table(arms: dict[str, dict]) -> dict[str, dict[str, int]]:
    """Each arm's counts, without its position lists (cases.jsonl and the manifest)."""
    return {a: {k: v for k, v in e.items() if k not in ("src", "dst", "layers")} for a, e in arms.items()}


def slot_of_answer(top: int, case: dict, digit_token) -> int | None:
    """The O locker slot whose digit is the top token (None: no locker's digit)."""
    hit = [s for s, (_, d) in enumerate(W.slots_of(case["context"])) if digit_token(str(d)) == top]
    return hit[0] if hit else None


def config_kinds_of(target: str) -> list[str]:
    """The target's layer kinds from its pinned config.json (attn_knockout.config_kinds: sliding windows count as full
    attention), without loading the model."""
    from huggingface_hub import hf_hub_download

    from scripts import attn_knockout as AK

    t = pins.TARGETS[target]
    cfg = json.loads(Path(hf_hub_download(t["repo"], "config.json", revision=t["revision"])).read_text())
    return AK.config_kinds(cfg.get("text_config", cfg))


def stage_plan(n_gen: int = R.N_GEN, with_c: bool = False) -> dict:
    """Tokenizer only: the plain and filler cases, drops, the positions' token counts, every arm's edge counts (the
    distinct values over the items; (c)'s with --with-c only) and one example (seed 0) with its marks. No model."""
    tok = tokenizer()
    target, layer = pins.TARGET, X.PREDICTED[pins.TARGET]
    kinds = config_kinds_of(target)
    sets = layer_sets(kinds, layer)
    base = plain_cases(tok, n_gen)
    cases, dropped = filler_cases(tok, base)
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for c in base[:50]:
        p = spans(tok, c)
        counts["plain: locker tokens per sentence"][str([len(s) for s in p["lockers"]])] += 1
    for c in cases:
        p = spans(tok, c)
        counts["locker tokens per sentence"][str([len(s) for s in p["lockers"]])] += 1
        counts["filler tokens"][len(p["filler"])] += 1
        counts["pick sentence tokens"][len(p["pick"])] += 1
        counts["prompt tokens (lookup, read)"][len(c["readers"][LK]["ids"]["org"]) + len(c["space"])] += 1
        for a, e in formation_arms(p, sets, kinds).items():
            counts[f"(b) {a} edges"][e["edges"]] += 1
        for w in X.READERS if with_c else ():
            counts[f"question tokens ({READER_NAME[w]})"][len(p["question"][w])] += 1
            for a, e in dereference_arms(p, sets, kinds, w).items():
                counts[f"(c) {READER_NAME[w]} {a} edges"][e["edges"]] += 1
    ex = cases[random.Random(X.EXAMPLES_SEED).randrange(len(cases))]
    p = spans(tok, ex)
    ids = ex["readers"][LK]["ids"]["org"] + ex["space"]
    decode = lambda t: tok.decode(t, skip_special_tokens=False)  # noqa: E731
    out = {"target": target, "layer": layer, "layer_kinds": collections.Counter(kinds), "layer_sets": sets,
           "filler": FILLER, "plain C2 cases": len(base), "filler cases": len(cases), "dropped": dict(dropped),
           "counts": {k: dict(v) for k, v in counts.items()},
           "example": {"scene": ex["scene"], "expect": ex["expect"],
                       "routes": {k: decode([v]) for k, v in ex["route_tokens"].items()},
                       "lookup_O_marked": marked(decode, ids, marks_of(p, LK)),
                       "recall_question_marked": marked(decode, ex["readers"][RC]["ids"]["org"] + ex["space"],
                                                        {"dst-c": p["question"][RC]})}}  # fmt: skip
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return out


# ---- the verify-pack marks (tokenizer only) --------------------------------------------------------------------------


def marks_of(p: dict, reader: str) -> dict[str, list[int]]:
    """The labelled spans a view marks in a reader's O prompt: the locker sentences (sources), the filler (the controls'
    sources), the asked pick sentence ((b)'s dests), the bridge word (the patch, (b)'s other dests), the question ((c)'s
    dests)."""
    out = {f"src-locker{i + 1}": s for i, s in enumerate(p["lockers"])}
    if p["filler"]:
        out["filler"] = p["filler"]
    out.update({"dst-b": p["pick"], "patch": p["bridge"], "dst-c": p["question"][reader]})
    return out


def marked(decode, ids: list[int], marks: dict[str, list[int]]) -> str:
    """The prompt decoded run by run with ⟦label: ...⟧ around each marked span (spans contiguous; nested or disjoint)."""
    spans_ = sorted(((min(v), max(v) + 1, k) for k, v in marks.items() if v), key=lambda s: (s[0], -s[1]))
    for a, b, k in spans_:
        assert sorted(marks[k]) == list(range(a, b)), f"{k}: not one contiguous span"
    opens = collections.defaultdict(list)
    closes = collections.defaultdict(list)
    for a, b, k in spans_:
        opens[a].append(k)
        closes[b].append(k)
    out: list[str] = []
    stack: list[str] = []
    start = 0
    for i in sorted({0, len(ids), *opens, *closes}):
        if i > start:
            out.append(decode(ids[start:i]))
        start = i
        while stack and stack[-1] in closes[i]:
            stack.pop()
            out.append("⟧")
        assert not set(stack) & set(closes[i]), f"spans cross at token {i}"
        for k in opens[i]:
            stack.append(k)
            out.append(f"⟦{k}: ")
    assert not stack, f"unclosed marks {stack}"
    return "".join(out)


# ---- GPU ------------------------------------------------------------------------------------------------------------


class _Stop(Exception):
    """Raised by the record hook: a forward that only needs block L's output stops there."""


def muse_capture(blocks, layers: list[int], q_positions: list[int], out: dict, home=None):
    """Muse Glimmer's attention softmax from the query positions to every key, per query head, recomputed from each
    listed layer's own inputs (knockout.capture_attention's method, ported: q and k projections, the scale-free qk norm,
    the query's scale factor, rotary embeddings on sliding layers (NoPE global layers get none), grouped keys, the
    module's scaling, causal and sliding-window masks): {layer: [batch, heads, len(q), T]} fp32. A context manager;
    the forward itself is unchanged."""
    import torch

    def hook_for(la: int):
        def hook(module, args, kwargs):
            hs = kwargs["hidden_states"] if "hidden_states" in kwargs else args[0]
            ns: Any = sys.modules[type(module).__module__]
            shape = (*hs.shape[:-1], -1, module.head_dim)
            q = module.qk_norm(module.q_proj(hs).view(shape).transpose(1, 2)) * module.qk_scale_factor
            k = module.qk_norm(module.k_proj(hs).view(shape).transpose(1, 2))
            pe = kwargs.get("position_embeddings")
            if pe is not None:
                q, k = ns.apply_rotary_pos_emb(q, k, *pe)
            k = ns.repeat_kv(k, module.num_key_value_groups)
            qp = torch.tensor(list(q_positions), device=hs.device)
            scores = (q[:, :, qp].float() @ k.float().transpose(-1, -2)) * module.scaling
            keys = torch.arange(hs.shape[1], device=hs.device)
            hide = keys[None, :] > qp[:, None]
            if getattr(module, "sliding_window", None):
                hide = hide | (qp[:, None] - keys[None, :] >= module.sliding_window)
            probs = scores.masked_fill(hide, float("-inf")).softmax(-1)
            out[la] = probs if home is None or probs.device == home else probs.to(home)

        return hook

    @contextlib.contextmanager
    def ctx():
        handles = [blocks[la].self_attn.register_forward_pre_hook(hook_for(la), with_kwargs=True) for la in layers]
        try:
            yield
        finally:
            for h in handles:
                h.remove()

    return ctx()


def attention_capture(model, layers: list[int], q_positions: list[int], out: dict):
    """Muse Glimmer: muse_capture; Qwen3.5 (gated, rotary full attention): knockout.capture_attention."""
    from bridge_jspace.knockout import capture_attention, decoder_layers

    blocks: Any = decoder_layers(model)
    attn = blocks[layers[0]].self_attn
    if hasattr(attn, "qk_norm") and hasattr(attn, "qk_scale_factor"):
        return muse_capture(
            blocks, layers, q_positions, out, getattr(model, "hf", model).get_input_embeddings().weight.device
        )
    return capture_attention(model, layers, q_positions, out)


def forward(model, ids: list[list[int]], adds=None, knock=None, record=None, capture=None):
    """One batched forward of equal-length prompts, uncached. Per row: adds, a list of (layer, position, vector [d])
    added to that block's output (AddRows' arithmetic: fp32 sum, back to the block's dtype); knock, (layers, sources,
    destinations) for knockout.knock_out (mode value) or None. record = (layer, position): the block's output there per
    row, fp32 on the home device, and the forward stops after that block (no logits). capture = (layers, q_positions,
    out): attention_capture fills out. Returns (last-position logits [rows, vocab] fp32 or None, states or None)."""
    import torch

    from bridge_jspace.knockout import knock_out
    from bridge_jspace.model import _forward_hooks

    n = len(ids)
    assert len({len(x) for x in ids}) == 1, "rows of different lengths"
    adds = adds or [None] * n
    knock = knock or [None] * n
    assert len(adds) == len(knock) == n
    home = getattr(model, "hf", model).get_input_embeddings().weight.device
    by_layer: dict[int, list] = collections.defaultdict(list)
    for r, row in enumerate(adds):
        for la, pos, vec in row or []:
            by_layer[la].append((r, pos, vec))
    seen: dict[str, Any] = {}

    def hook_for(la: int):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            if by_layer.get(la):
                h = h.clone()
                for r, pos, vec in by_layer[la]:
                    h[r, pos] = (h[r, pos].float() + vec.to(h.device).float()).to(h.dtype)
            if record is not None and la == record[0]:
                seen["h"] = h[:, record[1]].float().to(home)
                raise _Stop
            if not by_layer.get(la):
                return None
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    layers = sorted(set(by_layer) | ({record[0]} if record is not None else set()))
    batch = torch.tensor(ids, device=home)
    logits = None
    with contextlib.ExitStack() as stack:
        stack.enter_context(_forward_hooks([(model.layers[la], hook_for(la)) for la in layers]))
        if any(k is not None for k in knock):
            stack.enter_context(knock_out(model, [k[0] if k else [] for k in knock], [k[1] if k else [] for k in knock],
                                          [k[2] if k else [] for k in knock], mode="value"))  # fmt: skip
        if capture is not None:
            stack.enter_context(attention_capture(model, *capture))
        with contextlib.suppress(_Stop):
            logits = model.hf(input_ids=batch, use_cache=False, logits_to_keep=1).logits[:, -1].float().to(home)
    assert (record is None) == ("h" not in seen), "the record hook did not run (or ran without a record)"
    return logits, seen.get("h")


def eligible(model, cases: list[dict], out: Path, n: int = R.N_ITEMS):
    """x8_write.eligible on the given cases: the gate (O's read accuracy >= X.GATE per reader) and the first n cases
    both readers say and read right on O and S; competence.jsonl and gate.json written."""
    import torch

    tok = model.tokenizer
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    gate = {"cases": len(cases), "org_read_accuracy": acc, "gate_min": X.GATE,
            "pass": all(a >= X.GATE for a in acc.values()), "eligible": len(ok), "n": n}  # fmt: skip
    X.write_jsonl(out / "competence.jsonl", comp)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    return (ok[:n] if gate["pass"] else []), gate, digits


def manifest(name: str, part: str, why: str, layer: int, kinds: list[str], with_c: bool = False) -> dict:
    from bridge_jspace.utils import git_state

    sets = layer_sets(kinds, layer)
    arms: dict[str, list[str]] = (
        {"a": list(A_ARMS)}
        if part == "a"
        else {"b": ["unedited", "none", *formation_arms(_toy_positions(), sets, kinds)]}
    )
    if with_c:  # dropped (Dan, amendment 1): descriptive arms only, never in a rule
        arms["c"] = ["none", *dereference_arms(_toy_positions(), sets, kinds, LK)]
    return {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": "47.6", "part": part,
            "spec": "jobs/c3/batch47.yaml (47.6)", "question": f"{QUESTION} ({PREDICTIONS})",
            "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)},
            "layer": layer, "condition": COND, "n": R.N_ITEMS, "n_gen": R.N_GEN, "gate": X.GATE,
            "layer_kinds": kinds, "layer_sets": sets, "filler": FILLER if part == "b" else None,
            "pointer_from": R.STATES[pins.TARGET], "knockout_mode": "value",
            "knockout": (sys.modules["bridge_jspace.knockout"].__doc__ or "").split("\n\n")[1],
            "arms": arms, "with_c": with_c, "decisive": {"b": [DECISIVE_B, CONTROL_B]},
            "dropped": "(c) dereference, Dan's amendment 1 (28 Oct ~02:30): run only with --with-c, descriptive",
            "read": "X0's chat read: the prompt with a digit's space token appended, the top token",
            "seeds": {"scenes": R.SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "write_random": RAND_SEED,
                      "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT, "write_s": WRITE_S,
            "sealed": f"per-item files only; no verdict, view or figure until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip


def _toy_positions() -> dict:
    """Positions shaped like a filler case's, for listing the arm names (manifest)."""
    return {"lockers": [[3, 4], [5, 6], [7, 8]], "filler": [1, 2, 9, 10, 11, 12], "pick": [13, 14], "bridge": [14],
            "question": {LK: [16, 17], RC: [16, 17]}}  # fmt: skip


def stage_run(part: str, name: str, why: str, with_c: bool = False) -> Path:
    """part a or b; with_c adds the dropped (c) arms (descriptive, never in a rule) to a part-b run."""
    import torch

    from bridge_jspace.knockout import layer_kinds
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import attn_knockout as AK
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S
    from scripts import x0_massmean as MM

    assert part in ("a", "b"), part
    assert part == "b" or not with_c, "--with-c is a part-b option"
    pins.check_run_name(name)
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"47.6 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    kinds = config_kinds_of(target)
    m = manifest(name, part, why, layer, kinds, with_c)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    assert layer_kinds(model) == kinds, "the loaded model's layer kinds differ from its config's"
    window = getattr(model.hf.config.get_text_config(), "sliding_window", None)
    sets = layer_sets(kinds, layer)
    base = plain_cases(tok, R.N_GEN)
    dropped: collections.Counter = collections.Counter()
    cases = base
    if part == "b":
        cases, dropped = filler_cases(tok, base)
    pos_of = {c["scene"]: spans(tok, c) for c in cases}
    longest = max(len(c["readers"][w]["ids"]["org"]) + len(c["space"]) for c in cases for w in X.READERS)
    assert window is None or longest < window, f"a prompt of {longest} tokens reaches the sliding window {window}"
    chosen, gate, digits = eligible(model, cases, out, R.N_ITEMS)
    gate["dropped"] = dict(dropped)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not chosen:
        m["not_tested"] = "the gate fixed in advance missed (gate.json)"
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print("not tested: the gate missed or no eligible items (gate.json)", flush=True)
        return out
    U = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device=model.device)
    rows, norms = [], []
    keep_case = []
    digit_token = lambda d: S.answer_token(tok, d, "digit")  # noqa: E731
    with torch.no_grad():
        if part == "b":
            first = chosen[0]
            p0 = pos_of[first["scene"]]
            pseudo = {"ids": first["readers"][LK]["ids"]["org"] + first["space"],
                      "sources": {"lookup": sorted(t for s in p0["lockers"] for t in s)},
                      "dests": {"final": [len(first["readers"][LK]["ids"]["org"]) + len(first["space"]) - 1],
                                "both": p0["question"][LK]},
                      "context": [min(p0["filler"]), max(p0["pick"])]}  # fmt: skip
            check = AK.run_check(model, pseudo, kinds)
            (out / "check.json").write_text(json.dumps(check, indent=2) + "\n")
            assert check["passed"], "the knock-out's pre-run check failed (check.json); not running"
            for c in progress(chosen, f"47.6 (b) at L{layer} (item)"):
                p = pos_of[c["scene"]]
                b_arms = formation_arms(p, sets, kinds)
                lk_ids = c["readers"][LK]["ids"]
                cfgs = ["none", *b_arms]
                ids_rows = [lk_ids[v] for _ in cfgs for v in ("org", "alt")]
                knocks = [None if a == "none" else (b_arms[a]["layers"], b_arms[a]["src"], b_arms[a]["dst"])
                          for a in cfgs for _ in ("org", "alt")]  # fmt: skip
                _, h = forward(model, ids_rows, knock=knocks, record=(layer, c["pos"]))
                assert h is not None
                delta = {a: h[2 * i + 1] - h[2 * i] for i, a in enumerate(cfgs)}
                d0 = delta["none"]
                norms.append({"scene": c["scene"], **{a: {
                    "norm": round(float(d.norm()), 4),
                    "share_U": round(float((d @ U).norm() ** 2 / d.norm().clamp_min(1e-30) ** 2), 5),
                    "cos_none": round(float(d @ d0 / (d.norm() * d0.norm()).clamp_min(1e-30)), 5)}
                    for a, d in delta.items()}})  # fmt: skip
                for w in X.READERS:
                    rd = c["readers"][w]
                    ids = rd["ids"]["org"] + c["space"]
                    arms_b = ["unedited", *cfgs]
                    adds = [None] + [[(layer, c["pos"], delta[a])] for a in cfgs]
                    lg, _ = forward(model, [ids] * len(adds), adds=adds)
                    assert lg is not None
                    for a, x in zip(arms_b, lg, strict=True):
                        rows.append(row_of("b", c, w, a, x, rd, digits, digit_token))
                    if not with_c:  # (c) dropped (Dan, amendment 1); the arms below run only with --with-c
                        continue
                    c_arms = dereference_arms(p, sets, kinds, w)
                    arms_c = ["none", *c_arms]
                    knocks_c = [None] + [(c_arms[a]["layers"], c_arms[a]["src"], c_arms[a]["dst"]) for a in c_arms]
                    lg, _ = forward(model, [ids] * len(arms_c), knock=knocks_c)
                    assert lg is not None
                    for a, x in zip(arms_c, lg, strict=True):
                        rows.append(row_of("c", c, w, a, x, rd, digits, digit_token))
                keep_case.append(case_record(c, p, sets, kinds, with_c=with_c))
        else:
            mu = {k: torch.tensor(v, dtype=torch.float32, device=model.device)
                  for k, v in MM.pointer_means(R.STATES[target]).items()}  # fmt: skip
            basis = SP.random_basis(U.shape[0], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(model.device)
            gen = torch.Generator().manual_seed(RAND_SEED)
            att_layers = [la for la, k in enumerate(kinds) if k == FULL]
            masses = []
            for c in progress(chosen, f"47.6 (a) at L{layer} (item)"):
                p = pos_of[c["scene"]]
                lk_ids = c["readers"][LK]["ids"]
                _, h = forward(model, [lk_ids["org"], lk_ids["alt"]], record=(layer, c["pos"]))
                assert h is not None
                x = (h[1] - h[0])[None]
                ptr = (x @ U) @ U.T
                share = ptr.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                rand = SP.random_subspace_part(x, share, basis)
                j = [it for it, _ in W.slots_of(c["context"])].index(c["bridge"])
                ks = [k for k in (0, 1, 2) if k != j]
                writes = [WRITE_S * (mu[k] - mu[j]) for k in ks]
                rands = []
                for wv in writes:
                    r = torch.randn(wv.shape[0], generator=gen).to(model.device)
                    rands.append(r / r.norm() * wv.norm())
                vecs = {"none": None, "whole": x[0], "no_U": (x - ptr)[0], "no_U_rand": (x - rand)[0],
                        "write1": writes[0], "write2": writes[1], "rand1": rands[0], "rand2": rands[1]}  # fmt: skip
                assert tuple(vecs) == A_ARMS
                rd = c["readers"][LK]
                ids = rd["ids"]["org"] + c["space"]
                got: dict[int, Any] = {}
                adds = [None if v is None else [(layer, c["pos"], v)] for v in vecs.values()]
                lg, _ = forward(model, [ids] * len(adds), adds=adds, capture=(att_layers, [len(ids) - 1], got))
                assert lg is not None
                assert sorted(got) == att_layers, f"captured layers {sorted(got)}"
                mass = torch.stack([torch.stack([got[la][:, :, 0, s].sum(-1) for s in p["lockers"]], -1)
                                    for la in att_layers], 1)  # [arms, layers, heads, 3]  # fmt: skip
                masses.append(mass.half().cpu().numpy())
                for a, xl in zip(A_ARMS, lg, strict=True):
                    r = row_of("a", c, LK, a, xl, rd, digits, digit_token)
                    r.update({"j": j, "k": ks[int(a[-1]) - 1] if a[-1].isdigit() else None,
                              "norm": None if vecs[a] is None else round(float(vecs[a].norm()), 4)})  # fmt: skip
                    rows.append(r)
                norms.append(
                    {"scene": c["scene"], "norm": round(float(x.norm()), 4), "share_U": round(float(share), 5)}
                )
                keep_case.append(case_record(c, p, sets, kinds, with_edges=False))
            np.savez_compressed(out / "attention.npz", masses=np.stack(masses), scenes=np.array([c["scene"] for c in chosen]),
                                arms=np.array(A_ARMS), layers=np.array(att_layers))  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "cases.jsonl", keep_case)
    m["items"] = len(chosen)
    m["entities"] = len({c["bridge"] for c in chosen})
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(chosen)} items, {len(rows)} reads (sealed: no verdict)", flush=True)
    return out


def row_of(part: str, c: dict, reader: str, arm: str, lg, rd: dict, digits, digit_token) -> dict:
    """One read: X0's read_row (switched = S's answer, p_org, p_alt, ld), right = O's answer, the lookup's route and
    the O locker slot the top token names."""
    top = int(lg.argmax())
    return {"part": part, "scene": c["scene"], "entity": c["bridge"], "reader": reader, "arm": arm,
            **X.read_row(lg, rd, digits), "right": int(top == rd["tok_A"]),
            "route": R.classify(top, c) if reader == LK else None, "slot": slot_of_answer(top, c, digit_token)}  # fmt: skip


def case_record(c: dict, p: dict, sets: dict, kinds: list[str], with_edges: bool = True, with_c: bool = False) -> dict:
    """What the verdict and view read back: the case, its positions and each arm's edge counts ((c)'s with with_c)."""
    rec = {k: v for k, v in c.items()}
    rec["spans"] = p
    if with_edges:
        edges: dict[str, Any] = {"b": edge_table(formation_arms(p, sets, kinds))}
        if with_c:
            edges["c"] = {READER_NAME[w]: edge_table(dereference_arms(p, sets, kinds, w)) for w in X.READERS}
        rec["edges"] = edges
    return rec


# ---- verdict (CPU; refuses until Dan's answer is committed) ---------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.6 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return answer_in(text)


def answer_in(text: str, question: str = QUESTION) -> str:
    """The 'Dan:' line of the question's block (from its bold label to the next '**Q'), stripped; '' if none."""
    if f"**{question}**" not in text:
        return ""
    block = text.split(f"**{question}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def require_answer() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def table(rows: list[dict], part: str, reader: str, keys: dict[str, Any], n_boot: int = X.N_BOOT) -> dict:
    """Per arm, each key's rate over the items (key: row -> 0/1) with cluster-bootstrap CIs over the bridge items; the
    resamples paired across arms ('_r'). Every item must have every arm."""
    mine = [r for r in rows if r["part"] == part and r["reader"] == reader]
    arms = list(dict.fromkeys(r["arm"] for r in mine))
    by = {(r["scene"], r["arm"]): r for r in mine}
    scenes = list(dict.fromkeys(r["scene"] for r in mine))
    ent = {r["scene"]: r["entity"] for r in mine}
    missing = [(s, a) for s in scenes for a in arms if (s, a) not in by]
    assert not missing, f"{part} {reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    sw = {f"{a}|{k}": [int(f(by[(s, a)])) for s in scenes] for a in arms for k, f in keys.items()}
    rr = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot) if scenes else {}
    point = {k: float(np.mean(v)) if v else float("nan") for k, v in sw.items()}
    return {"n": len(scenes), "entities": len(set(ent.values())), "arms": arms,
            "rate": {k: [point[k], *X.interval(rr[k])] for k in sw}, "_r": rr, "_p": point}  # fmt: skip


def diff(t: dict, a: str, b: str, key: str) -> list[float]:
    """Rate of key under arm a minus under arm b, with the paired resamples' 95% interval."""
    return [t["_p"][f"{a}|{key}"] - t["_p"][f"{b}|{key}"], *X.interval(t["_r"][f"{a}|{key}"] - t["_r"][f"{b}|{key}"])]


def formation(lk: dict, rc: dict) -> dict:
    """(b)'s rule on one model (point estimates): the decisive block's position share <= 0.10, its identity share and
    the recall's switch within 0.10 of none's, and the control within 0.10 of none on the three."""
    p = {**lk["_p"], **{k.replace("|switched", "|recall"): v for k, v in rc["_p"].items()}}

    def get(arm: str, key: str) -> float:
        return p[f"{arm}|{key}"]

    near = {key: {arm: abs(get(arm, key) - get("none", key)) <= NEAR + EPS for arm in (DECISIVE_B, CONTROL_B)}
            for key in ("position", "identity", "recall")}  # fmt: skip
    clauses = {"position_fell": get(DECISIVE_B, "position") <= FALL_TO + EPS,
               "identity_within": near["identity"][DECISIVE_B], "recall_within": near["recall"][DECISIVE_B],
               "control_position_within": near["position"][CONTROL_B],
               "control_identity_within": near["identity"][CONTROL_B],
               "control_recall_within": near["recall"][CONTROL_B]}  # fmt: skip
    return {"holds": all(clauses.values()), "clauses": clauses,
            "values": {f"{a}|{k}": get(a, k) for a in ("none", DECISIVE_B, CONTROL_B) for k in ("position", "identity", "recall")}}  # fmt: skip


ROUTE_KEYS = {rt: (lambda r, rt=rt: r["route"] == rt) for rt in ROUTES}
RIGHT = {"right": lambda r: r["right"]}


def b_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's (b) run: pending (no files), not tested (gate), or its tables and the formation rule; a --with-c
    run's (c) accuracy tables beside them (descriptive, dropped from the rule)."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"run": run, "status": "pending", "why": "no run here"}
    m = json.loads((src / "manifest.json").read_text())
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"]}
    if m.get("not_tested"):
        return {**base, "status": "not tested", "why": m["not_tested"]}
    if not (src / "outcomes.jsonl").exists():
        return {**base, "status": "pending", "why": "no outcomes.jsonl here"}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    b_lk = table(rows, "b", LK, ROUTE_KEYS, n_boot)
    b_rc = table(rows, "b", RC, {"switched": lambda r: r["switched"]}, n_boot)
    with_c = any(r["part"] == "c" for r in rows)
    c_tables = ({"lookup": strip(table(rows, "c", LK, RIGHT, n_boot)), "recall": strip(table(rows, "c", RC, RIGHT, n_boot))}
                if with_c else None)  # fmt: skip
    norms = X.read_jsonl(src / "norms.jsonl")
    med = {a: {k: float(np.median([n[a][k] for n in norms])) for k in ("norm", "share_U", "cos_none")}
           for a in norms[0] if a != "scene"} if norms else {}  # fmt: skip
    cases = X.read_jsonl(src / "cases.jsonl")
    edges = cases[0]["edges"] if cases else {}
    same = all(c["edges"] == cases[0]["edges"] for c in cases)
    out = {**base, "status": "tested", "n": b_lk["n"], "entities": b_lk["entities"],
           "formation": formation(b_lk, b_rc),
           "b": {"lookup": strip(b_lk), "recall": strip(b_rc)}, "c": c_tables,
           "b_diffs": {a: {k: diff(b_lk, a, "none", k) for k in ("position", "identity")} | {"recall": diff(b_rc, a, "none", "switched")}
                       for a in b_lk["arms"] if a not in ("none", "unedited")},
           "norms_median": med, "edges_item0": edges, "edges_same_every_item": same,
           "position_reference": POSITION_REF.get(m["model"]["target"])}  # fmt: skip
    return out


def strip(t: dict) -> dict:
    return {k: v for k, v in t.items() if not k.startswith("_")}


def a_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """(a), descriptive: the lookup's routes per arm, and per attention layer and head how often the head's largest
    locker-sentence mass is on the answered locker (rows with a locker answer), per arm; the heads ranked by that rate
    under the whole change on the items whose answer moved off A's locker."""
    src = RESULTS / run
    if not (src / "outcomes.jsonl").exists():
        return {"run": run, "status": "pending"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    att = np.load(src / "attention.npz")
    masses = att["masses"].astype(np.float32)  # [items, arms, layers, heads, 3]
    scenes, arms, layers = list(att["scenes"]), list(att["arms"]), [int(x) for x in att["layers"]]
    routes = table(rows, "a", LK, ROUTE_KEYS, n_boot)
    slot = {(r["scene"], r["arm"]): r["slot"] for r in rows}
    j = {r["scene"]: r["j"] for r in rows}
    follow = follow_rates(masses, scenes, arms, slot)
    moved = follow_rates(
        masses, scenes, arms, slot, only=lambda s, a: slot[(s, a)] is not None and slot[(s, a)] != j[s]
    )
    top = np.dstack(
        np.unravel_index(np.argsort(-np.nan_to_num(moved["whole"], nan=-1), axis=None), moved["whole"].shape)
    )[0][:10]
    return {"run": run, "status": "tested", "target": m["model"]["target"], "layer": m["layer"], "layers": layers,
            "routes": strip(routes), "follow": {a: v.tolist() for a, v in follow.items()},
            "follow_moved": {a: v.tolist() for a, v in moved.items()},
            "top_heads_moved_whole": [{"layer": layers[int(li)], "head": int(h),
                                       **{a: round(float(moved[a][li, h]), 3) for a in arms if not np.isnan(moved[a][li, h])}}
                                      for li, h in top]}  # fmt: skip


def follow_rates(masses: np.ndarray, scenes: list, arms: list, slot: dict, only=None) -> dict[str, np.ndarray]:
    """Per arm, [layers, heads]: the share of items (with a locker answer; and `only(scene, arm)`) whose largest mass
    of the three locker sentences is on the answered locker's sentence; nan where no item counts."""
    out = {}
    for ai, a in enumerate(arms):
        keep = [i for i, s in enumerate(scenes) if slot[(s, a)] is not None and (only is None or only(s, a))]
        if not keep:
            out[a] = np.full(masses.shape[2:4], np.nan)
            continue
        best = masses[keep, ai].argmax(-1)  # [n, layers, heads]
        ans = np.array([slot[(scenes[i], a)] for i in keep])[:, None, None]
        out[a] = (best == ans).mean(0)
    return out


def fmt(v: list) -> str:
    return "-" if v[0] is None or np.isnan(v[0]) else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def stage_verdict(runs: dict[str, dict[str, str]] | None = None, n_boot: int = X.N_BOOT) -> Path:
    answer = require_answer()
    runs = runs or RUNS
    res = {t: b_result(runs[t]["b"], n_boot) for t in MODELS}
    ares = {t: a_result(runs[t]["a"], n_boot) for t in MODELS}
    for t, r in res.items():
        assert r["status"] != "tested" or r["target"] == t, f"{r['run']} is a {r['target']} run, not {t}'s"
    tested = {t: r for t, r in res.items() if r["status"] == "tested"}
    held = [t for t, r in tested.items() if r["formation"]["holds"]]
    verdict = {"formation": {"held_on": held, "holds": len(held) == len(MODELS),
                             "not_tested_or_pending": [t for t in MODELS if t not in tested]}}  # fmt: skip
    out = RESULTS / f"x47_6-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    lines = ["# 47.6: where is the pointer formed? (edge knock-outs)", "",
             f"Batch 47, test 47.6 (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). Routes C2 scenes with the filler "
             f"sentence first; L = the layer fixed in advance; cluster bootstrap over bridge items ({n_boot}, seed "
             f"{X.BOOT_SEED}); point estimates decide. Part (c) was dropped by Dan (amendment 1) before any run. "
             "UNVERIFIED.", "",
             f"**Formation** (block/sentence/all: the pick sentence cannot read the locker sentences at 0..L, both "
             f"forwards that form the change): {'holds' if verdict['formation']['holds'] else 'does not hold'} (holds on "
             f"{', '.join(verdict['formation']['held_on']) or 'none'}).", ""]  # fmt: skip
    for t in MODELS:
        r = res[t]
        if r["status"] != "tested":
            lines += [f"## {t}: {r['status']} ({r.get('why', '')})", ""]
            continue
        f = r["formation"]
        lines += [f"## {t} (L{r['layer']}, n = {r['n']} items, {r['entities']} bridge items)", "",
                  f"(b) routes (lookup) and the recall's switch per arm; the routes runs' whole-change position share "
                  f"was {r['position_reference']}.", "",
                  "| arm | " + " | ".join(ROUTES) + " | recall switch |", "|---|" + "---|" * (len(ROUTES) + 1)]  # fmt: skip
        for a in r["b"]["lookup"]["arms"]:
            lines.append(f"| {a} | " + " | ".join(fmt(r["b"]["lookup"]["rate"][f"{a}|{rt}"]) for rt in ROUTES)
                         + f" | {fmt(r['b']['recall']['rate'][f'{a}|switched'])} |")  # fmt: skip
        lines += [
            "",
            "Each arm minus none (paired): position, identity, recall switch.",
            "",
            "| arm | position | identity | recall switch |",
            "|---|---|---|---|",
        ]
        lines += [f"| {a} | {fmt(v['position'])} | {fmt(v['identity'])} | {fmt(v['recall'])} |"
                  for a, v in r["b_diffs"].items()]  # fmt: skip
        lines += [
            "",
            "Medians of the change at the bridge word per arm: norm, share in U, cosine with none's.",
            "",
            "| arm | norm | share in U | cos with none |",
            "|---|---|---|---|",
        ]
        lines += [
            f"| {a} | {v['norm']:.2f} | {v['share_U']:.3f} | {v['cos_none']:.3f} |"
            for a, v in r["norms_median"].items()
        ]
        lines += ["", f"Formation clauses: {', '.join(f'{k} {yn(v)}' for k, v in f['clauses'].items())} -> "
                  f"**{'holds' if f['holds'] else 'does not hold'}**.", ""]  # fmt: skip
        if r["c"]:  # a --with-c run: (c) accuracy, descriptive (dropped from the rule)
            lines += ["(c) accuracy per arm (top token = O's answer); dropped by Dan, descriptive only.", "",
                      "| arm | lookup | recall |", "|---|---|---|"]  # fmt: skip
            lines += [f"| {a} | {fmt(r['c']['lookup']['rate'][f'{a}|right'])} | {fmt(r['c']['recall']['rate'][f'{a}|right'])} |"
                      for a in r["c"]["lookup"]["arms"]] + [""]  # fmt: skip
        lines += [f"Edges per arm (item 0; every item the same: {yn(r['edges_same_every_item'])}): "
                  + "; ".join(f"(b) {a} {e['edges']}" for a, e in r["edges_item0"]["b"].items())
                  + "".join(f"; (c) {w} {a} {e['edges']}" for w, v in r["edges_item0"].get("c", {}).items() for a, e in v.items())
                  + ".", ""]  # fmt: skip
    lines += ["## (a) attention from the last token to the locker sentences (descriptive)", ""]
    for t in MODELS:
        a = ares[t]
        if a["status"] != "tested":
            lines += [f"{t}: {a['status']}.", ""]
            continue
        rt = a["routes"]
        lines += [f"### {t} (L{a['layer']}, n = {rt['n']})", "", "| arm | " + " | ".join(ROUTES) + " |",
                  "|---|" + "---|" * len(ROUTES)]  # fmt: skip
        lines += [
            f"| {arm} | " + " | ".join(fmt(rt["rate"][f"{arm}|{x}"]) for x in ROUTES) + " |" for arm in rt["arms"]
        ]
        lines += ["", "Heads whose largest locker mass is most often on the answered locker under the whole change, on "
                  "the items whose answer left A's locker; the same head's rate per arm (chance 1/3):", "",
                  "| layer | head | " + " | ".join(A_ARMS) + " |", "|---|---|" + "---|" * len(A_ARMS)]  # fmt: skip
        lines += [f"| {h['layer']} | {h['head']} | " + " | ".join(str(h.get(x, "-")) for x in A_ARMS) + " |"
                  for h in a["top_heads_moved_whole"]]  # fmt: skip
        lines.append("")
    blob = {"answer": answer, "verdict": verdict, "b": res, "a": ares}
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, default=str) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- the verify-pack view and (a)'s figure (CPU; refuse until Dan's answer) -----------------------------------------


def stage_view(name: str, k: int = N_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> Path:
    """k random items of a run (seed): each reader's O prompt exactly as the model reads it (special tokens and the
    digit's space included) with the sources, destinations and the patch marked, S's bridge, and every arm's answer."""
    require_answer()
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RCK

        tk = RCK.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = X.read_jsonl(src / "cases.jsonl")
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["scene"], r["reader"])].append(r)
    lines = [f"# 47.6 verify-pack view: {name}", "",
             f"{min(k, len(cases))} random items of {len(cases)} (seed {seed}); model {m['model']['target']}, layer "
             f"{m['layer']}, part {m['part']}. Marks: ⟦src-lockerN: …⟧ the locker sentences (the blocks' sources), "
             "⟦filler: …⟧ the controls' sources, ⟦dst-b: …⟧ the asked pick sentence ((b)'s destinations), ⟦patch: …⟧ "
             "the bridge word (where the change is added at L; (b)'s other destinations), ⟦dst-c: …⟧ the question to "
             "the last token ((c)'s destinations). UNVERIFIED.", ""]  # fmt: skip
    for i in sorted(random.Random(seed).sample(range(len(cases)), min(k, len(cases)))):
        c = cases[i]
        lines += [
            f"## {i + 1}. {c['scene']}: bridge {c['bridge']} -> {c['cf_bridge']} in S; expected {c['expect']}",
            "",
        ]
        for w in X.READERS:
            rd = c["readers"][w]
            ids = rd["ids"]["org"] + c["space"]
            marks = marks_of(c["spans"], w)
            lines += [f"### {READER_NAME[w]}: O answers {rd['answer']}, S answers {rd['cf_answer']}", "", "```",
                      marked(decode, ids, marks), "```", "", "| part | arm | answer | route | slot | switched | right |",
                      "|---|---|---|---|---|---|---|"]  # fmt: skip
            lines += [f"| {r['part']} | {r['arm']} | {decode([r['top']])!r} | {r['route'] or ''} | "
                      f"{'' if r['slot'] is None else r['slot']} | {r['switched']} | {r['right']} |" for r in by[(c['scene'], w)]]  # fmt: skip
            lines.append("")
        if "edges" in c:
            lines += ["Edges: " + "; ".join(f"(b) {a} {e['edges']}" for a, e in c["edges"]["b"].items()) + ".", ""]
    out = src / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


ARM_COLOR = {"none": "#3d3d3d", "whole": "#2a78d6", "no_U": "#eb6834", "write": "#1baf7a"}  # dataviz slots 1-3 + ink
ARM_LABEL = {"none": "no patch", "whole": "whole change", "no_U": "change without the pointer directions",
             "write": "pointer write (2x)"}  # fmt: skip


def stage_figures(name: str) -> Path:
    """(a)'s figure for one model: left, per attention layer and head, how often the head's largest locker-sentence
    mass is on the answered locker under the whole change, on the items whose answer left A's locker; right, per layer
    the best head's rate per arm (writes pooled over the two target slots), chance 1/3."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    require_answer()
    a = a_result(name)
    assert a["status"] == "tested", f"{name}: no outcomes"
    layers = a["layers"]
    src = RESULTS / name
    att = np.load(src / "attention.npz")
    rows = X.read_jsonl(src / "outcomes.jsonl")
    slot = {(r["scene"], r["arm"]): r["slot"] for r in rows}
    j = {r["scene"]: r["j"] for r in rows}
    masses = att["masses"].astype(np.float32)
    scenes, arms = list(att["scenes"]), list(att["arms"])
    # pool write1 / write2 into one "write" arm by stacking their items
    pooled = {"none": ["none"], "whole": ["whole"], "no_U": ["no_U"], "write": ["write1", "write2"]}
    best: dict[str, np.ndarray] = {}
    for key, members in pooled.items():
        hits, counts = np.zeros(masses.shape[2:4]), 0
        for arm in members:
            ai = arms.index(arm)
            keep = [i for i, s in enumerate(scenes) if slot[(s, arm)] is not None]
            if not keep:
                continue
            ans = np.array([slot[(scenes[i], arm)] for i in keep])[:, None, None]
            hits = hits + (masses[keep, ai].argmax(-1) == ans).sum(0)
            counts += len(keep)
        best[key] = (hits / counts).max(-1) if counts else np.full(len(layers), np.nan)
    heat = np.array(a["follow_moved"]["whole"], dtype=float)
    n_moved = sum(1 for s in scenes if slot[(s, "whole")] is not None and slot[(s, "whole")] != j[s])
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1.15, 1]})
    im = ax0.imshow(heat.T, aspect="auto", cmap="Blues", vmin=0, vmax=1, origin="lower")
    ax0.set_xticks(range(len(layers)))
    ax0.set_xticklabels(
        [str(x) for x in layers], fontsize=7 if len(layers) > 20 else 9, rotation=90 if len(layers) > 20 else 0
    )
    ax0.set_xlabel("attention layer")
    ax0.set_ylabel("query head")
    step = 1 if heat.shape[1] <= 16 else 4
    ax0.set_yticks(range(0, heat.shape[1], step))
    ax0.set_title(f"Whole change, answer moved off the original locker (n = {n_moved}):\nhow often the head looks "
                  "most at the answered locker's sentence", fontsize=10)  # fmt: skip
    fig.colorbar(im, ax=ax0, fraction=0.04, pad=0.02, label="share of items")
    x = np.arange(len(layers))
    for key, ys in best.items():
        ax1.plot(x, ys, color=ARM_COLOR[key], lw=2, marker="o", ms=4, label=ARM_LABEL[key])
    ax1.axhline(1 / 3, color="#a6a6a6", lw=1, ls="--", label="chance (one of three lockers)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [str(v) for v in layers], fontsize=7 if len(layers) > 20 else 9, rotation=90 if len(layers) > 20 else 0
    )
    ax1.set_ylim(0, 1.02)
    ax1.set_xlabel("attention layer")
    ax1.set_ylabel("best head's share of items")
    ax1.set_title("Best head per layer: largest mass on the answered locker", fontsize=10)
    ax1.grid(axis="y", color="#ececec", lw=0.8)
    ax1.legend(fontsize=8, frameon=False, loc="lower right")
    for ax in (ax0, ax1):
        ax.spines[["top", "right"]].set_visible(False)
    model = {"qwen3.5-9b": "Qwen3.5-9B", "muse-glimmer-30b": "Muse Glimmer 30B"}.get(a["target"], a["target"])
    fig.suptitle(f"{model}: does the last token's attention follow the lookup's answer? (patch at layer {a['layer']})",
                 fontsize=12)  # fmt: skip
    fig.tight_layout()
    out = src / f"figures-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    fig.savefig(out / "attention_follow.png", dpi=150)
    plt.close(fig)
    (out / "attention_follow.json").write_text(json.dumps({"layers": layers, "best_head_rate": {k: v.tolist() for k, v in best.items()},
                                                           "heat_whole_moved": heat.tolist(), "n_moved": n_moved}, indent=1) + "\n")  # fmt: skip
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view", "figures"])
    ap.add_argument("--part", choices=["a", "b"], help="run: (a) the attention measurement, or (b) formation")
    ap.add_argument("--with-c", action="store_true",
                    help="run / plan: also the dropped (c) dereference arms (descriptive, never in a rule)")  # fmt: skip
    ap.add_argument("--name", help="run / view / figures: the run name (results/x47_edges/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.6 (jobs/c3/batch47.yaml; Q47.6, sealed)")
    ap.add_argument("--n-gen", type=int, default=R.N_GEN, help="plan: scenes generated per condition")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.n_gen, a.with_c)
    elif a.stage == "run":
        assert a.part, "run needs --part"
        assert a.name, "run needs --name"
        stage_run(a.part, a.name, a.why, a.with_c)
    elif a.stage == "verdict":
        stage_verdict(n_boot=a.n_boot)
    elif a.stage == "view":
        assert a.name, "view needs --name"
        stage_view(a.name)
    else:
        assert a.name, "figures needs --name"
        stage_figures(a.name)


if __name__ == "__main__":
    main()
