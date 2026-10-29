"""x51_das (batch 51, test 51.3; jobs/c3/batch51.yaml, design and rules fixed in advance; Q51.3 in
predictions/2026-10-28_dan.md): DAS at scale. 48.1's DAS (scripts/x48_das.py) for the two readers and 49.8's DAS for the
address (scripts/x49_das_pos.py) on pooled pairs, 9B first, then Muse, the 27B.

Method (48.1's, unchanged; its functions imported): at the bridge token at L (the layer fixed in advance) of the O
prompt, h <- h_O + R R^T (h_S - h_O), R [d x k] with orthonormal columns (torch.nn.utils.parametrizations.orthogonal);
Adam lr 1e-3, batch 16 (micro-batches of 8, gradient accumulation), at most 300 steps; loss = cross-entropy of the target
token at X0's chat read position (the appended space). Early stopping on dev IIA (the brief's words; 48.1's code has no
early stopping, so it is added here around 48.1's loop, which it reproduces step for step): every 25 steps the dev
split's IIA (the share of dev rows whose argmax at the read is the target, under the current R, the training forward)
is read; the R of the best dev IIA is kept (ties: the earlier); training stops after 4 reads without a gain. The
shuffled-target baseline is early-stopped on its own (shuffled) dev targets. BJ_DAS_GDN=torch for the Qwen Gated
DeltaNet backward on Hopper (x48_das.torch_gdn).

Identity pairs (48.1's readers): every locker-first scene where the whole change switches the given reader, pooled from
the main test (the target's x0_necessity run of 48.1, the generator's cf), the clean design (the target's 45m run,
x0_necessity with alt fresh) and the routes scenes (x6_routes C0: the asked pick changes from A to B, nothing else; C1
keeps the item and C2 also moves two locker sentences, so neither is an identity pair). Each source's stored whole-change
read at L decides the reader's switch; the scenes are rebuilt with the tokenizer and asserted equal to the stored ids.
Target 300-600 pairs per reader: a reader with fewer than 300 from the stored runs is topped up with further C0 scenes
of x6_routes' generator (seed 2510; the stored run read the first 300 eligible), read here in generator order (X0's
competence: both readers say and read O's and S's answers right; then the whole change at L) until every reader has 300
or N_TOPUP_GEN generated scenes are used; a reader with more than 600 keeps its first 600 in pool order (main, clean,
routes, top-up). Entities held out 60 / 20 / 20 (train / select = dev / test) by the original bridge entity, seed 0
(x48_das.split_entities over the pooled pairs).

Address pairs (49.8's): x6_routes C1 position counterfactuals (the bridge's locker sentence swapped with another slot's,
a new number in S; the target = O's locker digit at the slot it moves to), every slot pair (i -> j) pooled, kept when
the whole change sends the lookup to the position answer; the stored routes run's 300 eligible C1 scenes first, then
further generator C1 scenes read here until >= 300 pairs (the same top-up). Split by bridge entity 60 / 20 / 20, seed 0.

k: recall {4, 16, 64, 128}; lookup {4, 16}; address {2, 4, 8}. Per R: an untrained random R of the same k and an R trained
on shuffled targets (48.1's and 49.8's seeds). Reads on the select and test pairs (X0's chat read, AddRows at L):
identity pairs, both readers, under none / whole / every R_lookup, R_recall and R_pos (the address subspace on each
reader: cross) / random / shuffled; address pairs as 49.8 (the lookup's route, the recall's move). 48.1's routes read
(R_lookup alone on 100 x6_routes C2 scenes) for its rule (d). Geometry (x48_das.geometry_row): energy, the share of
R R^T Delta inside the pair's 25 / 100 signed-OMP J++ atoms, its 25 W_E atoms, U, U_fit, W (47.2's slot subspace) and
outside the union (J++-25, U, W_E-25); per R ||R^T U||_F^2 / rank U and the same for W.
U = x0_massmean.subspaces' Alf on the target's probe run (x48_das.pointer_basis). W = 47.2's W: scripts/x47_six.py's
fit, results/x47_six/<x47_six.RUNS[target]>/fit.npz ("W", the layout-free slot subspace on the six-locker fit half),
not refit; absent for a target without that run (then every W read is None).

Rules (fixed in advance): 48.1's (a)-(d) and fallback (x48_das.rules) on the identity part; 49.8's labels at k = 4
(x49_das_pos.rules) on the address part; and "no low-dimensional recall subspace at this token and layer" if the
recall's own-IIA < 0.5 at k = 128 with >= 300 pairs (a result, not a failure to converge).

SEALED: the run writes no verdict; `verdict` and `view` (CPU) refuse until predictions/2026-10-28_dan.md holds Dan's
Q51.3 answer at the committed HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x51_das.py plan --out results/x51_das/plan-<UTC>       # CPU, tokenizer
BJ_TARGET=qwen3.5-9b BJ_DAS_GDN=torch uv run python scripts/x51_das.py run --name qwen35_9b_x51_3   # GPU (sealed)
uv run python scripts/x51_das.py verdict --runs qwen35_9b_x51_3 muse30_x51_3 x51_3_27b             # CPU, after Q51.3
uv run python scripts/x51_das.py view --runs qwen35_9b_x51_3 muse30_x51_3 x51_3_27b                # CPU, after Q51.3
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

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x48_das as D
from scripts import x49_das_pos as Q

EXP = "x51_das"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = D.PREDICTIONS
QUESTION = "Q51.3"
LOOKUP, RECALL = X.LOOKUP, X.RECALL
READER_NAME = D.READER_NAME
RENDERING = "chat"
# the stored runs the pairs come from (chat, the layer fixed in advance)
MAIN_RUN = D.MAIN_RUN  # the main test (the generator's cf), 48.1's
CLEAN_RUN = {"qwen3.5-9b": "qwen35_9b_x45m_fresh", "muse-glimmer-30b": "muse30b_x45m_fresh",
             "qwen3.6-27b": "x45m_fresh_27b"}  # the clean design (45m: alt fresh)  # fmt: skip
ROUTES_RUN = {
    "qwen3.5-9b": "qwen35_9b_x6_routes",
    "muse-glimmer-30b": "muse30b_x6_routes",
    "qwen3.6-27b": "x6_routes_27b",
    "nemotron-3.5-lightning": "nem35l_x52_routes",  # batch 52 C, at the committed L14
}
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_3", "muse-glimmer-30b": "muse30_x51_3", "qwen3.6-27b": "x51_3_27b"}
# Batch 52, Lightning ports (Dan's 08:55 queue item 3; jobs/c3/x52_lightning_das51.yaml): a coverage run (verdict
# --coverage, no seal guard, 'no prediction', x52_das51-<UTC>/); RUNS and 51.3's own verdict unchanged. Lightning's clean
# one-pick design has no run at L14 (its gate fails); its identity pool is the other two sources, both past their gates.
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_das51"}
# the coordinator's label (29 Oct 10:15 Paris, option A), in the spec, coverage.txt and the verdict
NO_CLEAN = {"nemotron-3.5-lightning": "adapted design: the clean one-pick source left out (its gate fails on Lightning, "
                                      "recall 0.751 < 0.80, results/x0_necessity/nem35l_x45s_smoke_clean/gate.json); "
                                      "pairs from the main test and routes C0 only (354 lookup / 350 recall, above the "
                                      "300 bar)"}  # fmt: skip
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_das/verdict-20261028T194630Z"  # 51.3's rules first scored (the 9B, Muse, the 27B)
KS = {LOOKUP: (4, 16), RECALL: (4, 16, 64, 128)}
KS_POS = (2, 4, 8)
K_POS_RULE = Q.K_RULE  # 49.8's rule reads k = 4
ID_MIN, ID_MAX, POS_MIN = 300, 600, 300
N_TOPUP_GEN = (
    1400  # x6_routes.scenes(tok, n) per condition for the top-up (prefix-stable: its first 700 are the stored runs')
)
TOPUP_CHUNK = 16
EVAL_EVERY, PATIENCE = 25, 4
OMP_CHUNK = 64
K_RECALL_RULE, NO_RECALL, N_RULE = 128, 0.5, 300
U_OVERLAP = 0.6  # Q51.3 (iii): the learned address overlaps U >= 0.6 (49.8's "ours" bar on U's energy in R_pos)
MOSTLY = 0.5  # Q51.3 (ii), descriptive: a part holding >= half of the lookup subspace's energy
EPS = 1e-9
SOURCES = ("main", "clean", "routes", "routes_topup")
RULE_NEW = ("no low-dimensional recall subspace at this token and layer: the recall's own-IIA < 0.5 at k = 128 with "
            ">= 300 pairs (a result, not a failure to converge)")  # fmt: skip
AS_COMPUTED = (
    "identity part: 48.1's as-computed reading (x48_das.AS_COMPUTED) with per-reader k sets (lookup {4, 16}, recall {4, "
    "16, 64, 128}): chosen k per reader = the smallest k <= 16 whose select-split own-IIA >= 0.7, else the k with the "
    "highest select own-IIA; every rule at the chosen k on the test entities' pairs; 48.1's fallback reads the lookup at "
    "k = 64, which 51.3 does not train, so it is 'not tested'; address part: 49.8's (x49_das_pos.AS_COMPUTED) at k = 4; "
    "the new rule: the recall's pairs (all splits) >= 300 and its test own-IIA at k = 128 < 0.5 (point estimate, EPS at "
    "the bar); Q51.3 (i) 'found' = >= 300 recall pairs and test own-IIA >= 0.5 at some k <= 128; (ii) the lookup "
    "subspace (R_lookup at its chosen k) on the test pairs: the share of R R^T Delta inside U, the J++-25 atoms, the "
    "W_E-25 atoms and outside their union, each part >= 0.5 named 'mostly' (descriptive; the parts overlap); (iii) U's "
    "energy in R_pos at k = 4 = ||R_pos^T U||_F^2 / rank U >= 0.6; cross-IIA: R_lookup read by the recall and R_recall "
    "by the lookup (48.1's), R_pos read by each reader on the identity test pairs (switch to S's answer) beside the "
    "random R of the same k, and the recall's move under R_pos on the address test pairs (49.8's); point estimates "
    "decide, cluster-bootstrap CIs over bridge entities (10,000, seed 0) beside; dev = the select split (early stopping "
    "and the choice of k)"
)


# ---- pairs (tokenizer only) ---------------------------------------------------------------------------------------


def marked_o(tok, rd: dict, pos: int, space: list[int]) -> str:
    """The reader's O prompt as the model reads it (the space token appended), the bridge token in ⟦bridge:…⟧."""
    return Q.marked(tok, rd["ids"]["org"], pos, space, {})


def identity_pair(tok, c: dict, sw: dict[str, int], source: str) -> dict:
    """One scene (an X0 case or an x6_routes C0 case) as an identity pair: both readers' prompts and answers, the stored
    whole-change switches, the original bridge's locker-sentence index (x0_probe.positions; U_fit's classes)."""
    from scripts import x0_probe as P

    pos = c["pos"]
    for v in ("org", "alt"):
        assert c["readers"][LOOKUP]["ids"][v][: pos + 1] == c["readers"][RECALL]["ids"][v][: pos + 1], (
            f"{c['scene']}: the readers' prompts differ through the bridge"
        )
    readers = {w: {**{k: rd[k] for k in ("question", "answer", "cf_answer", "tok_A", "tok_b", "ids")},
                   "marked": marked_o(tok, rd, pos, c["space"])} for w, rd in c["readers"].items()}  # fmt: skip
    return {"scene": f"{source}:{c['scene']}", "source": source, "source_scene": c["scene"], "entity": c["bridge"],
            "cf_bridge": c["cf_bridge"], "domain": c["domain"], "pos": pos, "space": c["space"], "context": c["context"],
            "cf_context": c["cf_context"], "stored_whole": {w: int(sw.get(w, 0)) for w in X.READERS},
            "locker_index": P.positions(c)[1], "readers": readers}  # fmt: skip


def x0_pool(tok, run: str, layer: int, alt: str, source: str) -> tuple[list[dict], dict]:
    """A stored x0_necessity run's eligible chat scenes at the layer (its read order), locker-first (x48_das.locker_first),
    switched by the stored whole change for at least one reader; rebuilt with the tokenizer (x48_das.rebuild; ids and
    the bridge index asserted equal to the stored ones). x48_das.select_pairs generalised to the 45m run's alt."""
    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert (m.get("alt") or "cf") == alt, f"{run}: alt {m.get('alt')!r}, not {alt!r}"
    assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
    assert layer in m["layers"], f"{run}: layer {layer} not read"
    assert m["model"]["target"] == pins.TARGET, f"{run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    if alt == "fresh":
        assert m["fresh"]["seed"] == X.FRESH_SEED, f"{run}: fresh seed {m['fresh']['seed']}, not {X.FRESH_SEED}"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
    whole = D.stored_whole(src, layer)
    order = json.loads((src / "gate.json").read_text()).get("order", {}).get(RENDERING) or sorted(whole)
    assert order, f"{run}: no chat scenes at layer {layer}"
    assert set(order) == set(whole), f"{run}: the chat order and the whole-arm scenes differ"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    rebuilt = {c["scene"]: c for c in D.rebuild(tok, m["set"], alt)}
    pool, counts = [], collections.Counter()
    for scene in order:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {run}"
        counts["read"] += 1
        if not D.locker_first(c):
            counts["not locker-first"] += 1
            continue
        sw = {w: whole[scene].get(w, 0) for w in X.READERS}
        if not any(sw.values()):
            counts["locker-first, the whole change switches neither reader"] += 1
            continue
        pool.append(identity_pair(tok, c, sw, source))
    counts["kept"] = len(pool)
    return pool, {"run": run, "alt": alt, "counts": dict(counts),
                  "per_reader": {READER_NAME[w]: sum(p["stored_whole"][w] for p in pool) for w in X.READERS}}  # fmt: skip


def scene_index(scene: str) -> int:
    """x6_routes' scene id 'C0-0123' -> its base scene's generator index (shared by C0 / C1 / C2)."""
    return int(scene.rsplit("-", 1)[1])


def routes_locker_first(c: dict) -> bool:
    """Every locker sentence before every pick sentence, in O and in S (x6_routes' layout)."""
    for ctx in (c["context"], c["cf_context"]):
        kinds = ["L" if s.startswith("The locker of") else "P" for s in ctx.split(". ")]
        if "P" in kinds and "L" in kinds[kinds.index("P") :]:
            return False
    return True


def stored_routes(run: str, layer: int, condition: str) -> tuple[Path, dict, dict[str, dict[str, dict]]]:
    """A stored x6_routes run (asserted: the target, the layer, the scene seed, chat): its cases of the condition and
    each scene's whole-change rows per reader."""
    from scripts import x6_routes as R

    src = R.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == pins.TARGET, f"{run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    assert m["layer"] == layer, f"{run}: layer {m['layer']}, not {layer}"
    assert m["seed"] == R.SEED, f"{run}: scene seed {m['seed']}, not {R.SEED}"
    assert m["model"].get("prompt_format", RENDERING) == RENDERING, f"{run} is not a chat run"
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["condition"] == condition}
    whole: dict[str, dict[str, dict]] = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["condition"] == condition and r["arm"] == "whole":
            whole.setdefault(r["scene"], {})[r["reader"]] = r
    assert whole, f"{run}: no {condition} whole-change reads"
    assert set(whole) <= set(cases), f"{run}: {condition} whole-change reads without a case"
    return src, cases, whole


def routes_pool(tok, run: str, layer: int, generated: list[dict]) -> tuple[list[dict], dict]:
    """The stored routes run's C0 scenes (the asked pick changes from A to B; locker-first by construction, asserted)
    the stored whole change switches for at least one reader; rebuilt from the generator's cases (ids asserted)."""
    _, cases, whole = stored_routes(run, layer, "C0")
    rebuilt = {c["scene"]: c for c in generated if c["condition"] == "C0"}
    pool, counts = [], collections.Counter()
    for scene, old in cases.items():
        if scene not in whole:
            continue
        c = rebuilt[scene]
        assert c["pos"] == old["pos"], f"{scene}: the bridge position moved since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {run}"
        assert routes_locker_first(c), f"{scene}: not locker-first"
        counts["read"] += 1
        sw = {w: int(whole[scene][w]["switched"]) for w in X.READERS}
        if not any(sw.values()):
            counts["the whole change switches neither reader"] += 1
            continue
        pool.append(identity_pair(tok, c, sw, "routes"))
    counts["kept"] = len(pool)
    return pool, {"run": run, "condition": "C0", "counts": dict(counts), "last_stored_index": max(map(scene_index, whole)),
                  "per_reader": {READER_NAME[w]: sum(p["stored_whole"][w] for p in pool) for w in X.READERS}}  # fmt: skip


def finish_identity(pool: list[dict]) -> tuple[list[dict], dict]:
    """The pooled identity pairs: duplicates (the same O and S prompts) dropped, each reader's pairs = the scenes its
    stored whole change switches, its first ID_MAX in pool order; scenes in neither reader's pairs dropped; split by
    the original bridge entity 60 / 20 / 20 (x48_das.split_entities, seed 0). Counts beside."""
    seen, uniq, dup = set(), [], 0
    for p in pool:
        key = tuple(p["readers"][LOOKUP]["ids"]["org"]), tuple(p["readers"][LOOKUP]["ids"]["alt"])
        if key in seen:
            dup += 1
            continue
        seen.add(key)
        uniq.append(p)
    before = {READER_NAME[w]: sum(p["stored_whole"][w] for p in uniq) for w in X.READERS}
    for w in X.READERS:
        n = 0
        for p in uniq:
            keep = bool(p["stored_whole"][w]) and n < ID_MAX
            p.setdefault("in_pairs", {})[w] = int(keep)
            n += keep
    out = [p for p in uniq if any(p["in_pairs"].values())]
    split = D.split_entities([p["entity"] for p in out]) if len(out) >= 3 else {}
    for p in out:
        p["split"] = split.get(p["entity"], "train")
    per = {READER_NAME[w]: {s: sum(p["split"] == s and p["in_pairs"][w] for p in out) for s in ("train", "select", "test")}
           for w in X.READERS}  # fmt: skip
    return out, {"pairs": len(out), "duplicates_dropped": dup, "per_reader_before_cap": before,
                 "per_reader": {READER_NAME[w]: sum(p["in_pairs"][w] for p in out) for w in X.READERS},
                 "per_reader_and_source": {READER_NAME[w]: dict(collections.Counter(p["source"] for p in out if p["in_pairs"][w]))
                                           for w in X.READERS},
                 "entities": len(split), "entities_per_split": dict(collections.Counter(split.values())),
                 "pairs_per_reader_and_split": per, "split_seed": D.SPLIT_SEED,
                 "scene_ids": {s: [p["scene"] for p in out if p["split"] == s] for s in ("train", "select", "test")}}  # fmt: skip


def need_identity(pool: list[dict]) -> dict[str, int]:
    """Per reader, how many identity pairs short of ID_MIN the pool is (0: enough)."""
    return {w: max(0, ID_MIN - sum(p["stored_whole"][w] for p in pool)) for w in X.READERS}


def generated_scenes(tok, n: int) -> list[dict]:
    from scripts import x6_routes as R

    return R.scenes(tok, n, rendering=RENDERING)[0]


def topup_candidates(generated: list[dict], condition: str, last_stored: int) -> list[dict]:
    """The generator's scenes of the condition after the stored run's last read one, in generator order."""
    return sorted((c for c in generated if c["condition"] == condition and scene_index(c["scene"]) > last_stored),
                  key=lambda c: scene_index(c["scene"]))  # fmt: skip


def pools(tok, target: str, layer: int, n_gen: int) -> dict[str, Any]:
    """Every stored pool of the target (CPU): identity from the main test, the clean design and routes C0; address from
    routes C1 (x49_das_pos.select_pairs); and the generator's top-up candidates (C0, C1) beyond the stored runs."""
    from scripts import x6_routes as R

    # one generation serves the stored scenes (routes_pool asserts their ids: the generator is prefix-stable in n) and
    # the top-up candidates after them
    generated = generated_scenes(tok, max(n_gen, R.N_GEN))
    main, i_main = x0_pool(tok, MAIN_RUN[target], layer, "cf", "main")
    if target in CLEAN_RUN:
        clean, i_clean = x0_pool(tok, CLEAN_RUN[target], layer, "fresh", "clean")
    else:  # batch 52: Lightning's clean design fails its gate (NO_CLEAN)
        clean, i_clean = [], {"run": None, "alt": "fresh", "absent": NO_CLEAN[target], "counts": {"read": 0, "kept": 0},
                              "per_reader": {READER_NAME[w]: 0 for w in X.READERS}}  # fmt: skip
    routes, i_routes = routes_pool(tok, ROUTES_RUN[target], layer, generated)
    address, i_address = Q.select_pairs(tok, ROUTES_RUN[target], layer)
    _, _, c1_whole = stored_routes(ROUTES_RUN[target], layer, "C1")
    last_c1 = max(map(scene_index, c1_whole))
    return {"identity": main + clean + routes, "address": address,
            "info": {"main": i_main, "clean": i_clean, "routes": i_routes,
                     "address": {k: v for k, v in i_address.items() if k != "scene_ids"}, "address_last_stored_index": last_c1},
            "candidates": {"C0": topup_candidates(generated, "C0", i_routes["last_stored_index"]),
                           "C1": topup_candidates(generated, "C1", last_c1)}}  # fmt: skip


def stored_eligible_beyond(run: str, condition: str, last: int) -> dict:
    """From the stored routes run's competence (it covers every generated scene of x6_routes.N_GEN): the scenes of the
    condition after the stored run's last read one that X0's competence check made eligible (both readers say and read
    O's and S's answers right): what the top-up can draw within the stored generation."""
    from scripts import x6_routes as R

    src = R.RESULTS / run
    ok: dict[str, bool] = collections.defaultdict(lambda: True)
    for r in X.read_jsonl(src / "competence.jsonl"):
        if r["scene"].startswith(condition) and r["rendering"] == RENDERING:
            ok[r["scene"]] = ok[r["scene"]] and bool(r["right"]) and bool(r["read_right"])
    beyond = [s for s in ok if scene_index(s) > last]
    return {"generated_beyond": len(beyond), "eligible_beyond": sum(ok[s] for s in beyond)}


def stage_plan(out: Path | None = None, n_gen: int = N_TOPUP_GEN) -> dict:
    """CPU: every pool from the stored runs with the target's tokenizer (counts per source and reader, after the cap,
    the split), the top-up need and supply (the stored competence beyond the stored reads), prompt lengths, arms."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target, layer = pins.TARGET, X.PREDICTED[pins.TARGET]
    pl = pools(tok, target, layer, n_gen)
    ident = pl["identity"]
    need = need_identity(ident)
    fin, i_fin = finish_identity(ident)
    addr = pl["address"]
    rates = {READER_NAME[w]: round(pl["info"]["routes"]["per_reader"][READER_NAME[w]] / max(1, pl["info"]["routes"]["counts"]["read"]), 4)
             for w in X.READERS}  # fmt: skip
    pos_rate = round(len(addr) / max(1, pl["info"]["address"]["scenes_read"]), 4)
    supply = {
        "C0": stored_eligible_beyond(ROUTES_RUN[target], "C0", pl["info"]["routes"]["last_stored_index"]),
        "C1": stored_eligible_beyond(ROUTES_RUN[target], "C1", pl["info"]["address_last_stored_index"]),
    }
    lengths = {s: [len(p["readers"][LOOKUP]["ids"]["org"]) for p in ident if p["source"] == s] for s in SOURCES}
    blob: dict[str, Any] = {
        "target": target, "layer": layer, "prefix": pins.RUN_PREFIX, "run_name": {**RUNS, **COVERAGE_RUNS}.get(target),
        "sources": {k: pl["info"][k] for k in ("main", "clean", "routes")},
        "identity_from_stored": {k: v for k, v in i_fin.items() if k != "scene_ids"},
        "identity_short_of_300": {READER_NAME[w]: n for w, n in need.items()},
        "identity_topup": {"needed": any(need.values()), "routes_C0_switch_rate_stored": rates,
                           "stored_generation_beyond": supply["C0"], "candidates_up_to_n_gen": len(pl["candidates"]["C0"]),
                           "n_gen": n_gen,
                           "expected_extra_switches_within_stored_generation": {
                               r: round(rate * supply["C0"]["eligible_beyond"], 1) for r, rate in rates.items()}},
        "address_from_stored": pl["info"]["address"],
        "address_short_of_300": max(0, POS_MIN - len(addr)),
        "address_topup": {"needed": len(addr) < POS_MIN, "position_rate_stored": pos_rate,
                          "stored_generation_beyond": supply["C1"], "candidates_up_to_n_gen": len(pl["candidates"]["C1"]),
                          "expected_extra_within_stored_generation": round(pos_rate * supply["C1"]["eligible_beyond"], 1)},
        "prompt_tokens": {s: [min(v), max(v)] for s, v in lengths.items() if v},
        "ks": {READER_NAME[w]: list(k) for w, k in KS.items()} | {"address": list(KS_POS)},
        "arms_identity": identity_arms(), "arms_address": Q.arm_names(KS_POS),
        "trainings": 2 * (sum(len(k) for k in KS.values()) + len(KS_POS)),
    }  # fmt: skip
    try:
        _, u = D.pointer_basis(target)
        blob["U"] = {"states_run": u["states_run"], "rank": u["rank"]}
    except FileNotFoundError as e:
        blob["U"] = f"probe run not here: {e}"
    blob["W"] = w_record(target, layer)
    pick = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(fin)), min(5, len(fin))))
    blob["rendered"] = [{"scene": fin[i]["scene"], "split": fin[i]["split"], "bridge": f"{fin[i]['entity']} -> {fin[i]['cf_bridge']}",
                         "S_context": fin[i]["cf_context"],
                         "readers": {READER_NAME[w]: {"marked": rd["marked"], "answer": rd["answer"], "cf_answer": rd["cf_answer"],
                                                      "in_pairs": fin[i]["in_pairs"][w]} for w, rd in fin[i]["readers"].items()}}
                        for i in pick]  # fmt: skip
    print(json.dumps({k: v for k, v in blob.items() if k != "rendered"}, indent=1, ensure_ascii=False))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{target}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
        blobs = [json.loads(p.read_text()) for p in sorted(out.glob("*.json"))]
        (out / "plan.md").write_text("\n".join(plan_lines(blobs)) + "\n")
        print("wrote", out)
    return blob


def plan_lines(blobs: list[dict]) -> list[str]:
    lines = ["# 51.3 plan (CPU, the stored runs and each target's tokenizer): DAS at scale", "",
             "Written by `scripts/x51_das.py plan` before any run. Identity pairs = locker-first scenes the stored whole "
             "change switches for the reader (main test, clean design, routes C0); address pairs = routes C1 scenes the "
             "stored whole change sends to the position answer. Counts from the stored runs only; the top-up (further "
             "generator scenes read on the GPU) is estimated from the stored rates. UNVERIFIED.", ""]  # fmt: skip
    for b in blobs:
        i = b["identity_from_stored"]
        lines += [f"## {b['target']} at L{b['layer']} (run {b['run_name']})", "",
                  "| source | run | read | locker-first scenes kept | lookup pairs | recall pairs |", "|---|---|---|---|---|---|"]  # fmt: skip
        for s, v in b["sources"].items():
            c = v["counts"]
            lines.append(f"| {s} | {v['run']} | {c.get('read')} | {c.get('kept')} | {v['per_reader']['lookup']} | "
                         f"{v['per_reader']['recall']} |")  # fmt: skip
        lines += ["", f"- identity pairs pooled: {i['pairs']} scenes ({i['duplicates_dropped']} duplicates dropped); per reader "
                  f"before the cap of {ID_MAX} {i['per_reader_before_cap']}, after {i['per_reader']}; per reader and source "
                  f"{i['per_reader_and_source']}",
                  f"- entities {i['entities']} ({i['entities_per_split']}); pairs per reader and split {i['pairs_per_reader_and_split']}",
                  f"- short of {ID_MIN} per reader: {b['identity_short_of_300']}; top-up: {b['identity_topup']}",
                  f"- address pairs from the stored run: {b['address_from_stored'].get('pairs')} of "
                  f"{b['address_from_stored'].get('scenes_read')} C1 scenes read (routes {b['address_from_stored'].get('whole_change_routes')}); "
                  f"moves {b['address_from_stored'].get('moves')}; short of {POS_MIN}: {b['address_short_of_300']}; top-up: {b['address_topup']}",
                  f"- prompt tokens per source {b['prompt_tokens']}; U {b['U']}; W {b['W']}",
                  f"- k {b['ks']}; trainings {b['trainings']} (R and shuffled per k); identity arms {len(b['arms_identity'])}, "
                  f"address arms {len(b['arms_address'])}", "",
                  f"### {len(b['rendered'])} random identity pairs (seed {X.EXAMPLES_SEED}), O as the model reads it", ""]  # fmt: skip
        for e in b["rendered"]:
            lines += [
                f"#### {e['scene']} ({e['split']}): bridge {e['bridge']}",
                "",
                f"S's context: {e['S_context']}",
                "",
            ]
            for r, rd in e["readers"].items():
                lines += [f"{r}: O answers {rd['answer']}, S answers {rd['cf_answer']}; in its pairs: {rd['in_pairs']}", "",
                          "```", rd["marked"], "```", ""]  # fmt: skip
    return lines


def w_record(target: str, layer: int) -> dict | str:
    try:
        return load_w(target, layer)[1]
    except FileNotFoundError as e:
        return f"absent: {e}"


def load_w(target: str, layer: int) -> tuple[np.ndarray, dict]:
    """W: 47.2's slot subspace (scripts/x47_six.py's fit on the six-locker fit half, results/x47_six/<run>/fit.npz "W"),
    the run x47_six.RUNS[target] (Lightning: its 47.2 coverage run, x47_six.COVERAGE_RUNS); not refit; its layer must be
    this test's. FileNotFoundError when the run is absent."""
    from scripts import x47_six as SIX

    run = SIX.RUNS.get(target) or SIX.COVERAGE_RUNS.get(target)
    if run is None:
        raise FileNotFoundError(f"no 47.2 run of {target}")
    src = SIX.RESULTS / run
    if not (src / "fit.npz").exists():
        raise FileNotFoundError(str((src / "fit.npz").relative_to(pins.REPO_ROOT)))
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name}: not a {target} run"
    assert m["layer"] == layer, f"{src.name}: layer {m['layer']}, not {layer}"
    w = np.load(src / "fit.npz")["W"].astype(np.float64)
    assert np.allclose(w.T @ w, np.eye(w.shape[1]), atol=1e-5), f"{src.name}: W's columns are not orthonormal"
    rel = str((src / "fit.npz").relative_to(pins.REPO_ROOT))
    return w, {"run": src.name, "slots": m.get("slots"), "rank": int(w.shape[1]), "file": rel,
               "sha256": X.sha256_of(src / "fit.npz")}  # fmt: skip


# ---- DAS with early stopping (torch) ------------------------------------------------------------------------------


def dev_iia(model, layer: int, dev: list[dict], targets: list[int], r_mat, micro: int) -> float:
    """The share of dev rows whose argmax at the read position is the target under h_O + R R^T delta (the training
    forward, x48_das.batch_logits, no gradient)."""
    import torch

    hits = 0
    with torch.no_grad():
        r = r_mat.to(model.device).float()
        for s in range(0, len(dev), micro):
            chunk = dev[s : s + micro]
            delta = torch.stack([d["delta"] for d in chunk]).to(model.device).float()
            logits = D.batch_logits(
                model, layer, [d["ids"] for d in chunk], [d["pos"] for d in chunk], (delta @ r) @ r.T
            )
            hits += int((logits.argmax(-1).cpu() == torch.tensor(targets[s : s + micro])).sum())
    return hits / len(dev)


def train_early(model, layer: int, rows: list[dict], dev: list[dict], k: int, seed: int, steps: int = D.STEPS,
                batch: int = D.BATCH, lr: float = D.LR, micro: int = D.MICRO, shuffle: int | None = None,
                eval_every: int = EVAL_EVERY, patience: int | None = PATIENCE, log: list | None = None,
                desc: str = "") -> tuple[Any, dict]:  # fmt: skip
    """x48_das.train_subspace's loop step for step (its init, Adam, batch draws, micro-batches, loss) with early stopping
    on dev IIA: every `eval_every` steps (and at the last) dev_iia under the current R; the best R kept (strictly
    better replaces; ties keep the earlier); stop after `patience` reads without a gain (None: never). With shuffle,
    the training rows' targets are permuted once as in train_subspace and the dev rows' targets with the same seed (the
    baseline stops on its own objective). No dev rows: train_subspace's R at the last step. Returns (R on the CPU,
    fp32, the stopping record)."""
    import torch

    from bridge_jspace.utils import progress

    targets = [r["target"] for r in rows]
    dev_targets = [r["target"] for r in dev]
    if shuffle is not None:
        random.Random(shuffle).shuffle(targets)
        random.Random(shuffle).shuffle(dev_targets)
    d = rows[0]["delta"].shape[-1]
    # the orthogonal parametrisation draws from the global torch RNG (its completion of the tall R), so 48.1's loop is
    # not fixed by its seed alone; seeding the global RNG here makes every R reproducible from its seed
    torch.manual_seed(seed)
    mod = D.subspace_module(d, k, seed).to(model.device)
    opt = torch.optim.Adam(mod.parameters(), lr=lr)
    rng = random.Random(D.BATCH_SEED + seed)
    n = len(rows)
    best, best_step, bad, evals, stopped = -1.0, None, 0, [], steps - 1
    r_best = None
    for step in progress(range(steps), desc or f"DAS k={k}", total=steps):
        idx = rng.sample(range(n), min(batch, n))
        opt.zero_grad(set_to_none=True)
        total, hits = 0.0, 0
        for s in range(0, len(idx), micro):
            r_mat: Any = mod.weight
            chunk = idx[s : s + micro]
            delta = torch.stack([rows[i]["delta"] for i in chunk]).to(model.device).float()
            adds = (delta @ r_mat) @ r_mat.T
            logits = D.batch_logits(
                model, layer, [rows[i]["ids"] for i in chunk], [rows[i]["pos"] for i in chunk], adds
            )
            tgt = torch.tensor([targets[i] for i in chunk], device=logits.device)
            loss = torch.nn.functional.cross_entropy(logits, tgt, reduction="sum") / len(idx)
            loss.backward()
            total += float(loss.detach())
            hits += int((logits.argmax(-1) == tgt).sum())
        opt.step()
        rec = {"k": k, "step": step, "loss": round(total, 4), "batch_acc": round(hits / len(idx), 4)}
        if dev and ((step + 1) % eval_every == 0 or step == steps - 1):
            with torch.no_grad():
                weight: Any = mod.weight
                r_now = weight.detach().float().cpu().clone()
            acc = dev_iia(model, layer, dev, dev_targets, r_now, micro)
            evals.append({"step": step, "dev_iia": round(acc, 4)})
            rec["dev_iia"] = round(acc, 4)
            if acc > best + EPS:
                best, best_step, r_best, bad = acc, step, r_now, 0
            else:
                bad += 1
            if log is not None:
                log.append(rec)
            if patience is not None and bad >= patience:
                stopped = step
                break
        elif log is not None and (step % 25 == 0 or step == steps - 1):
            log.append(rec)
    if r_best is None:
        with torch.no_grad():
            weight = mod.weight
            r_best = weight.detach().float().cpu().clone()
    assert torch.allclose(r_best.T @ r_best, torch.eye(k), atol=1e-4), "R's columns are not orthonormal"
    return r_best, {"best_step": best_step, "best_dev_iia": None if best < 0 else round(best, 4), "stopped_at": stopped,
                    "evals": evals, "n_dev": len(dev), "micro": micro}  # fmt: skip


def train_fit(model, layer: int, rows: list[dict], dev: list[dict], k: int, seed: int, steps: int, micro: int,
              shuffle: int | None, log: list, desc: str) -> tuple[Any, dict]:  # fmt: skip
    """train_early; on a CUDA out-of-memory error the same training restarts from its seed with half the micro-batch
    (the same step: batch 16 by gradient accumulation; the rows, k and steps unchanged), recorded in the stop record."""
    import torch

    tried: list[int] = []
    start = len(log)
    while True:
        try:
            r, info = train_early(model, layer, rows, dev, k, seed, steps=steps, micro=micro, shuffle=shuffle,
                                  log=log, desc=desc)  # fmt: skip
            return r, {**info, "oom_micro_tried": tried}
        except torch.cuda.OutOfMemoryError:
            tried.append(micro)
            if micro <= 1:
                raise
            print(f"{desc}: CUDA out of memory at micro-batch {micro}; restarting with {micro // 2}", flush=True)
            del log[start:]  # the failed try's records
            torch.cuda.empty_cache()
            micro //= 2


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def identity_arms() -> list[str]:
    """Every arm read on the identity pairs, in order: none, whole, R per reader and k, R_pos per k (cross), a random R
    per k of every part, the shuffled-target R per reader and k."""
    out = ["none", "whole"]
    out += [f"R_{w}_k{k}" for w in X.READERS for k in KS[w]]
    out += [f"R_pos_k{k}" for k in KS_POS]
    out += [f"rand_k{k}" for k in all_ks()]
    out += [f"shuf_{w}_k{k}" for w in X.READERS for k in KS[w]]
    return out


def all_ks() -> list[int]:
    return sorted({*KS[LOOKUP], *KS[RECALL], *KS_POS})


def bridge_states(model, pairs: list[dict], layer: int, desc: str):
    """h_O, h_S at the bridge token at the layer (one forward per prompt, the lookup's ids; the readers' prompts are
    identical through the bridge), fp32 on the CPU."""
    import torch

    from bridge_jspace.utils import progress

    h_o, h_s = [], []
    with torch.no_grad():
        for it in progress(pairs, desc) if desc else pairs:
            ids = it["readers"][LOOKUP]["ids"]
            for v, acc in (("org", h_o), ("alt", h_s)):
                rec = model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1]
                acc.append(rec[layer][it["pos"]].float().cpu().clone())
    return torch.stack(h_o), torch.stack(h_s)


def topup(model, cases: list[dict], layer: int, ws, digits, done, chunk: int = TOPUP_CHUNK) -> tuple[list[dict], dict]:
    """Further generator scenes read in order: X0's competence (both readers say and read O's and S's answers right:
    eligible), then the whole change (h_S - h_O at the bridge token at L, X0's chat read with AddRows) for both readers;
    after each scene done(records) decides whether to stop. The records (one per scene read) and the gate: O's read
    accuracy per reader over the scenes whose competence was read (>= 0.80)."""
    import torch

    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    records: list[dict] = []
    comp_all: list[dict] = []
    stop = False
    for s in range(0, len(cases), chunk):
        part = cases[s : s + chunk]
        comp = X.competence(model, part, digits, ws)
        right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
        for c in part:
            comp_all += [r for r in comp if r["scene"] == c["scene"]]
            ok = all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                     for w in X.READERS for v in ("org", "alt"))  # fmt: skip
            rec: dict[str, Any] = {"scene": c["scene"], "condition": c["condition"], "eligible": int(ok)}
            if ok:
                h_o, h_s = bridge_states(model, [c], layer, "")
                dx = (h_s - h_o).to(model.device)
                with torch.no_grad():
                    for w, rd in c["readers"].items():
                        lg = X.read_logits(model, rd["ids"]["org"], [{layer: AddRows(dx, [c["pos"]])}], RENDERING,
                                           c["space"], ws)[0][0]  # fmt: skip
                        row = X.read_row(lg, rd, digits)
                        rec[w] = {**{k: row[k] for k in ("switched", "top", "role")},
                                  "route": R.classify(row["top"], c) if w == LOOKUP else None}  # fmt: skip
            records.append(rec)
            if done(records):
                stop = True
                break
        if stop:
            break
    acc = {READER_NAME[w]: round(float(np.mean([r["read_right"] for r in comp_all if r["reader"] == w and r["variant"] == "org"])), 4)
           if comp_all else None for w in X.READERS}  # fmt: skip
    gate = {"scenes_read": len(records), "org_read_accuracy": acc, "eligible": sum(r["eligible"] for r in records),
            "pass": bool(comp_all) and all(a is not None and a >= X.GATE - EPS for a in acc.values()), "reached": stop}  # fmt: skip
    return records, gate


def identity_topup(model, tok, pool: list[dict], cands: list[dict], layer: int, ws, digits) -> tuple[list[dict], dict]:
    """Routes C0 scenes beyond the stored run, read until every reader has ID_MIN identity pairs (pool + top-up)."""
    need = need_identity(pool)
    if not any(need.values()):
        return [], {"needed": False}
    have = {w: sum(p["stored_whole"][w] for p in pool) for w in X.READERS}

    def done(recs: list[dict]) -> bool:
        return all(have[w] + sum(r.get(w, {}).get("switched", 0) for r in recs) >= ID_MIN for w in X.READERS)

    recs, gate = topup(model, cands, layer, ws, digits, done)
    by = {c["scene"]: c for c in cands}
    out = []
    for r in recs:
        if r["eligible"] and any(r[w]["switched"] for w in X.READERS):
            out.append(identity_pair(tok, by[r["scene"]], {w: r[w]["switched"] for w in X.READERS}, "routes_topup"))
    info = {"needed": True, "short": {READER_NAME[w]: n for w, n in need.items()}, "gate": gate,
            "added": {READER_NAME[w]: sum(p["stored_whole"][w] for p in out) for w in X.READERS}, "records": recs}  # fmt: skip
    if not gate["pass"]:
        info["dropped"] = "the top-up failed the 0.80 gate on O's read: its pairs are not used"
        return [], info
    return out, info


def address_topup(model, tok, pool: list[dict], cands: list[dict], layer: int, ws, digits) -> tuple[list[dict], dict]:
    """Routes C1 scenes beyond the stored run, read until POS_MIN position pairs (pool + top-up): those whose whole
    change sends the lookup to the position answer (x49_das_pos.position_pair)."""
    if len(pool) >= POS_MIN:
        return [], {"needed": False}

    def done(recs: list[dict]) -> bool:
        return len(pool) + sum(r.get(LOOKUP, {}).get("route") == "position" for r in recs) >= POS_MIN

    recs, gate = topup(model, cands, layer, ws, digits, done)
    by = {c["scene"]: c for c in cands}
    out = []
    for r in recs:
        if r["eligible"] and r[LOOKUP]["route"] == "position":
            p = Q.position_pair(tok, by[r["scene"]])
            p["stored_route"] = "position"
            p["stored_recall_kept"] = int(r[RECALL]["top"] == by[r["scene"]]["readers"][RECALL]["tok_A"])
            p["topup"] = 1
            out.append(p)
    info = {"needed": True, "short": POS_MIN - len(pool), "gate": gate, "added": len(out), "records": recs,
            "routes": dict(collections.Counter(r[LOOKUP]["route"] for r in recs if r["eligible"]))}  # fmt: skip
    if not gate["pass"]:
        info["dropped"] = "the top-up failed the 0.80 gate on O's read: its pairs are not used"
        return [], info
    return out, info


def geometry_rows(pairs: list[dict], x, mats: dict, jdic, wdic, u, u_fit, q_w, desc: str) -> list[dict]:
    """Per pair and R (x48_das.geometry_row): energy and the shares inside the pair's J++-25 / -100 and W_E-25 atoms,
    U, U_fit, W (if any) and outside the union; the OMP atoms per chunk of pairs."""
    import torch

    from bridge_jspace.utils import progress
    from scripts.x0_parts import omp_atoms

    atoms_j = torch.cat(
        [omp_atoms(jdic, x[s : s + OMP_CHUNK], max(D.K_JPP)).cpu() for s in range(0, len(x), OMP_CHUNK)]
    )
    atoms_w = torch.cat([omp_atoms(wdic, x[s : s + OMP_CHUNK], X.K_MAIN).cpu() for s in range(0, len(x), OMP_CHUNK)])
    on_x = {key: r_mat.to(x.device) for key, r_mat in mats.items()}
    geo = []
    for i, it in enumerate(progress(pairs, desc)):
        spans = D.spans_of(jdic, wdic, u, u_fit, atoms_j[i], atoms_w[i])
        if q_w is not None:
            spans["W"] = q_w
        for key, r_mat in on_x.items():
            geo.append({"scene": it["scene"], "entity": it["entity"], "split": it["split"], "R": key,
                        "norm": round(float(x[i].norm()), 4), **D.geometry_row(x[i], r_mat, spans)})  # fmt: skip
    return geo


def pos_reads(r_mat, u, w) -> dict[str, Any]:
    """x49_das_pos.subspace_reads; without W, its W fields None."""
    from scripts import x6_routes as R

    if w is not None:
        return Q.subspace_reads(r_mat, u, w)
    k, d = int(r_mat.shape[1]), int(r_mat.shape[0])
    return {"k": k, "cos2_U": round(float(R.mean_cos2(r_mat, R.orthonormal(u)) or 0.0), 6), "cos2_W": None,
            "random_expectation": round(k / d, 6), "angles_vs_U": D.principal_angles(r_mat.double(), R.orthonormal(u)),
            "angles_vs_W": None}  # fmt: skip


def stage_run(name: str, why: str, steps: int = D.STEPS, micro: int = D.MICRO, n_gen: int = N_TOPUP_GEN,
              n_routes: int = D.N_ROUTES) -> Path:  # fmt: skip
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.3 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"51.3 runs on {sorted({**RUNS, **COVERAGE_RUNS})}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    (out / "address").mkdir()
    u_np, u_info = D.pointer_basis(target)
    try:
        w_np, w_info = load_w(target, layer)
    except FileNotFoundError as e:
        w_np, w_info = None, f"absent: {e} (no 47.2 run of {target}; every W read is None)"
    x0_srcs = [X.RESULTS / r for r in (MAIN_RUN[target], CLEAN_RUN.get(target)) if r]
    files = [SPEC] + [s / f for s in x0_srcs for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "gate.json")]
    files += [R.RESULTS / ROUTES_RUN[target] / f
              for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "competence.jsonl", "gate.json")]  # fmt: skip
    if w_np is not None:
        files.append(pins.REPO_ROOT / w_info["file"])  # type: ignore[index]
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
        "test": "51.3", "spec": "jobs/c3/batch51.yaml (51.3)", "question": f"{QUESTION} ({PREDICTIONS})",
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in files},
        "layer": layer, "sources": {"main": MAIN_RUN[target], "clean": CLEAN_RUN.get(target) or NO_CLEAN[target],
                                    "routes": ROUTES_RUN[target]}, "adapted": NO_CLEAN.get(target),
        "ks": {READER_NAME[w]: list(k) for w, k in KS.items()} | {"address": list(KS_POS)},
        "training": {"method": "x48_das.train_subspace's loop (x51_das.train_early reproduces it step for step) with "
                               "early stopping on dev IIA", "optimizer": "Adam", "lr": D.LR, "max_steps": steps,
                     "batch": D.BATCH, "micro_batch": micro, "eval_every": EVAL_EVERY, "patience": PATIENCE,
                     "dev": "the select split (the reader's pairs; the address pairs)",
                     "dev_iia": "share of dev rows whose argmax at the read position (the training forward) is the target",
                     "shuffled_dev": "the dev rows' targets permuted with the shuffle seed (the baseline stops on its own objective)",
                     "oom": "on CUDA OOM a training restarts from its seed with half the micro-batch (recorded per R)",
                     "global_rng": "torch.manual_seed(the R's init seed) before each training (the orthogonal "
                                   "parametrisation draws from the global RNG; 48.1 / 49.8 left it unseeded)",
                     "seeds_identity": f"48.1's: init {D.INIT_SEED} + 100 k + reader (lookup 0, recall 1; shuffled + 10), "
                                       f"shuffle {D.SHUFFLE_SEED} + k + reader, random R {D.RAND_SEED} + k, batches "
                                       f"{D.BATCH_SEED} + the R's seed",
                     "seeds_address": f"49.8's: init {Q.INIT_SEED} + 100 k (shuffled + 10), shuffle {Q.SHUFFLE_SEED} + k, "
                                      f"random R {Q.RAND_SEED} + k"},
        "pairs": {"identity": "locker-first scenes the stored whole change switches for the reader, pooled (main test, "
                              "clean design, routes C0; duplicates dropped), routes C0 top-up to 300 per reader, the "
                              f"first {ID_MAX} per reader in pool order; split by bridge entity 60 / 20 / 20, seed "
                              f"{D.SPLIT_SEED}",
                  "address": "routes C1 scenes the whole change sends to the position answer (the stored run's, then "
                             f"the top-up to {POS_MIN}); split by bridge entity 60 / 20 / 20, seed {Q.SPLIT_SEED}",
                  "topup": f"x6_routes.scenes(tok, {n_gen}) (seed {R.SEED}), the scenes after the stored run's last "
                           "read one, in generator order; X0's competence, then the whole change at L"},
        "U": u_info, "W": w_info, "arms_identity": identity_arms(), "arms_address": Q.arm_names(KS_POS),
        "rules": {"48.1": D.RULE, "49.8": Q.RULE, "51.3": RULE_NEW}, "as_computed": AS_COMPUTED,
        "seeds": {"split": D.SPLIT_SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "routes_scenes": R.SEED},
        "n_boot": X.N_BOOT,
        "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer",
    }  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    if (patched := D.torch_gdn(model.hf)) is not None:
        m["gdn_kernel"] = f"torch reference ({D.GDN_ENV}=torch; {patched}.torch_chunk_gated_delta_rule replaced)"
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    if (record := D.torch_mamba(model.hf)) is not None:  # batch 52: NemotronH's Mamba-2 (x48_das.kernels_off)
        m["mamba_kernel"] = record
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    for p in model.hf.parameters():  # the DAS gradient reaches R only; no weight gradients are stored
        p.requires_grad_(False)
    tok = model.tokenizer
    dev = model.device
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    # 1. the pairs: the stored pools, the top-ups, the splits
    pl = pools(tok, target, layer, n_gen)
    extra_i, top_i = identity_topup(model, tok, pl["identity"], pl["candidates"]["C0"], layer, ws, digits)
    extra_a, top_a = address_topup(model, tok, pl["address"], pl["candidates"]["C1"], layer, ws, digits)
    X.write_jsonl(out / "topup.jsonl", [{"part": "identity", **r} for r in top_i.pop("records", [])]
                  + [{"part": "address", **r} for r in top_a.pop("records", [])])  # fmt: skip
    ident, i_info = finish_identity(pl["identity"] + extra_i)
    addr = pl["address"] + extra_a
    a_info = {"routes_run": ROUTES_RUN[target], "layer": layer, "condition": Q.CONDITION, **Q.split_info(addr)}
    info = {"target": target, "layer": layer, "sources": {k: pl["info"][k] for k in ("main", "clean", "routes")},
            "identity": i_info, "identity_topup": top_i, "address_stored": pl["info"]["address"], "address": a_info,
            "address_topup": top_a}  # fmt: skip
    (out / "pairs.json").write_text(json.dumps(info, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", ident)
    X.write_jsonl(out / "address" / "cases.jsonl", addr)
    (out / "address" / "pairs.json").write_text(json.dumps(a_info, indent=2) + "\n")
    print(json.dumps({k: v for k, v in i_info.items() if k != "scene_ids"}), flush=True)
    print(json.dumps({k: v for k, v in a_info.items() if k != "scene_ids"}), flush=True)
    for s in ("train", "select", "test"):
        for w in X.READERS:
            assert i_info["pairs_per_reader_and_split"][READER_NAME[w]][s] > 0, f"{READER_NAME[w]}: no {s} pairs"
        assert a_info.get("pairs_per_split", {}).get(s, 0) > 0, f"address: no {s} pairs"
    # 2. the states at the bridge token, cached
    ho_i, hs_i = bridge_states(model, ident, layer, f"identity states at L{layer} (pair)")
    ho_a, hs_a = bridge_states(model, addr, layer, f"address states at L{layer} (pair)")
    x_i, x_a = hs_i - ho_i, hs_a - ho_a
    torch.save({"scenes": [p["scene"] for p in ident], "h_O": ho_i, "h_S": hs_i, "delta": x_i, "layer": layer,
                "pos": [p["pos"] for p in ident]}, out / f"states_L{layer}.pt")  # fmt: skip
    torch.save({"scenes": [p["scene"] for p in addr], "h_O": ho_a, "h_S": hs_a, "delta": x_a, "layer": layer,
                "pos": [p["pos"] for p in addr]}, out / "address" / f"states_L{layer}.pt")  # fmt: skip
    d = x_i.shape[1]
    # 3. training: per reader and k R and its shuffled twin (identity), R_pos and its twin (address), random R per k
    mats: dict[str, Any] = {f"rand_k{k}": D.random_basis(d, k, D.RAND_SEED + k) for k in all_ks()}
    mats_a: dict[str, Any] = {f"rand_k{k}": D.random_basis(d, k, Q.RAND_SEED + k) for k in KS_POS}
    log_rows: list[dict] = []
    stops: dict[str, dict] = {}

    def rows_of(pairs, x, split, reader, target_of):
        return [{"ids": p["readers"][reader]["ids"]["org"] + p["space"], "pos": p["pos"], "delta": x[i],
                 "target": target_of(p)} for i, p in enumerate(pairs) if p["split"] == split]  # fmt: skip

    for wi, w in enumerate(X.READERS):
        mine = [p for p in ident if p["in_pairs"][w]]
        xi = x_i[[i for i, p in enumerate(ident) if p["in_pairs"][w]]]
        tr = rows_of(mine, xi, "train", w, lambda p, w=w: p["readers"][w]["tok_b"])
        dv = rows_of(mine, xi, "select", w, lambda p, w=w: p["readers"][w]["tok_b"])
        for k in KS[w]:
            for shuf in (False, True):
                key = f"{'shuf' if shuf else 'R'}_{w}_k{k}"
                tlog: list[dict] = []
                mats[key], stops[key] = train_fit(model, layer, tr, dv, k, D.INIT_SEED + 100 * k + wi + (10 if shuf else 0),
                                                  steps, micro, (D.SHUFFLE_SEED + k + wi) if shuf else None, tlog,
                                                  f"L{layer} DAS {key} ({len(tr)} rows, dev {len(dv)})")  # fmt: skip
                log_rows += [
                    {"part": "identity", "R": key, "reader": w, "shuffled": shuf, "n_rows": len(tr), **r} for r in tlog
                ]
                X.write_jsonl(out / "train.jsonl", log_rows)
    tr = rows_of(addr, x_a, "train", LOOKUP, lambda p: p["readers"][LOOKUP]["tok_b"])
    dv = rows_of(addr, x_a, "select", LOOKUP, lambda p: p["readers"][LOOKUP]["tok_b"])
    for k in KS_POS:
        for shuf in (False, True):
            key = f"{'shuf' if shuf else 'R'}_pos_k{k}"
            tlog = []
            mats_a[key], stops[key] = train_fit(model, layer, tr, dv, k, Q.INIT_SEED + 100 * k + (10 if shuf else 0), steps,
                                                micro, (Q.SHUFFLE_SEED + k) if shuf else None, tlog,
                                                f"L{layer} DAS {key} ({len(tr)} rows, dev {len(dv)})")  # fmt: skip
            log_rows += [
                {"part": "address", "R": key, "reader": LOOKUP, "shuffled": shuf, "n_rows": len(tr), **r} for r in tlog
            ]
            X.write_jsonl(out / "train.jsonl", log_rows)
    for k in KS_POS:
        mats[f"R_pos_k{k}"] = mats_a[f"R_pos_k{k}"]  # the address subspace read on the identity pairs (cross)
    (out / "stops.json").write_text(json.dumps(stops, indent=1) + "\n")
    torch.save({"R": mats, "R_address": mats_a, "U": torch.tensor(u_np),
                "W": None if w_np is None else torch.tensor(w_np)}, out / "R.pt")  # fmt: skip
    print("trained", sorted(stops), flush=True)
    # 4. the geometry (the dictionaries built here, after training, and freed after: lesson (3))
    lens = JLens(model, "jpp")
    letters = model.letter_token_ids()
    with torch.no_grad():
        jdic = lens.vectors(layer, letters)
        wdic = D.we_dictionary(model, letters)
        u = torch.tensor(u_np, dtype=torch.float32, device=jdic.device)
        w_t = None if w_np is None else torch.tensor(w_np, dtype=torch.float32, device=jdic.device)
        q_w = None if w_t is None else R.orthonormal(w_t)
        tr_i = [i for i, p in enumerate(ident) if p["split"] == "train"]
        tr_a = [i for i, p in enumerate(addr) if p["split"] == "train"]
        ufit_i = D.fit_pointer(ho_i[tr_i].numpy(), [ident[i]["locker_index"] for i in tr_i])
        ufit_a = D.fit_pointer(ho_a[tr_a].numpy(), [addr[i]["slot_o"] for i in tr_a])
        uf_i = torch.tensor(ufit_i, dtype=torch.float32, device=jdic.device)
        uf_a = torch.tensor(ufit_a, dtype=torch.float32, device=jdic.device)
        geo_i = geometry_rows(ident, x_i.to(jdic.device), mats, jdic, wdic, u, uf_i, q_w, f"L{layer} identity geometry")
        geo_a = geometry_rows(addr, x_a.to(jdic.device), mats_a, jdic, wdic, u, uf_a, q_w, f"L{layer} address geometry")
        del jdic, wdic
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    X.write_jsonl(out / "geometry.jsonl", geo_i)
    X.write_jsonl(out / "address" / "geometry.jsonl", geo_a)
    cos2 = lambda a, b: round(float(R.mean_cos2(a, b) or 0.0), 6)  # noqa: E731
    ro: dict[str, Any] = {key: {"k": int(r.shape[1]), "cos2_U": cos2(r.to(u.device), u), "cos2_Ufit": cos2(r.to(u.device), uf_i),
                                "cos2_W": None if w_t is None else cos2(r.to(u.device), w_t),
                                "random_expectation_cos2_U": round(r.shape[1] / d, 6)} for key, r in mats.items()}  # fmt: skip
    ro["principal_angles_deg"] = {f"k{k}": D.principal_angles(mats[f"R_{LOOKUP}_k{k}"], mats[f"R_{RECALL}_k{k}"])
                                  for k in KS[LOOKUP] if k in KS[RECALL]}  # fmt: skip
    ro["d"], ro["rank_U"], ro["rank_Ufit"] = d, int(R.orthonormal(u).shape[1]), int(uf_i.shape[1])
    ro["rank_W"] = None if q_w is None else int(q_w.shape[1])
    ro["U_vs_Ufit_cos2"] = cos2(uf_i, u)
    (out / "readouts.json").write_text(json.dumps(ro, indent=2) + "\n")
    ro_a: dict[str, Any] = {key: pos_reads(r.to(u.device), u, w_t) for key, r in mats_a.items()}
    ro_a["d"], ro_a["rank_U"], ro_a["rank_W"] = (
        d,
        int(R.orthonormal(u).shape[1]),
        None if q_w is None else int(q_w.shape[1]),
    )
    ro_a["rank_Ufit"] = int(uf_a.shape[1])
    ro_a["U_vs_W"] = ({"cos2_U_in_W": cos2(w_t, u), "cos2_W_in_U": cos2(u, w_t), "angles": D.principal_angles(R.orthonormal(u), q_w)}
                      if w_t is not None else {"cos2_U_in_W": None, "cos2_W_in_U": None, "angles": None})  # fmt: skip
    ro_a["U_vs_Ufit_cos2"] = cos2(uf_a, u)
    (out / "address" / "readouts.json").write_text(json.dumps(ro_a, indent=2) + "\n")
    # 5. the reads (real forwards, X0's chat read, AddRows at L), the select and test pairs
    arms = identity_arms()
    x_dev = x_i.to(dev)
    parts = {key: ((x_dev @ r.to(dev)) @ r.to(dev).T).float() for key, r in mats.items()}
    rows: list[dict] = []
    with torch.no_grad():
        held = [(i, p) for i, p in enumerate(ident) if p["split"] != "train"]
        for i, p in progress(held, f"L{layer} identity reads (pair)", total=len(held)):
            adds = {"none": None, "whole": x_dev[i : i + 1], **{key: v[i : i + 1] for key, v in parts.items()}}
            edits: list[dict] = [{} if adds[a] is None else {layer: AddRows(adds[a], [p["pos"]])} for a in arms]
            for w, rd in p["readers"].items():
                logits: Any = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, p["space"], ws)[0]
                for j, a in enumerate(arms):
                    lg: Any = logits[j]
                    top = int(lg.argmax())
                    rows.append({"layer": layer, "scene": p["scene"], "source": p["source"], "entity": p["entity"],
                                 "split": p["split"], "reader": w, "in_pairs": p["in_pairs"][w], "arm": a,
                                 **X.read_row(lg, rd, digits), "right": int(top == rd["tok_A"]), "top_text": tok.decode([top])})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    del parts
    arms_a = Q.arm_names(KS_POS)
    xa_dev = x_a.to(dev)
    parts_a = {key: ((xa_dev @ r.to(dev)) @ r.to(dev).T).float() for key, r in mats_a.items()}
    rows_a: list[dict] = []
    with torch.no_grad():
        held_a = [(i, p) for i, p in enumerate(addr) if p["split"] != "train"]
        for i, p in progress(held_a, f"L{layer} address reads (pair)", total=len(held_a)):
            rows_a += Q.read_rows(
                model, layer, p, xa_dev[i], {key: v[i] for key, v in parts_a.items()}, arms_a, ws, digits
            )
    X.write_jsonl(out / "address" / "outcomes.jsonl", rows_a)
    m_a = {"exp": EXP, "run": name, "part": "address (49.8's file layout; the run's manifest is ../manifest.json)",
           "layer": layer, "ks": list(KS_POS), "k_rule": K_POS_RULE, "model": {"target": target},
           "switches": m["switches"], "routes_run": ROUTES_RUN[target], "U": u_info, "W": w_info}  # fmt: skip
    (out / "address" / "manifest.json").write_text(json.dumps(m_a, indent=2, ensure_ascii=False) + "\n")
    # 6. 48.1's routes read (rule (d)): R_lookup alone on x6_routes C2 scenes
    r_cases, r_info = D.routes_scenes(model, ws, digits, n_routes)
    split_of = {p["source_scene"]: p["split"] for p in ident if p["source"] in ("routes", "routes_topup")}
    X.write_jsonl(out / "routes_cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in r_cases])
    r_arms = ["none", "whole", *(f"R_{LOOKUP}_k{k}" for k in KS[LOOKUP]), *(f"rand_k{k}" for k in KS[LOOKUP])]
    r_rows = []
    with torch.no_grad():
        for c in progress(r_cases, "routes read (scene)"):
            ids = c["readers"][LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][c["pos"]].float().clone()
                 for v in ("org", "alt")}  # fmt: skip
            dx = (h["alt"] - h["org"])[None]
            edits = [{}] + [{layer: AddRows(dx if a == "whole" else ((dx @ mats[a].to(dx.device)) @ mats[a].to(dx.device).T),
                                            [c["pos"]])} for a in r_arms[1:]]  # fmt: skip
            twin = f"C0-{scene_index(c['scene']):04d}"
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                for a, lg in zip(r_arms, logits, strict=True):
                    top = int(lg.argmax())
                    r_rows.append({"layer": layer, "scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a,
                                   "route": R.classify(top, c) if w == LOOKUP else None, **X.read_row(lg, rd, digits),
                                   "c0_twin_split": split_of.get(twin), "top_text": tok.decode([top])})  # fmt: skip
    X.write_jsonl(out / "routes.jsonl", r_rows)
    m["routes"] = {"design": "48.1's: x6_routes C2 scenes, R_lookup alone at the bridge word at L; the lookup's answer "
                             "classified; c0_twin_split = the split of the same base scene's C0 identity pair, if pooled",
                   **r_info}  # fmt: skip
    m["stops"] = {k: {kk: v[kk] for kk in ("best_step", "best_dev_iia", "stopped_at", "micro", "oom_micro_tried")}
                  for k, v in stops.items()}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- numbers and rules (CPU) --------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed Q51.3 answer (x48_das.dan_answer: the 'Dan:' / 'Dan (27B):' lines and bullet continuations of
    the Q51.3 block at `rev`), '' if none."""
    return D.dan_answer(QUESTION, rev)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def identity_numbers(src: Path, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """The identity part's numbers in x48_das.layer_numbers' layout (so x48_das.rules reads them), with per-reader k
    sets: per reader the select own-IIA by k and the chosen k; on the test pairs own-IIA, random and shuffled by k,
    cross-IIA (the other reader's R at its chosen k), own minus cross (paired), the address subspace read by the reader
    (R_pos per k beside the random R of that k); the geometry per R on the test pairs; the routes read."""
    m = json.loads((src / "manifest.json").read_text())
    ks = {w: tuple(m["ks"][READER_NAME[w]]) for w in X.READERS}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    readouts = json.loads((src / "readouts.json").read_text())
    pairs = json.loads((src / "pairs.json").read_text())
    readers: dict[str, Any] = {}
    for w in X.READERS:
        _, ent_s, sw_s = D.reader_table(rows, w, "select")
        sel = {k: float(np.mean(sw_s[f"R_{w}_k{k}"])) for k in ks[w]}
        readers[w] = {"select": {"n": len(ent_s), "entities": len(set(ent_s)), "own_iia": {k: round(v, 4) for k, v in sel.items()},
                                 "S_whole": round(float(np.mean(sw_s["whole"])), 4)},
                      "k": D.chosen_k(sel, ks[w]), "ks": list(ks[w]),
                      "n_pairs": pairs["identity"]["per_reader"][READER_NAME[w]]}  # fmt: skip
    for w in X.READERS:
        other = RECALL if w == LOOKUP else LOOKUP
        scenes, ent, sw = D.reader_table(rows, w, "test")
        k_star, k_other = readers[w]["k"], readers[other]["k"]
        own = {k: D.ci_of(sw[f"R_{w}_k{k}"], ent, n_boot) for k in ks[w]}
        s_whole = float(np.mean(sw["whole"]))
        readers[w]["test"] = {
            "n": len(scenes), "entities": len(set(ent)), "scenes": scenes, "S_whole_rerun": round(s_whole, 4),
            "S_none": round(float(np.mean(sw["none"])), 4), "own_iia": own,
            "own_over_whole": {k: (own[k][0] / s_whole if s_whole > 0 else None) for k in ks[w]},
            "random_iia": {k: D.ci_of(sw[f"rand_k{k}"], ent, n_boot) for k in ks[w]},
            "shuffled_iia": {k: D.ci_of(sw[f"shuf_{w}_k{k}"], ent, n_boot) for k in ks[w]},
            "cross_iia": D.ci_of(sw[f"R_{other}_k{k_other}"], ent, n_boot), "cross_R": f"R_{other}_k{k_other}",
            "own_minus_cross": D.paired_ci(sw[f"R_{w}_k{k_star}"], sw[f"R_{other}_k{k_other}"], ent, n_boot),
            "own_at_k": own[k_star], "own_at_k64": own.get(64), "own_at_k128": own.get(128),
            "pos_cross": {k: D.ci_of(sw[f"R_pos_k{k}"], ent, n_boot) for k in KS_POS},
            "pos_random": {k: D.ci_of(sw[f"rand_k{k}"], ent, n_boot) for k in KS_POS},
            "by_source": {s: round(float(np.mean([r["switched"] for r in rows if r["reader"] == w and r["split"] == "test"
                                                  and r["in_pairs"] and r["arm"] == f"R_{w}_k{k_star}" and r["source"] == s])), 4)
                          for s in sorted({r["source"] for r in rows if r["reader"] == w and r["split"] == "test" and r["in_pairs"]})},
        }  # fmt: skip
    geo = [g for g in X.read_jsonl(src / "geometry.jsonl") if g["split"] == "test"]
    geometry: dict[str, Any] = {}
    for key in sorted({g["R"] for g in geo}):
        mine = [g for g in geo if g["R"] == key]
        geometry[key] = {"n": len(mine), "cos2_U": readouts[key]["cos2_U"], "cos2_Ufit": readouts[key]["cos2_Ufit"],
                         "cos2_W": readouts[key]["cos2_W"], "k_over_d": readouts[key]["random_expectation_cos2_U"]}  # fmt: skip
        for what in ("energy", "in_jpp25", "in_jpp100", "in_we25", "in_U", "in_Ufit", "in_W", "outside_union"):
            kept = [g for g in mine if g.get(what) is not None]
            vals = [g[what] for g in kept]
            geometry[key][what] = D.ci_of(vals, [g["entity"] for g in kept], n_boot)
            geometry[key][f"{what}_median"] = round(statistics.median(vals), 4) if vals else None
    routes = X.read_jsonl(src / "routes.jsonl")
    routes_out: dict[str, Any] = {}
    for a in sorted({r["arm"] for r in routes}):
        lk = [r for r in routes if r["arm"] == a and r["reader"] == LOOKUP]
        rc = [r for r in routes if r["arm"] == a and r["reader"] == RECALL]
        ent = [r["entity"] for r in lk]
        routes_out[a] = {"n": len(lk),
                         **{rt: D.ci_of([int(r["route"] == rt) for r in lk], ent, n_boot) for rt in Q.ROUTES_NAMES_ALL},
                         "identity_twin_not_train": round(float(np.mean([r["route"] == "identity" for r in lk
                                                                         if r.get("c0_twin_split") != "train"] or [math.nan])), 4),
                         "recall_switch": round(float(np.mean([r["switched"] for r in rc])), 4) if rc else None}  # fmt: skip
    return {"target": m["model"]["target"], "run": src.name, "layer": m["layer"], "ks": {READER_NAME[w]: list(k) for w, k in ks.items()},
            "d": readouts["d"], "rank_U": readouts["rank_U"], "rank_W": readouts.get("rank_W"), "readers": readers,
            "geometry": geometry, "routes": routes_out, "principal_angles_deg": readouts["principal_angles_deg"],
            "pairs": {k: v for k, v in pairs["identity"].items() if k != "scene_ids"},
            "topup": pairs.get("identity_topup")}  # fmt: skip


def rules_51(ident: dict[str, Any], addr: dict[str, Any]) -> dict[str, Any]:
    """The new rule and Q51.3's readouts (point estimates, EPS at the bars): no low-dimensional recall subspace (the
    recall's test own-IIA < 0.5 at k = 128 with >= 300 pairs; fewer pairs: not tested); (i) found = >= 300 pairs and
    own-IIA >= 0.5 at some k <= 128; (ii) the lookup subspace's shares (U, J++-25, W_E-25, outside) at its chosen k, the
    parts >= 0.5 named; (iii) U's energy in R_pos at k = 4 >= 0.6."""
    rc, lk = ident["readers"][RECALL], ident["readers"][LOOKUP]
    n_rc = rc["n_pairs"]
    tested = n_rc >= N_RULE
    own = {k: v[0] for k, v in rc["test"]["own_iia"].items()}
    at128 = own.get(K_RECALL_RULE)
    no_sub = tested and at128 is not None and at128 < NO_RECALL - EPS
    found = tested and any(v >= NO_RECALL - EPS for k, v in own.items() if k <= K_RECALL_RULE)
    g = ident["geometry"][f"R_{LOOKUP}_k{lk['k']}"]
    shares = {
        "U": g["in_U"][0],
        "J++-25": g["in_jpp25"][0],
        "W_E-25": g["in_we25"][0],
        "outside": g["outside_union"][0],
    }
    mostly = [p for p, v in shares.items() if v is not None and not math.isnan(v) and v >= MOSTLY - EPS]
    u_e = addr["geometry"][f"R_pos_k{K_POS_RULE}"]["cos2_U"]
    return {"no_recall_subspace": bool(no_sub), "recall_rule_tested": bool(tested), "recall_pairs": n_rc,
            "recall_own_iia_k128": at128, "recall_found_q51_3_i": bool(found),
            "lookup_k": lk["k"], "lookup_shares": shares, "lookup_mostly": mostly,
            "lookup_cos2_U": g["cos2_U"], "address_cos2_U_k4": u_e, "address_overlaps_U": bool(u_e >= U_OVERLAP - EPS),
            "address_cos2_W_k4": addr["geometry"][f"R_pos_k{K_POS_RULE}"]["cos2_W"]}  # fmt: skip


def model_verdict(src: Path, n_boot: int) -> dict[str, Any]:
    ident = identity_numbers(src, n_boot)
    addr = Q.numbers(src / "address", n_boot)
    v48 = D.rules(ident)
    v48["fallback_tested"] = ident["readers"][LOOKUP]["test"]["own_at_k64"] is not None
    v49 = Q.rules(addr)
    v51 = rules_51(ident, addr)
    return {"run": src.name, "target": ident["target"], "layer": ident["layer"], "identity": ident, "address": addr,
            "rules_48_1": v48, "rules_49_8": v49, "rules_51_3": v51}  # fmt: skip


def yes(b: bool) -> str:
    return "yes" if b else "no"


def verdict_lines(mv: dict[str, Any], answer: str) -> list[str]:
    ident, addr, v48, v49, v51 = mv["identity"], mv["address"], mv["rules_48_1"], mv["rules_49_8"], mv["rules_51_3"]
    fmt = D.fmt
    recall_label = ("**no low-dimensional recall subspace at this token and layer**" if v51["no_recall_subspace"]
                    else "a recall subspace at k <= 128" if v51["recall_found_q51_3_i"]
                    else f"not tested (recall pairs {v51['recall_pairs']} < {N_RULE})" if not v51["recall_rule_tested"]
                    else "neither")  # fmt: skip
    lines = [f"## {mv['target']} ({mv['run']}, L{mv['layer']})", "",
             f"- 51.3 rule: {recall_label} (recall pairs {v51['recall_pairs']}; test own-IIA at k = 128 "
             f"{fmt(ident['readers'][RECALL]['test']['own_at_k128'])}); Q51.3 (i) found: {yes(v51['recall_found_q51_3_i'])}",
             f"- 48.1: (a) {yes(v48['a'])}, (b) {yes(v48['b'])}, (c) {yes(v48['c'])}, (d) {yes(v48['d'])}; fallback (the lookup at "
             f"k = 64): {'not tested (51.3 trains the lookup at k = 4, 16 only)' if not v48['fallback_tested'] else yes(v48['fallback_no_low_dimensional_mediator'])}"
             + (f"; not selective (energy >= 0.8 of Delta): {', '.join(sorted(v48['not_selective']))}" if v48["not_selective"] else ""),
             f"- 49.8 (k = 4): {v49['text']} (own-IIA {v49['detail']['own_iia']:.2f}, U's energy in R_pos "
             f"{v49['detail']['U_energy_in_R']:.3f}, the recall's cross-IIA {v49['detail']['recall_cross_iia']:.2f})",
             f"- Q51.3 (ii) the lookup subspace (k = {v51['lookup_k']}): " + ", ".join(f"in {p} {v:.2f}" for p, v in v51["lookup_shares"].items())
             + f"; mostly: {', '.join(v51['lookup_mostly']) or 'no part >= 0.5'}; U's energy in R_lookup {v51['lookup_cos2_U']:.4f}",
             f"- Q51.3 (iii) the learned address overlaps U >= 0.6: {yes(v51['address_overlaps_U'])} ({v51['address_cos2_U_k4']:.3f}); "
             f"W's energy in R_pos (k = 4): {'-' if v51['address_cos2_W_k4'] is None else f'{v51['address_cos2_W_k4']:.3f}'}", "",
             f"Identity pairs {ident['pairs']['pairs']} scenes ({ident['pairs']['entities']} entities): per reader {ident['pairs']['per_reader']}, "
             f"per reader and source {ident['pairs']['per_reader_and_source']}, per reader and split {ident['pairs']['pairs_per_reader_and_split']}; "
             f"top-up {json.dumps(ident['topup'])}.", "",
             "| reader | k | select own-IIA | test own-IIA | random R | shuffled R | own / S_whole |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in X.READERS:
        r = ident["readers"][w]
        for k in r["ks"]:
            ow = r["test"]["own_over_whole"][k]
            lines.append(f"| {READER_NAME[w]} | {k}{' (chosen)' if k == r['k'] else ''} | {r['select']['own_iia'][k]:.2f} | "
                         f"{fmt(r['test']['own_iia'][k])} | {fmt(r['test']['random_iia'][k])} | {fmt(r['test']['shuffled_iia'][k])} | "
                         f"{'-' if ow is None else f'{ow:.2f}'} |")  # fmt: skip
    lines += ["", "Cross-IIA on the identity test pairs:", "",
              "| reader | test n (entities) | S_whole rerun | the other reader's R | own − cross (paired) | R_pos k=2 | k=4 | k=8 | random k=2 | k=4 | k=8 |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in X.READERS:
        t = ident["readers"][w]["test"]
        lines.append(f"| {READER_NAME[w]} | {t['n']} ({t['entities']}) | {t['S_whole_rerun']:.2f} | {fmt(t['cross_iia'])} ({t['cross_R']}) | "
                     f"{fmt(t['own_minus_cross'])} | " + " | ".join(fmt(t["pos_cross"][k]) for k in KS_POS) + " | "
                     + " | ".join(fmt(t["pos_random"][k]) for k in KS_POS) + " |")  # fmt: skip
    lines += ["", "Own-IIA at the chosen k by source (test pairs): "
              + "; ".join(f"{READER_NAME[w]} {ident['readers'][w]['test']['by_source']}" for w in X.READERS), "",
              "Geometry on the identity test pairs (means [CI]):", "",
              "| R | energy | in J++-25 | in J++-100 | in W_E-25 | in U | in U_fit | in W | outside (J++-25 ∪ U ∪ W_E-25) | cos² U (k/d) | cos² W |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, g in ident["geometry"].items():
        cw = "-" if g["cos2_W"] is None else f"{g['cos2_W']:.4f}"
        lines.append(f"| {key} | {fmt(g['energy'])} | {fmt(g['in_jpp25'])} | {fmt(g['in_jpp100'])} | {fmt(g['in_we25'])} | "
                     f"{fmt(g['in_U'])} | {fmt(g['in_Ufit'])} | {fmt(g['in_W'])} | {fmt(g['outside_union'])} | "
                     f"{g['cos2_U']:.4f} ({g['k_over_d']:.4f}) | {cw} |")  # fmt: skip
    lines += ["", "Principal angles R_lookup vs R_recall (degrees): " + "; ".join(
        f"{k}: {a}" for k, a in ident["principal_angles_deg"].items()), "",
              "Routes read (C2 scenes, the lookup's answer classified; the recall's switch beside):", "",
              "| arm | n | identity | position | value | original | other | identity (C0 twin not in train) | recall switch |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for a, r in ident["routes"].items():
        lines.append(f"| {a} | {r['n']} | {fmt(r['identity'])} | {fmt(r['position'])} | {fmt(r['value'])} | {fmt(r['original'])} | "
                     f"{fmt(r['other'])} | {r['identity_twin_not_train']} | {r['recall_switch']} |")  # fmt: skip
    t = addr["test"]
    lines += ["", f"Address pairs {addr['pairs']['pairs']} ({addr['pairs']['entities']} entities; per split {addr['pairs']['pairs_per_split']}; "
              f"moves {addr['pairs']['moves']}); test n = {t['n']}. The whole change rerun: position {t['S_whole_rerun']:.2f}; the recall "
              f"moved under it {fmt(t['recall_moved_whole'])}.", "",
              "| k | select own-IIA | test own-IIA | random R | shuffled R | own / whole | recall moved (R_pos) | recall (random R) | U's energy in R_pos | W's |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for k in addr["ks"]:
        ow = t["own_over_whole"][k]
        gk = addr["geometry"][f"R_pos_k{k}"]
        lines.append(f"| {k} | {addr['select']['own_iia'][k]:.2f} | {fmt(t['own_iia'][k])} | {fmt(t['random_iia'][k])} | "
                     f"{fmt(t['shuffled_iia'][k])} | {'-' if ow is None else f'{ow:.2f}'} | {fmt(t['recall_cross'][k])} | "
                     f"{fmt(t['recall_random'][k])} | {gk['cos2_U']:.3f} | {'-' if gk['cos2_W'] is None else f'{gk['cos2_W']:.3f}'} |")  # fmt: skip
    lines += [
        "",
        f"Rule detail: 48.1 {json.dumps(v48['detail'])}; 49.8 {json.dumps(v49['detail'])}; 51.3 {json.dumps(v51)}",
        "",
    ]
    return lines


def figure(mv: dict[str, Any], path: Path) -> None:
    """Own-IIA on the test pairs by k (the trained R, the random R, the shuffled R; 95% CIs) for the lookup, the recall
    and the address."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, percent_axis, style_axes

    ident, addr = mv["identity"], mv["address"]
    panels = [(READER_NAME[w], ident["readers"][w]["ks"], ident["readers"][w]["test"], ident["readers"][w]["test"]["S_whole_rerun"])
              for w in X.READERS] + [("address (position)", addr["ks"], addr["test"], addr["test"]["S_whole_rerun"])]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, (title, ks, t, whole) in zip(axes, panels, strict=True):
        xs = np.arange(len(ks))
        for off, (lab, key, col) in zip((-0.25, 0.0, 0.25), (("trained R", "own_iia", INK), ("random R", "random_iia", MUTED),
                                                              ("shuffled R", "shuffled_iia", "#b0aea4")), strict=True):  # fmt: skip
            vals = [t[key][k] for k in ks]
            ax.bar(xs + off, [v[0] for v in vals], 0.22, color=col, label=lab,
                   yerr=[[max(0.0, v[0] - v[1]) for v in vals], [max(0.0, v[2] - v[0]) for v in vals]], capsize=2)  # fmt: skip
        ax.axhline(whole, color=INK, ls="--", lw=0.8, label="whole change")
        ax.axhline(NO_RECALL, color=MUTED, ls=":", lw=0.8)
        ax.set_xticks(xs, [f"k = {k}" for k in ks])
        ax.set_ylim(0, 1)
        ax.set_title(f"{title}: test n = {t['n']}", fontsize=10)
        percent_axis(ax)
        style_axes(ax)
    axes[0].legend(fontsize=7, frameon=False)
    fig.suptitle(f"51.3 {mv['target']} L{mv['layer']}: own-IIA by k (95% CI over bridge entities)", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """51.3's verdict (sealed until Q51.3), or with coverage (batch 52, Lightning ports) the same rules on the coverage
    runs: no seal guard, "no prediction" in place of Dan's answer, each run's pool sources stated, x52_das51-<UTC>/."""
    if coverage:
        answer = f"{NO_PREDICTION}; rules first scored in {SCORED}"
        names = set(COVERAGE_RUNS.values())
        assert set(runs) <= names, f"51.3 coverage runs are {sorted(names)}, not {runs}"
    else:
        answer = unsealed()
    stem = "x52_das51" if coverage else "verdict"
    out = RESULTS / f"{stem}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    models = []
    lines = ["# 51.3: DAS at scale", "",
             f"Batch 51, test 51.3 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). 48.1's DAS (early stopping on dev IIA) "
             "on pooled identity pairs and 49.8's on routes position pairs; k chosen on the select split, every number read "
             f"on the test entities' pairs; cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"As computed: {AS_COMPUTED}.", ""]  # fmt: skip
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ") for ln in lines]
    for run in runs:
        mv = model_verdict(RESULTS / run, n_boot)
        models.append(mv)
        if coverage:
            m = json.loads((RESULTS / run / "manifest.json").read_text())
            lines += [*([f"**{m['adapted']}**", ""] if m.get("adapted") else []),
                      f"Coverage run {run}: identity pool sources {json.dumps(m['sources'])}; DAS forward: "
                      f"{m.get('mamba_kernel') or m.get('gdn_kernel') or 'as loaded'}.", ""]  # fmt: skip
        lines += verdict_lines(mv, answer)
        figure(mv, out / f"{run}.png")
        lines += [f"Figure: {run}.png", ""]
    lines += ["Rules (fixed in advance): 48.1 " + "; ".join(f"({k}) {t}" for k, t in D.RULE.items()) + ". 49.8 "
              + "; ".join(f"{Q.LABELS[k]}: {t}" for k, t in Q.RULE.items()) + f". 51.3: {RULE_NEW}."]  # fmt: skip
    (out / "verdict.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(src: Path, k_prompts: int = 5, k_rows: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify pack of one run: k_prompts random identity pairs and address pairs (seed 0) as the model reads them
    (the bridge token marked) and k_rows random rows per arm (seed 0) of each part's outcomes."""
    ident = X.read_jsonl(src / "cases.jsonl")
    addr = X.read_jsonl(src / "address" / "cases.jsonl")
    lines = [
        f"## {src.name}",
        "",
        f"### {min(k_prompts, len(ident))} random identity pairs of {len(ident)} (seed {seed})",
        "",
    ]
    for i in sorted(random.Random(seed).sample(range(len(ident)), min(k_prompts, len(ident)))):
        p = ident[i]
        lines += [f"#### {p['scene']} ({p['split']}): bridge {p['entity']} → {p['cf_bridge']}; in the pairs: "
                  f"lookup {p['in_pairs'][LOOKUP]}, recall {p['in_pairs'][RECALL]}", "", f"S's context: {p['cf_context']}", ""]  # fmt: skip
        for w, rd in p["readers"].items():
            lines += [
                f"**{READER_NAME[w]}**: O answers {rd['answer']}, S answers {rd['cf_answer']}",
                "",
                "```",
                rd["marked"],
                "```",
                "",
            ]
    lines += [f"### {min(k_prompts, len(addr))} random address pairs of {len(addr)} (seed {seed})", ""]
    for i in sorted(random.Random(seed).sample(range(len(addr)), min(k_prompts, len(addr)))):
        p = addr[i]
        lk = p["readers"][LOOKUP]
        lines += [f"#### {p['scene']} ({p['split']}): the {p['entity']}'s locker sentence moves from slot {p['slot_o']} to "
                  f"{p['slot_s']}; O answers {lk['answer']}, the position answer {lk['cf_answer']}", "",
                  "O (lookup), as read:", "", "```", lk["marked"]["org"], "```", "", "S:", "", "```", lk["marked"]["alt"], "```", ""]  # fmt: skip
    for part, path in (("identity", src / "outcomes.jsonl"), ("address", src / "address" / "outcomes.jsonl")):
        rows = X.read_jsonl(path)
        for a in dict.fromkeys(r["arm"] for r in rows):
            mine = [r for r in rows if r["arm"] == a]
            pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
            lines += [f"### {part}, arm {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                      "| scene | split | reader | in pairs | top token | switched | route |", "|---|---|---|---|---|---|---|"]  # fmt: skip
            for j in pick:
                r = mine[j]
                lines.append(f"| {r['scene']} | {r['split']} | {READER_NAME[r['reader']]} | {r.get('in_pairs', '-')} | "
                             f"{r['top_text']!r} | {r['switched']} | {r.get('route') or '-'} |")  # fmt: skip
            lines.append("")
    return lines


def stage_view(runs: list[str]) -> Path:
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.3 verify pack: prompts exactly as the model reads them (⟦bridge:…⟧ the bridge token where R R^T Delta "
             "is added at L) and random rows per arm. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        lines += view_lines(RESULTS / run)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_das/<name>/)")
    ap.add_argument("--out", type=Path, default=None, help="plan: write plan.md and <target>.json here")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict / view: the 51.3 runs")
    ap.add_argument("--why", default="batch 51, test 51.3 (jobs/c3/batch51.yaml; Q51.3)")
    ap.add_argument("--steps", type=int, default=D.STEPS)
    ap.add_argument("--micro", type=int, default=D.MICRO)
    ap.add_argument("--n-gen", type=int, default=N_TOPUP_GEN)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true",
                    help=f"verdict: batch 52 coverage runs (default {list(COVERAGE_RUNS.values())}; '{NO_PREDICTION}')")  # fmt: skip
    a = ap.parse_args()
    runs = a.runs or list((COVERAGE_RUNS if a.coverage else RUNS).values())
    if a.stage == "plan":
        stage_plan(a.out, a.n_gen)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, steps=a.steps, micro=a.micro, n_gen=a.n_gen)
    elif a.stage == "verdict":
        stage_verdict(runs, a.n_boot, a.coverage)
    else:
        stage_view(runs)


if __name__ == "__main__":
    main()
