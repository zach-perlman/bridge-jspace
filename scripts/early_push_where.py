"""early_push_where (D4 v2, 2026-10-22): can the lens write a STATED bridge where it sits?

Background (UNVERIFIED; README slide 6): at layer 20 on Qwen3.6-27B, a lens push v_X - v_I (8x) on the question's
subject phrase switches bridges the model recalls (memory -> prompt 73%, memory -> memory 84%) but not bridges stated in
the prompt (prompt -> prompt 1%, prompt -> memory 2%). The stated bridge was pushed at the question, but it sits at its
own sentence ("Clara's pet is a cow.") until layer ~24 and over the whole context until ~44 (statement_positions
d1_map_n80_v1). The null for stated bridges may only mean that the push missed the bridge.

Design. Animal suite (wording A), the four families on the same scenes (suite_split map_A8_v1's cases, the first n per
family), Qwen3.6-27B, J++. Push positions of the unedited prompt:
  b  the question's subject phrase ("Clara's pet", "the animal known for mooing"): slide 6's own (replication anchor)
  s  the bridge's owner sentence ("Clara's pet is a cow."): where a stated bridge sits early
  w  the bridge's word in that sentence ("cow")
  c  the whole context (every sentence), layers 28-44 only: where a stated bridge sits later
At each layer of L (12-44, every 4) and scale of S (1, 2, 4, 8), each pushed position gets scale x the scene's reference
norm (early_push's: the RMS of C's copy delta over suite_split's question group, pooled over the scene's families), along
  lens      v_X - v_I (unit J++ vectors at that layer; X = the bridge of the C prompt)
  random    a random direction at the same per-position norms (one generator per item)
  offscene  v_Y - v_I, Y an animal not in the scene whose leg count differs from I's and X's (one Y per scene, seeded)
Text edits as early_push (E-name, E-insert, E-head, E-cue, E-unrelated); E-cue is the C prompt, which for prompt -> *
rebinds the stated sentence to X: the input-edit limit at s. Read: suite_split's (the top token after 'Answer:' and a
space): A (unchanged), b (X's answer), y (Y's legs; recall families only), oc (another in-context answer), other.
Families: prompt -> memory (BR) is the positive control (a stated bridge, a recalled answer: D1 found that the
lens-readable part of a stated bridge's change does the work there, 66%); prompt -> prompt (BL) is the test; memory ->
prompt and memory -> memory (RL, RR) are off the path at s and w (their bridge comes from the cue) and the replication
anchor at b. Only items the model answers right unedited count.

Decision rule (fixed 2026-10-22 before the run; the controls agreed with Dan):
  select   on BR rows only: cells (subset s or w, layer, scale) where the lens push switches BR to X's answer in >= 30%
           with Wilson lower bound >= 0.20, and the random push switches <= 5%. Primary cell: the selected cell with the
           highest BR rate (ties: smaller scale, earlier layer, w before s). No selected cell: the lens does not write a
           stated bridge at its sentence even for recall, and BL is not interpretable there (reported).
  valid    at the primary cell, the lens push changes <= 10% of RL and of RR answers (off the path), and the random
           push switches <= 5% of BL.
  verdict  H-where (the stated null of slide 6 was a location artefact): BL switched >= 30% with lower bound >= 0.20.
           H-around (consistent with D1: the lookup does not use the lens-writable form of a stated bridge): BL switched
           <= 10% and the scene-paired bootstrap of BR - BL has its 2.5th percentile >= 0.20. Otherwise inconclusive.
  reported, not decisive: every cell; c; b at layer 20, 8x against slide 6 (RL 73%, RR 84%, BL 1%, BR 2%); offscene
           (BR to Y's legs, BL changed); the edits.

Rule v2 (fixed 2026-10-22 evening, after d4_where_27b and before the fresh-scene run; config "rule": "v2"). In
d4_where_27b the primary cell (w, layer 28, 8x) changed 25% of RR, so the verdict was "not valid" while other cells
passed. v2 moves the validity conditions into the selection: a cell is selected iff it passes v1's selection AND, at
that cell, the lens push changes <= 10% of RL and of RR and the random push switches <= 5% of BL. The primary cell is
the selected cell with the highest BR rate (v1's ties); the verdicts are v1's. Runs without "rule" in their config use
v1. Fresh scenes (config "scenes": "fresh"): n scenes sampled (seed FRESH_SEED) from those eligible in all four
families under suite_split's rule (every competence prompt right) and not in the map run at all.

Rule v2.1 (amended 2026-10-22 20:35 +0200, Dan, while d4_where_fresh_27b ran and before any of its results was
opened): v2 applied to d4_where_27b (already opened) picks the word at layer 16, 8x (recall 90%, lookup 20%:
inconclusive), while every valid cell at layers 20-36 has lookup 0%; at layer 16 the push moves lookups too (an input
edit by another name, or the lens writing the lookup early: open). So v2.1 = v2 with the decisive cell chosen among
valid cells at layers >= 20 (V21_MIN_LAYER); the valid cells below 20 are reported separately (below_v21). v2.1 was
written knowing the old data, so v2 stays the main rule (revised 20:55): both verdicts are reported, and a
disagreement is stated as such. v2.1 is written by `analyze --name N --rule v2.1` into <run>/analysis-v2.1-<stamp>/
(the run's own summary keeps v2).

Layer-gap test (22 Oct 23:15, the outside review, before the run; `--patch`): at the stated bridge's word (w) and
sentence (s), every second layer 12-34, the lens push (4x, 8x), a random push (8x) and the full patch of C's residual
at those positions (its own size; C rebinds the sentence to X). lens_stop = the first grid layer from which the lens
push (the larger of 4x and 8x) switches <= 5% of prompt -> prompt lookups at that and every later grid layer;
patch_stop the same for the patch. At w: H-gap (between the two, the lookup's bridge is in the residual at the word but
outside the lens) iff patch_stop - lens_stop >= 6 layers and the patch switches >= 30% of lookups (Wilson lower bound
>= 0.20) at lens_stop; H-no-gap iff patch_stop - lens_stop <= 2; else inconclusive. Valid only if the random push
switches <= 5% of lookups at every grid layer. Reported: s the same way, the recall (BR) curves, the off-scene push.
Prior (the review's guess): lens_stop ~18-20, patch_stop ~30; the D1 map's patch at the sentence moves 0% of lookups
from layer 32 on (d1_map_n80_v1), so patch_stop <= 32 is expected.

Layer-gap test v2 (Dan, 22 Oct 23:30, before its run d4_layer_gap_v2_27b; flags --patch --embed --gap-rule v2): a fourth
arm, the input-embedding difference W_E[X] - W_E[I] at the lens push's norms (is the layer-16 effect an input edit?).
Each arm's valid cells: v2's off-path check with that arm's own rows. An arm STOPS at a layer iff at every valid cell
of that layer its lookup switch rate has the Wilson upper bound < 5%; it KEEPS MOVING iff the lower bound > 5% at some
valid cell; arm_stop = the first grid layer from which it stops at every later layer that has a valid cell. H-gap iff
patch_stop - lens_stop >= 6 and the patch keeps moving at lens_stop; H-no-gap iff <= 2; else inconclusive. The
embedding arm's stop and moving layers reported next to the lens's.

Layer-16 test (the night brief's T4, 22 Oct 23:00, before the run; `--embed --subsets w`): at the stated bridge's word,
layers 12-24 every second, scales 1/2/4/8, three directions of equal norm: the lens word difference, the input-embedding
difference W_E[X] - W_E[I] (an input edit's direction), a random direction. Valid cells: v2's off-path check. At the
valid cells of layers 16 and 18, items pooled, per item d_lens = lens - 2 x embed and d_input = embed - 0.5 x lens (1 =
the lookup switched to X), entity-cluster bootstrap (the bridge). H_lens iff d_lens's lower bound > 0 (the lens writes
lookup-relevant information before layer 20). H_input iff d_input's lower bound >= 0 and at layer 20 both pushes
switch <= 5% of lookups at every scale (layer 16 is an input edit). No lead iff the lens push switches <= 5% of lookups
at 16-18. Else inconclusive.

The scene's patch (the two tests below): C - clean of the scene's prompt -> prompt case at the stated bridge's word (w)
or sentence (s), one per scene for all four families. prompt -> memory reads the same context (its own patch there is
the same); memory -> prompt and memory -> memory, whose own C changes only the question (their own patch there is zero),
get it too, as they get the lens push's word difference, so their off-path check is a real one.

Dose control (Dan, 23 Oct, before its run d4_layer_gap_dose_27b; `--patch --patch-dir --gap-rule v2 --same-scenes
d4_layer_gap_v2_27b`): in d4_layer_gap_v2_27b the full patch moves lookups to layer 26 and the lens push stops at 20, but
the patch has its own size, not the pushes'. A fifth arm, patch_dir: the scene's patch over the pushed positions, as one
vector, rescaled to the lens push's norm there (scale x ref x sqrt(positions); at the word, one token, exactly the lens
push's), at 4x and 8x. Same scenes (the draw is asserted equal to d4_layer_gap_v2_27b's), positions, layers and scales.
With the layer-gap v2 machinery (each arm's valid cells, stops, moving; patch_dir's off-path rows are its own, its random
push the one at the same scale): dose_stop = patch_dir's stop (never stopping counts as after the grid). At the word:
H-direction (the gap is not dose) iff dose_stop - lens_stop >= 6 and patch_dir keeps moving at lens_stop; H-dose iff
dose_stop - lens_stop <= 2; else inconclusive (partly dose). Reported: the sentence the same way, the full patch's and the
lens push's stops (a replication of d4_layer_gap_v2_27b, with the share of items that keep their role), and the full
patch's norm in units of the 1x lens push's.

Layer-16 split (Dan, 23 Oct, before its run d4_l16_split_27b; `--split --same-scenes d4_layer_gap_v2_27b`, layers 14,
16, 18): at w and s, the scene's patch split as statement_positions' parts (finding 2; exp04_brew_parts' code): the
J-space part (25-atom signed OMP over the frozen J++'s letter-token vectors, per position) and the rest, the projection
on the bridge's and X's own lens vectors (lens2) and the rest, and the full patch; each pasted at its own size, each with
its null (every row a random direction at that row's norm). A part's cell is valid iff the part changes <= 10% of memory
-> prompt and of memory -> memory answers and its null switches <= 5% of lookups. A valid part moves lookups iff the
Wilson lower bound of the lookups switched to X is > 5%, and is inert iff the upper bound is < 5%. At the word, layer 16,
interpretable only if the full patch moves lookups there (lower bound > 5%): H-lens-part (the early lens write reaches
the lookup) iff the J-space part moves lookups; H-rest (the layer-16 movement is outside the lens part) iff the J-space
part is inert and the rest moves them; else inconclusive (a J-space cell that is not valid included). Reported: layers
14 and 18, the sentence, lens2 / not_lens2, each part's share of the patch's squared norm, the lens push at the same
cells.

Stages:  run --name N --why W [--n K] [--scenes map|fresh] [--rule v1|v2] [--patch] [--patch-dir] [--split]
         [--same-scenes RUN]   analyze --name N [--rule v2.1]   figures --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts import early_push as EP
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp

EXP = "early_push_where"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {"n": 100, "families": ["BL", "BR", "RL", "RR"], "map": "map_A8_v1", "wording": "A",
                            "layers": [12, 16, 20, 24, 28, 32, 36, 40, 44], "scales": [1.0, 2.0, 4.0, 8.0],
                            "context_layers": [28, 32, 36, 40, 44], "scenes": "map", "rule": "v1"}  # fmt: skip
WHERE = ("b", "s", "w", "c")
DIRS = ("lens", "random", "offscene")
SEED = 0
FRESH_SEED = 1
V21_MIN_LAYER = 20
SEL_RATE, SEL_LO, RAND_MAX, OFF_PATH_MAX = 0.30, 0.20, 0.05, 0.10
WHERE_RATE, WHERE_LO, AROUND_MAX, AROUND_GAP = 0.30, 0.20, 0.10, 0.20
SLIDE6 = {"RL": 0.73, "RR": 0.84, "BL": 0.01, "BR": 0.02}  # early_push d4_push_wording_b_v1, b, layer 20, 8x
GAP, NO_GAP = 6, 2  # the layer-gap v2 bars (layers), shared by the dose control
SPLIT_PARTS = ("full", "jspace", "not_jspace", "lens2", "not_lens2")
SPLIT_LAYER = 16
BATCH = P.BATCH


# ---- positions and the off-scene animal (pure; tests/test_early_push_where.py) ---------------------------------------


def stated_positions(c: dict) -> dict[str, list[int]]:
    """Token positions of the bridge's owner sentence (s), the bridge's word in it (w) and the whole context (c) in the
    unedited prompt (early_push.augment's offsets)."""
    owner = c["people"][c["pets"].index(c["bridge"])]
    sent = S.WORDINGS["A"]["own"].format(p=owner, a=c["bridge"])
    ctx, rendered, offsets = c["context"], c["prompts"]["clean"], c["offsets"]
    assert rendered.count(ctx) == 1, f"{c['id']}: the context not once in the prompt"
    assert ctx.count(sent) == 1, f"{c['id']}: {sent!r} not once in the context"
    c0 = rendered.index(ctx)
    a = c0 + ctx.index(sent)
    wa = a + sent.rindex(c["bridge"])
    out = {"s": EP.overlapping(offsets, a, a + len(sent)), "w": EP.overlapping(offsets, wa, wa + len(c["bridge"])),
           "c": EP.overlapping(offsets, c0, c0 + len(ctx))}  # fmt: skip
    assert out["w"], f"{c['id']}: no tokens for the bridge's word"
    assert set(out["w"]) <= set(out["s"]) <= set(out["c"]), f"{c['id']}: nested positions"
    assert max(out["c"]) < min(c["subsets"]["b"]), f"{c['id']}: the context after the question"
    return out


def offscene_animal(c: dict) -> str:
    """An animal not in the scene whose leg count differs from the bridge's and X's, the same for the whole scene."""
    legs = {a: v[0] for a, v in S.ANIMALS.items()}
    used = set(c["pets"]) | {c["bridge"], c["cf_bridge"]}
    cands = sorted(a for a in legs if a not in used and legs[a] not in (legs[c["bridge"]], legs[c["cf_bridge"]]))
    return random.Random(f"{SEED}:{c['scene']}").choice(cands)


def role_of(top: int, cand: dict, y_tok: int | None) -> str:
    """A (unchanged), b (X's answer), y (the off-scene animal's answer), oc (another in-context answer), other."""
    if top in (cand["A"], cand["b"]):
        return "A" if top == cand["A"] else "b"
    if y_tok is not None and top == y_tok:
        return "y"
    return "oc" if top in cand["oc"] else "other"


def fresh_scenes(eligible: dict[str, set[str]], used: set[str], n: int, seed: int = FRESH_SEED) -> list[str]:
    """n scenes eligible in every family and not used, sampled by seed (sorted first, so the draw is reproducible)."""
    pool = sorted(set.intersection(*eligible.values()) - used)
    return random.Random(seed).sample(pool, min(n, len(pool)))


def fresh_cases(tok, cfg: dict) -> tuple[list[dict], dict]:
    """The fresh-scene cases (suite_split's eligibility, none of the map run's scenes); a scene whose C or O does not
    line up in one family is dropped in all four, so the families stay on the same scenes."""
    rows = [json.loads(x) for x in (P.RESULTS / cfg["map"] / "cases.jsonl").read_text().splitlines()]
    used = {r["scene"] for r in rows if r["family"] in cfg["families"]}
    for run in cfg.get("exclude_runs", []):  # scenes an earlier fresh run drew
        used |= set(json.loads((RESULTS / run / "selection.json").read_text())["scenes"])
    eligible: dict[str, dict[str, dict]] = {}
    for fam in cfg["families"]:
        ok: dict[str, list[bool]] = collections.defaultdict(list)
        for line in P.competence_file(fam, cfg["wording"]).read_text().splitlines():
            r = json.loads(line)
            if r["family"] == fam:
                ok[r["id"]].append(r["correct"])
        good = {i for i, v in ok.items() if all(v)}
        eligible[fam] = {it["scene"]: it for it in S.load(fam, cfg["wording"]) if it["id"] in good}
    picked = fresh_scenes({f: set(v) for f, v in eligible.items()}, used, cfg["n"], cfg.get("fresh_seed", FRESH_SEED))
    cases, dropped = [], []
    for s in picked:
        try:
            cases += [{**eligible[f][s], **P.prepare(eligible[f][s], tok)} for f in cfg["families"]]
        except AssertionError:  # the comprehension fails before +=, so none of the scene's families is kept
            dropped.append(s)
    pool = len(set.intersection(*(set(v) for v in eligible.values())) - used)
    return cases, {"pool": pool, "picked": len(picked), "unaligned_dropped": dropped, "scenes": picked}


def at_norm(delta: torch.Tensor, norms: torch.Tensor) -> torch.Tensor:
    """The dose control's push: delta [P, d] as one vector, rescaled to the norm of a push with per-position norms
    `norms` [P] (sqrt(sum norms^2)). Its direction is delta's, positions with no change stay at zero."""
    size = float(delta.norm())
    assert size > 0, "a zero patch has no direction"
    return delta * (float(norms.norm()) / size)


def split_patch(delta: torch.Tensor, dictionary: torch.Tensor, pair: torch.Tensor, k: int = K_ATOMS) -> dict:
    """statement_positions' parts of a patch delta [P, d] (exp04_brew_parts' functions, as finding 2): the J-space part
    (k-atom signed OMP per row over `dictionary`, the lens's unit letter-token vectors) and the rest, the projection on
    `pair` (the bridge's and X's lens vectors) and the rest, and the full patch. Each pair of parts sums to delta."""
    jspace, lens2 = signed_omp(dictionary, delta, k), lens2_part(delta, pair)
    return {"full": delta, "jspace": jspace, "not_jspace": delta - jspace, "lens2": lens2, "not_lens2": delta - lens2}


# ---- the decision (pure) ----------------------------------------------------------------------------------------------


def cell_rate(cell: dict[str, str], hit: str = "b") -> tuple[float, float, float]:
    """Wilson (rate, lo, hi) of items whose role is `hit` ('changed': anything but A)."""
    k = sum((r != "A") if hit == "changed" else (r == hit) for r in cell.values())
    return wilson(k, len(cell))


def cell_valid(cells: dict[tuple, dict[str, str]], key: tuple) -> tuple[bool, dict, tuple]:
    """At (subset, layer, scale): the lens push changes <= OFF_PATH_MAX of RL and of RR, the random push switches
    <= RAND_MAX of BL. Returns (valid, {RL, RR: changed}, BL random)."""
    off = {f: cell_rate(cells[(f, *key, "lens")], "changed") for f in ("RL", "RR") if cells.get((f, *key, "lens"))}
    bl_rand = cell_rate(cells.get(("BL", *key, "random"), {}))
    valid = all(v[0] <= OFF_PATH_MAX for v in off.values()) and (math.isnan(bl_rand[0]) or bl_rand[0] <= RAND_MAX)
    return valid, off, bl_rand


def stop_layer(rates: dict[int, float], hi: float = 0.05) -> int | None:
    """The first grid layer from which the rate stays <= hi at it and every later layer (None: never)."""
    grid = sorted(rates)
    for i, la in enumerate(grid):
        if all(rates[g] <= hi for g in grid[i:]):
            return la
    return None


def layer_gap(cells: dict[tuple, dict[str, str]], layers: list[int], sub: str = "w") -> dict:
    """The layer-gap test (docstring) on BL rows at one subset. Pure."""
    lens = {la: max(cell_rate(cells.get(("BL", sub, la, sc, "lens"), {}))[0] for sc in (4.0, 8.0)) for la in layers}
    patch = {la: cell_rate(cells.get(("BL", sub, la, 0.0, "patch"), {}))[0] for la in layers}
    rnd = {la: cell_rate(cells.get(("BL", sub, la, 8.0, "random"), {}))[0] for la in layers}
    if any(math.isnan(v) for v in (*lens.values(), *patch.values())):
        return {"verdict": "no data", "subset": sub}
    ls, ps = stop_layer(lens), stop_layer(patch)
    valid = all(v <= RAND_MAX for v in rnd.values() if not math.isnan(v))
    out = {"subset": sub, "lens_stop": ls, "patch_stop": ps, "valid": valid,
           "lens": {la: round(v, 4) for la, v in lens.items()}, "patch": {la: round(v, 4) for la, v in patch.items()}}  # fmt: skip
    if ls is None or ps is None:
        out["verdict"] = "inconclusive (a curve never settles at <= 5%)"
        return out
    at = cell_rate(cells.get(("BL", sub, ls, 0.0, "patch"), {}))
    if ps - ls >= 6 and at[0] >= 0.30 and at[1] >= 0.20:
        verdict = "H-gap"
    elif ps - ls <= 2:
        verdict = "H-no-gap"
    else:
        verdict = "inconclusive"
    out.update(patch_at_lens_stop=at, verdict=verdict if valid else f"not valid ({verdict})")
    return out


def embed_test(
    cells: dict[tuple, dict[str, str]],
    bridge_of: dict[str, str],
    scales: list[float],
    test_layers: tuple[int, ...] = (16, 18),
    zero_layer: int = 20,
) -> dict:
    """The layer-16 test (docstring) on BL rows at w. Pure."""
    from bridge_jspace.stats import cluster_bootstrap

    valid = [(la, sc) for la in test_layers for sc in scales
             if cells.get(("BL", "w", la, sc, "lens")) and cell_valid(cells, ("w", la, sc))[0]]  # fmt: skip
    lens_v, emb_v, clusters = [], [], []
    for la, sc in valid:
        lens_c, emb_c = cells[("BL", "w", la, sc, "lens")], cells.get(("BL", "w", la, sc, "embed"), {})
        for item in sorted(set(lens_c) & set(emb_c)):
            lens_v.append(float(lens_c[item] == "b"))
            emb_v.append(float(emb_c[item] == "b"))
            clusters.append(bridge_of.get(item, item))
    out: dict[str, Any] = {"valid_cells": valid, "n": len(lens_v)}
    if not lens_v:
        return {**out, "verdict": "no valid cell at layers 16-18"}
    lens_rate, emb_rate = statistics.mean(lens_v), statistics.mean(emb_v)
    d_lens = cluster_bootstrap([lv - 2 * ev for lv, ev in zip(lens_v, emb_v, strict=True)], clusters, seed=SEED)
    d_input = cluster_bootstrap([ev - 0.5 * lv for lv, ev in zip(lens_v, emb_v, strict=True)], clusters, seed=SEED)
    at20 = [cell_rate(cells.get(("BL", "w", zero_layer, sc, d), {}))[0] for sc in scales for d in ("lens", "embed")]
    zero = all(not math.isnan(v) and v <= RAND_MAX for v in at20)
    out.update(lens=lens_rate, embed=emb_rate, d_lens=d_lens, d_input=d_input, zero_at_20=zero)
    if lens_rate <= RAND_MAX:
        verdict = "no lead: the lens push moves <= 5% of lookups at layers 16-18"
    elif d_lens[1] > 0:
        verdict = "H_lens: the lens writes lookup-relevant information before layer 20"
    elif d_input[1] >= 0 and zero:
        verdict = "H_input: layer 16 is an input edit"
    else:
        verdict = "inconclusive"
    return {**out, "verdict": verdict}


def arm_cells(cells: dict[tuple, dict[str, str]], sub: str, la: int, arm: str) -> list[tuple]:
    """The valid cells of one arm at one layer: v2's off-path check with that arm's own rows (memory -> prompt and
    memory -> memory changed <= 10%) and the random push switching <= 5% of lookups at the same layer and scale."""
    out = []
    for key in sorted(k for k in cells if k[0] == "BL" and k[1] == sub and k[2] == la and k[4] == arm):
        _, _, _, sc, _ = key
        off = [cell_rate(cells[(f, sub, la, sc, arm)], "changed")[0] for f in ("RL", "RR") if cells.get((f, sub, la, sc, arm))]  # fmt: skip
        rnd = cell_rate(cells.get(("BL", sub, la, 8.0 if arm == "patch" else sc, "random"), {}))[0]
        if all(v <= OFF_PATH_MAX for v in off) and (math.isnan(rnd) or rnd <= RAND_MAX):
            out.append(key)
    return out


def arm_course(cells: dict[tuple, dict[str, str]], layers: list[int], sub: str, arm: str) -> dict:
    """One arm over the grid (layer-gap test v2): it stops at a layer iff at every valid cell of that layer its lookup
    switch rate has the Wilson upper bound < 5% (None: no valid cell); it keeps moving iff the lower bound > 5% at some
    valid cell; stop = the first grid layer from which it stops at every later layer with a valid cell. Pure."""
    states = {}
    for la in layers:
        rs = [cell_rate(cells[k]) for k in arm_cells(cells, sub, la, arm)]
        states[la] = ((all(r[2] < RAND_MAX for r in rs) if rs else None), any(r[1] > RAND_MAX for r in rs))
    tested = [la for la in layers if states[la][0] is not None]
    stop = next((la for i, la in enumerate(tested) if all(states[g][0] for g in tested[i:])), None)
    return {"stop": stop, "stopped": {la: s[0] for la, s in states.items()}, "moving": {la: s[1] for la, s in states.items()}}  # fmt: skip


def layer_gap_v2(cells: dict[tuple, dict[str, str]], layers: list[int], sub: str = "w") -> dict:
    """The layer-gap test v2 (docstring; Dan, 22 Oct 23:30), each arm's course by arm_course. Pure."""
    out: dict[str, Any] = {"subset": sub, **{arm: arm_course(cells, layers, sub, arm) for arm in ("lens", "patch", "embed")}}  # fmt: skip
    ls, ps = out["lens"]["stop"], out["patch"]["stop"]
    if ls is None or ps is None:
        out["verdict"] = "inconclusive (an arm never stops for good)"
    elif ps - ls >= GAP and out["patch"]["moving"].get(ls):
        out["verdict"] = "H-gap"
    elif ps - ls <= NO_GAP:
        out["verdict"] = "H-no-gap"
    else:
        out["verdict"] = "inconclusive"
    return out


def dose_test(cells: dict[tuple, dict[str, str]], layers: list[int], sub: str = "w") -> dict:
    """The dose control (docstring; Dan, 23 Oct): the patch's direction at the lens push's norm (patch_dir) against the
    lens push, with layer_gap_v2's stops; the full patch's course reported. Pure."""
    out: dict[str, Any] = {"subset": sub, **{arm: arm_course(cells, layers, sub, arm) for arm in ("lens", "patch_dir", "patch")}}  # fmt: skip
    ls, ds = out["lens"]["stop"], out["patch_dir"]["stop"]
    gap = None if ls is None else (math.inf if ds is None else ds - ls)  # patch_dir never stopping: after the grid
    out["gap"] = gap if gap is None or math.isfinite(gap) else "beyond the grid"
    if gap is None:
        out["verdict"] = "inconclusive (the lens push never stops for good)"
    elif gap >= GAP and out["patch_dir"]["moving"].get(ls):
        out["verdict"] = "H-direction: at the lens push's norm the patch's direction keeps moving lookups (the gap is not dose)"  # fmt: skip
    elif gap <= NO_GAP:
        out["verdict"] = "H-dose: at the lens push's norm the patch's direction stops with the lens push (the gap is dose)"  # fmt: skip
    else:
        out["verdict"] = "inconclusive (partly dose)"
    return out


def split_cell(cells: dict[tuple, dict[str, str]], sub: str, la: int, part: str) -> dict | None:
    """One part of the scene's patch at (subset, layer): lookups switched to X, its null, memory -> prompt / memory ->
    memory changed, valid (off-path <= 10%, null <= 5%), moves (valid, lower bound > 5%), inert (valid, upper < 5%)."""
    bl = cells.get(("BL", sub, la, 0.0, f"split_{part}"))
    if not bl:
        return None
    rate = cell_rate(bl)
    null = cell_rate(cells.get(("BL", sub, la, 0.0, f"split_{part}_null"), {}))
    off = {f: cell_rate(cells.get((f, sub, la, 0.0, f"split_{part}"), {}), "changed") for f in ("RL", "RR")}
    valid = all(math.isnan(v[0]) or v[0] <= OFF_PATH_MAX for v in off.values()) and (math.isnan(null[0]) or null[0] <= RAND_MAX)  # fmt: skip
    return {"n": len(bl), "lookups": rate, "null": null, "off_path": off, "valid": valid,
            "moves": valid and rate[1] > RAND_MAX, "inert": valid and rate[2] < RAND_MAX}  # fmt: skip


def split_test(cells: dict[tuple, dict[str, str]], layers: list[int], sub: str = "w", at: int = SPLIT_LAYER) -> dict:
    """The layer-16 split (docstring; Dan, 23 Oct): which part of the scene's patch moves lookups at layer `at`. Pure."""
    by = {la: {p: c for p in SPLIT_PARTS if (c := split_cell(cells, sub, la, p))} for la in layers}
    full, j, rest = (by.get(at, {}).get(p) for p in ("full", "jspace", "not_jspace"))
    if not (full and j and rest):
        verdict = f"no data at layer {at}"
    elif not full["lookups"][1] > RAND_MAX:
        verdict = f"not interpretable: the full patch does not move lookups at layer {at}"
    elif j["moves"]:
        verdict = "H-lens-part: the J-space part moves lookups (the early lens write reaches the lookup)"
    elif j["inert"] and rest["moves"]:
        verdict = "H-rest: only the rest moves lookups (the movement is outside the lens part)"
    else:
        verdict = "inconclusive" + ("" if j["valid"] else " (the J-space part's cell is not valid)")
    return {"subset": sub, "layer": at, "verdict": verdict, "cells": by}


def agreement(a: dict[tuple, dict[str, str]], b: dict[tuple, dict[str, str]]) -> dict[str, list[int]]:
    """Per arm, over the cells and items two runs share: [items with the same role, items]. Pure."""
    out: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for key in a.keys() & b.keys():
        for item in a[key].keys() & b[key].keys():
            out[key[4]][0] += a[key][item] == b[key][item]
            out[key[4]][1] += 1
    return dict(sorted(out.items()))


def scene_norms(case_rows: list[dict]) -> dict:
    """Medians over scenes (prompt -> prompt rows): the scene's patch norm in units of the 1x lens push's (ref x
    sqrt(positions)), and with --split each part's share of the patch's squared norm; keys 'layer/subset'."""
    rows = [r for r in case_rows if r["family"] == "BL" and "patch_norm" in r]
    out: dict[str, dict] = {"patch_over_1x_lens": {}, "split_share": {}}
    for key in rows[0]["patch_norm"] if rows else []:
        la, sub = key.split("/")
        out["patch_over_1x_lens"][key] = round(statistics.median(
            r["patch_norm"][key] / (r["ref"][la] * math.sqrt(len(r["positions"][sub]))) for r in rows), 2)  # fmt: skip
        if "split_share" in rows[0]:
            out["split_share"][key] = {p: round(statistics.median(r["split_share"][key][p] for r in rows), 4)
                                       for p in rows[0]["split_share"][key]}  # fmt: skip
    return out


def decide(
    cells: dict[tuple, dict[str, str]],
    scene_of: dict[str, str],
    layers: list[int],
    scales: list[float],
    rule: str = "v1",
    min_layer: int = V21_MIN_LAYER,
) -> dict:
    """cells: (family, subset, layer, scale, dir) -> {item: role}, items answered right unedited only. rule v1:
    select on BR, then check validity at the primary cell; v2: only valid cells are selected; v2.1: v2 at layers
    >= min_layer (V21_MIN_LAYER on the 27B; scaled by depth on other models), the valid cells below in 'below_v21'."""
    assert rule in ("v1", "v2", "v2.1"), rule
    sel, below = [], []
    for sub in ("w", "s"):
        for la in layers:
            for sc in scales:
                br, rnd = cells.get(("BR", sub, la, sc, "lens")), cells.get(("BR", sub, la, sc, "random"))
                if not br or not rnd:
                    continue
                p, lo, _ = cell_rate(br)
                if p >= SEL_RATE and lo >= SEL_LO and cell_rate(rnd)[0] <= RAND_MAX:
                    if rule != "v1" and not cell_valid(cells, (sub, la, sc))[0]:
                        continue
                    row = {"subset": sub, "layer": la, "scale": sc, "br": round(p, 4)}
                    if rule == "v2.1" and la < min_layer:
                        bl = cell_rate(cells.get(("BL", sub, la, sc, "lens"), {}))
                        below.append({**row, "bl": None if math.isnan(bl[0]) else round(bl[0], 4)})
                        continue
                    sel.append(row)
    out: dict[str, Any] = {"rule": rule, "selected": sel, **({"below_v21": below} if rule == "v2.1" else {})}
    if not sel:
        none = "no cell" if rule == "v1" else "no valid cell"
        out.update(primary=None, valid=None, verdict=f"{none}: the lens does not write a stated bridge at its sentence")
        return out
    best = min(sel, key=lambda d: (-d["br"], d["scale"], d["layer"], 0 if d["subset"] == "w" else 1))
    key = (best["subset"], best["layer"], best["scale"])
    get = {f: cells.get((f, *key, "lens"), {}) for f in ("BL", "BR", "RL", "RR")}
    valid, off, bl_rand = cell_valid(cells, key)
    bl, br = cell_rate(get["BL"]), cell_rate(get["BR"])
    by_scene = {f: {scene_of[i]: float(r == "b") for i, r in get[f].items()} for f in ("BL", "BR")}
    common = sorted(set(by_scene["BL"]) & set(by_scene["BR"]))
    gap = paired_bootstrap_diff([by_scene["BR"][s] for s in common], [by_scene["BL"][s] for s in common], seed=SEED)
    if bl[0] >= WHERE_RATE and bl[1] >= WHERE_LO:
        verdict = "H-where: the lens writes a stated bridge for a lookup where it sits"
    elif bl[0] <= AROUND_MAX and gap[1] >= AROUND_GAP:
        verdict = "H-around: the lens writes a stated bridge for recall but not for a lookup where it sits"
    else:
        verdict = "inconclusive"
    out.update(primary=best, valid=valid, verdict=verdict if valid else f"not valid ({verdict})",
               rates={"BL": bl, "BR": br, "BL_random": bl_rand, **{f"{f}_changed": v for f, v in off.items()}},
               br_minus_bl=gap, n_scenes_paired=len(common))  # fmt: skip
    return out


# ---- model ------------------------------------------------------------------------------------------------------------


def run_scene(model, lens, scene: list[dict], cfg: dict, k0: int, out: dict, letters=None) -> None:
    layers = cfg["layers"]
    for c in scene:
        ids = torch.tensor([c["read"]["clean"], c["read"]["E-cue"]], device="cuda")
        logits, rec = EP.forward_rows(model, ids, [{}, {}], tuple(layers))
        c["ld_clean"], c["ld_cf"] = (float(lg[c["cand"]["b"]] - lg[c["cand"]["A"]]) for lg in logits)
        r = c["subsets"]["r"]
        c["_ref"] = {la: float((rec[la][1][r] - rec[la][0][r]).norm(dim=-1).pow(2).mean().sqrt()) for la in layers}
        c["_logits"] = logits
        if cfg.get("patch") or cfg.get("patch_dir") or cfg.get("split"):  # the full residual swap clean <- C
            c["_delta"] = {la: rec[la][1] - rec[la][0] for la in layers}  # (token-aligned) at each layer
    ref = {la: math.sqrt(statistics.mean(c["_ref"][la] ** 2 for c in scene)) for la in layers}
    if cfg.get("patch_dir") or cfg.get("split"):
        scene_patch(model, lens, scene, cfg, letters)
    y = offscene_animal(scene[0])
    for i, c in enumerate(scene):
        run_item(model, lens, c, ref, y, cfg, k0 + i, out)


@torch.no_grad()
def scene_patch(model, lens, scene: list[dict], cfg: dict, letters) -> None:
    """The scene's patch (docstring) at w and s for every case of the scene; with --split its parts at every layer (one
    fp32 letter dictionary at a time, as statement_positions' parts)."""
    src = next(c for c in scene if c["family"] == "BL")
    pos = stated_positions(src)
    patch = {(la, sub): src["_delta"][la][pos[sub]] for la in cfg["layers"] for sub in ("s", "w")}
    parts: dict[tuple, dict] = {}
    if cfg.get("split"):
        pair = torch.tensor([model.concept_token(a) for a in (src["bridge"], src["cf_bridge"])], device="cuda")
        for la in cfg["layers"]:
            dictionary = lens.vectors(la, letters)
            for sub in ("s", "w"):
                parts[(la, sub)] = split_patch(patch[(la, sub)], dictionary, lens.vectors(la, pair))
            del dictionary
    for c in scene:
        assert stated_positions(c) == pos, f"{c['id']}: the scene's families push different positions"
        c["_scene_patch"], c["_parts"] = patch, parts


def run_item(model, lens, c: dict, ref: dict, y: str, cfg: dict, k: int, out: dict) -> None:
    tok = model.tokenizer
    pos = {"b": c["subsets"]["b"], **stated_positions(c)}
    pair = torch.tensor([model.concept_token(a) for a in (c["bridge"], c["cf_bridge"], y)], device="cuda")
    dirs = {}
    for la in cfg["layers"]:
        v = lens.vectors(la, pair)
        dirs[la] = {"lens": v[1] - v[0], "offscene": v[2] - v[0]}
        if cfg.get("embed"):  # the input-embedding difference W_E[X] - W_E[I] (an input edit's direction), every layer
            e = model.text.embed_tokens.weight[pair[:2]].float()
            dirs[la]["embed"] = e[1] - e[0]
    y_tok = S.answer_token(tok, str(S.ANIMALS[y][0]), "digit") if c["family"].endswith("R") else None
    head = {"family": c["family"], "name": c["id"], "scene": c["scene"]}

    def emit(tags: dict, logits: torch.Tensor) -> None:
        top = int(logits.argmax())
        ld = float(logits[c["cand"]["b"]] - logits[c["cand"]["A"]])
        out["outcomes"].append({**head, **tags, "role": role_of(top, c["cand"], y_tok), "ld": round(ld, 3)})

    emit({"kind": "none"}, c["_logits"][0])
    for e in EP.EDITS:
        if e not in c["read"]:
            continue
        if e == "E-cue":
            emit({"kind": "edit", "edit": e}, c["_logits"][1])
        else:
            lg, _ = EP.forward_rows(model, torch.tensor([c["read"][e]], device="cuda"), [{}])
            emit({"kind": "edit", "edit": e}, lg[0])
    gen = torch.Generator(device="cuda").manual_seed(SEED + 1_000_003 * k)
    gen_split = torch.Generator(device="cuda").manual_seed(SEED + 1_000_003 * k + 1)  # its own: gen's draws unchanged
    rows: list[tuple[dict, dict]] = []
    for la in cfg["layers"]:
        for sc in cfg["scales"]:
            for sname in cfg.get("subsets", WHERE):
                if sname == "c" and la not in cfg["context_layers"]:
                    continue
                p = pos[sname]
                norms = torch.full((len(p),), sc * ref[la], device="cuda")
                lens_vec = EP.push_rows(dirs[la]["lens"], norms)
                tags = {"kind": "push", "layer": la, "scale": sc, "subset": sname}
                rows.append(({**tags, "dir": "lens"}, {la: AddRows(lens_vec, p)}))
                rows.append(({**tags, "dir": "random"}, {la: AddRows(null_rows(lens_vec, gen), p)}))
                rows.append(({**tags, "dir": "offscene"}, {la: AddRows(EP.push_rows(dirs[la]["offscene"], norms), p)}))
                if cfg.get("embed"):  # the same norms along the input-embedding difference
                    rows.append(({**tags, "dir": "embed"}, {la: AddRows(EP.push_rows(dirs[la]["embed"], norms), p)}))
                if cfg.get("patch_dir") and sname in ("s", "w"):  # the scene's patch at the lens push's norm
                    rows.append(({**tags, "dir": "patch_dir"}, {la: AddRows(at_norm(c["_scene_patch"][(la, sname)], norms), p)}))  # fmt: skip
        if cfg.get("patch"):
            for sname in ("s", "w"):  # C's residual at the stated bridge's sentence / word, at its own size (scale 0)
                p = pos[sname]
                tags = {"kind": "push", "layer": la, "scale": 0.0, "subset": sname, "dir": "patch"}
                rows.append((tags, {la: AddRows(c["_delta"][la][p], p)}))
        if cfg.get("split"):
            for sname in ("s", "w"):  # the scene's patch's parts at their own size, each with its null
                for part, vec in c["_parts"][(la, sname)].items():
                    tags = {"kind": "push", "layer": la, "scale": 0.0, "subset": sname, "dir": f"split_{part}"}
                    rows.append((tags, {la: AddRows(vec, pos[sname])}))
                    rows.append(({**tags, "dir": f"split_{part}_null"}, {la: AddRows(null_rows(vec, gen_split), pos[sname])}))  # fmt: skip
    ids = torch.tensor([c["read"]["clean"]], device="cuda")
    for start in range(0, len(rows), BATCH - 1):
        chunk = rows[start : start + BATCH - 1]
        logits, _ = EP.forward_rows(model, ids, [{}] + [e for _, e in chunk])
        out["diag"].append(float((logits[0] - c["_logits"][0]).abs().max()))
        for j, (tags, _) in enumerate(chunk, start=1):
            emit(tags, logits[j])
    row = {**head, "bridge": c["bridge"], "cf_bridge": c["cf_bridge"], "offscene": y,
           "answer": c["answer"], "cf_answer": c["cf_answer"], "subject": c["subject"],
           "positions": pos, "prompt": c["prompts"]["clean"],
           "ref": {str(la): round(ref[la], 3) for la in cfg["layers"]}}  # fmt: skip
    if cfg.get("patch_dir") or cfg.get("split"):  # the scene's patch: its norm, and its parts' shares of its square
        row["patch_norm"] = {f"{la}/{s}": round(float(v.norm()), 3) for (la, s), v in c["_scene_patch"].items()}
        if c["_parts"]:
            row["split_share"] = {f"{la}/{s}": {p: round(float(v.norm() ** 2 / ps["full"].norm() ** 2), 4) for p, v in ps.items()}
                                  for (la, s), ps in c["_parts"].items()}  # fmt: skip
    out["cases"].append(row)


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    inputs = [P.RESULTS / cfg["map"] / "cases.jsonl"] + [
        S.data_dir(cfg["wording"]) / f"{f}.json" for f in cfg["families"]
    ]
    if cfg["scenes"] == "fresh":
        inputs += sorted({P.competence_file(f, cfg["wording"]) for f in cfg["families"]})
    if cfg.get("same_scenes"):
        inputs.append(RESULTS / cfg["same_scenes"] / "selection.json")
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
                "seeds": {"random": f"{SEED} + 1000003 x item index", "offscene": f"Random('{SEED}:<scene>')",
                          "bootstrap": SEED, **({"fresh_scenes": cfg.get("fresh_seed", FRESH_SEED)} if cfg["scenes"] == "fresh" else {}),
                          **({"split_nulls": f"{SEED} + 1000003 x item index + 1"} if cfg.get("split") else {})},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids() if cfg.get("split") else None
    t0 = time.time()
    if cfg["scenes"] == "fresh":
        raw, selection = fresh_cases(model.tokenizer, cfg)
        if cfg.get("same_scenes"):  # the dose / split runs push on the layer-gap run's scenes, exactly
            want = json.loads((RESULTS / cfg["same_scenes"] / "selection.json").read_text())
            assert selection == want, f"the fresh draw differs from {cfg['same_scenes']}'s selection.json"
        (out_dir / "selection.json").write_text(json.dumps(selection, indent=2) + "\n")
        cases = [EP.augment(c, model.tokenizer, cfg["wording"]) for c in raw]
    else:
        cases = EP.build_cases(model.tokenizer, {**cfg, "countries": False})
    scenes: dict[str, list[dict]] = {}
    for c in cases:
        scenes.setdefault(c["scene"], []).append(c)
    out: dict[str, Any] = {"outcomes": [], "cases": [], "diag": []}
    done = {"outcomes": 0, "cases": 0}
    k = 0
    for scene in progress(list(scenes.values()), desc="scenes"):
        run_scene(model, lens, scene, cfg, k, out, letters)
        k += len(scene)
        for f in done:  # appended scene by scene: a run stopped early keeps every finished scene
            with open(out_dir / f"{f}.jsonl", "a") as fh:
                fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in out[f][done[f] :])
            done[f] = len(out[f])
    timing = {"seconds": round(time.time() - t0), "n_cases": len(cases), "n_outcomes": len(out["outcomes"]),
              "max_unedited_row_vs_clean_logit": max(out["diag"], default=None)}  # fmt: skip
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    stage_analyze(name)


# ---- analysis ---------------------------------------------------------------------------------------------------------


def load_cells(name: str) -> tuple[dict, dict, dict, list[dict]]:
    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    rows = [json.loads(x) for x in (d / "outcomes.jsonl").read_text().splitlines()]
    ok = {r["name"] for r in rows if r["kind"] == "none" and r["role"] == "A"}
    cells: dict[tuple, dict[str, str]] = collections.defaultdict(dict)
    edits: dict[tuple, dict[str, str]] = collections.defaultdict(dict)
    scene_of = {}
    for r in rows:
        scene_of[r["name"]] = r["scene"]
        if r["name"] not in ok:
            continue
        if r["kind"] == "push":
            cells[(r["family"], r["subset"], r["layer"], r["scale"], r["dir"])][r["name"]] = r["role"]
        elif r["kind"] == "edit":
            edits[(r["family"], r["edit"])][r["name"]] = r["role"]
    counts = collections.Counter(r["family"] for r in rows if r["kind"] == "none")
    eligible = collections.Counter(r["family"] for r in rows if r["kind"] == "none" and r["role"] == "A")
    return (
        m,
        dict(cells),
        dict(edits),
        [{"family": f, "n": counts[f], "right_unedited": eligible[f]} for f in sorted(counts)],
    )


def pct(t: tuple[float, float, float]) -> str:
    return "-" if math.isnan(t[0]) else f"{100 * t[0]:.0f}% [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"


def stage_analyze(name: str, rule: str | None = None) -> None:
    """The run's own rule into the run folder; another rule (an amendment) into a new <run>/analysis-<rule>-<stamp>/."""
    m, cells, edits, counts = load_cells(name)
    cfg = m["config"]
    rows = [json.loads(x) for x in (RESULTS / name / "outcomes.jsonl").read_text().splitlines()]
    scene_of = {r["name"]: r["scene"] for r in rows}
    out_dir = RESULTS / name
    if rule:
        out_dir = out_dir / f"analysis-{rule}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
        out_dir.mkdir()
    min_layer = cfg.get("v21_min_layer", V21_MIN_LAYER)
    dec = decide(cells, scene_of, cfg["layers"], cfg["scales"], rule or cfg.get("rule", "v1"), min_layer)
    anchor = {f: cell_rate(cells.get((f, "b", 20, 8.0, "lens"), {})) for f in cfg["families"]}
    summary = {"run": name, "decision": dec, "counts": counts,
               "slide6_anchor": {f: {"now": anchor[f], "slide6": SLIDE6.get(f)} for f in anchor},
               "cells": [{"family": f, "subset": s, "layer": la, "scale": sc, "dir": d, "n": len(v),
                          "to_x": cell_rate(v), "changed": cell_rate(v, "changed"), "to_y": cell_rate(v, "y")}
                         for (f, s, la, sc, d), v in sorted(cells.items())],
               "edits": [{"family": f, "edit": e, "n": len(v), "to_x": cell_rate(v), "changed": cell_rate(v, "changed")}
                         for (f, e), v in sorted(edits.items())]}  # fmt: skip
    if cfg.get("patch"):  # the gap rule in the run's config (v2 from d4_layer_gap_v2_27b on)
        gap = layer_gap_v2 if cfg.get("gap_rule") == "v2" else layer_gap
        summary["layer_gap"] = {sub: gap(cells, cfg["layers"], sub) for sub in ("w", "s")}
    if cfg.get("embed") and not cfg.get("patch"):
        bridge_of = {c["name"]: c["bridge"] for c in map(json.loads, (RESULTS / name / "cases.jsonl").read_text().splitlines())}  # fmt: skip
        summary["embed_test"] = embed_test(cells, bridge_of, cfg["scales"])
    if cfg.get("patch_dir"):
        summary["dose_test"] = {sub: dose_test(cells, cfg["layers"], sub) for sub in ("w", "s")}
    if cfg.get("split"):
        summary["split_test"] = {sub: split_test(cells, cfg["layers"], sub) for sub in ("w", "s")}
    if cfg.get("patch_dir") or cfg.get("split"):
        summary["scene_patch"] = scene_norms([json.loads(x) for x in (RESULTS / name / "cases.jsonl").read_text().splitlines()])  # fmt: skip
    if cfg.get("same_scenes"):  # the arms both runs have, item by item (the same scenes, so the same items)
        summary["replication"] = {"run": cfg["same_scenes"], "same_role": agreement(cells, load_cells(cfg["same_scenes"])[1])}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    lines = [f"# {EXP} / {name} (rule {dec['rule']})", "", f"Items: {counts}", "", f"**Verdict:** {dec['verdict']}", ""]
    if dec.get("primary"):
        p = dec["primary"]
        lines += [
            f"Primary cell: subset {p['subset']}, layer {p['layer']}, {p['scale']:g}x (valid: {dec['valid']})",
            "",
        ]
        lines += [f"- {k}: {pct(v)}" for k, v in dec["rates"].items()]
        g = dec["br_minus_bl"]
        lines += [f"- BR - BL (scene-paired, {dec['n_scenes_paired']} scenes): {100 * g[0]:+.0f} [{100 * g[1]:+.0f}, {100 * g[2]:+.0f}] points", ""]  # fmt: skip
    lines += [f"Selected cells (BR rows only): {len(dec['selected'])}", ""]
    if "embed_test" in summary:
        et = summary["embed_test"]
        lines += [f"**Layer-16 test:** {et['verdict']} (valid cells {et['valid_cells']}, n {et['n']})", ""]
    for sub, g in summary.get("layer_gap", {}).items():
        if "lens_stop" in g:
            lines += [f"**Layer gap ({sub}):** {g['verdict']} (lens_stop {g.get('lens_stop')}, patch_stop {g.get('patch_stop')}); "
                      f"lookups moved by layer, lens {g.get('lens')}, patch {g.get('patch')}", ""]  # fmt: skip
        else:
            lines += [f"**Layer gap v2 ({sub}):** {g['verdict']}; stops: " + ", ".join(f"{arm} {g[arm]['stop']}" for arm in ("lens", "patch", "embed")), ""]  # fmt: skip
    if "dose_test" in summary:
        for sub, g in summary["dose_test"].items():
            lines += [f"**Dose control ({sub}):** {g['verdict']}; stops: " + ", ".join(f"{arm} {g[arm]['stop']}" for arm in ("lens", "patch_dir", "patch")), ""]  # fmt: skip
        lines += ["Lookups switched to X (prompt → prompt), by layer:", "",
                  "| where | layer | lens 4x | lens 8x | patch dir. 4x | patch dir. 8x | full patch | random 8x |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        arms = [(4.0, "lens"), (8.0, "lens"), (4.0, "patch_dir"), (8.0, "patch_dir"), (0.0, "patch"), (8.0, "random")]
        for sub in ("w", "s"):
            for la in cfg["layers"]:
                lines.append(f"| {sub} | {la} | " + " | ".join(pct(cell_rate(cells.get(("BL", sub, la, sc, d), {}))) for sc, d in arms) + " |")  # fmt: skip
        lines += [""]
    for sub, g in summary.get("split_test", {}).items():
        lines += [f"**Layer-16 split ({sub}):** {g['verdict']}", "", "| layer | part | lookups → X | its null | memory → prompt / memory → memory changed | valid |", "|---|---|---|---|---|---|"]  # fmt: skip
        for la, parts in g["cells"].items():
            lines += [f"| {la} | {p} | {pct(c['lookups'])} | {pct(c['null'])} | {pct(c['off_path']['RL'])} / {pct(c['off_path']['RR'])} | {c['valid']} |"
                      for p, c in parts.items()]  # fmt: skip
        lines += [""]
    if "replication" in summary:
        rep = summary["replication"]
        lines += [f"Same role as {rep['run']}, item by item: " + ", ".join(f"{arm} {k}/{n}" for arm, (k, n) in rep["same_role"].items()), ""]  # fmt: skip
    if "scene_patch" in summary:
        sp = summary["scene_patch"]
        lines += ["The scene's patch in units of the 1x lens push's norm (median over scenes): "
                  + ", ".join(f"{k} {v:g}x" for k, v in sp["patch_over_1x_lens"].items()), ""]  # fmt: skip
        if sp["split_share"]:
            lines += ["Each part's share of the patch's squared norm (median over scenes): " + "; ".join(
                f"{k}: " + ", ".join(f"{p} {v:.0%}" for p, v in d.items() if p != "full") for k, d in sp["split_share"].items()), ""]  # fmt: skip
    if "below_v21" in dec:
        lines += [f"Valid cells below layer {min_layer} (reported, not decisive): "
                  + ("; ".join(f"{d['subset']} L{d['layer']} {d['scale']:g}x: BR {100 * d['br']:.0f}%, BL "
                               + ("-" if d["bl"] is None else f"{100 * d['bl']:.0f}%") for d in dec["below_v21"]) or "none"), ""]  # fmt: skip
    lines += ["Slide 6 anchor (b, layer 20, 8x, lens): " + ", ".join(f"{f} {pct(v)} (slide 6: {100 * SLIDE6[f]:.0f}%)" for f, v in anchor.items()), ""]  # fmt: skip
    lines += ["| family | where | layer | scale | lens → X | random → X | off-scene: changed | off-scene → Y |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for f in cfg["families"]:
        for s in WHERE:
            for la in cfg["layers"]:
                for sc in cfg["scales"]:
                    lens_c = cells.get((f, s, la, sc, "lens"))
                    if not lens_c:
                        continue
                    rnd, off = cells.get((f, s, la, sc, "random"), {}), cells.get((f, s, la, sc, "offscene"), {})
                    lines.append(f"| {f} | {s} | {la} | {sc:g} | {pct(cell_rate(lens_c))} | {pct(cell_rate(rnd))} | "
                                 f"{pct(cell_rate(off, 'changed'))} | {pct(cell_rate(off, 'y'))} |")  # fmt: skip
    lines += ["", "| family | edit | n | → X | changed |", "|---|---|---|---|---|"]
    for (f, e), v in sorted(edits.items()):
        lines.append(f"| {f} | {e} | {len(v)} | {pct(cell_rate(v))} | {pct(cell_rate(v, 'changed'))} |")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))


def stage_figures(name: str) -> None:
    """Per push position, % of answers switched to X's answer by layer: the four families under the lens push at the
    primary cell's scale (8x without one), the random push's highest family as a dotted line."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    m, cells, _, _ = load_cells(name)
    cfg = m["config"]
    dec = json.loads((RESULTS / name / "summary.json").read_text())["decision"]
    sc = dec["primary"]["scale"] if dec.get("primary") else 8.0
    cols = {"BL": "#eb6834", "BR": "#2a78d6", "RL": "#f2a27f", "RR": "#86b6ef"}
    names = {"BL": "prompt → prompt (stated bridge, lookup)", "BR": "prompt → memory (stated bridge, recall)",
             "RL": "memory → prompt (recalled bridge, lookup)", "RR": "memory → memory (recalled bridge, recall)"}  # fmt: skip
    titles = {"b": "the question's subject phrase\n(where slide 6 pushed)", "s": "the sentence stating the bridge",
              "w": "the bridge's word in that sentence", "c": "the whole context (layers 28-44)"}  # fmt: skip
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, sub in zip(axes, WHERE, strict=True):
        for f in cfg["families"]:
            pts = [(la, cell_rate(cells[(f, sub, la, sc, "lens")])) for la in cfg["layers"] if (f, sub, la, sc, "lens") in cells]  # fmt: skip
            if pts:
                ax.plot([p[0] for p in pts], [100 * p[1][0] for p in pts], marker="o", ms=3.5, lw=2, color=cols[f],
                        label=names[f])  # fmt: skip
        rnd = [(la, max(cell_rate(cells[(f, sub, la, sc, "random")])[0] for f in cfg["families"]
                        if (f, sub, la, sc, "random") in cells)) for la in cfg["layers"]
               if any((f, sub, la, sc, "random") in cells for f in cfg["families"])]  # fmt: skip
        ax.plot([p[0] for p in rnd], [100 * p[1] for p in rnd], color="#52514e", ls=":", lw=1.5, label="random push (highest family)")  # fmt: skip
        ax.set_title(titles[sub], loc="left", fontsize=9.5)
        ax.set_xlabel(f"layer (of {m['model'].get('n_layers', pins.N_LAYERS)})")
        ax.set_ylim(0, 100)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("% switched to the other\nbridge's answer")
    h, labs = axes[0].get_legend_handles_labels()
    fig.legend(h, labs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.16), fontsize=9)
    fig.suptitle(f"Where can the lens write a bridge? A lens push of {sc:g}x by layer and position ({m['model']['repo'].split('/')[-1]})",
                 x=0.125, ha="left", fontweight="bold")  # fmt: skip
    fig.savefig(RESULTS / name / "where.png", dpi=150, bbox_inches="tight")
    print("wrote", RESULTS / name / "where.png")
    if cfg.get("patch_dir") or cfg.get("split"):
        test_figures(name, m, cells)


def test_figures(name: str, m: dict, cells: dict) -> None:
    """The dose control's and the layer-16 split's figures (prompt -> prompt lookups switched to X's answer, Wilson 95%
    intervals) into a new <run>/analysis-figures-<stamp>/."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import INK, MUTED, finish, percent_axis, style_axes

    cfg, s = m["config"], json.loads((RESULTS / name / "summary.json").read_text())
    folder = RESULTS / name / f"analysis-figures-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    folder.mkdir()
    layers, model = cfg["layers"], m["model"]["repo"].split("/")[-1]
    where = {"w": "at the bridge's word", "s": "over the sentence stating the bridge"}
    blue, orange, aqua, yellow, grey = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#52514e"
    draw = f" (the draw of {cfg['same_scenes']})" if cfg.get("same_scenes") else ""
    data = (f"{model}; {cfg['n']} scenes{draw}, the prompt → prompt questions the model answers right unedited; "
            "one run, one random seed.")  # fmt: skip

    def rate(sub: str, la: int, sc: float, d: str) -> tuple[float, float, float]:
        return cell_rate(cells.get(("BL", sub, la, sc, d), {}))

    def split_plain(verdict: str) -> str:  # the rule's names in words (the other verdicts are words already)
        v = verdict.split(":")[0]
        return {"H-lens-part": "the lens-readable part of the patch moves lookups",
                "H-rest": "only the rest of the patch moves lookups"}.get(v, v)  # fmt: skip

    if "dose_test" in s:
        arms = [("lens", "lens push (other − original bridge)", blue), ("patch_dir", "the patch's direction, cut to the lens push's size", orange)]  # fmt: skip
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.4), sharey=True)
        for ax, sub in zip(axes, ("w", "s"), strict=True):
            style_axes(ax)
            for d, _, col in arms:
                for sc, ls in ((8.0, "-"), (4.0, "--")):
                    r = [rate(sub, la, sc, d) for la in layers]
                    ax.plot(layers, [v[0] for v in r], color=col, ls=ls, lw=2, marker="o", ms=4)
                    if sc == 8.0:
                        ax.fill_between(layers, [v[1] for v in r], [v[2] for v in r], color=col, alpha=0.12, lw=0)
            for d, sc, col, ls in (("patch", 0.0, aqua, "-"), ("random", 8.0, grey, ":")):
                ax.plot(layers, [rate(sub, la, sc, d)[0] for la in layers], color=col, ls=ls, lw=2, marker="o" if d == "patch" else None, ms=4)  # fmt: skip
            g = s["dose_test"][sub]
            ax.set_title(f"{where[sub]}\nstops: lens push {g['lens']['stop']}, patch's direction {g['patch_dir']['stop']}, "
                         f"whole patch {g['patch']['stop']}", loc="left", fontsize=9, color=INK)  # fmt: skip
            ax.set_xlabel(f"layer (of {m['model'].get('n_layers', pins.N_LAYERS)})", color=MUTED)
            ax.set_ylim(0, 1)
            percent_axis(ax)
        axes[0].set_ylabel("lookups switched to\nthe other bridge's answer", color=MUTED)
        handles = [Line2D([], [], color=c, lw=2, label=lab) for _, lab, c in arms] + [
            Line2D([], [], color=aqua, lw=2, marker="o", label="whole patch (its own size)"),
            Line2D([], [], color=grey, lw=2, ls=":", label="random push 8x"),
            Line2D([], [], color=MUTED, lw=2, ls="--", label="dashed: 4x, solid: 8x (band: 95% interval)")]  # fmt: skip
        v = s["dose_test"]["w"]["verdict"].split(":")[0]
        outcome = {"H-direction": "keeps moving lookups after the lens push stops", "H-dose": "stops with the lens push"}.get(v, "stops in between (inconclusive)")  # fmt: skip
        finish(fig, folder / "dose.png", f"Cut to the lens push's size, the patch's direction {outcome} (word)", data,
               handles=handles, ncols=3, handlelength=3, explain=[
                   ("What we did", "At the stated bridge's word (and sentence), every second layer, we added the patch from the prompt "
                    "that states the other bridge, rescaled to the lens push's size (4x, 8x a reference norm), next to the lens push itself and the whole patch at its own size."),
                   ("How to read", "Each line is the share of lookups that switch to the other bridge's answer. A layer where an arm "
                    "reads 0 from there on is where it stops. If the cut-down patch stops with the lens push, the whole patch moved more only because it is larger."),
                   ("Control", "A random push of the lens push's size; memory → prompt and memory → memory answers must not move (off-path check, in summary.md).")])  # fmt: skip
        print("wrote", folder / "dose.png")
    if "split_test" in s:
        bars = [("split_jspace", 0.0, "lens-readable part (J-space)", blue), ("split_not_jspace", 0.0, "the rest", orange),
                ("split_full", 0.0, "whole patch", aqua), ("lens", 8.0, "lens push 8x", yellow)]  # fmt: skip
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.4), sharey=True)
        for ax, sub in zip(axes, ("w", "s"), strict=True):
            style_axes(ax)
            for i, la in enumerate(layers):
                for j, (d, sc, _, col) in enumerate(bars):
                    x, r = i + (j - 1.5) * 0.2, rate(sub, la, sc, d)
                    if math.isnan(r[0]):
                        continue
                    ax.bar(x, r[0], 0.18, color=col, edgecolor="#fcfcfb", lw=1)
                    ax.plot([x, x], [r[1], r[2]], color=INK, lw=1)
                    if d.startswith("split_"):
                        ax.plot(x, rate(sub, la, 0.0, f"{d}_null")[0], marker="D", mfc="none", mec=INK, ms=5, ls="")
                    if la == SPLIT_LAYER:
                        ax.annotate(f"{r[0]:.0%}", (x, r[2]), xytext=(0, 2), textcoords="offset points", ha="center",
                                    va="bottom", fontsize=7.5, color=INK)  # fmt: skip
            ax.set_xticks(range(len(layers)), [f"layer {la}" for la in layers])
            ax.set_title(f"{where[sub]}\n{split_plain(s['split_test'][sub]['verdict'])}", loc="left", fontsize=9, color=INK)  # fmt: skip
            ax.set_ylim(0, 1.05)
            percent_axis(ax)
        axes[0].set_ylabel("lookups switched to\nthe other bridge's answer", color=MUTED)
        handles = [Patch(color=c, label=lab) for *_, lab, c in bars] + [
            Line2D([], [], marker="D", mfc="none", mec=INK, ls="", label="the part's null (random rows, same sizes)")]  # fmt: skip
        outcome = split_plain(s["split_test"]["w"]["verdict"])
        finish(fig, folder / "split.png", f"At layer {SPLIT_LAYER}, {outcome} (word)", data, handles=handles, ncols=3,
               explain=[
                   ("What we did", "The patch from the prompt that states the other bridge, at the bridge's word (and sentence), split "
                    "into the part the lens can read (a 25-word fit on the lens's word directions) and the rest; each added at its own size."),
                   ("How to read", "Bars: share of lookups that switch to the other bridge's answer (line: 95% interval). The lens push "
                    "at 8x is the effect being explained; the whole patch is the sum of the two parts."),
                   ("Control", "Each part's null (diamond); memory → prompt and memory → memory answers must not move (in summary.md).")])  # fmt: skip
        print("wrote", folder / "split.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--n", type=int, default=DEFAULTS["n"])
    ap.add_argument("--scenes", choices=["map", "fresh"], default=DEFAULTS["scenes"])
    ap.add_argument("--patch", action="store_true", help="run: add the full patch of the C residual at s and w")
    ap.add_argument("--embed", action="store_true", help="run: add the input-embedding difference direction")
    ap.add_argument("--gap-rule", choices=["v1", "v2"], default="v1", help="run, with --patch: the layer-gap rule")
    ap.add_argument("--patch-dir", action="store_true", help="run: the dose control (the scene's patch at the lens push's norm)")  # fmt: skip
    ap.add_argument("--split", action="store_true", help="run: the scene's patch split, J-space part / rest")
    ap.add_argument("--same-scenes", default=None, help="run, fresh scenes: assert this run's draw")
    ap.add_argument("--subsets", nargs="+", choices=list(WHERE), default=None, help="run: push positions (default all)")
    ap.add_argument("--rule", choices=["v1", "v2", "v2.1"], default=None,
                    help="run: the rule in the config (default v1); analyze: an amendment into a new folder")  # fmt: skip
    ap.add_argument("--layers", type=int, nargs="+", default=None, help="run: the layer grid (default the 27B's)")
    ap.add_argument("--context-layers", type=int, nargs="+", default=None, help="run, with --layers: the c layers")
    ap.add_argument("--v21-min-layer", type=int, default=V21_MIN_LAYER, help="run, with --layers: v2.1's lowest layer")
    ap.add_argument("--scales", type=float, nargs="+", default=None, help="run: the push sizes (default 1 2 4 8)")
    ap.add_argument("--fresh-seed", type=int, default=FRESH_SEED, help="run, fresh scenes: the draw's seed")
    ap.add_argument(
        "--exclude-runs", nargs="+", default=[], help="run, fresh scenes: also leave out these runs' scenes"
    )
    a = ap.parse_args()
    if a.stage == "run":
        assert a.why, "run needs --why"
        cfg = {**DEFAULTS, "n": a.n, "scenes": a.scenes, "rule": a.rule or DEFAULTS["rule"]}
        if a.layers:  # another depth (Qwen3.5-122B: the 27B's grid scaled by depth)
            assert a.context_layers, "--layers needs --context-layers"
            assert set(a.context_layers) <= set(a.layers), "--context-layers must be in --layers"
            cfg.update(layers=a.layers, context_layers=a.context_layers, v21_min_layer=a.v21_min_layer)
        if a.patch:
            cfg["patch"] = True
            cfg["gap_rule"] = a.gap_rule
        if a.embed:
            cfg["embed"] = True
        if a.patch_dir:
            cfg["patch_dir"] = True
        if a.split:
            cfg["split"] = True
        if a.same_scenes:
            assert a.scenes == "fresh", "--same-scenes compares a fresh draw"
            cfg["same_scenes"] = a.same_scenes
        if a.subsets:
            cfg["subsets"] = a.subsets
        if a.scales:
            cfg["scales"] = a.scales
        if a.scenes == "fresh" and (a.fresh_seed != FRESH_SEED or a.exclude_runs):
            cfg.update(fresh_seed=a.fresh_seed, exclude_runs=a.exclude_runs)
        stage_run(a.name, a.why, cfg)
    elif a.stage == "analyze":
        stage_analyze(a.name, a.rule)
    else:
        stage_figures(a.name)
