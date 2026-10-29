"""x49_attn (batch 49, test 49.7; jobs/c3/batch49.yaml, design and rules fixed in advance, amendment 2 included; Q49.7
in predictions/2026-10-28_dan.md): does the question's attention follow the written address?

Scenes: x8_write's items (x8_write.eligible: the routes test's C2 scenes, their original prompt O, x6_routes' generator,
gate and eligibility; locker-first by construction: three locker sentences, then three pick sentences), the first 300
eligible as x8 ran them. j = the bridge item's locker slot, k = each other slot (two writes per item).

Arms at the bridge word at L = X.PREDICTED (one forward each, the lookup's O prompt with X0's chat read suffix, the
attention recorded in the same forward): none; swap = h + s (mu_k - mu_j), s = 2, mu = x0_massmean.pointer_means (x8's
means, not refit); random = h + a random vector of the swap's norm (one per item and k, seed 4401 as x8_write). The
recall is read under the same arms (X0's chat read, batched as x8 reads).

Attention: softmax probabilities recomputed from each recorded layer's own inputs (x48_heads' method for Qwen3.5 and
Muse Glimmer, extended to several query positions), from the last token (the appended read token) and from each token
of the question text, to every token. Recorded layers: every softmax-attention layer > L. The 9B's (and 27B's) Gated
DeltaNet layers are skipped and logged (manifest 'skipped_linear_layers'); on Muse every layer > L (its sliding window
exceeds every prompt, asserted). Per head and query site (last; question = the mean over the question tokens): the mass
on each locker sentence (all its tokens, by character overlap) split into the item token(s), the number token(s) and the
rest; the attention entropy; the total-variation distance from the none arm's distribution; the mean pre-softmax logit
on each sentence's tokens. Stored per item (none) and per (item, k) (swap, random) for every recorded head, so the
verdict is CPU-only.

Heads (in the job, before the ablation; no outcome is read): items split by bridge entity into a fit and a read half
(sorted entities shuffled with random.Random(0), the first half fit). Candidate heads = the five (layer, head) with the
most mass on the locker sentences (the three summed) at the last token under none, mean over fit items
(x48_heads.select_heads' ties). The best head = the candidate with the largest mean move on the fit half's switched
pairs (none switched: the first candidate). move = (mass on slot k's sentence - mass on slot j's) under the arm minus
the same under none. Necessity arm (read half only): the best head's output (its slice of o_proj's input) zeroed at the
last token, and separately at the question tokens, under none and under each swap; both readers. States for the
weights-level check: the input to each candidate layer's attention (post input-norm) at the last token and the mean over
each locker sentence's tokens, every item, unedited; the best head's W_Q and W_K rows.

Rules (verdict stage, read half, decisive site: the last token; EPS 1e-9 at the bars; cluster bootstrap over bridge
entities, 10,000, seed 0): see RULES. SEALED: the run writes no verdict; verdict and view refuse until
predictions/2026-10-28_dan.md holds Dan's Q49.7 answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x49_attn.py plan                              # CPU: counts, 5 prompts
BJ_TARGET=qwen3.5-9b uv run python scripts/x49_attn.py run --name qwen35_9b_x49_7        # GPU (sealed)
uv run python scripts/x49_attn.py verdict --runs qwen35_9b_x49_7 muse30_x49_7 x49_7_27b   # CPU, after Dan's Q49.7
uv run python scripts/x49_attn.py view --runs qwen35_9b_x49_7 muse30_x49_7 x49_7_27b
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import json
import math
import random
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
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x48_heads as H

EXP = "x49_attn"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch49.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q49.7"
RUNS = {"qwen3.5-9b": "qwen35_9b_x49_7", "muse-glimmer-30b": "muse30_x49_7", "qwen3.6-27b": "x49_7_27b"}
# batch 52 C coverage (key row 10): Lightning (NemotronH; attention blocks 5 / 12 / 19 / 26 / 33 / 42, those > L14
# recorded); verdict --coverage reads it alone, 49.7's RUNS and own verdict unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_attn"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x49_attn/x49_7-20261028T154511Z"  # 49.7's rules first scored
S_WRITE = 2.0
SPLIT_SEED = 0
SITES = ("last", "question")
DECISIVE = "last"
PARTS = ("item", "num", "rest")
N_TOP = 5
FOLLOW, RANDOM_MAX, NONSWITCH_MAX = 0.30, 0.05, 0.10
ELSEWHERE, SWITCH_MIN, DISTRIBUTED = 0.15, 0.30, 0.30
NEC_FALL, NEC_IDENTITY, NEC_RECALL = 0.5, 0.10, 0.10
EPS = 1e-9
RULES = {
    "follows": "on read-half pairs where the lookup switched to slot k's locker under the swap, >= 1 of the five "
    "candidate heads has mean move >= 0.30 (cluster-bootstrap CI excluding 0), its mean move under the random vector on "
    "the same pairs <= 0.05, and its mean move on the non-switched swap pairs <= 0.10",
    "elsewhere": "the lookup switches to slot k on >= 0.3 of the read-half swap pairs and no recorded head (every "
    "full-attention layer > L, every head) reaches a mean move of 0.15 on the switched pairs",
    "distributed": "the summed mean move over the five candidate heads, or over every head of the best head's layer, is "
    ">= 0.30 while no single candidate head reaches 0.30 (beside the per-head rule)",
    "necessity": "the best head (chosen on the fit half) carries the position route if, under the swap with its output "
    "zeroed at the site, the lookup's switch to slot k falls by >= 0.5 of its swap value while the identity answers "
    "(read-half swap pairs answering slot j's locker under the swap) change <= 0.10 and the recall's answer changes "
    "<= 0.10 (swap + zero vs swap); per site (last token; question tokens)",
    "not_in_full_attention": "on a model with Gated DeltaNet layers, if 'elsewhere' holds: 'the dereference is not in "
    "full attention on this model' (Muse decides)",
}


# ---- pure (CPU) ---------------------------------------------------------------------------------------------------


# What the skipped layers (no softmax attention) are, per model; wording only. Lightning's: NemotronH's Mamba-2 and MoE
# blocks (config layers_block_type: mamba / moe / attention, snapshot a9904d24).
SKIPPED_KIND = {"qwen3.5-9b": "Gated DeltaNet", "qwen3.6-27b": "Gated DeltaNet",
                "nemotron-3.5-lightning": "Mamba-2 and MoE blocks"}  # fmt: skip


def skipped_kind(target: str) -> str:
    return SKIPPED_KIND.get(target, "no softmax attention")


def recorded_layers(kinds: list[str], layer: int) -> tuple[list[int], list[int]]:
    """The softmax-attention layers after `layer` (recorded) and the other layers after it (skipped: Gated DeltaNet on
    Qwen3.5, Mamba-2 and MoE blocks on NemotronH; SKIPPED_KIND)."""
    full = H.candidate_layers(kinds, layer)
    return full, [la for la, k in enumerate(kinds) if la > layer and k != FULL]


def locker_groups(offsets: list[tuple[int, int]], text: str, context: str) -> list[dict[str, list[int]]]:
    """Per locker slot (sentence order), its token positions by character overlap: the item word, the number, the rest
    of the sentence (every token overlapping the sentence that is neither). Asserted disjoint across slots and parts."""
    from scripts import statement_positions as SP

    assert text.count(context) == 1, "the context is not once in the prompt"
    base = text.index(context)
    out = []
    for m in W.LOCKER.finditer(context):
        sent = SP.tokens_in(offsets, base + m.start(), base + m.end())
        item = SP.tokens_in(offsets, base + m.start(1), base + m.end(1))
        num = SP.tokens_in(offsets, base + m.start(2), base + m.end(2))
        assert item, f"{m.group(0)!r}: no item token"
        assert num, f"{m.group(0)!r}: no number token"
        assert not set(item) & set(num), f"{m.group(0)!r}: item {item}, number {num} overlap"
        out.append({"item": item, "num": num, "rest": [p for p in sent if p not in item and p not in num]})
    assert len(out) == 3, f"{len(out)} locker sentences, not 3"
    flat = [p for g in out for part in PARTS for p in g[part]]
    assert len(flat) == len(set(flat)), "the locker sentences' tokens overlap"
    return out


def question_positions(offsets: list[tuple[int, int]], text: str, context: str, question: str) -> list[int]:
    """The question text's tokens (character overlap), after the context."""
    from scripts import statement_positions as SP

    q0 = text.index(context) + len(context)
    assert text.count(question, q0) == 1, "the question is not once after the context"
    i = text.index(question, q0)
    got = SP.tokens_in(offsets, i, i + len(question))
    assert got, "no question token"
    return got


def group_matrix(n_tokens: int, groups: list[dict[str, list[int]]]) -> np.ndarray:
    """[T, 9] one-hot: column slot * 3 + part (PARTS order); probs @ G = the mass per slot and part."""
    g = np.zeros((n_tokens, 3 * len(PARTS)), dtype=np.float32)
    for s, grp in enumerate(groups):
        for p, part in enumerate(PARTS):
            g[grp[part], s * len(PARTS) + p] = 1.0
    return g


def sentence_mean_matrix(n_tokens: int, groups: list[dict[str, list[int]]]) -> np.ndarray:
    """[T, 3]: column s averages over all of slot s's sentence tokens."""
    g = np.zeros((n_tokens, 3), dtype=np.float32)
    for s, grp in enumerate(groups):
        pos = [p for part in PARTS for p in grp[part]]
        g[pos, s] = 1.0 / len(pos)
    return g


def split_halves(entities: list[str], seed: int = SPLIT_SEED) -> tuple[set[str], set[str]]:
    """Fit and read halves of the bridge entities: sorted, shuffled with random.Random(seed), the first half fit
    (x8_write.stage_pairs' split)."""
    ents = sorted(set(entities))
    random.Random(seed).shuffle(ents)
    return set(ents[: len(ents) // 2]), set(ents[len(ents) // 2 :])


def slot_mass(mass: np.ndarray) -> np.ndarray:
    """[..., 3 slots, 3 parts] -> [..., 3 slots]."""
    return mass.sum(-1)


def moves(mass_arm: np.ndarray, mass_none: np.ndarray, j: np.ndarray, k: np.ndarray) -> np.ndarray:
    """Per pair: (m[k] - m[j]) under the arm minus the same under none. mass_*: [P, ..., 3 slots] (none already taken
    at the pair's item), j, k: [P] slot indices."""

    def diff(m: np.ndarray) -> np.ndarray:
        shape = (-1,) + (1,) * (m.ndim - 1)
        return np.take_along_axis(m, k.reshape(shape), -1)[..., 0] - np.take_along_axis(m, j.reshape(shape), -1)[..., 0]

    return diff(mass_arm) - diff(mass_none)


def select_candidates(locker_mass: np.ndarray, layers: list[int], fit: np.ndarray, k: int = N_TOP) -> list[dict]:
    """The k (layer, head) with the most locker-sentence mass under none, mean over the fit items. locker_mass:
    [items, layers, heads] (the three sentences summed, decisive site); fit: [items] bool."""
    sub = locker_mass[fit]
    mass = {(la, h): sub[:, li, h].tolist() for li, la in enumerate(layers) for h in range(sub.shape[2])}
    return H.select_heads(mass, k)


def best_head(cands: list[dict], move_fit: dict[tuple[int, int], np.ndarray]) -> tuple[dict, str]:
    """The candidate with the largest mean move on the fit half's switched pairs (ties: the earlier candidate); with no
    switched fit pair, the first candidate."""
    if not any(len(v) for v in move_fit.values()):
        return cands[0], "no switched pair on the fit half: the candidate with the most locker mass"
    scored = [(float(np.mean(move_fit[(c["layer"], c["head"])])), -i, c) for i, c in enumerate(cands)]
    best = max(scored, key=lambda t: (t[0], t[1]))
    return best[2], f"the largest mean move on the fit half's switched pairs ({best[0]:.4f})"


def mean_ci(values: np.ndarray, entities: list[str], n_boot: int = X.N_BOOT) -> list[float]:
    """[mean, lo, hi]: the mean over rows, its 95% cluster-bootstrap interval over the entities (X.resampled_rates)."""
    if len(values) == 0:
        return [math.nan, math.nan, math.nan]
    rr = X.resampled_rates({"v": np.asarray(values, dtype=float).tolist()}, list(entities), n_boot)
    return [float(np.mean(values)), *X.interval(rr["v"])]


def head_stats(swap: np.ndarray, rand: np.ndarray, switched: np.ndarray, ents: list[str], n_boot: int) -> dict:
    """One head's moves on the read pairs: switched swap pairs (mean, CI), the random vector on the same pairs, the
    non-switched swap pairs."""
    e = np.array(ents)
    return {"swap_switched": mean_ci(swap[switched], e[switched].tolist(), n_boot),
            "random_switched": mean_ci(rand[switched], e[switched].tolist(), n_boot),
            "swap_nonswitched": mean_ci(swap[~switched], e[~switched].tolist(), n_boot),
            "n_switched": int(switched.sum()), "n_nonswitched": int((~switched).sum())}  # fmt: skip


def follows_head(st: dict) -> bool:
    m, lo = st["swap_switched"][0], st["swap_switched"][1]
    return bool(st["n_switched"] > 0 and m >= FOLLOW - EPS and lo > 0 and st["random_switched"][0] <= RANDOM_MAX + EPS
                and not st["swap_nonswitched"][0] > NONSWITCH_MAX + EPS)  # fmt: skip


def rules(heads: list[dict], all_max: float, switch_share: float, sums: dict[str, float], has_linear: bool) -> dict:
    """The fixed rules on the five candidate heads' stats (each with 'stats'), the largest mean move on switched pairs
    over every recorded head, the read half's switch share, the two summed moves (five / best layer)."""
    follows = [f"L{h['layer']}:h{h['head']}" for h in heads if follows_head(h["stats"])]
    elsewhere = switch_share >= SWITCH_MIN - EPS and all_max < ELSEWHERE
    single = max((h["stats"]["swap_switched"][0] for h in heads), default=math.nan)
    distributed = max(sums.values()) >= DISTRIBUTED - EPS and not single >= FOLLOW - EPS
    label = "follows" if follows else "elsewhere" if elsewhere else "neither"
    out = {"label": label, "follows_heads": follows, "elsewhere": bool(elsewhere), "distributed": bool(distributed),
           "max_move_all_heads": all_max, "max_move_candidates": single, "switch_share": switch_share, "sums": sums}  # fmt: skip
    if has_linear and elsewhere:
        out["caveat"] = "the dereference is not in full attention on this model"
    return out


def necessity(rows: list[dict]) -> dict:
    """Per read-half swap pair: {'target_swap', 'target_zero' (0/1), 'identity_swap' (lookup answered slot j under the
    swap), 'lookup_changed' (top under swap + zero != under swap), 'recall_changed'}. The rule (RULES['necessity'])."""
    if not rows:
        return {"n": 0, "holds": False, "why": "no pairs"}
    s_swap = float(np.mean([r["target_swap"] for r in rows]))
    s_zero = float(np.mean([r["target_zero"] for r in rows]))
    ident = [r["lookup_changed"] for r in rows if r["identity_swap"]]
    id_change = float(np.mean(ident)) if ident else math.nan
    rc = float(np.mean([r["recall_changed"] for r in rows]))
    falls = s_swap > 0 and s_swap - s_zero >= NEC_FALL * s_swap - EPS
    holds = bool(falls and not id_change > NEC_IDENTITY + EPS and rc <= NEC_RECALL + EPS)
    return {"n": len(rows), "switch_swap": s_swap, "switch_zero": s_zero, "fall_share": (s_swap - s_zero) / s_swap
            if s_swap > 0 else math.nan, "falls": bool(falls), "identity_n": len(ident), "identity_changed": id_change,
            "recall_changed": rc, "holds": holds}  # fmt: skip


def dominance(s: np.ndarray) -> float:
    """(mean diagonal - mean off-diagonal) / SD of the off-diagonal entries (ddof 0); nan if undefined."""
    off = s[~np.eye(s.shape[0], dtype=bool)]
    if np.isnan(s).any() or float(np.std(off)) == 0.0:
        return math.nan
    return float((np.mean(np.diag(s)) - np.mean(off)) / np.std(off))


def score_matrix(w_q: np.ndarray, w_k: np.ndarray, mu_q: np.ndarray, mu_src: np.ndarray) -> np.ndarray:
    """S[k, k'] = (W_Q mu^q_k)^T (W_K mu^src_k'): w_q, w_k [hd, d]; mu_q, mu_src [3, d]. RoPE and the q/k norms are
    left out."""
    return (mu_q @ w_q.T) @ (mu_src @ w_k.T).T


def parse_answer(text: str) -> str:
    """Dan's Q49.7 answer (x47_chain.dan_answer's regex: per-model 'Dan (...):' lines and bullets), '' if none."""
    return H.parse_answer(text, QUESTION)


def dan_answer(rev: str = "HEAD") -> str:
    import subprocess

    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return parse_answer(text)


def sealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


# ---- items (tokenizer only) ---------------------------------------------------------------------------------------


def rendered(tok, context: str, question: str) -> str:
    return X.render(
        tok, {"format": "prose", "kind": "digit", "context": context, "question": question}, "chat", context
    )


def read_space(tok, case: dict) -> list[int]:
    """X0's chat read suffix (suite_v1.ids(tok, " ")); older stored cases do not carry it, newer ones must agree."""
    from scripts import suite_v1 as S

    space = S.ids(tok, " ")
    assert case.get("space", space) == space, f"{case['scene']}: the stored read suffix differs"
    return space


def layout(tok, case: dict) -> dict:
    """The lookup's O prompt as read: the read ids (O + X0's space suffix), the bridge, the locker groups, the question
    tokens and the last (read) position, checked against the case's stored ids."""
    from bridge_jspace.tokens import raw_encoding

    rd = case["readers"][X.LOOKUP]
    text = rendered(tok, case["context"], rd["question"])
    enc = raw_encoding(tok, text, offsets=True)
    ids = rd["ids"]["org"]
    assert enc["input_ids"] == ids, f"{case['scene']}: the rendered prompt's ids differ from the case's"
    off = enc["offset_mapping"]
    groups = locker_groups(off, text, case["context"])
    q = question_positions(off, text, case["context"], rd["question"])
    last = len(ids)
    flat = [p for g in groups for part in PARTS for p in g[part]]
    assert max(flat) < case["pos"] < min(q) < last, f"{case['scene']}: lockers, bridge, question out of order"
    return {"groups": groups, "question": q, "last": last, "read_len": last + len(read_space(tok, case))}


def item_record(tok, case: dict, half: str) -> dict:
    from scripts import suite_v1 as S

    sl = W.slots_of(case["context"])
    j = [x for x, _ in sl].index(case["bridge"])
    return {"scene": case["scene"], "entity": case["bridge"], "half": half, "j": j, "ks": [k for k in W.SLOTS if k != j],
            "slots": [[x, d] for x, d in sl], "digit_tokens": [S.answer_token(tok, str(d), "digit") for _, d in sl],
            "pos": case["pos"], "space": read_space(tok, case), "context": case["context"], "layout": layout(tok, case),
            "readers": {w: {k: case["readers"][w][k] for k in ("question", "answer", "tok_A")} | {"ids": case["readers"][w]["ids"]["org"]}
                        for w in X.READERS}}  # fmt: skip


def marked(tok, it: dict) -> str:
    """The lookup's prompt exactly as read: ⟦bridge:…⟧, each locker sentence ⟦slot s (j/k):…⟧, ⟦read:…⟧ the appended
    read token."""
    ids = it["readers"][X.LOOKUP]["ids"] + it["space"]
    start, end = {}, {}
    for s, g in enumerate(it["layout"]["groups"]):
        pos = sorted(p for part in PARTS for p in g[part])
        start[pos[0]] = f"⟦slot{s} ({'j' if s == it['j'] else 'k'}):"
        end[pos[-1]] = "⟧"
    out = []
    for i, t in enumerate(ids):
        piece = tok.decode([t])
        if i == it["pos"]:
            piece = f"⟦bridge:{piece}⟧"
        if i == len(ids) - 1:
            piece = f"⟦read:{piece}⟧"
        out.append(start.get(i, "") + piece + end.get(i, ""))
    return "".join(out)


def stored_items(target: str) -> list[dict]:
    """x8's items from its stored run: the lookup's none rows (its order) mapped to the routes run's C2 cases."""
    x8 = W.RESULTS / W.X8_RUN[target]
    scenes = [
        r["scene"] for r in X.read_jsonl(x8 / "outcomes.jsonl") if r["reader"] == X.LOOKUP and r["kind"] == "none"
    ]
    cases = {c["scene"]: c for c in X.read_jsonl(R.RESULTS / W.ROUTES_OF[target] / "cases.jsonl")
             if c["condition"] == "C2"}  # fmt: skip
    return [cases[s] for s in scenes]


def stage_plan() -> Path:
    """CPU (tokenizer and config): x8's stored items for this target, their layouts, the split, x8's s = 2 switch share
    (public since batch 44), the recorded / skipped layers, the forward count, 5 rendered prompts (seed 0)."""
    from huggingface_hub import hf_hub_download
    from transformers import AutoConfig

    from scripts import x45m

    target = pins.TARGET
    assert target in RUNS, f"49.7 runs on {sorted(RUNS)}, not {target}"
    tok = x45m.tokenizer()
    layer = X.PREDICTED[target]
    cases = stored_items(target)
    ents = [c["bridge"] for c in cases]
    fit, _read = split_halves(ents)
    items = [item_record(tok, c, "fit" if c["bridge"] in fit else "read") for c in cases]
    path = hf_hub_download(pins.MODEL_REPO, "config.json", revision=pins.MODEL_REVISION)
    cfg = AutoConfig.from_pretrained(path).get_text_config()
    kinds = config_layer_kinds(cfg)
    full, skipped = recorded_layers(kinds, layer)
    x8 = [r for r in X.read_jsonl(W.RESULTS / W.X8_RUN[target] / "outcomes.jsonl")
          if r["reader"] == X.LOOKUP and r["kind"] == "write" and r["s"] == S_WRITE]  # fmt: skip
    half = {it["scene"]: it["half"] for it in items}
    n_read = sum(it["half"] == "read" for it in items)
    counts = {"target": target, "layer": layer, "x8_run": W.X8_RUN[target], "routes_run": W.ROUTES_OF[target],
              "items": len(items), "entities": len(set(ents)), "fit_items": len(items) - n_read, "read_items": n_read,
              "fit_entities": len(fit), "read_entities": len(set(ents) - fit), "pairs": 2 * len(items),
              "read_pairs": 2 * n_read,
              "x8_s2_target_share": {"all": float(np.mean([r["class"] == "target" for r in x8])),
                                     **{h: float(np.mean([r["class"] == "target" for r in x8 if half[r["scene"]] == h]))
                                        for h in ("fit", "read")}},
              "x8_s2_switched_pairs": {h: sum(r["class"] == "target" for r in x8 if half[r["scene"]] == h)
                                       for h in ("fit", "read")},
              "recorded_layers": full, "skipped_linear_layers": skipped, "n_heads": cfg.num_attention_heads,
              "n_kv": cfg.num_key_value_heads, "head_dim": cfg.head_dim, "recorded_heads": len(full) * cfg.num_attention_heads,
              "sliding_window": getattr(cfg, "sliding_window", None),
              "max_read_len": max(it["layout"]["read_len"] for it in items),
              "question_tokens": dict(collections.Counter(len(it["layout"]["question"]) for it in items)),
              "locker_sentence_tokens": dict(collections.Counter(sum(len(g[p]) for p in PARTS)
                                                                 for it in items for g in it["layout"]["groups"])),
              "forwards": {"pass1_lookup_captured": 5 * len(items), "pass1_recall_reads": 5 * len(items),
                           "states": len(items), "ablation_reads": 2 * 2 * 3 * n_read + 2 * 3 * n_read,
                           "competence_reads": "x8_write.eligible over the routes generator's C2 scenes (as x8)"}}  # fmt: skip
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = RESULTS / f"plan-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    (out / f"plan_{target}.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    picks = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(items)), 5))
    lines = [f"# 49.7 plan, {target}: 5 random items (seed {X.EXAMPLES_SEED}) of {len(items)}", "",
             "The lookup's O prompt exactly as the model reads it (chat template, X0's read suffix appended); ⟦bridge:…⟧ the "
             "write position (L = " + f"{layer}), ⟦slotS (j|k):…⟧ each locker sentence's tokens (j = the bridge item's "
             "slot, k = a written slot), ⟦read:…⟧ the last token (a query site). Question tokens = the question text's "
             "tokens. UNVERIFIED.", ""]  # fmt: skip
    for i in picks:
        it = items[i]
        lo = it["layout"]
        lines += [f"## {it['scene']} ({it['half']} half): bridge {it['entity']}, j = {it['j']}, k in {it['ks']}; lockers "
                  f"{it['slots']}", "", "```", marked(tok, it), "```", "",
                  f"Question tokens {lo['question']} ({tok.decode([it['readers'][X.LOOKUP]['ids'][p] for p in lo['question']])!r}); "
                  "slot groups (item / number / rest): " + "; ".join(
                      f"slot{s} {g['item']} / {g['num']} / {g['rest']}" for s, g in enumerate(lo["groups"])), ""]  # fmt: skip
    (out / f"prompts_{target}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("wrote", out)
    return out


# ---- attention capture and head ablation ---------------------------------------------------------------------------


@contextlib.contextmanager
def capture_queries(model, layers: list[int], q_positions: list[int], out: dict[int, Any], inputs: dict | None = None):
    """While active, a forward of one prompt [1, T] fills out[layer] = (probs, scores) [heads, Q, T]: the softmax
    attention from each of q_positions to every key, and its pre-softmax scores (blocked keys -inf), recomputed from
    each listed layer's own inputs as x48_heads.capture_last_attention does (Qwen3.5: the query half of q_proj, q_norm /
    k_norm, rotary; Muse Glimmer: shared qk_norm, qk_scale_factor, rotary unless NoPE, the sliding window). With
    `inputs`, inputs[layer] = the attention's input [T, d] (post input-norm), fp32. Only softmax-attention layers."""
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
            qp = torch.tensor(list(q_positions), device=hs.device)
            scores = (q[0][:, qp].float() @ k[0].float().transpose(-1, -2)) * module.scaling  # [heads, Q, T]
            keys = torch.arange(t, device=hs.device)[None, :]
            blocked = keys > qp[:, None]
            window = getattr(module, "sliding_window", None)
            if window:
                blocked |= keys <= qp[:, None] - window
            scores = scores.masked_fill(blocked, float("-inf"))
            probs = scores.softmax(-1)
            out[la] = (probs.to(home), scores.to(home))
            if inputs is not None:
                inputs[la] = hs[0].float().to(home)

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


@contextlib.contextmanager
def zero_head(model, layer: int, head: int, positions: list[int]):
    """While active, query head `head` of `layer` contributes nothing at `positions`: its slice of o_proj's input (the
    head's attention output, after Qwen3.5's / Muse's sigmoid gate) is zeroed there, in every row of the batch."""
    attn: Any = attention_module(decoder_layers(model)[layer])
    hd = attn.head_dim
    pos = list(positions)

    def hook(_module, args):
        if not pos or args[0].shape[1] <= max(pos):  # a cached decoding step: the prompt positions are not in it
            return None
        x = args[0].clone()
        x[:, pos, head * hd : (head + 1) * hd] = 0
        return (x, *args[1:])

    handle = attn.o_proj.register_forward_pre_hook(hook)
    try:
        yield
    finally:
        handle.remove()


def head_qk_weights(attn, head: int, n_heads: int, n_kv: int, hd: int) -> tuple[Any, Any]:
    """The query head's W_Q rows [hd, d] (Qwen3.5: the query half of its q_proj block, not the gate) and its kv group's
    W_K rows [hd, d], fp32."""
    wq, wk = attn.q_proj.weight.float(), attn.k_proj.weight.float()
    d = wq.shape[1]
    gated = wq.shape[0] == 2 * n_heads * hd  # Qwen3.5: per head [query | gate]
    w_q = wq.view(n_heads, 2 * hd, d)[head, :hd] if gated else wq.view(n_heads, hd, d)[head]
    return w_q, wk.view(n_kv, hd, d)[H.kv_group(head, n_heads, n_kv)]


def reduce(probs, scores, g, gmean, sites: dict[str, list[int]]):
    """From [heads, Q, T] probs and scores: per site (mean over its query indices) the mass per slot and part [heads,
    sites, 9], the entropy [heads, sites], the mean logit on each sentence's tokens [heads, sites, 3]."""
    import torch

    mass = probs @ g  # [H, Q, 9]
    ent = -(probs * probs.clamp_min(1e-30).log()).sum(-1)  # [H, Q]
    logit = torch.nan_to_num(scores, neginf=0.0) @ gmean  # [H, Q, 3]; sentence tokens are never blocked
    pick = lambda x: torch.stack([x[:, sites[s]].mean(1) for s in SITES], 1)  # noqa: E731
    return pick(mass), pick(ent), pick(logit)


def tv_sites(probs, probs_none, sites: dict[str, list[int]]):
    """Total-variation distance from the none arm's attention, per head and site [heads, sites]."""
    import torch

    tv = 0.5 * (probs - probs_none).abs().sum(-1)  # [H, Q]
    return torch.stack([tv[:, sites[s]].mean(1) for s in SITES], 1)


# ---- GPU ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.knockout import layer_kinds
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.7 reads chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"49.7 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    x8 = W.RESULTS / W.X8_RUN[target]
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "test": "49.7", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "spec": "jobs/c3/batch49.yaml (49.7, amendment 2)",
        "question": f"{QUESTION} ({PREDICTIONS})", "layer": layer, "s": S_WRITE, "mu_from": R.STATES[target],
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in
                   (SPEC, x8 / "manifest.json", x8 / "outcomes.jsonl",
                    pins.RESULTS_DIR / "x0_probe" / R.STATES[target] / "states.npz") if p.exists()},
        "items_rule": "x8_write.eligible (the routes test's C2 scenes, O, its gate and eligibility; the first 300), as x8 ran",
        "arms": {"none": "O unedited", "swap": f"h + {S_WRITE} (mu_k - mu_j) at the bridge word at L, k each other slot",
                 "random": f"h + a random vector of the swap's norm (one per item and k, seed {W.RAND_SEED})"},
        "attention": "softmax probabilities recomputed from each softmax-attention layer > L's inputs (capture_queries), "
                     "from the last (read) token and each question-text token; sites: last, question (mean over its tokens)",
        "split": f"bridge entities sorted, shuffled with random.Random({SPLIT_SEED}), first half fit",
        "candidates": f"top {N_TOP} (layer, head) by locker-sentence mass (three summed) at the last token under none, mean "
                      "over fit items; best = the largest mean move on fit switched pairs",
        "necessity": "the best head's o_proj-input slice zeroed at the last token / the question tokens, under none and "
                     "each swap, read half, both readers",
        "rules": RULES, "seeds": {"scenes": R.SEED, "random_vectors": W.RAND_SEED, "split": SPLIT_SEED,
                                  "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
        "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {
            "question": NO_PREDICTION,
            "batch": 52,
            "rules_first_scored": SCORED,
            "sealed": "none (batch 52 coverage)",
        }
    manifest = out / "manifest.json"
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", manifest, flush=True)

    model = load_model()
    tok = model.tokenizer
    cfg = model.hf.config.get_text_config()
    kinds = layer_kinds(model)
    full, skipped = recorded_layers(kinds, layer)
    print(f"recording layers {full}; skipped ({skipped_kind(pins.TARGET)}) {skipped}", flush=True)
    n_heads, n_kv, hd = cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim
    m.update(recorded_layers=full, skipped_linear_layers=skipped, n_heads=n_heads, n_kv=n_kv, head_dim=hd,
             sliding_window=getattr(cfg, "sliding_window", None))  # fmt: skip
    chosen, gate, ws, _ = W.eligible(model, X.GATE, W.N_ITEMS)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not chosen:
        (out / "status.json").write_text(json.dumps({"status": "not tested", "gate": gate}, indent=2) + "\n")
        manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print("the gate missed: not tested", gate, flush=True)
        return out
    if (x8 / "outcomes.jsonl").exists():
        x8_scenes = [
            r["scene"] for r in X.read_jsonl(x8 / "outcomes.jsonl") if r["reader"] == X.LOOKUP and r["kind"] == "none"
        ]
        m["same_items_as_x8"] = [c["scene"] for c in chosen] == x8_scenes
    fit, _ = split_halves([c["bridge"] for c in chosen])
    items = [item_record(tok, c, "fit" if c["bridge"] in fit else "read") for c in chosen]
    if m["sliding_window"]:
        longest = max(it["layout"]["read_len"] for it in items)
        assert longest <= m["sliding_window"], f"a {longest}-token prompt exceeds the sliding window"
    X.write_jsonl(out / "cases.jsonl", items)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

    dev = model.device
    mu = {k: torch.tensor(v, dtype=torch.float32, device=dev) for k, v in MM.pointer_means(R.STATES[target]).items()}
    gen = torch.Generator().manual_seed(W.RAND_SEED)
    n, nl, n_pairs = len(items), len(full), 2 * len(items)
    shape_i, shape_p = (n, nl, n_heads, len(SITES)), (n_pairs, nl, n_heads, len(SITES))
    arr = {"mass_none": np.zeros((*shape_i, 3 * len(PARTS)), np.float32), "ent_none": np.zeros(shape_i, np.float32),
           "logit_none": np.zeros((*shape_i, 3), np.float32)}  # fmt: skip
    for a in ("swap", "random"):
        arr[f"mass_{a}"] = np.zeros((*shape_p, 3 * len(PARTS)), np.float32)
        arr[f"ent_{a}"] = np.zeros(shape_p, np.float32)
        arr[f"logit_{a}"] = np.zeros((*shape_p, 3), np.float32)
        arr[f"tv_{a}"] = np.zeros(shape_p, np.float32)
    pair_item, pair_k, rows, norms = [], [], [], []

    def lookup_forward(it: dict, vec):
        lo = it["layout"]
        ids = it["readers"][X.LOOKUP]["ids"] + it["space"]
        q_pos = [*lo["question"], lo["last"]]
        sites = {"question": list(range(len(lo["question"]))), "last": [len(q_pos) - 1]}
        att: dict[int, Any] = {}
        edits = {layer: AddRows(vec[None], [it["pos"]])} if vec is not None else None
        with capture_queries(model, full, q_pos, att):
            logits, _ = model.run(torch.tensor([ids], device=dev), edits)
        return int(logits.argmax()), att, sites

    with torch.no_grad():
        for i, it in enumerate(progress(items, f"49.7 pass 1 at L{layer} (item)")):
            j, toks = it["j"], dict(enumerate(it["digit_tokens"]))
            T = it["layout"]["read_len"]
            g = torch.tensor(group_matrix(T, it["layout"]["groups"]), device=dev)
            gm = torch.tensor(sentence_mean_matrix(T, it["layout"]["groups"]), device=dev)
            arms: list[tuple[str, int | None, Any]] = [("none", None, None)]
            for k in it["ks"]:
                step = S_WRITE * (mu[k] - mu[j])
                r = torch.randn(step.shape[0], generator=gen).to(dev)
                arms += [("swap", k, step), ("random", k, r / r.norm() * step.norm())]
                norms.append({"scene": it["scene"], "k": k, "swap_norm": round(float(step.norm()), 4)})
            p_none = None
            for kind, k, vec in arms:
                top, att, sites = lookup_forward(it, vec)
                red = {la: reduce(att[la][0], att[la][1], g, gm, sites) for la in full}
                if kind == "none":
                    p_none = {la: att[la][0] for la in full}
                    for li, la in enumerate(full):
                        arr["mass_none"][i, li], arr["ent_none"][i, li], arr["logit_none"][i, li] = (
                            x.cpu().numpy() for x in red[la]
                        )
                else:
                    pi = 2 * i + it["ks"].index(k)
                    for li, la in enumerate(full):
                        arr[f"mass_{kind}"][pi, li], arr[f"ent_{kind}"][pi, li], arr[f"logit_{kind}"][pi, li] = (
                            x.cpu().numpy() for x in red[la]
                        )
                        arr[f"tv_{kind}"][pi, li] = tv_sites(att[la][0], p_none[la], sites).cpu().numpy()  # type: ignore[index]
                cls = (
                    W.classify(top, toks, j, k)
                    if k is not None
                    else W.classify(top, toks, j, (j + 1) % 3).replace("target", "third")
                )  # none: slot j's digit = original; another slot's = third
                rows.append({"scene": it["scene"], "entity": it["entity"], "half": it["half"], "reader": X.LOOKUP,
                             "arm": kind, "j": j, "k": k, "zero": None, "top": top, "class": cls})  # fmt: skip
            for k in it["ks"]:
                pair_item.append(i)
                pair_k.append(k)
            rd = it["readers"][X.RECALL]
            edits = [{}] + [{layer: AddRows(vec[None], [it["pos"]])} for _, _, vec in arms[1:]]
            logits, _ = X.read_logits(model, rd["ids"], edits, "chat", it["space"], ws)
            for (kind, k, _), lg in zip(arms, logits, strict=True):
                top = int(lg.argmax())
                rows.append({"scene": it["scene"], "entity": it["entity"], "half": it["half"], "reader": X.RECALL,
                             "arm": kind, "j": j, "k": k, "zero": None, "top": top, "changed": int(top != rd["tok_A"])})  # fmt: skip
        X.write_jsonl(out / "outcomes.jsonl", rows)
        X.write_jsonl(out / "norms.jsonl", norms)
        np.savez_compressed(
            out / "attention.npz",
            layers=np.array(full),
            sites=np.array(SITES),
            parts=np.array(PARTS),
            pair_item=np.array(pair_item),
            pair_k=np.array(pair_k),
            **{
                k: v.astype(np.float16) if k.startswith(("mass_swap", "mass_random", "tv")) else v
                for k, v in arr.items()
            },
        )  # fmt: skip (none kept fp32: the verdict reselects from it)

        # heads on the fit half (no read-half outcome is used)
        is_fit = np.array([it["half"] == "fit" for it in items])
        si = SITES.index(DECISIVE)
        cands = select_candidates(arr["mass_none"][:, :, :, si].sum(-1), full, is_fit)
        lk = {(r["scene"], r["arm"], r["k"]): r for r in rows if r["reader"] == X.LOOKUP}
        pi_arr, pk_arr = np.array(pair_item), np.array(pair_k)
        pj_arr = np.array([items[i]["j"] for i in pair_item])
        sw_fit = np.array([is_fit[i] and lk[(items[i]["scene"], "swap", k)]["class"] == "target"
                           for i, k in zip(pair_item, pair_k, strict=True)])  # fmt: skip
        mv = moves(
            slot_mass(arr["mass_swap"].reshape(*shape_p, 3, len(PARTS))[:, :, :, si]),
            slot_mass(arr["mass_none"].reshape(*shape_i, 3, len(PARTS))[pi_arr][:, :, :, si]),
            pj_arr,
            pk_arr,
        )  # [P, L, H]
        move_fit = {(c["layer"], c["head"]): mv[sw_fit, full.index(c["layer"]), c["head"]] for c in cands}
        best, why_best = best_head(cands, move_fit)
        (out / "heads.json").write_text(json.dumps({"candidates": cands, "best": best, "why_best": why_best,
                                                    "fit_switched_pairs": int(sw_fit.sum())}, indent=2) + "\n")  # fmt: skip
        print("candidates:", json.dumps(cands), "best:", best, why_best, flush=True)

        # states for the weights-level check (unedited, every item), the best head's W_Q / W_K
        st_layers = sorted({c["layer"] for c in cands})
        st = {la: {"last": np.zeros((n, cfg.hidden_size), np.float32), "src": np.zeros((n, 3, cfg.hidden_size), np.float32)}
              for la in st_layers}  # fmt: skip
        for i, it in enumerate(progress(items, "49.7 states (item)")):
            lo = it["layout"]
            ins: dict[int, Any] = {}
            with capture_queries(model, st_layers, [lo["last"]], {}, inputs=ins):
                model.run(torch.tensor([it["readers"][X.LOOKUP]["ids"] + it["space"]], device=dev))
            for la in st_layers:
                st[la]["last"][i] = ins[la][lo["last"]].cpu().numpy()
                for s, grp in enumerate(lo["groups"]):
                    pos = [p for part in PARTS for p in grp[part]]
                    st[la]["src"][i, s] = ins[la][pos].mean(0).cpu().numpy()
        np.savez_compressed(out / "states.npz", j=np.array([it["j"] for it in items]), layers=np.array(st_layers),
                            **{f"last_L{la}": v["last"] for la, v in st.items()},
                            **{f"src_L{la}": v["src"] for la, v in st.items()})  # fmt: skip
        attn: Any = attention_module(decoder_layers(model)[best["layer"]])
        w_q, w_k = head_qk_weights(attn, best["head"], n_heads, n_kv, hd)
        np.savez_compressed(out / "head_weights.npz", w_q=w_q.cpu().numpy(), w_k=w_k.cpu().numpy(),
                            layer=best["layer"], head=best["head"])  # fmt: skip

        # the necessity arm: the best head zeroed (read half), under none and each swap, both readers
        abl = []
        for it in progress([x for x in items if x["half"] == "read"], "49.7 ablation (read item)"):
            j, toks = it["j"], dict(enumerate(it["digit_tokens"]))
            base: list[tuple[str, int | None, Any]] = [("none", None, None)]
            base += [("swap", k, S_WRITE * (mu[k] - mu[j])) for k in it["ks"]]
            edits = [{}] + [{layer: AddRows(v[None], [it["pos"]])} for _, _, v in base[1:]]
            for zero, pos in ((None, []), ("last", [it["layout"]["last"]]), ("question", it["layout"]["question"])):
                ctx = zero_head(model, best["layer"], best["head"], pos) if zero else contextlib.nullcontext()
                with ctx:
                    for w in X.READERS:
                        rd = it["readers"][w]
                        logits, _ = X.read_logits(model, rd["ids"], edits, "chat", it["space"], ws)
                        for (kind, k, _), lg in zip(base, logits, strict=True):
                            top = int(lg.argmax())
                            row = {"scene": it["scene"], "entity": it["entity"], "reader": w, "arm": kind, "j": j, "k": k,
                                   "zero": zero, "top": top}  # fmt: skip
                            if w == X.LOOKUP:
                                row["class"] = W.classify(top, toks, j, k if k is not None else (j + 1) % 3)
                                if k is None:
                                    row["class"] = row["class"].replace("target", "third")
                            else:
                                row["changed"] = int(top != rd["tok_A"])
                            abl.append(row)
        X.write_jsonl(out / "ablation.jsonl", abl)
    m["items"], m["pairs"] = n, n_pairs
    m["fit_items"], m["read_items"] = int(is_fit.sum()), int((~is_fit).sum())
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    (out / "status.json").write_text(json.dumps({"status": "tested"}, indent=2) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def load(run: str) -> dict:
    src = RESULTS / run
    a = np.load(src / "attention.npz")
    d = {k: a[k] for k in a.files}
    return {"src": src, "m": json.loads((src / "manifest.json").read_text()), "items": X.read_jsonl(src / "cases.jsonl"),
            "rows": X.read_jsonl(src / "outcomes.jsonl"), "abl": X.read_jsonl(src / "ablation.jsonl"),
            "heads": json.loads((src / "heads.json").read_text()), "a": d}  # fmt: skip


def analyse(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One run: pending / not tested / the rules and the report-beside numbers."""
    src = RESULTS / run
    if not (src / "status.json").exists():
        return {"run": run, "status": "pending", "why": "no status.json (not run or not finished)"}
    status = json.loads((src / "status.json").read_text())
    if status["status"] != "tested":
        return {"run": run, "status": status["status"], "why": f"read gate: {status.get('gate')}"}
    D = load(run)
    a, items, m = D["a"], D["items"], D["m"]
    layers = [int(x) for x in a["layers"]]
    nl, n_heads = len(layers), int(m["n_heads"])
    p_item, p_k = a["pair_item"].astype(int), a["pair_k"].astype(int)
    p_j = np.array([items[i]["j"] for i in p_item])
    read = np.array([items[i]["half"] == "read" for i in p_item])
    ents = [items[i]["entity"] for i in p_item]
    lk = {(r["scene"], r["arm"], r["k"]): r for r in D["rows"] if r["reader"] == X.LOOKUP}
    cls = {a_: np.array([lk[(items[i]["scene"], a_, k)]["class"] for i, k in zip(p_item, p_k, strict=True)])
           for a_ in ("swap", "random")}  # fmt: skip
    switched = cls["swap"] == "target"
    n_items = len(items)

    def m5(name, n):
        return a[name].astype(np.float32).reshape(n, nl, n_heads, len(SITES), 3, len(PARTS))

    mass = {"none": m5("mass_none", n_items)[p_item], "swap": m5("mass_swap", len(p_item)),
            "random": m5("mass_random", len(p_item))}  # fmt: skip
    mv = {
        arm: moves(slot_mass(mass[arm]), slot_mass(mass["none"]), p_j, p_k) for arm in ("swap", "random")
    }  # [P, L, H, S]
    r_ents = [e for e, keep in zip(ents, read, strict=True) if keep]
    r_sw = switched[read]
    out: dict[str, Any] = {"run": run, "status": "tested", "target": m["model"]["target"], "layer": m["layer"],
                           "recorded_layers": layers, "skipped_linear_layers": m["skipped_linear_layers"],
                           "items": n_items, "read_pairs": int(read.sum()), "read_switched": int(r_sw.sum())}  # fmt: skip
    sw = cls["swap"][read]
    out["switch_share"] = mean_ci((sw == "target").astype(float), r_ents, n_boot)
    out["lookup_shares"] = {
        arm: {c: float(np.mean(cls[arm][read] == c)) for c in W.CLASSES} for arm in ("swap", "random")
    }
    none_cls = [lk[(it["scene"], "none", None)]["class"] for it in items if it["half"] == "read"]
    out["lookup_shares"]["none"] = {
        c: float(np.mean([x == c for x in none_cls])) for c in ("original", "third", "other")
    }
    cands, best = D["heads"]["candidates"], D["heads"]["best"]
    # the candidates recomputed here from the stored masses (fit half), as a check of the job's selection
    is_fit = np.array([it["half"] == "fit" for it in items])
    si = SITES.index(DECISIVE)
    again = select_candidates(a["mass_none"][:, :, :, si].sum(-1), layers, is_fit)  # the job's sum, same order
    assert [(c["layer"], c["head"]) for c in again] == [(c["layer"], c["head"]) for c in cands], "candidates differ"
    per_site = {}
    for s_i, site in enumerate(SITES):
        sw_m, rd_m = mv["swap"][read][..., s_i], mv["random"][read][..., s_i]
        heads = []
        for c in cands:
            li = layers.index(c["layer"])
            heads.append(
                {**c, "stats": head_stats(sw_m[:, li, c["head"]], rd_m[:, li, c["head"]], r_sw, r_ents, n_boot)}
            )
        all_mean = sw_m[r_sw].mean(0) if r_sw.any() else np.full((nl, n_heads), np.nan)  # [L, H]
        all_max = float(np.nanmax(all_mean)) if r_sw.any() else math.nan
        bl = layers.index(best["layer"])
        sum5 = np.sum([sw_m[:, layers.index(c["layer"]), c["head"]] for c in cands], 0)
        sum_layer = sw_m[:, bl, :].sum(-1)
        sums = {
            "five": mean_ci(sum5[r_sw], [e for e, s in zip(r_ents, r_sw, strict=True) if s], n_boot),
            "best_layer": mean_ci(sum_layer[r_sw], [e for e, s in zip(r_ents, r_sw, strict=True) if s], n_boot),
        }
        verdict = rules(heads, all_max, out["switch_share"][0], {k: v[0] for k, v in sums.items()},
                        bool(m["skipped_linear_layers"]))  # fmt: skip
        top_all = np.unravel_index(np.nanargmax(all_mean), all_mean.shape) if r_sw.any() else None
        per_site[site] = {"heads": heads, "sums": sums, "rules": verdict,
                          "top_head_all": None if top_all is None else {"layer": layers[int(top_all[0])], "head": int(top_all[1]),
                                                                         "mean_move": all_max},
                          "all_heads_sum_move": float(np.nansum(all_mean)) if r_sw.any() else math.nan,
                          "tv_mean_all_heads": {arm: float(a[f"tv_{arm}"].astype(np.float32)[read][r_sw][..., s_i].mean())
                                                if r_sw.any() else math.nan for arm in ("swap", "random")}}  # fmt: skip
    out["sites"] = per_site
    out["label"] = per_site[DECISIVE]["rules"]["label"]
    # the best head, beside
    bl, bh = layers.index(best["layer"]), best["head"]
    sel = read & switched

    def role(mm: np.ndarray) -> np.ndarray:
        """[n, 3 slots, ...] -> [n, 3] by role: slot j, slot k, the third slot."""
        rows = np.arange(len(mm))
        return np.stack([mm[rows, p_j[sel]], mm[rows, p_k[sel]], mm[rows, 3 - p_j[sel] - p_k[sel]]], 1)

    bh_rep: dict[str, Any] = {
        "layer": best["layer"],
        "head": bh,
        "why": D["heads"]["why_best"],
        "layer_minus_L": best["layer"] - m["layer"],
    }
    for arm in ("none", "swap", "random"):
        mm = mass[arm][sel][:, bl, bh, si]  # [n, 3 slots, 3 parts]
        ent = (a["ent_none"][p_item] if arm == "none" else a[f"ent_{arm}"])[sel][:, bl, bh, si]
        lg = (a["logit_none"][p_item] if arm == "none" else a[f"logit_{arm}"])[sel][:, bl, bh, si]
        bh_rep[arm] = {"mass_by_role_j_k_third": role(mm.sum(-1)).mean(0).tolist() if sel.any() else None,
                       "slot_k_parts": dict(zip(PARTS, mm[np.arange(len(mm)), p_k[sel]].mean(0).tolist(), strict=True))
                       if sel.any() else None, "entropy": float(ent.mean()) if sel.any() else math.nan,
                       "logit_by_role_j_k_third": role(lg).mean(0).tolist() if sel.any() else None}  # fmt: skip
    out["best_head"] = bh_rep
    out["necessity"] = necessity_of(D["abl"], items)
    out["weights"] = weights_check(D["src"], best)
    return out


def necessity_of(abl: list[dict], items: list[dict]) -> dict:
    by = {(r["scene"], r["reader"], r["arm"], r["k"], r["zero"]): r for r in abl}
    res: dict[str, Any] = {}
    for zero in ("last", "question"):
        rows, clean = [], {"lookup": [], "recall": []}
        for it in items:
            if it["half"] != "read":
                continue
            s = it["scene"]
            for k in it["ks"]:
                a0, az = by[(s, X.LOOKUP, "swap", k, None)], by[(s, X.LOOKUP, "swap", k, zero)]
                r0, rz = by[(s, X.RECALL, "swap", k, None)], by[(s, X.RECALL, "swap", k, zero)]
                rows.append({"target_swap": int(a0["class"] == "target"), "target_zero": int(az["class"] == "target"),
                             "identity_swap": a0["class"] == "original", "lookup_changed": int(a0["top"] != az["top"]),
                             "recall_changed": int(r0["top"] != rz["top"])})  # fmt: skip
            for w, key in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
                clean[key].append(int(by[(s, w, "none", None, None)]["top"] != by[(s, w, "none", None, zero)]["top"]))
        res[zero] = necessity(rows) | {"clean_lookup_changed": float(np.mean(clean["lookup"])) if clean["lookup"] else math.nan,
                                       "clean_recall_changed": float(np.mean(clean["recall"])) if clean["recall"] else math.nan}  # fmt: skip
    return res


def weights_check(src: Path, best: dict) -> dict:
    """S[k, k'] for the best head from the cached states (mu^q by the picked item's slot j, mu^src per slot), diagonal
    dominance; descriptive. RoPE and the q/k norms left out."""
    st, hw = np.load(src / "states.npz"), np.load(src / "head_weights.npz")
    la = best["layer"]
    j, last, srcs = st["j"], st[f"last_L{la}"], st[f"src_L{la}"]
    mu_q = np.stack([last[j == s].mean(0) if (j == s).any() else np.full(last.shape[1], np.nan) for s in range(3)])
    mu_src = srcs.mean(0)
    s = score_matrix(hw["w_q"], hw["w_k"], mu_q, mu_src)
    return {
        "S": s.tolist(),
        "dominance": dominance(s),
        "items_by_slot": [int((j == x).sum()) for x in range(3)],
        "note": "RoPE and the q/k norms left out; actual logits on slot k's tokens are in best_head",
    }


def fmt(v) -> str:
    return "-" if v is None or (isinstance(v, float) and math.isnan(v)) else (
        f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]" if isinstance(v, list) else f"{v:.3f}")  # fmt: skip


def figure(res: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bh = res["best_head"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.6), constrained_layout=True)
    arms, roles, colors = (
        ("none", "swap", "random"),
        ("slot j (bridge)", "slot k (written)", "third"),
        ("#7a7a7a", "#2a6fdb", "#d98c1f"),
    )
    x = np.arange(len(roles))
    for i, arm in enumerate(arms):
        v = bh[arm]["mass_by_role_j_k_third"] or [0, 0, 0]
        ax1.bar(x + (i - 1) * 0.27, v, 0.27, label=arm, color=colors[i])
    ax1.set_xticks(x, roles)
    ax1.set_ylabel("attention mass (last token)")
    ax1.set_title(f"{res['target']}: best head L{bh['layer']}:h{bh['head']} (switched read pairs)")
    ax1.legend(frameon=False)
    sh = res["lookup_shares"]
    classes = ("target", "original", "third", "other")
    for i, arm in enumerate(arms):
        v = [sh[arm].get(c, 0.0) for c in classes]
        ax2.bar(np.arange(4) + (i - 1) * 0.27, v, 0.27, label=arm, color=colors[i])
    ax2.set_xticks(np.arange(4), ["slot k", "slot j", "third", "other"])
    ax2.set_ylabel("share of lookup answers (read half)")
    ax2.set_ylim(0, 1)
    ax2.set_title("the lookup's answers")
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """49.7's verdict (sealed until Q49.7), or with coverage (batch 52) the same rules on the given runs, no seal guard,
    "no prediction" in place of Dan's answer (x52_attn-<UTC>/)."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else sealed()
    res = [analyse(r, n_boot) for r in runs]
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = RESULTS / f"{'x52_attn' if coverage else 'x49_7'}-{stamp}"
    out.mkdir(parents=True)
    lines = [
        "# 49.7: does the question's attention follow the written address?",
        "",
        f"Batch 49, test 49.7 (jobs/c3/batch49.yaml with amendment 2; "
        f"{'batch 52 coverage, ' if coverage else QUESTION + ', Dan: '}{answer}). x8_write's items, "
        f"the swap s (mu_k - mu_j) at s = {S_WRITE} at the bridge word at L, a random vector of its norm; heads chosen "
        "on the fit half, read on the other; decisive site the last token, question tokens beside; cluster bootstrap "
        f"over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.",
        "",
        "Rules (fixed in advance):",
        "",
    ]
    lines += [f"- {k}: {v}." for k, v in RULES.items()]
    for r in res:
        lines += ["", f"## {r.get('target', r['run'])} ({r['run']})", ""]
        if r["status"] != "tested":
            lines.append(f"{r['status']}: {r['why']}.")
            continue
        d = r["sites"][DECISIVE]
        ru = d["rules"]
        lines += [f"**{ru['label']}**" + (f" (heads {', '.join(ru['follows_heads'])})" if ru["follows_heads"] else "")
                  + f"; distributed: {'yes' if ru['distributed'] else 'no'}"
                  + (f"; {ru['caveat']}" if "caveat" in ru else "") + ".", "",
                  f"L = {r['layer']}; recorded layers {r['recorded_layers']}; skipped ({skipped_kind(r['target'])}) "
                  f"{r['skipped_linear_layers'] or 'none'}. Read pairs {r['read_pairs']}, switched {r['read_switched']}; "
                  f"switch share {fmt(r['switch_share'])} (bar {SWITCH_MIN}). Largest mean move over every recorded head "
                  f"{fmt(ru['max_move_all_heads'])} (L{(d['top_head_all'] or {}).get('layer')}:h{(d['top_head_all'] or {}).get('head')}); "
                  f"summed: five {fmt(d['sums']['five'])}, best layer {fmt(d['sums']['best_layer'])}; all heads "
                  f"{fmt(d['all_heads_sum_move'])}; mean TV from none over every head: swap {fmt(d['tv_mean_all_heads']['swap'])}, "
                  f"random {fmt(d['tv_mean_all_heads']['random'])}.", "",
                  "| site | head | locker mass (fit, none) | move, switched [CI] | random, same pairs | swap, non-switched | follows |",
                  "|---|---|---|---|---|---|---|"]  # fmt: skip
        for site in SITES:
            for h in r["sites"][site]["heads"]:
                st = h["stats"]
                lines.append(f"| {site}{' (decisive)' if site == DECISIVE else ''} | L{h['layer']}:h{h['head']} | "
                             f"{h['mean_mass']:.3f} | {fmt(st['swap_switched'])} | {fmt(st['random_switched'])} | "
                             f"{fmt(st['swap_nonswitched'])} | {'yes' if follows_head(st) else 'no'} |")  # fmt: skip
        bh = r["best_head"]
        lines += ["", f"Best head (fit half): L{bh['layer']}:h{bh['head']} (L + {bh['layer_minus_L']}; {bh['why']}).", "",
                  "| arm | mass j / k / third | slot k: item / number / rest | entropy | logit j / k / third |",
                  "|---|---|---|---|---|"]  # fmt: skip
        for arm in ("none", "swap", "random"):
            b = bh[arm]
            f3 = lambda v: "-" if v is None else " / ".join(f"{x:.3f}" for x in v)  # noqa: E731
            lines.append(f"| {arm} | {f3(b['mass_by_role_j_k_third'])} | {f3(list(b['slot_k_parts'].values()) if b['slot_k_parts'] else None)} | "
                         f"{fmt(b['entropy'])} | {f3(b['logit_by_role_j_k_third'])} |")  # fmt: skip
        lines += ["", "Necessity (read half, the best head zeroed; rule: falls >= 0.5 of the swap value, identity answers "
                  "changed <= 0.10, recall changed <= 0.10):", "",
                  "| zeroed at | n | switch: swap -> zeroed | falls | identity changed (n) | recall changed | clean lookup / recall changed | holds |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for zero, nr in r["necessity"].items():
            if not nr["n"]:
                lines.append(f"| {zero} | 0 | | | | | | no |")
                continue
            lines.append(f"| {zero} | {nr['n']} | {nr['switch_swap']:.3f} -> {nr['switch_zero']:.3f} | {nr['falls']} | "
                         f"{fmt(nr['identity_changed'])} ({nr['identity_n']}) | {nr['recall_changed']:.3f} | "
                         f"{fmt(nr['clean_lookup_changed'])} / {fmt(nr['clean_recall_changed'])} | {'yes' if nr['holds'] else 'no'} |")  # fmt: skip
        wc = r["weights"]
        lines += ["", f"Weights (descriptive; RoPE and q/k norms left out): S = (W_Q mu^q_k)^T (W_K mu^src_k') = "
                  f"{np.round(np.array(wc['S']), 2).tolist()}; diagonal dominance {fmt(wc['dominance'])} (off-diagonal SDs); "
                  f"items by slot {wc['items_by_slot']}."]  # fmt: skip
        figure(r, out / f"best_head_{r['target']}.png")
        lines += ["", f"![best head](best_head_{r['target']}.png)"]
    (out / "verdict.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "results": res}, indent=1, default=str) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "examples.md").write_text("\n".join(view_lines(runs)) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """10 random items per run (seed 0): the lookup's prompt as read (bridge, locker sentences, read token marked), each
    arm's answers (lookup class and decoded top, recall top), the best head's masses j / k / third per arm."""
    from scripts import x45m

    lines = ["# 49.7 view (verify pack): the lookup's prompt exactly as the model reads it. UNVERIFIED.", ""]
    for run in runs:
        src = RESULTS / run
        if not (src / "status.json").exists() or json.loads((src / "status.json").read_text())["status"] != "tested":
            continue
        D = load(run)
        target = D["m"]["model"]["target"]
        tok = x45m.tokenizer() if target == pins.TARGET else None  # decoding needs BJ_TARGET = the run's model
        items, rows, a, best = D["items"], D["rows"], D["a"], D["heads"]["best"]
        layers = [int(x) for x in a["layers"]]
        li, nh = layers.index(best["layer"]), int(D["m"]["n_heads"])
        dec = (lambda t, tok=tok: tok.decode([t])) if tok is not None else str
        by = {(r["scene"], r["reader"], r["arm"], r["k"]): r for r in rows}
        mn = a["mass_none"].astype(np.float32).reshape(len(items), len(layers), nh, len(SITES), 3, len(PARTS)).sum(-1)
        ms = {arm: a[f"mass_{arm}"].astype(np.float32).reshape(-1, len(layers), nh, len(SITES), 3, len(PARTS)).sum(-1)
              for arm in ("swap", "random")}  # fmt: skip
        lines += [f"## {run} ({target}): {min(k, len(items))} random items of {len(items)} (seed {seed}); best head "
                  f"L{best['layer']}:h{best['head']}", ""]  # fmt: skip
        for i in sorted(random.Random(seed).sample(range(len(items)), min(k, len(items)))):
            it = items[i]
            lines += [f"### {it['scene']} ({it['half']}): bridge {it['entity']}, j = {it['j']}, lockers {it['slots']}", "",
                      "```", marked(tok, it) if tok is not None else "(tokenizer of another target)", "```", "",
                      "| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |", "|---|---|---|---|---|"]  # fmt: skip
            m0 = mn[i, li, best["head"], 0]
            lines.append(f"| none | - | {by[(it['scene'], X.LOOKUP, 'none', None)]['class']} ({dec(by[(it['scene'], X.LOOKUP, 'none', None)]['top'])!r}) | "
                         f"{dec(by[(it['scene'], X.RECALL, 'none', None)]['top'])!r} | {' / '.join(f'{x:.3f}' for x in m0)} |")  # fmt: skip
            for kk in it["ks"]:
                pi = 2 * i + it["ks"].index(kk)
                for arm in ("swap", "random"):
                    lr, rr = by[(it["scene"], X.LOOKUP, arm, kk)], by[(it["scene"], X.RECALL, arm, kk)]
                    lines.append(f"| {arm} | {kk} | {lr['class']} ({dec(lr['top'])!r}) | {dec(rr['top'])!r} | "
                                 f"{' / '.join(f'{x:.3f}' for x in ms[arm][pi, li, best['head'], 0])} |")  # fmt: skip
            lines.append("")
    return lines


def stage_view(runs: list[str]) -> Path:
    sealed()
    out = RESULTS / f"x49_7-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "view.md").write_text("\n".join(view_lines(runs)) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x49_attn/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the runs")
    ap.add_argument("--why", default="batch 49, test 49.7 (jobs/c3/batch49.yaml; Q49.7)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "view":
        stage_view(a.runs)
    else:
        stage_verdict(a.runs, a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
