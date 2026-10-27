"""pointer_fit (D3b): is there a "slot" direction at the last tokens that steers the in-prompt lookup where the lens
push does not?

Background (UNVERIFIED; README "Depth track", D3, pointer_swap d3_main_ae_27b): in memory → prompt, patching the alt
prompt's hidden states into the tokens after the question at layers 44-50 most often gives the answer at the same
statement slot (29% vs 9% for bridge alt's own statement), and the lens push (bridge alt − bridge org) cannot steer
there. If the last tokens carry a pointer to a statement slot, a direction fitted to that slot should steer the lookup.

Design (Qwen3.6-27B; scenes from scripts/pointer_v1.py, 5 statements, animals and elements, the domains that pass the
competence gate):
  collect  fit set (pointer_v1 `fit`: memory → prompt only, scenes never used elsewhere): the hidden states at every
           token after the question (instruction, template, 'Answer:'; the same tokens in every item) at the collect
           layers, labelled by the asked statement's slot (0-4). Only items the model answers right, and only those whose
           queried entity is in a seeded half of each domain's pool (the other half is held out)
  fit      per layer: the slot direction = difference of class means, per token (mean over items asking slot j minus
           the mean over all items); a rank-k subspace (k = 1, 2, 4, 8, 16) = the top principal directions of those
           per-token class-mean deviations (the between-class scatter, unwhitened: LDA's whitening by the within-class
           covariance would upweight low-variance directions, the route to Makelov et al. 2023's illusion); a
           shuffled-label difference of means (labels permuted, seed 1); the span of real activation differences = the
           top 32 principal directions of the per-token-centred fit states; slot decodability (nearest class mean,
           5-fold cross-validation over items)
  steer    held-out main items (other scenes; memory → prompt and, as a control, memory → memory), at each steer layer
           and all of them at once ('window'), at 0.5-4x the per-token norm of the alt-prompt patch there (the D3 alt
           prompt: statements reordered, another entity asked; target slot j = the slot the alt prompt asks, current
           slot a = the asked one): add at every token after the question
             slot      unit(mean_j − mean_a) per token x norm
             sub k     the same difference projected on the rank-k subspace, renormalised
             shuffled  the shuffled-label difference (control: should do nothing)
             random    a random direction per token at the same norm (control)
             lens      the lens push unit(v_bridge alt − v_bridge org), the same at every token
             span / rest   the slot vector split into its part inside the span of real activation differences and the
                       remainder, each added alone at its own norm (illusion control)
             patch     the alt prompt's hidden states pasted at those tokens (reference; no scaling)
           read: suite_split's answer read (one forward, a space appended); roles as pointer_swap (none = answer org kept;
           position = the answer at slot j; identity = bridge alt's statement; value = the alt prompt's own answer)
  geometry per steer layer: cosine of the slot deviations with the J-lens word directions of every entity of both
           pools (and a random-vector null); principal angles between the rank-k subspace and the entities' span (and a
           random-subspace null); the share of each slot deviation inside the J-space (25-atom signed OMP over the
           lens's letter-token vectors) vs a random dictionary of the same size and a random vector
Decision rule (fixed before the 27B run): primary cell = memory → prompt, pooled domains, all held-out items, the slot
direction at layer 48 (D3's slot peak), 1x the alt-prompt patch's norm. "The slot direction steers the lookup where the
lens push does not" iff (a) its slot-target rate (role position) has a Wilson 95% lower bound >= 0.30, and (b) it is at
least 20 points above both the lens push and the random direction at the same norm (point estimate; the paired
bootstrap 95% lower bound of each difference also > 0). Valid only if the shuffled-label direction (memory → prompt)
and the slot direction on memory → memory both keep the slot-target rate's Wilson upper bound <= 0.10 (n >= 35 each).
Illusion flag (reported with the verdict): the out-of-span remainder alone reaches at least half of the full direction's
rate while the in-span part alone stays below half. Reported, not decisive: every layer and the window, every scale,
the rank-k subspaces, the held-out-entity cut (queried entity never queried in the fit), geometry.
Decision rule, pointer_v4 additions (--data pointer_v4; fixed 2026-10-21, before any v4 run): the fit uses pointer_v4's
fit set (fit entities and wordings only: data/pointer_v4/split.json); the steer items are main items whose asked entity
or wording is held out of the fit (cut entity, wording or both; never "neither"), the fit's entity split is the one in
split.json. Every interval the rule reads is the entity-cluster bootstrap 95% interval (asked entity resampled within
each topic, 2000 resamples, seed 0; for the differences, of the per-item paired difference), widened to the item-level
Wilson interval where that is wider (rates only); item-level intervals are reported next to them. The thresholds are
unchanged. Reported, not decisive: per topic, per cut (held-out entity / wording / both), n items / k entities / t
wordings for every primary cell.
Decision rule, sharp C2 step b additions (--ident; fixed 2026-10-22, before any --ident run): the identity direction
  at a steer layer = the per-token mean, over fit items asking entity e, of the states minus their slot's mean (the
  bridge's identity at the tokens after the question with the slot label taken out; entities with >= 3 fit items);
  pushed as unit(identity(bridge alt) - identity(bridge org)) per token at the same norm as the other conditions, on
  memory -> prompt and memory -> memory items whose two bridges both have an identity mean (fit and test are different
  scenes; an entity must be seen in the fit to have a mean, so held-out entities get no identity push). Read in the
  cells scripts/c2_cells.py selected from memory -> memory rows alone (lens on recall >= 0.20, random <= 0.05, patch
  >= 0.20), on memory -> prompt items whose alt prompt asks statement 3-5: "the same bridge is carried by two codes"
  iff the identity push moves >= 0.15 of those lookups to the bridge's statement AND >= 0.20 of the cell's recalls to
  bridge alt's answer (it must be a bridge code, like the lens), while the lens push stays <= random + 0.05 and <= its
  recall rate / 3 and the patch moves >= 0.20; pooled over the selected cells, >= 12 distinct asked entities.

Stages:  run --name N --why W [...]  (manifest.json first, then collect, fit, geometry, steer)
         analyze --name N   figures --name N   examples --name N [--k 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "pointer_fit"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {
    "data": "pointer_v1", "domains": ["animals", "elements"], "collect_layers": [40, 42, 44, 46, 48, 50, 52],
    "steer_layers": [44, 46, 48, 50, 52], "scales": [0.5, 1.0, 2.0, 4.0], "ks": [1, 2, 4, 8, 16], "n_test": 100,
    "rr_n": 50, "fit_limit": None, "span_rank": 32, "primary_layer": 48, "primary_scale": 1.0,
    "competence": "d3_competence_27b",
}  # fmt: skip
DATASETS = ("pointer_v1", "pointer_v4")
N_SLOTS = 5
SPLIT_SEED, SHUFFLE_SEED, SAMPLE_SEED, NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 1, 0, 0, 0, 2000, 0
RATE_MIN, MARGIN, CONTROL_MAX = 0.30, 0.20, 0.10
FOLDS = 5
CONDS_RR = ("slot", "shuffled", "random", "lens")
IDENT_MIN = 3  # --ident: an entity's identity mean needs at least this many fit items
BATCH = PS.BATCH


def conds_for(cfg: dict, family: str) -> tuple[str, ...]:
    """The additive conditions per item: memory → prompt gets every one, memory → memory the four that test the rule;
    --ident adds the identity direction to both."""
    extra = ("ident",) if cfg.get("ident") else ()
    if family == "RR":
        return (*CONDS_RR, *extra)
    return ("slot", *(f"sub{k}" for k in cfg["ks"]), "shuffled", "random", "lens", "span", "rest", *extra)


# ---- pure helpers (tests/test_pointer_fit.py) ---------------------------------------------------------------------


def entity_split(pool: list[str], seed: int = SPLIT_SEED) -> tuple[list[str], list[str]]:
    """(fit half, held-out half) of a domain's entity pool, seeded."""
    order = sorted(pool)
    random.Random(seed).shuffle(order)
    half = (len(order) + 1) // 2
    return sorted(order[:half]), sorted(order[half:])


def class_means(x: torch.Tensor, y: torch.Tensor, n_classes: int = N_SLOTS) -> tuple[torch.Tensor, torch.Tensor]:
    """x [N, P, d], y [N] -> (per-class per-token means [C, P, d], per-token grand mean [P, d]); an empty class is the
    grand mean (no deviation)."""
    m = x.mean(0)
    mu = m.expand(n_classes, *m.shape).clone()
    for c in range(n_classes):
        sel = y == c
        if bool(sel.any()):
            mu[c] = x[sel].mean(0)
    return mu, m


def identity_means(
    x: torch.Tensor, y: torch.Tensor, ents: list[str], mu: torch.Tensor, min_count: int = IDENT_MIN
) -> dict[str, torch.Tensor]:
    """x [N, P, d], slot labels y [N], asked entities ents [N], slot means mu [C, P, d] -> per entity, the per-token mean
    of the states minus their slot's mean (the bridge's identity at these tokens with the slot label taken out); entities
    with fewer than min_count items are left out."""
    resid = x - mu[y]
    out = {}
    for e in sorted(set(ents)):
        sel = torch.tensor([v == e for v in ents], device=x.device)
        if int(sel.sum()) >= min_count:
            out[e] = resid[sel].mean(0)
    return out


def top_directions(rows: torch.Tensor, k: int) -> torch.Tensor:
    """[k, d] orthonormal: the top right singular vectors of rows [n, d] (no centring)."""
    _, _, vh = torch.linalg.svd(rows.float(), full_matrices=False)
    return vh[:k]


def between_basis(mu: torch.Tensor, m: torch.Tensor, k: int) -> torch.Tensor:
    """The rank-k slot subspace: top principal directions of the per-token class-mean deviations [C*P, d]."""
    return top_directions((mu - m).reshape(-1, mu.shape[-1]), k)


def data_span(x: torch.Tensor, m: torch.Tensor, r: int) -> torch.Tensor:
    """Span of real activation differences: top-r principal directions of the per-token-centred states."""
    return top_directions((x - m).reshape(-1, x.shape[-1]), r)


def project(v: torch.Tensor, basis: torch.Tensor) -> torch.Tensor:
    """v [..., d] projected on the row span of an orthonormal basis [k, d]."""
    return (v @ basis.T) @ basis


def unit_rows(v: torch.Tensor) -> torch.Tensor:
    return torch.nn.functional.normalize(v, dim=-1)


def matched(direction: torch.Tensor, norms: torch.Tensor) -> torch.Tensor:
    """Per-token unit direction [P, d] (or [d]) scaled to per-token norms [P]."""
    d = unit_rows(direction).expand(norms.shape[0], -1) if direction.dim() == 1 else unit_rows(direction)
    return d * norms[:, None]


def nearest_mean_cv(x: torch.Tensor, y: torch.Tensor, folds: int = FOLDS, seed: int = 0) -> float:
    """Slot decodability: k-fold accuracy of the nearest per-token class mean (summed squared distance over tokens)."""
    n = x.shape[0]
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    hits = 0
    for f in range(folds):
        test = idx[f::folds]
        train = [i for i in idx if i not in set(test)]
        if not test or not train:
            continue
        tr = torch.tensor(train, device=x.device)
        mu, _ = class_means(x[tr], y[tr])
        present = torch.tensor([bool((y[tr] == c).any()) for c in range(mu.shape[0])], device=x.device)
        for i in test:
            dist = ((x[i][None] - mu) ** 2).sum((1, 2))
            dist[~present] = float("inf")
            hits += int(int(dist.argmin()) == int(y[i]))
    return hits / n


def principal_cosines(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Cosines of the principal angles between the row spans of a [k, d] and b [m, d] (largest first)."""
    qa = torch.linalg.qr(a.float().T)[0]
    qb = torch.linalg.qr(b.float().T)[0]
    return torch.linalg.svdvals(qa.T @ qb)


def boot_diff(a, b, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> list[float]:
    """mean(a) - mean(b) over paired items, item bootstrap [point, lo, hi]."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.size == 0:
        return [math.nan] * 3
    idx = np.random.default_rng(seed).integers(0, a.size, size=(n_boot, a.size))
    d = a[idx].mean(1) - b[idx].mean(1)
    return [float(a.mean() - b.mean()), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]


def statement_spans(text: str, context: str) -> list[tuple[int, int]]:
    """Char spans of the context's statements in a rendered prompt."""
    start = text.index(context)
    out, pos = [], 0
    for sent in re.split(r"(?<=\.) ", context):
        i = context.index(sent, pos)
        out.append((start + i, start + i + len(sent)))
        pos = i + len(sent)
    return out


# ---- items ----------------------------------------------------------------------------------------------------------


def data_gen(cfg: dict):
    """The items' generator: pointer_v1 (the default; older manifests have no 'data') or pointer_v4."""
    import importlib

    return importlib.import_module(f"scripts.{cfg.get('data', 'pointer_v1')}")


def is_v4(cfg: dict) -> bool:
    return cfg.get("data") == "pointer_v4"


def ci_of(cfg: dict) -> dict | None:
    """pointer_v4: the entity-cluster bootstrap (pointer_swap's CLUSTER_CI); else None (Wilson, item bootstrap)."""
    return PS.CLUSTER_CI if is_v4(cfg) else None


def pools(cfg: dict | list[str]) -> dict[str, tuple[list[str], list[str]]]:
    """(fit entities, held-out entities) per domain: pointer_v4's recorded split, else a seeded half of each pool. A
    list of domains (older callers: scripts/pointer_probe.py, pointer_fair.py) means pointer_v1."""
    if isinstance(cfg, list):
        cfg = {"domains": cfg}
    G = data_gen(cfg)
    if is_v4(cfg):
        sp = G.load_split()["domains"]
        return {d: (sp[d]["fit_entities"], sp[d]["held_out_entities"]) for d in cfg["domains"]}
    return {d: entity_split(list(G.DOMAINS[d]["entities"])) for d in cfg["domains"]}


def fit_items(cfg: dict) -> list[dict]:
    G = data_gen(cfg)
    out = []
    for d in cfg["domains"]:
        its = PV.load_file(G.DATA / "fit" / f"{d}_RL_e5f0.json")
        out += its[: cfg["fit_limit"]] if cfg["fit_limit"] else its
    return out


def eligible_main(comp_run: str, cfg: dict | None = None) -> set[str]:
    """Main-set item ids with every competence prompt right (keyed by set: pointer_v1's main and dev reuse ids)."""
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    for line in (data_gen(cfg or {}).RESULTS / comp_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("label", "").startswith("main/"):
            ok[r["id"]].append(r["correct"])
    return {i for i, v in ok.items() if all(v)}


def test_items(cfg: dict) -> list[dict]:
    """Eligible main items, up to n_test (RL) and rr_n (RR) per domain, seeded; pointer_v4: only items whose asked
    entity or wording the fit never saw."""
    G = data_gen(cfg)
    good = eligible_main(cfg["competence"], cfg) if cfg["competence"] else None
    rng = random.Random(SAMPLE_SEED)
    out = []
    for fam, n in (("RL", cfg["n_test"]), ("RR", cfg["rr_n"])):
        for d in cfg["domains"]:
            its = [
                it
                for it in PV.load_file(G.DATA / "main" / f"{d}_{fam}_e5f0.json")
                if (good is None or it["id"] in good) and (not is_v4(cfg) or it["cut"] != "neither")
            ]
            out += [its[i] for i in sorted(rng.sample(range(len(its)), min(n, len(its))))]
    return out


def input_files(cfg: dict) -> list[Path]:
    G = data_gen(cfg)
    files = [G.DATA / "fit" / f"{d}_RL_e5f0.json" for d in cfg["domains"]]
    files += [G.DATA / "main" / f"{d}_{f}_e5f0.json" for d in cfg["domains"] for f in ("RL", "RR")]
    if is_v4(cfg):
        files.append(G.split_file())
    if cfg["competence"]:
        files.append(G.RESULTS / cfg["competence"] / "items.jsonl")
    return files


def rel(p: Path) -> str:
    """A path relative to the repo, or absolute (a smoke's data outside it)."""
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


# ---- the run ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows

    pins.check_run_name(name)
    assert set(cfg["steer_layers"]) <= set(cfg["collect_layers"]), "every steer layer must be a fitted layer"
    assert cfg["primary_layer"] in cfg["steer_layers"], "the primary layer must be a steer layer"
    assert cfg["primary_scale"] in cfg["scales"], "the primary scale must be one of the scales"
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {rel(p): sha256_of(p) for p in input_files(cfg)},
                "entity_split": {d: {"fit": a, "held_out": b} for d, (a, b) in pools(cfg).items()},
                "ci": ci_of(cfg) or {"kind": "wilson; differences: item bootstrap"},
                "seeds": {"split": SPLIT_SEED, "shuffle": SHUFFLE_SEED, "sample": SAMPLE_SEED, "null": NULL_SEED,
                          "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    split = pools(cfg)
    G = data_gen(cfg)
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    # 1. collect
    layers = tuple(cfg["collect_layers"])
    feats: dict[int, list[torch.Tensor]] = {la: [] for la in layers}
    labels, kept, n_fit, fit_ents = [], [], 0, []
    preps = []
    # another target's tokenizer may split a cue differently: items whose prompts are not token-aligned under it are
    # dropped (pointer_swap.drop_unaligned's rule), counted in unaligned.json
    unaligned: collections.Counter = collections.Counter()
    for it in fit_items(cfg):
        try:
            preps.append((it, PS.prepare(it, tok)))
        except AssertionError:
            unaligned[f"fit/{it['domain']}"] += 1
    n_final = {len(p["groups"]["final"]) for _, p in preps}
    assert len(n_final) == 1, f"the tokens after the question differ in number: {n_final}"
    by_len: dict[int, list[tuple[dict, dict]]] = collections.defaultdict(list)
    for it, p in preps:
        by_len[len(p["read_ids"]["base"])].append((it, p))
    chunks = [g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)]
    for chunk in progress(chunks, "collect"):
        ids = torch.tensor([p["read_ids"]["base"] for _, p in chunk], device="cuda")
        logits, rec = forward_rows(model, ids, [{}] * len(chunk), layers)
        for ri, (it, p) in enumerate(chunk):
            n_fit += 1
            right = digit_tok.get(int(logits[ri].argmax())) == it["answer"]
            if (cfg.get("require_correct", True) and not right) or it["query"] not in split[it["domain"]][0]:
                continue
            for la in layers:
                feats[la].append(rec[la][ri, p["groups"]["final"]].half().cpu())
            labels.append(it["slots"]["query"])
            kept.append(it["id"])
            fit_ents.append(it["query"])
    y = torch.tensor(labels, device="cuda")
    print(f"collect: {len(kept)} of {n_fit} fit items kept", flush=True)
    # 2. fit
    fits: dict[int, dict[str, torch.Tensor]] = {}
    idents: dict[int, dict[str, torch.Tensor]] = {}  # --ident: per layer, the asked entities' identity means
    fit_rows = []
    gen_s = torch.Generator().manual_seed(SHUFFLE_SEED)
    y_shuf = y[torch.randperm(len(y), generator=gen_s).to(y.device)]
    for la in layers:
        x = torch.stack(feats[la]).cuda().float()
        mu, m = class_means(x, y)
        mu_s, _ = class_means(x, y_shuf)
        fits[la] = {"mu": mu, "m": m, "basis": between_basis(mu, m, max(cfg["ks"])), "span": data_span(x, m, cfg["span_rank"]),
                    "mu_shuf": mu_s}  # fmt: skip
        ident = identity_means(x, y, fit_ents, mu) if cfg.get("ident") else {}
        dev = (mu - m).norm(dim=-1)
        fit_rows.append({"layer": la, "n": int(x.shape[0]), "per_slot": [int((y == c).sum()) for c in range(N_SLOTS)],
                         "decode_cv": round(nearest_mean_cv(x, y), 4), "decode_cv_shuffled": round(nearest_mean_cv(x, y_shuf), 4),
                         "deviation_norm_median": round(float(dev.median()), 3),
                         "state_norm_median": round(float(x.norm(dim=-1).median()), 2),
                         **({"ident_entities": sorted(ident)} if cfg.get("ident") else {})})  # fmt: skip
        idents[la] = ident
        del x
    cache = pins.CACHE_DIR / EXP / name
    cache.mkdir(parents=True, exist_ok=True)
    torch.save({la: {k: v.cpu() for k, v in f.items()} for la, f in fits.items()}, cache / "fits.pt")
    if cfg.get("ident"):
        torch.save({la: {e: v.cpu() for e, v in d.items()} for la, d in idents.items()}, cache / "idents.pt")
    # 3. geometry
    geometry = []
    ents = sorted({e for d in cfg["domains"] for e in G.DOMAINS[d]["entities"]})
    ent_tok = torch.tensor([model.concept_token(e) for e in ents], device="cuda")
    letters = model.letter_token_ids()
    from scripts.exp04_brew_parts import K_ATOMS, signed_omp

    for la in cfg["steer_layers"]:
        f = fits[la]
        dev = unit_rows((f["mu"] - f["m"]).reshape(-1, f["m"].shape[-1]))
        u = lens.vectors(la, ent_tok)
        g = torch.Generator(device="cuda").manual_seed(NULL_SEED + la)
        rnd = unit_rows(torch.randn(dev.shape, device="cuda", generator=g))
        row: dict[str, Any] = {"layer": la, "n_vectors": int(dev.shape[0]), "entities": len(ents),
                               "max_abs_cos_entity_median": round(float((dev @ u.T).abs().max(1).values.median()), 4),
                               "max_abs_cos_entity_null": round(float((rnd @ u.T).abs().max(1).values.median()), 4),
                               "principal_cos": {}}  # fmt: skip
        for k in cfg["ks"]:
            pc = principal_cosines(f["basis"][:k], u)
            rb = torch.linalg.qr(torch.randn(f["m"].shape[-1], k, device="cuda", generator=g))[0].T
            row["principal_cos"][str(k)] = {
                "top": round(float(pc[0]), 4),
                "null_top": round(float(principal_cosines(rb, u)[0]), 4),
            }
        dictionary = lens.vectors(la, letters)
        share = (signed_omp(dictionary, dev, K_ATOMS).norm(dim=-1) ** 2).median()
        share_rand_vec = (signed_omp(dictionary, rnd, K_ATOMS).norm(dim=-1) ** 2).median()
        rand_dict = unit_rows(torch.randn(dictionary.shape, device="cuda", generator=g))
        del dictionary
        torch.cuda.empty_cache()
        share_rand_dict = (signed_omp(rand_dict, dev, K_ATOMS).norm(dim=-1) ** 2).median()
        del rand_dict
        torch.cuda.empty_cache()
        row |= {"jspace_share_median": round(float(share), 4), "random_dictionary_share_median": round(float(share_rand_dict), 4),
                "random_vector_jspace_share_median": round(float(share_rand_vec), 4)}  # fmt: skip
        geometry.append(row)
    (out_dir / "fit.json").write_text(json.dumps({"kept": len(kept), "of": n_fit, "layers": fit_rows,
                                                  "geometry": geometry}, indent=2) + "\n")  # fmt: skip
    # 4. steer
    tests = []
    for c in test_items(cfg):
        try:
            PS.prepare(c, tok)
            tests.append(c)
        except AssertionError:
            unaligned[f"test/{c['domain']}"] += 1
    (out_dir / "unaligned.json").write_text(json.dumps(dict(unaligned), indent=2) + "\n")
    steer = tuple(cfg["steer_layers"])
    settings: list[tuple[Any, tuple[int, ...]]] = [(la, (la,)) for la in steer] + [("window", steer)]
    out_f = open(out_dir / "outcomes.jsonl", "w")  # noqa: SIM115 - appended item by item, closed below
    cases = []
    n_rows = 0
    for ci, c in enumerate(progress(tests, "steer")):
        p = PS.prepare(c, tok)
        fin = p["groups"]["final"]
        ids = torch.tensor([p["read_ids"]["base"], p["read_ids"]["dissoc"]], device="cuda")
        logits0, rec = forward_rows(model, ids, [{}, {}], steer)
        hb, hs = {la: rec[la][0] for la in steer}, {la: rec[la][1] for la in steer}
        j, a = c["slots"]["position"], c["slots"]["query"]
        q_s, q_b = c["sources"]["dissoc"]["query"], c["query"]
        pair = torch.tensor([model.concept_token(q_b), model.concept_token(q_s)], device="cuda")
        lens_dir = {la: lens.vectors(la, pair) for la in steer}
        lens_dir = {la: v[1] - v[0] for la, v in lens_dir.items()}
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_003 * ci)
        rl = c["family"] != "RR"
        conds = conds_for(cfg, c["family"])
        vec: dict[tuple[int, float, str], torch.Tensor] = {}
        for la in steer:
            f = fits[la]
            base_norm = (hs[la][fin] - hb[la][fin]).norm(dim=-1)
            dm = f["mu"][j] - f["mu"][a]
            for s in cfg["scales"]:
                nn_ = s * base_norm
                sv = matched(dm, nn_)
                vec[(la, s, "slot")] = sv
                vec[(la, s, "shuffled")] = matched(f["mu_shuf"][j] - f["mu_shuf"][a], nn_)
                vec[(la, s, "random")] = PS.null_rows(sv, gen)
                vec[(la, s, "lens")] = matched(lens_dir[la], nn_)
                if q_b in idents.get(la, {}) and q_s in idents[la]:  # --ident: both bridges seen in the fit
                    vec[(la, s, "ident")] = matched(idents[la][q_s] - idents[la][q_b], nn_)
                if rl:
                    for k in cfg["ks"]:
                        vec[(la, s, f"sub{k}")] = matched(project(dm, f["basis"][:k]), nn_)
                    inside = project(sv, f["span"])
                    vec[(la, s, "span")], vec[(la, s, "rest")] = inside, sv - inside
        jobs: list[tuple[dict, dict]] = [({"cond": "unedited", "layer": None, "scale": None}, {})]
        for key, group in settings:
            jobs.append(
                ({"cond": "patch", "layer": key, "scale": None}, {la: PS.SetRows(hs[la][fin], fin) for la in group})
            )
            for s in cfg["scales"]:
                for cn in conds:
                    if any((la, s, cn) not in vec for la in group):  # ident: a bridge not seen in the fit
                        continue
                    jobs.append(
                        (
                            {"cond": cn, "layer": key, "scale": s},
                            {la: PS.AddRows(vec[(la, s, cn)], fin) for la in group},
                        )
                    )
        preds = c["sources"]["dissoc"]["predictions"]
        roles = PS.role_map(c, preds, rl)
        ptok = {h: S.ids(tok, v)[0] for h, v in preds.items()}
        read = torch.tensor([p["read_ids"]["base"]], device="cuda")
        held_out = c["query"] in split[c["domain"]][1]
        wording = PS.wording_of(c)  # pointer_v4: the wording and the held-out cut
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            logits, _ = forward_rows(model, read, [e for _, e in chunk])
            pr = logits.softmax(-1)
            for ri, (tags, _) in enumerate(chunk):
                top = int(logits[ri].argmax())
                digit = digit_tok.get(top)
                o = {"family": c["family"], "domain": c["domain"], "name": c["id"], "held_out_entity": held_out,
                     "entity": q_b, **wording, "slot": PS.slot_class(c), **tags, "top": tok.decode([top]).strip(),
                     "role": roles.get(digit, "other_digit") if digit is not None else "other",
                     "p": {h: round(float(pr[ri, t]), 4) for h, t in ptok.items()}}  # fmt: skip
                out_f.write(json.dumps(o) + "\n")
                n_rows += 1
        cases.append({"id": c["id"], "family": c["family"], "domain": c["domain"], "held_out_entity": held_out,
                      **wording, "question": c["question"],
                      "query_slot": a, "target_slot": j, "query": q_b, "alt_query": q_s, "answer": c["answer"],
                      "predictions": preds, "text": p["text"], "alt_text": p["source_text"], "context": c["context"],
                      "final_chars": [list(p["offsets"][i]) for i in fin],
                      "unedited_top": tok.decode([int(logits0[0].argmax())]).strip()})  # fmt: skip
    out_f.close()
    write_rows(out_dir / "cases.jsonl", cases)
    extra = {"seconds": round(time.time() - t0), "edited_reads": n_rows, "n_cases": len(cases)}
    sm = summarise(load_outcomes(name), cfg, extra)
    (out_dir / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(sm))
    print((out_dir / "summary.md").read_text())


def write_rows(path: Path, rows: list[dict]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def load_outcomes(name: str) -> list[dict]:
    return [json.loads(x) for x in (RESULTS / name / "outcomes.jsonl").read_text().splitlines()]


# ---- analysis ---------------------------------------------------------------------------------------------------------


def cell(rows: list[dict], **where) -> dict[str, dict]:
    return {o["name"]: o for o in rows if all(o.get(k) == v for k, v in where.items())}


def hit(o: dict, role: str = "position") -> float:
    return float(o["role"] == role)


def rate(c: dict[str, dict], role: str = "position", ci: dict | None = None) -> list[float]:
    """[rate, lo, hi, n]: Wilson 95%, or (pointer_v4) the entity-cluster bootstrap widened to Wilson where wider."""
    rows = list(c.values())
    return [*PS.rate_ci([o["role"] == role for o in rows], rows, ci), len(c)]


def paired(c1: dict, c2: dict, role: str = "position", ci: dict | None = None) -> list[float]:
    """Paired difference of the role's share on the items in both cells: item bootstrap, or (pointer_v4) the
    entity-cluster bootstrap of the per-item differences."""
    names = sorted(set(c1) & set(c2))
    if not (ci and names):
        return boot_diff([hit(c1[n], role) for n in names], [hit(c2[n], role) for n in names])
    from bridge_jspace.stats import cluster_bootstrap

    diffs = [hit(c1[n], role) - hit(c2[n], role) for n in names]
    d = cluster_bootstrap(diffs, [(c1[n]["domain"], c1[n]["entity"]) for n in names],
                          [c1[n]["domain"] for n in names], ci["n_boot"], ci["seed"])  # fmt: skip
    return [round(x, 4) for x in d]


def nkt(c: dict[str, dict]) -> list[int]:
    """n items, k asked entities, t wordings of a cell (k, t: 0 where the rows do not record them)."""
    rows = list(c.values())
    return [len(rows), len({(o["domain"], o["entity"]) for o in rows if "entity" in o}),
            len({(o["domain"], o["template"]) for o in rows if "template" in o})]  # fmt: skip


def summarise(rows: list[dict], cfg: dict, extra: dict) -> dict:
    la, sc = cfg["primary_layer"], cfg["primary_scale"]
    ci = ci_of(cfg)
    rl = [o for o in rows if o["family"] == "RL"]
    rr = [o for o in rows if o["family"] == "RR"]
    prim = {cn: cell(rl, cond=cn, layer=la, scale=sc) for cn in conds_for(cfg, "RL")}
    prim["patch"] = cell(rl, cond="patch", layer=la)
    slot = prim["slot"]
    rr_cell = cell(rr, cond="slot", layer=la, scale=sc)
    r_slot, r_lens, r_rand = rate(slot, ci=ci), rate(prim["lens"], ci=ci), rate(prim["random"], ci=ci)
    d_lens, d_rand = paired(slot, prim["lens"], ci=ci), paired(slot, prim["random"], ci=ci)
    shuf, rr_slot = rate(prim["shuffled"], ci=ci), rate(rr_cell, ci=ci)
    span_r, rest_r = rate(prim["span"], ci=ci), rate(prim["rest"], ci=ci)
    held = rate({n: o for n, o in slot.items() if o["held_out_entity"]}, ci=ci)
    seen = rate({n: o for n, o in slot.items() if not o["held_out_entity"]}, ci=ci)
    v4: dict[str, Any] = {}
    if ci:  # pointer_v4: item-level intervals next to the cluster ones, n / k / t, per topic and per held-out cut
        v4 = {
            "ci": ci,
            "item_level": {"slot": rate(slot), "lens": rate(prim["lens"]), "random": rate(prim["random"]),
                           "shuffled": rate(prim["shuffled"]), "rr_slot": rate(rr_cell),
                           "slot_minus_lens": paired(slot, prim["lens"]), "slot_minus_random": paired(slot, prim["random"])},
            "n_k_t": {"slot": nkt(slot), "lens": nkt(prim["lens"]), "random": nkt(prim["random"]),
                      "shuffled": nkt(prim["shuffled"]), "rr_slot": nkt(rr_cell)},
            "per_domain": {d: {"slot": rate(s_d := {n: o for n, o in slot.items() if o["domain"] == d}, ci=ci),
                               "lens": rate({n: o for n, o in prim["lens"].items() if o["domain"] == d}, ci=ci),
                               "random": rate({n: o for n, o in prim["random"].items() if o["domain"] == d}, ci=ci),
                               "n_k_t": nkt(s_d)} for d in cfg["domains"]},
            "per_cut": {cut: {"slot": rate(s_c := {n: o for n, o in slot.items() if o.get("cut") == cut}, ci=ci),
                              "n_k_t": nkt(s_c)} for cut in ("entity", "template", "both")},
        }  # fmt: skip
    ok_a = r_slot[1] >= RATE_MIN
    ok_b = d_lens[0] >= MARGIN and d_rand[0] >= MARGIN and d_lens[1] > 0 and d_rand[1] > 0
    valid = shuf[2] <= CONTROL_MAX and rr_slot[2] <= CONTROL_MAX and shuf[3] >= 35 and rr_slot[3] >= 35
    illusion = rest_r[0] >= 0.5 * r_slot[0] > 0 and span_r[0] < 0.5 * r_slot[0]
    verdict = ("the slot direction steers the lookup where the lens push does not" if ok_a and ok_b else
               "not shown: the slot direction does not steer the lookup by the rule")  # fmt: skip
    if not valid:
        verdict += " (controls failed: not interpretable)"
    grid: dict[str, Any] = {}
    for fam, rows_f, conds in (
        ("RL", rl, (*conds_for(cfg, "RL"), "patch")),
        ("RR", rr, (*conds_for(cfg, "RR"), "patch")),
    ):
        for cn in conds:
            for key in [*cfg["steer_layers"], "window"]:
                for s in [None] if cn == "patch" else cfg["scales"]:
                    c_ = cell(rows_f, cond=cn, layer=key, scale=s)
                    if c_:
                        roles = collections.Counter(o["role"] for o in c_.values())
                        grid[f"{fam}|{cn}|{key}|{s}"] = {"position": rate(c_), "roles": dict(roles)}
    unedited = cell(rows, cond="unedited")
    return {"primary": {"layer": la, "scale": sc, "slot": r_slot, "lens": r_lens, "random": r_rand,
                        "slot_minus_lens": d_lens, "slot_minus_random": d_rand, "shuffled": shuf, "rr_slot": rr_slot,
                        "span_only": span_r, "rest_only": rest_r, "held_out_entities": held, "seen_entities": seen,
                        "patch": rate(prim["patch"]), **{f"sub{k}": rate(prim[f"sub{k}"]) for k in cfg["ks"]}},
            "checks": {"a_lower_bound_ge_0.30": ok_a, "b_20_points_above_lens_and_random": ok_b,
                       "controls_valid": valid, "illusion_flag": illusion,
                       "unedited_answer_org": round(statistics.mean(o["role"] == "none" for o in unedited.values()), 4) if unedited else None},
            "verdict": verdict, "grid": grid, **({"pointer_v4": v4} if v4 else {}), **extra}  # fmt: skip


def summary_md(sm: dict) -> str:
    p = sm["primary"]

    def r(x):
        return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}] (n={x[3]})"

    def d(x):
        return f"{100 * x[0]:+.0f} [{100 * x[1]:+.0f}, {100 * x[2]:+.0f}] pts"

    lines = [f"# {EXP}", "", f"Verdict: **{sm['verdict']}**", "", f"Checks: {json.dumps(sm['checks'])}", "",
             f"Primary cell (memory → prompt, layer {p['layer']}, {p['scale']:g}x): % answers that become the answer at slot j",
             "", "| condition | rate |", "|---|---|"]  # fmt: skip
    for k in ("slot", "lens", "random", "shuffled", "rr_slot", "span_only", "rest_only", "held_out_entities",
              "seen_entities", "patch", *[k for k in p if k.startswith("sub")]):  # fmt: skip
        lines.append(f"| {k} | {r(p[k])} |")
    lines += ["", f"slot - lens {d(p['slot_minus_lens'])}; slot - random {d(p['slot_minus_random'])}"]
    v4 = sm.get("pointer_v4")
    if v4:
        il, nk = v4["item_level"], v4["n_k_t"]
        lines += ["", "Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where "
                  "wider. Item level and n items / k entities / t wordings:", "",
                  "| condition | item level | n / k / t |", "|---|---|---|"]  # fmt: skip
        lines += [f"| {k} | {r(il[k])} | {' / '.join(map(str, nk[k]))} |" for k in nk]
        lines += [
            f"| slot - lens | {d(il['slot_minus_lens'])} | |",
            f"| slot - random | {d(il['slot_minus_random'])} | |",
        ]
        lines += ["", "| topic | slot | lens | random | n / k / t |", "|---|---|---|---|---|"]
        lines += [f"| {t} | {r(x['slot'])} | {r(x['lens'])} | {r(x['random'])} | {' / '.join(map(str, x['n_k_t']))} |"
                  for t, x in v4["per_domain"].items()]  # fmt: skip
        lines += ["", "| held out of the fit | slot | n / k / t |", "|---|---|---|"]
        lines += [f"| {c} | {r(x['slot'])} | {' / '.join(map(str, x['n_k_t']))} |" for c, x in v4["per_cut"].items()]
    return "\n".join(lines) + "\n"


def stage_analyze(name: str) -> Path:
    m = json.loads((RESULTS / name / "manifest.json").read_text())
    sm = summarise(load_outcomes(name), m["config"], {})
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(sm))
    print(out)
    return out


# ---- figures ------------------------------------------------------------------------------------------------------------

COND_WORDS = {"slot": "slot direction", "lens": "lens push (bridge alt − bridge org)", "random": "random push (same size)",
              "shuffled": "shuffled-label direction", "patch": "patch from the alt prompt", "span": "slot direction, part "
              "inside real activation differences", "rest": "slot direction, the remainder"}  # fmt: skip
COND_COLOURS = {"slot": "#2a78d6", "lens": "#eb6834", "patch": "#1baf7a"}


def save_fig(fig, out: Path, stem: str, title: str, explain: list[tuple[str, str]], data: str, handles=None, ncols=None,
             figs: list[str] | None = None) -> None:  # fmt: skip
    """plotting.finish's frame with its labelled caption rows; 200-dpi PNG and SVG."""
    import textwrap

    import matplotlib.pyplot as plt

    from bridge_jspace import plotting as PL

    h, w = fig.get_figheight(), fig.get_figwidth()
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=PL.INK)
    label_w, y = 1.05, 0.38
    for label, text in [*explain, ("Data", data)]:
        lines = textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]
        fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=PL.INK, fontweight="bold")
        fig.text(
            label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=PL.MUTED, linespacing=1.4
        )
        y += 0.155 * len(lines) + 0.05
    rows_ = -(-len(handles) // (ncols or len(handles))) if handles else 0
    foot = 0.2 + 0.25 * rows_ if handles else 0.05
    if handles:
        fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=9,
                   handlelength=2.6, labelcolor=PL.INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - (y + 0.1) / h))
    out.mkdir(exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(out / f"{stem}.{ext}", dpi=200, facecolor=PL.SURFACE)
    plt.close(fig)
    if figs is not None:
        figs.append(f"{stem}.png")


def example_text(cases: list[dict]) -> str:
    c = next((x for x in cases if x["family"] == "RL"), None)
    if c is None:
        return ""
    q = c.get("question") or c["text"][c["text"].rindex("Which") :].split("?")[0] + "?"  # older runs: no question
    sents = re.split(r"(?<=\.) ", c["context"])
    return (f"\"{sents[c['query_slot']]} ... {sents[c['target_slot']]} ... {q}\" -> answer org {c['answer']} (statement "
            f"{c['query_slot'] + 1}); pushing toward statement {c['target_slot'] + 1} should give "
            f"{c['predictions']['position']}.")  # fmt: skip


def stage_figures(name: str) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as PL

    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    cfg = m["config"]
    for old in d.glob("analysis-*-figures"):  # one figures folder per run: a redraw replaces it
        for f in old.iterdir():
            f.unlink()
        old.rmdir()
    out = d / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    rows = load_outcomes(name)
    cases = [json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines()]
    fitj = json.loads((d / "fit.json").read_text())
    sm = summarise(rows, cfg, {})
    model_name = m["model"]["repo"].split("/")[-1]
    flips = PL.TERM["flips"].replace(
        "the alternative answer (answer org → answer alt)", "the answer at the target slot"
    )
    keys = [*cfg["steer_layers"], "window"]
    xs = np.arange(len(keys))
    xl = [str(k) for k in cfg["steer_layers"]] + ["all"]
    figs: list[str] = []
    n_rl = len({c["id"] for c in cases if c["family"] == "RL"})
    n_rr = len({c["id"] for c in cases if c["family"] == "RR"})
    ex = example_text(cases)
    ci = ci_of(cfg)
    ci_text = "Wilson 95%"
    held_lab, seen_lab = "slot direction, held-out entities", "slot direction, entities seen in the fit"
    if ci:  # pointer_v4: entities and wordings next to n, cluster intervals; every steered item is held out somehow
        rl_c = [c for c in cases if c["family"] == "RL"]
        n_rl = (f"{n_rl} ({len({(c['domain'], c['query']) for c in rl_c})} asked entities, "
                f"{len({(c['domain'], c.get('template')) for c in rl_c})} wordings, all held out of the fit by entity or "
                "wording)")  # fmt: skip
        ci_text = (
            "entity-cluster bootstrap 95% (asked entity resampled within each topic), widened to Wilson where wider"
        )
        held_lab = "slot direction, entity held out (wording held out or not)"
        seen_lab = "slot direction, entity seen in the fit, wording held out"

    # 1. headline: slot direction vs lens push vs random vs patch, by layer and size
    # at least 12.6 in wide (fewer sizes would clip the legend) and tall enough for the caption and two panel rows
    fig, axes = plt.subplots(
        2, len(cfg["scales"]), figsize=(max(4.2 * len(cfg["scales"]), 12.6), 9.6), sharey=True, squeeze=False
    )
    for i, (fam, rows_f) in enumerate((("RL", rows), ("RR", rows))):
        for jx, s in enumerate(cfg["scales"]):
            ax = axes[i][jx]
            PL.style_axes(ax)
            PL.percent_axis(ax)
            for k_, cn in enumerate(("slot", "lens", "random", "shuffled", "patch")):
                vals = []
                for key in keys:
                    c_ = cell(
                        [o for o in rows_f if o["family"] == fam],
                        cond=cn,
                        layer=key,
                        scale=None if cn == "patch" else s,
                    )
                    vals.append(rate(c_, ci=ci)[:3] if c_ else [math.nan] * 3)
                v = np.array(vals, float)
                colour = COND_COLOURS.get(cn, PL.MUTED)
                ls = "--" if cn in ("random", "shuffled") else "-"
                ax.errorbar(xs + (k_ - 2) * 0.08, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None),
                            color=colour, ls=ls, lw=2 if ls == "-" else 1.2, marker="o", ms=4,
                            mfc=PL.SURFACE if cn == "shuffled" else colour, elinewidth=1, capsize=0)  # fmt: skip
            ax.set_xticks(xs, xl)
            ax.set_ylim(-0.04, 1.04)
            if i == 0:
                ax.set_title(f"{s:g}x the alt-prompt patch's size", fontsize=9.5, color=PL.INK, loc="left")
            if jx == 0:
                ax.set_ylabel(f"{PL.family_label(fam)}\n" + "\n".join(_wrap(flips, 46)), fontsize=8.5, color=PL.INK)
            if i == 1:
                ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
    handles = [Line2D([], [], color=COND_COLOURS["slot"], lw=2, marker="o", label=COND_WORDS["slot"]),
               Line2D([], [], color=COND_COLOURS["lens"], lw=2, marker="o", label=COND_WORDS["lens"]),
               Line2D([], [], color=COND_COLOURS["patch"], lw=2, marker="o", label=COND_WORDS["patch"] + " (not rescaled)"),
               Line2D([], [], color=PL.MUTED, ls="--", marker="o", label="control: " + COND_WORDS["random"]),
               Line2D([], [], color=PL.MUTED, ls="--", marker="o", mfc=PL.SURFACE, label="control: " + COND_WORDS["shuffled"])]  # fmt: skip
    explain = [("What we did", "Added a fitted 'slot' direction (the target statement minus the asked one) to the tokens after "
                               "the question, at one layer (or all), sized like the alt-prompt patch there; compared with "
                               "the lens push and a random push of the same size."),
               ("Example", ex),
               ("How to read", "Each dot: the share of items whose answer becomes the answer at the target slot. Top: "
                               "memory → prompt (a lookup); bottom: memory → memory (no lookup: the direction should do nothing)."),
               ("Control", "Dashed: a random push and a direction fitted with shuffled slot labels, same size; both should "
                           "stay near 0%.")]  # fmt: skip
    save_fig(fig, out, "fig1_slot_direction_vs_lens", "Does a fitted slot direction steer the lookup where the lens push does not?",
             explain, f"{model_name}; held-out scenes: {n_rl} memory → prompt and {n_rr} memory → memory items; error bars: {ci_text}.",
             handles, ncols=3, figs=figs)  # fmt: skip

    # 2. the decision: primary cell and its controls
    p = sm["primary"]
    bars = [("slot direction", p["slot"]), ("lens push (bridge alt − bridge org)", p["lens"]),
            ("random push (same size)", p["random"]), ("shuffled-label direction", p["shuffled"]),
            ("slot direction on memory → memory", p["rr_slot"]), (held_lab, p["held_out_entities"]),
            (seen_lab, p["seen_entities"]),
            ("part inside real activation differences", p["span_only"]), ("the remainder", p["rest_only"]),
            *[(f"rank-{k[3:]} slot subspace", p[k]) for k in p if k.startswith("sub")],
            ("patch from the alt prompt (not rescaled)", p["patch"])]  # fmt: skip
    fig, ax = plt.subplots(figsize=(10, 6.2))
    PL.style_axes(ax)
    PL.percent_axis(ax, "x")
    ys = np.arange(len(bars))[::-1]
    for y_, (lab, r_) in zip(ys, bars, strict=True):
        ctrl = lab.startswith(("random", "shuffled", "slot direction on memory"))
        if not math.isnan(r_[0]):
            ax.barh(y_, r_[0], height=0.62, color=PL.MUTED if ctrl else "#52514e", zorder=2)
            ax.errorbar(
                r_[0],
                y_,
                xerr=np.clip([[r_[0] - r_[1]], [r_[2] - r_[0]]], 0, None),
                color=PL.INK,
                elinewidth=0.9,
                capsize=0,
                zorder=3,
            )
            ax.text(min(r_[2], 1) + 0.02, y_, f"{100 * r_[0]:.0f}% (n={r_[3]})", va="center", fontsize=8, color=PL.INK)
    ax.axvline(RATE_MIN, color=PL.MUTED, ls=":", lw=1)
    ax.axvline(CONTROL_MAX, color=PL.MUTED, ls="--", lw=1)
    ax.set_yticks(ys, [b[0] for b in bars], fontsize=8.5, color=PL.INK)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("\n".join(_wrap(flips, 70)), fontsize=9, color=PL.MUTED)
    explain = [("What we did", f"The pre-registered cell: memory → prompt, layer {p['layer']}, {p['scale']:g}x the alt-prompt "
                               "patch's size, next to its controls."),
               ("Example", ex),
               ("How to read", f"Verdict: '{sm['verdict']}'. Dotted line: the rule's 30% bar for the slot direction's lower "
                               "bound; dashed: the 10% bar the controls must stay under."),
               ("Control", "Gray bars: random push, shuffled-label direction, memory → memory items; the two parts of the "
                           "slot direction test for an illusion (an effect carried only by the remainder).")]  # fmt: skip
    save_fig(fig, out, "fig2_decision_cell", "Does the slot direction pass the pre-registered test?", explain,
             f"{model_name}; held-out scenes; error bars: {ci_text}. Slot minus lens push {100 * p['slot_minus_lens'][0]:+.0f} "
             f"[{100 * p['slot_minus_lens'][1]:+.0f}, {100 * p['slot_minus_lens'][2]:+.0f}] points; minus random "
             f"{100 * p['slot_minus_random'][0]:+.0f} [{100 * p['slot_minus_random'][1]:+.0f}, {100 * p['slot_minus_random'][2]:+.0f}] "
             f"({'entity-cluster' if ci else 'item'} bootstrap).", figs=figs)  # fmt: skip

    # 3. geometry: decodability, entity cosines, principal angles, J-space share
    fig, axes = plt.subplots(1, 3, figsize=(15, 6.0))  # room for the caption rows above the panels
    lay = [r_["layer"] for r_ in fitj["layers"]]
    ax = axes[0]
    PL.style_axes(ax)
    PL.percent_axis(ax)
    ax.plot(
        lay,
        [r_["decode_cv"] for r_ in fitj["layers"]],
        color=COND_COLOURS["slot"],
        lw=2,
        marker="o",
        label="true slot labels",
    )
    ax.plot(
        lay,
        [r_["decode_cv_shuffled"] for r_ in fitj["layers"]],
        color=PL.MUTED,
        ls="--",
        marker="o",
        label="control: shuffled labels",
    )
    ax.axhline(1 / N_SLOTS, color=PL.MUTED, ls=":", lw=1)
    ax.set_ylim(0, 1.04)
    ax.set_xlabel("layer", fontsize=9, color=PL.MUTED)
    ax.set_title("which statement is asked, read from the last tokens", fontsize=9.5, color=PL.INK, loc="left")
    ax.set_ylabel("cross-validated accuracy (5 slots; chance 20%)", fontsize=9, color=PL.INK)
    ax.legend(frameon=False, fontsize=8)
    geo = fitj["geometry"]
    gl = [g["layer"] for g in geo]
    ax = axes[1]
    PL.style_axes(ax)
    ax.plot(
        gl,
        [g["max_abs_cos_entity_median"] for g in geo],
        color=COND_COLOURS["slot"],
        lw=2,
        marker="o",
        label="slot directions (one statement vs the mean)",
    )
    ax.plot(
        gl,
        [g["max_abs_cos_entity_null"] for g in geo],
        color=COND_COLOURS["slot"],
        ls="--",
        marker="o",
        mfc=PL.SURFACE,
        label="control: random directions",
    )
    for k, colour in ((4, "#eb6834"), (16, "#1baf7a")):
        if str(k) not in geo[0]["principal_cos"]:
            continue
        ax.plot(gl, [g["principal_cos"][str(k)]["top"] for g in geo], color=colour, lw=2, marker="o",
                label=f"rank-{k} slot subspace (smallest angle)")  # fmt: skip
        ax.plot(gl, [g["principal_cos"][str(k)]["null_top"] for g in geo], color=colour, ls="--", marker="o",
                mfc=PL.SURFACE, label=f"control: random rank-{k} subspace")  # fmt: skip
    ax.set_ylim(0, 0.6)
    ax.set_xlabel("layer", fontsize=9, color=PL.MUTED)
    ax.set_title("alignment with the entities' lens word directions", fontsize=9.5, color=PL.INK, loc="left")
    ax.set_ylabel("largest |cosine|", fontsize=9, color=PL.INK)
    ax.legend(frameon=False, fontsize=7)
    ax = axes[2]
    PL.style_axes(ax)
    PL.percent_axis(ax)
    ax.plot(
        gl,
        [g["jspace_share_median"] for g in geo],
        color=COND_COLOURS["slot"],
        lw=2,
        marker="o",
        label="slot directions, lens-readable part",
    )
    ax.plot(
        gl,
        [g["random_dictionary_share_median"] for g in geo],
        color=PL.MUTED,
        ls="--",
        marker="o",
        label="control: random dictionary",
    )
    ax.plot(
        gl,
        [g["random_vector_jspace_share_median"] for g in geo],
        color=PL.MUTED,
        ls=":",
        marker="o",
        label="control: random vector",
    )
    ax.set_ylim(0, 1)
    ax.set_xlabel("layer", fontsize=9, color=PL.MUTED)
    ax.set_title("share inside the lens-readable space (25 words)", fontsize=9.5, color=PL.INK, loc="left")
    ax.set_ylabel("share of the direction's squared length", fontsize=9, color=PL.INK)
    ax.legend(frameon=False, fontsize=7)
    fit_set = ("fit entities (two thirds of each topic) and two of the three wordings only" if ci
               else "queried entity in the fitting half")  # fmt: skip
    explain = [("What we did", f"Fitted per-token slot means on the fit scenes ({fit_set}), then "
                               "compared the slot directions with the lens's word directions for the entities."),
               ("Example", ex),
               ("How to read", "Left: is the asked slot readable at all. Middle: does the slot direction point along an "
                               "entity's word direction. Right: how much of it a 25-word lens fit explains."),
               ("Control", "Dashed: shuffled labels, random directions, a random dictionary of the same size.")]  # fmt: skip
    save_fig(fig, out, "fig3_geometry", "Is the slot code readable, and is it made of the lens's word directions?", explain,
             f"{model_name}; {fitj['kept']} of {fitj['of']} fit items (answered right; {fit_set}); "
             "medians over slots x tokens.", figs=figs)  # fmt: skip
    (out / "summary.json").write_text(json.dumps({"run": name, "verdict": sm["verdict"], "checks": sm["checks"],
                                                  "primary": sm["primary"], **({"pointer_v4": sm["pointer_v4"]} if ci else {}),
                                                  "fit": fitj, "figures": figs}, indent=2) + "\n")  # fmt: skip
    print(out)
    return out


def _wrap(text: str, width: int) -> list[str]:
    import textwrap

    return textwrap.wrap(text, width)


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    m = json.loads((d / "manifest.json").read_text())
    la, sc = m["config"]["primary_layer"], m["config"]["primary_scale"]
    rows = load_outcomes(name)
    cases = {c["id"]: c for c in (json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines())}
    slot = cell([o for o in rows if o["family"] == "RL"], cond="slot", layer=la, scale=sc)
    groups = {"slot_answer": "the slot direction gives the answer at the target slot",
              "kept": "the slot direction leaves answer org", "other": "the slot direction gives another answer"}  # fmt: skip
    members: dict[str, list[str]] = {g: [] for g in groups}
    for n, o in slot.items():
        members["slot_answer" if o["role"] == "position" else "kept" if o["role"] == "none" else "other"].append(n)
    rng = np.random.default_rng(seed)
    examples = []
    for g, names in members.items():
        for n in (
            [names[i] for i in sorted(rng.choice(len(names), size=min(k, len(names)), replace=False))] if names else []
        ):
            c = cases[n]
            spans = statement_spans(c["text"], c["context"])
            base_spans = [{"start": spans[c["query_slot"]][0], "end": spans[c["query_slot"]][1], "role": "asked statement"},
                          {"start": spans[c["target_slot"]][0], "end": spans[c["target_slot"]][1], "role": "target slot"},
                          {"start": c["final_chars"][0][0], "end": c["final_chars"][-1][1], "role": "pushed tokens"}]  # fmt: skip
            for cn in ("slot", "lens", "random", "shuffled", "patch"):
                o = cell(rows, cond=cn, layer=la, scale=None if cn == "patch" else sc).get(n)
                if o is None:
                    continue
                examples.append({"group": g, "family": c["family"], "item_id": n, "prompt": c["text"] + " ", "spans": base_spans,
                                 "condition": f"{COND_WORDS[cn]} at layer {la}" + ("" if cn == "patch" else f", {sc:g}x the patch's size"),
                                 "answers": {"clean": c["predictions"]["none"], "edited": o["top"],
                                             "expected": {"H-slot": c["predictions"]["position"] if cn in ("slot", "patch") else c["predictions"]["none"],
                                                          "H-word": c["predictions"]["identity"] if cn in ("lens", "patch") else c["predictions"]["none"]}},
                                 "numbers": {"role": o["role"], **{f"p_{h}": v for h, v in o["p"].items()}},
                                 "why": f"{groups[g]} (asked statement {c['query_slot'] + 1}, target {c['target_slot'] + 1})"})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--data", default=DEFAULTS["data"], choices=list(DATASETS), help="the items' generator")
    ap.add_argument(
        "--domains", nargs="+", default=None, help="default: pointer_v1 animals elements; pointer_v4 all used"
    )
    for key in ("collect_layers", "steer_layers", "ks"):
        ap.add_argument("--" + key.replace("_", "-"), nargs="+", type=int, default=DEFAULTS[key])
    ap.add_argument("--scales", nargs="+", type=float, default=DEFAULTS["scales"])
    for key in ("n_test", "rr_n", "span_rank", "primary_layer"):
        ap.add_argument("--" + key.replace("_", "-"), type=int, default=DEFAULTS[key])
    ap.add_argument("--primary-scale", type=float, default=DEFAULTS["primary_scale"])
    ap.add_argument("--fit-limit", type=int, default=None, help="fit items per domain (a smoke: few)")
    ap.add_argument("--competence", default=None, help="the --data generator's competence run (pointer_v1 default: "
                    f"{DEFAULTS['competence']}; pointer_v4: required)")  # fmt: skip
    ap.add_argument("--no-eligibility", action="store_true", help="a smoke on another model: no competence filter")
    ap.add_argument(
        "--keep-wrong", action="store_true", help="a smoke on a weak model: fit on items it answers wrong too"
    )
    ap.add_argument("--ident", action="store_true", help="add the identity direction (sharp C2, step b)")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        assert set(args.ks) <= set(DEFAULTS["ks"]), "ks must be a subset of the defaults (the conditions are fixed)"
        v4 = args.data == "pointer_v4"
        domains = args.domains or (list(data_gen({"data": args.data}).DOMAINS) if v4 else DEFAULTS["domains"])
        competence = args.competence or (None if v4 else DEFAULTS["competence"])
        assert competence or args.no_eligibility, "pointer_v4 needs --competence RUN (or --no-eligibility for a smoke)"
        config = {"data": args.data, "domains": domains, "collect_layers": args.collect_layers, "steer_layers": args.steer_layers,
                  "scales": args.scales, "ks": args.ks, "n_test": args.n_test, "rr_n": args.rr_n, "fit_limit": args.fit_limit,
                  "span_rank": args.span_rank, "primary_layer": args.primary_layer, "primary_scale": args.primary_scale,
                  "competence": None if args.no_eligibility else competence,
                  "require_correct": not args.keep_wrong, **({"ident": True} if args.ident else {})}  # fmt: skip
        stage_run(args.name, args.why, config)
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
