"""x47_anatomy (batch 47, test 47.8, amendment 2; jobs/c3/batch47.yaml, design and rules (a)-(e) fixed in advance; Q47.8
in predictions/2026-10-28_dan.md): layer anatomy of the switch. As depth increases, what does a change at the bridge word
move, and through which part: the lens-readable identity (J++), the identity outside the lens (I), the address (U), or
nothing?

Scenes: x6_routes' generator (seed 2510), locker-first by construction, conditions C2 (another item moved: Iris's pick
B, B's and C's locker sentences swapped, B's digit new) and C0 (the sanity swap: Iris picks B, nothing else moves); X0's
competence gate (0.80 per reader on unedited scenes) and eligibility (both readers say and read O's and S's answers
right). The eligible C2 scenes are split by bridge entity (the O bridge, X0's cluster) into a test half and a fit half:
the entities in a seeded order (SPLIT_SEED) go to the test half until it holds N_TEST scenes, the rest to the fit half
(at least N_FIT_MIN scenes, else the run stops). C0's test scenes are the test scenes' own base scenes.

Per layer l of the model's sweep (LAYERS: 9B every 2nd L2-L30, Muse every 4th L2-L50, 27B every 4th L4-L60), from one
forward of O and one of S per scene recording every sweep layer at the bridge word:
  fit half   layout-free residuals (x0_massmean: each layout group's mean taken out; layout = x0_probe.layout); the slot
             class means (the O bridge's locker slot, 0-2) and U_l = their mass-mean basis (rank classes - 1 = 2 with
             three lockers: the spec's "rank 4" is not reachable in routes scenes, reported as the rank); the entity
             class means over the O states (entity = the O bridge) and the S states (entity = the S bridge; both, so a
             test entity held out of the fit half's O bridges still has a mean) and Id_l = their mass-mean basis;
             probes (x0_probe (a) answer digit, (b) slot, (c) bridge identity; entities held out by x0_probe's folds) on
             the O states; the refit's held-out accuracy on the test half (slot by the nearest slot mean in U_l, entity
             by the nearest entity mean in Id_l); the lens's top-10 rate (the bridge token among the layer-l J++
             readout's top 10 at the bridge word; an in-job proxy for the lens check's pass@10, not jpp_lens's).
  test half  Delta_l = h_S - h_O at the bridge word. Parts: J = the signed-OMP part on 25 atoms of the layer-l J++ lens
             (X.fit, letter tokens); U = the projection on U_l; I = the rank-1 part along mu_S-bridge - mu_O-bridge
             orthogonalised against the scene's 25 atoms (x6_routes.identity_dirs' "idout"; a scene whose entity has no
             fit-half mean keeps a zero I part and is left out of the I arms' cells). Also W_E's 25-atom part (input
             embeddings) and its overlap with J (D4). Random parts of the same share per scene: for J, random lens atoms
             (a seeded permutation of the layer's lens atoms, orthonormalised, the leading ones up to the share, as
             statement_positions.random_subspace_part picks them; seed 777 + l); for U and I, X0's random subspace (seed
             888 + l).
Arms per layer, the test half, both readers (X0's chat read): none; whole; keep_J, keep_U, keep_I (only that part added);
no_J, no_U, no_I (the change minus the part); each keep and no arm paired with its random part (keep_X_rand,
no_X_rand). C0 scenes: none and whole only. Lookup answers classified identity / position / value / original / other
(x6_routes.classify); recall answers changed item / original item / the item at the target slot (C) / other.

SEALED: the run writes per-item outcomes, norms, the fit record and the cache (fit-half states fp16 per layer, the
locker-sentence item and number tokens every CACHE_STEP layers, U_l / Id_l / class means) and no verdict. verdict, view
and figures refuse until predictions/2026-10-28_dan.md holds Dan's committed Q47.8 answer at HEAD. The rule (verdict):
per model, over the test half, cluster bootstrap over bridge entities (10,000, seed 0); a reader's layer is "not
interpretable" where the whole change switches < 0.30 of it (lookup switch = the answer moved to identity, position or
value; recall switch = the changed item's answer). l_J = the first layer from which the lookup's extra loss without J
(Jdep - Rdep, X.cell) stays <= 0.10 at every later interpretable layer; l_P = the first interpretable layer where the
position share under the whole change >= 0.20; l_probe = the first layer where the slot probe >= 0.80. (a) handoff:
l_P >= l_J, gap l_P - l_J; (b) l_probe <= l_P; (c) identity with keep_J >= 0.5 at the earliest interpretable layer and
<= 0.1 at L, identity with keep_I >= 0.3 at L, on >= 2 of 3 models, with the crossing layer; (d) value <= 0.05 at every
interpretable layer; (e) the recall window (whole switch >= 0.5) and whether no_J's extra loss >= 0.3 throughout it,
with the recall's own onset layer. EPS 1e-9 at every bar.

uv run python scripts/x47_anatomy.py plan                                                  # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_anatomy.py run --name qwen35_9b_x47_anatomy # GPU (sealed)
uv run python scripts/x47_anatomy.py preview                                               # CPU, the figure on Fig 6's runs
uv run python scripts/x47_anatomy.py verdict | view                                        # CPU, after Dan's Q47.8
uv run python scripts/x47_anatomy.py figures --verdict results/x47_anatomy/x47_8-<UTC>
"""

from __future__ import annotations

import argparse
import collections
import json
import math
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_probe as PR
from scripts import x6_routes as R

EXP = "x47_anatomy"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.8"
RENDERING = "chat"
# Lightning (batch 52 C coverage, amendment 3): Muse's design for a 52-block model, verbatim (every 4th layer L2-L50,
# which holds the committed L14; 200 test scenes; C0 >= 0.5, no one-pick reference)
LAYERS = {"qwen3.5-9b": tuple(range(2, 31, 2)), "muse-glimmer-30b": tuple(range(2, 51, 4)),
          "qwen3.6-27b": tuple(range(4, 61, 4)), "nemotron-3.5-lightning": tuple(range(2, 51, 4))}  # fmt: skip
N_TEST = {"qwen3.5-9b": 200, "muse-glimmer-30b": 200, "qwen3.6-27b": 150, "nemotron-3.5-lightning": 200}
N_FIT_MIN, N_FIT_MAX = 150, 250  # the fit half: at least 150 scenes (the spec), at most 250 (the cache's size)
C0_MIN = {"muse-glimmer-30b": 0.5, "nemotron-3.5-lightning": 0.5}  # no one-pick reference (x6_routes --c0-min, G2)
RUNS = {
    "qwen3.5-9b": "qwen35_9b_x47_anatomy",
    "qwen3.6-27b": "x47_anatomy_27b",
    "muse-glimmer-30b": "muse30_x47_anatomy",
}
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_anatomy"}  # batch 52: verdict --coverage, no Q-line
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x47_anatomy/x47_8-20261028T154518Z"  # 47.8's rules first scored
SPLIT_SEED, ATOMS_SEED = 0, 777
LOCKER_STEP, N_LOCKER = (
    8,
    160,
)  # D4 (3): the locker-sentence tokens' states cached every 8th layer, the first 160 fit scenes
K = X.K_MAIN
PARTS = ("J", "U", "I")
PART_TEXT = {"J": "the J++ part (25 signed-OMP atoms of the layer's lens)", "U": "the address part (U_l, the slot "
             "class means' basis refit at the layer)", "I": "identity outside J++ (mu_alt - mu_org orthogonalised "
             "against the scene's 25 atoms)"}  # fmt: skip
ARMS = ("none", "whole", *(f"{kind}_{p}{r}" for p in PARTS for kind in ("keep", "no") for r in ("", "_rand")))
C0_ARMS = ("none", "whole")
LOOKUP_ROUTES = R.ROUTES
RECALL_ROUTES = ("changed", "original", "slot", "other")
MOVED = ("identity", "position", "value")  # the lookup "switched": its answer left the original
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
NOT_INTERPRETABLE, L_J_BAR, L_P_BAR, L_PROBE_BAR = 0.30, 0.10, 0.20, 0.80
C_EARLY, C_LATE_J, C_LATE_I, C_MODELS, VALUE_BAR = 0.5, 0.1, 0.3, 2, 0.05
RECALL_WINDOW, RECALL_J_BAR = 0.5, 0.3
EPS = 1e-9
MARK = "⟦{}⟧"
AS_COMPUTED = (
    "Scenes: x6_routes' generator (seed 2510; locker-first), conditions C2 and C0, X0's gate (0.80 per reader on "
    "unedited scenes) and eligibility; the eligible C2 scenes split by bridge entity (seed 0; entities in a seeded "
    "order fill the test half to N_TEST scenes, the rest form the fit half, >= 150 or the run stops). Per sweep layer, "
    "from one forward of O and of S per scene: on the fit half the layout-free slot means and U_l (mass-mean basis; "
    "rank 2 with three lockers, the spec's rank 4 is not reachable here), the entity means over O and S bridge-word "
    "states and Id_l, x0_probe's three probes (entities held out), the refit's held-out slot / entity accuracy on the "
    "test half, the lens's top-10 rate for the bridge token; on the test half Delta = h_S - h_O and its parts J "
    "(signed OMP, 25 atoms of the layer's J++ lens, letter tokens), U (projection on U_l), I (rank-1 along mu_S - mu_O "
    "orthogonalised against the scene's atoms; zero where an entity has no mean, the scene left out of the I cells), "
    "W_E's 25-atom part and its overlap with J (D4). Random parts of the same share per scene: random lens atoms "
    "(seed 777 + l) for J, X0's random subspace (seed 888 + l) for U and I. Arms: none, whole, keep_X, keep_X_rand, "
    "no_X, no_X_rand for X in J, U, I; C0 scenes none and whole. Reads: X0's chat read, both readers; lookup answers "
    "classified identity / position / value / original / other, recall answers changed / original / slot item / "
    "other. Verdict (CPU, after Q47.8): per model and layer, shares and extra losses (X.cell) with cluster-bootstrap "
    "CIs over bridge entities (10,000, seed 0); the lookup's switch = identity + position + value, the recall's = "
    "changed; not interpretable where the whole change switches < 0.30; l_J, l_P, l_probe and rules (a)-(e) as the "
    "spec words them, point estimates, EPS 1e-9. C0 check at L: the whole change's lookup switch within 0.10 of the "
    "one-pick reference (Muse: >= 0.5), else the job fails after writing its files."
)


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def base_id(scene: str) -> str:
    """'C2-0017' -> '0017': the generator's base scene, shared by its conditions."""
    return scene.split("-", 1)[1]


def legs_of() -> dict[str, int]:
    from scripts import tasks_v2 as T

    return T.DOMAINS["animals"].values


def scene_cases(tok) -> tuple[list[dict], collections.Counter]:
    """x6_routes' scenes (seed 2510, chat), C0 and C2 only, each with its slot / pick features and the recall's route
    tokens (changed item, original item, the item at the target slot)."""
    cases, dropped = R.scenes(tok, R.N_GEN, rendering=RENDERING)
    return enrich(tok, cases), dropped


def enrich(tok, cases: list[dict]) -> list[dict]:
    """The C0 and C2 cases with their features: base scene, the O bridge's locker slot, the asked pick's sentence
    index, the layout key, the item at the target slot and the recall's route tokens."""
    from scripts import suite_v1 as S
    from scripts import x8_write as W

    legs = legs_of()
    out = []
    for c in cases:
        if c["condition"] not in ("C0", "C2"):
            continue
        pick, locker, n = PR.positions(c)
        items = [x for x, _ in W.slots_of(c["context"])]
        third = [x for x in items if x not in (c["bridge"], c["cf_bridge"])]
        assert len(third) == 1, c["scene"]
        assert locker == items.index(c["bridge"]), c["scene"]
        c = {**c, "base": base_id(c["scene"]), "slot": locker, "pick_index": pick, "sentences": n,
             "layout": PR.layout(c["context"], pick), "slot_item": third[0],
             "recall_tokens": {"changed": c["readers"][X.RECALL]["tok_b"], "original": c["readers"][X.RECALL]["tok_A"],
                               "slot": S.answer_token(tok, str(legs[third[0]]), "digit")}}  # fmt: skip
        out.append(c)
    return out


def recall_classify(top: int, case: dict) -> str:
    """The recall answer's route: the changed item's legs, the original item's, the item at the target slot's, other
    (in that order where two items share a leg count)."""
    hit = [r for r in ("changed", "original", "slot") if case["recall_tokens"][r] == top]
    return hit[0] if hit else "other"


def split_by_entity(cases: list[dict], n_test: int, seed: int = SPLIT_SEED, n_fit_min: int = N_FIT_MIN,
                    n_fit_max: int = N_FIT_MAX) -> tuple[list[dict], list[dict], dict]:  # fmt: skip
    """The eligible C2 cases split by bridge entity: entities in a seeded order go to the test half until it holds
    n_test cases, every other entity to the fit half; the test half is its first n_test cases in scene order, the fit
    half its first n_fit_max. Raises SystemExit under n_fit_min fit cases."""
    ents = sorted({c["bridge"] for c in cases})
    rng = random.Random(seed)
    rng.shuffle(ents)
    count = collections.Counter(c["bridge"] for c in cases)
    test_ents: list[str] = []
    while sum(count[e] for e in test_ents) < n_test and len(test_ents) < len(ents):
        test_ents.append(ents[len(test_ents)])
    fit_ents = [e for e in ents if e not in test_ents]
    test = [c for c in cases if c["bridge"] in test_ents][:n_test]
    fit = [c for c in cases if c["bridge"] in fit_ents][:n_fit_max]
    info = {"seed": seed, "entities": len(ents), "test_entities": sorted(test_ents), "fit_entities": sorted(fit_ents),
            "test": len(test), "fit": len(fit), "eligible": len(cases), "n_test": n_test, "n_fit_min": n_fit_min}  # fmt: skip
    if len(fit) < n_fit_min or len(test) < n_test:
        raise SystemExit(f"the split by entity gives {len(test)} test and {len(fit)} fit scenes (need {n_test} and "
                         f">= {n_fit_min}); stop: {info}")  # fmt: skip
    return test, fit, info


def stage_plan() -> dict:
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    cases, dropped = scene_cases(tok)
    c2 = [c for c in cases if c["condition"] == "C2"]
    target = pins.TARGET
    counts = {"target": target, "generated": dict(collections.Counter(c["condition"] for c in cases)),
              "dropped": dict(dropped), "entities": len({c["bridge"] for c in c2}), "layers": list(LAYERS[target]),
              "n_test": N_TEST[target], "arms": ARMS, "rows_per_scene_per_reader": 1 + len(LAYERS[target]) * (len(ARMS) - 1)}  # fmt: skip
    try:
        _, _, counts["split_if_all_eligible"] = split_by_entity(c2, N_TEST[target])
    except SystemExit as e:
        counts["split_if_all_eligible"] = str(e)
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


# ---- fits (CPU / GPU tensors) -------------------------------------------------------------------------------------


def orthonormal_basis(vectors):
    """An orthonormal basis [d, r] of the span of the rows of `vectors` [m, d] (double; r = numerical rank)."""
    import torch

    v = vectors.double()
    if v.shape[0] == 0:
        return v.new_zeros(v.shape[1], 0)
    u, s, _ = torch.linalg.svd(v.T, full_matrices=False)
    return u[:, s > s[0] * 1e-8] if s.numel() and float(s[0]) > 0 else u[:, :0]


def layout_free(h, layouts: list[str]) -> tuple[Any, dict[str, Any]]:
    """x0_massmean's layout-free residuals: each layout group's mean taken out (rows of h [n, d], double); singletons
    keep themselves minus the grand mean. Returns (residuals, {layout: mean})."""
    h = h.double()
    res = h.clone()
    means: dict[str, Any] = {}
    for g in sorted(set(layouts)):
        rows = [i for i, x in enumerate(layouts) if x == g]
        means[g] = h[rows].mean(0) if len(rows) > 1 else h.mean(0)
        res[rows] -= means[g]
    return res, means


def class_means(res, labels: list) -> dict[Any, Any]:
    return {c: res[[i for i, x in enumerate(labels) if x == c]].mean(0) for c in sorted(set(labels), key=str)}


def mass_mean_basis(means: dict[Any, Any]):
    """x0_massmean.mass_mean: the basis of the class means minus their grand mean [d, classes - 1]."""
    import torch

    m = torch.stack(list(means.values()))
    return orthonormal_basis(m - m.mean(0))


def nearest_class(res, means: dict[Any, Any], basis) -> list:
    """Each row's nearest class mean in the basis' coordinates (the refit's held-out read)."""
    import torch

    keys = list(means)
    proj = res.double() @ basis
    cen = torch.stack([means[k] for k in keys]) @ basis
    d2 = ((proj[:, None, :] - cen[None, :, :]) ** 2).sum(-1)
    return [keys[int(j)] for j in d2.argmin(1)]


def fit_layer(h_o, h_s, fit: list[dict]) -> dict[str, Any]:
    """One layer's fit-half quantities (CPU, double): layout means, slot means and U_l, entity means (O and S bridge
    words) and Id_l."""
    import torch

    layouts = [c["layout"] for c in fit]
    res_o, lay = layout_free(h_o, layouts)
    res_s = h_s.double() - torch.stack([lay[g] for g in layouts])
    slot_means = class_means(res_o, [c["slot"] for c in fit])
    ent_means = class_means(torch.cat([res_o, res_s]), [c["bridge"] for c in fit] + [c["cf_bridge"] for c in fit])
    return {"layout_means": lay, "slot_means": slot_means, "U": mass_mean_basis(slot_means),
            "entity_means": ent_means, "Id": mass_mean_basis(ent_means), "res_o": res_o}  # fmt: skip


def held_out_accuracy(f: dict, h_test, test: list[dict]) -> dict[str, Any]:
    """The refit read on the test half's O states: slot by the nearest slot mean in U_l (chance 1 / 3), entity by the
    nearest entity mean in Id_l over the scenes whose entity has a mean."""
    import torch

    lay = f["layout_means"]
    grand = torch.stack(list(lay.values())).mean(0)
    res = h_test.double() - torch.stack([lay.get(c["layout"], grand) for c in test])
    slot_pred = nearest_class(res, f["slot_means"], f["U"])
    slot_acc = float(np.mean([p == c["slot"] for p, c in zip(slot_pred, test, strict=True)]))
    have = [i for i, c in enumerate(test) if c["bridge"] in f["entity_means"]]
    ent_acc = None
    if have:
        pred = nearest_class(res[have], f["entity_means"], f["Id"])
        ent_acc = float(np.mean([p == test[i]["bridge"] for p, i in zip(pred, have, strict=True)]))
    return {"slot": slot_acc, "slot_chance": 1 / len(f["slot_means"]), "entity": ent_acc, "entity_n": len(have),
            "entity_chance": 1 / len(f["entity_means"]), "rank_U": int(f["U"].shape[1]), "rank_Id": int(f["Id"].shape[1])}  # fmt: skip


def probe_items(fit: list[dict]) -> list[dict]:
    return [{"scene": c["scene"], "entity": c["bridge"], "answer": c["readers"][X.LOOKUP]["answer"],
             "locker_index": c["slot"], "pick_index": c["pick_index"], "layout": c["layout"]} for c in fit]  # fmt: skip


def probes_at(h_o, fit: list[dict], n_boot: int) -> dict[str, dict]:
    """x0_probe's three probes on the fit half's O states at one layer (entities held out by its folds)."""
    x = np.asarray(h_o, dtype=np.float64)
    items = probe_items(fit)
    return {t: PR.score(x, items, t, n_boot) for t in PR.TARGETS}


def random_atoms_basis(jdic, seed: int):
    """A random orthonormal basis [d, d] spanned by lens atoms in a seeded random order (the J part's random control:
    random lens atoms, their leading ones up to the share as random_subspace_part picks them)."""
    import torch

    n, d = jdic.shape
    perm = torch.randperm(n, generator=torch.Generator().manual_seed(seed))[:d].to(jdic.device)
    q, r = torch.linalg.qr(jdic[perm].T.double())
    return (q * torch.sign(torch.diagonal(r))).float()


def identity_parts(x, atoms, jdic, means: dict, pairs: list[tuple[str, str]]):
    """Per row of x: the rank-1 part along mu_alt - mu_org orthogonalised against the row's atoms (x6_routes' idout),
    zero where an entity has no mean; the share of the raw direction inside the atoms' span; the missing flags."""
    import torch

    part = torch.zeros_like(x)
    inside, missing = [], []
    for i, (org, alt) in enumerate(pairs):
        if org not in means or alt not in means:
            missing.append(True)
            inside.append(None)
            continue
        u = (means[alt] - means[org]).to(x.device).double()
        u = u / u.norm()
        q, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        pu = q @ (q.T @ u)
        inside.append(round(float(pu.norm() ** 2), 6))
        v = u - pu
        v = (v / v.norm()).float()
        part[i] = (x[i] @ v) * v
        missing.append(False)
    return part, inside, missing


def shares_of(x, parts: dict[str, Any]) -> dict[str, Any]:
    return {k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30) for k, v in parts.items()}


def arms_of(x, parts: dict[str, Any], rand: dict[str, Any]) -> dict[str, Any]:
    """Every arm's rows [n, d] from the parts and their random parts, in ARMS order (none excluded)."""
    arms = {"whole": x}
    for p in PARTS:
        arms[f"keep_{p}"], arms[f"keep_{p}_rand"] = parts[p], rand[p]
        arms[f"no_{p}"], arms[f"no_{p}_rand"] = x - parts[p], x - rand[p]
    assert tuple(arms) == ARMS[1:]
    return arms


def overlap(a, atoms_b, dic_b) -> list[float]:
    """Per row: the share of part a inside the span of the row's atoms_b (rows of dic_b); 0 for a zero row."""
    import torch

    out = []
    for i in range(a.shape[0]):
        q, _ = torch.linalg.qr(dic_b[atoms_b[i]].T.double())
        v = a[i].double()
        out.append(round(float((q @ (q.T @ v)).norm() ** 2 / v.norm().clamp_min(1e-30) ** 2), 6))
    return out


def lens_top10(lens, h, layer: int, token_ids: list[int], k: int = 10) -> float:
    """The share of rows whose bridge token is among the layer's lens readout's top k."""
    import torch

    logits = lens.readout(h, layer)
    top = logits.topk(k, dim=-1).indices
    return float((top == torch.tensor(token_ids, device=top.device)[:, None]).any(1).float().mean())


def we_dictionary(model, lens, layer: int, letters):
    return X.dictionary("we", layer, model, lens, letters)


def competence(model, cases: list[dict], digits, ws) -> list[dict]:
    return X.competence(model, cases, digits, ws)


def locker_token_positions(tok, c: dict) -> list[list[int]]:
    """Per locker sentence of the O prompt (context order): the item token's and the number token's positions (the last
    token of each where a name spans several)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import x45b_binding as B

    text = X.render(tok, {"format": "prose", "kind": "digit", "context": c["context"],
                          "question": c["readers"][X.LOOKUP]["question"]}, RENDERING, c["context"])  # fmt: skip
    enc = raw_encoding(tok, text, offsets=True)
    assert enc["input_ids"] == c["readers"][X.LOOKUP]["ids"]["org"], f"{c['scene']}: the rendered prompt's ids differ"
    out = []
    for (a, _), sent in zip(B.locker_spans(text, c["context"]), B.locker_sentences(c["context"]), strict=True):
        m = B.LOCKER_RE.match(sent)
        assert m, sent
        pos = []
        for g in (1, 2):
            s, e = m.span(g)
            toks = SP.tokens_in(enc["offset_mapping"], a + s, a + e)
            assert toks, f"{c['scene']}: no token for {sent[s:e]!r}"
            pos.append(toks[-1])
        out.append(pos)
    return out


def locker_layers(layers: tuple[int, ...], step: int = LOCKER_STEP) -> tuple[int, ...]:
    """The sweep layers at which the locker-sentence tokens are cached: every (step / sweep step)-th sweep layer from
    the first (the 9B's L2, L10, ...; Muse's L2, L10, ...; the 27B's L4, L12, ...)."""
    every = max(1, step // (layers[1] - layers[0])) if len(layers) > 1 else 1
    return tuple(layers[::every])


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def read_labels(layers: tuple[int, ...], arms: tuple[str, ...]) -> list[tuple[int | None, str]]:
    """The rows of one scene's read: none once, then every arm but none at every layer."""
    out: list[tuple[int | None, str]] = [(None, "none")]
    return out + [(la, a) for la in layers for a in arms if a != "none"]


# ---- GPU ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, n_boot: int = X.N_BOOT, layers: tuple[int, ...] | None = None) -> Path:
    """layers: a sweep other than LAYERS[target] (49.4, the 27B's reduced grid); recorded in the manifest."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows
    from scripts.x0_parts import omp_atoms

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.8 renders chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in LAYERS, f"47.8 runs on {sorted(LAYERS)}, not {target}"
    layers, n_test, fixed = tuple(layers or LAYERS[target]), N_TEST[target], X.PREDICTED[target]
    assert fixed in layers, f"the fixed layer L{fixed} is not in the sweep {layers}"
    pins.check_lens_layers(layers)
    cached = locker_layers(layers)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    ref = R.c0_reference(target)
    c0_min = C0_MIN.get(target)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "47.8",
         "spec": "jobs/c3/batch47.yaml (47.8, amendment 2; D4 cache per amendment 3)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)}, "layers": list(layers), "fixed_layer": fixed,
         "n_layers": pins.N_LAYERS, "n_test": n_test, "n_fit_min": N_FIT_MIN, "n_fit_max": N_FIT_MAX, "k": K, "omp": "signed",
         "arms": list(ARMS), "c0_arms": list(C0_ARMS), "parts": PART_TEXT, "as_computed": AS_COMPUTED,
         "c0_reference": {"run": R.C0_REF.get(target, (None,))[0], "lookup_switch": ref, "tolerance": R.C0_TOL, "c0_min": c0_min},
         "seeds": {"scenes": R.SEED, "split": SPLIT_SEED, "random_atoms": f"{ATOMS_SEED} + layer", "random_subspace": f"{X.SUBSPACE_SEED} + layer",
                   "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": n_boot, "gate": X.GATE,
         "cache": {"layers_states": list(layers), "layers_locker": list(cached), "dtype": "float16",
                   "locker_tokens": "per locker sentence in context order: [item token, number token] (the last token of each)"},
         "read": "X0's chat read: the prompt with a digit's space token appended; the top token classified",
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {
            "question": NO_PREDICTION,
            "batch": 52,
            "rules_first_scored": SCORED,
            "sealed": "none (batch 52 coverage)",
        }
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    dev = model.device
    cases, dropped = scene_cases(tok)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    comp = competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate, ok_by = {}, {}
    for cond in ("C0", "C2"):
        mine = [c for c in cases if c["condition"] == cond]
        acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in mine])) for w in X.READERS}
        ok = [c for c in mine if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                     for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
        gate[cond] = {"cases": len(mine), "org_read_accuracy": acc, "pass": all(a >= X.GATE for a in acc.values()),
                      "eligible": len(ok)}  # fmt: skip
        ok_by[cond] = ok
    X.write_jsonl(out / "competence.jsonl", comp)
    (out / "gate.json").write_text(json.dumps({"dropped": dropped, "gate": gate}, indent=2) + "\n")
    if not gate["C2"]["pass"]:
        raise SystemExit("C2 failed the gate fixed in advance (0.80 per reader); not tested; see gate.json")
    test, fit, split = split_by_entity(ok_by["C2"], n_test, SPLIT_SEED, N_FIT_MIN, N_FIT_MAX)
    bases = {c["base"] for c in test}
    c0 = [c for c in ok_by["C0"] if c["base"] in bases] if gate["C0"]["pass"] else []
    split["c0_test"] = len(c0)
    split["c0_gate_pass"] = gate["C0"]["pass"]
    (out / "split.json").write_text(json.dumps(split, indent=2) + "\n")
    slim = lambda c: {k: v for k, v in c.items() if k != "space"}  # noqa: E731
    X.write_jsonl(out / "cases.jsonl", [{**slim(c), "half": "test"} for c in test] + [{**slim(c), "half": "fit"} for c in fit]
                  + [{**slim(c), "half": "c0"} for c in c0])  # fmt: skip
    print(json.dumps({"gate": gate, "split": split}), flush=True)

    # forwards: every sweep layer at the bridge word (fit: O and S; test and c0: O and S), the locker tokens (fit)
    with torch.no_grad():
        d = int(
            model.run(torch.tensor([fit[0]["readers"][X.LOOKUP]["ids"]["org"]], device=dev), record=layers[:1])[1][
                layers[0]
            ].shape[1]
        )
    n_lock = min(len(fit), N_LOCKER)
    locker_pos = [locker_token_positions(tok, c) for c in fit[:n_lock]]
    h_fit = {v: {la: torch.empty(len(fit), d) for la in layers} for v in ("org", "alt")}
    h_lock = {la: torch.empty(n_lock, 3, 2, d, dtype=torch.float16) for la in cached}
    lens = JLens(model, "jpp")
    top10_ids = [c["readers"][X.LOOKUP]["ids"]["org"][c["pos"]] for c in fit]
    with torch.no_grad():
        for i, c in enumerate(progress(fit, "fit half: states at the bridge word (scene)")):
            ids = c["readers"][X.LOOKUP]["ids"]
            for v in ("org", "alt"):
                st = model.run(torch.tensor([ids[v]], device=dev), record=layers)[1]
                for la in layers:
                    h_fit[v][la][i] = st[la][c["pos"]].float().cpu()
                    if v == "org" and la in cached and i < n_lock:
                        h_lock[la][i] = (
                            st[la][[p for pair in locker_pos[i] for p in pair]].reshape(3, 2, d).half().cpu()
                        )
        deltas = {la: torch.empty(len(test), d) for la in layers}
        h_test_o = {la: torch.empty(len(test), d) for la in layers}
        for i, c in enumerate(progress(test, "test half: Δ at the bridge word (scene)")):
            ids = c["readers"][X.LOOKUP]["ids"]
            st = {v: model.run(torch.tensor([ids[v]], device=dev), record=layers)[1] for v in ("org", "alt")}
            for la in layers:
                h_test_o[la][i] = st["org"][la][c["pos"]].float().cpu()
                deltas[la][i] = (st["alt"][la][c["pos"]] - st["org"][la][c["pos"]]).float().cpu()
        d_c0 = {la: torch.empty(len(c0), d) for la in layers}
        for i, c in enumerate(progress(c0, "C0: Δ at the bridge word (scene)")):
            ids = c["readers"][X.LOOKUP]["ids"]
            st = {v: model.run(torch.tensor([ids[v]], device=dev), record=layers)[1] for v in ("org", "alt")}
            for la in layers:
                d_c0[la][i] = (st["alt"][la][c["pos"]] - st["org"][la][c["pos"]]).float().cpu()

        # per layer: the fit, the parts, the arms
        letters = model.letter_token_ids()
        pairs = [(c["bridge"], c["cf_bridge"]) for c in test]
        fit_rec: dict[str, Any] = {"layers": list(layers), "per_layer": {}}
        arms_by_layer: dict[int, dict[str, Any]] = {}
        norms_by: dict[tuple[str, int], dict] = {}
        cache_bases: dict[str, Any] = {}
        for la in progress(layers, "per-layer fit and parts (layer)"):
            f = fit_layer(h_fit["org"][la], h_fit["alt"][la], fit)
            ho = held_out_accuracy(f, h_test_o[la], test)
            probes = probes_at(h_fit["org"][la].numpy(), fit, n_boot)
            jdic = lens.vectors(la, letters)
            wedic = we_dictionary(model, lens, la, letters)
            x = deltas[la].to(dev)
            atoms = omp_atoms(jdic, x, K)
            we_atoms = omp_atoms(wedic, x, K)
            parts = {
                "J": X.fit(jdic, x, K, "signed").float(),
                "U": (x @ f["U"].float().to(dev)) @ f["U"].float().to(dev).T,
            }
            parts["I"], inside, missing = identity_parts(x, atoms, jdic, f["entity_means"], pairs)
            we_part = X.fit(wedic, x, K, "signed").float()
            sh = shares_of(x, {**parts, "WE": we_part})
            basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            abasis = random_atoms_basis(jdic, ATOMS_SEED + la)
            rand = {"J": SP.random_subspace_part(x, sh["J"], abasis), "U": SP.random_subspace_part(x, sh["U"], basis),
                    "I": SP.random_subspace_part(x, sh["I"], basis)}  # fmt: skip
            rsh = shares_of(x, rand)
            arms_by_layer[la] = {a: v.cpu() for a, v in arms_of(x, parts, rand).items()}
            ov_we_in_j, ov_j_in_we = overlap(we_part, atoms, jdic), overlap(parts["J"], we_atoms, wedic)
            u_cos = [R.mean_cos2(jdic[atoms[i]].T, f["U"].float().to(dev)) for i in range(len(test))]
            for i, c in enumerate(test):
                uc = u_cos[i]
                norms_by[(c["scene"], la)] = {
                    "scene": c["scene"], "layer": la, "norm": round(float(x[i].norm()), 4),
                    **{f"share_{p}": round(float(sh[p][i]), 5) for p in (*PARTS, "WE")},
                    **{f"share_{p}_rand": round(float(rsh[p][i]), 5) for p in PARTS},
                    "I_missing": missing[i], "id_inside_J": inside[i], "cos2_U_J": None if uc is None else round(uc, 6),
                    "WE_inside_J": ov_we_in_j[i], "J_inside_WE": ov_j_in_we[i],
                    "atoms_J": [int(t) for t in atoms[i]], "atoms_WE": [int(t) for t in we_atoms[i]]}  # fmt: skip
            fit_rec["per_layer"][str(la)] = {
                "n_fit": len(fit), "held_out": ho, "probes": probes,
                "lens_top10": lens_top10(lens, h_fit["org"][la].to(dev), la, top10_ids),
                "entities_with_mean": len(f["entity_means"]), "I_missing": int(sum(missing)),
                "median_share": {p: round(float(sh[p].median()), 5) for p in (*PARTS, "WE")},
                "median_share_rand": {p: round(float(rsh[p].median()), 5) for p in PARTS},
                "jpp_share_of_U": float(np.mean([v for v in u_cos if v is not None])) if any(v is not None for v in u_cos) else None,
                "jpp_share_of_I": float(np.mean([v for v in inside if v is not None])) if any(v is not None for v in inside) else None,
                "WE_inside_J_median": float(np.median(ov_we_in_j)), "J_inside_WE_median": float(np.median(ov_j_in_we))}  # fmt: skip
            ents = list(f["entity_means"])
            cache_bases.update({f"U_L{la}": f["U"].float().numpy(), f"Id_L{la}": f["Id"].half().numpy(),
                                f"slot_means_L{la}": torch.stack([f["slot_means"][k] for k in sorted(f["slot_means"])]).half().numpy(),
                                f"entity_means_L{la}": torch.stack([f["entity_means"][e] for e in ents]).half().numpy(),
                                f"layout_means_L{la}": torch.stack([f["layout_means"][g] for g in sorted(f["layout_means"])]).half().numpy()})  # fmt: skip
            fit_rec["per_layer"][str(la)]["entities"] = ents
            fit_rec["per_layer"][str(la)]["layouts"] = sorted(f["layout_means"])
            del x, atoms, we_atoms, parts, rand, basis, abasis, jdic, wedic
        (out / "fit.json").write_text(json.dumps(fit_rec, indent=1) + "\n")
        X.write_jsonl(out / "norms.jsonl", [norms_by[(c["scene"], la)] for c in test for la in layers])
        cache = out / "cache"
        cache.mkdir()
        np.savez_compressed(cache / "bases.npz", **cache_bases)
        states = {"scene": np.array([c["scene"] for c in fit]),
                  **{f"O_L{la}": h_fit["org"][la].half().numpy() for la in layers},
                  **{f"S_L{la}": h_fit["alt"][la].half().numpy() for la in layers},
                  **{f"locker_L{la}": h_lock[la].numpy() for la in cached}}  # fmt: skip
        np.savez_compressed(cache / "fit_states.npz", **states)
        (cache / "locker_positions.json").write_text(
            json.dumps({c["scene"]: p for c, p in zip(fit[:n_lock], locker_pos, strict=True)}) + "\n"
        )
        print("wrote", out / "fit.json", "and the cache", flush=True)

        # reads
        rows, greedy = [], []
        examples = set(example_indices(len(test)))
        labels = read_labels(layers, ARMS)
        for i, c in enumerate(progress(test, f"reads over {len(layers)} layers (scene)")):
            edits = [{} if la is None else {la: AddRows(arms_by_layer[la][a][i : i + 1].to(dev), [c["pos"]])}
                     for la, a in labels]  # fmt: skip
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                for (la, a), lg in zip(labels, logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "condition": "C2", "entity": c["bridge"], "reader": w, "layer": la,
                                 "arm": a, "route": R.classify(top, c) if w == X.LOOKUP else recall_classify(top, c),
                                 **X.read_row(lg, rd, digits), "top_text": tok.decode([top])})  # fmt: skip
                if i in examples:
                    at_l = [(la, a) for la, a in labels if la in (None, fixed)]
                    ed = [edits[labels.index(k)] for k in at_l]
                    texts = model.generate_batch(torch.tensor([rd["ids"]["org"]], device=dev), X.GEN_TOKENS, ed)
                    greedy += [{"scene": c["scene"], "reader": w, "layer": la, "arm": a, "greedy": t}
                               for (la, a), t in zip(at_l, texts, strict=True)]  # fmt: skip
        labels0 = read_labels(layers, C0_ARMS)
        for i, c in enumerate(progress(c0, "C0 reads (scene)")):
            edits = [{} if la is None else {la: AddRows(d_c0[la][i : i + 1].to(dev), [c["pos"]])} for la, _ in labels0]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                for (la, a), lg in zip(labels0, logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "condition": "C0", "entity": c["bridge"], "reader": w, "layer": la,
                                 "arm": a, "route": None, **X.read_row(lg, rd, digits), "top_text": tok.decode([top])})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    at = [r["switched"] for r in rows if r["condition"] == "C0" and r["reader"] == X.LOOKUP and r["arm"] == "whole"
          and r["layer"] == fixed]  # fmt: skip
    rate = float(np.mean(at)) if at else float("nan")
    ok = (rate >= c0_min) if c0_min is not None else (ref is not None and abs(rate - ref) <= R.C0_TOL)
    (out / "c0_check.json").write_text(json.dumps({"layer": fixed, "n": len(at), "c0_lookup_switch": rate, "reference": ref,
                                                   "c0_min": c0_min, "ok": bool(ok)}) + "\n")  # fmt: skip
    print(f"wrote {out}: {len(rows)} reads (sealed: no verdict); C0 at L{fixed}: {rate:.3f} (ok={ok})", flush=True)
    if not ok:
        raise SystemExit("C0 sanity failed at L (" + (f"below {c0_min}" if c0_min is not None else
                                                      f"not within {R.C0_TOL} of the reference {ref}") + "); stop")  # fmt: skip
    return out


# ---- verdict (CPU, sealed) ----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD", question: str = QUESTION, predictions: str = PREDICTIONS) -> str:
    """Dan's committed answer (the 'Dan:' line of the question's block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{predictions}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{question}**" not in text:
        return ""
    block = text.split(f"**{question}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def ci3(point: float, draws: np.ndarray) -> list[float]:
    return [float(point), *X.interval(draws)]


def layer_cells(rows: list[dict], norms: list[dict], layer: int, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One layer's cells over the test half (C2): per reader the whole change's switch rate, every arm's route shares,
    and each part's extra loss (X.cell: Jdep - Rdep) with paired cluster-bootstrap CIs over bridge entities; the I arms
    over the scenes whose I part exists."""
    out: dict[str, Any] = {"layer": layer}
    missing = {n["scene"] for n in norms if n["layer"] == layer and n.get("I_missing")}
    for w in X.READERS:
        by = {a: {r["scene"]: r for r in rows if r["condition"] == "C2" and r["reader"] == w and r["layer"] in (layer, None)
                  and r["arm"] == a} for a in ARMS}  # fmt: skip
        scenes_ = sorted(set.intersection(*(set(v) for v in by.values())))
        if not scenes_:
            continue
        routes = LOOKUP_ROUTES if w == X.LOOKUP else RECALL_ROUTES
        moved = MOVED if w == X.LOOKUP else ("changed",)
        ents = [by["whole"][s]["entity"] for s in scenes_]
        sw = {f"{rt}|{a}": [int(by[a][s]["route"] == rt) for s in scenes_] for a in ARMS for rt in routes}
        sw.update({f"moved|{a}": [int(by[a][s]["route"] in moved) for s in scenes_] for a in ARMS})
        rr = X.resampled_rates(sw, ents, n_boot)
        pt = {k: float(np.mean(v)) for k, v in sw.items()}
        cell: dict[str, Any] = {"n": len(scenes_), "entities": len(set(ents)),
                                "switch": {a: ci3(pt[f"moved|{a}"], rr[f"moved|{a}"]) for a in ARMS},
                                "share": {a: {rt: ci3(pt[f"{rt}|{a}"], rr[f"{rt}|{a}"]) for rt in routes} for a in ARMS},
                                "loss": {}}  # fmt: skip
        cell["interpretable"] = bool(cell["switch"]["whole"][0] >= NOT_INTERPRETABLE - EPS)
        for p in PARTS:
            keep = [s for s in scenes_ if p != "I" or s not in missing]
            if not keep:
                continue
            idx = [scenes_.index(s) for s in keep]
            c = X.cell({"whole": [sw["moved|whole"][i] for i in idx], "no_part": [sw[f"moved|no_{p}"][i] for i in idx],
                        "no_rand": [sw[f"moved|no_{p}_rand"][i] for i in idx]}, [ents[i] for i in idx], n_boot)  # fmt: skip
            cell["loss"][p] = {"n": c["n"], "excess": c["excess"], "Jdep": c["Jdep"], "Rdep": c["Rdep"],
                               "S_whole": c["S_whole"], "valid": c["valid"]}  # fmt: skip
        out[READER_NAME[w]] = cell
    return out


def c0_cells(rows: list[dict], layers: tuple[int, ...]) -> dict[str, dict[str, float]]:
    """C0's whole-change switch rate per reader and layer (the sanity swap across depth)."""
    out: dict[str, dict[str, float]] = {}
    for w in X.READERS:
        for la in layers:
            sw = [
                r["switched"]
                for r in rows
                if r["condition"] == "C0" and r["reader"] == w and r["layer"] == la and r["arm"] == "whole"
            ]
            if sw:
                out.setdefault(READER_NAME[w], {})[str(la)] = float(np.mean(sw))
    return out


def reader_cells(cells: dict[int, dict], layers: tuple[int, ...], reader: str) -> dict[int, dict]:
    """One reader's cell per layer, at the layers that have one."""
    return {la: cells[la][reader] for la in layers if la in cells and reader in cells[la]}


def first_layers(cells: dict[int, dict], fit: dict[str, Any], layers: tuple[int, ...]) -> dict[str, Any]:
    """l_J: the first layer from which the lookup's extra loss without J stays <= L_J_BAR at every later interpretable
    layer (None if the last interpretable layer fails, or no layer is interpretable); l_P: the first interpretable layer
    with position share (whole) >= L_P_BAR; l_probe: the first layer with the slot probe >= L_PROBE_BAR."""
    lk = reader_cells(cells, layers, "lookup")
    interp = [la for la in layers if la in lk and lk[la]["interpretable"]]
    l_j = None
    for la in interp:
        later = [x for x in interp if x >= la]
        if all("J" in lk[x]["loss"] and lk[x]["loss"]["J"]["excess"][0] <= L_J_BAR + EPS for x in later):
            l_j = la
            break
    l_p = next((la for la in interp if lk[la]["share"]["whole"]["position"][0] >= L_P_BAR - EPS), None)
    slot = {int(la): v["probes"]["locker sentence"]["probe"][0] for la, v in fit["per_layer"].items()}
    l_probe = next((la for la in layers if la in slot and slot[la] >= L_PROBE_BAR - EPS), None)
    return {"l_J": l_j, "l_P": l_p, "l_probe": l_probe, "interpretable_lookup": interp,
            "extra_loss_J": {str(la): lk[la]["loss"]["J"]["excess"][0] for la in interp if "J" in lk[la]["loss"]},
            "position_whole": {str(la): lk[la]["share"]["whole"]["position"][0] for la in interp},
            "slot_probe": {str(la): slot[la] for la in layers if la in slot}}  # fmt: skip


def rules(cells: dict[int, dict], fit: dict[str, Any], layers: tuple[int, ...], fixed: int) -> dict[str, Any]:
    """Rules (a)-(e) on one model (point estimates; (c)'s batch count is summed over models by batch_rules)."""
    fl = first_layers(cells, fit, layers)
    l_j, l_p, l_probe = fl["l_J"], fl["l_P"], fl["l_probe"]
    out: dict[str, Any] = {**fl}
    out["a"] = {"holds": None if l_j is None or l_p is None else bool(l_p >= l_j), "gap": None if l_j is None or l_p is None else l_p - l_j,
                "why": f"l_P = {l_p}, l_J = {l_j}"}  # fmt: skip
    out["a"]["gap_bucket"] = (
        None
        if out["a"]["gap"] is None
        else "<= 2"
        if out["a"]["gap"] <= 2
        else "3-6"
        if out["a"]["gap"] <= 6
        else "> 6"
    )
    out["b"] = {"holds": None if l_probe is None or l_p is None else bool(l_probe <= l_p), "why": f"l_probe = {l_probe}, l_P = {l_p}",
                "probe_after_use": bool(l_probe is not None and l_p is not None and l_probe > l_p)}  # fmt: skip
    interp = fl["interpretable_lookup"]
    lk = reader_cells(cells, layers, "lookup")
    early = interp[0] if interp else None
    at_l = lk.get(fixed)
    if early is not None and at_l is not None and at_l["interpretable"]:
        e_j = lk[early]["share"]["keep_J"]["identity"][0]
        l_jj, l_i = at_l["share"]["keep_J"]["identity"][0], at_l["share"]["keep_I"]["identity"][0]
        holds = e_j >= C_EARLY - EPS and l_jj <= C_LATE_J + EPS and l_i >= C_LATE_I - EPS
        cross = next(
            (
                la
                for la in interp
                if lk[la]["share"]["keep_I"]["identity"][0] > lk[la]["share"]["keep_J"]["identity"][0]
            ),
            None,
        )
        out["c"] = {"holds": bool(holds), "earliest": early, "keep_J_identity_early": e_j, "keep_J_identity_L": l_jj,
                    "keep_I_identity_L": l_i, "crossing": cross,
                    "why": f"keep_J identity {e_j:.2f} at L{early}, {l_jj:.2f} at L{fixed}; keep_I identity {l_i:.2f} at L{fixed}"}  # fmt: skip
    else:
        out["c"] = {"holds": None, "why": "no interpretable layer, or L itself is not interpretable"}
    values = {str(la): lk[la]["share"]["whole"]["value"][0] for la in interp}
    out["d"] = {"holds": bool(interp) and all(v <= VALUE_BAR + EPS for v in values.values()), "value_whole": values,
                "max_value": max(values.values(), default=None)}  # fmt: skip
    rc = reader_cells(cells, layers, "recall")
    window = [la for la in layers if la in rc and rc[la]["switch"]["whole"][0] >= RECALL_WINDOW - EPS]
    loss = {str(la): rc[la]["loss"]["J"]["excess"][0] for la in window if "J" in rc[la]["loss"]}
    onset = next(
        (la for la in window if "J" in rc[la]["loss"] and rc[la]["loss"]["J"]["excess"][0] >= RECALL_J_BAR - EPS), None
    )
    out["e"] = {"window": window, "needs_J_throughout": bool(window) and all(v >= RECALL_J_BAR - EPS for v in loss.values()),
                "extra_loss_J": loss, "onset": onset, "l_J": l_j}  # fmt: skip
    return out


def batch_rules(models: list[dict]) -> dict[str, Any]:
    """Q47.8's answers over the models: (a), (b), (d) per model; (c) on >= C_MODELS of 3."""
    tested = [m for m in models if m["status"] == "tested"]
    c_hold = [m["target"] for m in tested if m["rules"]["c"]["holds"]]
    return {"a": {m["target"]: m["rules"]["a"] for m in tested}, "b": {m["target"]: m["rules"]["b"]["holds"] for m in tested},
            "c": {"holds": len(c_hold) >= C_MODELS, "held_on": c_hold, "pending": [m["target"] for m in models if m["status"] != "tested"]},
            "d": {m["target"]: m["rules"]["d"]["holds"] for m in tested}}  # fmt: skip


def figure_data(m: dict[str, Any]) -> dict[str, Any]:
    """A tested model's curves in x47_anatomy_fig's contract (rows keyed by quantity, layer -> (v, lo, hi))."""
    rows: dict[str, dict[int, Any]] = collections.defaultdict(dict)
    ni = {"lookup": [], "recall": []}
    for la_s, c in m["cells"].items():
        la = int(la_s)
        for w in ("lookup", "recall"):
            if w not in c:
                continue
            if not c[w]["interpretable"]:
                ni[w].append(la)
            for p in PARTS:
                if p in c[w]["loss"]:
                    rows[f"loss.{w}.{p}"][la] = c[w]["loss"][p]["excess"]
        if "lookup" in c:
            for rt in ("identity", "position", "value", "original"):
                rows[f"lookup.whole.{rt}"][la] = c["lookup"]["share"]["whole"][rt]
            for a, rt in (
                ("keep_U", "position"),
                ("keep_U_rand", "position"),
                ("keep_J", "identity"),
                ("keep_J_rand", "identity"),
                ("keep_I", "identity"),
                ("keep_I_rand", "identity"),
            ):
                rows[f"{a}.{rt}"][la] = c["lookup"]["share"][a][rt]
        if "recall" in c:
            rows["recall.whole.switch"][la] = c["recall"]["switch"]["whole"]
            rows["recall.whole.slot"][la] = c["recall"]["share"]["whole"]["slot"]
    for la_s, f in m["fit"]["per_layer"].items():
        la = int(la_s)
        for key, t in (("identity", "bridge identity"), ("slot", "locker sentence"), ("digit", "answer digit")):
            rows[f"probe.{key}"][la] = f["probes"][t]["probe"]
        for p in ("U", "I"):
            if f.get(f"jpp_share_of_{p}") is not None:
                rows[f"jpp_share.{p}"][la] = [f[f"jpp_share_of_{p}"], None, None]
        rows["lens_top10"][la] = [f["lens_top10"], None, None]
    return {"target": m["target"], "n_layers": m["n_layers"], "L": m["layer"], "layers": m["layers"], "ni": ni,
            "rows": {k: dict(v) for k, v in rows.items()}, "status": "sealed run"}  # fmt: skip


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.8 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    norms = X.read_jsonl(src / "norms.jsonl")
    fit = json.loads((src / "fit.json").read_text())
    layers = tuple(m["layers"])
    cells = {la: layer_cells(rows, norms, la, n_boot) for la in layers}
    out = {"run": run, "target": m["model"]["target"], "status": "tested", "layer": m["fixed_layer"], "layers": list(layers),
           "n_layers": m["n_layers"], "cells": {str(la): c for la, c in cells.items()}, "fit": fit,
           "rules": rules(cells, fit, layers, m["fixed_layer"]), "c0": c0_cells(rows, layers),
           "c0_check": json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else None,
           "split": json.loads((src / "split.json").read_text()) if (src / "split.json").exists() else None}  # fmt: skip
    out["figure"] = figure_data(out)
    return out


def fmt(v) -> str:
    if v is None or (isinstance(v, (list, tuple)) and (v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])))):
        return "-"
    if isinstance(v, (list, tuple)):
        return (f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]" if v[1] is not None else f"{v[0]:.2f}").replace("-", "−")
    return f"{v:.2f}".replace("-", "−") if isinstance(v, float) else str(v)


def yn(v) -> str:
    return "-" if v is None else "yes" if v else "no"


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """47.8's verdict (sealed until Q47.8), or with coverage (batch 52) the same rules on the given runs only (no pending
    rows for the others), no seal guard, "no prediction" in place of Dan's answer, written to x52_anatomy-<UTC>/."""
    from scripts import x47_anatomy_fig as F

    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [
        {"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"}
        for t in RUNS
        if t not in targets and not coverage
    ]
    tested = [m for m in models if m["status"] == "tested"]
    b = batch_rules(models)
    out = RESULTS / f"{'x52_anatomy' if coverage else 'x47_8'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    who = f"batch 52 coverage, {answer}" if coverage else f"{QUESTION}, Dan: {answer}"
    lines = ["# 47.8: layer anatomy of the switch", "",
             f"Batch 47, test 47.8 (jobs/c3/batch47.yaml, amendment 2; {who}). Routes scenes "
             "(another item moved), locker-first, the test half (split by bridge entity, seed 0); every arm at every "
             f"sweep layer on O, X0's chat read. Cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). "
             "A reader's layer is not interpretable where the whole change switches < 0.30 of it (lookup switch = the "
             "answer moved to identity, position or value). UNVERIFIED.", "", "## Rules (point estimates, EPS 1e-9)", "",
             "| model | l_J | l_P | l_probe | (a) handoff l_P >= l_J | gap | (b) l_probe <= l_P | (c) identity leaves the lens | (d) never the value | (e) recall window | needs J throughout | recall onset |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | pending ({m['why']}) | | | | | | | | | | |")
            continue
        r = m["rules"]
        w = r["e"]["window"]
        lines.append(f"| {m['target']} | {r['l_J']} | {r['l_P']} | {r['l_probe']} | {yn(r['a']['holds'])} | "
                     f"{r['a']['gap']} ({r['a']['gap_bucket']}) | {yn(r['b']['holds'])} | {yn(r['c']['holds'])} "
                     f"(cross {r['c'].get('crossing')}) | {yn(r['d']['holds'])} (max {fmt(r['d']['max_value'])}) | "
                     f"{f'L{w[0]}-L{w[-1]}' if w else '-'} | {yn(r['e']['needs_J_throughout'])} | {r['e']['onset']} |")  # fmt: skip
    lines += ["", f"**{QUESTION}**: (a) " + "; ".join(f"{t}: {yn(v['holds'])}, gap {v['gap']} ({v['gap_bucket']})" for t, v in b["a"].items())
              + ". (b) " + "; ".join(f"{t}: {yn(v)}" for t, v in b["b"].items())
              + f". (c) {yn(b['c']['holds'])} (holds on {b['c']['held_on'] or 'none'}; pending {b['c']['pending'] or 'none'})."
              + " (d) " + "; ".join(f"{t}: {yn(v)}" for t, v in b["d"].items()) + ".", ""]  # fmt: skip
    lines += ["## Per layer (the lookup)", "",
              "| model | layer | n | interpretable | switch (whole) | identity | position | value | original | keep_J identity (rand) | keep_U position (rand) | keep_I identity (rand) | extra loss no_J | no_U | no_I |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for la_s, c in m["cells"].items():
            lk = c.get("lookup")
            if not lk:
                continue
            s = lk["share"]
            lines.append(f"| {m['target']} | {la_s} | {lk['n']} | {yn(lk['interpretable'])} | {fmt(lk['switch']['whole'])} | "
                         + " | ".join(fmt(s["whole"][rt]) for rt in ("identity", "position", "value", "original"))
                         + f" | {fmt(s['keep_J']['identity'])} ({fmt(s['keep_J_rand']['identity'])}) | {fmt(s['keep_U']['position'])} "
                         f"({fmt(s['keep_U_rand']['position'])}) | {fmt(s['keep_I']['identity'])} ({fmt(s['keep_I_rand']['identity'])}) | "
                         + " | ".join(fmt(lk["loss"][p]["excess"]) if p in lk["loss"] else "-" for p in PARTS) + " |")  # fmt: skip
    lines += ["", "## Per layer (the recall)", "",
              "| model | layer | n | interpretable | switch (changed) | original | slot item | other | extra loss no_J | no_U | no_I |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for la_s, c in m["cells"].items():
            rc = c.get("recall")
            if not rc:
                continue
            s = rc["share"]["whole"]
            lines.append(f"| {m['target']} | {la_s} | {rc['n']} | {yn(rc['interpretable'])} | {fmt(rc['switch']['whole'])} | "
                         f"{fmt(s['original'])} | {fmt(s['slot'])} | {fmt(s['other'])} | "
                         + " | ".join(fmt(rc["loss"][p]["excess"]) if p in rc["loss"] else "-" for p in PARTS) + " |")  # fmt: skip
    lines += ["", "## Fit half per layer (probes, the refit's held-out read, the lens's top-10 rate, shares)", "",
              "| model | layer | n fit | probe identity | probe slot | probe digit | held-out slot (U_l, rank) | held-out entity (Id_l) | lens top-10 | median share J / U / I / W_E | J++ share of U_l / of I_l | W_E inside J (median) | I missing |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for la_s, f in m["fit"]["per_layer"].items():
            p, ho, ms = f["probes"], f["held_out"], f["median_share"]
            lines.append(f"| {m['target']} | {la_s} | {f['n_fit']} | {fmt(p['bridge identity']['probe'])} | {fmt(p['locker sentence']['probe'])} | "
                         f"{fmt(p['answer digit']['probe'])} | {fmt(ho['slot'])} (rank {ho['rank_U']}) | {fmt(ho['entity'])} (n {ho['entity_n']}) | "
                         f"{fmt(f['lens_top10'])} | {ms['J']:.3f} / {ms['U']:.3f} / {ms['I']:.3f} / {ms['WE']:.3f} | "
                         f"{fmt(f.get('jpp_share_of_U'))} / {fmt(f.get('jpp_share_of_I'))} | {fmt(f['WE_inside_J_median'])} | {f['I_missing']} |")  # fmt: skip
    lines += ["", "C0 (the sanity swap) whole-change switch rate by layer: " + "; ".join(
        f"{m['target']} lookup " + ", ".join(f"L{la} {v:.2f}" for la, v in m["c0"].get("lookup", {}).items())
        + (f" (check at L: {m['c0_check']})" if m.get("c0_check") else "") for m in tested) + ".", "",
        "Arms: " + "; ".join(f"{p}: {t}" for p, t in PART_TEXT.items()) + "; keep_X = only that part added, no_X = the change "
        "minus it, _rand = a random part of the same share (random lens atoms for J, a random subspace for U and I).", ""]  # fmt: skip
    (out / "x47_8.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "batch": b, "models": models}, indent=1) + "\n"
    )
    (out / "x47_8.md").write_text("\n".join(lines) + "\n")
    if tested:
        F.figure([m["figure"] for m in tested], out / "x47_anatomy.png")
    print("\n".join(lines[:20]))
    print(out)
    return out


# ---- view (CPU, sealed) -------------------------------------------------------------------------------------------


def marked_prompt(text: str, ids: list[int], pos: int, tok) -> str:
    """The prompt as the model reads it with the bridge token marked ⟦…⟧ (decoded token by token)."""
    return (
        "".join(MARK.format(tok.decode([t])) if i == pos else tok.decode([t]) for i, t in enumerate(ids))
        if tok
        else text
    )


def view_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    fixed, layers = m["fixed_layer"], m["layers"]
    test = [c for c in X.read_jsonl(src / "cases.jsonl") if c["half"] == "test"]
    reads = {(r["scene"], r["reader"], r["layer"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {
        (g["scene"], g["reader"], g["layer"], g["arm"]): g["greedy"]
        for g in X.read_jsonl(src / "examples_greedy.jsonl")
    }
    lines = [f"## {run}: {min(k, len(test))} random test items of {len(test)} (seed {seed}); the patch at the bridge word ⟦…⟧, "
             f"every arm at L{fixed}, the whole change at every layer", ""]  # fmt: skip
    for i in example_indices(len(test), k, seed):
        c = test[i]
        exp = c["expect"]
        lines += [f"### {c['scene']}: bridge {c['bridge']} → {c['cf_bridge']}; slot {c['slot']}; expected digits identity "
                  f"{exp['identity']}, position {exp['position']}, value {exp['value']}, original {exp['original']}", "",
                  f"O: {c['context']}", "", f"S: {c['cf_context']}", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            name = READER_NAME[w]
            lines += [f"**{name}** ({rd['question']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}; the bridge token at "
                      f"position {c['pos']} of the prompt", "",
                      "| arm | top token | route | switched | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            for a in ARMS:
                r = reads[(c["scene"], w, None if a == "none" else fixed, a)]
                lines.append(
                    f"| {a} | {r['top_text']!r} | {r['route']} | {r['switched']} | {greedy.get((c['scene'], w, None if a == 'none' else fixed, a))!r} |"
                )
            lines += [
                "",
                "whole by layer: "
                + ", ".join(f"L{la} {reads[(c['scene'], w, la, 'whole')]['route']}" for la in layers),
                "",
            ]
    return lines


def stage_view(runs: list[str]) -> Path:
    unsealed()
    out = RESULTS / f"x47_8-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.8 verify-pack view: prompts (O and S contexts) and every arm's answer at L. UNVERIFIED.", ""]
    for r in runs:
        if (RESULTS / r / "outcomes.jsonl").exists():
            lines += view_lines(r)
    (out / "examples.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def stage_figures(verdict_dir: Path) -> Path:
    from scripts import x47_anatomy_fig as F

    unsealed()
    blob = json.loads((verdict_dir / "x47_8.json").read_text())
    folder = verdict_dir / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-figures"
    folder.mkdir()
    return F.figure([m["figure"] for m in blob["models"] if m["status"] == "tested"], folder / "x47_anatomy.png")


def stage_preview() -> Path:
    """The figure on the existing Fig 6 runs (CPU; the code path the sweep will use), labelled preview."""
    from scripts import x47_anatomy_fig as F

    out = RESULTS / f"preview-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    models = F.preview_models()
    (out / "preview_data.json").write_text(json.dumps(models, indent=1) + "\n")
    path = F.figure(models, out / "x47_anatomy_preview.png", preview=True)
    print(path)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view", "figures", "preview"])
    ap.add_argument("--name", help="run: the run name (results/x47_anatomy/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.8 (jobs/c3/batch47.yaml, amendment 2; Q47.8, sealed)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the 47.8 runs")
    ap.add_argument("--verdict", type=Path, help="figures: the verdict folder (results/x47_anatomy/x47_8-<UTC>)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--layers", type=int, nargs="+", help="run: a sweep other than the target's default (49.4)")
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.n_boot, tuple(a.layers) if a.layers else None)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, a.coverage)
    elif a.stage == "view":
        stage_view(a.runs)
    elif a.stage == "figures":
        assert a.verdict, "figures needs --verdict"
        stage_figures(a.verdict)
    else:
        stage_preview()


if __name__ == "__main__":
    main()
