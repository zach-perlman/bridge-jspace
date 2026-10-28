"""x51_heads (batch 51, test 51.2; jobs/c3/batch51.yaml, design and rules fixed in advance; Q51.2 in
predictions/2026-10-28_dan.md): joint head ablation under the address swap.

Extends 49.7 (scripts/x49_attn.py; its functions imported, none changed). Items: 49.7's (x8_write.eligible, the routes
test's C2 scenes, locker-first, the first 300; the run asserts they are 49.7's run's items, in order, with the same
halves). Swap: h + 2 (mu_k - mu_j) at the bridge word at L (x0_massmean.pointer_means, as 49.7), k each other slot.
Attention layers only: the heads are those 49.7 recorded (every softmax-attention layer > L); the Gated DeltaNet layers
(9B, 27B) are skipped and logged.

Ranking (CPU, no new forward; 49.7 is not rerun): every recorded head by its mean attention move at the last token on
the fit half's switched swap pairs, from 49.7's stored attention.npz and outcomes (x49_attn.moves; move = (mass on slot
k's sentence - mass on slot j's) under the swap minus the same under none; switched = the lookup answered slot k's
locker under the swap in 49.7's forward). Ties: the lower layer, then the lower head. No fit pair switched: every fit
swap pair (recorded).

Sets: top k by that ranking, k in {1, 3, 5, 10} (across layers; the top 10 across layers is the k = 10 set); every head
of the best layer (the layer of the rank-1 head, 49.7's best-layer convention). Controls: per top-k set, N_DRAWS random
sets with the same number of heads in each of the same layers (the set's own heads excluded); for the best-layer set
(no other head is left in that layer), N_DRAWS random sets of its size from the other recorded layers. random.Random(
HEAD_SEED), drawn in a fixed order.

Mean ablation: a head's slice of o_proj's input (its attention output after the gate, head_dim wide) is replaced, at
the site's positions, by its mean over the fit half's unedited prompts of the same reader at the same position: the
last token (the appended read token); the question tokens by index within the question (each reader's question has a
fixed token count, asserted). Means from one unedited forward per fit item and reader. Each ablation is read on the
read half under none and both swaps (one batched read of 3 rows), both readers, at each site (last token; question
tokens) as separate arms; a baseline (no ablation) read beside. Each reader is ablated at its own positions.

Rules (verdict stage; read half; decisive site the last token as in 49.7, the question tokens beside under the same
rules; cluster bootstrap over bridge entities, 10,000, seed 0; EPS 1e-9 at the bars): see RULES. CPU beside: per read
pair, the summed attention move (49.7's stored, last token; every recorded head, the top 10 beside) vs switched (49.7's
lookup class), a logistic fit and the AUC. SEALED: the run writes no verdict; verdict and view refuse until
predictions/2026-10-28_dan.md holds Dan's Q51.2 answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x51_heads.py plan                              # CPU: counts, sets, 5 prompts
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_heads.py run --name qwen35_9b_x51_2        # GPU (sealed)
uv run python scripts/x51_heads.py verdict --runs qwen35_9b_x51_2 muse30_x51_2 x51_2_27b   # CPU, after Dan's Q51.2
BJ_TARGET=<model> uv run python scripts/x51_heads.py view --runs <that model's run>
"""

from __future__ import annotations

import argparse
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
from bridge_jspace.knockout import decoder_layers
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x48_heads as H
from scripts import x49_attn as A

EXP = "x51_heads"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.2"
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_2", "muse-glimmer-30b": "muse30_x51_2_r2", "qwen3.6-27b": "x51_2_27b"}
SOURCE = A.RUNS  # target -> the 49.7 run whose items, halves and attention this test uses
S_WRITE = A.S_WRITE
SITES = A.SITES
DECISIVE = A.DECISIVE
RANK_SITE = "last"
KS = (1, 3, 5, 10)
N_DRAWS = 5
HEAD_SEED = 512
SMALL_CUT, IDENT_MAX, RECALL_MAX, RANDOM_CUT_MAX, DIST_CUT = A.NEC_FALL, A.NEC_IDENTITY, A.NEC_RECALL, 0.15, 0.30
EPS = A.EPS
RULES = {
    "cut": "cut = (switch - switch under the ablation) / switch, switch = the read-half swap pairs' share answering slot "
    "k's locker (the lookup's switch to the swapped-in slot), both read in this run (baseline and ablated)",
    "small_set": "some top-k set, k in {1, 3, 5, 10}, cuts >= 0.5 while the identity answers (read pairs answering slot "
    "j's locker under the swap) change <= 0.10 and the recall's answer changes <= 0.10 (swap + ablation vs swap), and "
    "the matched random sets of k heads (same layers) cut <= 0.15 (mean over the draws)",
    "distributed": "every head of the best layer together cuts < 0.3",
    "label": "'small set' if small_set holds, else 'distributed' if distributed holds, else 'neither'; both flags shown",
}


# ---- pure (CPU) ---------------------------------------------------------------------------------------------------


def fit_moves(a: dict, items: list[dict], rows: list[dict], site: str = RANK_SITE) -> tuple[np.ndarray, str]:
    """49.7's stored swap moves [P, L, H] at `site` on the fit half's switched pairs (none switched: every fit pair)."""
    layers = [int(x) for x in a["layers"]]
    p_item, p_k = np.asarray(a["pair_item"]).astype(int), np.asarray(a["pair_k"]).astype(int)
    n_items, nl = len(items), len(layers)
    n_heads = a["mass_none"].shape[2]
    p_j = np.array([items[i]["j"] for i in p_item])
    si = SITES.index(site)
    shape = (nl, n_heads, len(SITES), 3, len(A.PARTS))
    none = a["mass_none"].astype(np.float32).reshape(n_items, *shape)[p_item][:, :, :, si]
    swap = a["mass_swap"].astype(np.float32).reshape(len(p_item), *shape)[:, :, :, si]
    mv = A.moves(A.slot_mass(swap), A.slot_mass(none), p_j, p_k)
    lk = {(r["scene"], r["k"]): r["class"] for r in rows if r["reader"] == X.LOOKUP and r["arm"] == "swap"}
    fit = np.array([items[i]["half"] == "fit" for i in p_item])
    switched = np.array([lk[(items[i]["scene"], int(k))] == "target" for i, k in zip(p_item, p_k, strict=True)])
    if (fit & switched).any():
        return mv[fit & switched], f"the fit half's switched swap pairs ({int((fit & switched).sum())})"
    return mv[fit], f"no fit pair switched: every fit swap pair ({int(fit.sum())})"


def rank_heads(mv: np.ndarray, layers: list[int]) -> list[dict]:
    """Every (layer, head) by its mean move over the rows of mv [P, L, H], largest first; ties: lower layer, then head."""
    mean = mv.mean(0)
    out = [
        {"layer": la, "head": h, "move": float(mean[li, h])} for li, la in enumerate(layers) for h in range(mv.shape[2])
    ]
    return sorted(out, key=lambda r: (-r["move"], r["layer"], r["head"]))


def by_layer(heads: list[tuple[int, int]]) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    for la, h in heads:
        out.setdefault(la, []).append(h)
    return {la: sorted(hs) for la, hs in sorted(out.items())}


def random_matched(heads: list[tuple[int, int]], n_heads: int, rng: random.Random) -> list[tuple[int, int]]:
    """As many heads in each layer as `heads` has there, drawn from that layer's other heads."""
    out = []
    for la, hs in by_layer(heads).items():
        pool = [h for h in range(n_heads) if h not in hs]
        assert len(pool) >= len(hs), f"L{la}: {len(hs)} heads in the set leave {len(pool)} to draw from"
        out += [(la, h) for h in sorted(rng.sample(pool, len(hs)))]
    return out


def random_other_layers(
    size: int, layer: int, layers: list[int], n_heads: int, rng: random.Random
) -> list[tuple[int, int]]:
    """`size` heads drawn from the recorded layers other than `layer`."""
    pool = [(la, h) for la in layers if la != layer for h in range(n_heads)]
    assert len(pool) >= size, f"{size} heads wanted, {len(pool)} in the other layers"
    return sorted(rng.sample(pool, size))


def head_sets(ranking: list[dict], layers: list[int], n_heads: int, ks=KS, n_draws: int = N_DRAWS,
              seed: int = HEAD_SEED) -> dict[str, dict]:  # fmt: skip
    """The ablated sets, in run order: top{k}, best_layer, then per base set its random draws ('<base>_r<d>')."""
    sets: dict[str, dict] = {}
    for k in ks:
        sets[f"top{k}"] = {"kind": "top", "k": k, "heads": [(r["layer"], r["head"]) for r in ranking[:k]]}
    best = ranking[0]["layer"]
    sets["best_layer"] = {"kind": "layer", "k": n_heads, "layer": best, "heads": [(best, h) for h in range(n_heads)]}
    rng = random.Random(seed)
    for base in list(sets):
        for d in range(n_draws):
            if sets[base]["kind"] == "top":
                heads = random_matched(sets[base]["heads"], n_heads, rng)
            else:
                heads = random_other_layers(n_heads, best, layers, n_heads, rng)
            sets[f"{base}_r{d}"] = {"kind": "random", "of": base, "draw": d, "k": len(heads), "heads": heads}
    return sets


def cut_of(s_swap: float, s_abl: float) -> float:
    return (s_swap - s_abl) / s_swap if s_swap > 0 else math.nan


def ablation_cell(by: dict, items: list[dict], name: str, site: str, n_boot: int) -> dict:
    """One (set, site) on the read half: x49_attn.necessity's numbers (switch, ablated switch, fall share = the cut,
    identity answers changed, the recall changed) with the cut's paired cluster-bootstrap interval, the clean answers
    lost (none + ablation vs none)."""
    rows, ents, clean = [], [], {"lookup": [], "recall": []}
    for it in items:
        if it["half"] != "read":
            continue
        s = it["scene"]
        for k in it["ks"]:
            a0, az = by[(s, X.LOOKUP, "swap", k, None, None)], by[(s, X.LOOKUP, "swap", k, name, site)]
            r0, rz = by[(s, X.RECALL, "swap", k, None, None)], by[(s, X.RECALL, "swap", k, name, site)]
            rows.append({"target_swap": int(a0["class"] == "target"), "target_zero": int(az["class"] == "target"),
                         "identity_swap": a0["class"] == "original", "lookup_changed": int(a0["top"] != az["top"]),
                         "recall_changed": int(r0["top"] != rz["top"])})  # fmt: skip
            ents.append(it["entity"])
        for w, key in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
            clean[key].append(
                int(by[(s, w, "none", None, None, None)]["top"] != by[(s, w, "none", None, name, site)]["top"])
            )
    out = A.necessity(rows)
    if rows:
        rr = X.resampled_rates({"swap": [r["target_swap"] for r in rows], "abl": [r["target_zero"] for r in rows]},
                               ents, n_boot)  # fmt: skip
        out["cut"] = [cut_of(out["switch_swap"], out["switch_zero"]), *X.interval(X.dependence(rr["swap"], rr["abl"]))]
    else:
        out["cut"] = [math.nan, math.nan, math.nan]
    out["clean_lookup_changed"] = float(np.mean(clean["lookup"])) if clean["lookup"] else math.nan
    out["clean_recall_changed"] = float(np.mean(clean["recall"])) if clean["recall"] else math.nan
    return out


def random_summary(cells: list[dict]) -> dict:
    """The draws of one base set: the cut's mean, SD (ddof 0), min and max; identity / recall changed means."""
    cuts = np.array([c["cut"][0] for c in cells], dtype=float)
    mean = lambda key: float(np.nanmean([c[key] for c in cells])) if cells else math.nan  # noqa: E731
    return {"draws": len(cells), "cut_mean": float(np.nanmean(cuts)) if cells else math.nan,
            "cut_sd": float(np.nanstd(cuts)) if cells else math.nan,
            "cut_min": float(np.nanmin(cuts)) if cells else math.nan, "cut_max": float(np.nanmax(cuts)) if cells else math.nan,
            "identity_changed": mean("identity_changed"), "recall_changed": mean("recall_changed"),
            "cuts": cuts.tolist()}  # fmt: skip


def rules(top: dict[int, dict], rand: dict[int, dict], layer_cell: dict) -> dict:
    """The fixed rules at one site: top[k] = ablation_cell of the top-k set, rand[k] = random_summary of its draws,
    layer_cell = the best layer's ablation_cell."""
    small = [k for k in sorted(top) if top[k]["holds"] and not rand[k]["cut_mean"] > RANDOM_CUT_MAX + EPS]
    lc = layer_cell["cut"][0]
    distributed = bool(not math.isnan(lc) and lc < DIST_CUT - EPS)
    label = "small set" if small else "distributed" if distributed else "neither"
    return {
        "label": label,
        "small_set": bool(small),
        "small_ks": small,
        "distributed": distributed,
        "best_layer_cut": lc,
    }


def fit_logistic(x: np.ndarray, y: np.ndarray) -> dict:
    """P(y = 1) = sigmoid(a + b z), z = (x - mean) / SD; maximum likelihood (scipy BFGS). Also b per unit of x."""
    from scipy.optimize import minimize

    x, y = np.asarray(x, float), np.asarray(y, float)
    sd = float(x.std())
    if len(x) < 2 or sd == 0.0 or y.min() == y.max():
        return {"a": math.nan, "b_std": math.nan, "b_per_unit": math.nan, "converged": False, "n": len(x)}
    z = (x - x.mean()) / sd

    def nll(p):
        t = p[0] + p[1] * z
        return float(np.sum(np.logaddexp(0.0, t) - y * t))

    res = minimize(nll, np.zeros(2), method="BFGS")
    return {"a": float(res.x[0]), "b_std": float(res.x[1]), "b_per_unit": float(res.x[1] / sd), "converged": bool(res.success),
            "n": len(x), "x_mean": float(x.mean()), "x_sd": sd}  # fmt: skip


def auc_ci(
    x: np.ndarray, y: np.ndarray, ents: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED
) -> list[float]:
    """[AUC, lo, hi]: P(a switched pair's x > a non-switched pair's), ties 1/2 (x47_margins.auc), and its 95% cluster-
    bootstrap interval over the entities."""
    from scripts import x47_margins as MG

    x, y = np.asarray(x, float), np.asarray(y).astype(bool)
    est = MG.auc(x[y], x[~y])
    keys = sorted(set(ents))
    idx = {e: np.flatnonzero(np.array(ents) == e) for e in keys}
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        take = np.concatenate([idx[keys[i]] for i in rng.integers(0, len(keys), len(keys))])
        boots.append(MG.auc(x[take][y[take]], x[take][~y[take]]))
    return [est, *X.interval(np.array(boots))]


def summed_moves(a: dict, items: list[dict], heads: list[tuple[int, int]] | None, site: str = RANK_SITE) -> np.ndarray:
    """Per 49.7 pair [P]: the swap's move at `site` summed over `heads` (None: every recorded head)."""
    layers = [int(x) for x in a["layers"]]
    p_item, p_k = np.asarray(a["pair_item"]).astype(int), np.asarray(a["pair_k"]).astype(int)
    n_heads = a["mass_none"].shape[2]
    p_j = np.array([items[i]["j"] for i in p_item])
    si = SITES.index(site)
    shape = (len(layers), n_heads, len(SITES), 3, len(A.PARTS))
    none = a["mass_none"].astype(np.float32).reshape(len(items), *shape)[p_item][:, :, :, si]
    swap = a["mass_swap"].astype(np.float32).reshape(len(p_item), *shape)[:, :, :, si]
    mv = A.moves(A.slot_mass(swap), A.slot_mass(none), p_j, p_k)  # [P, L, H]
    if heads is None:
        return mv.sum((1, 2))
    return np.sum([mv[:, layers.index(la), h] for la, h in heads], 0)


def parse_answer(text: str) -> str:
    """Dan's Q51.2 answer (x47_chain.dan_answer's regex: per-model 'Dan (...):' lines and bullets), '' if none."""
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


def reader_sites(tok, context: str, question: str, ids: list[int], space: list[int]) -> dict[str, list[int]]:
    """One reader's ablation positions in its prompt as read (ids + X0's one-token read suffix): last = the read
    token; question = the question text's tokens (character overlap), checked against the stored ids."""
    from bridge_jspace.tokens import raw_encoding

    assert len(space) == 1, f"the read suffix is {len(space)} tokens, not 1"
    text = A.rendered(tok, context, question)
    enc = raw_encoding(tok, text, offsets=True)
    assert enc["input_ids"] == ids, "the rendered prompt's ids differ from the stored ones"
    q = A.question_positions(enc["offset_mapping"], text, context, question)
    return {"last": [len(ids)], "question": q}


def with_sites(tok, it: dict) -> dict:
    """An x49_attn.item_record with each reader's sites; the lookup's agree with 49.7's layout."""
    sites = {w: reader_sites(tok, it["context"], it["readers"][w]["question"], it["readers"][w]["ids"], it["space"])
             for w in X.READERS}  # fmt: skip
    lo = it["layout"]
    assert sites[X.LOOKUP] == {"last": [lo["last"]], "question": lo["question"]}, f"{it['scene']}: lookup sites differ"
    return {**it, "sites": sites}


def source_run(target: str) -> dict:
    src = A.RESULTS / SOURCE[target]
    a = np.load(src / "attention.npz")
    return {"src": src, "m": json.loads((src / "manifest.json").read_text()), "items": X.read_jsonl(src / "cases.jsonl"),
            "rows": X.read_jsonl(src / "outcomes.jsonl"), "a": {k: a[k] for k in a.files}}  # fmt: skip


def design(target: str) -> dict:
    """The ranking and the sets from 49.7's stored run (CPU)."""
    S = source_run(target)
    layers = [int(x) for x in S["a"]["layers"]]
    n_heads = int(S["m"]["n_heads"])
    mv, basis = fit_moves(S["a"], S["items"], S["rows"])
    ranking = rank_heads(mv, layers)
    sets = head_sets(ranking, layers, n_heads)
    return {"S": S, "layers": layers, "n_heads": n_heads, "ranking": ranking, "basis": basis, "sets": sets}


def q_lengths(items: list[dict]) -> dict[str, list[int]]:
    return {w: sorted({len(it["sites"][w]["question"]) for it in items}) for w in X.READERS}


def forwards(n_fit: int, n_read: int, n_sets: int) -> dict:
    return {"means_single_forwards": 2 * n_fit, "baseline_batched_reads": 2 * n_read,
            "ablation_batched_reads": n_sets * len(SITES) * 2 * n_read, "rows_per_batched_read": 3,
            "competence_reads": "x8_write.eligible over the routes generator's C2 scenes (as x8 and 49.7)"}  # fmt: skip


def stage_plan() -> Path:
    """CPU (tokenizer, 49.7's stored run): items and halves, each reader's sites, the ranking and the sets, counts, 5
    rendered prompts (seed 0)."""
    from scripts import x45m

    target = pins.TARGET
    assert target in RUNS, f"51.2 runs on {sorted(RUNS)}, not {target}"
    tok = x45m.tokenizer()
    D = design(target)
    S = D["S"]
    items = [with_sites(tok, it) for it in S["items"]]
    ql = q_lengths(items)
    assert all(len(v) == 1 for v in ql.values()), f"question token counts vary: {ql}"
    n_read = sum(it["half"] == "read" for it in items)
    sw49 = {
        (r["scene"], r["k"]): r["class"] == "target"
        for r in S["rows"]
        if r["reader"] == X.LOOKUP and r["arm"] == "swap"
    }
    half = {it["scene"]: it["half"] for it in items}
    sets = D["sets"]
    counts = {"target": target, "layer": S["m"]["layer"], "source_run": SOURCE[target], "items": len(items),
              "entities": len({it["entity"] for it in items}), "fit_items": len(items) - n_read, "read_items": n_read,
              "fit_entities": len({it["entity"] for it in items if it["half"] == "fit"}),
              "read_entities": len({it["entity"] for it in items if it["half"] == "read"}), "read_pairs": 2 * n_read,
              "x49_7_switched_pairs": {h: sum(v for (s, _), v in sw49.items() if half[s] == h) for h in ("fit", "read")},
              "recorded_layers": D["layers"], "skipped_linear_layers": S["m"]["skipped_linear_layers"],
              "n_heads": D["n_heads"], "recorded_heads": len(D["layers"]) * D["n_heads"], "head_dim": S["m"]["head_dim"],
              "question_tokens": ql, "ranking_basis": D["basis"], "ranking_top10": D["ranking"][:10],
              "best_layer": sets["best_layer"]["layer"],
              "sets": {k: {"kind": v["kind"], "n": len(v["heads"]), "by_layer": by_layer(v["heads"])} for k, v in sets.items()},
              "arms": {"sets": len(sets), "sites": list(SITES), "per_set_site": "none + both swaps, both readers"},
              "forwards": forwards(len(items) - n_read, n_read, len(sets))}  # fmt: skip
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = RESULTS / f"plan-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    (out / f"plan_{target}.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False, default=str) + "\n")
    picks = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(items)), 5))
    lines = [f"# 51.2 plan, {target}: 5 random items (seed {X.EXAMPLES_SEED}) of {len(items)}", "",
             "The lookup's O prompt exactly as the model reads it (x49_attn.marked: ⟦bridge:…⟧ the swap position, "
             "⟦slotS (j|k):…⟧ the locker sentences, ⟦read:…⟧ the last token). Ablation positions per reader: last = the read "
             "token; question = the question text's tokens. UNVERIFIED.", ""]  # fmt: skip
    for i in picks:
        it = items[i]
        lines += [f"## {it['scene']} ({it['half']} half): bridge {it['entity']}, j = {it['j']}, k in {it['ks']}; lockers "
                  f"{it['slots']}", "", "```", A.marked(tok, it), "```", ""]  # fmt: skip
        for w in X.READERS:
            ids = it["readers"][w]["ids"] + it["space"]
            st = it["sites"][w]
            lines.append(f"- {w}: question tokens {st['question']} ({tok.decode([ids[p] for p in st['question']])!r}); "
                         f"last {st['last']} ({tok.decode([ids[p] for p in st['last']])!r})")  # fmt: skip
        lines.append("")
    (out / f"prompts_{target}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts, indent=2, ensure_ascii=False, default=str))
    print("wrote", out)
    return out


# ---- mean capture and mean ablation --------------------------------------------------------------------------------


@contextlib.contextmanager
def capture_o_inputs(model, layers: list[int], positions: list[int], out: dict[int, Any]):
    """While active, a forward of one prompt [1, T] fills out[layer] = o_proj's input at `positions` [P, heads *
    head_dim], fp32 (every head's attention output after the gate, the slices zero_head / mean_heads act on)."""
    blocks: Any = decoder_layers(model)
    pos = list(positions)

    def hook_for(la: int):
        def hook(_module, args):
            x = args[0]
            assert x.shape[0] == 1, f"one prompt at a time, got a batch of {x.shape[0]}"
            out[la] = x[0, pos].float().clone()

        return hook

    handles = [blocks[la].self_attn.o_proj.register_forward_pre_hook(hook_for(la)) for la in layers]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


@contextlib.contextmanager
def mean_heads(model, heads: dict[int, list[int]], positions: list[int], means: dict[int, Any]):
    """While active, each listed head's slice of o_proj's input at `positions` is replaced by means[layer][p, slice]
    (means[layer]: [len(positions), heads * head_dim]), in every row of the batch; other heads and positions untouched."""
    import torch

    blocks: Any = decoder_layers(model)
    pos = list(positions)

    def hook_for(la: int, hs: list[int]):
        hd = blocks[la].self_attn.head_dim
        cols = torch.tensor([c for h in hs for c in range(h * hd, (h + 1) * hd)])
        value = means[la][:, cols.to(means[la].device)]

        def hook(_module, args):
            if not pos or args[0].shape[1] <= max(pos):  # a cached decoding step: the prompt positions are not in it
                return None
            x = args[0].clone()
            p = torch.tensor(pos, device=x.device)
            c = cols.to(x.device)
            x[:, p[:, None], c[None, :]] = value.to(x.device, x.dtype)[None]
            return (x, *args[1:])

        return hook

    handles = [blocks[la].self_attn.o_proj.register_forward_pre_hook(hook_for(la, hs)) for la, hs in heads.items()]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


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
    assert chat.FORMAT == "chat", "51.2 reads chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"51.2 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    D = design(target)  # CPU: 49.7's stored attention, fit half only
    S, sets = D["S"], D["sets"]
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "test": "51.2", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "spec": "jobs/c3/batch51.yaml (51.2)",
        "question": f"{QUESTION} ({PREDICTIONS})", "layer": layer, "s": S_WRITE, "mu_from": R.STATES[target],
        "source_run": f"results/x49_attn/{SOURCE[target]}",
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in
                   (SPEC, *(S["src"] / f for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "attention.npz")),
                    pins.RESULTS_DIR / "x0_probe" / R.STATES[target] / "states.npz") if p.exists()},
        "items_rule": "x8_write.eligible (the routes test's C2 scenes, O, gate 0.80 per reader, the first 300); asserted "
                      "to be 49.7's run's items in order, with its halves",
        "swap": f"h + {S_WRITE} (mu_k - mu_j) at the bridge word at L, k each other slot (49.7's)",
        "ranking": f"every recorded head by its mean attention move at the {RANK_SITE} token on {D['basis']} (49.7's "
                   "stored attention.npz; ties lower layer, then head)",
        "ranking_top10": D["ranking"][:10], "best_layer": sets["best_layer"]["layer"],
        "sets": {k: {kk: vv for kk, vv in v.items() if kk != "heads"} | {"heads": [list(x) for x in v["heads"]]}
                 for k, v in sets.items()},
        "random_sets": f"per top-k set {N_DRAWS} draws with the same number of heads in each of its layers (its own heads "
                       f"excluded); per best-layer set {N_DRAWS} draws of its size from the other recorded layers; "
                       f"random.Random({HEAD_SEED}), drawn in the order of 'sets'",
        "mean_ablation": "a head's slice of o_proj's input replaced at the site's positions by its mean over the fit half's "
                         "unedited prompts of the same reader at the same position: last = the read token; question = "
                         "each question-token index (fixed count per reader, asserted); every row of the batch",
        "sites": {"last": "the read token (X0's appended space token)", "question": "the question text's tokens"},
        "reads": "read half; per (set, site): none and both swaps in one batched X0 chat read, both readers, each reader "
                 "ablated at its own positions; a baseline read (no ablation) beside",
        "rules": RULES, "decisive_site": DECISIVE,
        "seeds": {"scenes": R.SEED, "split": A.SPLIT_SEED, "heads": HEAD_SEED, "bootstrap": X.BOOT_SEED,
                  "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
        "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    manifest = out / "manifest.json"
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", manifest, flush=True)

    model = load_model()
    tok = model.tokenizer
    cfg = model.hf.config.get_text_config()
    full, skipped = A.recorded_layers(layer_kinds(model), layer)
    assert full == D["layers"], f"recorded layers {full} differ from 49.7's {D['layers']}"
    assert cfg.num_attention_heads == D["n_heads"], "head count differs from 49.7's"
    print(f"heads at layers {full}; skipped (Gated DeltaNet) {skipped}", flush=True)
    m.update(
        recorded_layers=full, skipped_linear_layers=skipped, n_heads=cfg.num_attention_heads, head_dim=cfg.head_dim
    )
    chosen, gate, ws, _ = W.eligible(model, X.GATE, W.N_ITEMS)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not chosen:
        (out / "status.json").write_text(json.dumps({"status": "not tested", "gate": gate}, indent=2) + "\n")
        manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print("the gate missed: not tested", gate, flush=True)
        return out
    src_items = S["items"]
    # 49.7's items, in its order and with its halves (the ranking read from its stored run depends on them): those the
    # gate still makes eligible here. A borderline competence read can flip on another box's GPU (x51_2_muse on the
    # helper, 28 Oct: the eligible list was not 49.7's), so the overlap is kept and the drops recorded, not asserted.
    by_scene = {c["scene"]: c for c in chosen}
    half = {it["scene"]: it["half"] for it in src_items}
    kept = [by_scene[it["scene"]] for it in src_items if it["scene"] in by_scene]
    overlap = {"x49_7_items": len(src_items), "eligible_here": len(chosen), "kept": len(kept),
               "dropped": [it["scene"] for it in src_items if it["scene"] not in by_scene],
               "new_not_used": [c["scene"] for c in chosen if c["scene"] not in half]}  # fmt: skip
    print("items vs 49.7:", json.dumps({k: (v if isinstance(v, int) else len(v)) for k, v in overlap.items()}), flush=True)
    assert len(kept) >= 0.9 * len(src_items), f"fewer than 90% of 49.7's items stay eligible: {overlap}"
    items = [with_sites(tok, A.item_record(tok, c, half[c["scene"]])) for c in kept]
    ql = q_lengths(items)
    assert all(len(v) == 1 for v in ql.values()), f"question token counts vary: {ql}"
    X.write_jsonl(out / "cases.jsonl", items)
    m["same_items_as_x49_7"] = not overlap["dropped"] and not overlap["new_not_used"]
    m["items_vs_x49_7"] = overlap
    m["question_tokens"] = ql
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

    dev = model.device
    hdim = cfg.num_attention_heads * cfg.head_dim
    fit_items = [it for it in items if it["half"] == "fit"]
    read_items = [it for it in items if it["half"] == "read"]
    with torch.no_grad():
        # means over the fit half's unedited prompts, per reader and site, every recorded layer
        sums = {(w, s): {la: torch.zeros(len(fit_items[0]["sites"][w][s]), hdim, device=dev) for la in full}
                for w in X.READERS for s in SITES}  # fmt: skip
        for it in progress(fit_items, "51.2 means (fit item)"):
            for w in X.READERS:
                ids = it["readers"][w]["ids"] + it["space"]
                pos = [p for s in SITES for p in it["sites"][w][s]]
                got: dict[int, Any] = {}
                with capture_o_inputs(model, full, pos, got):
                    model.run(torch.tensor([ids], device=dev))
                n_last = len(it["sites"][w]["last"])
                for la in full:
                    sums[(w, "last")][la] += got[la][:n_last].to(dev)
                    sums[(w, "question")][la] += got[la][n_last:].to(dev)
        means = {key: {la: v / len(fit_items) for la, v in per.items()} for key, per in sums.items()}
        arrays: dict[str, Any] = {f"{w}_{s}_L{la}": means[(w, s)][la].cpu().numpy() for w, s in means for la in full}
        np.savez_compressed(out / "means.npz", layers=np.array(full), **arrays)
        del sums

        mu = {
            k: torch.tensor(v, dtype=torch.float32, device=dev) for k, v in MM.pointer_means(R.STATES[target]).items()
        }
        rows = []
        for it in progress(read_items, "51.2 ablation (read item)"):
            j, toks = it["j"], dict(enumerate(it["digit_tokens"]))
            arms: list[tuple[str, int | None]] = [("none", None)]
            arms += [("swap", k) for k in it["ks"]]
            edits = [{}] + [{layer: AddRows((S_WRITE * (mu[k] - mu[j]))[None], [it["pos"]])} for k in it["ks"]]

            def read(w: str, name: str | None, site: str | None, it=it, toks=toks, j=j, arms=arms, edits=edits):
                rd = it["readers"][w]
                if name is None:
                    ctx = contextlib.nullcontext()
                else:
                    assert site is not None, "an ablation needs a site"
                    pos = it["sites"][w][site]
                    ctx = mean_heads(model, by_layer(sets[name]["heads"]), pos, means[(w, site)])
                with ctx:
                    logits, _ = X.read_logits(model, rd["ids"], edits, "chat", it["space"], ws)
                for (kind, k), lg in zip(arms, logits, strict=True):
                    top = int(lg.argmax())
                    row = {"scene": it["scene"], "entity": it["entity"], "reader": w, "arm": kind, "k": k, "set": name,
                           "site": site, "top": top}  # fmt: skip
                    if w == X.LOOKUP:
                        row["class"] = W.classify(top, toks, j, k if k is not None else (j + 1) % 3)
                        if k is None:
                            row["class"] = row["class"].replace("target", "third")
                    rows.append(row)

            for w in X.READERS:
                read(w, None, None)
            for name in sets:
                for site in SITES:
                    for w in X.READERS:
                        read(w, name, site)
        X.write_jsonl(out / "ablation.jsonl", rows)
    m["items"], m["fit_items"], m["read_items"] = len(items), len(fit_items), len(read_items)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    (out / "status.json").write_text(json.dumps({"status": "tested"}, indent=2) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def analyse(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One run: pending / not tested / the rules per site, the random draws, the CPU-beside fit."""
    src = RESULTS / run
    if not (src / "status.json").exists():
        return {"run": run, "status": "pending", "why": "no status.json (not run or not finished)"}
    status = json.loads((src / "status.json").read_text())
    if status["status"] != "tested":
        return {"run": run, "status": status["status"], "why": f"read gate: {status.get('gate')}"}
    m = json.loads((src / "manifest.json").read_text())
    items = X.read_jsonl(src / "cases.jsonl")
    by = {
        (r["scene"], r["reader"], r["arm"], r["k"], r["set"], r["site"]): r
        for r in X.read_jsonl(src / "ablation.jsonl")
    }
    sets = m["sets"]
    out: dict[str, Any] = {"run": run, "status": "tested", "target": m["model"]["target"], "layer": m["layer"],
                           "recorded_layers": m["recorded_layers"], "skipped_linear_layers": m["skipped_linear_layers"],
                           "items": len(items), "read_items": sum(it["half"] == "read" for it in items),
                           "ranking_top10": m["ranking_top10"], "best_layer": m["best_layer"], "sets": sets}  # fmt: skip
    per_site = {}
    for site in SITES:
        cells = {name: ablation_cell(by, items, name, site, n_boot) for name in sets}
        tops = {sets[n]["k"]: cells[n] for n in sets if sets[n]["kind"] == "top"}
        rand = {}
        for base in [n for n in sets if sets[n]["kind"] != "random"]:
            rand[base] = random_summary([cells[n] for n in sets if sets[n].get("of") == base])
        verdict = rules(tops, {sets[b]["k"]: rand[b] for b in rand if sets[b]["kind"] == "top"}, cells["best_layer"])
        per_site[site] = {"cells": cells, "random": rand, "rules": verdict}
    out["sites"] = per_site
    out["label"] = per_site[DECISIVE]["rules"]["label"]
    base = per_site[DECISIVE]["cells"]["top1"]
    out["switch_swap"] = base["switch_swap"]
    out["read_pairs"] = base["n"]
    out["beside"] = beside(m, items, n_boot)
    return out


def beside(m: dict, items: list[dict], n_boot: int) -> dict:
    """CPU beside, from 49.7's stored run (the same forward as its lookup answer): per read pair, the summed move at the
    last token (every recorded head; the top 10 beside) vs switched; logistic fit and AUC with a cluster-bootstrap CI."""
    target = m["model"]["target"]
    S = source_run(target)
    a, s_items = S["a"], S["items"]
    # this run's items are 49.7's that stayed eligible here (run stage); 49.7's pairs on dropped items are left out
    ours = {it["scene"] for it in items}
    p_item, p_k = np.asarray(a["pair_item"]).astype(int), np.asarray(a["pair_k"]).astype(int)
    read = np.array([s_items[i]["half"] == "read" and s_items[i]["scene"] in ours for i in p_item])
    lk = {(r["scene"], r["k"]): r["class"] for r in S["rows"] if r["reader"] == X.LOOKUP and r["arm"] == "swap"}
    y = np.array([lk[(s_items[i]["scene"], int(k))] == "target" for i, k in zip(p_item, p_k, strict=True)])[read]
    ents = [s_items[i]["entity"] for i in p_item[read]]
    out = {}
    for key, heads in (("all_heads", None), ("top10", [tuple(x) for x in m["sets"]["top10"]["heads"]])):
        x = summed_moves(a, s_items, heads)[read]
        out[key] = {"n": len(x), "switched": int(y.sum()), "mean_switched": float(x[y].mean()) if y.any() else math.nan,
                    "mean_nonswitched": float(x[~y].mean()) if (~y).any() else math.nan,
                    "auc": auc_ci(x, y, ents, n_boot), "logistic": fit_logistic(x, y)}  # fmt: skip
    return out


def fmt(v) -> str:
    return A.fmt(v)


SET_ORDER = ("top1", "top3", "top5", "top10", "best_layer")


def figure(res: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True)
    x = np.arange(len(SET_ORDER))
    labels = ["top 1", "top 3", "top 5", "top 10", f"all of L{res['best_layer']}"]
    colors = {"last": "#2a6fdb", "question": "#7a7a7a"}
    for i, site in enumerate(SITES):
        d = res["sites"][site]
        cut = [d["cells"][n]["cut"] for n in SET_ORDER]
        mid = np.array([c[0] for c in cut], float)
        err = np.array([[c[0] - c[1], c[2] - c[0]] for c in cut], float).T
        off = (i - 0.5) * 0.36
        ax1.bar(x + off, mid, 0.34, yerr=err, color=colors[site], label=f"top sets, {site}", capsize=2)
        rm = np.array([d["random"][n]["cut_mean"] for n in SET_ORDER], float)
        rlo = np.array([d["random"][n]["cut_min"] for n in SET_ORDER], float)
        rhi = np.array([d["random"][n]["cut_max"] for n in SET_ORDER], float)
        ax1.errorbar(x + off, rm, yerr=[rm - rlo, rhi - rm], fmt="o", color="black", ms=3, capsize=2,
                     label="random sets (mean, min-max)" if i == 0 else None)  # fmt: skip
    ax1.axhline(SMALL_CUT, color="#2a6fdb", ls="--", lw=0.8)
    ax1.axhline(DIST_CUT, color="#d98c1f", ls="--", lw=0.8)
    ax1.axhline(0, color="black", lw=0.5)
    ax1.set_xticks(x, labels)
    ax1.set_ylabel("cut of the switch to slot k")
    ax1.set_title(f"{res['target']}: mean-ablated heads under the swap (read half)")
    ax1.legend(frameon=False, fontsize=7)
    d = res["sites"][DECISIVE]["cells"]
    ax2.plot(x, [d[n]["identity_changed"] for n in SET_ORDER], "o-", label="identity answers changed")
    ax2.plot(x, [d[n]["recall_changed"] for n in SET_ORDER], "s-", label="recall changed")
    ax2.plot(x, [d[n]["clean_lookup_changed"] for n in SET_ORDER], "^:", label="clean lookup changed")
    ax2.axhline(IDENT_MAX, color="black", ls="--", lw=0.8)
    ax2.set_xticks(x, labels)
    ax2.set_ylim(0, 1)
    ax2.set_title(f"collateral ({DECISIVE} token)")
    ax2.legend(frameon=False, fontsize=7)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = sealed()
    res = [analyse(r, n_boot) for r in runs]
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = RESULTS / f"x51_2-{stamp}"
    out.mkdir(parents=True)
    lines = ["# 51.2: joint head ablation under the address swap", "",
             f"Batch 51, test 51.2 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). 49.7's items and swap (s = {S_WRITE} "
             "(mu_k - mu_j) at the bridge word at L); heads ranked by their attention move at the last token on the fit "
             "half (49.7's stored attention), mean-ablated on the read half at the last token / the question tokens; "
             f"random sets of the same size in the same layers ({N_DRAWS} draws, seed {HEAD_SEED}). Decisive site "
             f"{DECISIVE}. Cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             "Rules (fixed in advance):", ""]  # fmt: skip
    lines += [f"- {k}: {v}." for k, v in RULES.items()]
    for r in res:
        lines += ["", f"## {r.get('target', r['run'])} ({r['run']})", ""]
        if r["status"] != "tested":
            lines.append(f"{r['status']}: {r['why']}.")
            continue
        ru = r["sites"][DECISIVE]["rules"]
        rq = r["sites"]["question"]["rules"]
        lines += [f"**{ru['label']}** ({DECISIVE} token; small set at k = {ru['small_ks'] or 'none'}; distributed: "
                  f"{'yes' if ru['distributed'] else 'no'}). Question tokens beside: {rq['label']}.", "",
                  f"L = {r['layer']}; heads at layers {r['recorded_layers']}; skipped (Gated DeltaNet) "
                  f"{r['skipped_linear_layers'] or 'none'}. Read items {r['read_items']}, read pairs {r['read_pairs']}; "
                  f"switch under the swap (this run, no ablation) {r['switch_swap']:.3f}. Best layer L{r['best_layer']}. "
                  "Top 10 (fit move): " + ", ".join(f"L{h['layer']}:h{h['head']} {h['move']:.2f}" for h in r["ranking_top10"]) + ".",
                  ""]  # fmt: skip
        for site in SITES:
            d = r["sites"][site]
            lines += [f"### {site} token{'s' if site == 'question' else ''}{' (decisive)' if site == DECISIVE else ''}", "",
                      "| set | heads | switch: swap -> ablated | cut [CI] | identity changed (n) | recall changed | clean lookup / recall changed | random cut mean (SD; min-max) | random identity / recall |",
                      "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
            for n in SET_ORDER:
                c, rd = d["cells"][n], d["random"][n]
                lines.append(f"| {n} | {len(r['sets'][n]['heads'])} | {c['switch_swap']:.3f} -> {c['switch_zero']:.3f} | "
                             f"{fmt(c['cut'])} | {fmt(c['identity_changed'])} ({c['identity_n']}) | {fmt(c['recall_changed'])} | "
                             f"{fmt(c['clean_lookup_changed'])} / {fmt(c['clean_recall_changed'])} | {rd['cut_mean']:.3f} "
                             f"({rd['cut_sd']:.3f}; {rd['cut_min']:.3f}-{rd['cut_max']:.3f}) | "
                             f"{fmt(rd['identity_changed'])} / {fmt(rd['recall_changed'])} |")  # fmt: skip
            lines.append("")
        lines += ["CPU beside (49.7's stored forward; read pairs; summed move at the last token vs switched):", "",
                  "| heads summed | n (switched) | mean move switched / not | AUC [CI] | logistic b per SD (per unit), a |",
                  "|---|---|---|---|---|"]  # fmt: skip
        for key, b in r["beside"].items():
            lg = b["logistic"]
            lines.append(f"| {key} | {b['n']} ({b['switched']}) | {fmt(b['mean_switched'])} / {fmt(b['mean_nonswitched'])} | "
                         f"{fmt(b['auc'])} | {fmt(lg['b_std'])} ({fmt(lg['b_per_unit'])}), {fmt(lg['a'])}"
                         f"{'' if lg['converged'] else ' (not converged)'} |")  # fmt: skip
        figure(r, out / f"heads_{r['target']}.png")
        lines += ["", f"![ablation](heads_{r['target']}.png)"]
    (out / "verdict.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "results": res}, indent=1, default=str) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "examples.md").write_text("\n".join(view_lines(runs)) + "\n")
    print("\n".join(lines))
    print(out)
    return out


VIEW_SETS = (*SET_ORDER, *(f"{n}_r0" for n in SET_ORDER))


def view_lines(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """Per run: 5 random items' prompts as read (seed 0), and per arm (set x site; the random sets' draw 0) 10 random
    read pairs (seed 0): the lookup's class and top under the swap without and with the ablation, the recall's tops."""
    from scripts import x45m

    lines = ["# 51.2 view (verify pack): prompts as read, rows per arm. UNVERIFIED.", ""]
    for run in runs:
        src = RESULTS / run
        if not (src / "status.json").exists() or json.loads((src / "status.json").read_text())["status"] != "tested":
            continue
        m = json.loads((src / "manifest.json").read_text())
        target = m["model"]["target"]
        tok = x45m.tokenizer() if target == pins.TARGET else None  # decoding needs BJ_TARGET = the run's model
        dec = (lambda t, tok=tok: repr(tok.decode([t]))) if tok is not None else str
        items = X.read_jsonl(src / "cases.jsonl")
        by = {
            (r["scene"], r["reader"], r["arm"], r["k"], r["set"], r["site"]): r
            for r in X.read_jsonl(src / "ablation.jsonl")
        }
        lines += [f"## {run} ({target})", "", f"### 5 random items of {len(items)} (seed {seed})", ""]
        for i in sorted(random.Random(seed).sample(range(len(items)), min(5, len(items)))):
            it = items[i]
            lines += [f"#### {it['scene']} ({it['half']}): bridge {it['entity']}, j = {it['j']}, lockers {it['slots']}", "",
                      "```", A.marked(tok, it) if tok is not None else "(tokenizer of another target)", "```", "",
                      f"Sites: {json.dumps(it['sites'])}", ""]  # fmt: skip
        pairs = [(it, kk) for it in items if it["half"] == "read" for kk in it["ks"]]
        for name in VIEW_SETS:
            heads = ", ".join(f"L{la}:h{h}" for la, h in m["sets"][name]["heads"])
            for site in SITES:
                lines += [f"### {name} at the {site} token(s): {heads}", "",
                          "| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |",
                          "|---|---|---|---|---|---|"]  # fmt: skip
                for p in sorted(random.Random(seed).sample(range(len(pairs)), min(k, len(pairs)))):
                    it, kk = pairs[p]
                    s = it["scene"]
                    a0, az = by[(s, X.LOOKUP, "swap", kk, None, None)], by[(s, X.LOOKUP, "swap", kk, name, site)]
                    r0, rz = by[(s, X.RECALL, "swap", kk, None, None)], by[(s, X.RECALL, "swap", kk, name, site)]
                    lines.append(f"| {s} | {kk} | {a0['class']} ({dec(a0['top'])}) | {az['class']} ({dec(az['top'])}) | "
                                 f"{dec(r0['top'])} | {dec(rz['top'])} |")  # fmt: skip
                lines.append("")
    return lines


def stage_view(runs: list[str]) -> Path:
    sealed()
    out = RESULTS / f"x51_2-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "view.md").write_text("\n".join(view_lines(runs)) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_heads/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the runs")
    ap.add_argument("--why", default="batch 51, test 51.2 (jobs/c3/batch51.yaml; Q51.2)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "view":
        stage_view(a.runs)
    else:
        stage_verdict(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
