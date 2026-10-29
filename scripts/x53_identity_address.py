"""x53_identity_address (batch 53, test 53.6; jobs/c3/batch53.yaml, the rule fixed in Dan's brief of 29 Oct 09:30 before
any run; no prediction): the recall, lens identity vs address, in conflict.

Scenes: x6_routes' generator (seed 2510; animals; three single-token items A, B, C with their locker sentences first,
then three pick sentences; O: Iris picked A), its C0 pairs: S_B = O with Iris's pick changed to B (nothing else). X0's
competence on every generated C0 scene (both readers say and read O's and S's answers right = eligible) and x6_routes'
gate per condition (O's read accuracy >= 0.80 per reader). C = the third item. The recall's three answers must differ:
the generator makes legs(A) != legs(B); scenes where C's legs equal A's or B's are dropped and counted. The first
N_ITEMS such eligible scenes in generator order.

At the bridge word (Iris's pick) at the layer fixed in advance (X0.PREDICTED; Lightning's committed L14), on O:
  lens   the lens part toward B: P_J Δ_B, Δ_B = h_{S_B} - h_O (B's change), P_J = X0's 25-atom signed OMP over the
         letter-token J++ dictionary at the layer (x49_gain.lens_parts)
  addr   the address swap toward C's slot at s = 2: 2 (mu_{j_C} - mu_{j_A}), mu = the pointer means of the target's probe
         run (x0_massmean.pointer_means(x6_routes.STATES[target]), as x8_write), j = the locker-sentence slot in O
  both   lens + addr (the conflict arm: the rule reads it)
  both_rand  lens + a random direction of addr's norm (seeded per scene, RAND_SEED; beside)
  none   O unedited
Read: X0's chat read, both readers. The recall's top token classed B (B's legs), C (C's legs), original (A's legs) or
other; the lookup's (beside) B (B's locker digit), C (C's), original (A's) or other.

Rule (Dan's brief, 53.6), on the recall under both: "the recall follows the lens identity" if B's share >= 2x C's;
"follows the address" if C's >= 2x B's; else "both". As computed: shares over the scenes (point estimates decide, EPS
1e-9; cluster-bootstrap CIs over the original bridge item A, 10,000, seed 0, beside); the clauses read in the brief's
order; neither B's nor C's answer at all (both shares 0): "neither (no B or C answers)", where both clauses would hold
by arithmetic alone. Beside: the lens and the address alone, both_rand, the lookup's classes, ||lens||, ||addr||,
||Δ_B|| and the lens part's share of Δ_B.

No prediction, not sealed: verdict (CPU) to results/x53_identity_address/x53_identity_address-<UTC>/ (verdict.md,
verdict.json, a figure, examples.md: 10 random scenes, seed 0). UNVERIFIED.

BJ_TARGET=qwen3.5-9b uv run python scripts/x53_identity_address.py plan                        # CPU, the tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_identity_address.py run --name qwen35_9b_x53_6  # GPU
uv run python scripts/x53_identity_address.py verdict --runs qwen35_9b_x53_6                   # CPU
"""

from __future__ import annotations

import argparse
import collections
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x49_gain as G

EXP = "x53_identity_address"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
TEST = "53.6"
NO_PREDICTION = "no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)"
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_6", "nemotron-3.5-lightning": "nem35l_x53_6",
        # Dan 11:25 (jobs/c3/batch53.yaml critic_1125, order item 4): "53.6 on the 27B and Muse (same rule)"
        "qwen3.6-27b": "x53_6_27b", "muse-glimmer-30b": "muse30_x53_6",
        # Dan 12:20 (batch53.yaml fallback_1220): coverage on the 122B, the same rule; in the rule across models it is one
        # of "the others" (not in Dan's moved list; the coordinator's reading, flagged)
        "qwen3.5-122b-a10b": "qwen35_122b_x53_6"}  # fmt: skip
# the rule across models, verbatim (critic_1125); the "moved" models are Dan's list, verbatim
RULE_ACROSS = ("\"the recall's pointer use tracks the swap's collateral\" if the models whose recall the address swap "
               "moved (9B, Lightning) give \"both\" and the others give \"follows the lens identity\"")  # fmt: skip
MOVED = ("qwen3.5-9b", "nemotron-3.5-lightning")  # Dan's list (critic_1125), verbatim
ACROSS_LABEL = "the recall's pointer use tracks the swap's collateral"
RENDERING = "chat"
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
K = X.K_MAIN  # 25
S_DOSE = 2
RAND_SEED = 5306
N_ITEMS = R.N_ITEMS  # 300
# 1,400 per condition (x51_das's top-up generation): about a third of the C0 scenes have three distinct legs counts
N_GEN = 1400
ARMS = ("none", "lens", "addr", "both", "both_rand")
ARM_TEXT = {"none": "O unedited", "lens": "the lens part toward B: P_J (h_{S_B} - h_O)",
            "addr": "the address swap toward C's slot: 2 (mu_{j_C} - mu_{j_A})", "both": "lens + addr (the rule's arm)",
            "both_rand": "lens + a random direction of addr's norm (beside)"}  # fmt: skip
CLASSES = ("B", "C", "original", "other")
RATIO = 2.0
EPS = 1e-9
LABELS = {"identity": "the recall follows the lens identity", "address": "the recall follows the address",
          "both": "both", "neither": "neither (no B or C answers)"}  # fmt: skip
RULE = ("on the recall under lens + address: \"the recall follows the lens identity\" if B's share >= 2x C's; "
        "\"follows the address\" if C's >= 2x B's; else \"both\"")  # fmt: skip


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def roles(tok, case: dict, legs: dict[str, int]) -> dict[str, Any] | None:
    """A (O's pick), B (S_B's pick), C (the third item): slots in O's locker order, locker digits, legs and their answer
    tokens. None if C's legs equal A's or B's (the recall's classes would be ambiguous)."""
    from scripts import suite_v1 as S

    sl = W.slots_of(case["context"])
    items = [x for x, _ in sl]
    a, b = case["bridge"], case["cf_bridge"]
    (c,) = [x for x in items if x not in (a, b)]
    if legs[c] in (legs[a], legs[b]):
        return None
    out: dict[str, Any] = {}
    for role, x in (("original", a), ("B", b), ("C", c)):
        j = items.index(x)
        out[role] = {"item": x, "slot": j, "digit": sl[j][1], "legs": legs[x],
                     "tok_digit": S.answer_token(tok, str(sl[j][1]), "digit"),
                     "tok_legs": S.answer_token(tok, str(legs[x]), "digit")}  # fmt: skip
    assert out["original"]["tok_legs"] == case["readers"][X.RECALL]["tok_A"], f"{case['scene']}: A's legs token"
    assert out["B"]["tok_legs"] == case["readers"][X.RECALL]["tok_b"], f"{case['scene']}: B's legs token"
    return out


def c0_cases(tok, n_gen: int | None = None) -> tuple[list[dict], dict]:
    """The generator's C0 scenes (x6_routes.scenes, n_gen per condition, seed 2510; prefix-stable in n: its first 700 are
    the routes runs') and the generator's drops."""
    cases, dropped = R.scenes(tok, n_gen or N_GEN, rendering=RENDERING)
    return [c for c in cases if c["condition"] == "C0"], dict(dropped)


def with_roles(tok, cases: list[dict]) -> tuple[list[dict], collections.Counter]:
    legs, _, _ = R.pools(tok)
    kept, counts = [], collections.Counter()
    for c in cases:
        r = roles(tok, c, legs)
        if r is None:
            counts["C's legs equal A's or B's"] += 1
            continue
        kept.append({**c, "roles": r})
    counts["kept"] = len(kept)
    return kept, counts


def classify(top: int, rl: dict[str, Any], key: str) -> str:
    """The class of a top token: B, C or original by the roles' tokens (key: tok_legs for the recall, tok_digit for the
    lookup), else other."""
    for cl in ("B", "C", "original"):
        if rl[cl][key] == top:
            return cl
    return "other"


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    cases, dropped = c0_cases(tok)
    kept, counts = with_roles(tok, cases)
    slots = collections.Counter((r["roles"]["original"]["slot"], r["roles"]["C"]["slot"]) for r in kept)
    blob = {"target": pins.TARGET, "run": RUNS.get(pins.TARGET), "layer": X.PREDICTED[pins.TARGET],
            "c0_generated": len(cases), "generator_dropped": dropped, "roles": dict(counts),
            "moves_A_to_C_slot": {f"{a}->{c}": n for (a, c), n in sorted(slots.items())},
            "mu_from": R.STATES.get(pins.TARGET), "reads_per_scene": 2 * len(ARMS)}  # fmt: skip
    print(json.dumps(blob, indent=1))
    return blob


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def arm_vectors(lens, addr, rand_dir) -> dict[str, Any]:
    """The vectors each arm adds at the bridge word (one scene): rand_dir a unit vector."""
    return {"lens": lens, "addr": addr, "both": lens + addr, "both_rand": lens + rand_dir * addr.norm()}


def stage_run(name: str, why: str, n_items: int = N_ITEMS) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "53.6 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"53.6 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": TEST,
         "spec": "jobs/c3/batch53.yaml (53.6)", "question": NO_PREDICTION, "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)):
         X.sha256_of(SPEC)}, "layer": layer, "k": K, "s": S_DOSE, "arms": ARM_TEXT, "classes": list(CLASSES),
         "rule": RULE, "mu_from": R.STATES[target], "n_items": n_items,
         "scenes": f"x6_routes.scenes (seed {R.SEED}, {N_GEN} per condition), the C0 pairs (S_B: Iris picked B) whose "
                   "three items have distinct legs counts; on these X0's competence and X0's gate (O's read accuracy "
                   f">= 0.80 per reader); the first {n_items} eligible in generator order",
         "seeds": {"scenes": R.SEED, "random_directions": RAND_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer",
                   "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "sealed": "none (no prediction)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    model = load_model()
    tok = model.tokenizer
    dev = model.device
    generated, dropped = c0_cases(tok)
    cases, counts = with_roles(tok, generated)  # three distinct legs counts; the gate and eligibility on these
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    chosen = ok[:n_items]
    gate = {"c0_generated": len(generated), "roles": dict(counts), "cases": len(cases), "org_read_accuracy": acc,
            "pass": all(a >= X.GATE for a in acc.values()), "gate_min": X.GATE, "eligible": len(ok),
            "used": len(chosen), "generator_dropped": dropped}  # fmt: skip
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not gate["pass"] or not chosen:
        raise SystemExit(f"the gate fixed in advance missed or no eligible scene: {gate}")
    X.write_jsonl(out / "cases.jsonl", chosen)
    mu = {k: torch.tensor(v, dtype=torch.float32, device=dev) for k, v in MM.pointer_means(R.STATES[target]).items()}
    gen = torch.Generator().manual_seed(RAND_SEED)
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        ho, hs = [], []
        for c in progress(chosen, f"53.6: states at the bridge word, L{layer} (scene)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            for v, store in (("org", ho), ("alt", hs)):
                store.append(model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][c["pos"]].float()
                             .cpu().clone())  # fmt: skip
        delta = torch.stack(hs) - torch.stack(ho)  # [n, d], CPU
        jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
        d = delta.shape[1]
        basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        lens = torch.cat([G.lens_parts(jdic, delta[s : s + 64].to(dev), K, basis)[0].float().cpu()
                          for s in range(0, len(chosen), 64)])  # fmt: skip
        del jdic, basis
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        rows, norms = [], []
        for i, c in enumerate(progress(chosen, f"53.6: reads, {len(ARMS)} arms x 2 readers (scene)")):
            rl = c["roles"]
            addr = (S_DOSE * (mu[rl["C"]["slot"]] - mu[rl["original"]["slot"]])).cpu()
            r = torch.randn(d, generator=gen)
            vecs = arm_vectors(lens[i], addr, r / r.norm())
            norms.append({"scene": c["scene"], "norm_delta": round(float(delta[i].norm()), 4),
                          "norm_lens": round(float(lens[i].norm()), 4), "norm_addr": round(float(addr.norm()), 4),
                          "share_lens": round(float(G.share(lens[i : i + 1], delta[i : i + 1])[0]), 6),
                          "slot_A": rl["original"]["slot"], "slot_C": rl["C"]["slot"]})  # fmt: skip
            edits = [{}] + [{layer: AddRows(vecs[a][None].to(dev), [c["pos"]])} for a in ARMS[1:]]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                key = "tok_legs" if w == X.RECALL else "tok_digit"
                for a, lg in zip(ARMS, logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a, "top": top,
                                 "top_text": model.decoded[top], "class": classify(top, rl, key)})  # fmt: skip
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    print(f"wrote {out}: {len(rows)} reads of {len(chosen)} scenes", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def label(b: float, c: float) -> str:
    """The brief's rule on the recall's B and C shares under both (point estimates, EPS)."""
    if b <= EPS and c <= EPS:
        return "neither"
    if b >= RATIO * c - EPS:
        return "identity"
    if c >= RATIO * b - EPS:
        return "address"
    return "both"


def shares(rows: list[dict], n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """Per class, its share with a cluster-bootstrap CI over the bridge items; n."""
    sw = {cl: [int(r["class"] == cl) for r in rows] for cl in CLASSES}
    boot = X.resampled_rates(sw, [r["entity"] for r in rows], n_boot)
    return {"n": len(rows), **{cl: [float(np.mean(sw[cl])), *X.interval(boot[cl])] for cl in CLASSES}}


def run_numbers(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cells = {w: {a: shares([r for r in rows if r["reader"] == w and r["arm"] == a], n_boot) for a in ARMS}
             for w in X.READERS}  # fmt: skip
    both = cells[X.RECALL]["both"]
    lab = label(both["B"][0], both["C"][0])
    norms = X.read_jsonl(src / "norms.jsonl")
    med = {
        k: round(float(np.median([r[k] for r in norms])), 4)
        for k in ("norm_delta", "norm_lens", "norm_addr", "share_lens")
    }
    gate = json.loads((src / "gate.json").read_text())
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "label": lab, "text": LABELS[lab],
            "cells": cells, "norms_median": med, "gate": gate}  # fmt: skip


def fmt(v: list) -> str:
    if v is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(models: list[dict], path: Path) -> None:
    """Per model a panel: the recall's B / C / original / other shares per arm (stacked)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(models), figsize=(5.0 * len(models), 3.6), squeeze=False)
    for ax, mdl in zip(axes[0], models, strict=True):
        rc = mdl["cells"][X.RECALL]
        bottom = np.zeros(len(ARMS))
        for cl in CLASSES:
            vals = np.array([rc[a][cl][0] for a in ARMS])
            ax.bar(range(len(ARMS)), vals, bottom=bottom, label=cl)
            bottom += vals
        ax.set_xticks(range(len(ARMS)))
        ax.set_xticklabels(ARMS, fontsize=7)
        ax.set_ylim(0, 1)
        ax.set_ylabel("recall's answer (share)")
        ax.set_title(f"{mdl['target']} L{mdl['layer']}: {mdl['text']}", fontsize=8)
    axes[0][0].legend(fontsize=7)
    fig.suptitle("53.6: the recall, lens identity (B) vs address (C) (UNVERIFIED)", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    cases = X.read_jsonl(src / "cases.jsonl")
    reads = X.read_jsonl(src / "outcomes.jsonl")
    pick = sorted(random.Random(seed).sample(range(len(cases)), min(k, len(cases))))
    lines = [f"## {run}: {len(pick)} random scenes of {len(cases)} (seed {seed})", ""]
    for i in pick:
        c = cases[i]
        rl = c["roles"]
        lines += [f"### {c['scene']}: A = {rl['original']['item']} (slot {rl['original']['slot']}, locker "
                  f"{rl['original']['digit']}, {rl['original']['legs']} legs), B = {rl['B']['item']} (slot {rl['B']['slot']}, "
                  f"locker {rl['B']['digit']}, {rl['B']['legs']} legs), C = {rl['C']['item']} (slot {rl['C']['slot']}, "
                  f"locker {rl['C']['digit']}, {rl['C']['legs']} legs)", "", f"O: {c['context']}", "",
                  f"S_B: {c['cf_context']}", "", "| reader | arm | top token | class |", "|---|---|---|---|"]  # fmt: skip
        for r in reads:
            if r["scene"] == c["scene"]:
                lines.append(f"| {r['reader']} | {r['arm']} | {r['top_text']!r} | {r['class']} |")
        lines.append("")
    return lines


def across(models: list[dict]) -> dict[str, Any]:
    """The rule across models (critic_1125): the moved models (MOVED, Dan's list) "both", every other model run "follows
    the lens identity"; with every model of RUNS (the 122B among "the others"): holds / does not hold; fewer: pending (unless already broken)."""
    labels = {m["target"]: m["label"] for m in models}
    want = {t: ("both" if t in MOVED else "identity") for t in RUNS}
    broken = [t for t, lab in labels.items() if t in want and lab != want[t]]
    missing = [t for t in RUNS if t not in labels]
    if broken:
        lab = "does not hold"
    elif missing:
        lab = f"pending ({len(labels)} of {len(RUNS)} models; missing {', '.join(missing)})"
    else:
        lab = f"holds: {ACROSS_LABEL}"
    return {"label": lab, "per_model": {t: {"label": labels.get(t), "wanted": want[t]} for t in RUNS}, "broken": broken,
            "moved": list(MOVED)}  # fmt: skip


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    models = [run_numbers(r, n_boot) for r in runs]
    acr = across(models)
    out = RESULTS / f"x53_identity_address-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 53.6: the recall, lens identity vs address, in conflict", "",
             f"Batch 53, test 53.6 (jobs/c3/batch53.yaml; {NO_PREDICTION}). At the bridge word: the lens part toward B "
             f"(P_J of B's change, k = {K}) plus the address swap toward C's slot (s = {S_DOSE}, the probe run's pointer "
             "means); x6_routes' C0 scenes with three distinct legs counts. UNVERIFIED.", "", f"Rule (Dan's brief): {RULE}.",
             "", f"Rule across models (Dan 11:25, critic_1125, verbatim): {RULE_ACROSS}. As computed: the moved models are "
             f"Dan's list ({', '.join(MOVED)}); every other model of the four is wanted at \"follows the lens identity\"; "
             "a model with another label breaks it.", "", f"**Across models: {acr['label']}** (per model, label / wanted: "
             + "; ".join(f"{t} {v['label']} / {v['wanted']}" for t, v in acr["per_model"].items()) + ").", "",
             "| model | layer | n | recall B | recall C | recall original | recall other | label |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in models:
        b = mdl["cells"][X.RECALL]["both"]
        lines.append(f"| {mdl['target']} | {mdl['layer']} | {b['n']} | {fmt(b['B'])} | {fmt(b['C'])} | "
                     f"{fmt(b['original'])} | {fmt(b['other'])} | **{mdl['text']}** |")  # fmt: skip
    lines += ["", "Every arm, both readers (shares, cluster-bootstrap CIs over the bridge item A):", "",
              "| model | reader | arm | B | C | original | other |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in models:
        for w, cells in mdl["cells"].items():
            for a in ARMS:
                s = cells[a]
                lines.append(f"| {mdl['target']} | {READER_NAME[w]} | {a} | {fmt(s['B'])} | {fmt(s['C'])} | {fmt(s['original'])} | "
                             f"{fmt(s['other'])} |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ". The lookup's classes: B = B's "
              "locker digit, C = C's, original = A's.", ""]  # fmt: skip
    for mdl in models:
        lines.append(f"- {mdl['target']}: medians {mdl['norms_median']}; gate {mdl['gate']['org_read_accuracy']} "
                     f"(pass {mdl['gate']['pass']}), eligible {mdl['gate']['eligible']}, roles {mdl['gate']['roles']}, "
                     f"used {mdl['gate']['used']}.")  # fmt: skip
    lines += ["", "Figure: x53_identity_address.png"]
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "question": NO_PREDICTION, "rule": RULE,
                                                  "rule_across": RULE_ACROSS, "across": acr, "models": models},
                                                 indent=1) + "\n")  # fmt: skip
    figure(models, out / "x53_identity_address.png")
    ex = ["# 53.6 examples (verify pack): the scene's roles, O and S_B, every arm's top token. UNVERIFIED.", ""]
    for mdl in models:
        ex += example_lines(mdl["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x53_identity_address/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the runs (default: every one of RUNS here)")
    ap.add_argument("--why", default="batch 53, test 53.6 (jobs/c3/batch53.yaml)")
    ap.add_argument("--n-items", type=int, default=N_ITEMS)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.n_items)
    else:
        runs = a.runs or [r for r in RUNS.values() if (RESULTS / r / "outcomes.jsonl").exists()]
        stage_verdict(runs, a.n_boot)


if __name__ == "__main__":
    main()
