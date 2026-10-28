"""x51_lightning (batch 51, test 51.6, optional; jobs/c3/batch51.yaml, design and rule fixed in advance; Q51.6 in
predictions/2026-10-28_dan.md): the main test on NVIDIA Nemotron 3.5 Lightning 30B-A3B, at a layer picked on dev scenes.

Model: pins.TARGETS["nemotron-3.5-lightning"] as pinned (hybrid Mamba-2 / attention / MoE, 52 blocks; HF-hub mamba-ssm
kernels; no BOS; thinking off through the chat template; our local J++ lens, LN rule, layers 0-50, sha 3306b6e4). One
GPU (the 45s smoke peaked at 62.5 GB on an H100 PCIe 80 GB).

Scenes: the main test's (x0_necessity, alt cf: two people swap their picks; d1_topics_v3, chat), built on Lightning's
tokenizer (x0_necessity.build_cases), X0's competence pass and gate on every scene (unedited org accuracy under the
top-token read >= 0.80 for both readers, >= 150 eligible; a failed gate is "not tested"), X0's eligibility (both
readers say and read O's and S's answers right). The eligible scenes (scene order) split once: dev = N_DEV of them drawn
with random.Random(DEV_SEED).sample (kept in scene order); test = the first N_TEST eligible scenes not in dev.

Step 1 (dev): Δ_l = h_S - h_O at the bridge word at every layer l of LAYERS (every 2nd layer, L2-L50; one forward of O
and one of S per scene recording all of them), the whole change Δ_l added at the bridge word at l on O (X0's AddRows),
both readers, X0's chat read (switch = the top token over the vocabulary is S's answer's first token). Rule fixed in
advance: the layer is the earliest l where both readers' switch rates are >= 0.3 (point estimates, EPS at the bar). If
no layer passes, the job records "no layer passes step 1" and stops (no step 2).
Step 2 (test, only if step 1 passes): the main test's three arms at that layer, X0's machinery: whole (Δ), without J++
(Δ - P_J Δ; P_J = X0's 25-atom signed OMP over the J++ lens's letter-token atoms at L, x0_necessity.fit), without a
random part of the same share (Δ - R Δ; X0's random subspace, seed 888 + L, statement_positions.random_subspace_part),
plus the unedited row; both readers on the identical patch.

Q51.6 (verdict, CPU): (i) a layer passes step 1 (yes / no, and which); (ii) if yes, "the split holds there": gap >= 0.3
and the lookup's extra loss <= 0.10, where extra loss = X0's excess = Jdep - Rdep = (S_no_rand - S_no_part) / S_whole
and gap = the recall's minus the lookup's (x45m.group_cells / x45m.holds, point estimates, EPS 1e-9). Cluster bootstrap
over the bridge items (10,000, seed 0) beside; X0's validity bar per cell (S_whole >= 0.30 and >= 30 switches) and X0's
23 Oct verdict reported, not in the rule.

SEALED: the run writes per-item files, the step-1 layer pick (the procedure needs it) and no verdict; verdict and view
refuse until predictions/2026-10-28_dan.md holds Dan's committed Q51.6 answer at HEAD.

Batch 52 (jobs/c3/batch52.yaml, part C; Dan 29 Oct 00:25 / 00:30): the `prereq` stage fixes Lightning's layer for the
coverage cells by the published rule before any scored run: the gate on 60 main-test scenes (the first 60 in scene
order, X0's read and bar 0.80 per reader; X0's all-scene gate beside), then step 1 alone on the same 60 dev scenes
(the 51.6 split, seed 0) at every 4th layer L2-L50, the layer = the earliest where both readers switch >= 0.3. It
writes layer.json (the artefact the coverage specs read once it is committed) and no step 2, no verdict. Not a
prediction: a design choice by the published rule (the batch 52 addendum).

uv run python scripts/x51_lightning.py plan                                              # CPU, Lightning's tokenizer
BJ_TARGET=nemotron-3.5-lightning uv run python scripts/x51_lightning.py run --name nem35l_x51_6   # GPU (sealed)
BJ_TARGET=nemotron-3.5-lightning uv run python scripts/x51_lightning.py prereq --name nem35l_x52_layer  # GPU, batch 52
uv run python scripts/x51_lightning.py verdict | view                                    # CPU, after Dan's Q51.6
"""

from __future__ import annotations

import argparse
import collections
import json
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
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X

EXP = "x51_lightning"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.6"
TEST = "51.6"
TARGET = "nemotron-3.5-lightning"
RUN = "nem35l_x51_6"  # the live prefix of the pin (nem35l_, as nem35l_x45s_*)
SET = "d1_topics_v3"
RENDERING = "chat"
LAYERS = tuple(range(2, 51, 2))  # every 2nd layer, L2-L50 (the lens's maps: 0-50; as 47.8's 9B sweep, from L2)
N_DEV, DEV_SEED, N_TEST = 60, 0, 200
SWITCH_MIN = 0.3  # step 1: both readers' whole-change switch rate
GAP_MIN, LOOKUP_MAX = 0.3, 0.10  # step 2: the split (x45m's bars)
EPS = 1e-9  # a value exactly at a bar counts as at the bar
KERNEL_REVISION = "28017f36635a6b94d911333812beeed5dd901ac0"  # the mamba-ssm commit the 45s smoke loaded and passed
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0  # the verify pack
ARMS2 = ("none", "whole", "no_part", "no_rand")  # step 2's read order (X0's)
NO_LAYER = "the bridge word does not redirect the lookup at any layer on Lightning"  # the brief's wording
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
# Batch 52 prerequisite (Dan's published rule, jobs/c3/batch52.yaml part C): every 4th layer; L2-L50 as batch 47's Muse
# sweep (also 52 blocks) and a subset of 51.6's grid; the gate on 60 main-test scenes.
LAYERS4 = tuple(range(2, 51, 4))
N_GATE = 60
PREREQ_RUN = "nem35l_x52_layer"
LAYER_RUN = "nem35l_x52_layer_r2"  # whose committed layer.json the coverage cells read (r2: --gate main)
PREREQ_RULE = ("Batch 52 prerequisite (jobs/c3/batch52.yaml part C, Dan's words): \"the gate passes on 60 main-test scenes; "
               "the layer is fixed by the published rule (earliest layer where both readers switch >= 0.3, sweeping "
               "every 4th layer)\". As computed: the gate = X0's (unedited org accuracy under X0's top-token read >= 0.80 "
               "for both readers) on the first 60 main-test scenes in scene order; the sweep = the whole change at the "
               "bridge word on 60 dev scenes (51.6's split: random.Random(0).sample of the eligible scenes) at L2, L6, ..., "
               "L50; the layer by amendment 1 (PICK_RULE: the earliest layer where both readers' switch rates are >= 0.3 "
               "at relative depth >= 0.25); every swept layer's rates, passing status and the bridge word's lens "
               f"readability recorded; none: \"{NO_LAYER}\" and the column is cancelled")  # fmt: skip
NO_PREDICTION = "no prediction: the layer is a design choice fixed by the published rule (batch 52 addendum)"
MIN_DEPTH = 0.25  # amendment 1: the pick's relative depth l / n_layers (Lightning: 52 blocks -> l >= 13, so L14 on)
PICK_RULE = ("jobs/c3/batch52.yaml amendment_1 (Dan, 29 Oct ~00:50 Paris, before any sweep ran), verbatim: \"earliest "
             "layer passing the gate at relative depth >= 0.25; tie-break = highest lens readability of the bridge "
             "word\". As computed: passing = both readers' whole-change switch rates >= 0.3 on the 60 dev scenes (point "
             "estimates, EPS 1e-9); relative depth = l / 52; readability = the J++ lens readout at the bridge word of "
             "O's and S's lookup prompts, the share of the 120 rows whose own bridge token is its top-1 over the "
             "vocabulary (then the lower median rank); distinct swept layers leave 'earliest' no tie, so the tie-break "
             "is recorded per layer and not used")  # fmt: skip
# r2 (coordinator for Dan, 29 Oct ~01:10 Paris, to be flagged at 02:00, reversible): nem35l_x52_layer failed the
# 60-scene gate (lookup 0.883, recall 0.783) while X0's gate on all 516 scenes passed (0.957 / 0.816); --gate main
# decides on the main test's gate verbatim (X0's: 0.80 per reader on all scenes, >= 150 eligible), the 60-scene gate
# reported beside as a pre-check.
GATES = {"first60": "the gate on the first 60 main-test scenes (X0's read and bar)",
         "main": "the main test's gate verbatim (X0's: unedited org accuracy >= 0.80 for both readers on all main-test "
                 "scenes, >= 150 eligible); the 60-scene gate reported beside as a pre-check"}  # fmt: skip
RULE = ("Step 1 (dev, 60 scenes): the whole change's switch rate per reader by layer, every 2nd layer; the layer is the "
        "earliest where both readers switch >= 0.3. Step 2 (200 scenes disjoint from dev): the main test's three arms "
        "at that layer (whole / without J++ / without a random part of the same share). If no layer passes step 1: "
        f"\"{NO_LAYER}\", no step 2. Q51.6 (ii): the split holds there iff gap >= 0.3 and the lookup's extra loss "
        "<= 0.10 (extra loss = Jdep - Rdep; gap = recall's minus lookup's; point estimates)")  # fmt: skip


# ---- the procedure's pieces (CPU-testable) -------------------------------------------------------------------------


def split_scenes(eligible: list[dict], n_dev: int | None = None, n_test: int | None = None, seed: int = DEV_SEED):
    """(dev, test): dev = n_dev (N_DEV) eligible scenes drawn by random.Random(seed).sample over their indices, kept in
    scene order; test = the first n_test (N_TEST) eligible scenes not in dev, in scene order."""
    n_dev, n_test = N_DEV if n_dev is None else n_dev, N_TEST if n_test is None else n_test
    pick = set(random.Random(seed).sample(range(len(eligible)), min(n_dev, len(eligible))))
    dev = [c for i, c in enumerate(eligible) if i in pick]
    test = [c for i, c in enumerate(eligible) if i not in pick][:n_test]
    return dev, test


def step1_rates(rows: list[dict]) -> dict[int, dict[str, float]]:
    """{layer: {reader: the whole change's switch rate}} from step 1's outcome rows."""
    hits: dict[tuple[int, str], list[int]] = collections.defaultdict(list)
    for r in rows:
        if r["arm"] == "whole":
            hits[(r["layer"], r["reader"])].append(int(r["switched"]))
    out: dict[int, dict[str, float]] = collections.defaultdict(dict)
    for (la, w), v in sorted(hits.items()):
        out[la][w] = sum(v) / len(v)
    return dict(out)


def passing_layers(rates: dict[int, dict[str, float]], bar: float | None = None) -> list[int]:
    """The layers where every reader's rate is >= bar (EPS), in order."""
    bar = SWITCH_MIN if bar is None else bar
    return [la for la in sorted(rates) if set(rates[la]) == set(X.READERS)
            and all(rates[la][w] >= bar - EPS for w in X.READERS)]  # fmt: skip


def pick_layer(rates: dict[int, dict[str, float]]) -> int | None:
    """The rule fixed in advance: the earliest layer where both readers switch >= 0.3; None if none does."""
    ok = passing_layers(rates)
    return ok[0] if ok else None


def step2_parts(jdic, delta, layer: int):
    """X0's parts of Δ [n, d] at the layer: (P_J Δ, R Δ, P_J Δ's share): the 25-atom signed OMP part over jdic and the
    random subspace's part of its share (basis seed 888 + layer), as x0_necessity.run_rendering builds them."""
    import torch

    from scripts import statement_positions as SP

    x = delta.float()
    part = X.fit(jdic, x, X.K_MAIN, "signed")
    share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(x.device)
    return part, SP.random_subspace_part(x, share, basis), share


def step2_result(rows: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """Step 2's numbers on the test scenes: per reader X0's cell (J++ k = 25 signed), the gap on the same bootstrap
    draws (x45m.group_cells), the rule (x45m.holds: gap >= 0.3 and the lookup's extra loss <= 0.10) and X0's 23 Oct
    verdict beside."""
    from scripts import x45m

    mine = [r for r in rows if r["arm"] in X.ARMS]
    scenes = sorted({r["scene"] for r in mine if r["arm"] == "whole"})
    entity = {r["scene"]: r["entity"] for r in mine}
    cells = x45m.group_cells(mine, scenes, entity, n_boot)
    ok, why = x45m.holds(cells)
    return {"n": len(scenes), "cells": cells, "holds": ok, "why": why,
            "x0_verdict": X.verdict(cells["lookup"], cells["recall"]) if cells else "no rows"}  # fmt: skip


# ---- the plan (tokenizer only) --------------------------------------------------------------------------------------


def build(tok) -> tuple[list[dict], dict]:
    """The main test's chat cases on the tokenizer (X0's build_cases, alt cf)."""
    X.ALT, X.RENDERINGS = "cf", (RENDERING,)
    return X.build_cases(tok, SET)


def as_read(decode, case: dict, reader: str, variant: str = "org") -> str:
    """The reader's prompt exactly as the model reads it (the digit's space token appended), the bridge word in ⟦...⟧."""
    from scripts import x6_routes as R

    return R.marked(decode, case["readers"][reader]["ids"][variant] + case["space"], case["pos"])


def stage_plan(smoke_run: str = "nem35l_x45s_smoke_main") -> Path:
    """Tokenizer only: the cases made and dropped, the expected eligibility and split from the 45s smoke's stored
    competence pass (same scenes, same code path; the job recomputes it), layers, arms and reads, 5 rendered prompts."""
    from scripts import x45m

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}: run the plan with BJ_TARGET={TARGET}"
    tok = x45m.tokenizer()
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    cases, counts = build(tok)
    src = X.RESULTS / smoke_run
    comp = X.read_jsonl(src / "competence.jsonl")
    expected: dict[str, Any] = {"source": f"results/x0_necessity/{smoke_run}/competence.jsonl"}
    if comp:
        n_items = X.N_ITEMS
        X.N_ITEMS = len(cases)
        try:
            gate, eligible = X.gate_and_eligible(cases, comp)
        finally:
            X.N_ITEMS = n_items
        dev, test = split_scenes(eligible[RENDERING])
        expected |= {"gate": gate[RENDERING], "eligible": len(eligible[RENDERING]), "dev": len(dev), "test": len(test),
                     "dev_entities": len({c["bridge"] for c in dev}), "test_entities": len({c["bridge"] for c in test}),
                     "dev_scenes": [c["scene"] for c in dev]}  # fmt: skip
    reads1 = expected.get("dev", N_DEV) * len(X.READERS) * (1 + len(LAYERS))
    reads2 = expected.get("test", N_TEST) * len(X.READERS) * len(ARMS2)
    chosen = random.Random(VIEW_SEED).sample(cases, min(N_PROMPTS, len(cases)))
    blob = {"target": pins.TARGET, "run": RUN, "prefix": pins.RUN_PREFIX, "set": SET, "rendering": RENDERING, **counts,
            "domains": dict(collections.Counter(c["domain"] for c in cases)), "expected": expected,
            "layers": list(LAYERS), "n_layers_swept": len(LAYERS), "step2_arms": list(ARMS2),
            "reads": {"step1": reads1, "step2_at_most": reads2, "competence_cases": len(cases)},
            "prompts": [{"scene": c["scene"], "bridge": f"{c['bridge']} -> {c['cf_bridge']}",
                         **{f"{READER_NAME[w]}_O_as_read": as_read(decode, c, w) for w in X.READERS},
                         "lookup_S_as_read": as_read(decode, c, X.LOOKUP, "alt")} for c in chosen]}  # fmt: skip
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan on {pins.TARGET} (tokenizer only): {len(chosen)} rendered prompts (seed {VIEW_SEED}), ⟦…⟧ "
             "the bridge word (where each arm adds its vector)", ""]  # fmt: skip
    for p in blob["prompts"]:
        lines += [f"## {p['scene']} ({p['bridge']})", ""]
        for k, v in p.items():
            if k.endswith("as_read"):
                lines += [f"**{k}**", "", "```", v, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in blob.items() if k != "prompts"}, indent=1, ensure_ascii=False)[:4000])
    print("wrote", out, flush=True)
    return out


# ---- GPU -----------------------------------------------------------------------------------------------------------


def preflight() -> None:
    """Before anything is written: the pinned lens file and the snapshot's weight shards are on this machine (the job
    downloads nothing large; see the spec's notes for the prefetch)."""
    from huggingface_hub import try_to_load_from_cache

    lens = pins.REPO_ROOT / pins.LENS_SOURCES["jpp"][1]
    assert lens.exists(), (f"{lens} is missing: copy it from sesterce-h100x2:~/bridge-jspace/{pins.LENS_SOURCES['jpp'][1]} "
                           "(sha256 3306b6e4..., a local lens with no download source)")  # fmt: skip
    index = try_to_load_from_cache(pins.MODEL_REPO, "model.safetensors.index.json", revision=pins.MODEL_REVISION)
    assert isinstance(index, str), f"{pins.MODEL_REPO}@{pins.MODEL_REVISION[:8]} is not cached: prefetch it first"
    shards = sorted(set(json.loads(Path(index).read_text())["weight_map"].values()))
    missing = [s for s in shards if not isinstance(
        try_to_load_from_cache(pins.MODEL_REPO, s, revision=pins.MODEL_REVISION), str)]  # fmt: skip
    assert not missing, f"{len(missing)} of {len(shards)} weight shards are not cached (e.g. {missing[:2]}): prefetch"


def deltas(model, cases: list[dict], layers: tuple[int, ...]):
    """Δ [n, len(layers), d] fp32 on the CPU: h_S - h_O at the bridge word, one forward of O and of S per case (the
    lookup's prompts; both readers' prompts agree through the bridge word)."""
    import torch

    from bridge_jspace.utils import progress

    rows = []
    for c in progress(cases, "51.6: Δ at the bridge word (case)"):
        ids = c["readers"][X.LOOKUP]["ids"]
        h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=tuple(layers))[1] for v in ("org", "alt")}
        rows.append(torch.stack([(h["alt"][la][c["pos"]] - h["org"][la][c["pos"]]).float().cpu() for la in layers]))
        del h
    return torch.stack(rows)


def base_row(c: dict) -> dict:
    return {"scene": c["scene"], "entity": c["bridge"], "domain": c["domain"], "rendering": RENDERING}


def step1_reads(model, cases: list[dict], layers: tuple[int, ...], delta, digits) -> list[dict]:
    """Per case and reader: O unedited, then the whole change at each layer (one row per layer), X0's chat read."""
    from bridge_jspace.utils import progress
    from scripts.exp04_brew_parts import AddRows

    rows = []
    for i, c in enumerate(progress(cases, f"51.6 step 1: whole change at {len(layers)} layers (case)")):
        edits = [{}] + [
            {la: AddRows(delta[i, li : li + 1].to(model.device), [c["pos"]])} for li, la in enumerate(layers)
        ]
        for w, rd in c["readers"].items():
            logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], None)
            keys = [("none", None), *(("whole", la) for la in layers)]
            rows += [{**base_row(c), "step": 1, "reader": w, "arm": arm, "layer": la, **X.read_row(lg, rd, digits)}
                     for (arm, la), lg in zip(keys, logits, strict=True)]  # fmt: skip
    return rows


def step2_reads(model, lens, cases: list[dict], layer: int, digits) -> tuple[list[dict], list[dict], list[dict]]:
    """X0's three arms (plus the unedited row) at the layer, both readers: outcome rows in X0's format, per case the
    parts' shares, and the example cases' greedy texts (10, seed 0) under each arm."""
    from bridge_jspace.utils import progress
    from scripts.exp04_brew_parts import AddRows
    from scripts.x49_gain import greedy_texts

    delta = deltas(model, cases, (layer,))[:, 0].to(model.device)
    jdic = lens.vectors(layer, model.letter_token_ids())
    part, rand, share = step2_parts(jdic, delta, layer)
    del jdic
    arms = {"whole": delta, "no_part": delta - part, "no_rand": delta - rand}
    rshare = rand.norm(dim=-1) ** 2 / (delta.norm(dim=-1) ** 2).clamp_min(1e-30)
    shares = [{"scene": c["scene"], "layer": layer, "dict": "jpp", "k": X.K_MAIN, "omp": "signed",
               "norm_delta": round(float(delta[i].norm()), 4), "share": round(float(share[i]), 5),
               "rand_share": round(float(rshare[i]), 5)} for i, c in enumerate(cases)]  # fmt: skip
    examples = set(random.Random(X.EXAMPLES_SEED).sample(range(len(cases)), min(X.K_EXAMPLES, len(cases))))
    key = {"none": ("-", 0, "-"), "whole": ("-", 0, "-"), "no_part": ("jpp", X.K_MAIN, "signed"),
           "no_rand": ("jpp", X.K_MAIN, "signed")}  # fmt: skip
    rows, greedy = [], []
    for i, c in enumerate(progress(cases, f"51.6 step 2: three arms at L{layer} (case)")):
        edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in ARMS2[1:]]
        for w, rd in c["readers"].items():
            logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], None)
            rows += [{**base_row(c), "step": 2, "layer": layer, "reader": w, "arm": a,
                      **dict(zip(("dict", "k", "omp"), key[a], strict=True)), **X.read_row(lg, rd, digits)}
                     for a, lg in zip(ARMS2, logits, strict=True)]  # fmt: skip
            if i in examples:
                greedy += [{"scene": c["scene"], "reader": w, "arm": a, "greedy": t}
                           for a, t in zip(ARMS2, greedy_texts(model, rd["ids"]["org"], edits), strict=True)]  # fmt: skip
    return rows, shares, greedy


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts import suite_split as SUITE
    from scripts import x45s

    pins.check_run_name(name)
    assert pins.TARGET == TARGET, f"51.6 runs on {TARGET}, not {pins.TARGET}"
    assert chat.FORMAT == "chat", "51.6 renders X0's chat prompts: run with BJ_FORMAT unset"
    pins.check_lens_layers(LAYERS)
    preflight()
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items = pins.DATA_DIR / "tasks_v2" / SET / "items.jsonl"
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": pins.git_state(), "lens": X.lens_record(),
         "test": TEST, "spec": "jobs/c3/batch51.yaml (51.6)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in (items, SPEC)},
         "set": SET, "rendering": RENDERING, "alt": "cf", "layers": list(LAYERS), "k": X.K_MAIN, "omp": "signed",
         "n": {"dev": N_DEV, "test": N_TEST, "min": X.N_MIN}, "gate": X.GATE, "switch_min": SWITCH_MIN,
         "split_bars": {"gap_min": GAP_MIN, "lookup_max": LOOKUP_MAX, "eps": EPS}, "rule": RULE,
         "scenes": f"X0's eligible main-test scenes (scene order); dev = random.Random({DEV_SEED}).sample of {N_DEV} "
                   f"(kept in scene order); test = the first {N_TEST} eligible not in dev",
         "step1": "Δ_l = h_S - h_O at the bridge word, every layer of LAYERS from one forward of O and one of S; the "
                  "whole Δ_l added at l on O (AddRows); both readers; X0's chat read",
         "step2": "at the picked layer: whole Δ, Δ - P_J Δ (x0_necessity.fit, J++ letter atoms, k 25, signed), Δ - R Δ "
                  "(statement_positions.random_subspace_part at P_J Δ's share, basis seed 888 + L); the unedited row",
         "read": "X0's chat read: O's prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token",
         "kernel": {"repo": x45s.KERNEL_REPO, "expected": KERNEL_REVISION, "how": "loaded_hub_kernels() after the "
                    "competence forwards, against the commit the 45s smoke passed; recorded and flagged, not a stop"},
         "seeds": {"dev_split": DEV_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)",
                   "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "view": VIEW_SEED, "set": 24},
         "n_boot": X.N_BOOT,
         "order": {**X.order_record(), "step1": f"per dev case and reader: the unedited row, then the whole change at "
                   f"each layer of LAYERS in order, in batches of at most {SUITE.BATCH} rows",
                   "step2": f"per test case and reader: {list(ARMS2)}, one batch of {len(ARMS2)} rows"},
         "sealed": f"no verdict in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is the pin
    missing = [la for la in LAYERS if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at {missing}"
    cases, counts = build(model.tokenizer)
    ws = X.whitespace_mask(model)
    digit_list = X.digit_ids(model.tokenizer)
    X.DIGIT_IDS.update(digit_list)
    digits = torch.tensor(digit_list, device=model.device)
    with torch.no_grad():
        comp = X.competence(model, cases, digits, ws)
    n_items = X.N_ITEMS
    X.N_ITEMS = len(cases)  # every eligible scene, then split into dev and test
    try:
        gate, eligible = X.gate_and_eligible(cases, comp)
    finally:
        X.N_ITEMS = n_items
    dev, test = split_scenes(eligible[RENDERING])
    tested = bool(eligible[RENDERING])
    kernels = loaded_hub_kernels()
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    (out / "gate.json").write_text(json.dumps({
        "counts": counts, "gate": gate[RENDERING], "tested": tested, "eligible": len(eligible[RENDERING]),
        "dev": [c["scene"] for c in dev], "test": [c["scene"] for c in test], "hub_kernels": kernels,
        "kernel_check": x45s.kernel_revision_check(kernels, KERNEL_REVISION)}, indent=2) + "\n")  # fmt: skip
    print(json.dumps(gate[RENDERING], indent=2), flush=True)
    if not tested:
        (out / "step1.json").write_text(json.dumps({"status": "not tested", "why": "X0's gate fixed in advance "
                                                    "(0.80 per reader, >= 150 eligible) did not pass"}) + "\n")  # fmt: skip
        print("the gate fixed in advance did not pass: not tested; see gate.json", flush=True)
        return out

    with torch.no_grad():
        rows1 = step1_reads(model, dev, LAYERS, deltas(model, dev, LAYERS), digits)
    X.write_jsonl(out / "step1_outcomes.jsonl", rows1)
    rates = step1_rates(rows1)
    layer = pick_layer(rates)
    (out / "step1.json").write_text(json.dumps({
        "status": "done", "n": len(dev), "layers": list(LAYERS), "rates": {str(k): v for k, v in rates.items()},
        "layer": layer, "rule": f"the earliest layer where both readers switch >= {SWITCH_MIN} (EPS {EPS})"},
        indent=2) + "\n")  # fmt: skip
    print(f"step 1: {len(rows1)} reads on {len(dev)} dev scenes; layer {layer}", flush=True)
    if layer is None:
        (out / "step2.json").write_text(json.dumps({"status": "no layer passes step 1", "label": NO_LAYER}) + "\n")
        print("no layer passes step 1: no step 2", flush=True)
        return out
    if len(test) < X.N_MIN:
        (out / "step2.json").write_text(json.dumps({"status": "not tested", "layer": layer,
                                                    "why": f"{len(test)} test scenes, fewer than {X.N_MIN}"}) + "\n")  # fmt: skip
        return out
    with torch.no_grad():
        rows2, shares, greedy = step2_reads(model, lens, test, layer, digits)
    X.write_jsonl(out / "step2_outcomes.jsonl", rows2)
    X.write_jsonl(out / "step2_shares.jsonl", shares)
    X.write_jsonl(out / "step2_examples.jsonl", greedy)
    (out / "step2.json").write_text(json.dumps({"status": "done", "layer": layer, "n": len(test)}) + "\n")
    print(
        f"wrote {out}: step 2 at L{layer}, {len(rows2)} reads of {len(test)} test scenes (sealed: no verdict)",
        flush=True,
    )
    return out


# ---- batch 52: the prerequisite (the gate on 60 scenes and the layer, before any scored run) -------------------------


def gate_first(cases: list[dict], comp: list[dict], n: int | None = None) -> dict:
    """The prerequisite's gate: X0's gate (unedited org accuracy under the decisive read >= X0.GATE, both readers) on the
    first n (N_GATE) cases in scene order; fewer than n cases fails."""
    n = N_GATE if n is None else n
    first = cases[:n]
    right = {(r["scene"], r["rendering"], r["reader"], r["variant"]): r for r in comp}
    acc = X.org_rate(right, first, RENDERING, "read_right")
    return {"cases": len(first), "n_required": n, "scenes": [c["scene"] for c in first], "org_accuracy": acc,
            "said_accuracy": X.org_rate(right, first, RENDERING, "right"), "bar": X.GATE,
            "pass": len(first) == n and bool(acc) and all(a >= X.GATE for a in acc.values())}  # fmt: skip


def readability(model, lens, cases: list[dict], layers: tuple[int, ...]) -> dict[int, dict]:
    """Amendment 1's tie-break measure, per layer: the J++ lens readout (lens.readout, full vocabulary) at the bridge
    word of O's and of S's lookup prompt, each scored on its own bridge token: the share of the 2n rows where that
    token is the lens's top-1, the share in the top 5, and the median rank (1 = top). Unedited forwards only."""
    import torch

    ranks: dict[int, list[int]] = {la: [] for la in layers}
    with torch.no_grad():
        for c in cases:
            ids = c["readers"][X.LOOKUP]["ids"]
            for v in ("org", "alt"):
                tok = int(ids[v][c["pos"]])
                rec = model.run(torch.tensor([ids[v]], device=model.device), record=tuple(layers))[1]
                for la in layers:
                    lg = lens.readout(rec[la][c["pos"]].float()[None], la)[0].float()
                    ranks[la].append(int((lg > lg[tok]).sum()) + 1)
    return {la: {"n": len(r), "top1": float(np.mean([x == 1 for x in r])), "top5": float(np.mean([x <= 5 for x in r])),
                 "median_rank": float(np.median(r))} for la, r in ranks.items()}  # fmt: skip


def pick_layer_a1(rates: dict[int, dict[str, float]], read: dict[int, dict], n_layers: int) -> int | None:
    """Amendment 1 (Dan ~00:50, before any sweep): the earliest layer passing (both readers >= 0.3) at relative depth
    l / n_layers >= 0.25; tie-break = the highest lens readability of the bridge word (top-1 share, then the lower
    median rank). Swept layers are distinct, so 'earliest' leaves no tie and the tie-break is recorded, not used."""
    ok = [la for la in passing_layers(rates) if la / n_layers >= MIN_DEPTH - EPS]
    if not ok:
        return None
    tied = [la for la in ok if la == min(ok)]
    return max(tied, key=lambda la: (read[la]["top1"], -read[la]["median_rank"]))


def layer_record(rows: list[dict], read: dict[int, dict], n_layers: int, n_boot: int = X.N_BOOT) -> dict:
    """layer.json's body: per swept layer the rates with cluster-bootstrap CIs, whether both readers pass, whether its
    relative depth is >= 0.25, the bridge word's lens readability; every candidate; amendment 1's pick."""
    rates = step1_rates(rows)
    layer = pick_layer_a1(rates, read, n_layers)
    passing = passing_layers(rates)
    cand = [la for la in passing if la / n_layers >= MIN_DEPTH - EPS]
    ci = step1_numbers(rows, n_boot)
    per = {str(la): {"depth": round(la / n_layers, 4), "passes": la in passing, "deep_enough": la / n_layers >= MIN_DEPTH - EPS,
                     "candidate": la in cand, **{READER_NAME[w]: ci[la][w] for w in X.READERS},
                     "readability": read.get(la)} for la in sorted(rates)}  # fmt: skip
    label = f"L{layer}" if layer is not None else (NO_LAYER if not passing else
                                                   f"{NO_LAYER} at relative depth >= {MIN_DEPTH}")  # fmt: skip
    return {"status": "done" if layer is not None else "no layer passes", "layer": layer, "label": label,
            "rule": PICK_RULE, "n_layers": n_layers, "passing_layers": passing, "candidates": cand,
            "rates": {str(k): {READER_NAME[w]: v[w] for w in X.READERS} for k, v in rates.items()},
            "rates_ci": {str(k): {READER_NAME[w]: v[w] for w in X.READERS} for k, v in ci.items()},
            "per_layer": per}  # fmt: skip


def committed_layer(run: str = LAYER_RUN, rev: str = "HEAD") -> int:
    """Lightning's layer for the batch 52 coverage cells: layer.json of the prerequisite run, as committed at `rev`
    (refuses if it is not committed or no layer passed)."""
    path = f"results/{EXP}/{run}/layer.json"
    got = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=pins.REPO_ROOT, capture_output=True, text=True)
    assert got.returncode == 0, f"{path} is not committed at {rev}: the layer must be committed before any scored run"
    rec = json.loads(got.stdout)
    assert rec.get("layer") is not None, f"{path}: {rec.get('status')} ({rec.get('label')}); the column is cancelled"
    return int(rec["layer"])


def gate_passes(gate_mode: str, g60: dict, g: dict) -> bool:
    """The prerequisite's gate decision: the 60-scene gate (first60), or X0's all-scene gate and n (main)."""
    assert gate_mode in GATES, gate_mode
    return bool(g60["pass"]) if gate_mode == "first60" else bool(g.get("pass") and g.get("enough"))


def prereq_md(rec: dict, gate: dict) -> list[str]:
    g60, g = gate["gate60"], gate["gate"]
    mode = gate.get("prereq_gate", "first60")
    decides = {"first60": ("decides", "beside"), "main": ("beside, a pre-check", "decides")}[mode]
    lines = ["# Batch 52 prerequisite: Lightning's layer (dev set, the published rule)", "",
             f"{NO_PREDICTION}. Model {TARGET}. UNVERIFIED.", "", f"Rule: {PREREQ_RULE}.", "",
             f"Gate ({mode}): {GATES[mode]}.", "",
             f"Gate on the first {g60['cases']} main-test scenes ({decides[0]}): org accuracy {g60['org_accuracy']} "
             f"(bar {g60['bar']}) -> **{'pass' if g60['pass'] else 'FAIL'}**. X0's gate on all {g.get('cases')} "
             f"scenes ({decides[1]}): {g.get('org_accuracy')}, pass {g.get('pass')}; eligible {gate['eligible']}; dev "
             f"{len(gate['dev'])}, test (for the coverage runs) {len(gate['test'])}.", "",
             f"**Layer: {rec.get('label')}**", ""]  # fmt: skip
    if rec.get("per_layer"):
        lines += [f"Pick rule: {rec['rule']}.", "", f"Every passing layer: {rec['passing_layers']}; candidates "
                  f"(relative depth >= {MIN_DEPTH}): {rec['candidates']}.", "",
                  "| layer | depth | lookup switch [CI] | recall switch [CI] | both >= 0.3 | depth >= 0.25 | lens top-1 "
                  "(bridge word) | median rank |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for la, v in rec["per_layer"].items():
            r = v.get("readability") or {}
            lines.append(f"| L{la}{' (pick)' if int(la) == rec.get('layer') else ''} | {v['depth']:.2f} | "
                         f"{fmt(v['lookup'])} | {fmt(v['recall'])} | {'yes' if v['passes'] else ''} | "
                         f"{'yes' if v['deep_enough'] else ''} | {r.get('top1', float('nan')):.2f} | "
                         f"{r.get('median_rank', float('nan')):g} |")  # fmt: skip
        lines += ["", "The conflict result at every swept layer comes from the Lightning conflict-test run (all 13 "
                  "layers, deciding at the pick), not from this sweep."]  # fmt: skip
    return lines


def stage_prereq(name: str, why: str, n_boot: int = X.N_BOOT, gate_mode: str = "first60") -> Path:
    """Batch 52's prerequisite on Lightning: X0's competence on every main-test scene, the gate on the first 60, X0's
    gate and eligibility, 51.6's dev / test split, then step 1 alone at every 4th layer on the dev scenes; writes
    gate.json, step1_outcomes.jsonl, layer.json and prereq.md (no step 2, no verdict). gate_mode (GATES) picks the
    gate that decides: the 60-scene gate (first60, the default) or the main test's gate verbatim (main)."""
    assert gate_mode in GATES, f"gate {gate_mode!r}: not one of {sorted(GATES)}"
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts import suite_split as SUITE
    from scripts import x45s

    pins.check_run_name(name)
    assert pins.TARGET == TARGET, f"the prerequisite runs on {TARGET}, not {pins.TARGET}"
    assert chat.FORMAT == "chat", "X0's chat prompts: run with BJ_FORMAT unset"
    pins.check_lens_layers(LAYERS4)
    preflight()
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items = pins.DATA_DIR / "tasks_v2" / SET / "items.jsonl"
    spec52 = pins.REPO_ROOT / "jobs" / "c3" / "batch52.yaml"
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": pins.git_state(), "lens": X.lens_record(),
         "batch": 52, "spec": "jobs/c3/batch52.yaml (part C, prerequisites for a new family)", "question": NO_PREDICTION,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in (items, spec52)},
         "set": SET, "rendering": RENDERING, "alt": "cf", "layers": list(LAYERS4), "n_gate": N_GATE,
         "n": {"dev": N_DEV, "test": N_TEST, "min": X.N_MIN}, "gate": X.GATE, "switch_min": SWITCH_MIN, "eps": EPS,
         "rule": PREREQ_RULE, "prereq_gate": {"mode": gate_mode, "text": GATES[gate_mode]},
         "scenes": f"gate: the first {N_GATE} main-test scenes in scene order; sweep: X0's eligible scenes (scene order), "
                   f"dev = random.Random({DEV_SEED}).sample of {N_DEV} (51.6's split); test = the first {N_TEST} "
                   "eligible not in dev (recorded for the coverage runs, not read here)",
         "step1": "Δ_l = h_S - h_O at the bridge word, every layer of LAYERS4 from one forward of O and one of S; the "
                  "whole Δ_l added at l on O (AddRows); both readers; X0's chat read",
         "kernel": {"repo": x45s.KERNEL_REPO, "expected": KERNEL_REVISION},
         "seeds": {"dev_split": DEV_SEED, "bootstrap": X.BOOT_SEED, "set": 24}, "n_boot": n_boot,
         "order": {**X.order_record(), "step1": f"per dev case and reader: the unedited row, then the whole change at "
                   f"each layer of LAYERS4 in order, in batches of at most {SUITE.BATCH} rows"}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is the pin
    missing = [la for la in LAYERS4 if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at {missing}"
    cases, counts = build(model.tokenizer)
    ws = X.whitespace_mask(model)
    digit_list = X.digit_ids(model.tokenizer)
    X.DIGIT_IDS.update(digit_list)
    digits = torch.tensor(digit_list, device=model.device)
    with torch.no_grad():
        comp = X.competence(model, cases, digits, ws)
    g60 = gate_first(cases, comp)
    n_items = X.N_ITEMS
    X.N_ITEMS = len(cases)
    try:
        gate, eligible = X.gate_and_eligible(cases, comp)
    finally:
        X.N_ITEMS = n_items
    gate_ok = gate_passes(gate_mode, g60, gate[RENDERING])
    dev, test = split_scenes(eligible[RENDERING]) if gate_ok else ([], [])
    kernels = loaded_hub_kernels()
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    gate_blob = {"counts": counts, "prereq_gate": gate_mode, "gate_passes": gate_ok, "gate60": g60,
                 "gate": gate[RENDERING], "eligible": len(eligible[RENDERING]),
                 "dev": [c["scene"] for c in dev], "test": [c["scene"] for c in test], "hub_kernels": kernels,
                 "kernel_check": x45s.kernel_revision_check(kernels, KERNEL_REVISION)}  # fmt: skip
    (out / "gate.json").write_text(json.dumps(gate_blob, indent=2) + "\n")
    print(json.dumps({"gate60": g60["org_accuracy"], "gate": gate[RENDERING]["org_accuracy"]}), flush=True)
    if not gate_ok or len(dev) < N_DEV:
        failed = {"first60": "the gate on the first 60 main-test scenes failed",
                  "main": "the main test's gate (X0's, all scenes, >= 150 eligible) failed"}[gate_mode]  # fmt: skip
        why_not = failed if not gate_ok else f"{len(dev)} dev scenes, fewer than {N_DEV} (X0's gate or eligibility)"
        rec = {"status": "prerequisite failed", "layer": None, "label": f"prerequisite failed: {why_not}"}
    else:
        with torch.no_grad():
            rows1 = step1_reads(model, dev, LAYERS4, deltas(model, dev, LAYERS4), digits)
        X.write_jsonl(out / "step1_outcomes.jsonl", rows1)
        read = readability(model, lens, dev, LAYERS4)
        rec = layer_record(rows1, read, pins.TARGETS[pins.TARGET]["n_layers"], n_boot)
    rec |= {"n_dev": len(dev), "layers": list(LAYERS4), "rule": PREREQ_RULE, "prediction": NO_PREDICTION,
            "prereq_gate": gate_mode, "gate60_pass": g60["pass"], "main_gate_pass": bool(gate[RENDERING]["pass"])}  # fmt: skip
    (out / "layer.json").write_text(json.dumps(rec, indent=2) + "\n")
    (out / "prereq.md").write_text("\n".join(prereq_md(rec, gate_blob)) + "\n")
    print(f"wrote {out}: {rec['label']}", flush=True)
    return out


# ---- verdict and view (CPU, sealed) --------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.6 (the 'Dan:' / 'Dan (<model>):' lines of its block, with '- ' continuations, in
    the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def read_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def step1_numbers(rows: list[dict], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict[int, dict[str, list]]:
    """Per layer and reader: the whole change's switch rate with a 95% cluster-bootstrap CI over the bridge items."""
    out: dict[int, dict[str, list]] = {}
    for la in sorted({r["layer"] for r in rows if r["arm"] == "whole"}):
        out[la] = {}
        for w in X.READERS:
            mine = [r for r in rows if r["arm"] == "whole" and r["layer"] == la and r["reader"] == w]
            sw, ents = [int(r["switched"]) for r in mine], [r["entity"] for r in mine]
            boot = X.resampled_rates({"whole": sw}, ents, n_boot, seed)["whole"]
            out[la][w] = [float(np.mean(sw)), *X.interval(boot)]
    return out


def result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """The run's outcome: pending, not tested (gate / n), no layer passes step 1, or step 2's split at the layer."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"run": run, "status": "pending", "label": "pending", "why": "no manifest here"}
    m = read_json(src / "manifest.json")
    assert m["model"]["target"] == TARGET, f"{run} is a {m['model']['target']} run, not {TARGET}'s"
    gate, s1, s2 = (read_json(src / f) for f in ("gate.json", "step1.json", "step2.json"))
    base = {"run": run, "gate": gate.get("gate"), "eligible": gate.get("eligible"), "counts": gate.get("counts"),
            "kernel_check": gate.get("kernel_check")}  # fmt: skip
    if not gate.get("tested", False):
        why = s1.get("why") or "the run has no gate.json yet"
        return {**base, "status": "not tested" if gate else "pending", "label": "not tested" if gate else "pending",
                "why": why}  # fmt: skip
    if s1.get("status") != "done":
        return {**base, "status": "pending", "label": "pending", "why": "step 1 did not finish"}
    rows1 = X.read_jsonl(src / "step1_outcomes.jsonl")
    rates = step1_rates(rows1)
    layer = pick_layer(rates)
    assert layer == s1["layer"], f"{run}: step1.json picked {s1['layer']}, the rows give {layer}"
    one = {**base, "n_dev": s1["n"], "step1": step1_numbers(rows1, n_boot), "layer": layer,
           "passing_layers": passing_layers(rates), "q51_6_i": "yes" if layer is not None else "no"}  # fmt: skip
    if layer is None:
        return {**one, "status": "no layer passes step 1", "label": f"no layer passes step 1: {NO_LAYER}"}
    if s2.get("status") != "done":
        st = s2.get("status", "pending")
        return {**one, "status": st, "label": st, "why": s2.get("why", "step 2 did not finish")}
    rows2 = X.read_jsonl(src / "step2_outcomes.jsonl")
    res = step2_result(rows2, n_boot)
    none = {READER_NAME[w]: sum(r["role"] == "A" for r in rows2 if r["arm"] == "none" and r["reader"] == w)
            for w in X.READERS}  # fmt: skip
    shares = X.read_jsonl(src / "step2_shares.jsonl")
    label = f"L{layer}: the split holds" if res["holds"] else f"L{layer}: the split does not hold"
    return {**one, "status": "tested", "label": label, "n_test": res["n"], "step2": res,
            "q51_6_ii": "yes" if res["holds"] else "no", "none_reads_O": none,
            "share_median": float(np.median([s["share"] for s in shares])) if shares else None}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None or v[0] is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def verdict_lines(r: dict, answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.6: Lightning, the main test", "",
             f"Batch 51, test 51.6 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). Model {TARGET}, run {r['run']}. "
             "Main-test scenes (two people swap picks; d1_topics_v3, chat), X0's gate, eligibility and chat read. "
             f"Cluster bootstrap over the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}.", "", f"**Label: {r['label']}**", ""]  # fmt: skip
    if r["status"] in ("pending", "not tested"):
        return [*lines, f"Why: {r.get('why')}", "", f"Gate: {r.get('gate')}"]
    g = r["gate"]
    lines += [f"Gate (all {g['cases']} scenes): org accuracy {g['org_accuracy']} (bar {X.GATE}), eligible "
              f"{r['eligible']}; dev n = {r['n_dev']}. Kernel: {r['kernel_check']}.", "",
              f"Q51.6 (i) a layer passes step 1: **{r['q51_6_i']}**"
              + (f" (L{r['layer']}); every passing layer: {r['passing_layers']} (descriptive beside the rule: the last "
                 f"is L{r['passing_layers'][-1]})" if r["layer"] is not None else ""), "",
              "Step 1 (dev): the whole change's switch rate by layer", "", "| layer | lookup | recall | both >= 0.3 |",
              "|---|---|---|---|"]  # fmt: skip
    for la, v in r["step1"].items():
        both = all(v[w][0] >= SWITCH_MIN - EPS for w in X.READERS)
        lines.append(f"| L{la} | {fmt(v[X.LOOKUP])} | {fmt(v[X.RECALL])} | {'yes' if both else ''} |")
    if r["status"] != "tested":
        return [*lines, "", f"Step 2: {r['status']} ({r.get('why', r['label'])})."]
    s = r["step2"]
    c = s["cells"]
    lines += ["", f"Step 2 (test, n = {r['n_test']}, {c['lookup']['entities']} bridge items) at L{r['layer']}: "
              f"Q51.6 (ii) the split holds: **{r['q51_6_ii']}** ({s['why']}); X0's 23 Oct verdict beside: "
              f"{s['x0_verdict']}.", "",
              "| reader | S_whole | S_no J++ | S_no random | Jdep | Rdep | extra loss | X0 valid |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in ("lookup", "recall"):
        x = c[w]
        lines.append(f"| {w} | {fmt(x['S_whole'])} | {fmt(x['S_no_part'])} | {fmt(x['S_no_rand'])} | {fmt(x['Jdep'])} | "
                     f"{fmt(x['Rdep'])} | {fmt(x['excess'])} | {x['valid']} ({x['switched_whole']} switched) |")  # fmt: skip
    lines += ["", f"Gap (recall's extra loss minus the lookup's): {fmt(c['gap'])}.",
              f"O unedited reads O's answer: lookup {r['none_reads_O']['lookup']}, recall {r['none_reads_O']['recall']} "
              f"of {r['n_test']}. Median share of ||Δ||^2 in the J++ part: {r['share_median']:.4g}.", "",
              "S_x are Wilson intervals; Jdep, Rdep, extra loss and gap cluster-bootstrap intervals (paired draws)."]  # fmt: skip
    return lines


def stage_verdict(run: str = RUN, n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    r = result(run, n_boot)
    out = RESULTS / f"x51_6-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(r, answer, n_boot)
    (out / "verdict.json").write_text(json.dumps({"dan": answer, "rule": RULE, "result": r}, indent=1,
                                                 ensure_ascii=False, default=str) + "\n")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def row_table(rows: list[dict], decode, k: int = N_ROWS, seed: int = VIEW_SEED) -> list[str]:
    """k random rows (seed) as a markdown table: scene, reader, layer, the answers, the top token read, switched."""
    pick = sorted(random.Random(seed).sample(range(len(rows)), min(k, len(rows))))
    out = [
        "| scene | reader | layer | top token | role | switched | p_org | p_alt |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i in pick:
        r = rows[i]
        out.append(f"| {r['scene']} | {READER_NAME[r['reader']]} | {r['layer']} | {decode([r['top']])!r} | {r['role']} | "
                   f"{r['switched']} | {r['p_org']} | {r['p_alt']} |")  # fmt: skip
    return out


def stage_view(run: str = RUN, decode=None) -> Path:
    """The verify pack: 5 rendered test prompts (seed 0; dev if no step 2) with the bridge word marked, and 10 random
    rows (seed 0) per arm: step 1's whole change (pooled over layers) and step 2's four arms."""
    from scripts import x47_atoms as A

    answer = unsealed()
    src = RESULTS / run
    decode = decode or A.default_decode(TARGET)
    gate = read_json(src / "gate.json")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    scenes = gate.get("test") or gate.get("dev") or sorted(cases)
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = [f"# 51.6 verify pack: {run} (Dan: {answer}). UNVERIFIED.", "",
             "O's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, "
             "where each arm adds its vector.", ""]  # fmt: skip
    for s in random.Random(VIEW_SEED).sample(scenes, min(N_PROMPTS, len(scenes))):
        c = cases[s]
        lines += [f"## {s} ({c['domain']}): {c['bridge']} (O) → {c['cf_bridge']} (S), token {c['pos']}", ""]
        for w, rd in c["readers"].items():
            lines += [f"**{READER_NAME[w]}**: O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "", "```",
                      as_read(decode, c, w), "```", ""]  # fmt: skip
    rows1 = [r for r in X.read_jsonl(src / "step1_outcomes.jsonl") if r["arm"] == "whole"]
    if rows1:
        lines += ["## Step 1: the whole change (all layers pooled), 10 random rows", "", *row_table(rows1, decode), ""]
    rows2 = X.read_jsonl(src / "step2_outcomes.jsonl")
    for a in ARMS2 if rows2 else ():
        lines += [
            f"## Step 2: arm {a}, 10 random rows",
            "",
            *row_table([r for r in rows2 if r["arm"] == a], decode),
            "",
        ]
    greedy = X.read_jsonl(src / "step2_examples.jsonl")
    if greedy:
        lines += ["## Step 2: greedy texts of the example scenes (seed 0)", "", "| scene | reader | arm | greedy |",
                  "|---|---|---|---|", *(f"| {g['scene']} | {READER_NAME[g['reader']]} | {g['arm']} | {g['greedy']!r} |"
                                         for g in greedy)]  # fmt: skip
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "prereq", "layer", "verdict", "view"])
    ap.add_argument("--name", default=None, help="run / prereq / verdict / view: results/x51_lightning/<name>/")
    ap.add_argument(
        "--why", default="batch 51, test 51.6 (jobs/c3/batch51.yaml; Q51.6): Lightning, the main test; sealed"
    )
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--gate", choices=sorted(GATES), default="first60",
                    help="prereq: the gate that decides (first60: the first 60 scenes; main: the main test's, verbatim)")  # fmt: skip
    a = ap.parse_args()
    a.name = a.name or (PREREQ_RUN if a.stage == "prereq" else RUN)
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        stage_run(a.name, a.why)
    elif a.stage == "prereq":
        stage_prereq(a.name, a.why, a.n_boot, a.gate)
    elif a.stage == "layer":  # batch 52: the committed layer, alone on stdout (the coverage specs' BJ_PREDICTED_LAYER)
        print(committed_layer(a.name if a.name != RUN else LAYER_RUN))
    elif a.stage == "verdict":
        stage_verdict(a.name, a.n_boot)
    else:
        stage_view(a.name)


if __name__ == "__main__":
    main()
