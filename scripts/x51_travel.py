"""x51_travel (batch 51, test 51.4; jobs/c3/batch51.yaml, design and rules fixed in advance; Q51.4 in
predictions/2026-10-28_dan.md): does the address travel? The pointer swap at the last token.

Scenes: the routes test's C0 scenes (x6_routes' generator, seed 2510; three locker sentences, then three pick
sentences), their original prompt O; eligibility and gate as x8_write.eligible, on C0 instead of C2 (both readers say
and read O's and S's answers right; O's read accuracy >= 0.80 per reader over the generated C0 scenes; the first 300).
j = the bridge item's locker slot, k = each other slot (two swaps per item). Halves: bridge entities sorted, shuffled
with random.Random(0), the first half fit (x49_attn.split_halves).

The last token = the read position: X0's chat read appends a digit's space token to the prompt and reads the answer
there (position len(ids) + len(space) - 1). Layers: L = X.PREDICTED and L + 4. Arms, each added at the last token's
block output at the layer (X0's AddRows), on O, both readers (one write, two reads, as x8_write):
  none            O unedited
  bridge_swap     s (mu_k - mu_j), mu = x8_write's slot means (x0_massmean.pointer_means: the layout-free mass-mean
                  slot means fit at the bridge word at L on the probe run's fresh scenes; not refit; the same vector at
                  L + 4), s in {1, 2} (the pointer swap's doses), every item
  bridge_random   a random vector of bridge_swap's norm (one per item, k, layer and s; seed 4401 as x8_write)
  last_swap       s (mu'_k - mu'_j), mu' = the class means of the lookup prompt's last-token states at that layer on
                  the fit half (by j; plain means, the routes scenes have one layout); read half only
  last_random     a random vector of last_swap's norm (same stream)
Read: X0's chat read; the lookup's answer classed as x8_write.classify (target = slot k's digit, original = slot j's,
third, other); the recall changed or not (top token != O's answer) and whose legs it gives (x8_write.recall_item).
Norms: per item ||h_last|| at L and L + 4, ||h_bridge|| at L and every arm's ||vector||; the swap's norm relative to
the last token's state norm at L is the report. Probe: the slot j from the lookup's last-token state at every layer
(x0_probe.cv_predict: one-hot ridge, 5 outer folds holding out whole bridge entities, the penalty by an inner 4-fold
CV), from the states cached in the run folder (states_last.npz, fp16, gitignored: 80-200 MB).

Rules (fixed in advance; verdict stage; point estimates decide, EPS 1e-9 at the bars; cells = layer in {L, L + 4} x
s in {1, 2}; bridge_swap over every item, last_swap over the read half; cluster-bootstrap CIs over bridge items,
10,000, seed 0, beside): see RULE.

SEALED: the run writes per-item files only; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's
Q51.4 answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x51_travel.py plan                              # CPU: counts, 5 prompts
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_travel.py run --name qwen35_9b_x51_4        # GPU (sealed)
uv run python scripts/x51_travel.py verdict --runs qwen35_9b_x51_4 muse30_x51_4 x51_4_27b  # CPU, after Dan's Q51.4
uv run python scripts/x51_travel.py view --runs qwen35_9b_x51_4 muse30_x51_4 x51_4_27b
"""

from __future__ import annotations

import argparse
import json
import random
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
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x49_attn as A

EXP = "x51_travel"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.4"
MODELS = ("qwen3.5-9b", "muse-glimmer-30b", "qwen3.6-27b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_4", "muse-glimmer-30b": "muse30_x51_4", "qwen3.6-27b": "x51_4_27b"}
# batch 52 C coverage (amendment 3, extra f): Lightning; verdict --coverage reads it alone, RUNS / own verdict unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_travel"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_travel/x51_4-20261028T173333Z"  # 51.4's rules first scored
CONDITION = "C0"
DOSES = (1.0, 2.0)
LAYER_STEP = 4
FITS = ("bridge", "last")
SWAP_ARMS = tuple(f"{f}_{kind}" for f in FITS for kind in ("swap", "random"))
STATES_FILE = "states_last.npz"
N_PROMPTS = 5
N_VIEW_ROWS = 10
EPS = 1e-9
TRAVEL_MIN, RAND_MAX, LOW_MAX, REENC_MIN, PROBE_MIN = 0.30, 0.05, 0.10, 0.30, 0.80
LABELS = {"travels": "(a) the code travels", "reencoded": "(b) re-encoded on copy",
          "not_last": "(c) not at the last token", "between": "(d) in between"}  # fmt: skip
RULE = ('"The code travels": the bridge-fit swap sends >= 0.3 of lookups to slot k (random <= 0.05). "Re-encoded on '
        'copy": bridge-fit <= 0.10 while last-token-fit >= 0.3. "Not at the last token": both <= 0.10 while the probe '
        "reads the slot there >= 0.8. Otherwise in between")  # fmt: skip
AS_COMPUTED = ("over the four cells (layer L or L + 4, s = 1 or 2): travels if some cell has bridge_swap's target share "
               ">= 0.30 and its own bridge_random's <= 0.05; else re-encoded if every cell's bridge_swap <= 0.10 and "
               "some cell's last_swap >= 0.30; else not at the last token if every cell's bridge_swap and last_swap "
               "<= 0.10 and the probe's held-out accuracy at the last token at L or L + 4 >= 0.80; else in between. "
               "bridge_swap / bridge_random over every item, last_swap / last_random over the read half")  # fmt: skip


# ---- items and arms (CPU-testable) ----------------------------------------------------------------------------------


def layers_of(target: str) -> tuple[int, int]:
    """(L, L + 4): the layer fixed in advance and four above it."""
    return X.PREDICTED[target], X.PREDICTED[target] + LAYER_STEP


def last_position(ids: list[int], space: list[int]) -> int:
    """The read position of X0's chat read: the last token of ids + space."""
    return len(ids) + len(space) - 1


def item_record(tok, case: dict, half: str) -> dict:
    """One C0 scene as the run uses it: the bridge's slot j, the other slots, the slots' digit tokens, both readers'
    O ids, answers and read positions."""
    from scripts import suite_v1 as S

    sl = W.slots_of(case["context"])
    assert len(sl) == 3, f"{case['scene']}: {len(sl)} locker sentences"
    j = [x for x, _ in sl].index(case["bridge"])
    space = A.read_space(tok, case)
    readers = {}
    for w in X.READERS:
        rd = case["readers"][w]
        ids = rd["ids"]["org"]
        readers[w] = {"question": rd["question"], "answer": rd["answer"], "tok_A": rd["tok_A"], "ids": ids,
                      "last": last_position(ids, space)}  # fmt: skip
    return {"scene": case["scene"], "entity": case["bridge"], "half": half, "j": j, "ks": [k for k in W.SLOTS if k != j],
            "slots": [[x, d] for x, d in sl], "digit_tokens": [S.answer_token(tok, str(d), "digit") for _, d in sl],
            "pos": case["pos"], "space": space, "context": case["context"], "readers": readers}  # fmt: skip


def class_means(states: np.ndarray, j: np.ndarray, mask: np.ndarray) -> dict[int, np.ndarray]:
    """Per slot k, the mean of the masked rows with j == k (float64); every slot must be present."""
    out = {}
    for k in W.SLOTS:
        rows = states[mask & (j == k)]
        assert len(rows), f"no fit item with slot {k}"
        out[k] = rows.astype(np.float64).mean(0)
    return out


def step_cos(mu_a: dict, mu_b: dict, j: int, k: int) -> float:
    """cos between two fits' steps mu_k - mu_j."""
    u, v = mu_a[k] - mu_a[j], mu_b[k] - mu_b[j]
    return float(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v))


def arm_specs(item: dict, layers: tuple[int, int], has_last: bool) -> list[tuple[str, int, int, float]]:
    """Every swap arm of one item in read order: (arm, layer, k, s); the last-token fit only on the read half."""
    fits = FITS if has_last else FITS[:1]
    return [(f"{f}_{kind}", la, k, s) for k in item["ks"] for la in layers for s in DOSES for f in fits
            for kind in ("swap", "random")]  # fmt: skip


def arm_vectors(specs, j: int, mu: dict, gen) -> list:
    """The vector of each spec: swap = s (mu_k - mu_j) with mu = mu[(fit, layer)]; random = a Gaussian direction of
    the preceding swap's norm (one draw per random arm, in spec order, from gen)."""
    import torch

    out: list = []
    for arm, la, k, s in specs:
        fit, kind = arm.split("_")
        if kind == "swap":
            m = mu[(fit, la)]
            out.append(s * (m[k] - m[j]))
        else:
            ref = out[-1]
            r = torch.randn(ref.shape[0], generator=gen).to(ref.device)
            out.append(r / r.norm() * ref.norm())
    return out


# ---- rules (CPU-testable) -----------------------------------------------------------------------------------------


def rule(cells: dict[tuple[str, str, float], float], probe: dict[str, float]) -> dict:
    """The rules fixed in advance on point estimates. cells: (arm, 'L' | 'L+4', s) -> the lookup's target share;
    probe: 'L' | 'L+4' -> the probe's held-out accuracy at the last token."""
    keys = sorted({(la, s) for _, la, s in cells})
    bs = {c: cells[("bridge_swap", *c)] for c in keys}
    br = {c: cells[("bridge_random", *c)] for c in keys}
    ls = {c: cells[("last_swap", *c)] for c in keys}
    travel_cells = [c for c in keys if bs[c] >= TRAVEL_MIN - EPS and br[c] <= RAND_MAX + EPS]
    bridge_low = all(v <= LOW_MAX + EPS for v in bs.values())
    last_high = [c for c in keys if ls[c] >= REENC_MIN - EPS]
    last_low = all(v <= LOW_MAX + EPS for v in ls.values())
    probe_high = max(probe.values()) >= PROBE_MIN - EPS
    clauses = {"travels": bool(travel_cells), "reencoded": bridge_low and bool(last_high),
               "not_last": bridge_low and last_low and probe_high}  # fmt: skip
    key = next((k for k in ("travels", "reencoded", "not_last") if clauses[k]), "between")
    fmt = lambda cs: [f"{la} s={s:g}" for la, s in cs]  # noqa: E731
    return {"label": LABELS[key], "key": key, "clauses": clauses, "travel_cells": fmt(travel_cells),
            "last_high_cells": fmt(last_high), "bridge_all_low": bridge_low, "last_all_low": last_low,
            "probe_max": max(probe.values()), "probe_high": probe_high}  # fmt: skip


def probe_rows(states: np.ndarray, j: list[int], ents: list[str], scenes: list[str], layers: list[int]) -> list[dict]:
    """Per layer and item: the slot j predicted from the last-token state by x0_probe's entity-held-out ridge
    (cv_predict, grouped) and by the training folds' majority (baseline). states [n, layers, d]."""
    from scripts import x0_probe as P

    rows = []
    for li, la in enumerate(layers):
        x = states[:, li].astype(np.float64)
        pred, outer, _ = P.cv_predict(x, list(j), ents, True)
        maj = P.baseline(list(j), outer)
        rows += [{"layer": la, "scene": s, "entity": e, "j": int(t), "pred": int(p), "right": int(p == t),
                  "majority_right": int(b == t), "fold": int(f)}
                 for s, e, t, p, b, f in zip(scenes, ents, j, pred, maj, outer, strict=True)]  # fmt: skip
    return rows


# ---- plan (CPU) ---------------------------------------------------------------------------------------------------


def stored_c0(target: str) -> tuple[list[dict], dict]:
    """The routes run's C0 items (its outcomes' order; the items its gate made eligible, the first 300) and its gate."""
    src = R.RESULTS / W.ROUTES_OF[target]
    scenes = list(
        dict.fromkeys(r["scene"] for r in X.read_jsonl(src / "outcomes.jsonl") if r["condition"] == CONDITION)
    )
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["condition"] == CONDITION}
    return [cases[s] for s in scenes], json.loads((src / "gate.json").read_text())["gate"][CONDITION]


def check_ids(tok, case: dict) -> None:
    """The lookup's O prompt re-rendered on this tokenizer gives the stored ids."""
    from bridge_jspace.tokens import raw_encoding

    rd = case["readers"][X.LOOKUP]
    text = A.rendered(tok, case["context"], rd["question"])
    assert raw_encoding(tok, text)["input_ids"] == rd["ids"]["org"], f"{case['scene']}: the stored ids differ"


def marked(decode, it: dict, reader: str = X.LOOKUP) -> str:
    """The reader's O prompt exactly as read (X0's space token appended), ⟦bridge:…⟧ the bridge word, ⟦last:…⟧ the
    read token where every swap is added."""
    ids = it["readers"][reader]["ids"] + it["space"]
    last = it["readers"][reader]["last"]
    assert last == len(ids) - 1
    out = []
    for i, t in enumerate(ids):
        piece = decode([t])
        out.append(f"⟦bridge:{piece}⟧" if i == it["pos"] else f"⟦last:{piece}⟧" if i == last else piece)
    return "".join(out)


def stage_plan() -> Path:
    """CPU (tokenizer and config): the routes run's C0 items for this target (the run re-selects them with
    x8_write's eligibility on C0 and records whether they agree), the split, layers, arms, reads, the cached states'
    size and 5 rendered prompts (seed 0)."""
    from huggingface_hub import hf_hub_download
    from transformers import AutoConfig

    from scripts import x0_massmean as MM
    from scripts import x45m

    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"51.4 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    tok = x45m.tokenizer()
    cases, gate = stored_c0(target)
    for c in cases:
        check_ids(tok, c)
    ents = [c["bridge"] for c in cases]
    fit, _ = A.split_halves(ents)
    items = [item_record(tok, c, "fit" if c["bridge"] in fit else "read") for c in cases]
    path = hf_hub_download(pins.MODEL_REPO, "config.json", revision=pins.MODEL_REVISION)
    cfg = AutoConfig.from_pretrained(path).get_text_config()
    n_layers, d = int(cfg.num_hidden_layers), int(cfg.hidden_size)
    lay = layers_of(target)
    assert lay[1] < n_layers, f"L + 4 = {lay[1]} is past the last layer {n_layers - 1}"
    n_read = sum(it["half"] == "read" for it in items)
    j_fit = [it["j"] for it in items if it["half"] == "fit"]
    try:
        mu = MM.pointer_means(R.STATES[target])
        step = {f"{a}-{b}": round(float(np.linalg.norm(mu[b] - mu[a])), 4) for a in W.SLOTS for b in W.SLOTS if a < b}
    except (OSError, KeyError) as e:
        step = {"not available here": str(e)}
    n_fit_arms, n_read_arms = len(arm_specs(items[0], lay, False)), len(arm_specs(items[0], lay, True))
    reads = (len(items) - n_read) * (1 + n_fit_arms) + n_read * (1 + n_read_arms)
    counts = {
        "target": target, "layers": list(lay), "n_layers": n_layers, "d": d, "routes_run": W.ROUTES_OF[target],
        "routes_c0_gate": gate, "items": len(items), "entities": len(set(ents)), "fit_items": len(items) - n_read,
        "read_items": n_read, "fit_entities": len(fit), "read_entities": len(set(ents) - fit),
        "fit_items_by_slot": {k: j_fit.count(k) for k in W.SLOTS},
        "items_by_slot": {k: sum(it["j"] == k for it in items) for k in W.SLOTS},
        "pairs": 2 * len(items), "read_pairs": 2 * n_read, "doses": list(DOSES),
        "arms_per_item": {"fit half": 1 + n_fit_arms, "read half": 1 + n_read_arms},
        "rows_per_cell_per_reader": {"bridge_swap / bridge_random (every item)": 2 * len(items),
                                     "last_swap / last_random (read half)": 2 * n_read},
        "cells": [f"L{la} s={s:g}" for la in lay for s in DOSES],
        "reads_per_reader": reads, "reads": 2 * reads,
        "states_last_mb": round(len(items) * n_layers * d * 2 / 1e6, 1),
        "bridge_fit_step_norms": step, "mu_from": R.STATES[target],
        "max_read_len": max(len(it["readers"][w]["ids"]) + len(it["space"]) for it in items for w in X.READERS),
    }  # fmt: skip
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    (out / f"plan_{target}.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    lines = [f"# 51.4 plan, {target}: {N_PROMPTS} random items (seed {X.EXAMPLES_SEED}) of {len(items)}", "",
             "Each reader's O prompt exactly as the model reads it (chat template, X0's read suffix appended); "
             f"⟦bridge:…⟧ the bridge word (where x8's swap was written), ⟦last:…⟧ the read token, where every 51.4 arm "
             f"adds its vector at L{lay[0]} or L{lay[1]}. UNVERIFIED.", ""]  # fmt: skip
    for i in sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(items)), min(N_PROMPTS, len(items)))):
        it = items[i]
        lines += [f"## {it['scene']} ({it['half']} half): bridge {it['entity']}, j = {it['j']}, k in {it['ks']}; lockers "
                  f"{it['slots']}", ""]  # fmt: skip
        for w in X.READERS:
            lines += [
                f"**{w}** (O's answer {it['readers'][w]['answer']}):",
                "",
                "```",
                marked(decode, it, w),
                "```",
                "",
            ]
    (out / f"prompts_{target}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("wrote", out)
    return out


# ---- GPU ----------------------------------------------------------------------------------------------------------


def eligible_c0(model, gate_min: float, n: int):
    """x8_write.eligible on the routes test's C0 scenes (x8 takes C2): the gate on O's read accuracy per reader over
    the generated C0 scenes, eligible = both readers say and read O's and S's answers right; the first n."""
    import torch

    cases, _ = R.scenes(model.tokenizer, R.N_GEN)
    cases = [c for c in cases if c["condition"] == CONDITION]
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
    X.DIGIT_IDS.update(X.digit_ids(model.tokenizer))
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    gate = {"condition": CONDITION, "cases": len(cases), "org_read_accuracy": acc, "gate_min": gate_min,
            "pass": all(a >= gate_min for a in acc.values()), "eligible": len(ok)}  # fmt: skip
    return (ok[:n] if gate["pass"] else []), gate


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import tasks_v2 as T
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.4 reads chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"51.4 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    lay = layers_of(target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    routes = R.RESULTS / W.ROUTES_OF[target]
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "test": "51.4", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
        "spec": "jobs/c3/batch51.yaml (51.4)", "question": f"{QUESTION} ({PREDICTIONS})", "layers": list(lay),
        "doses": list(DOSES), "mu_from": R.STATES[target],
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in
                   (SPEC, routes / "gate.json", routes / "outcomes.jsonl",
                    pins.RESULTS_DIR / "x0_probe" / R.STATES[target] / "states.npz") if p.exists()},
        "items_rule": f"x8_write.eligible's gate and eligibility on the routes generator's {CONDITION} scenes (O; gate "
                      f"{X.GATE} per reader on O's read accuracy; the first {W.N_ITEMS} eligible)",
        "site": "the last token = the read position of X0's chat read (the digit's space token appended to O)",
        "arms": {"none": "O unedited",
                 "bridge_swap": "s (mu_k - mu_j) added at the last token at the layer; mu = x0_massmean.pointer_means "
                                "(fit at the bridge word at L on the probe run's scenes; not refit, the same at L + 4)",
                 "bridge_random": f"a Gaussian vector of bridge_swap's norm (one per item, k, layer, s; seed {W.RAND_SEED})",
                 "last_swap": "s (mu'_k - mu'_j), mu' = class means by j of the lookup's last-token states at that "
                              "layer over the fit half; read half only",
                 "last_random": "a Gaussian vector of last_swap's norm (same stream)"},
        "split": f"bridge entities sorted, shuffled with random.Random({A.SPLIT_SEED}), first half fit (x49_attn.split_halves)",
        "probe": "x0_probe.cv_predict on the lookup's last-token states per layer (one-hot ridge, 5 outer folds holding "
                 "out whole bridge entities, inner 4-fold penalty); majority baseline (training folds); chance 1/3",
        "rule": RULE, "as_computed": AS_COMPUTED,
        "seeds": {"scenes": R.SEED, "random_vectors": W.RAND_SEED, "split": A.SPLIT_SEED, "bootstrap": X.BOOT_SEED,
                  "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
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
    dev = model.device
    n_layers = len(model.layers)
    assert lay[1] < n_layers, f"L + 4 = {lay[1]} is past the last layer"
    chosen, gate = eligible_c0(model, X.GATE, W.N_ITEMS)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not chosen:
        (out / "status.json").write_text(json.dumps({"status": "not tested", "gate": gate}, indent=2) + "\n")
        print("the gate missed (or no eligible items): not tested", gate, flush=True)
        return out
    stored = [c["scene"] for c in stored_c0(target)[0]] if (routes / "outcomes.jsonl").exists() else None
    m["same_items_as_routes_run"] = None if stored is None else [c["scene"] for c in chosen] == stored
    fit, _ = A.split_halves([c["bridge"] for c in chosen])
    items = [item_record(tok, c, "fit" if c["bridge"] in fit else "read") for c in chosen]
    X.write_jsonl(out / "cases.jsonl", items)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

    all_layers = tuple(range(n_layers))
    n = len(items)
    cache = None
    h_swap = {la: [] for la in lay}  # fp32 last-token rows at L and L + 4 (the fit's inputs)
    norms: list[dict] = []
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"51.4: last-token states, {n_layers} layers (item)")):
            ids = it["readers"][X.LOOKUP]["ids"] + it["space"]
            last = it["readers"][X.LOOKUP]["last"]
            _, rec = model.run(torch.tensor([ids], device=dev), record=all_layers)
            row = torch.stack([rec[la][last] for la in all_layers]).cpu()
            if cache is None:
                cache = np.zeros((n, n_layers, row.shape[1]), np.float16)
            cache[i] = row.half().numpy()
            for la in lay:
                h_swap[la].append(rec[la][last].clone().cpu())
            norms.append({"scene": it["scene"], "entity": it["entity"], "half": it["half"],
                          **{f"h_last_L{la}": round(float(rec[la][last].norm()), 4) for la in lay},
                          f"h_bridge_L{lay[0]}": round(float(rec[lay[0]][it["pos"]].norm()), 4)})  # fmt: skip
            del rec
    assert cache is not None
    j_all = np.array([it["j"] for it in items])
    np.savez(out / STATES_FILE, h=cache, layers=np.array(all_layers), j=j_all,
             scenes=np.array([it["scene"] for it in items]), entities=np.array([it["entity"] for it in items]))  # fmt: skip
    is_fit = np.array([it["half"] == "fit" for it in items])
    mu_np = {("bridge", la): MM.pointer_means(R.STATES[target]) for la in lay}
    for la in lay:
        mu_np[("last", la)] = class_means(torch.stack(h_swap[la]).numpy(), j_all, is_fit)
    means = np.stack([np.stack([mu_np[("last", la)][k] for k in W.SLOTS]) for la in lay])  # [layers, slots, d]
    np.savez(out / "u_last.npz", means=means, layers=np.array(lay), slots=np.array(W.SLOTS))
    m["steps"] = {f"{f}_L{la}": {f"{a}-{b}": round(float(np.linalg.norm(mu_np[(f, la)][b] - mu_np[(f, la)][a])), 4)
                                 for a in W.SLOTS for b in W.SLOTS if a < b} for f in FITS for la in lay}  # fmt: skip
    m["cos_bridge_last"] = {f"L{la}": {f"{a}-{b}": round(step_cos(mu_np[("bridge", la)], mu_np[("last", la)], a, b), 4)
                                       for a in W.SLOTS for b in W.SLOTS if a < b} for la in lay}  # fmt: skip
    m["fit_items_by_slot"] = {k: int(((j_all == k) & is_fit).sum()) for k in W.SLOTS}
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    del h_swap

    mu = {
        key: {k: torch.tensor(v, dtype=torch.float32, device=dev) for k, v in val.items()} for key, val in mu_np.items()
    }
    legs = T.DOMAINS["animals"].values
    gen = torch.Generator().manual_seed(W.RAND_SEED)
    rows: list[dict] = []
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"51.4: swaps at the last token, L{lay[0]} / L{lay[1]} (item)")):
            specs = arm_specs(it, lay, it["half"] == "read")
            vecs = arm_vectors(specs, it["j"], mu, gen)
            for (arm, la, k, s), v in zip(specs, vecs, strict=True):
                norms[i][f"{arm}|L{la}|k{k}|s{s:g}"] = round(float(v.norm()), 4)
            tokens = dict(enumerate(it["digit_tokens"]))
            slots = [tuple(x) for x in it["slots"]]
            base = {"scene": it["scene"], "entity": it["entity"], "half": it["half"], "j": it["j"]}
            for w, rd in it["readers"].items():
                edits = [{}] + [
                    {la: AddRows(v[None], [rd["last"]])} for (_, la, _, _), v in zip(specs, vecs, strict=True)
                ]
                logits, _ = X.read_logits(model, rd["ids"], edits, "chat", it["space"], None)
                for spec, lg in zip([("none", None, None, 0.0), *specs], logits, strict=True):
                    arm, la, k, s = spec
                    top = int(lg.argmax())
                    row = {**base, "reader": w, "arm": arm, "layer": la, "k": k, "s": s, "top": top}
                    if w == X.LOOKUP:
                        row["class"] = W.classify(top, tokens, it["j"], k)
                        row["right"] = int(top == rd["tok_A"])
                    else:
                        row["changed"] = int(top != rd["tok_A"])
                        if k is not None:
                            row["recall_class"] = W.recall_item(tok.decode([top]).strip(), slots, legs, it["j"], k)
                    rows.append(row)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    print(f"wrote {len(rows)} reads of {n} items; fitting the probe per layer (CPU)", flush=True)
    probe = probe_rows(cache, [it["j"] for it in items], [it["entity"] for it in items], [it["scene"] for it in items],
                       list(all_layers))  # fmt: skip
    X.write_jsonl(out / "probe.jsonl", probe)
    (out / "status.json").write_text(json.dumps({"status": "tested", "items": n}, indent=2) + "\n")
    print(f"wrote {out} (sealed: no verdict)", flush=True)
    return out


# ---- verdict and view (CPU, sealed) -------------------------------------------------------------------------------


def parse_answer(text: str) -> str:
    """Dan's Q51.4 answer (x48_heads.parse_answer: 'Dan:' and 'Dan (27B):' lines and bullet continuations), ''."""
    from scripts import x48_heads as H

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


def tag(layer: int, lay: list[int]) -> str:
    return "L" if layer == lay[0] else "L+4"


def in_cell(r: dict, arm: str, layer: int, s: float, scope: str) -> bool:
    """A row of this arm, layer and dose, on every item ('all') or the read half."""
    return (r["arm"], r["layer"], r["s"]) == (arm, layer, s) and (scope == "all" or r["half"] == "read")


def analyse(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One run's numbers: per (arm, layer, s) the lookup's class shares (target / original / third / other) and the
    recall's (changed, the target item's legs), CIs by cluster bootstrap over bridge entities; the paired target
    difference swap minus its random; the probe per layer; the norm ratios; the rule."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"run": run, "status": "pending", "label": "pending"}
    m = json.loads((src / "manifest.json").read_text())
    st = json.loads((src / "status.json").read_text()) if (src / "status.json").exists() else {"status": "not finished"}
    if st["status"] != "tested":
        return {"run": run, "target": m["model"]["target"], "status": st["status"], "label": st["status"],
                "gate": st.get("gate")}  # fmt: skip
    lay = m["layers"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    lk = [r for r in rows if r["reader"] == X.LOOKUP]
    rc = [r for r in rows if r["reader"] == X.RECALL]
    cells, table, diffs = {}, [], {}
    for arm in SWAP_ARMS:
        for la in lay:
            for s in DOSES:
                for scope in ("all", "read") if arm.startswith("bridge") else ("read",):
                    mine = [r for r in lk if in_cell(r, arm, la, s, scope)]
                    if not mine:
                        continue
                    sh = W.shares(mine, "class", W.CLASSES, n_boot)
                    rmine = [r for r in rc if in_cell(r, arm, la, s, scope)]
                    rch = W.shares([{**r, "c": str(r["changed"])} for r in rmine], "c", ("1",), n_boot)
                    rtg = W.shares(rmine, "recall_class", ("target",), n_boot)
                    entry = {"arm": arm, "layer": la, "tag": tag(la, lay), "s": s, "scope": scope, "n": sh["n"],
                             **{c: sh[c] for c in W.CLASSES}, "recall_changed": rch["1"], "recall_target_item": rtg["target"],
                             "_r": sh["_r"]["target"]}  # fmt: skip
                    table.append(entry)
                    decisive = scope == ("all" if arm.startswith("bridge") else "read")
                    if decisive:
                        cells[(arm, tag(la, lay), s)] = sh["target"][0]
    by = {(e["arm"], e["layer"], e["s"], e["scope"]): e for e in table}
    for fit, scope in (("bridge", "all"), ("bridge", "read"), ("last", "read")):
        for la in lay:
            for s in DOSES:
                a, b = by.get((f"{fit}_swap", la, s, scope)), by.get((f"{fit}_random", la, s, scope))
                if a and b:
                    diffs[f"{fit}|{scope}|{tag(la, lay)}|s{s:g}"] = [
                        a["target"][0] - b["target"][0],
                        *X.interval(a["_r"] - b["_r"]),
                    ]
    none = [r for r in lk if r["arm"] == "none"]
    none_rc = [r for r in rc if r["arm"] == "none"]
    pr = X.read_jsonl(src / "probe.jsonl")
    probe = {}
    for la in sorted({r["layer"] for r in pr}):
        mine = [r for r in pr if r["layer"] == la]
        rr = X.resampled_rates({"p": [r["right"] for r in mine], "m": [r["majority_right"] for r in mine]},
                               [r["entity"] for r in mine], n_boot)  # fmt: skip
        probe[la] = {"acc": [float(np.mean([r["right"] for r in mine])), *X.interval(rr["p"])],
                     "majority": [float(np.mean([r["majority_right"] for r in mine])), *X.interval(rr["m"])], "n": len(mine)}  # fmt: skip
    norms = X.read_jsonl(src / "norms.jsonl")
    ratio: dict[str, float] = {}
    for arm in ("bridge_swap", "last_swap"):
        for la in lay:
            for s in DOSES:
                vals = [nr[key] / nr[f"h_last_L{lay[0]}"] for nr in norms for key in nr
                        if key.startswith(f"{arm}|L{la}|") and key.endswith(f"|s{s:g}")]  # fmt: skip
                if vals:
                    ratio[f"{arm}|{tag(la, lay)}|s{s:g}"] = float(np.median(vals))
    bridge_ratio = [nr[f"bridge_swap|L{lay[0]}|k{k}|s1"] / nr[f"h_bridge_L{lay[0]}"] for nr in norms for k in W.SLOTS
                    if f"bridge_swap|L{lay[0]}|k{k}|s1" in nr]  # fmt: skip
    last_norm_ratio = [nr[f"h_last_L{lay[0]}"] / nr[f"h_bridge_L{lay[0]}"] for nr in norms]
    res = rule(cells, {tag(la, lay): probe[la]["acc"][0] for la in lay})
    per_layer = {}
    for t in ("L", "L+4"):
        sub = {k: v for k, v in cells.items() if k[1] == t}
        per_layer[t] = rule(sub, {t: probe[lay[0] if t == "L" else lay[1]]["acc"][0]})["label"]
    return {"run": run, "target": m["model"]["target"], "status": "tested", "layers": lay, "n_items": len(none),
            "n_entities": len({r["entity"] for r in none}), "n_read": sum(r["half"] == "read" for r in none),
            "none_lookup_right": float(np.mean([r["right"] for r in none])),
            "none_recall_changed": float(np.mean([r["changed"] for r in none_rc])),
            "table": [{k: v for k, v in e.items() if k != "_r"} for e in table], "cells": {"|".join(map(str, k)): v for k, v in cells.items()},
            "swap_minus_random": diffs, "probe": probe, "ratio_to_h_last_L": ratio,
            "bridge_swap_s1_over_h_bridge_L_median": float(np.median(bridge_ratio)) if bridge_ratio else None,
            "h_last_over_h_bridge_L_median": float(np.median(last_norm_ratio)), "steps": m.get("steps"),
            "cos_bridge_last": m.get("cos_bridge_last"), "same_items_as_routes_run": m.get("same_items_as_routes_run"),
            **res, "label_per_layer": per_layer}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(res: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.2))
    decisive = [e for e in res["table"] if e["scope"] == ("all" if e["arm"].startswith("bridge") else "read")]
    labels = [f"{e['tag']}\ns={e['s']:g}" for e in decisive if e["arm"] == "bridge_swap"]
    x = np.arange(len(labels))
    colors = {"bridge_swap": "#1f5fa8", "bridge_random": "#9bb7d9", "last_swap": "#b8562a", "last_random": "#e2b49c"}
    for i, arm in enumerate(SWAP_ARMS):
        es = [e for e in decisive if e["arm"] == arm]
        t = np.array([e["target"] for e in es])
        ax.bar(x + (i - 1.5) * 0.2, t[:, 0], 0.2, yerr=[t[:, 0] - t[:, 1], t[:, 2] - t[:, 0]], color=colors[arm],
               label=arm.replace("_", " "), capsize=2)  # fmt: skip
    ax.axhline(TRAVEL_MIN, color="0.4", ls=":", lw=1)
    ax.axhline(LOW_MAX, color="0.6", ls=":", lw=1)
    ax.set_xticks(x, labels)
    ax.set_ylabel("lookup answers slot k (share)")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title(f"{res['target']}: the swap at the last token")
    la = sorted(res["probe"])
    acc = np.array([res["probe"][x_]["acc"] for x_ in la])
    bx.plot(la, acc[:, 0], color="#1f5fa8", label="probe (entity held out)")
    bx.fill_between(la, acc[:, 1], acc[:, 2], color="#1f5fa8", alpha=0.2, lw=0)
    bx.plot(la, [res["probe"][x_]["majority"][0] for x_ in la], color="0.5", ls="--", label="majority")
    bx.axhline(1 / 3, color="0.7", ls=":", lw=1)
    bx.axhline(PROBE_MIN, color="0.4", ls=":", lw=1)
    for v in res["layers"]:
        bx.axvline(v, color="#b8562a", lw=0.8)
    bx.set_xlabel("layer")
    bx.set_ylabel("slot j read at the last token")
    bx.set_ylim(0, 1.02)
    bx.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def verdict_lines(results: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.4: does the address travel? The swap at the last token", "",
             f"Batch 51, test 51.4 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). Routes C0 scenes, O; the pointer "
             "swap s (mu_k - mu_j) added at the last (read) token at L and L + 4, with x8's bridge-word means and with "
             f"means refit on the last token (fit half), each against a random vector of its norm. Cluster bootstrap over "
             f"the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             f"As computed: {AS_COMPUTED}.", "",
             "| model | run | n (read) | label | per layer (L / L+4) | probe at L / L+4 | none: lookup right |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in results:
        if r["status"] != "tested":
            lines.append(f"| {r.get('target', '?')} | {r['run']} | {r['status']} | **{r['label']}** | | | |")
            continue
        p = r["probe"]
        lines.append(f"| {r['target']} | {r['run']} | {r['n_items']} ({r['n_read']}) | **{r['label']}** | "
                     f"{r['label_per_layer']['L']} / {r['label_per_layer']['L+4']} | {fmt(p[r['layers'][0]]['acc'])} / "
                     f"{fmt(p[r['layers'][1]]['acc'])} | {r['none_lookup_right']:.2f} |")  # fmt: skip
    for r in results:
        if r["status"] != "tested":
            continue
        lay = r["layers"]
        lines += ["", f"## {r['target']} ({r['run']}; L = {lay[0]}, L + 4 = {lay[1]}; {r['n_items']} items, "
                  f"{r['n_entities']} bridge items, read half {r['n_read']})", "",
                  "Clauses: " + "; ".join(f"{k} {v}" for k, v in r["clauses"].items())
                  + f"; travel cells {r['travel_cells']}; last-fit cells >= 0.3 {r['last_high_cells']}.", "",
                  "| arm | layer | s | items | n | slot k (target) | original (clean answer kept) | third | other | "
                  "recall changed | recall gives slot k's item |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for e in r["table"]:
            lines.append(f"| {e['arm']} | {e['tag']} | {e['s']:g} | {e['scope']} | {e['n']} | {fmt(e['target'])} | "
                         f"{fmt(e['original'])} | {fmt(e['third'])} | {fmt(e['other'])} | {fmt(e['recall_changed'])} | "
                         f"{fmt(e['recall_target_item'])} |")  # fmt: skip
        lines += ["", "Swap minus its random (target share, paired CI): "
                  + "; ".join(f"{k} {fmt(v)}" for k, v in r["swap_minus_random"].items()) + ".", "",
                  f"Norms (median): the swap's norm / ||h_last|| at L{lay[0]}: "
                  + ", ".join(f"{k} {v:.3f}" for k, v in r["ratio_to_h_last_L"].items())
                  + f". Beside: x8's swap at the bridge word, s = 1, / ||h_bridge|| at L: "
                  f"{r['bridge_swap_s1_over_h_bridge_L_median']:.3f}; ||h_last|| / ||h_bridge|| at L: "
                  f"{r['h_last_over_h_bridge_L_median']:.2f}. ||mu_k - mu_j||: {r['steps']}; cos(bridge-fit, "
                  f"last-fit step): {r['cos_bridge_last']}.", "",
                  f"Unedited: the lookup reads O's answer on {r['none_lookup_right']:.2f}; the recall changed on "
                  f"{r['none_recall_changed']:.2f}. Items as the routes run's C0 items: {r['same_items_as_routes_run']}.", "",
                  "Probe (slot j at the last token; entity held out; chance 0.33): "
                  + ", ".join(f"L{la} {v['acc'][0]:.2f} (maj {v['majority'][0]:.2f})" for la, v in r["probe"].items())
                  + ".", "", f"![{r['target']}](travel_{r['target']}.png)"]  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """51.4's verdict (sealed until Q51.4), or with coverage (batch 52) the same rules on the given runs, no seal guard,
    "no prediction" in place of Dan's answer (x52_travel-<UTC>/)."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else sealed()
    results = [analyse(run, n_boot) for run in runs]
    out = RESULTS / f"{'x52_travel' if coverage else 'x51_4'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    for r in results:
        if r["status"] == "tested":
            figure(r, out / f"travel_{r['target']}.png")
    lines = verdict_lines(results, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ") for ln in lines]
    blob = {"dan": answer, "rule": RULE, "as_computed": AS_COMPUTED, "labels": LABELS, "models": results,
            "per_model": {r.get("target", r["run"]): r["label"] for r in results}}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False, default=str) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(runs: list[str], decode_for=None, k: int = N_VIEW_ROWS, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """Per tested run: 5 rendered prompts (seed 0; both readers, bridge and last token marked) and 10 random rows per
    arm (seed 0) with the decoded top token."""
    from scripts import x47_atoms as AT

    lines = [
        "# 51.4 view (verify pack): prompts exactly as the model reads them; 10 random rows per arm. UNVERIFIED.",
        "",
    ]
    for run in runs:
        src = RESULTS / run
        if not (src / "status.json").exists() or json.loads((src / "status.json").read_text())["status"] != "tested":
            continue
        target = json.loads((src / "manifest.json").read_text())["model"]["target"]
        decode = (decode_for or AT.default_decode)(target)
        items = X.read_jsonl(src / "cases.jsonl")
        rows = X.read_jsonl(src / "outcomes.jsonl")
        lines += [f"## {run} ({target})", ""]
        for i in sorted(random.Random(seed).sample(range(len(items)), min(N_PROMPTS, len(items)))):
            it = items[i]
            lines += [
                f"### {it['scene']} ({it['half']}): bridge {it['entity']}, j = {it['j']}, lockers {it['slots']}",
                "",
            ]
            for w in X.READERS:
                lines += [
                    f"**{w}** (O's answer {it['readers'][w]['answer']}):",
                    "",
                    "```",
                    marked(decode, it, w),
                    "```",
                    "",
                ]
        for arm in ("none", *SWAP_ARMS):
            mine = [r for r in rows if r["arm"] == arm]
            pick = sorted(random.Random(seed).sample(range(len(mine)), min(k, len(mine))))
            lines += [f"### {arm}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                      "| scene | reader | layer | j | k | s | top | lookup class / recall changed (item) |",
                      "|---|---|---|---|---|---|---|---|"]  # fmt: skip
            for p in pick:
                r = mine[p]
                what = r["class"] if r["reader"] == X.LOOKUP else f"{r['changed']} ({r.get('recall_class', '-')})"
                lines.append(f"| {r['scene']} | {r['reader']} | {r['layer']} | {r['j']} | {r['k']} | {r['s']:g} | "
                             f"{decode([r['top']])!r} | {what} |")  # fmt: skip
            lines.append("")
    return lines


def stage_view(runs: list[str], decode_for=None) -> Path:
    sealed()
    out = RESULTS / f"x51_4-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "view.md").write_text("\n".join(view_lines(runs, decode_for)) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_travel/<name>/)")
    ap.add_argument("--runs", nargs="+", default=[RUNS[t] for t in MODELS], help="verdict / view: the runs")
    ap.add_argument(
        "--why", default="batch 51, test 51.4 (jobs/c3/batch51.yaml; Q51.4): the swap at the last token; sealed"
    )
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
