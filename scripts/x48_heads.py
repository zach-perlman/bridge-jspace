"""x48_heads (batch 48, test 48.4; jobs/c3/batch48.yaml, design and rule fixed in advance; Q48.4 in
predictions/2026-10-28_dan.md): why the lookup reads the rest: what the copying heads transmit.

Items: the stored main run's scenes (X0's main test: two people swap picks; x0_necessity, chat, the scenes read at the
layer fixed in advance), kept where the scene is locker-first: both the org and the alt item's locker sentence come
before the asked pick (x0_strata). Nothing is edited.

Per item, three forwards: org and alt without the read suffix (Delta = h_alt - h_org at the bridge word at L, as X0
computes it), and the lookup's org prompt with X0's read suffix appended (the read step), with the softmax attention
of every candidate layer recomputed from that layer's inputs (bridge_jspace.knockout's method, extended to Muse
Glimmer's attention): the mass from the last token to the bridge token, per query head. Candidate layers: layers > L
whose attention is softmax over the whole prompt: the 9B's full_attention layers (its other layers are Gated DeltaNet);
on Muse Glimmer every layer (all 52 are softmax attention; its sliding_attention layers' window, 2048, exceeds every
prompt here, asserted; its config's full_attention layers are the NoPE ones, reported, not a restriction). The recall's
prompt's attention is recorded beside (descriptive). Heads: the five (layer, head) with the largest mean mass over the
items (ties: the lower layer, then the lower head).

W_OV of query head h, with kv group g = h // (n_heads / n_kv) (transformers' repeat_kv): W_OV = W_O[:, h*hd:(h+1)*hd]
@ W_V[g*hd:(g+1)*hd, :], W_O = o_proj.weight [d, n_heads*hd], W_V = v_proj.weight [n_kv*hd, d]: the rule's
W_O W_V, literally ("ov"). What it leaves out, by the HF modelling code of both architectures: the q/k norms (not on
the value path), the sigmoid output gate (a per-channel multiplier computed from the query token: Qwen3.5's gate half of
q_proj, Muse's gate_proj), and the block's input RMSNorm. The input norm's per-dimension gain (1 + weight in both:
Qwen3_5RMSNorm, MuseGlimmerTextCenteredRMSNorm; the per-token 1/rms is a scalar and cancels in a ratio) is a fixed
linear map on the value path, so a second variant folds it in: W_OV diag(1 + w_in) ("ov_gain"), reported beside.
r(x) = ||W_OV x|| / ||x|| for x = the J++ part of Delta (signed OMP, k = 25, over the J++ lens atoms at L as X0 takes
them), the rest Delta - P_J Delta, the address U U^T Delta (U = the 4 pointer directions, x0_massmean's Alf on the
target's x0_probe_v4 states, never refit), and a random part of J++'s share (X0's random subspace, seed 888 + L).
Median over items. r is computed for every candidate head (weights only) and stored; the rule reads the five.

Rule (verdict stage, point medians, variant ov): a head reads the rest if r(rest) >= 2 r(J++) and r(random) is between
them or below both (r(random) <= r(rest)); a model holds on >= 3 of its 5 heads; the batch holds if both models hold.
r(address) reported beside: whether the heads transmit the address at >= r(rest). Cluster-bootstrap CIs of the medians
over the bridge items (10,000, seed 0) beside the points. EPS 1e-9 at the bars.

SEALED: the run writes per-head, per-item r values and no verdict. The verdict stage refuses until
predictions/2026-10-28_dan.md holds Dan's Q48.4 answer at the committed HEAD.

uv run python scripts/x48_heads.py plan                                                  # CPU: items, layers
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_heads.py run --name qwen35_9b_x48_heads   # GPU (sealed)
uv run python scripts/x48_heads.py verdict --runs qwen35_9b_x48_heads muse30_x48_heads   # CPU, after Dan's Q48.4
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import json
import math
import random
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.knockout import FULL, attention_module, config_layer_kinds, decoder_layers, layer_kind
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x48_heads"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch48.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q48.4"
MAIN_RUN = {"qwen3.5-9b": "qwen35_9b_x0_necessity", "muse-glimmer-30b": "muse30b_x0_necessity"}
STATES = {"qwen3.5-9b": "qwen35_9b_x0_probe_v4", "muse-glimmer-30b": "muse30b_x0_probe_v4"}  # x6_routes.STATES
RUNS = {"qwen3.5-9b": "qwen35_9b_x48_heads", "muse-glimmer-30b": "muse30_x48_heads"}
# batch 52 C coverage (amendment 2: the 27B fills every gap): run-stage targets beyond the design's; the
# verdict's own model list is unchanged (verdict --coverage reads these runs alone)
COVERAGE_RUNS = {"qwen3.6-27b": "x48_heads_27b", "nemotron-3.5-lightning": "nem35l_x52_heads48"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x48_heads/x48_heads-20261028T113126Z"  # 48.4's rule first scored (the 9B and Muse)
COVERAGE_SOURCES = {
    "qwen3.6-27b": ("x0_necessity_27b_chat", "x0_probe_v4_27b"),
    "nemotron-3.5-lightning": ("nem35l_x52_conflict", "nem35l_x52_probe"),
}  # (main run, states run)


def main_run_of(target: str) -> str:
    return MAIN_RUN[target] if target in MAIN_RUN else COVERAGE_SOURCES[target][0]


def states_of(target: str) -> str:
    return STATES[target] if target in STATES else COVERAGE_SOURCES[target][1]


RENDERING = "chat"
PARTS = ("jpp", "rest", "address", "random")
VARIANTS = ("ov", "ov_gain")
DECISIVE = "ov"
N_TOP, RATIO, HEADS_MIN, MODELS_MIN, N_U = 5, 2.0, 3, 2, 4
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULE = ("a head reads the rest if r(rest) >= 2 r(J++) with r(random) between them or below both (r(random) <= "
        "r(rest)), medians over items, W_OV = W_O W_V; a model holds on at least 3 of its 5 heads; the batch holds if "
        "both models hold")  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


# ---- pure (CPU) ---------------------------------------------------------------------------------------------------


def candidate_layers(kinds: list[str], layer: int) -> list[int]:
    """The layers after `layer` whose token mixer is softmax attention (knockout's FULL)."""
    return [la for la, k in enumerate(kinds) if k == FULL and la > layer]


def kv_group(head: int, n_heads: int, n_kv: int) -> int:
    """The key/value head query head `head` reads (repeat_kv: each kv head serves n_heads / n_kv consecutive heads)."""
    assert n_heads % n_kv == 0, (n_heads, n_kv)
    return head // (n_heads // n_kv)


def ov_apply(w_o, w_v, head: int, n_heads: int, n_kv: int, head_dim: int, x):
    """W_OV x for the rows of x [n, d]: W_O[:, head's slice] (W_V[its kv group's slice] x), fp32, without the [d, d]
    product. w_o = o_proj.weight [d, n_heads * head_dim], w_v = v_proj.weight [n_kv * head_dim, d]."""
    g = kv_group(head, n_heads, n_kv)
    v = x.float() @ w_v[g * head_dim : (g + 1) * head_dim].float().T  # [n, head_dim]
    return v @ w_o[:, head * head_dim : (head + 1) * head_dim].float().T  # [n, d]


def ov_matrix(w_o, w_v, head: int, n_heads: int, n_kv: int, head_dim: int):
    """The head's W_OV [d, d] (tests and small models)."""
    g = kv_group(head, n_heads, n_kv)
    return w_o[:, head * head_dim : (head + 1) * head_dim].float() @ w_v[g * head_dim : (g + 1) * head_dim].float()


def ratios(y, x) -> list[float]:
    """||y_i|| / ||x_i|| per row; nan where x_i is zero."""
    nx, ny = x.float().norm(dim=-1), y.float().norm(dim=-1)
    return [float(b / a) if a > 0 else math.nan for a, b in zip(nx.tolist(), ny.tolist(), strict=True)]


def select_heads(mass: dict[tuple[int, int], list[float]], k: int = N_TOP) -> list[dict]:
    """The k (layer, head) with the largest mean attention mass over items; ties by the lower layer, then head."""
    ranked = sorted(mass, key=lambda lh: (-statistics.fmean(mass[lh]), lh[0], lh[1]))
    return [{"layer": la, "head": h, "mean_mass": statistics.fmean(mass[(la, h)]),
             "median_mass": statistics.median(mass[(la, h)]), "n": len(mass[(la, h)])} for la, h in ranked[:k]]  # fmt: skip


def head_rule(r: dict[str, float]) -> dict[str, Any]:
    """One head's medians: reads the rest iff r(rest) >= RATIO r(J++) and r(random) <= r(rest) (EPS at the bars)."""
    if any(math.isnan(r[p]) for p in ("jpp", "rest", "random")):
        return {"reads_rest": False, "ratio_ok": False, "random_ok": False, "why": "a median is nan"}
    ratio_ok = r["rest"] >= RATIO * r["jpp"] - EPS
    random_ok = r["random"] <= r["rest"] + EPS
    why = (f"r(rest) = {r['rest']:.4f} {'>=' if ratio_ok else '<'} {RATIO} x r(J++) = {RATIO * r['jpp']:.4f}; "
           f"r(random) = {r['random']:.4f} {'<=' if random_ok else '>'} r(rest)")  # fmt: skip
    return {"reads_rest": ratio_ok and random_ok, "ratio_ok": ratio_ok, "random_ok": random_ok, "why": why}


def model_rule(heads: list[dict]) -> dict[str, Any]:
    """A model holds iff at least HEADS_MIN of its heads read the rest (each head's dict holds its 'rule')."""
    n = sum(bool(h["rule"]["reads_rest"]) for h in heads)
    carries = sum(not math.isnan(h["r"]["address"]) and h["r"]["address"] >= h["r"]["rest"] - EPS for h in heads)
    return {"status": "tested", "holds": n >= HEADS_MIN, "heads_reading_rest": n, "heads": len(heads),
            "heads_address_at_least_rest": carries,
            "why": f"{n} of {len(heads)} heads read the rest (at least {HEADS_MIN} needed)"}  # fmt: skip


def batch_verdict(models: list[dict]) -> dict[str, Any]:
    """Holds once MODELS_MIN models hold; does not hold once too few can still hold; else pending."""
    n_hold = sum(bool(m["holds"]) for m in models)
    n_pending = sum(m["status"] == "pending" for m in models)
    label = "holds" if n_hold >= MODELS_MIN else "does not hold" if n_hold + n_pending < MODELS_MIN else "pending"
    answer = {"holds": "yes", "does not hold": "no"}.get(label, "pending")
    return {"label": label, QUESTION: answer, "models_holding": n_hold, "models": len(models),
            "tested": [m["run"] for m in models if m["status"] == "tested"],
            "pending": [m["run"] for m in models if m["status"] == "pending"]}  # fmt: skip


def parse_answer(text: str, question: str = QUESTION) -> str:
    """The 'Dan:' line of the question's block in a predictions file, '' if none or empty."""
    if f"**{question}**" not in text:
        return ""
    block = text.split(f"**{question}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q48.4 at `rev`, '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return parse_answer(text)


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def median_ci(values: list[float], entities: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> list:
    """[median, lo, hi]: the median over items and its 95% percentile CI from a cluster bootstrap over the bridge
    entities (resample entities with replacement, take their items). nan values are left out."""
    keep = [(v, e) for v, e in zip(values, entities, strict=True) if not math.isnan(v)]
    if not keep:
        return [math.nan, math.nan, math.nan]
    vals = np.array([v for v, _ in keep])
    ents = sorted({e for _, e in keep})
    by = [np.flatnonzero(np.array([e == x for _, e in keep])) for x in ents]
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(ents), size=(n_boot, len(ents)))
    meds = np.array([np.median(vals[np.concatenate([by[j] for j in row])]) for row in draws])
    return [float(np.median(vals)), float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))]


# ---- items (no model) ---------------------------------------------------------------------------------------------


def select(main_run: str, layer: int, space: list[int]) -> tuple[list[dict], dict]:
    """The main run's chat scenes read at the layer, in its order, kept where both the org and the alt item's locker
    sentence come before the asked pick (x0_strata), with the counts. `space` is X0's chat read suffix (the space
    token's ids, suite_v1.ids(tok, " ")), which the stored cases of the main runs do not carry."""
    src = X.RESULTS / main_run
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt", "cf") == "cf", f"{main_run}: alt {m.get('alt')!r}, not the main test's cf"
    assert m["predicted"] == layer, f"{main_run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{main_run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    scenes: dict[str, None] = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] == RENDERING and r["layer"] == layer and r["arm"] == "whole" and r["reader"] == X.LOOKUP:
            scenes.setdefault(r["scene"])
    assert scenes, f"{main_run}: no chat outcomes at layer {layer}"
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    out, order = [], collections.Counter()
    for scene in scenes:
        c = cases[scene]
        feats = ST.features(c)
        key = f"org {feats['org locker vs asked pick']}, alt {feats['alt locker vs asked pick']}"
        order[key] += 1
        if feats["org locker vs asked pick"] != "before" or feats["alt locker vs asked pick"] != "before":
            continue
        out.append({"scene": scene, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
                    "upstream": c["upstream"], "pos": c["pos"], "space": list(space), "features": feats,
                    "context": c["context"], "cf_context": c["cf_context"],
                    "readers": {w: {k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "ids")}
                                for w in X.READERS}})  # fmt: skip
    counts = {"main_run": main_run, "layer": layer, "items_at_L": len(scenes), "locker vs asked pick": dict(order),
              "items": len(out), "entities": len({it["entity"] for it in out}),
              "max_read_len": max(len(it["readers"][w]["ids"]["org"]) + len(space)
                                  for it in out for w in X.READERS) if out else 0}  # fmt: skip
    return out, counts


def read_suffix(tok) -> list[int]:
    """X0's chat read suffix: the ids of a space (suite_v1.ids), appended to the prompt at the read step."""
    from scripts import suite_v1 as S

    return S.ids(tok, " ")


def marked(tok, ids: list[int], pos: int, space: list[int]) -> str:
    """The prompt as the model reads it at the read step, the bridge token and the read token marked."""
    return (tok.decode(ids[:pos]) + "⟦bridge:" + tok.decode([ids[pos]]) + "⟧" + tok.decode(ids[pos + 1 :])
            + "⟦read:" + tok.decode(space) + "⟧")  # fmt: skip


def stage_plan() -> dict:
    """CPU: the target's items (its tokenizer for the read suffix), the candidate layers and head counts from the
    pinned config."""
    from huggingface_hub import hf_hub_download
    from transformers import AutoConfig

    from scripts import x45m

    assert pins.TARGET in MAIN_RUN or pins.TARGET in COVERAGE_SOURCES, f"48.4 does not run on {pins.TARGET}"
    layer = X.PREDICTED[pins.TARGET]
    _items, counts = select(main_run_of(pins.TARGET), layer, read_suffix(x45m.tokenizer()))
    path = hf_hub_download(pins.MODEL_REPO, "config.json", revision=pins.MODEL_REVISION)  # the cache when present
    cfg = AutoConfig.from_pretrained(path).get_text_config()
    counts.update(target=pins.TARGET, **architecture(cfg, layer))
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


def architecture(cfg, layer: int) -> dict:
    """The candidate layers and head geometry of a text config."""
    kinds = config_layer_kinds(cfg)
    types = list(getattr(cfg, "layer_types", None) or [])
    cand = candidate_layers(kinds, layer)
    return {"candidate_layers": cand, "config_full_attention": [la for la in cand if types and types[la] == "full_attention"],
            "layer_types": dict(collections.Counter(types)) if types else "none listed (softmax attention everywhere)",
            "sliding_window": getattr(cfg, "sliding_window", None), "n_heads": cfg.num_attention_heads,
            "n_kv": cfg.num_key_value_heads, "head_dim": cfg.head_dim,
            "candidate_heads": len(cand) * cfg.num_attention_heads}  # fmt: skip


# ---- attention capture (both architectures) -----------------------------------------------------------------------


@contextlib.contextmanager
def capture_last_attention(model, layers: list[int], q_pos: int, out: dict[int, Any]):
    """While active, a forward of one prompt [1, T] fills out[layer] = the softmax attention [heads, T] from position
    q_pos to every key position, recomputed from each listed layer's own inputs (the forward keeps its attention
    implementation). Qwen3.5: the query half of q_proj, per-head q_norm / k_norm, rotary, repeat_kv, scaling, causal
    softmax (as knockout.capture_attention). Muse Glimmer: q_proj and k_proj through the shared unscaled qk_norm, the
    query times qk_scale_factor, rotary unless the layer is NoPE (position_embeddings None), the sliding window where
    the layer has one (keys at or before q_pos - window blocked, as transformers' sliding_window_overlay)."""
    import torch

    blocks: Any = decoder_layers(model)
    home = getattr(model, "hf", model).get_input_embeddings().weight.device

    def hook_for(la: int):
        def hook(module, args, kwargs):
            hs = kwargs["hidden_states"] if "hidden_states" in kwargs else args[0]
            pe = kwargs.get("position_embeddings")
            ns: Any = sys.modules[type(module).__module__]
            b, t, _ = hs.shape
            assert b == 1, f"one prompt at a time, got a batch of {b}"
            shape = (b, t, -1, module.head_dim)
            if hasattr(module, "qk_norm"):  # Muse Glimmer
                q = module.qk_norm(module.q_proj(hs).view(shape).transpose(1, 2)) * module.qk_scale_factor
                k = module.qk_norm(module.k_proj(hs).view(shape).transpose(1, 2))
            elif type(module).__name__ == "NemotronHAttention":  # batch 52: plain q / k projections, no norm, NoPE
                q = module.q_proj(hs).view(shape).transpose(1, 2)
                k = module.k_proj(hs).view(shape).transpose(1, 2)
            else:  # Qwen3.5: q_proj holds the query and its output gate
                q, _gate = torch.chunk(module.q_proj(hs).view(b, t, -1, module.head_dim * 2), 2, dim=-1)
                q = module.q_norm(q.reshape(shape)).transpose(1, 2)
                k = module.k_norm(module.k_proj(hs).view(shape)).transpose(1, 2)
            if pe is not None:
                q, k = ns.apply_rotary_pos_emb(q, k, *pe)
            k = ns.repeat_kv(k, module.num_key_value_groups)
            scores = (q[0, :, q_pos : q_pos + 1].float() @ k[0].float().transpose(-1, -2))[
                :, 0
            ] * module.scaling  # [heads, T]
            keys = torch.arange(t, device=hs.device)
            blocked = keys > q_pos
            window = getattr(module, "sliding_window", None)
            if window:
                blocked |= keys <= q_pos - window
            probs = scores.masked_fill(blocked, float("-inf")).softmax(-1)
            out[la] = probs if probs.device == home else probs.to(home)

        return hook

    handles = []
    for la in layers:
        assert layer_kind(blocks[la]) == FULL, f"layer {la} is not a softmax-attention layer"
        handles.append(attention_module(blocks[la]).register_forward_pre_hook(hook_for(la), with_kwargs=True))
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


def input_gain(block) -> Any:
    """The block's input RMSNorm gain per dimension, fp32: 1 + weight for the zero-centred norms of Qwen3.5
    (Qwen3_5RMSNorm) and Muse Glimmer (MuseGlimmerTextCenteredRMSNorm); weight otherwise (NemotronH's pre-mixer `norm`,
    NemotronHRMSNorm: a plain weight, batch 52)."""
    norm = block.input_layernorm if hasattr(block, "input_layernorm") else block.norm
    name = type(norm).__name__
    w = norm.weight.float()
    return 1.0 + w if ("Centered" in name or name.startswith("Qwen3_5")) else w


# ---- GPU ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.4 reads the main run's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN or target in COVERAGE_SOURCES, f"48.4 does not run on {target}"
    main_run, layer = main_run_of(target), X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / main_run
    states = pins.RESULTS_DIR / "x0_probe" / states_of(target) / "states.npz"
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "48.4",
         "spec": "jobs/c3/batch48.yaml (48.4)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl", states)},
         "main_run": main_run, "layer": layer, "states_run": states_of(target), "k": X.K_MAIN, "omp": "signed",
         "parts": {"jpp": "the J++ part of Delta (signed OMP, k = 25, J++ lens atoms at L, letter tokens)",
                   "rest": "Delta minus its J++ part", "address": "U U^T Delta, U = x0_massmean's Alf (4 pointer "
                   "directions on the x0_probe_v4 states; not refit)",
                   "random": f"a random part of J++'s share (X0's random subspace, seed {X.SUBSPACE_SEED} + layer)"},
         "items_rule": "the main run's chat scenes read at L, kept where both the org and the alt item's locker "
                       "sentence come before the asked pick (x0_strata); unedited",
         "delta": "h_alt - h_org at the bridge word at L, X0's two forwards (no read suffix)",
         "attention": "one forward of the reader's org prompt with X0's read suffix appended; per candidate layer the "
                      "softmax attention from the last token to the bridge token, per query head, recomputed from the "
                      "layer's inputs (capture_last_attention); the lookup's selects the heads, the recall's is beside",
         "candidate_layers_rule": "layers > L whose token mixer is softmax attention over the whole prompt: the 9B's "
                                  "full_attention layers; on Muse every layer (sliding window 2048 > every prompt, "
                                  "asserted; its config's full_attention = NoPE layers, reported)",
         "head_selection": f"the {N_TOP} (layer, head) with the largest mean lookup mass over items; ties: the lower "
                           "layer, then the lower head",
         "w_ov": {"ov": "W_O[:, h*hd:(h+1)*hd] @ W_V[g*hd:(g+1)*hd, :], g = h // (n_heads / n_kv); the rule's",
                  "ov_gain": "ov @ diag(1 + input_layernorm.weight): the block's input RMSNorm gain folded in (beside)",
                  "excluded": "the q/k norms (not on the value path), the sigmoid output gate (query-token dependent), "
                              "the per-token 1/rms of the input norm (a scalar, cancels in r)"},
         "r": "||W_OV x|| / ||x|| per item and part; stored for every candidate head (r_all.npz) and per item for the "
              "five (r_items.jsonl)", "rule": RULE, "decisive_variant": DECISIVE,
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer"},
         "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    cfg = model.hf.config.get_text_config()
    arch = architecture(cfg, layer)
    kinds = config_layer_kinds(cfg)
    for la in arch["candidate_layers"]:
        assert layer_kind(decoder_layers(model)[la]) == kinds[la]
    items, counts = select(main_run, layer, read_suffix(tok))
    assert items, "no items"
    if arch["sliding_window"]:
        assert counts["max_read_len"] <= arch["sliding_window"], (
            f"a prompt of {counts['max_read_len']} tokens exceeds the sliding window {arch['sliding_window']}: the "
            "sliding layers would not attend over the whole prompt; rethink the candidate layers"
        )
    for it in items:
        for w in X.READERS:
            ids = it["readers"][w]["ids"]["org"]
            it["readers"][w]["marked"] = marked(tok, ids, it["pos"], it["space"])
            assert tok.decode([ids[it["pos"]]]).strip() == it["entity"], f"{it['scene']}: the bridge token moved"
    counts.update(target=target, **arch)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)

    cand, n_heads, n_kv, hd = arch["candidate_layers"], arch["n_heads"], arch["n_kv"], arch["head_dim"]
    blocks = decoder_layers(model)
    dev = model.device
    deltas, att_rows = [], []
    mass: dict[str, dict[tuple[int, int], list[float]]] = {w: collections.defaultdict(list) for w in X.READERS}
    with torch.no_grad():
        for it in progress(items, f"48.4 at L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer] for v in ("org", "alt")}
            deltas.append((h["alt"][it["pos"]] - h["org"][it["pos"]]).float())
            for w in X.READERS:
                read = it["readers"][w]["ids"]["org"] + it["space"]
                att: dict[int, Any] = {}
                with capture_last_attention(model, cand, len(read) - 1, att):
                    model.run(torch.tensor([read], device=dev))
                for la in cand:
                    row = att[la][:, it["pos"]].tolist()
                    att_rows.append(
                        {"scene": it["scene"], "reader": w, "layer": la, "mass": [round(v, 6) for v in row]}
                    )
                    for hh, v in enumerate(row):
                        mass[w][(la, hh)].append(v)
        X.write_jsonl(out / "attention.jsonl", att_rows)
        heads = select_heads(mass[X.LOOKUP])
        for sel in heads:
            sel["recall_mean_mass"] = statistics.fmean(mass[X.RECALL][(sel["layer"], sel["head"])])
        (out / "heads.json").write_text(json.dumps({"selected_by": "lookup", "heads": heads}, indent=2) + "\n")
        print("heads:", json.dumps(heads), flush=True)

        x = torch.stack(deltas)  # [n, d] fp32, home device
        jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
        part = X.fit(jdic, x.to(jdic.device), X.K_MAIN, "signed").float().to(dev)
        share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        rand = SP.random_subspace_part(x, share, basis).float()
        u = torch.tensor(MM.subspaces(states_of(target))[0]["Alf"], dtype=torch.float32, device=dev)
        assert u.shape[1] == N_U, f"U has {u.shape[1]} directions, not {N_U}"
        addr = (x @ u) @ u.T
        parts = {"jpp": part, "rest": x - part, "address": addr, "random": rand}
        shares = [{"scene": it["scene"], "delta_norm": round(float(x[i].norm()), 4),
                   **{f"{p}_share": round(float(parts[p][i].norm() ** 2 / x[i].norm().clamp_min(1e-30) ** 2), 5)
                      for p in PARTS}} for i, it in enumerate(items)]  # fmt: skip
        X.write_jsonl(out / "shares.jsonl", shares)
        del jdic
        torch.cuda.empty_cache()

        r_all = {v: np.full((len(cand), n_heads, len(items), len(PARTS)), np.nan, dtype=np.float32) for v in VARIANTS}
        for li, la in enumerate(progress(cand, "48.4 W_OV (layer)")):
            attn: Any = attention_module(blocks[la])
            w_o, w_v = attn.o_proj.weight, attn.v_proj.weight
            assert tuple(w_o.shape) == (x.shape[1], n_heads * hd), w_o.shape
            assert tuple(w_v.shape) == (n_kv * hd, x.shape[1]), w_v.shape
            gain = input_gain(blocks[la]).to(dev)
            for hh in range(n_heads):
                for v in VARIANTS:
                    for pi, p in enumerate(PARTS):
                        xp = parts[p] if v == "ov" else parts[p] * gain
                        y = ov_apply(w_o.to(dev), w_v.to(dev), hh, n_heads, n_kv, hd, xp)
                        r_all[v][li, hh, :, pi] = np.array(ratios(y, parts[p]), dtype=np.float32)
        np.savez_compressed(out / "r_all.npz", layers=np.array(cand), parts=np.array(PARTS), ov=r_all["ov"],
                            ov_gain=r_all["ov_gain"])  # fmt: skip
        medians = [{"layer": la, "head": hh, "variant": v, "lookup_mean_mass": round(statistics.fmean(mass[X.LOOKUP][(la, hh)]), 6),
                    **{p: round(float(np.nanmedian(r_all[v][li, hh, :, pi])), 6) for pi, p in enumerate(PARTS)}}
                   for li, la in enumerate(cand) for hh in range(n_heads) for v in VARIANTS]  # fmt: skip
        X.write_jsonl(out / "r_all_medians.jsonl", medians)
        rows = [{"scene": it["scene"], "entity": it["entity"], "layer": h_["layer"], "head": h_["head"], "variant": v,
                 "lookup_mass": round(mass[X.LOOKUP][(h_["layer"], h_["head"])][i], 6),
                 "recall_mass": round(mass[X.RECALL][(h_["layer"], h_["head"])][i], 6),
                 "r": {p: float(r_all[v][cand.index(h_["layer"]), h_["head"], i, pi]) for pi, p in enumerate(PARTS)}}
                for h_ in heads for v in VARIANTS for i, it in enumerate(items)]  # fmt: skip
        X.write_jsonl(out / "r_items.jsonl", rows)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One run: pending (not here), or per head and variant the medians (with CIs) and the rule (variant ov)."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "r_items.jsonl").exists():
        target = {r: t for t, r in {**RUNS, **COVERAGE_RUNS}.items()}.get(run)
        assert target, f"no 48.4 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False,
                "why": "the run has no manifest or r_items here"}  # fmt: skip
    m = json.loads((src / "manifest.json").read_text())
    heads = json.load((src / "heads.json").open())["heads"]
    rows = X.read_jsonl(src / "r_items.jsonl")
    assert len(heads) == N_TOP, f"{run}: {len(heads)} heads, not {N_TOP}"
    for h_ in heads:
        for v in VARIANTS:
            mine = [r for r in rows if (r["layer"], r["head"], r["variant"]) == (h_["layer"], h_["head"], v)]
            ents = [r["entity"] for r in mine]
            h_[v] = {p: median_ci([r["r"][p] for r in mine], ents, n_boot) for p in PARTS}
            h_[v]["n"] = len(mine)
        h_["r"] = {p: h_[DECISIVE][p][0] for p in PARTS}
        h_["rule"] = head_rule(h_["r"])
    plan = json.loads((src / "plan.json").read_text())
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "main_run": m["main_run"],
            **model_rule(heads), "selected_heads": heads, "plan": plan}  # fmt: skip


def fmt(v: list) -> str:
    return "-" if v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]")  # fmt: skip


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items (seed 0): the lookup's prompt as read (bridge and read tokens marked), and on each selected head
    its mass from the last token to the bridge token (lookup / recall) and r per part (variant ov)."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    heads = json.load((src / "heads.json").open())["heads"]
    by = {
        (r["scene"], r["layer"], r["head"]): r for r in X.read_jsonl(src / "r_items.jsonl") if r["variant"] == DECISIVE
    }
    lines = [f"## {run}: {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} (alt {it['cf_bridge']}); lookup "
                  f"{it['readers'][X.LOOKUP]['id']}: O's answer {it['readers'][X.LOOKUP]['answer']}", "", "```",
                  it["readers"][X.LOOKUP]["marked"], "```", "",
                  "| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |",
                  "|---|---|---|---|---|---|---|"]  # fmt: skip
        for h_ in heads:
            r = by[(it["scene"], h_["layer"], h_["head"])]
            lines.append(f"| L{h_['layer']}:h{h_['head']:02d} | {r['lookup_mass']:.3f} | {r['recall_mass']:.3f} | "
                         + " | ".join(f"{r['r'][p]:.3f}" for p in PARTS) + " |")  # fmt: skip
        lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """48.4's verdict (sealed until Q48.4), or with coverage (batch 52 C) the same rule on the given coverage runs alone:
    no seal guard, "no prediction" in place of Dan's answer, no pending rows, written to x52_heads48-<UTC>/."""
    answer = (f"{NO_PREDICTION}; rule first scored in {SCORED}; the both-models count covers the given runs only, "
              "not re-scored") if coverage else dan_answer()  # fmt: skip
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    known = set(COVERAGE_RUNS) if coverage else set(MAIN_RUN)
    assert set(targets) <= known, f"48.4 runs on {sorted(known)}, not {sorted(set(targets) - known)}"
    if not coverage:
        models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
                   for t in MAIN_RUN if t not in targets]  # fmt: skip
    v = batch_verdict(models)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    stem = "x52_heads48" if coverage else "x48_heads"
    out = next(p for p in (RESULTS / f"{stem}-{stamp}{s}" for s in ("", *(f"-{i}" for i in range(2, 100))))
               if not p.exists())  # a second verdict within the same second gets its own folder (never overwritten)  # fmt: skip
    out.mkdir(parents=True)
    lines = ["# 48.4: what the copying heads transmit", "",
             f"Batch 48, test 48.4 (jobs/c3/batch48.yaml; {QUESTION}, Dan: {answer}). Unedited locker-first main-test "
             "scenes; the five heads at layers > L with the most attention mass from the last token to the bridge token "
             "(lookup prompt, read step); r(x) = ||W_OV x|| / ||x||, W_OV = W_O W_V per head (kv group by repeat_kv), "
             f"medians over items with cluster-bootstrap CIs over bridge items ({n_boot}, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             f"**Verdict: {v['label']}** ({QUESTION} {v[QUESTION]}): {v['models_holding']} of {v['models']} models hold "
             f"(both needed)" + (f"; pending: {', '.join(v['pending'])}" if v["pending"] else "") + ".", "",
             "| model | run | status | items | heads reading the rest | heads with r(address) >= r(rest) | holds |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m.get('target', '-')} | {m['run']} | pending ({m['why']}) | | | | |")
            continue
        lines.append(f"| {m['target']} | {m['run']} | {m['status']} | {m['plan']['items']} | {m['heads_reading_rest']} of "
                     f"{m['heads']} | {m['heads_address_at_least_rest']} of {m['heads']} | {'yes' if m['holds'] else 'no'} |")  # fmt: skip
    for variant in VARIANTS:
        lines += ["", f"Per head, variant {variant}" + (" (the rule's)" if variant == DECISIVE else
                  " (the input norm's gain folded in; beside)") + ": median r per part [95% CI].", "",
                  "| model | head | lookup mass (mean) | recall mass (mean) | r(J++) | r(rest) | r(address) | r(random) | reads the rest |",
                  "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for m in models:
            if m["status"] == "pending":
                continue
            for h_ in m["selected_heads"]:
                verdict = (
                    head_rule({p: h_[variant][p][0] for p in PARTS})["reads_rest"]
                    if variant != DECISIVE
                    else h_["rule"]["reads_rest"]
                )
                lines.append(f"| {m['target']} | L{h_['layer']}:h{h_['head']:02d} | {h_['mean_mass']:.3f} | "
                             f"{h_['recall_mean_mass']:.3f} | " + " | ".join(fmt(h_[variant][p]) for p in PARTS)
                             + f" | {'yes' if verdict else 'no'} |")  # fmt: skip
    if coverage:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ")
    lines += ["", "Items and layers (descriptive):", ""]
    for m in models:
        if m["status"] == "pending":
            continue
        p = m["plan"]
        lines.append(f"- {m['target']} ({m['run']}, from {m['main_run']}, L{m['layer']}): {p['items']} items of "
                     f"{p['items_at_L']} at L (locker vs asked pick {p['locker vs asked pick']}); candidate layers "
                     f"{p['candidate_layers']} (config full_attention {p['config_full_attention']}; layer types "
                     f"{p['layer_types']}; sliding window {p['sliding_window']}, longest read {p['max_read_len']}); "
                     f"{p['n_heads']} query heads, {p['n_kv']} kv heads, head dim {p['head_dim']}; per head: "
                     + "; ".join(f"L{h_['layer']}:h{h_['head']:02d} {h_['rule']['why']}" for h_ in m["selected_heads"]))  # fmt: skip
    (out / "x48_heads.json").write_text(json.dumps({"runs": runs, "dan": answer, "verdict": v, "models": models},
                                                   indent=1) + "\n")  # fmt: skip
    (out / "x48_heads.md").write_text("\n".join(lines) + "\n")
    ex = ["# 48.4 examples (verify pack): the lookup's prompt exactly as the model reads it at the read step; "
          "⟦bridge:…⟧ the bridge token, ⟦read:…⟧ the appended read token (the query position). UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x48_heads/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 48.4 runs (9B, Muse)")
    ap.add_argument("--why", default="batch 48, test 48.4 (jobs/c3/batch48.yaml; Q48.4)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        stage_verdict(a.runs, a.n_boot, a.coverage)


if __name__ == "__main__":
    main()
