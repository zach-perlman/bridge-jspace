"""x47_zero (batch 47, test 47.5; jobs/c3/batch47.yaml, design and rule fixed in advance; Q47.5 in
predictions/2026-10-28_dan.md): followed or needed, one-layer zeroing. "Without the J++ part" (X0) is a conflict test:
the J++ part says the old item, the rest of the change the new one. Whether the recall needs that part is Zach's
zeroing: take it out of the changed prompt itself.

Scenes: the main test (two people swap picks; d1_topics_v3, chat), X0's gate (0.80 per reader on O unedited, >= 150
eligible) and eligibility (both readers say and read O's and S's answers right), the first 200 eligible in scene order.
S = the changed prompt. At the bridge word and layer l, Δ_l = h_S - h_O; its 25 signed-OMP atoms over the J++ lens's
letter-token atoms at l (X0's OMP: x0_parts.omp_atoms, the k = 25 picks of x0_necessity.fit). Arms, all on S, read by
X0's chat read (the prompt with a digit's space token appended), both readers:
  none     S unedited
  zero_L   at L: S's state at the bridge word minus its projection on the span of Δ_L's 25 atoms
  rand_L   at L: minus its projection on the first k columns of X0's random basis (seed 888 + L), k per item so that
           the projection's share of ||h_S||^2 matches the atoms' (statement_positions.random_subspace_part's rule)
  zero_L3  zero_L's edit at L, L+1, L+2 and L+3 in one forward, each layer with its own lens, Δ_l and OMP (the edit
           acts on the state as it arrives, so above L on the state already edited below)
  rand_L3  rand_L's edit at the four layers (seed 888 + l, k from S's clean state at l)
Kept = the top token is S's answer's first token. Per item in norms.jsonl and per layer: ||h_S||, ||Δ||, the atoms'
share of ||h_S||^2 and of ||Δ||^2, the random part's k and achieved share.

Rule (stage verdict; fixed in advance, as computed in the job specs): on the recall at L, "followed, not needed at one
layer" if it keeps >= 0.80 of its answers under the zeroing and |kept(zero_L) - kept(rand_L)| <= 0.10; "needed" if
kept(rand_L) - kept(zero_L) >= 0.30; else neither. The lookup and L..L+3 reported beside (the same numbers,
descriptive). The README's verb for the main test becomes "follows / reads" unless "needed" holds on all three models
(9B, 27B, Muse). Point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the bridge items (10,000,
seed 0) beside them.

SEALED: the jobs write per-item outputs only; verdict refuses until predictions/2026-10-28_dan.md holds Dan's Q47.5
answer at the committed HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x47_zero.py run --name qwen35_9b_x47_5      # GPU (sealed)
uv run python scripts/x47_zero.py verdict                                                # CPU, after Dan's Q47.5
"""

from __future__ import annotations

import argparse
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
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_atoms as A

EXP = "x47_zero"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml"
QUESTION = "Q47.5"
SET = "d1_topics_v3"
RENDERING = "chat"
SPAN = 4  # L..L+3
K = X.K_MAIN
ARMS = ("none", "zero_L", "rand_L", "zero_L3", "rand_L3")
ARM_TEXT = {
    "none": "S unedited",
    "zero_L": "at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms",
    "rand_L": "at L, without its projection on a random subspace of the same share of ||h_S||^2",
    "zero_L3": "the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP)",
    "rand_L3": "the random subspace of the same share at L..L+3",
}
PAIRS = (("L", "zero_L", "rand_L"), ("L..L+3", "zero_L3", "rand_L3"))
DECISIVE = "L"  # one layer, the recall
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_5", "qwen3.6-27b": "x47_5_27b", "muse-glimmer-30b": "muse30_x47_5"}
# batch 52 C coverage (amendment 2: the full grid on Lightning; jobs/c3/x52_lightning_zero.yaml): read by verdict
# --coverage alone (MODELS / RUNS and the design's own verdict unchanged); the run takes --exclude-dev (Lightning's 60
# dev scenes, which chose its layer, stay out of the items, as in its conflict run)
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_zero"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x47_zero/x47_5-20261028T113106Z"  # 47.5's rule first scored (9B, 27B, Muse)
KEEP_FOLLOWED, NEAR, NEEDED = 0.80, 0.10, 0.30
EPS = 1e-9  # a value exactly at a bar counts as at the bar
FOLLOWED, NEEDS, NEITHER = "followed, not needed at one layer", "needed", "neither (between the bars)"
RULE = ('"followed, not needed at one layer" if the recall keeps >= 0.80 of its answers under the zeroing, within 0.10 '
        'of the random arm; "needed" if it loses >= 0.30 beyond random. The lookup reported beside. Whatever the result, '
        'the README\'s verb for the main test becomes "follows / reads" unless "needed" holds on all three')  # fmt: skip
READER_NAME = A.READER_NAME


class ProjectOut:
    """Edit for one layer: at the given positions, the state minus its projection on the span of `basis`'s columns
    ([d, r], orthonormal): h <- h - (h Q) Q^T, on the state as it arrives (after any edit at an earlier layer)."""

    def __init__(self, basis, positions: list[int]):
        self.basis, self.positions = basis, positions

    def __call__(self, h):
        q = self.basis.to(h.device, h.dtype)
        out = h.clone()
        rows = h[self.positions]
        out[self.positions] = rows - (rows @ q) @ q.T
        return out


# ---- the parts (CPU-testable) ---------------------------------------------------------------------------------------


def atom_bases(jdic, delta, k: int = K) -> tuple[list, Any]:
    """Per row of delta [n, d] (Δ at one layer): an orthonormal basis [d, r] (float32, r <= k) of the span of its k
    signed-OMP atoms over jdic (x0_parts.omp_atoms: X0's picks), and the atoms [n, k]."""
    from scripts import x0_parts as XP

    atoms = XP.omp_atoms(jdic, delta, k)
    return [R.orthonormal(jdic[atoms[i]].T).float() for i in range(delta.shape[0])], atoms


def share_in(h, q) -> float:
    """||Q^T h||^2 / ||h||^2 for one row h [d] and an orthonormal basis Q [d, r]."""
    return float((q.T.double() @ h.double()).norm() ** 2 / (h.double().norm() ** 2).clamp_min(1e-30))


def layer_parts(jdic, h_s, h_o, basis, k: int = K) -> tuple[list, list[int], list[dict]]:
    """One layer's zeroing for every item: h_s, h_o [n, d] (the bridge word's clean states in S and O). Returns each
    item's atom basis (Δ = h_s - h_o, atom_bases), the random basis's column count k (random_k: the first k columns
    of `basis` hold the same share of ||h_s||^2 as the atoms' span), and per item the norms and shares."""
    import torch

    q, _ = atom_bases(jdic, (h_s - h_o).float(), k)
    share = torch.tensor([share_in(h_s[i], q[i]) for i in range(h_s.shape[0])], device=h_s.device)
    ks = [int(v) for v in R.random_k(h_s.float(), share, basis)]
    recs = [{"norm_hS": round(float(h_s[i].norm()), 4), "norm_delta": round(float((h_s[i] - h_o[i]).norm()), 4),
             "share_hS_atoms": round(float(share[i]), 6), "share_delta_atoms": round(share_in(h_s[i] - h_o[i], q[i]), 6),
             "atoms_rank": int(q[i].shape[1]), "k_rand": ks[i], "share_hS_rand": round(share_in(h_s[i], basis[:, : ks[i]]), 6)}
            for i in range(h_s.shape[0])]  # fmt: skip
    return q, ks, recs


def edit_sets(layers: tuple[int, ...], pos: int, q: dict[int, Any], bases: dict[int, Any], ks: dict[int, int]) -> dict:
    """Each arm's edit set ({layer: ProjectOut}) for one item, in ARMS order: q[l] its atom basis at layer l, bases[l]
    the layer's random basis and ks[l] its column count for the item."""
    first = layers[0]

    def rand(la: int) -> ProjectOut:
        return ProjectOut(bases[la][:, : ks[la]], [pos])

    out = {"none": {}, "zero_L": {first: ProjectOut(q[first], [pos])}, "rand_L": {first: rand(first)},
           "zero_L3": {la: ProjectOut(q[la], [pos]) for la in layers}, "rand_L3": {la: rand(la) for la in layers}}  # fmt: skip
    assert tuple(out) == ARMS
    return out


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


# ---- GPU ------------------------------------------------------------------------------------------------------------


def run_items(model, lens, items: list[dict], layers: tuple[int, ...], ws, digits) -> tuple[list, list, list]:
    """The zeroing arms on each item's S prompt, both readers: (outcome rows, per-item norms, greedy texts of the
    example items). States: one forward of O and of S per item (the lookup's prompt; both readers' prompts agree up to
    the bridge word), recorded at every layer of `layers`."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP

    dev = model.device
    letters = model.letter_token_ids()
    h = {"org": {la: [] for la in layers}, "alt": {la: [] for la in layers}}
    for c in progress(items, "47.5: states at the bridge word (item)"):
        ids = c["readers"][X.LOOKUP]["ids"]
        for v in ("org", "alt"):
            rec = model.run(torch.tensor([ids[v]], device=dev), record=layers)[1]
            for la in layers:
                h[v][la].append(rec[la][c["pos"]].float())
    q: dict[int, list] = {}
    ks: dict[int, list[int]] = {}
    bases, recs = {}, [[] for _ in items]
    for la in layers:
        hs, ho = torch.stack(h["alt"][la]).to(dev), torch.stack(h["org"][la]).to(dev)
        bases[la] = SP.random_basis(hs.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
        jdic = lens.vectors(la, letters)
        q[la], ks[la], per = layer_parts(jdic, hs, ho, bases[la])
        q[la] = [b.cpu() for b in q[la]]
        del jdic
        for i, r in enumerate(per):
            recs[i].append({"layer": la, **r})
    rows, greedy = [], []
    examples = set(example_indices(len(items)))
    with torch.no_grad():
        for i, c in enumerate(progress(items, f"47.5: reads at L{layers[0]}..L{layers[-1]} (item)")):
            edits = edit_sets(layers, c["pos"], {la: q[la][i].to(dev) for la in layers}, bases,
                              {la: ks[la][i] for la in layers})  # fmt: skip
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["alt"], list(edits.values()), RENDERING, c["space"], ws)
                for arm, lg in zip(edits, logits, strict=True):
                    r = X.read_row(lg, rd, digits)
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "domain": c["domain"], "reader": w,
                                 "arm": arm, "kept": r["switched"], "to_org": int(r["top"] == rd["tok_A"]),
                                 "cand_kept": r["cand_switched"], **{k: r[k] for k in ("top", "role", "p_org", "p_alt", "ld")}})  # fmt: skip
                if i in examples:
                    s_ids = torch.tensor([rd["ids"]["alt"]], device=dev)
                    texts = model.generate_batch(s_ids, X.GEN_TOKENS, list(edits.values()))
                    greedy += [{"scene": c["scene"], "reader": w, "arm": arm, "greedy": t}
                               for arm, t in zip(edits, texts, strict=True)]  # fmt: skip
    norms = [{"scene": c["scene"], "entity": c["bridge"], "layers": recs[i]} for i, c in enumerate(items)]
    return rows, norms, greedy


def stage_run(name: str, why: str, set_name: str = SET) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.5 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    layer = X.PREDICTED[target]
    layers = tuple(range(layer, layer + SPAN))
    assert layers[-1] <= pins.N_LAYERS - 2, f"L..L+3 = {layers}: past the last block whose output is read on"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items_file = pins.DATA_DIR / "tasks_v2" / set_name / "items.jsonl"
    spec = pins.REPO_ROOT / SPEC
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "47.5",
         "spec": f"{SPEC} (47.5)", "question": f"{QUESTION} ({A.PREDICTIONS})", "set": set_name, "rendering": RENDERING,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in (items_file, spec)},
         "layer": layer, "layers": list(layers), "k": K, "omp": "signed (x0_parts.omp_atoms, X0's k = 25 picks)",
         "arms": ARM_TEXT, "edit": "ProjectOut: h <- h - (h Q) Q^T at the bridge word, on the state as it arrives",
         "random_part": f"the first k columns of X0's random basis (seed {X.SUBSPACE_SEED} + layer), k per item matching "
                        "the atoms' share of ||h_S||^2 on S's clean state at that layer",
         "read": "X0's chat read of S: the prompt with a digit's space token appended; kept = the top token is S's "
                 "answer's first token", "gate": X.GATE, "n": {"items": X.N_ITEMS, "min": X.N_MIN},
         "order": {**X.order_record(), "reads": f"per item and reader: S's prompt under the arms in ARMS order, in "
                                                f"batches of at most {X.order_record()['batch']} rows"},
         "rule": RULE, "decisive": "the recall at L (one layer)",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the job; results closed until {A.PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52 C: no Q-line; verdict --coverage
        m |= {"question": NO_PREDICTION, "batch": 52, "sealed": "none (batch 52 coverage; verdict --coverage)"}
    if X.EXCLUDE:
        m["excluded_scenes"] = sorted(X.EXCLUDE)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    missing = [la for la in layers if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at layers {missing} (L..L+3 = {layers})"
    old = X.RENDERINGS
    X.RENDERINGS = (RENDERING,)  # build and gate the chat cases only
    try:
        cases, counts = X.build_cases(model.tokenizer, set_name)
        ws = X.whitespace_mask(model)
        digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
        X.DIGIT_IDS.update(X.digit_ids(model.tokenizer))
        comp = X.competence(model, cases, digits, ws)
        gate, eligible = X.gate_and_eligible(cases, comp)
    finally:
        X.RENDERINGS = old
    items = eligible[RENDERING]
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in items])
    (out / "gate.json").write_text(json.dumps({"counts": counts, "gate": gate, "order": [c["scene"] for c in items],
                                              "hub_kernels": loaded_hub_kernels()}, indent=2) + "\n")  # fmt: skip
    print(json.dumps(gate, indent=2), flush=True)
    if not items:
        print("the gate fixed in advance did not pass (or too few eligible): not tested; see gate.json", flush=True)
        return out
    rows, norms, greedy = run_items(model, lens, items, layers, ws, digits)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) --------------------------------------------------------------------------------------------------


def numbers(rows: list[dict], reader: str, n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """One reader's share of S's answers kept per arm (cluster-bootstrap CIs over the bridge items) and per pair (L,
    L..L+3) the loss beyond random, kept(rand) - kept(zero), paired."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["kept"])
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in ARMS if (s, a) not in by]
    assert not missing, f"{reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    kept = {a: [by[(s, a)] for s in scenes] for a in ARMS}
    boot = X.resampled_rates(kept, [entity[s] for s in scenes], n_boot, seed)
    pt = {a: float(np.mean(v)) if v else math.nan for a, v in kept.items()}
    return {"n": len(scenes), "entities": len(set(entity.values())),
            "kept": {a: [pt[a], *X.interval(boot[a])] for a in ARMS},
            "beyond_random": {p: [pt[rd] - pt[z], *X.interval(boot[rd] - boot[z])] for p, z, rd in PAIRS}}  # fmt: skip


def label(nums: dict, pair: str = DECISIVE) -> str:
    """The rule on one reader's numbers at one pair (L: the rule; L..L+3: the same bars, descriptive)."""
    _, z, rd = next(p for p in PAIRS if p[0] == pair)
    kz, kr = nums["kept"][z][0], nums["kept"][rd][0]
    if kz >= KEEP_FOLLOWED - EPS and abs(kz - kr) <= NEAR + EPS:
        return FOLLOWED
    if kr - kz >= NEEDED - EPS:
        return NEEDS
    return NEITHER


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), not tested (the gate), or its numbers and labels."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending", "label": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    rows = X.read_jsonl(src / "outcomes.jsonl")
    gate = (
        json.loads((src / "gate.json").read_text())["gate"].get(RENDERING, {}) if (src / "gate.json").exists() else {}
    )
    if not rows:
        return {"target": target, "run": run, "status": "not tested", "label": "not tested", "gate": gate,
                "why": "no outcomes: the gate fixed in advance failed or the run did not finish"}  # fmt: skip
    readers = {READER_NAME[w]: numbers(rows, w, n_boot) for w in X.READERS}
    labels = {f"{w} {p}": label(readers[w], p) for w in ("recall", "lookup") for p, _, _ in PAIRS}
    norms = X.read_jsonl(src / "norms.jsonl")
    shares = {}
    for la in m["layers"]:
        recs = [r for n in norms for r in n["layers"] if r["layer"] == la]
        shares[la] = {k: float(np.median([r[k] for r in recs])) for k in ("share_hS_atoms", "share_delta_atoms",
                                                                          "share_hS_rand", "k_rand", "norm_hS", "norm_delta")}  # fmt: skip
    return {"target": target, "run": run, "layer": m["layer"], "layers": m["layers"], "status": "tested",
            "label": labels[f"recall {DECISIVE}"], "labels": labels, "readers": readers, "gate": gate,
            "shares_median": shares}  # fmt: skip


def batch_verb(models: list[dict]) -> dict:
    """The README's verb: "needs" only if "needed" holds on all three models; "follows / reads" once one model cannot
    hold it (tested and not needed, or not tested); pending while the rest could still all hold it."""
    needed = [m["label"] == NEEDS for m in models]
    pending = [m["status"] == "pending" for m in models]
    blocked = any(not n and not p for n, p in zip(needed, pending, strict=True))
    verb = "follows / reads" if blocked else "needs" if all(needed) else "pending"
    return {"verb": verb, "needed_on": [m["target"] for m in models if m["label"] == NEEDS],
            "per_model": {m["target"]: m["label"] for m in models}}  # fmt: skip


def fmt(v) -> str:
    return A.fmt(v)


def verdict_lines(models: list[dict], batch: dict, answer: str, n_boot: int) -> list[str]:
    lines = ["# 47.5: followed or needed? One-layer zeroing", "",
             f"Batch 47, test 47.5 ({SPEC}; {QUESTION}, Dan: {answer}). Main-test scenes (two people swap picks, chat); "
             "on S, at the bridge word: its projection on Δ's 25 OMP atoms removed at L (and at L..L+3, per-layer lens), "
             "against a random subspace of the same share of ||h_S||^2. Kept = S's answer read (X0's chat read). Cluster "
             f"bootstrap over the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}.", "",
             f"**The README's verb: {batch['verb']}** (\"needed\" on {len(batch['needed_on'])} of {len(models)} models: "
             f"{', '.join(batch['needed_on']) or 'none'}).", "",
             "| model | run | n | recall kept: zeroed at L | random at L | lost beyond random | label |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | | **{m['label']}** |")
            continue
        rc = m["readers"]["recall"]
        lines.append(f"| {m['target']} | {m['run']} | {rc['n']} | {fmt(rc['kept']['zero_L'])} | {fmt(rc['kept']['rand_L'])} "
                     f"| {fmt(rc['beyond_random']['L'])} | **{m['label']}** |")  # fmt: skip
    lines += ["", "Both readers, every arm: share of S's answers kept; lost beyond random = kept(random) - kept(zeroed), "
              "paired; labels at L..L+3 and for the lookup are descriptive (the same bars).", "",
              "| model | reader | " + " | ".join(ARMS) + " | lost beyond random, L | L..L+3 | label L | label L..L+3 |",
              "|---|---|" + "---|" * (len(ARMS) + 4)]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for w in ("recall", "lookup"):
            r = m["readers"][w]
            lines.append(f"| {m['target']} | {w} | " + " | ".join(fmt(r["kept"][a]) for a in ARMS) + " | "
                         + " | ".join(fmt(r["beyond_random"][p]) for p, _, _ in PAIRS) + " | "
                         + " | ".join(m["labels"][f"{w} {p}"] for p, _, _ in PAIRS) + " |")  # fmt: skip
    lines += ["", "Per layer (median over items): the atoms' share of ||h_S||^2 (what the zeroing removes) and of ||Δ||^2 "
              "(the J++ part's share of the change), the random part's achieved share and column count, the norms.", "",
              "| model | layer | atoms' share of h_S | atoms' share of Δ | random share of h_S | random k | ||h_S|| | ||Δ|| |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for la, s in m["shares_median"].items():
            lines.append(f"| {m['target']} | {la} | {s['share_hS_atoms']:.4f} | {s['share_delta_atoms']:.3f} | "
                         f"{s['share_hS_rand']:.4f} | {s['k_rand']:.0f} | {s['norm_hS']:.1f} | {s['norm_delta']:.1f} |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def example_lines(target: str, run: str, decode, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view of one run: k random items (seed, the run's greedy examples), each reader's S prompt as the
    model reads it with the bridge word in ⟦...⟧ (where the projection acts, at L or L..L+3), each arm's answer (the
    top token at the read, kept or not) and greedy text."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {target}: {run}, {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        c = items[i]
        lines += [f"### {c['scene']} ({c['domain']}): bridge {c['bridge']} (O) → {c['cf_bridge']} (S), token {c['pos']}",
                  ""]  # fmt: skip
        for w, rd in c["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "",
                      "S, as read:", "", "```", A.marked(decode, rd["ids"]["alt"], c["pos"]), "```", "",
                      "| arm | what | answer (top token) | kept S's | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            for arm in ARMS:
                r = reads[(c["scene"], w, arm)]
                g = greedy.get((c["scene"], w, arm))
                lines.append(f"| {arm} | {ARM_TEXT[arm]} | {decode([r['top']])!r} | {r['kept']} | "
                             f"{'' if g is None else repr(g)} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(
    runs: dict[str, str] | None = None, n_boot: int = X.N_BOOT, decode_for=None, coverage: bool = False
) -> Path:
    """47.5's verdict over MODELS (sealed until Q47.5), or with coverage (batch 52 C) the same rule on the coverage runs
    (target -> run, default COVERAGE_RUNS) alone: no seal guard, "no prediction" in place of Dan's answer, written to
    x52_zero-<UTC>/."""
    answer = (f"{NO_PREDICTION}; rule first scored in {SCORED}; the README verb counts the given runs only, not "
              "re-scored") if coverage else A.require_answer(QUESTION)  # fmt: skip
    runs = runs or (COVERAGE_RUNS if coverage else RUNS)
    if coverage:
        assert set(runs) <= set(COVERAGE_RUNS), f"47.5 coverage runs on {sorted(COVERAGE_RUNS)}, not {sorted(runs)}"
    models = [model_result(t, runs[t], n_boot) for t in (runs if coverage else MODELS)]
    batch = batch_verb(models)
    out = RESULTS / f"{'x52_zero' if coverage else 'x47_5'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, batch, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ") for ln in lines]
    (out / "x47_5.json").write_text(json.dumps({"dan": answer, "batch": batch, "models": models}, indent=1) + "\n")
    (out / "x47_5.md").write_text("\n".join(lines) + "\n")
    ex = ["# 47.5 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the "
          "bridge word, where its projection on the atoms (or the random subspace) is removed. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] == "tested":
            ex += example_lines(m["target"], m["run"], (decode_for or A.default_decode)(m["target"]))
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x47_zero/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.5 (jobs/c3/batch47.yaml; Q47.5): one-layer zeroing; sealed")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--runs", nargs=3, default=None, metavar=("9B", "27B", "MUSE"),
                    help=f"verdict: runs in place of the specs' {[RUNS[t] for t in MODELS]}")  # fmt: skip
    ap.add_argument("--coverage", action="store_true",
                    help=f"verdict: batch 52 coverage runs {COVERAGE_RUNS} ('{NO_PREDICTION}')")  # fmt: skip
    ap.add_argument("--exclude-dev", default=None, metavar="GATE_JSON",
                    help="run: keep the 'dev' scenes of this gate.json out of the items (x0_necessity's flag)")  # fmt: skip
    a = ap.parse_args()
    if a.exclude_dev:
        X.EXCLUDE.update(json.loads((pins.REPO_ROOT / a.exclude_dev).read_text())["dev"])
        assert X.EXCLUDE, f"{a.exclude_dev}: no dev scenes"
    if a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        assert not (a.coverage and a.runs), "verdict --coverage reads COVERAGE_RUNS (no --runs)"
        runs = {**RUNS, **dict(zip(MODELS, a.runs, strict=True))} if a.runs else None
        stage_verdict(runs, n_boot=a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
