"""x49_das_pos (batch 49, test 49.8; jobs/c3/batch49.yaml, design and rules fixed in advance; Q49.8 in
predictions/2026-10-28_dan.md): DAS for the address. Does a learned low-dimensional subspace of the change at the bridge
word carry the locker sentence's position, and is it the hand-built address U?

48.1's DAS (scripts/x48_das.py: its orthonormal R, the edit h <- h_O + R R^T (h_S - h_O) at the bridge token at L, its
training loop, the random and shuffled-target baselines, the energy reads, BJ_DAS_GDN=torch) on routes position
counterfactuals: x6_routes' C1 scenes (three lockers first, then three picks; same item in O and S, its locker sentence
moved to another slot, swapped with the sentence there, and given a new number in S). The counterfactual answer is the
position route's: O's locker digit at the slot the bridge's sentence occupies in S (x6_routes' expect["position"]); S's
own answer (the new digit) is not the target.

As computed (fixed before any run; Dan may override before the enqueue):
Pairs: the stored routes run of the target (x6_routes, chat, L, seed 2510; the 9B: qwen35_9b_x6_routes), its C1 scenes
read under the whole change (the first 300 eligible: both readers say and read O's and S's answers right), restricted to
those whose stored whole change sent the lookup to the position answer (as 48.1 restricts to the switched pairs; the
other routes counted in pairs.json). The scenes are rebuilt with the tokenizer and asserted equal to the stored ids.
Split by bridge entity 60 / 20 / 20 (train / select / test), seed 0 (x48_das.split_entities).
R_pos (one reader, the lookup) for k in {2, 4, 8}: Adam lr 1e-3, 300 steps, batch 16 (micro-batches of 8), cross-entropy
of the position answer's token at X0's chat read (the appended space) of the O prompt; one untrained random R per k and
one R trained on shuffled targets per k. Reads on the select and test pairs, both readers, arms none / whole / R_pos /
random / shuffled per k: own-IIA = the lookup's top token is the position answer; the lookup's route (identity /
position / value / other); the recall's move = its top token is not O's answer (the item is the same, so the recall
should not move: its cross read). Geometry per pair and R (x48_das.geometry_row): energy ||R R^T Delta||^2 /
||Delta||^2; the share of R R^T Delta inside the pair's 25 / 100 signed-OMP J++ atoms at L, its 25 W_E atoms, U, W, U_fit
and outside the union (J++-25, U, W_E-25). Per R: U's energy inside R = ||R^T U||_F^2 / rank U (x6_routes.mean_cos2;
random k / d), W's the same; principal angles R_pos vs U, R_pos vs W, U vs W.
U: x0_massmean.subspaces' Alf on the target's probe run (x48_das.pointer_basis; 4-d, first vs rest), not refit.
W: 47.2's slot subspace (x47_six: the layout-free mass-mean of the bridge-word states by slot on the six-locker fit half,
rank 5), loaded from the target's 47.2 run (fit.npz "W"), not refit. U_fit (descriptive): x48_das.fit_pointer on the
train pairs' h_O by the bridge's O slot (rank 2).
Rules at k = 4 on the test pairs' point estimates (EPS at the bars; cluster-bootstrap CIs over bridge entities, 10,000,
seed 0, beside): "ours" if U's energy in R_pos >= 0.6, own-IIA >= 0.6 and the recall's cross-IIA <= 0.1; "two address
codes" if own-IIA >= 0.6 and U's energy <= 0.2 (then W's energy in R_pos and the angles U vs W, U vs R_pos, W vs R_pos are
the report); "no low-dimensional mediator" if own-IIA < 0.6; else "in between" (Q49.8 (a)-(d)).

SEALED: the run writes no verdict; `verdict` (CPU) refuses until predictions/2026-10-28_dan.md holds Dan's Q49.8 answer
at the committed HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x49_das_pos.py plan --out results/x49_das_pos/plan-<UTC>    # CPU, tokenizer
BJ_TARGET=qwen3.5-9b BJ_DAS_GDN=torch uv run python scripts/x49_das_pos.py run --name qwen35_9b_x49_das_pos   # GPU
uv run python scripts/x49_das_pos.py verdict --runs qwen35_9b_x49_das_pos                 # CPU, after Dan's Q49.8
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
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

EXP = "x49_das_pos"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch49.yaml"
PREDICTIONS = D.PREDICTIONS
QUESTION = "Q49.8"
ROUTES_RUN = {"qwen3.5-9b": "qwen35_9b_x6_routes"}  # the stored routes run (C1 scenes, the whole change's routes)
W_RUN = {"qwen3.5-9b": "qwen35_9b_x47_2"}  # 47.2's run on the target: fit.npz holds W
RUNS = {"qwen3.5-9b": "qwen35_9b_x49_das_pos"}
CONDITION = "C1"  # x6_routes: same bridge, its locker sentence swapped with another slot's, a new number in S
RENDERING = "chat"
KS, K_RULE = (2, 4, 8), 4
SPLIT_SEED, INIT_SEED, SHUFFLE_SEED, RAND_SEED = 0, 49, 4981, 4982  # batches: x48_das.BATCH_SEED + the R's seed
OWN_IIA, U_OURS, U_TWO, RECALL_CROSS = 0.6, 0.6, 0.2, 0.1
NOT_SELECTIVE = D.NOT_SELECTIVE
EPS = 1e-9  # a value exactly at a bar counts as at the bar
LOCKER = re.compile(r"The locker of the (\w+) is (\d)\.")
ROUTES_NAMES_ALL = ("identity", "position", "value", "original", "other")  # x6_routes.classify
LABELS = {
    "ours": "(a) the learned address is ours",
    "two_codes": "(b) two address codes",
    "no_mediator": "(c) no low-dimensional mediator",
    "in_between": "(d) in between",
}
RULE = {
    "ours": "at k = 4, >= 0.6 of U's energy lies in R_pos (random k/d ~ 0.001), own-IIA >= 0.6 and the recall's "
            "cross-IIA <= 0.1",
    "two_codes": "own-IIA >= 0.6 but U's energy in R_pos <= 0.2; then report which one the writes used (47.2's "
                 "slot-specific result: W) and the angle between them",
    "no_mediator": "own-IIA < 0.6",
    "in_between": "none of the above",
}  # fmt: skip
AS_COMPUTED = (
    "every rule at k = 4 on the test entities' pairs: own-IIA = the share of test pairs whose lookup top token under "
    "R_pos is the position answer (O's locker digit at the slot the bridge's sentence occupies in S); U's energy in "
    "R_pos = ||R_pos^T U||_F^2 / rank U (x6_routes.mean_cos2; a random R: k / d); the recall's cross-IIA = the share of "
    "test pairs whose recall top token under R_pos is not O's answer (the item is the same in O and S, so any move is "
    "collateral); point estimates at the bars (EPS 1e-9), cluster-bootstrap CIs over bridge entities (10,000, seed 0) "
    "beside them; exactly one label holds: ours, else two codes, else no mediator (own-IIA < 0.6), else in between; "
    "own-IIA / the whole change's rerun position share beside; the select split reported, not used to choose k"
)


# ---- pairs (tokenizer only) ---------------------------------------------------------------------------------------


def lockers(context: str) -> list[tuple[str, int]]:
    """The locker sentences of a routes context in order: (item, digit) per slot."""
    return [(x, int(d)) for x, d in LOCKER.findall(context)]


def marked(tok, ids: list[int], pos: int, space: list[int], marks: dict[str, str]) -> str:
    """The prompt as the model reads it (the read's space token appended) with the bridge token in ⟦bridge:…⟧ and
    each sentence of `marks` ({label: sentence}) in ⟦label:…⟧."""
    text = (tok.decode(ids[:pos]) + "⟦bridge:" + tok.decode(ids[pos : pos + 1]) + "⟧"
            + tok.decode(ids[pos + 1 :] + space))  # fmt: skip
    for label, s in marks.items():
        assert text.count(s) == 1, f"{s!r} is not once in the decoded prompt"
        text = text.replace(s, f"⟦{label}:{s}⟧", 1)
    return text


def position_pair(tok, c: dict) -> dict:
    """An x6_routes C1 case as a 49.8 pair: the same bridge item in O and S, its locker sentence at slot i in O and at
    slot j != i in S; the counterfactual answer = O's locker digit at slot j (the position route); S's own answer (the
    new digit) kept beside. The lookup's tok_b is the position answer's token (X.read_row's switch = own-IIA); the
    recall's is O's answer (it cannot switch: a move is collateral)."""
    assert c["condition"] == CONDITION, f"{c['scene']}: not a same-item move ({c['condition']})"
    assert c["bridge"] == c["cf_bridge"], f"{c['scene']}: not a same-item move (the bridge changes)"
    lo, ls = lockers(c["context"]), lockers(c["cf_context"])
    items_o, items_s = [x for x, _ in lo], [x for x, _ in ls]
    assert sorted(items_o) == sorted(items_s), f"{c['scene']}: the items differ"
    assert len(set(items_o)) == len(items_o), f"{c['scene']}: an item twice"
    b = c["bridge"]
    i, j = items_o.index(b) + 1, items_s.index(b) + 1
    assert i != j, f"{c['scene']}: the bridge's locker sentence did not move"
    target = lo[j - 1][1]
    exp = c["expect"]
    assert target == exp["position"], f"{c['scene']}: the position answer is not O's digit at slot {j}"
    assert lo[i - 1][1] == exp["original"], f"{c['scene']}: O's answer"
    assert ls[j - 1][1] == exp["value"], f"{c['scene']}: S's answer"
    lk, rc = c["readers"][X.LOOKUP], c["readers"][X.RECALL]
    assert rc["tok_A"] == rc["tok_b"], f"{c['scene']}: the recall's answers differ for one item"
    pos_tok = c["route_tokens"]["position"]
    assert pos_tok not in (lk["tok_A"], lk["tok_b"]), f"{c['scene']}: the position answer is O's or S's answer"
    sent = lambda ctx, slot: re.split(r"(?<=\.) ", ctx)[slot - 1]  # noqa: E731
    readers = {
        X.LOOKUP: {**lk, "s_answer": lk["cf_answer"], "tok_s": lk["tok_b"], "cf_answer": str(target), "tok_b": pos_tok},
        X.RECALL: dict(rc),
    }
    for rd in readers.values():
        rd["marked"] = {
            "org": marked(tok, rd["ids"]["org"], c["pos"], c["space"],
                          {"own": sent(c["context"], i), "target": sent(c["context"], j)}),
            "alt": marked(tok, rd["ids"]["alt"], c["pos"], c["space"], {"moved": sent(c["cf_context"], j)}),
        }  # fmt: skip
    return {"scene": c["scene"], "entity": b, "cf_bridge": c["cf_bridge"], "domain": c["domain"],
            "condition": c["condition"], "pos": c["pos"], "space": c["space"], "context": c["context"],
            "cf_context": c["cf_context"], "slot_o": i, "slot_s": j, "move": f"{i}->{j}", "lockers_o": lo,
            "expect": exp, "route_tokens": c["route_tokens"], "readers": readers}  # fmt: skip


def select_pairs(tok, routes_run: str, layer: int) -> tuple[list[dict], dict]:
    """The 49.8 pairs in the stored routes run's read order: its C1 scenes read under the whole change (the eligible
    ones), those whose stored whole change sent the lookup to the position answer; rebuilt with the tokenizer (ids and
    the bridge index asserted equal to the stored ones); split by bridge entity. Counts beside."""
    from scripts import x6_routes as R

    src = R.RESULTS / routes_run
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == pins.TARGET, f"{routes_run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    assert m["layer"] == layer, f"{routes_run}: layer {m['layer']}, not {layer}"
    assert m["seed"] == R.SEED, f"{routes_run}: scene seed {m['seed']}, not {R.SEED}"
    assert m["model"].get("prompt_format", RENDERING) == RENDERING, f"{routes_run} is not a chat run"
    stored = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["condition"] == CONDITION}
    whole: dict[str, dict[str, dict]] = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["condition"] == CONDITION and r["arm"] == "whole":
            whole.setdefault(r["scene"], {})[r["reader"]] = r
    assert whole, f"{routes_run}: no {CONDITION} whole-change reads"
    rebuilt = {c["scene"]: c for c in R.scenes(tok, R.N_GEN, rendering=RENDERING)[0] if c["condition"] == CONDITION}
    pool, counts = [], collections.Counter()
    for scene, rows in whole.items():
        c, old = rebuilt[scene], stored[scene]
        assert c["pos"] == old["pos"], f"{scene}: the bridge position moved since {routes_run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {routes_run}"
        route = rows[X.LOOKUP]["route"]
        counts[route] += 1
        if route != "position":
            continue
        p = position_pair(tok, c)
        p["stored_route"] = route
        p["stored_recall_kept"] = int(rows[X.RECALL]["top"] == c["readers"][X.RECALL]["tok_A"])
        pool.append(p)
    info = split_info(pool)
    info = {"routes_run": routes_run, "layer": layer, "condition": CONDITION, "scenes_read": len(whole),
            "whole_change_routes": dict(counts), "kept": "the lookup's stored whole-change route is position", **info}  # fmt: skip
    return pool, info


def split_info(pool: list[dict]) -> dict:
    """Splits the pool by bridge entity (x48_das.split_entities, SPLIT_SEED) in place; the counts."""
    if not pool:
        return {"pairs": 0}
    split = D.split_entities([p["entity"] for p in pool], seed=SPLIT_SEED)
    for p in pool:
        p["split"] = split[p["entity"]]
    return {"pairs": len(pool), "entities": len(split), "split_seed": SPLIT_SEED,
            "entities_per_split": dict(collections.Counter(split.values())),
            "pairs_per_split": dict(collections.Counter(p["split"] for p in pool)),
            "moves": dict(sorted(collections.Counter(p["move"] for p in pool).items())),
            "slot_o_train": dict(sorted(collections.Counter(p["slot_o"] for p in pool if p["split"] == "train").items())),
            "stored_recall_kept": round(float(np.mean([p["stored_recall_kept"] for p in pool])), 4)
            if "stored_recall_kept" in pool[0] else None,
            "scene_ids": {s: [p["scene"] for p in pool if p["split"] == s] for s in ("train", "select", "test")}}  # fmt: skip


def load_w(target: str, layer: int) -> tuple[np.ndarray, dict]:
    """W: 47.2's slot subspace on the target (x47_six's fit on the six-locker fit half, fit.npz "W", [d, slots - 1]),
    not refit; its run's layer must be this test's."""
    from scripts import x47_six as SIX

    src = SIX.RESULTS / W_RUN[target]
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name}: not a {target} run"
    assert m["layer"] == layer, f"{src.name}: layer {m['layer']}, not {layer}"
    w = np.load(src / "fit.npz")["W"].astype(np.float64)
    assert np.allclose(w.T @ w, np.eye(w.shape[1]), atol=1e-5), f"{src.name}: W's columns are not orthonormal"
    rel = str((src / "fit.npz").relative_to(pins.REPO_ROOT))
    return w, {"run": src.name, "slots": m.get("slots"), "rank": int(w.shape[1]), "file": rel,
               "sha256": X.sha256_of(src / "fit.npz")}  # fmt: skip


def plan_lines(blob: dict) -> list[str]:
    i = blob["pairs"]
    lines = ["# 49.8 plan (CPU, the real tokenizer): DAS for the address, the routes position pairs", "",
             f"Written by `scripts/x49_das_pos.py plan` before any run. Target {blob['target']} at L{blob['layer']}; "
             f"pairs from {i['routes_run']} ({CONDITION}: the bridge's locker sentence moved to another slot, a new "
             "number in S). UNVERIFIED.", "",
             f"- {CONDITION} scenes read under the whole change (eligible): {i['scenes_read']}; the lookup's stored "
             f"whole-change routes: {i['whole_change_routes']}",
             f"- kept ({i['kept']}): {i['pairs']} pairs, {i['entities']} bridge entities; entities per split "
             f"{i['entities_per_split']}; pairs per split {i['pairs_per_split']}",
             f"- moves (O slot -> S slot): {i['moves']}; the bridge's O slot in train (U_fit's classes): {i['slot_o_train']}",
             f"- the recall kept O's answer under the stored whole change: {i['stored_recall_kept']}",
             f"- prompt tokens {blob['prompt_tokens']}; bridge token index {blob['bridge_token_index']}",
             f"- U: {blob['U']}", f"- W: {blob['W']}", "",
             f"## {len(blob['rendered'])} random pairs (seed {X.EXAMPLES_SEED}): O and S as the model reads them", "",
             "⟦bridge:…⟧ the bridge token where R R^T Delta is added; in O ⟦own:…⟧ the bridge's locker sentence and "
             "⟦target:…⟧ the sentence at the slot it moves to in S (its digit is the counterfactual answer); in S "
             "⟦moved:…⟧ the bridge's sentence at its new slot.", ""]  # fmt: skip
    for e in blob["rendered"]:
        lk, rc = e["readers"][X.LOOKUP], e["readers"][X.RECALL]
        lines += [f"### {e['scene']} ({e['split']}): the {e['entity']}'s locker sentence moves from slot {e['slot_o']} "
                  f"to slot {e['slot_s']}", "",
                  f"Lookup ({lk['question']}): O answers {lk['answer']}, S answers {lk['s_answer']} (the new digit), "
                  f"the counterfactual (position) answer {lk['cf_answer']}. Recall ({rc['question']}): {rc['answer']} in "
                  "both.", "", "O (lookup), as read:", "", "```", lk["marked"]["org"], "```", "", "S (lookup, the source):",
                  "", "```", lk["marked"]["alt"], "```", ""]  # fmt: skip
    return lines


def stage_plan(out: Path | None = None) -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    pairs, info = select_pairs(tok, ROUTES_RUN[pins.TARGET], layer)
    blob: dict[str, Any] = {"target": pins.TARGET, "layer": layer, "prefix": pins.RUN_PREFIX, "run_name": RUNS.get(pins.TARGET),
                            "pairs": {k: v for k, v in info.items() if k != "scene_ids"}}  # fmt: skip
    lengths = [len(p["readers"][X.LOOKUP]["ids"]["org"]) for p in pairs]
    blob["prompt_tokens"] = [min(lengths), max(lengths)] if lengths else None
    blob["bridge_token_index"] = sorted({p["pos"] for p in pairs})
    try:
        _, u = D.pointer_basis(pins.TARGET)
        blob["U"] = {"states_run": u["states_run"], "rank": u["rank"]}
    except FileNotFoundError as e:
        blob["U"] = f"probe run not here: {e}"
    try:
        blob["W"] = load_w(pins.TARGET, layer)[1]
    except (FileNotFoundError, KeyError) as e:
        blob["W"] = f"47.2 run not here: {e}"
    pick = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(pairs)), min(5, len(pairs))))
    blob["rendered"] = [{k: pairs[i][k] for k in ("scene", "split", "entity", "slot_o", "slot_s", "expect")}
                        | {"readers": {w: {k: rd[k] for k in ("question", "answer", "s_answer", "cf_answer", "marked")
                                           if k in rd} for w, rd in pairs[i]["readers"].items()}} for i in pick]  # fmt: skip
    print(json.dumps({k: v for k, v in blob.items() if k != "rendered"}, indent=1, ensure_ascii=False))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{pins.TARGET}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
        (out / "plan.md").write_text("\n".join(plan_lines(blob)) + "\n")
        print("wrote", out)
    return blob


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def arm_names(ks: tuple[int, ...] = KS) -> list[str]:
    """Every evaluated arm, in order: none, whole, then per k R_pos, the random R, the shuffled-target R."""
    out = ["none", "whole"]
    for k in ks:
        out += [f"R_pos_k{k}", f"rand_k{k}", f"shuf_pos_k{k}"]
    return out


def subspace_reads(r_mat, u, w) -> dict[str, Any]:
    """One R's subspace reads: U's and W's energy inside R (||R^T B||_F^2 / rank B, x6_routes.mean_cos2), k / d, and the
    principal angles (degrees) R vs U and R vs W."""
    from scripts import x6_routes as R

    k, d = int(r_mat.shape[1]), int(r_mat.shape[0])
    qu, qw = R.orthonormal(u), R.orthonormal(w)
    return {"k": k, "cos2_U": round(float(R.mean_cos2(r_mat, qu) or 0.0), 6), "cos2_W": round(float(R.mean_cos2(r_mat, qw) or 0.0), 6),
            "random_expectation": round(k / d, 6), "angles_vs_U": D.principal_angles(r_mat.double(), qu),
            "angles_vs_W": D.principal_angles(r_mat.double(), qw)}  # fmt: skip


def read_rows(model, layer: int, it: dict, x, parts: dict, arms: list[str], ws, digits) -> list[dict]:
    """Every arm on one held-out pair, both readers (X0's chat read with the AddRows edit at the bridge token): the
    lookup's switch (= the position answer) and route, the recall's move (its top token is not O's answer)."""
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    adds = {"none": None, "whole": x[None], **{key: v[None] for key, v in parts.items()}}
    edits: list[dict] = [{} if adds[a] is None else {layer: AddRows(adds[a], [it["pos"]])} for a in arms]
    rows = []
    for w, rd in it["readers"].items():
        logits: Any = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], ws)[0]
        assert len(logits) == len(arms)
        for j, a in enumerate(arms):
            lg: Any = logits[j]
            top = int(lg.argmax())
            rows.append({"layer": layer, "scene": it["scene"], "entity": it["entity"], "split": it["split"], "reader": w,
                         "arm": a, "move": it["move"], **X.read_row(lg, rd, digits),
                         "route": R.classify(top, it) if w == X.LOOKUP else None, "moved": int(top != rd["tok_A"]),
                         "top_text": model.tokenizer.decode([top])})  # fmt: skip
    return rows


def stage_run(name: str, why: str, steps: int = D.STEPS, ks: tuple[int, ...] = KS) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x6_routes as R
    from scripts.x0_parts import omp_atoms

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.8 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in ROUTES_RUN, f"49.8 runs on {sorted(ROUTES_RUN)}, not {target}"
    assert target in W_RUN, f"no 47.2 run (W) for {target}"
    assert K_RULE in ks, f"the rule reads k = {K_RULE}; ks {ks}"
    layer, routes_run = X.PREDICTED[target], ROUTES_RUN[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = R.RESULTS / routes_run
    u_np, u_info = D.pointer_basis(target)
    w_np, w_info = load_w(target, layer)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
         "test": "49.8", "spec": "jobs/c3/batch49.yaml (49.8)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in
                    (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")},
         "routes_run": routes_run, "condition": CONDITION, "layer": layer, "ks": list(ks), "k_rule": K_RULE,
         "training": {"loss": "cross-entropy of the position answer's token (O's locker digit at the slot the bridge's "
                              "sentence occupies in S) at the read position (the appended space) of the O prompt under "
                              "h_O + R R^T (h_S - h_O) at the bridge token at L; x48_das.train_subspace",
                      "optimizer": "Adam", "lr": D.LR, "steps": steps, "batch": D.BATCH, "micro_batch": D.MICRO,
                      "batching": f"each step {D.BATCH} training rows drawn without replacement (seed {D.BATCH_SEED} + the R's seed)",
                      "parametrization": "torch.nn.utils.parametrizations.orthogonal on Linear(k, d).weight [d, k]",
                      "init_seed": f"{INIT_SEED} + 100 * k (shuffled: + 10)",
                      "shuffled_targets": f"the training rows' targets permuted once, seed {SHUFFLE_SEED} + k",
                      "random_R": f"QR of a seeded Gaussian, seed {RAND_SEED} + k"},
         "pairs": f"{routes_run}'s {CONDITION} scenes read under the whole change, those whose stored whole change sent "
                  "the lookup to the position answer; split by bridge entity 60 / 20 / 20 (train / select / test), seed "
                  f"{SPLIT_SEED}",
         "read": "X0's chat read (a digit's space token appended, the top token); the lookup's switch = the position "
                 "answer (own-IIA); the recall's move = its top token is not O's answer (cross read)",
         "geometry": "per pair and R (x48_das.geometry_row): energy; the share of R R^T Delta inside the pair's 25 / 100 "
                     "signed-OMP J++ atoms, its 25 W_E atoms, U, W, U_fit, and outside the union (J++-25, U, W_E-25); per "
                     "R: ||R^T U||_F^2 / rank U, the same for W, principal angles vs U and W; U vs W",
         "U": u_info, "W": w_info, "arms": arm_names(ks), "rule": RULE, "as_computed": AS_COMPUTED,
         "seeds": {"split": SPLIT_SEED, "init": INIT_SEED, "shuffle": SHUFFLE_SEED, "random_R": RAND_SEED,
                   "batches": D.BATCH_SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "routes_scenes": R.SEED},
         "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    if (patched := D.torch_gdn(model.hf)) is not None:
        m["gdn_kernel"] = f"torch reference ({D.GDN_ENV}=torch; {patched}.torch_chunk_gated_delta_rule replaced)"
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    for p in model.hf.parameters():  # the DAS gradient reaches R only
        p.requires_grad_(False)
    tok = model.tokenizer
    pairs, info = select_pairs(tok, routes_run, layer)
    (out / "pairs.json").write_text(json.dumps(info, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", pairs)
    print(json.dumps({k: v for k, v in info.items() if k != "scene_ids"}), flush=True)
    for s in ("train", "select", "test"):
        assert info.get("pairs_per_split", {}).get(s, 0) > 0, f"no {s} pairs"
    dev = model.device
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    letters = model.letter_token_ids()
    lens = JLens(model, "jpp")
    jdic = lens.vectors(layer, letters)
    wdic = D.we_dictionary(model, letters)
    # 1. the states at the bridge token, cached (the readers' prompts are the same through it: x6_routes.encode)
    h_o, h_s = [], []
    with torch.no_grad():
        for it in progress(pairs, f"states at L{layer} (pair)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][it["pos"]].float().cpu()
                 for v in ("org", "alt")}  # fmt: skip
            h_o.append(h["org"])
            h_s.append(h["alt"])
    h_o_t, h_s_t = torch.stack(h_o), torch.stack(h_s)
    delta = h_s_t - h_o_t
    torch.save({"scenes": [it["scene"] for it in pairs], "h_O": h_o_t, "h_S": h_s_t, "delta": delta, "layer": layer,
                "pos": [it["pos"] for it in pairs]}, out / f"states_L{layer}.pt")  # fmt: skip
    d = delta.shape[1]
    train_idx = [i for i, it in enumerate(pairs) if it["split"] == "train"]
    u_fit_np = D.fit_pointer(h_o_t[train_idx].numpy(), [pairs[i]["slot_o"] for i in train_idx])
    # 2. training: R_pos per k, its shuffled-target twin, a random R
    rows = [{"ids": pairs[i]["readers"][X.LOOKUP]["ids"]["org"] + pairs[i]["space"], "pos": pairs[i]["pos"],
             "delta": delta[i], "target": pairs[i]["readers"][X.LOOKUP]["tok_b"]} for i in train_idx]  # fmt: skip
    mats: dict[str, Any] = {}
    log_rows: list[dict] = []
    for k in ks:
        mats[f"rand_k{k}"] = D.random_basis(d, k, RAND_SEED + k)
        for shuf in (False, True):
            key = f"{'shuf' if shuf else 'R'}_pos_k{k}"
            tlog: list[dict] = []
            mats[key] = D.train_subspace(model, layer, rows, k, INIT_SEED + 100 * k + (10 if shuf else 0), steps=steps,
                                         shuffle=(SHUFFLE_SEED + k) if shuf else None, log=tlog,
                                         desc=f"L{layer} DAS {key} ({len(rows)} rows)")  # fmt: skip
            log_rows += [{"layer": layer, "R": key, "shuffled": shuf, "n_rows": len(rows), **r} for r in tlog]
            X.write_jsonl(out / "train.jsonl", log_rows)
    print("trained", sorted(mats), flush=True)
    # 3. the geometry per pair and R
    x = delta.to(jdic.device)
    u = torch.tensor(u_np, dtype=torch.float32, device=x.device)
    w_t = torch.tensor(w_np, dtype=torch.float32, device=x.device)
    u_fit = torch.tensor(u_fit_np, dtype=torch.float32, device=x.device)
    atoms_j = omp_atoms(jdic, x, max(D.K_JPP)).cpu()
    atoms_w = omp_atoms(wdic, x, X.K_MAIN).cpu()
    q_w = R.orthonormal(w_t)
    geo = []
    for i, it in enumerate(progress(pairs, f"L{layer} geometry (pair)")):
        spans = {**D.spans_of(jdic, wdic, u, u_fit, atoms_j[i], atoms_w[i]), "W": q_w}
        for key, r_mat in mats.items():
            geo.append({"layer": layer, "scene": it["scene"], "entity": it["entity"], "split": it["split"], "R": key,
                        "norm": round(float(x[i].norm()), 4), **D.geometry_row(x[i], r_mat.to(x.device), spans)})  # fmt: skip
    X.write_jsonl(out / "geometry.jsonl", geo)
    readouts: dict[str, Any] = {key: subspace_reads(r_mat.to(x.device), u, w_t) for key, r_mat in mats.items()}
    readouts["d"], readouts["rank_U"], readouts["rank_W"] = d, int(R.orthonormal(u).shape[1]), int(q_w.shape[1])
    readouts["rank_Ufit"] = int(u_fit.shape[1])
    readouts["U_vs_W"] = {"cos2_U_in_W": round(float(R.mean_cos2(w_t, u) or 0.0), 6),
                          "cos2_W_in_U": round(float(R.mean_cos2(u, w_t) or 0.0), 6),
                          "angles": D.principal_angles(R.orthonormal(u), q_w)}  # fmt: skip
    readouts["U_vs_Ufit_cos2"] = round(float(R.mean_cos2(u_fit, u) or 0.0), 6)
    torch.save({"R": mats, "U": torch.tensor(u_np), "W": torch.tensor(w_np), "U_fit": torch.tensor(u_fit_np)},
               out / "R.pt")  # fmt: skip
    (out / "readouts.json").write_text(json.dumps(readouts, indent=2) + "\n")
    # 4. the reads: every arm on the select and test pairs, both readers
    arms = arm_names(ks)
    parts = {key: ((x @ r_mat.to(x.device)) @ r_mat.to(x.device).T).float() for key, r_mat in mats.items()}
    out_rows: list[dict] = []
    with torch.no_grad():
        held = [(i, it) for i, it in enumerate(pairs) if it["split"] != "train"]
        for i, it in progress(held, f"L{layer} reads (pair)", total=len(held)):
            out_rows += read_rows(model, layer, it, x[i], {key: v[i] for key, v in parts.items()}, arms, ws, digits)
    X.write_jsonl(out / "outcomes.jsonl", out_rows)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed Q49.8 answer (x48_das.dan_answer: x47_chain's regex, per-model 'Dan (...):' lines and bullet
    lines), '' if none."""
    return D.dan_answer(QUESTION, rev)


def split_table(rows: list[dict], split: str) -> tuple[list[str], list[str], dict[str, dict[str, dict[str, list]]]]:
    """A split's pairs (row order), their entities, and per reader and arm the per-pair reads (switched, moved,
    route); every pair must have every arm for both readers."""
    by: dict[tuple[str, str, str], dict] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["split"] == split:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["reader"], r["arm"])] = r
    scenes = list(entity)
    arms = sorted({a for _, _, a in by})
    missing = [(s, w, a) for s in scenes for w in X.READERS for a in arms if (s, w, a) not in by]
    assert not missing, f"{split}: {len(missing)} pair-reader-arm reads missing, e.g. {missing[:3]}"
    table = {w: {a: {"switched": [by[(s, w, a)]["switched"] for s in scenes], "moved": [by[(s, w, a)]["moved"] for s in scenes],
                     "route": [by[(s, w, a)]["route"] for s in scenes]} for a in arms} for w in X.READERS}  # fmt: skip
    return scenes, [entity[s] for s in scenes], table


def numbers(src: Path, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One run's numbers: per k on the test pairs own-IIA (R_pos, random, shuffled), the recall's cross-IIA (moves) under
    each, the lookup's route shares per arm, the whole change's rerun; the select split's own-IIA; the geometry means
    over the test pairs per R with the readouts."""
    m = json.loads((src / "manifest.json").read_text())
    ks = tuple(m["ks"])
    rows = X.read_jsonl(src / "outcomes.jsonl")
    readouts = json.loads((src / "readouts.json").read_text())
    _, _, sel = split_table(rows, "select")
    scenes, ent, t = split_table(rows, "test")
    lk, rc = t[X.LOOKUP], t[X.RECALL]
    s_whole = float(np.mean(lk["whole"]["switched"]))
    test: dict[str, Any] = {
        "n": len(scenes), "entities": len(set(ent)), "S_whole_rerun": round(s_whole, 4),
        "S_none": round(float(np.mean(lk["none"]["switched"])), 4),
        "recall_moved_whole": D.ci_of(rc["whole"]["moved"], ent, n_boot),
        "recall_moved_none": round(float(np.mean(rc["none"]["moved"])), 4),
        "own_iia": {}, "random_iia": {}, "shuffled_iia": {}, "recall_cross": {}, "recall_random": {}, "own_over_whole": {},
    }  # fmt: skip
    for k in ks:
        test["own_iia"][k] = D.ci_of(lk[f"R_pos_k{k}"]["switched"], ent, n_boot)
        test["random_iia"][k] = D.ci_of(lk[f"rand_k{k}"]["switched"], ent, n_boot)
        test["shuffled_iia"][k] = D.ci_of(lk[f"shuf_pos_k{k}"]["switched"], ent, n_boot)
        test["recall_cross"][k] = D.ci_of(rc[f"R_pos_k{k}"]["moved"], ent, n_boot)
        test["recall_random"][k] = D.ci_of(rc[f"rand_k{k}"]["moved"], ent, n_boot)
        test["own_over_whole"][k] = test["own_iia"][k][0] / s_whole if s_whole > 0 else None
    routes = {a: {rt: round(float(np.mean([r == rt for r in v["route"]])), 4) for rt in ROUTES_NAMES_ALL}
              for a, v in lk.items()}  # fmt: skip
    select = {"n": len(sel[X.LOOKUP]["none"]["switched"]),
              "own_iia": {k: round(float(np.mean(sel[X.LOOKUP][f"R_pos_k{k}"]["switched"])), 4) for k in ks},
              "S_whole": round(float(np.mean(sel[X.LOOKUP]["whole"]["switched"])), 4)}  # fmt: skip
    geo_rows = [g for g in X.read_jsonl(src / "geometry.jsonl") if g["split"] == "test"]
    geometry: dict[str, Any] = {}
    for key in sorted({g["R"] for g in geo_rows}):
        mine = [g for g in geo_rows if g["R"] == key]
        geometry[key] = {"n": len(mine), **{f: readouts[key][f] for f in ("cos2_U", "cos2_W", "random_expectation",
                                                                             "angles_vs_U", "angles_vs_W")}}  # fmt: skip
        for what in ("energy", "in_jpp25", "in_jpp100", "in_we25", "in_U", "in_W", "in_Ufit", "outside_union"):
            kept = [g for g in mine if g.get(what) is not None]
            geometry[key][what] = D.ci_of([g[what] for g in kept], [g["entity"] for g in kept], n_boot)
    return {"run": src.name, "target": m["model"]["target"], "layer": m["layer"], "ks": list(ks), "test": test,
            "select": select, "routes": routes, "geometry": geometry, "U_vs_W": readouts["U_vs_W"],
            "d": readouts["d"], "rank_U": readouts["rank_U"], "rank_W": readouts["rank_W"],
            "pairs": {k: v for k, v in json.loads((src / "pairs.json").read_text()).items() if k != "scene_ids"}}  # fmt: skip


def rules(num: dict[str, Any], k: int = K_RULE) -> dict[str, Any]:
    """Q49.8's labels at k (point estimates, EPS at the bars); exactly one holds: ours, else two codes, else no
    mediator, else in between. The not-selective flag (energy >= 0.8 of Delta) per R beside."""
    own = num["test"]["own_iia"][k][0]
    u_e = num["geometry"][f"R_pos_k{k}"]["cos2_U"]
    cross = num["test"]["recall_cross"][k][0]
    high = own >= OWN_IIA - EPS
    ours = high and u_e >= U_OURS - EPS and cross <= RECALL_CROSS + EPS
    two = high and u_e <= U_TWO + EPS
    no_med = not high
    label = "ours" if ours else "two_codes" if two else "no_mediator" if no_med else "in_between"
    not_selective = sorted(key for key, g in num["geometry"].items() if g["energy"][0] >= NOT_SELECTIVE - EPS)
    return {"label": label, "text": LABELS[label], "ours": bool(ours), "two_codes": bool(two), "no_mediator": bool(no_med),
            "in_between": label == "in_between", "k": k,
            "detail": {"own_iia": own, "U_energy_in_R": u_e, "W_energy_in_R": num["geometry"][f"R_pos_k{k}"]["cos2_W"],
                       "recall_cross_iia": cross, "random_expectation": num["geometry"][f"R_pos_k{k}"]["random_expectation"]},
            "not_selective": not_selective}  # fmt: skip


def report_lines(num: dict[str, Any], v: dict[str, Any], answer: str, n_boot: int) -> list[str]:
    t, g, ks = num["test"], num["geometry"], num["ks"]
    lines = ["# 49.8: DAS for the address", "",
             f"Batch 49, test 49.8 (jobs/c3/batch49.yaml; {QUESTION}, Dan: {answer}). {num['target']} at L{num['layer']} "
             f"({num['run']}). Pairs: {num['pairs']['pairs']} routes position counterfactuals ({num['pairs']['entities']} "
             f"bridge entities; per split {num['pairs']['pairs_per_split']}); test n = {t['n']} ({t['entities']} entities); "
             f"cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"**{v['text']}** (k = {v['k']}: own-IIA {v['detail']['own_iia']:.2f}, U's energy in R_pos "
             f"{v['detail']['U_energy_in_R']:.3f} (k/d {v['detail']['random_expectation']:.4f}), W's "
             f"{v['detail']['W_energy_in_R']:.3f}, the recall's cross-IIA {v['detail']['recall_cross_iia']:.2f})"
             + (f"; not selective (energy >= 0.8 of Delta): {', '.join(v['not_selective'])}" if v["not_selective"] else ""), "",
             f"As computed: {AS_COMPUTED}.", "",
             f"The whole change rerun on the test pairs: position {t['S_whole_rerun']:.2f}; O unedited {t['S_none']:.2f}; "
             f"the recall moved under the whole change {D.fmt(t['recall_moved_whole'])}, unedited {t['recall_moved_none']:.2f}.", "",
             "| k | select own-IIA | test own-IIA | random R | shuffled R | own / whole | recall cross (R_pos) | recall (random R) |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for k in ks:
        ow = t["own_over_whole"][k]
        lines.append(f"| {k}{' (rule)' if k == v['k'] else ''} | {num['select']['own_iia'][k]:.2f} | {D.fmt(t['own_iia'][k])} | "
                     f"{D.fmt(t['random_iia'][k])} | {D.fmt(t['shuffled_iia'][k])} | {'-' if ow is None else f'{ow:.2f}'} | "
                     f"{D.fmt(t['recall_cross'][k])} | {D.fmt(t['recall_random'][k])} |")  # fmt: skip
    lines += ["", "The lookup's routes on the test pairs per arm (shares):", "",
              "| arm | " + " | ".join(ROUTES_NAMES_ALL) + " |", "|---" * (len(ROUTES_NAMES_ALL) + 1) + "|"]  # fmt: skip
    for a, r in num["routes"].items():
        lines.append(f"| {a} | " + " | ".join(f"{r[rt]:.2f}" for rt in ROUTES_NAMES_ALL) + " |")
    lines += ["", f"Geometry on the test pairs (means [CI]); d = {num['d']}, rank U = {num['rank_U']}, rank W = {num['rank_W']}:", "",
              "| R | U's energy in R | W's energy in R | k/d | energy | in J++-25 | in J++-100 | in W_E-25 | in U | in W | in U_fit | outside (J++-25 ∪ U ∪ W_E-25) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, r in g.items():
        lines.append(f"| {key} | {r['cos2_U']:.3f} | {r['cos2_W']:.3f} | {r['random_expectation']:.4f} | {D.fmt(r['energy'])} | "
                     f"{D.fmt(r['in_jpp25'])} | {D.fmt(r['in_jpp100'])} | {D.fmt(r['in_we25'])} | {D.fmt(r['in_U'])} | "
                     f"{D.fmt(r['in_W'])} | {D.fmt(r['in_Ufit'])} | {D.fmt(r['outside_union'])} |")  # fmt: skip
    uw = num["U_vs_W"]
    rk = g[f"R_pos_k{v['k']}"]
    lines += ["", f"Angles (degrees, principal): U vs W {uw['angles']} (U's energy in W {uw['cos2_U_in_W']:.3f}, W's in U "
              f"{uw['cos2_W_in_U']:.3f}); R_pos (k = {v['k']}) vs U {rk['angles_vs_U']}; vs W {rk['angles_vs_W']}.", "",
              "Rules (fixed in advance): " + "; ".join(f"{LABELS[k_]}: {t_}" for k_, t_ in RULE.items()) + ".",
              f"Detail: {json.dumps(v['detail'])}"]  # fmt: skip
    return lines


def example_lines(src: Path, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view: k random test pairs (seed 0), each reader's O and S prompts as read (the bridge and the
    moved sentences marked), and every arm's top token with the lookup's route and the recall's move."""
    items = [it for it in X.read_jsonl(src / "cases.jsonl") if it["split"] == "test"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    pick = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    lines = [f"## {src.name}: {len(pick)} random test pairs of {len(items)} (seed {seed})", ""]
    for i in pick:
        it = items[i]
        lk = it["readers"][X.LOOKUP]
        lines += [f"### {it['scene']}: the {it['entity']}'s locker sentence moves from slot {it['slot_o']} to slot "
                  f"{it['slot_s']}; O answers {lk['answer']}, S answers {lk['s_answer']}, the counterfactual (position) "
                  f"answer {lk['cf_answer']}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{D.READER_NAME[w]}** ({rd['question']}), O as read:", "", "```", rd["marked"]["org"], "```", "",
                      "S (the source):", "", "```", rd["marked"]["alt"], "```", "",
                      "| arm | top token | " + ("route | position |" if w == X.LOOKUP else "moved off O's answer |"),
                      "|---|---|" + ("---|---|" if w == X.LOOKUP else "---|")]  # fmt: skip
            for a in arms:
                r = reads.get((it["scene"], w, a))
                if r is not None:
                    tail = f"{r['route']} | {r['switched']} |" if w == X.LOOKUP else f"{r['moved']} |"
                    lines.append(f"| {a} | {r['top_text']!r} | {tail}")
            lines.append("")
    return lines


def figure(num: dict[str, Any], v: dict[str, Any], path: Path) -> None:
    """Left: own-IIA on the test pairs by k (R_pos, random R, shuffled R; the whole change's rerun as a line) and the
    recall's moves under R_pos. Right: U's and W's energy inside R_pos by k against k / d."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, percent_axis, style_axes

    ks, t, g = num["ks"], num["test"], num["geometry"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    xs = np.arange(len(ks))
    for off, (lab, key, col) in zip((-0.27, -0.09, 0.09, 0.27), (("R_pos", "own_iia", INK), ("random R", "random_iia", MUTED),
                                                                 ("shuffled R", "shuffled_iia", "#b0aea4"),
                                                                 ("recall moved (R_pos)", "recall_cross", "#c0504d")), strict=True):  # fmt: skip
        vals = [t[key][k] for k in ks]
        a1.bar(xs + off, [x[0] for x in vals], 0.18, color=col, label=lab,
               yerr=[[x[0] - x[1] for x in vals], [x[2] - x[0] for x in vals]], capsize=2)  # fmt: skip
    a1.axhline(t["S_whole_rerun"], color=INK, ls="--", lw=0.8, label="whole change")
    a1.axhline(OWN_IIA, color=MUTED, ls=":", lw=0.8)
    a1.set_xticks(xs, [f"k = {k}" for k in ks])
    a1.set_ylim(0, 1)
    a1.set_title("Does R_pos alone move the lookup to the position answer?", fontsize=10)
    percent_axis(a1)
    style_axes(a1)
    a1.legend(fontsize=7, frameon=False)
    a2.plot(ks, [g[f"R_pos_k{k}"]["cos2_U"] for k in ks], "o-", color=INK, label="U's energy in R_pos")
    a2.plot(ks, [g[f"R_pos_k{k}"]["cos2_W"] for k in ks], "s-", color="#4f81bd", label="W's energy in R_pos")
    a2.plot(ks, [g[f"rand_k{k}"]["cos2_U"] for k in ks], "o:", color=MUTED, label="U in a random R")
    a2.axhline(U_OURS, color=MUTED, ls=":", lw=0.8)
    a2.set_ylim(0, 1)
    a2.set_xticks(ks)
    a2.set_xlabel("k")
    a2.set_title("Is the learned subspace the hand-built address?", fontsize=10)
    style_axes(a2)
    a2.legend(fontsize=7, frameon=False)
    fig.suptitle(f"49.8 {num['target']} L{num['layer']}: {v['text']} (test n = {t['n']}, 95% CI over bridge entities)",
                 fontsize=10)  # fmt: skip
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    out = RESULTS / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    models, lines = [], []
    ex = ["# 49.8 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word where "
          "R R^T Delta is added at L. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        num = numbers(src, n_boot)
        v = rules(num)
        models.append({**num, "rules": v})
        lines += [*report_lines(num, v, answer, n_boot), ""]
        figure(num, v, out / f"{run}.png")
        lines += [f"Figure: {run}.png", ""]
        ex += example_lines(src)
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x49_das_pos/<name>/)")
    ap.add_argument("--out", type=Path, default=None, help="plan: write plan.md and <target>.json here")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the 49.8 runs")
    ap.add_argument("--why", default="batch 49, test 49.8 (jobs/c3/batch49.yaml; Q49.8)")
    ap.add_argument("--steps", type=int, default=D.STEPS)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.out)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, steps=a.steps)
    else:
        stage_verdict(a.runs or [RUNS["qwen3.5-9b"]], a.n_boot)


if __name__ == "__main__":
    main()
