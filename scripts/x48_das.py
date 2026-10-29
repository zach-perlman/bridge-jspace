"""x48_das (batch 48, test 48.1; jobs/c3/batch48.yaml, design, rule and readouts fixed in advance; Q48.1 in
predictions/2026-10-28_dan.md): DAS at the bridge word, two readers, two subspaces? Also batch 47's D3 (amendment 3,
jobs/c3/batch47.yaml: the same DAS at other layers on the 9B; Q-depth D3), see --layers / --depth below.

Custom distributed alignment search, no pyvene. At the bridge token at L (the layer fixed in advance), on the O prompt:
    h <- h_O + R R^T (h_S - h_O),   R in R^{d x k}, orthonormal columns (torch.nn.utils.parametrizations.orthogonal).
Loss: cross-entropy of S's answer (its first token) at the read position on the O prompt, X0's chat read (the prompt with
a digit's space token appended; the read is the last token). One R per reader: R_lookup from the lookup's loss, R_recall
from the recall's. k in {1, 4, 16, 64}; Adam, lr 1e-3, 300 steps, batch 16 (micro-batches of MICRO rows with gradient
accumulation: the same step). Baselines: an untrained random R of the same k (QR of a Gaussian, one per k); R trained on
shuffled targets (the training rows' target tokens permuted, seed SHUFFLE_SEED).

Pairs: the target's stored main-test run (x0_necessity, the generator's cf: two people swap picks; chat rendering, layer
L), its eligible scenes that are locker-first (both items' locker sentences before the asked pick, x0_strata.features),
restricted per reader to the pairs the stored whole change switches for that reader. The scene ids are recorded
(pairs.json). Split by the original bridge entity, 60 / 20 / 20 (train / select k / test), seed SPLIT_SEED: the sorted
entities shuffled once, the first 60% train, the next 20% select, the rest test; every reader and layer uses the split.

States: h_O and h_S at the bridge token at the layer are cached once (one forward per prompt, states.pt); the lookup's
and the recall's prompts are identical through the bridge token (asserted), so one cache serves both readers. R is
trained with real forward passes of the O prompt (the loss needs the layers after L; the cached Delta is what the edit
adds) and the IIA is evaluated with X0's read (generate_batch with the AddRows edit, as every X0 arm).

Read-outs (geometry.jsonl per pair and R; readouts.json per R; outcomes.jsonl per pair, reader and arm; routes.jsonl):
own-IIA by k (the switch rate under R_own); cross-IIA (R_lookup applied, the recall's switch; R_recall applied, the
lookup's switch); energy ||R R^T Delta||^2 / ||Delta||^2 per pair; the share of R R^T Delta inside the span of the pair's
25 signed-OMP J++ atoms at the layer (and 100), inside the span of its 25 W_E atoms (x0_necessity's "we" dictionary),
inside U (the pointer directions, x0_massmean.subspaces' Alf on the target's probe run, at the layer fixed in advance)
and inside U_fit (the pointer directions refit at the layer: x0_massmean.mass_mean of the train-split pairs' h_O by the
original bridge's locker-sentence index), and outside the union span(J++-25, U, W_E-25); cos^2 with U: ||R^T U||_F^2 /
rank(U) (x6_routes.mean_cos2; a random R: k / d); principal angles between R_lookup and R_recall at each k; the routes
read: R_lookup alone written on x6_routes C2 scenes (another item moved), the lookup's answer classified identity /
position / value / original / other, the recall beside.

--layers l ... (D3): the whole procedure at each listed layer (states, R per reader and k, reads, geometry at that
layer's J++ atoms and U_fit); --depth leaves out the shuffled baselines and the routes read (D3 reports own-IIA,
cross-IIA, energy inside J++-25 and cos^2 with U_l by layer). The depth verdict reads 48.1's run for L and the D3 runs
for the other layers.

SEALED: the run writes no verdict. The verdict stages (CPU) apply the rules exactly as written (48.1: (a)-(d) and the
fallback, jobs/c3/batch48.yaml; depth: D3's rule, jobs/c3/batch47.yaml) and refuse until predictions/2026-10-28_dan.md
holds Dan's answer (Q48.1, or Q-depth for D3) at the committed HEAD.

uv run python scripts/x48_das.py plan                                      # CPU, the target's tokenizer: pairs, splits
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_das.py run --name qwen35_9b_x48_das            # GPU (sealed), 48.1 at L
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_das.py run --name qwen35_9b_x47_d3 --layers 6 24 --depth   # D3
uv run python scripts/x48_das.py verdict --runs qwen35_9b_x48_das muse30_x48_das       # CPU, after Dan's Q48.1
uv run python scripts/x48_das.py depth --runs qwen35_9b_x48_das qwen35_9b_x47_d3       # CPU, after Dan's Q-depth

Batch 52 (Lightning ports): BJ_DAS_MAMBA=torch runs every forward that records a gradient on transformers' torch
reference (NemotronH's Mamba-2 and the other HF-hub kernel forwards; kernels_off); `gradcheck` checks that path first.
BJ_TARGET=nemotron-3.5-lightning BJ_DAS_MAMBA=torch BJ_PREDICTED_LAYER=14 uv run python scripts/x48_das.py gradcheck
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import json
import math
import os
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x48_das"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch48.yaml"
SPEC_47 = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION, QUESTION_DEPTH = "Q48.1", "Q-depth"
# the stored main-test runs the pairs come from (chat rendering, the generator's cf, the layer fixed in advance)
MAIN_RUN = {"qwen3.5-9b": "qwen35_9b_x0_necessity", "muse-glimmer-30b": "muse30b_x0_necessity",
            "qwen3.6-27b": "x0_necessity_27b_chat",
            # batch 52 (Lightning ports): the main test at the committed L14 (the 60 dev scenes excluded), as 48.2 A's
            "nemotron-3.5-lightning": "nem35l_x52_conflict"}  # fmt: skip
# the 9B's runs are the r2 retries (BJ_DAS_GDN=torch): the first x48_1_9b failed in fla's backward (28 Oct)
RUNS = {"qwen3.5-9b": "qwen35_9b_x48_das_r2", "muse-glimmer-30b": "muse30_x48_das", "qwen3.6-27b": "x48_das_27b"}
DEPTH_RUNS = {"qwen3.5-9b": ["qwen35_9b_x48_das_r2", "qwen35_9b_x47_d3_r2"]}
# batch 52 C coverage (amendment 2, the 27B gap; jobs/c3/x48_1_27b_r2.yaml): 48.1 named the 27B ("if time") and its run
# never ran; read by verdict --coverage alone (48.1's own verdict, the 9B and Muse, unchanged). Lightning: batch 52's
# ports (Dan's 08:55 queue item 3, jobs/c3/x52_lightning_das48.yaml; BJ_DAS_MAMBA=torch after the gradcheck)
COVERAGE_RUNS = {"qwen3.6-27b": "x48_das_27b", "nemotron-3.5-lightning": "nem35l_x52_das"}
GRADCHECK_RUN = "nem35l_x52_das_gradcheck"
GC_ITEMS, GC_K, GC_STEPS, GC_SEED = 8, 16, 20, 5200
# the check's bars (fixed with the spec, before the run; jobs/c3/x52_lightning_das_gradcheck.yaml): the torch path's
# forward agrees with the kernels' (relative L2 of h at L at the bridge token, of the read's logits; the read's top
# token on >= 30 of the 32 reads: 8 items x 2 readers, unedited and under the whole change), and the DAS loss's
# gradient on the torch path is finite and nonzero
GC_H_REL, GC_LOGIT_REL, GC_TOP_MIN = 0.02, 0.05, 30
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x48_das/verdict-20261028T134153Z"  # 48.1's rules first scored (the 9B and Muse)
RENDERING = "chat"
KS = (1, 4, 16, 64)
K_LOW = 16  # rule (a): own-IIA >= 0.7 at some k <= 16
LR, STEPS, BATCH, MICRO = 1e-3, 300, 16, 8
SPLIT = (0.6, 0.2, 0.2)
SPLIT_SEED, INIT_SEED, SHUFFLE_SEED, RAND_SEED, BATCH_SEED = 0, 48, 4801, 4802, 4803
N_ROUTES, N_ROUTES_CANDIDATES = 100, 160  # the routes read: the first eligible C2 scenes of x6_routes' generator
K_JPP = (X.K_MAIN, 100)
EPS = 1e-9  # a value exactly at a bar counts as at the bar
OWN_IIA, CROSS_IIA = 0.7, 0.25
LENS_RECALL, LENS_RANDOM, LENS_LOOKUP = 0.5, 0.15, 0.2
ADDRESS, OUTSIDE, ROUTES_IDENTITY = 0.5, 0.5, 0.3
NO_MEDIATOR, NOT_SELECTIVE = 0.5, 0.8
D3_IIA, D3_HALF, D3_L, D3_STAYS = 0.6, 0.4, 0.2, 0.4
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
RULE = {
    "a": "two readers, two subspaces: own-IIA >= 0.7 at some k <= 16 for both readers, and cross-IIA <= 0.25 in both "
         "directions (paired CI excluding overlap with own-IIA)",
    "b": "the recall's subspace is the lens's part: R_recall's energy inside the J++-25 part >= 0.5 (random R <= 0.15); "
         "R_lookup's <= 0.2",
    "c": "the address is part of the lookup's subspace: ||R_lookup^T U||_F^2 / 4 >= 0.5 (random R ~ k/d)",
    "d": "a third identity code: R_lookup's energy outside (J++-25 u U u W_E-25) >= 0.5 while its own-IIA >= 0.7, and "
         "R_lookup alone gives identity answers >= 0.3 in the routes read",
    "fallback": "if own-IIA stays < 0.5 at k = 64 for the lookup: no low-dimensional mediator at this token and layer",
}  # fmt: skip
RULE_D3 = ("'the lookup's subspace leaves the lens with depth' if R_lookup's energy inside J++ falls from >= 0.4 at L/2 "
           "to <= 0.2 at L while own-IIA stays >= 0.6; 'the recall's stays' if R_recall's share stays >= 0.4 at every "
           "layer where its IIA >= 0.6")  # fmt: skip
AS_COMPUTED = (
    "chosen k per reader = the smallest k <= 16 whose select-split own-IIA >= 0.7, else the k with the highest select "
    "own-IIA; every rule is read at the chosen k on the test entities' pairs (point estimates = means over the reader's "
    "test pairs; cluster-bootstrap CIs over bridge entities, 10,000, seed 0, beside them); 'paired CI excluding overlap' = "
    "the paired bootstrap of own-IIA minus cross-IIA over the reader's test pairs has a lower bound > 0; cross-IIA for "
    "a reader = its switch rate under the other reader's R at that reader's chosen k; energy inside a part = the share of "
    "R R^T Delta's squared norm in the span of the pair's signed-OMP atoms (J++ / W_E) or of U; outside = 1 minus the "
    "share in the orthonormalised union of the three; cos^2 with U = ||R^T U||_F^2 / rank(U); the routes read at the "
    "lookup's chosen k on the eligible C2 scenes; fallback read on the lookup's test own-IIA at k = 64"
)
AS_COMPUTED_D3 = (
    "per layer and reader the chosen k as in 48.1 (the select split at that layer); 'R_lookup's energy inside J++' = the "
    "test-pair mean of the share of R R^T Delta inside the span of the pair's 25 signed-OMP J++ atoms at that layer, at "
    "the chosen k; 'leaves the lens' = that share >= 0.4 at L/2 and <= 0.2 at L with the lookup's test own-IIA >= 0.6 at "
    "both layers; 'the recall's stays' = among the layers run where the recall's test own-IIA >= 0.6, every one has its "
    "share >= 0.4 (no such layer: not tested); L and L/2 from the target's layer fixed in advance; the L row from the "
    "48.1 run, the other layers from the D3 runs; cos^2 with U_l uses the pointer directions refit at l on the "
    "train-split pairs' h_O (x0_massmean.mass_mean by the original bridge's locker-sentence index)"
)


# ---- pairs (tokenizer only) ---------------------------------------------------------------------------------------


GDN_ENV = "BJ_DAS_GDN"


def torch_gdn(hf) -> str | None:
    """With BJ_DAS_GDN=torch, the linear-attention layers' chunked gated delta rule runs transformers' torch reference
    instead of fla: fla 0.5.2's backward refuses on Hopper with Triton 3.6 (wrong gradients, fla #640; x48_1_9b,
    28 Oct), and DAS needs that backward. Returns the patched module's name; None when the switch is off or the model
    has no gated DeltaNet (Muse)."""
    if os.environ.get(GDN_ENV, "") != "torch":
        return None
    from bridge_jspace.knockout import reference_chunk_rule

    gdn = next((mod for mod in hf.modules() if type(mod).__name__.endswith("GatedDeltaNet")), None)
    if gdn is None:
        return None
    ns = sys.modules[type(gdn).__module__]
    vars(ns)["torch_chunk_gated_delta_rule"] = reference_chunk_rule(gdn)  # the GDN forward reads the module global
    return ns.__name__


# Batch 52 (Lightning ports, Dan's 08:55 queue item 3): NemotronH's Mamba-2 mixer runs HF-hub kernels (mamba-ssm's conv1d
# and chunk scan; pins: use_kernels) whose backward no run of ours has checked. With BJ_DAS_MAMBA=torch every forward
# that records a gradient (the DAS training forward, batch_logits) runs transformers' torch reference instead, so the
# backward is autograd's; reads without a gradient keep the pinned kernels. `gradcheck` compares the two paths first.
MAMBA_ENV = "BJ_DAS_MAMBA"


def _closure(f) -> dict[str, Any]:
    return dict(zip(f.__code__.co_freevars, (c.cell_contents for c in f.__closure__ or ()), strict=True))


def kernelized(hf) -> list:
    """Every object whose forward an HF-hub kernel may replace (kernels.kernelize sets an instance `forward` on it), each
    once: the kernel functions attached to a module (use_kernelized_func: NemotronH's Mamba-2 causal_conv1d_fn,
    mamba_chunk_scan_combined, ...; its attention's rotary_pos_emb) and the kernel-layer modules (NemotronHRMSNorm)."""
    out, seen = [], set()
    for mod in hf.modules():
        own = [mod] if hasattr(type(mod), "kernel_layer_name") else []
        for obj in [*vars(mod).get("_kernel_funcs", {}).values(), *own]:
            if id(obj) not in seen:
                seen.add(id(obj))
                out.append(obj)
    return out


def torch_reference_of(obj) -> str:
    """What obj's own (class) forward runs, asserted to be transformers' torch code: a kernel function made by
    use_kernel_func_from_hub_with_fallback must not resolve to an installed package (mamba_ssm, causal_conv1d)."""
    fwd = type(obj).forward
    func = _closure(fwd).get("func") if fwd.__closure__ else None  # kernels' Func module wraps a plain function
    if func is None:
        return f"{type(obj).__module__}.{type(obj).__name__}.forward"
    inner = _closure(func) if func.__closure__ else {}
    assert not inner.get("is_new_implementation", False), (
        f"{type(obj).kernel_layer_name}: its fallback is {inner.get('implementation')}, not transformers' torch reference"
    )
    ref = inner.get("torch_function", func)
    return f"{ref.__module__}.{ref.__name__}"


@contextlib.contextmanager
def kernels_off(hf):
    """Within: every forward an HF-hub kernel replaced runs its own class forward again (transformers' torch reference,
    asserted per object); the kernel forwards are put back on exit. Yields the replaced objects' torch references."""
    saved, refs = [], []
    for obj in kernelized(hf):
        refs.append(torch_reference_of(obj))
        if "forward" in vars(obj):
            assert not hasattr(obj, "_hf_hook"), f"{type(obj).__name__}: an accelerate hook wraps forward; not handled"
            saved.append((obj, vars(obj).pop("forward")))
    try:
        yield sorted(set(refs))
    finally:
        for obj, fwd in saved:
            obj.forward = fwd


def das_forward_path(hf):
    """The path of a DAS forward: kernels_off(hf) with BJ_DAS_MAMBA=torch while a gradient is recorded, else as loaded."""
    import torch

    if os.environ.get(MAMBA_ENV, "") == "torch" and torch.is_grad_enabled():
        return kernels_off(hf)
    return contextlib.nullcontext()


def torch_mamba(hf) -> str | None:
    """With BJ_DAS_MAMBA=torch: the manifest's record of the switch (checked: the model has Mamba-2 mixers and every
    kernel function falls back to transformers' torch code); None when the switch is off."""
    if os.environ.get(MAMBA_ENV, "") != "torch":
        return None
    n = sum(type(m).__name__.endswith("Mamba2Mixer") for m in hf.modules())
    assert n, f"{MAMBA_ENV}=torch: {type(hf).__name__} has no Mamba-2 mixer"
    with kernels_off(hf) as refs:
        pass
    return (f"torch reference for the DAS training forward ({MAMBA_ENV}=torch): while a gradient is recorded the {n} "
            f"Mamba-2 mixers and every other HF-hub kernel forward run transformers' torch code ({', '.join(refs)}; "
            "autograd's backward); reads without a gradient keep the pinned kernels")  # fmt: skip


def rebuild(tok, set_name: str, alt: str) -> list[dict]:
    """The main run's chat cases (x0_necessity.build_cases) rebuilt on this tokenizer; X0's settings restored after."""
    old = X.ALT, X.RENDERINGS
    X.ALT, X.RENDERINGS = alt, (RENDERING,)
    try:
        cases, _ = X.build_cases(tok, set_name)
    finally:
        X.ALT, X.RENDERINGS = old
    return cases


def stored_whole(src: Path, layer: int) -> dict[str, dict[str, int]]:
    """Per scene of the stored run's chat outcomes at the layer, each reader's whole-change switch."""
    out: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] == RENDERING and r["layer"] == layer and r["arm"] == "whole":
            out[r["scene"]][r["reader"]] = int(r["switched"])
    return dict(out)


def locker_first(case: dict) -> bool:
    f = ST.features(case)
    return f["org locker vs asked pick"] == "before" and f["alt locker vs asked pick"] == "before"


def split_entities(entities: list[str], seed: int = SPLIT_SEED, shares: tuple[float, ...] = SPLIT) -> dict[str, str]:
    """Each bridge entity's split: the sorted entities shuffled once (seed), the first round(60%) train, the next
    round(20%) select, the rest test (each part at least one entity)."""
    ents = sorted(set(entities))
    assert len(ents) >= 3, f"{len(ents)} entities: too few to split"
    random.Random(seed).shuffle(ents)
    n_train = max(1, round(shares[0] * len(ents)))
    n_select = max(1, round(shares[1] * len(ents)))
    n_train = min(n_train, len(ents) - n_select - 1)
    out = {}
    for i, e in enumerate(ents):
        out[e] = "train" if i < n_train else "select" if i < n_train + n_select else "test"
    return out


def select_pairs(tok, main_run: str, layer: int) -> tuple[list[dict], dict]:
    """The 48.1 pairs in the stored run's scene order: the run's eligible chat scenes at the layer, locker-first (both
    items' lockers before the asked pick), switched by the stored whole change for at least one reader; per pair the
    readers' stored switches (the per-reader restriction), the split, both readers' prompts, the original bridge's
    locker-sentence index (x0_probe.positions). Counts beside."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T
    from scripts import x0_probe as P

    src = X.RESULTS / main_run
    m = json.loads((src / "manifest.json").read_text())
    alt = m.get("alt") or "cf"
    assert alt == "cf", f"{main_run}: alt {alt!r}, not the main test's cf (two people swap)"
    assert m["predicted"] == layer, f"{main_run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{main_run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {main_run}"
    whole = stored_whole(src, layer)
    # the read order (gate.json "order" since 24 Oct; older runs: build_cases' sorted scene ids, the eligible kept in order)
    order = json.loads((src / "gate.json").read_text()).get("order", {}).get(RENDERING) or sorted(whole)
    assert order, f"{main_run}: no chat scenes at layer {layer}"
    assert set(order) == set(whole), f"{main_run}: the chat order and the whole-arm scenes differ"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    rebuilt = {c["scene"]: c for c in rebuild(tok, m["set"], alt)}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    pool, counts = [], collections.Counter()
    for scene in order:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {main_run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        if not locker_first(c):
            counts["not locker-first"] += 1
            continue
        sw = {w: whole[scene].get(w, 0) for w in X.READERS}
        if not any(sw.values()):
            counts["locker-first, the whole change switches neither reader"] += 1
            continue
        ids = {w: c["readers"][w]["ids"] for w in X.READERS}
        pos = c["pos"]
        # the read position: both readers read the last token of their own prompt (the appended space) after the same
        # patched context: the prompts identical through the bridge token, the patch at one position
        assert ids[X.LOOKUP]["org"][: pos + 1] == ids[X.RECALL]["org"][: pos + 1], f"{scene}: prefixes differ"
        assert ids[X.LOOKUP]["alt"][: pos + 1] == ids[X.RECALL]["alt"][: pos + 1], f"{scene}: alt prefixes differ"
        texts = {}
        for w in X.READERS:
            texts[w] = X.render(tok, by_id[c["readers"][w]["id"]], RENDERING, c["context"])
            enc = raw_encoding(tok, texts[w], offsets=True)
            assert enc["input_ids"] == ids[w]["org"], f"{scene} {w}: the rendered prompt's ids differ"
            if w == X.LOOKUP:
                mark = list(enc["offset_mapping"][pos])
        _, locker_index, _ = P.positions(c)
        pool.append({
            "scene": scene, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
            "upstream": c["upstream"], "pos": pos, "space": c["space"], "read_suffix": tok.decode(c["space"]),
            "context": c["context"], "cf_context": c["cf_context"], "stored_whole": sw, "bridge_mark": mark,
            "locker_index": locker_index, "read_index": {w: len(ids[w]["org"]) for w in X.READERS},
            "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b",
                                                             "ids")}, "text": {"org": texts[w]}} for w in X.READERS},
        })  # fmt: skip
    split = split_entities([p["entity"] for p in pool])
    for p in pool:
        p["split"] = split[p["entity"]]
    per = {READER_NAME[w]: {s: sum(p["split"] == s and p["stored_whole"][w] for p in pool)
                            for s in ("train", "select", "test")} for w in X.READERS}  # fmt: skip
    info = {"main_run": main_run, "layer": layer, "scenes_at_L": len(order), "dropped": dict(counts), "pairs": len(pool),
            "entities": len(split), "entities_per_split": dict(collections.Counter(split.values())),
            "pairs_per_reader_and_split": per, "split_seed": SPLIT_SEED,
            "locker_index_classes_train": dict(collections.Counter(p["locker_index"] for p in pool if p["split"] == "train")),
            "scene_ids": {s: [p["scene"] for p in pool if p["split"] == s] for s in ("train", "select", "test")}}  # fmt: skip
    return pool, info


def pointer_basis(target: str):
    """U: the pointer directions (x0_massmean.subspaces' Alf, [d, r] orthonormal) on the target's probe run."""
    from scripts import x0_massmean as MM
    from scripts import x6_routes as R

    sub, info = MM.subspaces(R.STATES[target])
    return sub["Alf"], {"states_run": R.STATES[target], "rank": int(sub["Alf"].shape[1]), "info": info}


def fit_pointer(h_o: np.ndarray, locker_index: list[int]) -> np.ndarray:
    """U_fit [d, classes - 1]: the pointer directions refit at a layer, x0_massmean.mass_mean of the train-split pairs'
    h_O by the original bridge's locker-sentence index (no layout-free step: too few pairs per layout group)."""
    from scripts import x0_massmean as MM

    assert len(set(locker_index)) >= 2, f"one locker-index class in the train split: {set(locker_index)}"
    return MM.mass_mean(h_o.astype(np.float64), list(locker_index))


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    pairs, info = select_pairs(tok, MAIN_RUN[pins.TARGET], layer)
    info["target"] = pins.TARGET
    try:
        _, u = pointer_basis(pins.TARGET)
        info["U"] = {"states_run": u["states_run"], "rank": u["rank"]}
    except FileNotFoundError as e:
        info["U"] = f"probe run not here: {e}"
    if pairs:
        it = pairs[0]
        info["example"] = {"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}", "split": it["split"],
                           "lookup_O_marked": marked_prompt(it, X.LOOKUP)}  # fmt: skip
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return info


def marked_prompt(it: dict, reader: str) -> str:
    """The reader's O prompt as the model reads it (the space token appended), the bridge word in ⟦bridge:…⟧."""
    a, b = it["bridge_mark"]
    text = it["readers"][reader]["text"]["org"] + it["read_suffix"]
    while a < b and text[a].isspace():
        a += 1
    return f"{text[:a]}⟦bridge:{text[a:b]}⟧{text[b:]}"


# ---- DAS (torch) --------------------------------------------------------------------------------------------------


def intervene(h_o, delta, r):
    """The intervention at one position: h_O + R R^T (h_S - h_O) for rows h_o, delta [n, d] and R [d, k]."""
    return h_o + (delta @ r) @ r.T


def subspace_module(d: int, k: int, seed: int):
    """R [d, k] with orthonormal columns as a parametrised module: the weight of a Linear(k, d) under
    torch.nn.utils.parametrizations.orthogonal (tall: orthonormal columns), initialised from a seeded Gaussian."""
    import torch
    from torch.nn.utils import parametrizations

    lin = torch.nn.Linear(k, d, bias=False)
    with torch.no_grad():
        lin.weight.copy_(torch.randn(d, k, generator=torch.Generator().manual_seed(seed)))
    return parametrizations.orthogonal(lin)


def random_basis(d: int, k: int, seed: int):
    """An untrained random R [d, k]: QR of a seeded Gaussian, signs fixed."""
    import torch

    q, r = torch.linalg.qr(torch.randn(d, k, generator=torch.Generator().manual_seed(seed)))
    return q * torch.sign(torch.diagonal(r))


def padded(model, rows: list[list[int]]):
    """Right-padded ids [B, S] and the attention mask; the real tokens of a row come first, so a causal model's states
    at them are those of the unpadded prompt."""
    import torch

    pad = model.tokenizer.pad_token_id
    pad = model.tokenizer.eos_token_id if pad is None else pad
    S = max(len(r) for r in rows)
    ids = torch.full((len(rows), S), int(pad), dtype=torch.long)
    mask = torch.zeros((len(rows), S), dtype=torch.long)
    for i, r in enumerate(rows):
        ids[i, : len(r)], mask[i, : len(r)] = torch.tensor(r), 1
    return ids.to(model.device), mask.to(model.device)


def batch_logits(model, layer: int, rows: list[list[int]], positions: list[int], adds):
    """Logits [B, vocab] (fp32) at each row's last token of one forward of several prompts with gradient, adds[i]
    [d] added to row i's block output at `layer`, position positions[i] (the DAS edit; gradient flows into adds). With
    BJ_DAS_MAMBA=torch a forward recording a gradient runs the torch reference (das_forward_path)."""
    import torch

    from bridge_jspace.model import _forward_hooks

    ids, mask = padded(model, rows)
    last = torch.tensor([len(r) - 1 for r in rows], device=ids.device)
    b = torch.arange(len(rows), device=ids.device)
    p = torch.tensor(positions, device=ids.device)

    def hook(_module, _args, out):
        h = out[0] if isinstance(out, tuple) else out
        add = torch.zeros_like(h)
        add[b, p] = adds.to(h.dtype)
        h = h + add
        return (h, *out[1:]) if isinstance(out, tuple) else h

    with _forward_hooks([(model.layers[layer], hook)]), das_forward_path(model.hf):
        logits = model.hf(input_ids=ids, attention_mask=mask, use_cache=False).logits
    return logits[b, last].float()


def train_subspace(model, layer: int, rows: list[dict], k: int, seed: int, steps: int = STEPS, batch: int = BATCH,
                   lr: float = LR, micro: int = MICRO, shuffle: int | None = None, log: list | None = None,
                   desc: str = "") -> Any:  # fmt: skip
    """DAS: R [d, k] (orthonormal columns) trained by Adam on the cross-entropy of each row's target at the read position
    of its O prompt (the space token appended) under h_O + R R^T delta at the bridge token. rows: {"ids": O's ids,
    "pos", "delta" [d], "target"}. Each step: `batch` rows drawn without replacement (seed BATCH_SEED + seed), in
    micro-batches of `micro` with gradient accumulation (one Adam step). With shuffle (a seed) the rows' targets are
    permuted once before training (the shuffled-target baseline). Returns R on the CPU (fp32); `log` gets one record
    per 25 steps (loss, the batch's share of argmax == target)."""
    import torch

    from bridge_jspace.utils import progress

    targets = [r["target"] for r in rows]
    if shuffle is not None:
        targets = list(targets)
        random.Random(shuffle).shuffle(targets)
    d = rows[0]["delta"].shape[-1]
    mod = subspace_module(d, k, seed).to(model.device)
    opt = torch.optim.Adam(mod.parameters(), lr=lr)
    rng = random.Random(BATCH_SEED + seed)
    n = len(rows)
    for step in progress(range(steps), desc or f"DAS k={k}", total=steps):
        idx = rng.sample(range(n), min(batch, n))
        opt.zero_grad(set_to_none=True)
        total, hits = 0.0, 0
        for s in range(0, len(idx), micro):
            # R recomputed per micro-batch: each backward frees the orthogonal map's graph (no parametrize.cached)
            r_mat: Any = mod.weight  # [d, k], orthonormal columns
            chunk = idx[s : s + micro]
            delta = torch.stack([rows[i]["delta"] for i in chunk]).to(model.device).float()
            adds = (delta @ r_mat) @ r_mat.T
            logits = batch_logits(model, layer, [rows[i]["ids"] for i in chunk], [rows[i]["pos"] for i in chunk], adds)
            tgt = torch.tensor([targets[i] for i in chunk], device=logits.device)
            loss = torch.nn.functional.cross_entropy(logits, tgt, reduction="sum") / len(idx)
            loss.backward()
            total += float(loss.detach())
            hits += int((logits.argmax(-1) == tgt).sum())
        opt.step()
        if log is not None and (step % 25 == 0 or step == steps - 1):
            log.append({"k": k, "step": step, "loss": round(total, 4), "batch_acc": round(hits / len(idx), 4)})
    with torch.no_grad():
        weight: Any = mod.weight
        r_out = weight.detach().float().cpu().clone()
    assert torch.allclose(r_out.T @ r_out, torch.eye(k), atol=1e-4), "R's columns are not orthonormal"
    return r_out


# ---- geometry (torch, CPU or GPU) ---------------------------------------------------------------------------------


def share_in(v, q) -> float:
    """The share of v's squared norm inside the span of the orthonormal columns q ([d, m]); nan for a zero v."""
    n2 = float(v.double().norm() ** 2)
    if n2 <= 0:
        return math.nan
    if q.shape[1] == 0:
        return 0.0
    return float((q.double().T @ v.double()).norm() ** 2 / n2)


def principal_angles(a, b) -> list[float]:
    """The principal angles (degrees, ascending) between the column spans of a and b (orthonormal columns)."""
    import torch

    s = torch.linalg.svdvals(a.double().T @ b.double()).clamp(-1, 1)
    return [round(float(math.degrees(math.acos(float(x)))), 3) for x in s]


def geometry_row(delta, r_mat, spans: dict[str, Any]) -> dict[str, float | None]:
    """One pair and one R: the energy ||R R^T Delta||^2 / ||Delta||^2, the share of R R^T Delta inside each span of
    `spans` (orthonormal column bases: jpp25, jpp100, we25, U, Ufit, union) and outside the union."""
    v = (delta.double() @ r_mat.double()) @ r_mat.double().T
    n2 = float(delta.double().norm() ** 2)
    out = {"energy": float(v.norm() ** 2 / n2) if n2 > 0 else math.nan}
    for name, q in spans.items():
        out[f"in_{name}"] = share_in(v, q) if q is not None else math.nan
    out["outside_union"] = 1.0 - out["in_union"] if not math.isnan(out["in_union"]) else math.nan
    return {k: (round(x, 6) if not math.isnan(x) else None) for k, x in out.items()}


def spans_of(jdic, wdic, u, u_fit, atoms_j, atoms_w) -> dict[str, Any]:
    """The pair's spans: its 25 and 100 signed-OMP J++ atoms (the first 25 of the greedy 100 picks are the 25-atom
    fit's), its 25 W_E atoms, U (the probe run's pointer directions; None if absent), U_fit (refit at the layer), and
    the orthonormalised union of J++-25, U (U_fit where U is absent) and W_E-25."""
    import torch

    from scripts.x6_routes import orthonormal

    j25, w25 = jdic[atoms_j[: X.K_MAIN]].T, wdic[atoms_w[: X.K_MAIN]].T
    u_union = u if u is not None else u_fit
    return {"jpp25": orthonormal(j25), "jpp100": orthonormal(jdic[atoms_j[:100]].T), "we25": orthonormal(w25),
            "U": None if u is None else orthonormal(u), "Ufit": orthonormal(u_fit),
            "union": orthonormal(torch.cat([j25.double(), u_union.double(), w25.double()], 1))}  # fmt: skip


def we_dictionary(model, letters):
    """x0_necessity's "we" dictionary (unit input-embedding rows of the letter tokens) on the model's home device."""
    import torch

    w = model.hf.get_input_embeddings().weight
    return torch.nn.functional.normalize(w[letters.to(w.device)].float().to(model.device), dim=-1)


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def arm_names(ks: tuple[int, ...] = KS, shuffled: bool = True) -> list[str]:
    """Every evaluated arm, in order: none, whole, then per k R_lookup, R_recall, random, [shuffled lookup / recall]."""
    out = ["none", "whole"]
    for k in ks:
        out += [f"R_{X.LOOKUP}_k{k}", f"R_{X.RECALL}_k{k}", f"rand_k{k}"]
        if shuffled:
            out += [f"shuf_{X.LOOKUP}_k{k}", f"shuf_{X.RECALL}_k{k}"]
    return out


def routes_scenes(
    model, ws, digits, n: int = N_ROUTES, candidates: int = N_ROUTES_CANDIDATES
) -> tuple[list[dict], dict]:
    """x6_routes' C2 scenes (another item moved: Iris picks B, B's and C's locker sentences swapped, B's digit new), the
    first `candidates` generated, the first n eligible under X0's competence check (both readers say and read O's and
    S's answers right)."""
    from scripts import x6_routes as R

    cases, dropped = R.scenes(model.tokenizer, R.N_GEN, rendering=RENDERING)
    c2 = [c for c in cases if c["condition"] == "C2"][:candidates]
    comp = X.competence(model, c2, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    ok = [c for c in c2 if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                               for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    acc = {READER_NAME[w]: round(float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in c2])), 4)
           for w in X.READERS}  # fmt: skip
    return ok[:n], {"generated_C2": sum(c["condition"] == "C2" for c in cases), "candidates": len(c2),
                    "eligible": len(ok), "used": min(n, len(ok)), "org_read_accuracy": acc,
                    "dropped_by_generator": dict(dropped), "seed": R.SEED}  # fmt: skip


def run_layer(model, out: Path, pairs: list[dict], layer: int, ks: tuple[int, ...], steps: int, shuffled: bool,
              u_np: np.ndarray | None, lens, log_rows: list[dict]) -> dict[str, Any]:  # fmt: skip
    """The whole procedure at one layer: the states cached, R per reader and k (and the baselines), the geometry per
    pair and R, every arm read on the select and test pairs (rows appended to the run's files, tagged with the layer).
    Returns the R matrices and the per-R readouts."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows
    from scripts.x0_parts import omp_atoms

    dev = model.device
    tok = model.tokenizer
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    letters = model.letter_token_ids()
    jdic = lens.vectors(layer, letters)
    wdic = we_dictionary(model, letters)
    # 1. the states at the bridge token (one forward per prompt), cached
    h_o, h_s = [], []
    with torch.no_grad():
        for it in progress(pairs, f"states at L{layer} (pair)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][it["pos"]].float().cpu()
                 for v in ("org", "alt")}  # fmt: skip
            h_o.append(h["org"])
            h_s.append(h["alt"])
    h_o_t, h_s_t = torch.stack(h_o), torch.stack(h_s)
    delta = h_s_t - h_o_t  # [n, d] fp32, CPU
    torch.save({"scenes": [it["scene"] for it in pairs], "h_O": h_o_t, "h_S": h_s_t, "delta": delta, "layer": layer,
                "pos": [it["pos"] for it in pairs]}, out / f"states_L{layer}.pt")  # fmt: skip
    d = delta.shape[1]
    train_idx = [i for i, it in enumerate(pairs) if it["split"] == "train"]
    u_fit_np = fit_pointer(h_o_t[train_idx].numpy(), [pairs[i]["locker_index"] for i in train_idx])
    # 2. training (one R per reader and k; the shuffled-target baseline beside; a random R per k)
    rows_of = {w: [{"ids": it["readers"][w]["ids"]["org"] + it["space"], "pos": it["pos"], "delta": delta[i],
                    "target": it["readers"][w]["tok_b"]}
                   for i, it in enumerate(pairs) if it["split"] == "train" and it["stored_whole"][w]]
               for w in X.READERS}  # fmt: skip
    mats: dict[str, Any] = {}
    for k in ks:
        mats[f"rand_k{k}"] = random_basis(d, k, RAND_SEED + k)
        for wi, w in enumerate(X.READERS):
            for shuf in (False, True) if shuffled else (False,):
                key = f"{'shuf' if shuf else 'R'}_{w}_k{k}"
                tlog: list[dict] = []
                mats[key] = train_subspace(model, layer, rows_of[w], k, INIT_SEED + 100 * k + wi + (10 if shuf else 0),
                                           steps=steps, shuffle=(SHUFFLE_SEED + k + wi) if shuf else None, log=tlog,
                                           desc=f"L{layer} DAS {key} ({len(rows_of[w])} rows)")  # fmt: skip
                log_rows += [{"layer": layer, "R": key, "reader": w, "shuffled": shuf, "n_rows": len(rows_of[w]), **r}
                             for r in tlog]  # fmt: skip
    print(f"L{layer}: trained", sorted(mats), flush=True)
    # 3. the geometry per pair and R (the J++ / W_E atoms per pair at this layer, U and U_fit)
    x = delta.to(jdic.device)
    u = None if u_np is None else torch.tensor(u_np, dtype=torch.float32, device=x.device)
    u_fit = torch.tensor(u_fit_np, dtype=torch.float32, device=x.device)
    atoms_j = omp_atoms(jdic, x, max(K_JPP)).cpu()
    atoms_w = omp_atoms(wdic, x, X.K_MAIN).cpu()
    geo = []
    for i, it in enumerate(progress(pairs, f"L{layer} geometry (pair)")):
        spans = spans_of(jdic, wdic, u, u_fit, atoms_j[i], atoms_w[i])
        for key, r_mat in mats.items():
            geo.append({"layer": layer, "scene": it["scene"], "entity": it["entity"], "split": it["split"], "R": key,
                        "norm": round(float(x[i].norm()), 4), **geometry_row(x[i], r_mat.to(x.device), spans)})  # fmt: skip
    with (out / "geometry.jsonl").open("a") as f:
        f.writelines(json.dumps(r) + "\n" for r in geo)
    cos2 = lambda a, b: round(float(R.mean_cos2(a, b) or 0.0), 6)  # noqa: E731 (None only for a zero b; U is not)
    readouts: dict[str, Any] = {key: {"k": int(r_mat.shape[1]),
                                      "cos2_U": None if u is None else cos2(r_mat.to(x.device), u),
                                      "cos2_Ufit": cos2(r_mat.to(x.device), u_fit),
                                      "random_expectation_cos2_U": round(r_mat.shape[1] / d, 6)}
                                for key, r_mat in mats.items()}  # fmt: skip
    readouts["principal_angles_deg"] = {f"k{k}": principal_angles(mats[f"R_{X.LOOKUP}_k{k}"], mats[f"R_{X.RECALL}_k{k}"])
                                        for k in ks}  # fmt: skip
    readouts["d"], readouts["rank_U"] = d, None if u is None else int(R.orthonormal(u).shape[1])
    readouts["rank_Ufit"] = int(u_fit.shape[1])
    readouts["U_vs_Ufit_cos2"] = None if u is None else cos2(u_fit, u)
    # 4. the reads: every arm on the select and test pairs, both readers (real forwards, X0's read)
    arms = arm_names(ks, shuffled)
    parts = {key: ((x @ r_mat.to(x.device)) @ r_mat.to(x.device).T).float() for key, r_mat in mats.items()}
    rows = []
    with torch.no_grad():
        held = [(i, it) for i, it in enumerate(pairs) if it["split"] != "train"]
        for i, it in progress(held, f"L{layer} reads (pair)", total=len(held)):
            adds = {"none": None, "whole": x[i : i + 1]}
            adds.update({key: parts[key][i : i + 1] for key in mats})
            edits: list[dict] = [{} if adds[a] is None else {layer: AddRows(adds[a], [it["pos"]])} for a in arms]
            for w, rd in it["readers"].items():
                logits: Any = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], ws)[0]
                assert len(logits) == len(arms)
                for j, a in enumerate(arms):
                    lg: Any = logits[j]
                    top = int(lg.argmax())
                    rows.append({"layer": layer, "scene": it["scene"], "entity": it["entity"], "split": it["split"],
                                 "reader": w, "in_pairs": it["stored_whole"][w], "arm": a, **X.read_row(lg, rd, digits),
                                 "right": int(top == rd["tok_A"]), "top_text": tok.decode([top])})  # fmt: skip
    with (out / "outcomes.jsonl").open("a") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    return {"mats": mats, "readouts": readouts, "u_fit": u_fit_np}


def stage_run(name: str, why: str, layers: tuple[int, ...] | None = None, depth: bool = False, steps: int = STEPS,
              ks: tuple[int, ...] = KS, n_routes: int = N_ROUTES) -> Path:  # fmt: skip
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.1 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"48.1 runs on {sorted(MAIN_RUN)}, not {target}"
    main_run, main_layer = MAIN_RUN[target], X.PREDICTED[target]
    layers = tuple(layers) if layers else (main_layer,)
    assert len(set(layers)) == len(layers), f"a layer twice: {layers}"
    shuffled, routes = not depth, not depth
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / main_run
    u_np, u_info = pointer_basis(target)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
         "test": "47 D3" if depth else "48.1", "spec": "jobs/c3/batch47.yaml (D3)" if depth else "jobs/c3/batch48.yaml (48.1)",
         "question": f"{QUESTION_DEPTH if depth else QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in
                    (SPEC_47 if depth else SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl",
                     src / "gate.json")},
         "main_run": main_run, "layer": main_layer, "layers": list(layers), "depth": depth, "ks": list(ks), "k_low": K_LOW,
         "training": {"loss": "cross-entropy of S's answer's first token at the read position (the appended space) of "
                              "the O prompt under h_O + R R^T (h_S - h_O) at the bridge token at the layer; real forward "
                              "passes of the O prompt (right-padded micro-batches), the cached Delta added",
                      "optimizer": "Adam", "lr": LR, "steps": steps, "batch": BATCH, "micro_batch": MICRO,
                      "batching": f"each step {BATCH} training rows drawn without replacement (seed {BATCH_SEED} + the R's seed)",
                      "parametrization": "torch.nn.utils.parametrizations.orthogonal on Linear(k, d).weight [d, k]",
                      "init_seed": f"{INIT_SEED} + 100 * k + reader index (lookup 0, recall 1; shuffled: + 10)",
                      "shuffled_targets": (f"the training rows' targets permuted once, seed {SHUFFLE_SEED} + k + reader index"
                                           if shuffled else "not run (D3)"),
                      "random_R": f"QR of a seeded Gaussian, seed {RAND_SEED} + k (one per k, both readers)"},
         "pairs": "the stored main-test run's eligible chat scenes at L, locker-first (both items' lockers before the "
                  "asked pick), switched by the stored whole change for at least one reader; each reader trains and is "
                  "read on the pairs the whole change switches for it; split by the original bridge entity 60 / 20 / 20 "
                  f"(train / select k / test), seed {SPLIT_SEED}; the same pairs and split at every layer",
         "states": "h_O and h_S at the bridge token at the layer cached once per pair (states_L<l>.pt); the readers' "
                   "prompts are identical through the bridge token (asserted), one cache for both",
         "read": "X0's chat read: the prompt with a digit's space token appended, the top token; switch = S's answer's "
                 "first token (own-IIA, cross-IIA); every read a real forward with the AddRows edit at the layer",
         "read_position": "both readers read the last token of their own prompt after the same patched context (the "
                          "prompts identical through the bridge token, asserted per pair; the index per reader recorded)",
         "geometry": "per pair and R: energy ||R R^T Delta||^2 / ||Delta||^2; the share of R R^T Delta inside the span of "
                     "the pair's 25 / 100 signed-OMP J++ atoms at the layer, its 25 W_E atoms (x0_necessity's we "
                     "dictionary), U (the probe run's pointer directions; at the layer fixed in advance only), U_fit "
                     "(refit at the layer on the train-split pairs' h_O by the original bridge's locker-sentence index), "
                     "and outside the orthonormalised union of J++-25, U (U_fit where U is absent) and W_E-25; per R: "
                     "||R^T U||_F^2 / rank(U), the same with U_fit, the principal angles R_lookup vs R_recall per k",
         "U": u_info,
         "routes": ({"design": "x6_routes C2 scenes (another item moved), R_lookup alone written at the bridge word at L; "
                               "the lookup's answer classified identity / position / value / original / other; whole and "
                               "random R beside", "n": n_routes} if routes else "not run (D3)"),
         "arms": arm_names(ks, shuffled), "rule": RULE_D3 if depth else RULE,
         "as_computed": AS_COMPUTED_D3 if depth else AS_COMPUTED,
         "seeds": {"split": SPLIT_SEED, "init": INIT_SEED, "shuffle": SHUFFLE_SEED, "random_R": RAND_SEED,
                   "batches": BATCH_SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "routes_scenes": R.SEED},
         "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's "
                   f"{QUESTION_DEPTH if depth else QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    if (patched := torch_gdn(model.hf)) is not None:
        m["gdn_kernel"] = f"torch reference ({GDN_ENV}=torch; {patched}.torch_chunk_gated_delta_rule replaced)"
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    if (record := torch_mamba(model.hf)) is not None:
        m["mamba_kernel"] = record
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    for p in model.hf.parameters():  # the DAS gradient reaches R only; no weight gradients are stored
        p.requires_grad_(False)
    tok = model.tokenizer
    pairs, info = select_pairs(tok, main_run, main_layer)
    (out / "pairs.json").write_text(json.dumps(info, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", pairs)
    print(json.dumps({k: v for k, v in info.items() if k != "scene_ids"}), flush=True)
    assert pairs, "no pairs"
    for s in ("train", "select", "test"):
        for w in X.READERS:
            assert info["pairs_per_reader_and_split"][READER_NAME[w]][s] > 0, f"{READER_NAME[w]}: no {s} pairs"
    lens = JLens(model, "jpp")
    log_rows: list[dict] = []
    mats_all, readouts_all, u_fits = {}, {}, {}
    for layer in layers:
        got = run_layer(
            model, out, pairs, layer, ks, steps, shuffled, u_np if layer == main_layer else None, lens, log_rows
        )
        mats_all[f"L{layer}"], readouts_all[f"L{layer}"], u_fits[f"L{layer}"] = (
            got["mats"],
            got["readouts"],
            got["u_fit"],
        )
        torch.save({"R": mats_all, "U_fit": {k: torch.tensor(v) for k, v in u_fits.items()},
                    "U": torch.tensor(u_np)}, out / "R.pt")  # tensors only: torch.load's weights_only default  # fmt: skip
        (out / "readouts.json").write_text(json.dumps(readouts_all, indent=2) + "\n")
        X.write_jsonl(out / "train.jsonl", log_rows)
    if routes:  # 5. the routes read: R_lookup alone (every k), whole and random R, on C2 scenes, at L
        dev = model.device
        ws = X.whitespace_mask(model)
        digits = torch.tensor(X.digit_ids(tok), device=dev)
        mats = mats_all[f"L{main_layer}"]
        r_cases, r_info = routes_scenes(model, ws, digits, n_routes)
        m["routes"].update(r_info)
        X.write_jsonl(out / "routes_cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in r_cases])
        r_arms = ["none", "whole", *(f"R_{X.LOOKUP}_k{k}" for k in ks), *(f"rand_k{k}" for k in ks)]
        r_rows = []
        with torch.no_grad():
            for c in progress(r_cases, "routes read (scene)"):
                ids = c["readers"][X.LOOKUP]["ids"]
                h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(main_layer,))[1][main_layer][c["pos"]].float()
                     for v in ("org", "alt")}  # fmt: skip
                dx = (h["alt"] - h["org"])[None]
                edits = [{}] + [{main_layer: AddRows(dx if a == "whole" else ((dx @ mats[a].to(dx.device)) @ mats[a].to(dx.device).T),
                                                     [c["pos"]])} for a in r_arms[1:]]  # fmt: skip
                for w, rd in c["readers"].items():
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                    for a, lg in zip(r_arms, logits, strict=True):
                        top = int(lg.argmax())
                        r_rows.append({"layer": main_layer, "scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a,
                                       "route": R.classify(top, c) if w == X.LOOKUP else None, **X.read_row(lg, rd, digits),
                                       "top_text": tok.decode([top])})  # fmt: skip
        X.write_jsonl(out / "routes.jsonl", r_rows)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- the torch path's check (GPU; batch 52, Lightning) ------------------------------------------------------------


def rel_l2(a, b) -> float:
    """||a - b|| / ||b|| (fp64)."""
    return float((a.double() - b.double()).norm() / b.double().norm().clamp_min(1e-30))


def stage_gradcheck(name: str, why: str, n_items: int = GC_ITEMS) -> Path:
    """Before any DAS on a Mamba-2 model (Dan's 08:55 queue item 3): on the first n_items train pairs of 48.1's pairs
    (both readers' O prompts, 2 x n_items rows), the kernels' forward and the torch path's (kernels_off) agree, and the
    DAS loss's gradient through the torch path is finite. Read without a gradient on both paths: h at L at the bridge
    token (O and S prompts), the read's logits unedited and under the whole change; then on the torch path the DAS loss
    (48.1's: cross-entropy of S's first token at the read, h_O + R R^T Delta, R at k = GC_K, seed GC_SEED) and its
    gradient, timed and with the peak memory, in micro-batches of MICRO; beside: the kernels' gradient (their backward,
    if it runs) and 20 steps of train_subspace through batch_logits with the switch as the runs set it. Writes
    gradcheck.json / gradcheck.md; exits nonzero if a bar fails (the ports depend on this job)."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "the check reads X0's chat prompts: run with BJ_FORMAT unset"
    assert os.environ.get(MAMBA_ENV) == "torch", f"run the check with {MAMBA_ENV}=torch, as the ports"
    target = pins.TARGET
    main_run, layer = MAIN_RUN[target], X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    bars = {"h_rel_l2_max": GC_H_REL, "logit_rel_l2_max": GC_LOGIT_REL,
            "top_token_agree_min": f"{GC_TOP_MIN} of {4 * n_items}", "gradient": "finite and nonzero (torch path)"}  # fmt: skip
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "stage": "gradcheck",
         "main_run": main_run, "layer": layer, "items": f"the first {n_items} train pairs of 48.1's pairs (select_pairs)",
         "k": GC_K, "seed": GC_SEED, "micro_batch": MICRO, "bars": bars,
         "spec": "jobs/c3/x52_lightning_das_gradcheck.yaml", "question": "no prediction: a check of the method"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    model = load_model()
    m["mamba_kernel"] = torch_mamba(model.hf)
    m["experts_implementation"] = getattr(getattr(model.hf, "config", None), "_experts_implementation", None)
    for p in model.hf.parameters():
        p.requires_grad_(False)
    dev = model.device
    pairs, _ = select_pairs(model.tokenizer, main_run, layer)
    items = [p for p in pairs if p["split"] == "train"][:n_items]
    assert len(items) == n_items, f"{len(items)} train pairs, {n_items} wanted"
    rows = [{"scene": it["scene"], "reader": w, "ids": it["readers"][w]["ids"]["org"] + it["space"], "pos": it["pos"],
             "target": it["readers"][w]["tok_b"], "item": i} for i, it in enumerate(items) for w in X.READERS]  # fmt: skip

    def states() -> dict[str, Any]:
        with torch.no_grad():
            h = {v: torch.stack([model.run(torch.tensor([it["readers"][X.LOOKUP]["ids"][v]], device=dev), record=(layer,))[1]
                                 [layer][it["pos"]].float() for it in items]) for v in ("org", "alt")}  # fmt: skip
        return h

    def reads(delta) -> dict[str, Any]:
        out_: dict[str, Any] = {}
        with torch.no_grad():
            for arm in ("none", "whole"):
                lg = []
                for s in range(0, len(rows), MICRO):
                    ch = rows[s : s + MICRO]
                    adds = torch.stack([delta[r["item"]] for r in ch]) * (arm == "whole")
                    lg.append(batch_logits(model, layer, [r["ids"] for r in ch], [r["pos"] for r in ch], adds))
                out_[arm] = torch.cat(lg)
        return out_

    def timed(fn):
        torch.cuda.synchronize()
        t0 = time.time()
        val = fn()
        torch.cuda.synchronize()
        return val, time.time() - t0

    h_k, t_hk = timed(states)  # the kernels (as loaded)
    delta = (h_k["alt"] - h_k["org"]).to(dev)
    lg_k, t_lk = timed(lambda: reads(delta))
    with kernels_off(model.hf) as refs:
        h_t, t_ht = timed(states)
        lg_t, t_lt = timed(lambda: reads(delta))
    fwd = {"h_O": [rel_l2(h_t["org"][i], h_k["org"][i]) for i in range(n_items)],
           "h_S": [rel_l2(h_t["alt"][i], h_k["alt"][i]) for i in range(n_items)],
           "h_max_abs": float(max((h_t[v] - h_k[v]).abs().max() for v in ("org", "alt"))),
           "logits": {a: [rel_l2(lg_t[a][j], lg_k[a][j]) for j in range(len(rows))] for a in lg_k},
           "logits_max_abs": {a: float((lg_t[a] - lg_k[a]).abs().max()) for a in lg_k},
           "top_agree": {a: int((lg_t[a].argmax(-1) == lg_k[a].argmax(-1)).sum()) for a in lg_k},
           "torch_references": refs,
           "seconds": {"kernel_states": t_hk, "kernel_reads": t_lk, "torch_states": t_ht, "torch_reads": t_lt}}  # fmt: skip

    def das_grad(path: str) -> dict[str, Any]:
        """The DAS loss and its gradient w.r.t. R itself (a leaf: random_basis(d, GC_K, GC_SEED); not the orthogonal
        parametrisation's `original`, whose basis is completed with the unseeded global RNG, so its gradient's
        direction differs between two modules of one seed), over the rows in micro-batches of MICRO, on the given path;
        seconds per micro-batch and the peak memory beside."""
        r_leaf = random_basis(delta.shape[1], GC_K, GC_SEED).to(dev).requires_grad_()
        tgt_all = torch.tensor([r["target"] for r in rows], device=dev)
        torch.cuda.reset_peak_memory_stats()
        ctx = kernels_off(model.hf) if path == "torch" else contextlib.nullcontext()
        old = os.environ.pop(MAMBA_ENV)  # batch_logits must not switch on its own here: the path is set by ctx
        loss_sum, secs = 0.0, []
        try:
            with ctx:
                for s in range(0, len(rows), MICRO):
                    ch = rows[s : s + MICRO]
                    d_ch = torch.stack([delta[r["item"]] for r in ch]).float()
                    adds = (d_ch @ r_leaf) @ r_leaf.T
                    torch.cuda.synchronize()
                    t0 = time.time()
                    lg = batch_logits(model, layer, [r["ids"] for r in ch], [r["pos"] for r in ch], adds)
                    loss = torch.nn.functional.cross_entropy(lg, tgt_all[s : s + len(ch)], reduction="sum") / len(rows)
                    loss.backward()
                    torch.cuda.synchronize()
                    secs.append(time.time() - t0)
                    loss_sum += float(loss.detach())
        finally:
            os.environ[MAMBA_ENV] = old
        assert r_leaf.grad is not None, "no gradient reached R"
        g = r_leaf.grad.flatten()
        return {"loss": loss_sum, "grad": g.detach().double().cpu(), "finite": bool(torch.isfinite(g).all()),
                "grad_norm": float(g.double().norm()), "seconds_per_micro_batch": secs,
                "peak_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2)}  # fmt: skip

    g_t = das_grad("torch")
    tlog: list[dict] = []
    lookup_rows = [{**r, "delta": delta[r["item"]].cpu()} for r in rows if r["reader"] == X.LOOKUP]
    t0 = time.time()
    train_subspace(
        model, layer, lookup_rows, GC_K, GC_SEED, steps=GC_STEPS, log=tlog, desc="train_subspace (torch path)"
    )
    t_train = time.time() - t0
    n_reads = 2 * len(rows)
    ok = {"h": max(fwd["h_O"] + fwd["h_S"]) <= GC_H_REL + EPS,
          "logits": max(fwd["logits"]["none"] + fwd["logits"]["whole"]) <= GC_LOGIT_REL + EPS,
          "top": sum(fwd["top_agree"].values()) >= GC_TOP_MIN,
          "gradient": g_t["finite"] and g_t["grad_norm"] > 0 and all(math.isfinite(r["loss"]) for r in tlog)}  # fmt: skip
    res = {"pass": all(ok.values()), "checks": ok, "bars": bars, "n_items": n_items, "rows": len(rows), "reads": n_reads,
           "layer": layer, "forward": fwd, "torch_grad": {k: v for k, v in g_t.items() if k != "grad"},
           "kernel_grad": "not run yet", "train_subspace": {"steps": GC_STEPS, "log": tlog, "seconds": t_train,
                                                            "seconds_per_step": t_train / GC_STEPS},
           "scenes": [it["scene"] for it in items]}  # fmt: skip

    def write() -> None:
        (out / "gradcheck.json").write_text(json.dumps(res, indent=1) + "\n")
        tg = res["torch_grad"]
        lines = [f"# DAS gradient check on {target} at L{layer} ({name}): {'PASS' if res['pass'] else 'FAIL'}", "",
                 f"{n_items} items (the first train pairs of 48.1's pairs from {main_run}), both readers: {len(rows)} "
                 f"rows, {n_reads} reads per path. Kernels = the pinned HF-hub kernels as loaded; torch = kernels_off "
                 f"(transformers' torch reference: {', '.join(refs)}). Bars fixed with the spec. UNVERIFIED.", "",
                 "| check | value | bar | ok |", "|---|---|---|---|",
                 f"| h at L (bridge token, O and S), relative L2, max over items | {max(fwd['h_O'] + fwd['h_S']):.2e} | "
                 f"<= {GC_H_REL} | {ok['h']} |",
                 f"| read logits (unedited, whole change), relative L2, max over rows | "
                 f"{max(fwd['logits']['none'] + fwd['logits']['whole']):.2e} | <= {GC_LOGIT_REL} | {ok['logits']} |",
                 f"| read top token, torch = kernels | {sum(fwd['top_agree'].values())} of {n_reads} | >= {GC_TOP_MIN} | "
                 f"{ok['top']} |",
                 f"| DAS loss gradient (torch path) | finite {tg['finite']}, norm {tg['grad_norm']:.3e} | finite, > 0 | "
                 f"{ok['gradient']} |", "",
                 f"Beside: h max abs diff {fwd['h_max_abs']:.3e}; logits max abs diff {fwd['logits_max_abs']}; torch "
                 f"path {statistics.mean(tg['seconds_per_micro_batch']):.2f} s per micro-batch of {MICRO} (forward + "
                 f"backward), peak {tg['peak_gb']} GB; train_subspace {GC_STEPS} steps in {t_train:.0f} s, loss log "
                 f"{json.dumps(tlog)}; forward seconds {json.dumps(fwd['seconds'])}; the kernels' own gradient (their "
                 f"backward, not used by the runs) vs the torch path's: {json.dumps(res['kernel_grad'])}."]  # fmt: skip
        (out / "gradcheck.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines), flush=True)

    write()
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    try:  # last and beside, never a bar: the kernels' backward is what the switch avoids (a fault here ends nothing)
        g_k = das_grad("kernel")
        res["kernel_grad"] = {
            "loss": g_k["loss"], "finite": g_k["finite"], "grad_norm": g_k["grad_norm"],
            "cos_with_torch": float(torch.nn.functional.cosine_similarity(g_k["grad"], g_t["grad"], dim=0)),
            "rel_l2_vs_torch": rel_l2(g_k["grad"], g_t["grad"]),
            "seconds_per_micro_batch": g_k["seconds_per_micro_batch"], "peak_gb": g_k["peak_gb"]}  # fmt: skip
    except Exception as e:
        res["kernel_grad"] = {"error": f"{type(e).__name__}: {e}"[:500]}
    write()
    if not res["pass"]:
        raise SystemExit(f"gradcheck FAILED: {ok}")
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(question: str = QUESTION, rev: str = "HEAD") -> str:
    """Dan's committed answer to a question (the 'Dan:' line of its block in the predictions file at `rev`), '' if
    none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{question}**" not in text:
        return ""
    block = text.split(f"**{question}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def ci_of(values: list, entities: list[str], n_boot: int, key: str = "v") -> list[float]:
    """[mean, lo, hi]: the mean of per-pair values (0/1 or shares) with X0's cluster bootstrap over the bridge
    entities (resampled_rates: the resample's mean of the values)."""
    if not values:
        return [math.nan, math.nan, math.nan]
    r = X.resampled_rates({key: list(values)}, entities, n_boot)
    return [float(np.mean(values)), *X.interval(r[key])]


def paired_ci(a: list, b: list, entities: list[str], n_boot: int) -> list[float]:
    """[mean(a - b), lo, hi]: the paired cluster bootstrap of the per-pair difference."""
    r = X.resampled_rates({"a": list(a), "b": list(b)}, entities, n_boot)
    return [float(np.mean(a) - np.mean(b)), *X.interval(r["a"] - r["b"])]


def reader_table(rows: list[dict], reader: str, split: str) -> tuple[list[str], list[str], dict[str, list[int]]]:
    """The reader's pairs of a split (the pairs the stored whole change switches for it, in row order), their entities
    and each arm's 0/1 switch per pair; every pair must have every arm."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader and r["split"] == split and r["in_pairs"]:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["switched"])
    scenes = list(entity)
    arms = sorted({a for _, a in by})
    missing = [(s, a) for s in scenes for a in arms if (s, a) not in by]
    assert not missing, f"{reader} {split}: {len(missing)} pair-arm reads missing, e.g. {missing[:3]}"
    return scenes, [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in arms}


def chosen_k(select_iia: dict[int, float], ks: tuple[int, ...] = KS) -> int:
    """The smallest k <= K_LOW whose select-split own-IIA >= OWN_IIA; else the k with the highest select own-IIA."""
    for k in sorted(ks):
        if k <= K_LOW and select_iia[k] >= OWN_IIA - EPS:
            return k
    return max(sorted(ks), key=lambda k: (select_iia[k], -k))


def layer_numbers(src: Path, layer: int, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One run's numbers at one layer: per reader the select own-IIA by k and the chosen k; on the test pairs own-IIA
    by k, the random (and shuffled) baselines, cross-IIA at the other reader's chosen k, own minus cross (paired), IIA /
    S_whole; the geometry means over the test pairs per R; the per-R readouts."""
    m = json.loads((src / "manifest.json").read_text())
    ks = tuple(m["ks"])
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["layer"] == layer]
    assert rows, f"{src.name}: no outcomes at layer {layer}"
    geo = [g for g in X.read_jsonl(src / "geometry.jsonl") if g["layer"] == layer]
    readouts = json.loads((src / "readouts.json").read_text())[f"L{layer}"]
    readers: dict[str, Any] = {}
    for w in X.READERS:
        _, ent_s, sw_s = reader_table(rows, w, "select")
        sel = {k: float(np.mean(sw_s[f"R_{w}_k{k}"])) for k in ks}
        readers[w] = {"select": {"n": len(ent_s), "entities": len(set(ent_s)), "own_iia": {k: round(v, 4) for k, v in sel.items()},
                                 "S_whole": round(float(np.mean(sw_s["whole"])), 4)}, "k": chosen_k(sel, ks)}  # fmt: skip
    for w in X.READERS:
        other = X.RECALL if w == X.LOOKUP else X.LOOKUP
        scenes, ent, sw = reader_table(rows, w, "test")
        k_star, k_other = readers[w]["k"], readers[other]["k"]
        own = {k: ci_of(sw[f"R_{w}_k{k}"], ent, n_boot) for k in ks}
        s_whole = float(np.mean(sw["whole"]))
        shuf = {k: ci_of(sw[f"shuf_{w}_k{k}"], ent, n_boot) for k in ks if f"shuf_{w}_k{k}" in sw}
        readers[w]["test"] = {
            "n": len(scenes), "entities": len(set(ent)), "scenes": scenes, "S_whole_rerun": round(s_whole, 4),
            "S_none": round(float(np.mean(sw["none"])), 4),
            "own_iia": {k: own[k] for k in ks},
            "own_over_whole": {k: (own[k][0] / s_whole if s_whole > 0 else None) for k in ks},
            "random_iia": {k: ci_of(sw[f"rand_k{k}"], ent, n_boot) for k in ks},
            "shuffled_iia": shuf or None,
            "cross_iia": ci_of(sw[f"R_{other}_k{k_other}"], ent, n_boot), "cross_R": f"R_{other}_k{k_other}",
            "own_minus_cross": paired_ci(sw[f"R_{w}_k{k_star}"], sw[f"R_{other}_k{k_other}"], ent, n_boot),
            "own_at_k": own[k_star], "own_at_k64": own.get(64),
        }  # fmt: skip
    test_geo = [g for g in geo if g["split"] == "test"]
    geometry: dict[str, Any] = {}
    for key in sorted({g["R"] for g in test_geo}):
        mine = [g for g in test_geo if g["R"] == key]
        geometry[key] = {"n": len(mine), "cos2_U": readouts[key]["cos2_U"], "cos2_Ufit": readouts[key]["cos2_Ufit"],
                         "k_over_d": readouts[key]["random_expectation_cos2_U"]}  # fmt: skip
        for what in ("energy", "in_jpp25", "in_jpp100", "in_we25", "in_U", "in_Ufit", "outside_union"):
            kept = [g for g in mine if g.get(what) is not None]
            vals = [g[what] for g in kept]
            geometry[key][what] = ci_of(vals, [g["entity"] for g in kept], n_boot)
            geometry[key][f"{what}_median"] = round(statistics.median(vals), 4) if vals else None
    return {"layer": layer, "ks": list(ks), "d": readouts["d"], "rank_U": readouts["rank_U"], "rank_Ufit": readouts["rank_Ufit"],
            "U_vs_Ufit_cos2": readouts["U_vs_Ufit_cos2"], "readers": readers, "geometry": geometry,
            "principal_angles_deg": readouts["principal_angles_deg"]}  # fmt: skip


def model_numbers(src: Path, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One 48.1 run's numbers at its layer fixed in advance, with the routes shares."""
    m = json.loads((src / "manifest.json").read_text())
    num = layer_numbers(src, m["layer"], n_boot)
    routes = X.read_jsonl(src / "routes.jsonl")
    routes_out: dict[str, Any] = {}
    for a in sorted({r["arm"] for r in routes}):
        lk = [r for r in routes if r["arm"] == a and r["reader"] == X.LOOKUP]
        rc = [r for r in routes if r["arm"] == a and r["reader"] == X.RECALL]
        ent = [r["entity"] for r in lk]
        routes_out[a] = {"n": len(lk),
                         **{rt: ci_of([int(r["route"] == rt) for r in lk], ent, n_boot) for rt in
                            ("identity", "position", "value", "original", "other")},
                         "recall_switch": round(float(np.mean([r["switched"] for r in rc])), 4) if rc else None}  # fmt: skip
    return {"target": m["model"]["target"], "main_run": m["main_run"], **num, "routes": routes_out,
            "pairs": {k: v for k, v in json.loads((src / "pairs.json").read_text()).items() if k != "scene_ids"}}  # fmt: skip


def rules(num: dict[str, Any]) -> dict[str, Any]:
    """Rules (a)-(d) and the fallback of 48.1 on one model's numbers (point estimates at the bars, EPS; the CI clause of
    (a) as the as-computed paragraph reads it), and the not-selective flag per R."""
    lk, rc = num["readers"][X.LOOKUP], num["readers"][X.RECALL]
    k_l, k_r = lk["k"], rc["k"]
    g = num["geometry"]
    r_l, r_r, rand_r = f"R_{X.LOOKUP}_k{k_l}", f"R_{X.RECALL}_k{k_r}", f"rand_k{k_r}"
    own_ok = {w: (num["readers"][w]["k"] <= K_LOW and num["readers"][w]["test"]["own_at_k"][0] >= OWN_IIA - EPS)
              for w in X.READERS}  # fmt: skip
    cross_ok = {w: (num["readers"][w]["test"]["cross_iia"][0] <= CROSS_IIA + EPS
                    and num["readers"][w]["test"]["own_minus_cross"][1] > 0) for w in X.READERS}  # fmt: skip
    a = all(own_ok.values()) and all(cross_ok.values())
    b = (g[r_r]["in_jpp25"][0] >= LENS_RECALL - EPS and g[rand_r]["in_jpp25"][0] <= LENS_RANDOM + EPS
         and g[r_l]["in_jpp25"][0] <= LENS_LOOKUP + EPS)  # fmt: skip
    cos2 = g[r_l]["cos2_U"]
    c = cos2 is not None and cos2 >= ADDRESS - EPS
    routes_id = num["routes"].get(r_l, {}).get("identity", [math.nan])[0]
    d = (g[r_l]["outside_union"][0] >= OUTSIDE - EPS and lk["test"]["own_at_k"][0] >= OWN_IIA - EPS
         and routes_id >= ROUTES_IDENTITY - EPS)  # fmt: skip
    at64 = lk["test"]["own_at_k64"]
    fallback = at64 is not None and at64[0] < NO_MEDIATOR
    not_selective = {key: v["energy"][0] >= NOT_SELECTIVE - EPS for key, v in g.items()}
    return {"a": bool(a), "b": bool(b), "c": bool(c), "d": bool(d),
            "fallback_no_low_dimensional_mediator": bool(fallback),
            "detail": {"own_ok": {READER_NAME[w]: bool(v) for w, v in own_ok.items()},
                       "cross_ok": {READER_NAME[w]: bool(v) for w, v in cross_ok.items()},
                       "chosen_k": {READER_NAME[X.LOOKUP]: k_l, READER_NAME[X.RECALL]: k_r},
                       "R_recall_in_jpp25": g[r_r]["in_jpp25"][0], "random_in_jpp25": g[rand_r]["in_jpp25"][0],
                       "R_lookup_in_jpp25": g[r_l]["in_jpp25"][0], "R_lookup_cos2_U": cos2,
                       "R_lookup_outside_union": g[r_l]["outside_union"][0], "R_lookup_own_iia": lk["test"]["own_at_k"][0],
                       "R_lookup_routes_identity": routes_id, "lookup_own_iia_k64": None if at64 is None else at64[0]},
            "not_selective": {key: bool(v) for key, v in not_selective.items() if v}}  # fmt: skip


def rules_d3(by_layer: dict[int, dict[str, Any]], main_layer: int) -> dict[str, Any]:
    """D3's rule on the per-layer numbers {layer: layer_numbers(...)} (point estimates, EPS): the lookup's subspace
    leaves the lens with depth; the recall's stays (not tested when its IIA reaches 0.6 at no layer)."""
    half = main_layer // 2

    def at(layer: int, w: str) -> tuple[float, float]:
        r = by_layer[layer]["readers"][w]
        return by_layer[layer]["geometry"][f"R_{w}_k{r['k']}"]["in_jpp25"][0], r["test"]["own_at_k"][0]

    lk = {la: at(la, X.LOOKUP) for la in by_layer}
    rc = {la: at(la, X.RECALL) for la in by_layer}
    have = half in by_layer and main_layer in by_layer
    leaves = (have and lk[half][0] >= D3_HALF - EPS and lk[main_layer][0] <= D3_L + EPS
              and lk[half][1] >= D3_IIA - EPS and lk[main_layer][1] >= D3_IIA - EPS)  # fmt: skip
    tested = [la for la in by_layer if rc[la][1] >= D3_IIA - EPS]
    stays = bool(tested) and all(rc[la][0] >= D3_STAYS - EPS for la in tested)
    return {"leaves_the_lens": bool(leaves), "leaves_tested": bool(have), "recall_stays": stays,
            "recall_tested_layers": sorted(tested), "L": main_layer, "L_half": half,
            "lookup": {la: {"in_jpp25": v[0], "own_iia": v[1]} for la, v in sorted(lk.items())},
            "recall": {la: {"in_jpp25": v[0], "own_iia": v[1]} for la, v in sorted(rc.items())}}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def example_lines(src: Path, layer: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view: k random test pairs (seed 0), each reader's O prompt with the bridge word marked, S's
    context, and every arm's top token with its switch flag at the layer."""
    items = [it for it in X.read_jsonl(src / "cases.jsonl") if it["split"] == "test"]
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["layer"] == layer]
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    pick = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    lines = [f"## {src.name} at L{layer}: {len(pick)} random test pairs of {len(items)} (seed {seed})", ""]
    for i in pick:
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} → {it['cf_bridge']}; the whole change "
                  f"switches: lookup {it['stored_whole'][X.LOOKUP]}, recall {it['stored_whole'][X.RECALL]} (stored)", "",
                  f"S's context: {it['cf_context']}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}; "
                      f"in this reader's pairs: {it['stored_whole'][w]}", "", "```", marked_prompt(it, w), "```", "",
                      "| arm | top token | switched | right |", "|---|---|---|---|"]  # fmt: skip
            for a in arms:
                r = reads.get((it["scene"], w, a))
                if r is not None:
                    lines.append(f"| {a} | {r['top_text']!r} | {r['switched']} | {r['right']} |")
            lines.append("")
    return lines


def layer_lines(num: dict[str, Any], label: str) -> list[str]:
    """The tables of one layer's numbers (IIA by k, cross, geometry, angles)."""
    lines = [f"{label}: d = {num['d']}, rank U = {num['rank_U']}, rank U_fit = {num['rank_Ufit']} (U vs U_fit mean cos² "
             f"{num['U_vs_Ufit_cos2']}).", "",
             "| reader | k | select own-IIA | test own-IIA | random R | shuffled R | own / S_whole |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in X.READERS:
        r = num["readers"][w]
        for k in num["ks"]:
            star = " (chosen)" if k == r["k"] else ""
            ow = r["test"]["own_over_whole"][k]
            sh = r["test"]["shuffled_iia"]
            lines.append(f"| {READER_NAME[w]} | {k}{star} | {r['select']['own_iia'][k]:.2f} | {fmt(r['test']['own_iia'][k])} | "
                         f"{fmt(r['test']['random_iia'][k])} | {fmt(sh[k]) if sh else '-'} | "
                         f"{'-' if ow is None else f'{ow:.2f}'} |")  # fmt: skip
    lines += ["", "| reader | test n (entities) | S_whole rerun | cross-IIA (the other reader's R) | own − cross (paired) |",
              "|---|---|---|---|---|"]  # fmt: skip
    for w in X.READERS:
        t = num["readers"][w]["test"]
        lines.append(f"| {READER_NAME[w]} | {t['n']} ({t['entities']}) | {t['S_whole_rerun']:.2f} | {fmt(t['cross_iia'])} "
                     f"({t['cross_R']}) | {fmt(t['own_minus_cross'])} |")  # fmt: skip
    lines += ["", "Geometry on the test pairs (means [CI]; the energy's median in brackets):", "",
              "| R | energy | in J++-25 | in J++-100 | in W_E-25 | in U | in U_fit | outside (J++-25 ∪ U ∪ W_E-25) | cos² U (k/d) | cos² U_fit |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, g in num["geometry"].items():
        cu = "-" if g["cos2_U"] is None else f"{g['cos2_U']:.4f}"
        lines.append(f"| {key} | {fmt(g['energy'])} [{g['energy_median']}] | {fmt(g['in_jpp25'])} | {fmt(g['in_jpp100'])} | "
                     f"{fmt(g['in_we25'])} | {fmt(g['in_U'])} | {fmt(g['in_Ufit'])} | {fmt(g['outside_union'])} | "
                     f"{cu} ({g['k_over_d']:.4f}) | {g['cos2_Ufit']:.4f} |")  # fmt: skip
    lines += ["", "Principal angles R_lookup vs R_recall (degrees): " + "; ".join(
        f"{k}: {a}" for k, a in num["principal_angles_deg"].items()), ""]  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """48.1's verdict (sealed until Q48.1), or with coverage (batch 52 C) the same rules on the coverage runs: no seal
    guard, "no prediction" in place of Dan's answer, written to x52_das-<UTC>/."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else dan_answer(QUESTION)
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    if coverage:
        names = {**RUNS, **COVERAGE_RUNS}
        targets = [json.loads((RESULTS / r / "manifest.json").read_text())["model"]["target"] if
                   (RESULTS / r / "manifest.json").exists() else {v: k for k, v in names.items()}.get(r) for r in runs]  # fmt: skip
        assert set(targets) <= set(COVERAGE_RUNS), f"48.1 coverage runs on {sorted(COVERAGE_RUNS)}, not {targets}"
    out = RESULTS / f"{'x52_das' if coverage else 'verdict'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    models = []
    lines = ["# 48.1: DAS at the bridge word, two readers, two subspaces?", "",
             f"Batch 48, test 48.1 (jobs/c3/batch48.yaml; {QUESTION}, Dan: {answer}). Pairs: the main test's locker-first "
             "scenes the whole change switches (per reader); split by bridge entity 60 / 20 / 20; k chosen on the select "
             f"split, every number read on the test entities' pairs; cluster bootstrap over bridge entities ({n_boot}, "
             f"seed {X.BOOT_SEED}). UNVERIFIED.", "", f"As computed: {AS_COMPUTED}.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        num = model_numbers(src, n_boot)
        v = rules(num)
        models.append({"run": run, **num, "rules": v})
        lines += [f"## {num['target']} ({run}, L{num['layer']}): (a) {'yes' if v['a'] else 'no'}, (b) {'yes' if v['b'] else 'no'}, "
                  f"(c) {'yes' if v['c'] else 'no'}, (d) {'yes' if v['d'] else 'no'}"
                  + ("; FALLBACK: no low-dimensional mediator at this token and layer (the lookup's own-IIA < 0.5 at k = 64)"
                     if v["fallback_no_low_dimensional_mediator"] else "")
                  + (f"; not selective (energy >= 0.8 of Delta): {', '.join(sorted(v['not_selective']))}" if v["not_selective"] else ""),
                  "", f"Pairs: {num['pairs']['pairs']} ({num['pairs']['entities']} entities; per reader and split "
                  f"{num['pairs']['pairs_per_reader_and_split']}).", ""]  # fmt: skip
        lines += layer_lines(num, f"Layer {num['layer']}")
        lines += ["Routes read (C2 scenes, the lookup's answer classified; the recall's switch beside):", "",
                  "| arm | n | identity | position | value | original | other | recall switch |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for a, r in num["routes"].items():
            lines.append(f"| {a} | {r['n']} | {fmt(r['identity'])} | {fmt(r['position'])} | {fmt(r['value'])} | "
                         f"{fmt(r['original'])} | {fmt(r['other'])} | {r['recall_switch']} |")  # fmt: skip
        lines += ["", f"Rule detail: {json.dumps(v['detail'])}", ""]
    lines += ["Rules (fixed in advance): " + "; ".join(f"({k}) {t}" for k, t in RULE.items()) + "."]
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ") for ln in lines]
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    ex = ["# 48.1 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word where "
          "R R^T Delta is added at L. UNVERIFIED.", ""]  # fmt: skip
    for mdl in models:
        ex += example_lines(RESULTS / mdl["run"], mdl["layer"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_depth(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    """D3: the per-layer numbers over the runs (48.1's for L, the D3 runs' for the other layers; one target), D3's rule."""
    answer = dan_answer(QUESTION_DEPTH)
    assert answer, (
        f"sealed: {PREDICTIONS} has no committed answer to {QUESTION_DEPTH} (its 'Dan:' line is empty at HEAD)"
    )
    by_layer: dict[int, dict[str, Any]] = {}
    targets, source = set(), {}
    for run in runs:
        src = RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        targets.add(m["model"]["target"])
        for layer in m["layers"]:
            assert layer not in by_layer, f"layer {layer} in two runs ({source[layer]}, {run})"
            by_layer[layer] = layer_numbers(src, layer, n_boot)
            source[layer] = run
    assert len(targets) == 1, f"one target per depth verdict: {sorted(targets)}"
    target = targets.pop()
    main_layer = X.PREDICTED[target]
    v = rules_d3(by_layer, main_layer)
    out = RESULTS / f"depth-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# D3: DAS at four layers (batch 47, amendment 3)", "",
             f"{target}: runs {', '.join(runs)}; {QUESTION_DEPTH}, Dan: {answer}. Layers {sorted(by_layer)} (L = {main_layer}, "
             f"L/2 = {main_layer // 2}); cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"As computed: {AS_COMPUTED_D3}.", "",
             f"**The lookup's subspace leaves the lens with depth: {'yes' if v['leaves_the_lens'] else 'no'}"
             f"{'' if v['leaves_tested'] else ' (not tested: L/2 or L missing)'}; the recall's stays: "
             f"{'yes' if v['recall_stays'] else 'no'}{'' if v['recall_tested_layers'] else ' (not tested: the recall reaches IIA 0.6 at no layer)'}"
             f"** (recall layers tested: {v['recall_tested_layers']}).", "",
             "| layer | run | reader | chosen k | test own-IIA | cross-IIA | energy in J++-25 (own R) | random R in J++-25 | cos² U_fit (k/d) | cos² U (probe) |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for layer in sorted(by_layer):
        num = by_layer[layer]
        for w in X.READERS:
            r = num["readers"][w]
            g = num["geometry"][f"R_{w}_k{r['k']}"]
            rnd = num["geometry"][f"rand_k{r['k']}"]
            lines.append(f"| {layer} | {source[layer]} | {READER_NAME[w]} | {r['k']} | {fmt(r['test']['own_at_k'])} | "
                         f"{fmt(r['test']['cross_iia'])} | {fmt(g['in_jpp25'])} | {fmt(rnd['in_jpp25'])} | "
                         f"{g['cos2_Ufit']:.4f} ({g['k_over_d']:.4f}) | {'-' if g['cos2_U'] is None else f'{g['cos2_U']:.4f}'} |")  # fmt: skip
    lines.append("")
    for layer in sorted(by_layer):
        lines += layer_lines(by_layer[layer], f"## Layer {layer} ({source[layer]})")
    lines += [f"Rule (fixed in advance, jobs/c3/batch47.yaml D3): {RULE_D3}.", f"Detail: {json.dumps(v)}"]
    (out / "depth.json").write_text(json.dumps({"runs": runs, "dan": answer, "target": target, "rule": v,
                                                "layers": {str(k): val for k, val in by_layer.items()}}, indent=1) + "\n")  # fmt: skip
    (out / "depth.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "depth", "gradcheck"])
    ap.add_argument("--name", help="run: the run name (results/x48_das/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the 48.1 runs; depth: 48.1's and the D3 runs")
    ap.add_argument("--why", default="batch 48, test 48.1 (jobs/c3/batch48.yaml; Q48.1)")
    ap.add_argument(
        "--layers", nargs="+", type=int, default=None, help="run: the layers (default: the layer fixed in advance)"
    )
    ap.add_argument("--depth", action="store_true", help="run: D3 (no shuffled baselines, no routes read)")
    ap.add_argument("--steps", type=int, default=STEPS)
    ap.add_argument("--n-routes", type=int, default=N_ROUTES)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true",
                    help=f"verdict: batch 52 coverage runs (default {COVERAGE_RUNS['qwen3.6-27b']}; any of {list(COVERAGE_RUNS.values())} by --runs; '{NO_PREDICTION}')")  # fmt: skip
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, layers=tuple(a.layers) if a.layers else None, depth=a.depth, steps=a.steps,
                  n_routes=a.n_routes)  # fmt: skip
    elif a.stage == "verdict":
        # --coverage without --runs: the 27B's run, as before Lightning's (its job names its run)
        default = [COVERAGE_RUNS["qwen3.6-27b"]] if a.coverage else [RUNS["qwen3.5-9b"], RUNS["muse-glimmer-30b"]]
        stage_verdict(a.runs or default, a.n_boot, a.coverage)
    elif a.stage == "gradcheck":
        stage_gradcheck(a.name or GRADCHECK_RUN, a.why)
    else:
        stage_depth(a.runs or DEPTH_RUNS["qwen3.5-9b"], a.n_boot)


if __name__ == "__main__":
    main()
