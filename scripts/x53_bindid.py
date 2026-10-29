"""x53_bindid (batch 53, test 53.8; jobs/c3/batch53.yaml critic_1125 item 6, Dan 29 Oct 11:25, stretch; the rule fixed in
Dan's text before any run; no prediction): a binding-ID test for the lookup's identity code.

Dan's text, verbatim (RULE_VERBATIM): "Stretch, 53.8, a binding-ID test for the lookup's identity code (9B, then Muse): at
L, take the state at item X's mention in its locker sentence minus X's token embedding (mean over scenes, X fixed by
slot), add it at the bridge word at 1x / 2x the size of a real identity change, against a random vector of the same
norm and against the same with another item Y's mention. Read: lookups sent to X's locker. Rule: "a shared identity
code" if X's share minus random >= 0.25 at 2x and minus Y's version >= 0.15; "no" if <= 0.05; else in between."

As built (each choice fixed here before any run; the manifest, the spec notes and the verdict state them):
Scenes: x6_routes' generator (seed 2510; animals; three one-token items, their locker sentences first, "The locker of
  the frog is 5.", then three pick sentences; O: Iris picked A), N_GEN = 1,000 per condition, its C0 scenes in
  generator order (prefix-stable: the first 700 are the routes runs' C0 scenes).
  Test pool: C0 scenes 1-700 (the routes runs'); X0's competence on them, X0's gate (O's read accuracy >= 0.80 per
  reader, lookup and recall) and X0's eligibility (both readers say and read O's and S_B's answers right); the first
  N_ITEMS = 300 eligible in generator order.
  Mean pool: C0 scenes 701-1,000 (300 other draws of the generator; none is a test scene, so no test scene's own state
  enters a vector it is read under).
X's vector, per locker slot k = 0, 1, 2 ("X fixed by slot": X is the item whose locker sentence is the k-th): on each
  mean-pool scene's O lookup prompt (chat), the block output at L at the item's mention in its locker sentence (the
  item word: one token by the generator's rule, " frog"), minus that token's input-embedding row
  (model.hf.get_input_embeddings, the raw row); the mean over the mean-pool scenes: c_k (codes.npz).
Dose: "the size of a real identity change" = ||Δ||, Δ = h_{S_B} - h_O at the bridge word at L, S_B = O with Iris's
  pick changed from A to B and nothing else (x6_routes' C0 pair), per scene: the existing definition of x52_answer_map's
  ans1 / ans2 ("s = ||Δ|| at that position and layer, Δ = h_S - h_O, the real change there"). 1x and 2x.
Arms, each added at the bridge word (Iris's pick) at L on O (X0's AddRows), per test scene with A at slot j_A:
  code{k}_x{d}   d ||Δ|| c_k / ||c_k|| for both slots k != j_A (the scene's two other items take turns as X and Y)
  rand_x{d}      d ||Δ|| r / ||r||, r one Gaussian direction per scene (seed RAND_SEED, drawn in scene order)
  ccode{k}_x{d}  the centered arm (Dan 12:10, decisions_1210b item 1, added before any run): d ||Δ|| c~_k / ||c~_k||,
                 c~_k = c_k - the mean of c_0, c_1, c_2 (the slot-specific part); its controls are the same random arm
                 (rand_x{d}: the same norm, d ||Δ||) and Y's centered version (ccode{k'}_x{d})
  whole          Δ itself (the real identity change; beside: the lookup sent to B's locker)
  none           O unedited
Read: X0's chat read (the top token after the digit's space), both readers; the lookup's top token classed by locker
  slot (slot k's digit token, as x8_write.classify) or other; the recall's kept = its top token is A's legs (collateral).
Per (scene, X slot k), Y = the scene's remaining slot: X's share under X (code{k}), under Y's version (code{k'}) and
  under random (rand) = the share of those reads whose lookup goes to slot k's locker; both assignments per scene
  pooled; cluster-bootstrap CIs over the bridge item A (10,000 draws, seed 0), the differences paired on the same draws.
Rule (Dan's text; at 2x, point estimates; EPS 1e-9 at the bars): "a shared identity code" if X - random >= 0.25 and
  X - Y >= 0.15; "no" if X - random <= 0.05 (the reading of Dan's "<= 0.05": X's share minus random's, at 2x); else "in
  between". A failed gate: "not tested (gate x < 0.80)", never lowered. The headline is the pre-specified (uncentered)
  arm's label; the centered arm gets its own label by the same thresholds, reported beside (Dan 12:10).
Beside, not in the rule: 1x; the per-slot split; every arm's classes (X / Y / original / other); the collateral (the
  lookup's and the recall's clean answers kept); ||Δ|| and ||U^T Δ|| (U: the pointer directions, x47_atoms.pointer_basis:
  E6c's unit of a real pointer change); the slot vectors' norms and cosines (raw and centered), the norm of each
  slot-specific part ||c~_k|| (Dan 12:10), and the slot differences against the pointer means (x0_massmean.pointer_means).

No prediction, not sealed: verdict (CPU) to results/x53_bindid/x53_bindid-<UTC>/ (verdict.md, verdict.json, a figure
with the four model slots, examples.md: 10 random scenes, seed 0). UNVERIFIED.

Models: the 9B (L12), then Muse (L26), then the 27B (L32; fallback_1220, Dan 12:22: "53.8 на 27B, після 9B і Muse").

BJ_TARGET=qwen3.5-9b uv run python scripts/x53_bindid.py plan                          # CPU, the tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_bindid.py run --name qwen35_9b_x53_8c   # GPU
uv run python scripts/x53_bindid.py verdict --runs qwen35_9b_x53_8c                    # CPU
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
import textwrap
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

EXP = "x53_bindid"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
TEST = "53.8"
NO_PREDICTION = "no prediction (batch 53: the rule fixed in Dan's text, 29 Oct 11:25, before any run)"
# Dan: "9B, then Muse"; the 27B after them (fallback_1220, Dan 12:22). With the centered arm (Dan 12:10): new names;
# qwen35_9b_x53_8 / muse30_x53_8 (specs x53_8_bindid_9b / _muse) were queued and cancelled before running, unused
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_8c", "muse-glimmer-30b": "muse30_x53_8c", "qwen3.6-27b": "x53_8c_27b"}
MODEL_ORDER = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")  # the four figure slots
MODEL_SHORT = {
    "qwen3.5-9b": "9B",
    "qwen3.6-27b": "27B",
    "muse-glimmer-30b": "Muse",
    "nemotron-3.5-lightning": "Lightning",
}
NOT_DESIGNED = "not designed (9B, Muse, then 27B: Dan 11:25, 12:22; Lightning not added)"
RENDERING = "chat"
N_GEN = 1000  # per condition; prefix-stable, so C0 scenes 1-700 are the routes runs'
N_TEST_POOL = R.N_GEN  # 700: the test pool, C0 scenes 1-700
N_MEAN = 300  # the mean pool, C0 scenes 701-1,000
N_ITEMS = R.N_ITEMS  # 300 test scenes
SLOTS = W.SLOTS  # (0, 1, 2)
DOSES = (1, 2)
RULE_DOSE = 2
RAND_SEED = 5308
SHARED_RAND, SHARED_Y, NO_RAND = 0.25, 0.15, 0.05
EPS = 1e-9
LEAD = "The locker of the "  # x6_routes.context's locker sentence: the item word follows it
ROLES = ("X", "Y", "original", "other")
KINDS = ("X", "Y", "R")  # the arm read for X's share: X's own vector, Y's version, the random vector
KIND_TEXT = {"X": "X's vector", "Y": "Y's version", "R": "random (same norm)"}
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
# the two constructions, by their arms' prefix: the pre-specified (the headline) and Dan's 12:10 centered arm (beside)
VARIANTS = {"uncentered": "code", "centered": "ccode"}
HEADLINE = "uncentered"
VARIANT_TEXT = {"uncentered": "pre-specified, uncentered c_k (headline)",
                "centered": "centered c_k - mean over slots (Dan 12:10, beside)"}  # fmt: skip
CENTERED_VERBATIM = (
    "53.8: keep your construction (uncentered, dose 1x = ||Δ|| at the bridge word, as in 52) as the pre-specified arm, "
    "rule unchanged. Add, now, before any run: a centered arm (X's vector minus the mean over slots), same doses, same "
    "controls (random of the same norm; Y's centered version), the same rule thresholds reported for it beside. Report "
    "the slot-vector cosines and the norm of the slot-specific part."
)
RULE_VERBATIM = (
    "Stretch, 53.8, a binding-ID test for the lookup's identity code (9B, then Muse): at L, take the state at item X's "
    "mention in its locker sentence minus X's token embedding (mean over scenes, X fixed by slot), add it at the bridge "
    "word at 1x / 2x the size of a real identity change, against a random vector of the same norm and against the same "
    "with another item Y's mention. Read: lookups sent to X's locker. Rule: \"a shared identity code\" if X's share "
    'minus random >= 0.25 at 2x and minus Y\'s version >= 0.15; "no" if <= 0.05; else in between.'
)
RULE = (
    f'at {RULE_DOSE}x, point estimates (EPS {EPS:g}): "a shared identity code" if X - random >= {SHARED_RAND} and '
    f'X - Y >= {SHARED_Y}; "no" if X - random <= {NO_RAND} (Dan\'s "<= 0.05" read as X\'s share minus random\'s at '
    f'{RULE_DOSE}x); else "in between"; a failed gate: "not tested (gate x < {X.GATE:.2f})"'
)
LABELS = {"shared": "a shared identity code", "no": "no", "between": "in between"}
DESIGN = {
    "scenes": f"x6_routes.scenes (seed {R.SEED}, {N_GEN} per condition, prefix-stable), the C0 scenes in generator "
              f"order; test pool = C0 scenes 1-{N_TEST_POOL} (the routes runs'), X0's competence, gate and eligibility "
              f"there, the first {N_ITEMS} eligible; mean pool = C0 scenes {N_TEST_POOL + 1}-{N_TEST_POOL + N_MEAN} "
              "(held out: no test scene's own state enters a vector)",
    "x_vector": "per locker slot k: mean over the mean-pool scenes of (the block output at L at the k-th locker "
                "sentence's item word in O's chat lookup prompt) - (that token's input-embedding row, raw); X = the "
                "item at slot k (X fixed by slot); the item word is one token (the generator's rule, asserted)",
    "x_and_y": "per test scene the two items other than the bridge item A take turns as X and Y (X = slot k, Y = the "
               "remaining slot k'); both assignments pooled",
    "dose": "the size of a real identity change = ||Δ||, Δ = h_{S_B} - h_O at the bridge word at L (C0: Iris's pick "
            "A -> B, nothing else), per scene: x52_answer_map's ans1 / ans2 (s = ||Δ||); 1x and 2x",
    "controls": f"a random Gaussian direction per scene (seed {RAND_SEED}) at the same norm; Y's version = slot k''s "
                "vector at the same norm",
    "centered": "Dan 12:10 (decisions_1210b item 1, before any run): a second arm with c~_k = c_k - (c_0 + c_1 + c_2) / 3 "
                "(the slot-specific part) in place of c_k, the same doses (d ||Δ||), the same random arm (same norm) "
                "and Y's centered version as controls, its own label by the same thresholds, beside; the headline is "
                "the uncentered arm's",
    "read": "X0's chat read, both readers; the lookup's top token classed by locker slot (the slot's digit token) or "
            "other; X's share = the lookup's top token is X's locker digit",
    "collateral": "the clean answers kept: the lookup's (A's locker) and the recall's (A's legs) top token unchanged",
    "ci": f"cluster bootstrap over the bridge item A ({X.N_BOOT:,} draws, seed {X.BOOT_SEED}), arms paired",
}  # fmt: skip


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def c0_cases(tok, n_gen: int | None = None) -> tuple[list[dict], dict]:
    """The generator's C0 scenes in generator order (x6_routes.scenes, n_gen per condition, seed 2510) and its drops."""
    cases, dropped = R.scenes(tok, n_gen or N_GEN, rendering=RENDERING)
    return [c for c in cases if c["condition"] == "C0"], dict(dropped)


def split_pools(cases: list[dict], n_test: int = N_TEST_POOL, n_mean: int = N_MEAN) -> tuple[list[dict], list[dict]]:
    """The test pool (the first n_test C0 scenes) and the mean pool (the next n_mean), with no context in both."""
    test, mean = cases[:n_test], cases[n_test : n_test + n_mean]
    seen = {c["context"] for c in test}
    return test, [c for c in mean if c["context"] not in seen]


def mention_positions(tok, case: dict) -> list[int] | None:
    """Per locker slot, the token index of its item's mention in O's lookup prompt (as x6_routes.encode renders it), or
    None if an item word is not exactly one token there."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    rd = case["readers"][X.LOOKUP]
    ctx = case["context"]
    item = {"format": "prose", "kind": "digit", "context": ctx, "question": rd["question"]}
    text = X.render(tok, item, case["rendering"], ctx)
    enc = raw_encoding(tok, text, offsets=True)
    assert list(enc["input_ids"]) == list(rd["ids"]["org"]), f"{case['scene']}: O's lookup prompt does not re-encode"
    at0 = text.index(ctx)
    out = []
    for x, d in W.slots_of(ctx):
        sent = f"{LEAD}{x} is {d}."
        assert ctx.count(sent) == 1, f"{case['scene']}: locker sentence {sent!r} not once"
        w0 = at0 + ctx.index(sent) + len(LEAD)
        hit = SP.tokens_in(enc["offset_mapping"], w0, w0 + len(x))
        if len(hit) != 1:
            return None
        out.append(hit[0])
    return out


def slot_info(tok, case: dict) -> dict[str, Any]:
    """The scene's locker slots: items, digits and digit tokens in O's order; A's slot (O's pick) and B's (S_B's)."""
    from scripts import suite_v1 as S

    sl = W.slots_of(case["context"])
    items = [x for x, _ in sl]
    toks = [S.answer_token(tok, str(d), "digit") for _, d in sl]
    out = {"items": items, "digits": [d for _, d in sl], "tokens": toks, "slot_a": items.index(case["bridge"]),
           "slot_b": items.index(case["cf_bridge"])}  # fmt: skip
    assert toks[out["slot_a"]] == case["readers"][X.LOOKUP]["tok_A"], f"{case['scene']}: A's locker token"
    assert toks[out["slot_b"]] == case["readers"][X.LOOKUP]["tok_b"], f"{case['scene']}: B's locker token"
    return out


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    cases, dropped = c0_cases(tok)
    test, mean = split_pools(cases)
    pos = [mention_positions(tok, c) for c in mean]
    a_slots = collections.Counter(slot_info(tok, c)["slot_a"] for c in test)
    not_item = sum(tok.decode([c["readers"][X.LOOKUP]["ids"]["org"][p]]).strip() != x
                   for c, ps in zip(mean, pos, strict=True) if ps
                   for p, (x, _) in zip(ps, W.slots_of(c["context"]), strict=True))  # fmt: skip
    blob = {"target": pins.TARGET, "run": RUNS.get(pins.TARGET), "layer": X.PREDICTED[pins.TARGET],
            "c0_generated": len(cases), "generator_dropped": dropped, "test_pool": len(test), "mean_pool": len(mean),
            "mean_pool_mention_not_one_token": sum(p is None for p in pos), "mentions_not_decoding_to_item": not_item,
            "test_pool_A_slots": {str(k): v for k, v in sorted(a_slots.items())},
            "test_pool_entities": len({c["bridge"] for c in test}),
            "reads_per_scene": 2 * len(arm_names(0))}  # fmt: skip
    print(json.dumps(blob, indent=1))
    return blob


# ---- vectors and arms ---------------------------------------------------------------------------------------------


def mention_codes(h, e):
    """Per slot, the mean over scenes of (the mention's state at L - its token's input embedding): [n, S, d] -> [S, d]."""
    assert h.dim() == 3, f"states {tuple(h.shape)}: want [scenes, slots, d]"
    assert h.shape == e.shape, f"states {tuple(h.shape)} vs embeddings {tuple(e.shape)}"
    return (h - e).mean(0)


def centered(codes):
    """The slot-specific parts (Dan 12:10): each slot's vector minus the mean over the slots ([S, d] -> [S, d])."""
    return codes - codes.mean(0)


def dosed(v, size: float):
    """v rescaled to norm `size` (its direction kept)."""
    return v * (size / v.norm())


def arm_names(slot_a: int) -> list[str]:
    """The read order of one scene's rows: none, whole, then per dose the two other slots' vectors, the random one and
    the two other slots' centered vectors."""
    others = [k for k in SLOTS if k != slot_a]
    return ["none", "whole"] + [
        a
        for d in DOSES
        for a in (*(f"code{k}_x{d}" for k in others), f"rand_x{d}", *(f"ccode{k}_x{d}" for k in others))
    ]


def arm_vectors(codes, rand_dir, slot_a: int, size: float, delta) -> dict[str, Any]:
    """The vector each arm adds at the bridge word (one scene; every arm but none): codes [S, d], rand_dir [d] (any norm),
    size = ||Δ|| (the real identity change's), delta = Δ. Every arm at dose d has norm d ||Δ||."""
    cc = centered(codes)
    out = {"whole": delta}
    for d in DOSES:
        for k in SLOTS:
            if k != slot_a:
                out[f"code{k}_x{d}"] = dosed(codes[k], d * size)
        out[f"rand_x{d}"] = dosed(rand_dir, d * size)
        for k in SLOTS:
            if k != slot_a:
                out[f"ccode{k}_x{d}"] = dosed(cc[k], d * size)
    assert list(out) == arm_names(slot_a)[1:]
    return out


def lookup_slot(top: int, tokens: list[int]) -> int:
    """The locker slot whose digit token is the lookup's top token, -1 for any other token."""
    hit = [k for k, t in enumerate(tokens) if t == top]
    return hit[0] if hit else -1


def role(slot: int, x: int, y: int, a: int) -> str:
    return "X" if slot == x else "Y" if slot == y else "original" if slot == a else "other"


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def pointer_refs(target: str) -> tuple[Any, dict[int, np.ndarray] | None, str]:
    """The pointer directions U (x47_atoms.pointer_basis) and means (x0_massmean.pointer_means) of the target's probe
    run (descriptive only), or None with the reason where they are not in this checkout."""
    from scripts import x0_massmean as MM
    from scripts import x47_atoms as A47

    try:
        return A47.pointer_basis(target), MM.pointer_means(R.STATES[target]), R.STATES[target]
    except (KeyError, FileNotFoundError) as e:
        return None, None, f"not available: {e!r}"


def stage_run(name: str, why: str, n_items: int = N_ITEMS, n_test: int = N_TEST_POOL, n_mean: int = N_MEAN) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "53.8 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"53.8 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": TEST,
         "spec": "jobs/c3/batch53.yaml (critic_1125, item 6)", "question": NO_PREDICTION,
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)}, "layer": layer, "doses": list(DOSES),
         "rule_verbatim": RULE_VERBATIM, "rule": RULE, "design": DESIGN, "arms": arm_names(0),
         "centered_verbatim": CENTERED_VERBATIM, "variants": VARIANT_TEXT, "headline": HEADLINE,
         "n": {"items": n_items, "test_pool": n_test, "mean_pool": n_mean, "gen_per_condition": N_GEN},
         "gate_min": X.GATE, "seeds": {"scenes": R.SEED, "random_directions": RAND_SEED, "bootstrap": X.BOOT_SEED,
                                       "examples": X.EXAMPLES_SEED}, "sealed": "none (no prediction)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    model = load_model()
    tok = model.tokenizer
    dev = model.device
    generated, dropped = c0_cases(tok)
    test, mean = split_pools(generated, n_test, n_mean)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp = X.competence(model, test, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in test])) for w in X.READERS}
    ok = [c for c in test if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                 for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    passed = all(a >= X.GATE for a in acc.values())
    chosen = [{**c, "slots": slot_info(tok, c)} for c in ok[:n_items]] if passed else []
    gate = {"c0_generated": len(generated), "test_pool": len(test), "mean_pool": len(mean), "org_read_accuracy": acc,
            "pass": passed, "gate_min": X.GATE, "eligible": len(ok), "used": len(chosen),
            "generator_dropped": dropped}  # fmt: skip
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    X.write_jsonl(out / "competence.jsonl", comp)
    if not gate["pass"] or not chosen:  # the verdict says "not tested"; nothing is read
        print(f"53.8: not tested, the gate fixed in advance missed or no eligible scene: {gate}", flush=True)
        return out
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in chosen])
    U, _, refs = pointer_refs(target)
    Ut = torch.tensor(U, dtype=torch.float32) if U is not None else None
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        emb = model.hf.get_input_embeddings().weight
        hm, em, used = [], [], []
        for c in progress(mean, f"53.8: mention states at L{layer}, mean pool (scene)"):
            pos = mention_positions(tok, c)
            if pos is None:
                continue
            ids = c["readers"][X.LOOKUP]["ids"]["org"]
            h = model.run(torch.tensor([ids], device=dev), record=(layer,))[1][layer]
            hm.append(h[pos].float().cpu().clone())
            em.append(emb[torch.tensor([ids[p] for p in pos], device=emb.device)].float().cpu().clone())
            used.append({"scene": c["scene"], "context": c["context"], "positions": pos,
                         "items": [x for x, _ in W.slots_of(c["context"])]})  # fmt: skip
        assert used, "no mean-pool scene with one-token mentions"
        h_m, e_m = torch.stack(hm), torch.stack(em)  # [n, 3, d]
        codes = mention_codes(h_m, e_m)  # [3, d]
        np.savez(out / "codes.npz", codes=codes.numpy(), n=np.array(len(used)),
                 norm_h=h_m.norm(dim=-1).mean(0).numpy(), norm_e=e_m.norm(dim=-1).mean(0).numpy())  # fmt: skip
        X.write_jsonl(out / "mean_cases.jsonl", used)
        ho, hs = [], []
        for c in progress(chosen, f"53.8: the real identity change at the bridge word, L{layer} (scene)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            for v, store in (("org", ho), ("alt", hs)):
                store.append(model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][c["pos"]].float()
                             .cpu().clone())  # fmt: skip
        delta = torch.stack(hs) - torch.stack(ho)  # [n, d], CPU
        gen = torch.Generator().manual_seed(RAND_SEED)
        rows, norms = [], []
        for i, c in enumerate(progress(chosen, f"53.8: reads, {len(arm_names(0))} rows x 2 readers (scene)")):
            sl = c["slots"]
            size = float(delta[i].norm())
            r = torch.randn(delta.shape[1], generator=gen)
            vecs = arm_vectors(codes, r, sl["slot_a"], size, delta[i])
            diff = codes[sl["slot_b"]] - codes[sl["slot_a"]]
            norms.append({"scene": c["scene"], "slot_a": sl["slot_a"], "slot_b": sl["slot_b"],
                          "norm_delta": round(size, 4), "norm_U_delta": None if Ut is None else
                          round(float((Ut.T @ delta[i]).norm()), 4),
                          "cos_delta_codes_b_minus_a": round(float(delta[i] @ diff / (size * diff.norm() + 1e-30)), 4),
                          "arm_norms": {a: round(float(v.norm()), 4) for a, v in vecs.items()}})  # fmt: skip
            names = arm_names(sl["slot_a"])
            edits = [{}] + [{layer: AddRows(vecs[a][None].to(dev), [c["pos"]])} for a in names[1:]]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)
                for a, lg in zip(names, logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a, "top": top,
                                 "top_text": model.decoded[top], "kept": int(top == rd["tok_A"]),
                                 "slot": lookup_slot(top, sl["tokens"]) if w == X.LOOKUP else None})  # fmt: skip
    info = {"pointer_refs": refs, "mean_pool_used": len(used)}  # the manifest stays as written before the run
    (out / "run_info.json").write_text(json.dumps(info, indent=2) + "\n")
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    print(
        f"wrote {out}: {len(rows)} reads of {len(chosen)} scenes; codes from {len(used)} mean-pool scenes", flush=True
    )
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def label(x_rand: float, x_y: float) -> str:
    """Dan's rule on the 2x point estimates: X - random and X - Y (EPS at the bars)."""
    if x_rand >= SHARED_RAND - EPS and x_y >= SHARED_Y - EPS:
        return "shared"
    if x_rand <= NO_RAND + EPS:
        return "no"
    return "between"


def gate_status(gate: dict) -> str | None:
    """None if the run was read; else why not: "not tested (gate x < 0.80)" (the lower reader's accuracy)."""
    if not gate["pass"]:
        a = min(gate["org_read_accuracy"].values())
        return f"not tested (gate {a:.3f} < {gate['gate_min']:.2f})"
    if not gate["used"]:
        return "not tested (no eligible scene)"
    return None


def pair_rows(rows: list[dict], cases: list[dict], prefix: str = VARIANTS[HEADLINE]) -> list[dict]:
    """Per (scene, X slot k), Y = the scene's remaining slot: per dose the lookup's role (X / Y / original / other)
    under X's vector, Y's version (prefix: "code" uncentered, "ccode" centered) and the random vector."""
    lk = {(r["scene"], r["arm"]): r["slot"] for r in rows if r["reader"] == X.LOOKUP}
    out = []
    for c in cases:
        a = c["slots"]["slot_a"]
        others = [k for k in SLOTS if k != a]
        for x in others:
            (y,) = [k for k in others if k != x]
            rec: dict[str, Any] = {"scene": c["scene"], "entity": c["bridge"], "x": x, "y": y, "a": a}
            for d in DOSES:
                arm = {"X": f"{prefix}{x}_x{d}", "Y": f"{prefix}{y}_x{d}", "R": f"rand_x{d}"}
                for kind, name in arm.items():
                    rec[f"{kind}_x{d}"] = role(lk[(c["scene"], name)], x, y, a)
            out.append(rec)
    return out


def share_ci(hits: list[int], entities: list[str], n_boot: int) -> list[float]:
    boot = X.resampled_rates({"s": hits}, entities, n_boot)["s"]
    return [float(np.mean(hits)), *X.interval(boot)]


def dose_cell(pairs: list[dict], d: int, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """X's share under X / Y / random at dose d, their paired differences, every kind's roles; CIs over the bridge item."""
    ents = [p["entity"] for p in pairs]
    hits = {k: [int(p[f"{k}_x{d}"] == "X") for p in pairs] for k in KINDS}
    boot = X.resampled_rates(hits, ents, n_boot)
    pt = {k: float(np.mean(v)) for k, v in hits.items()}
    roles = {k: {ro: share_ci([int(p[f"{k}_x{d}"] == ro) for p in pairs], ents, n_boot) for ro in ROLES}
             for k in KINDS}  # fmt: skip
    return {"n": len(pairs), "scenes": len({p["scene"] for p in pairs}), "entities": len(set(ents)),
            **{k: [pt[k], *X.interval(boot[k])] for k in KINDS},
            "X_minus_R": [pt["X"] - pt["R"], *X.interval(boot["X"] - boot["R"])],
            "X_minus_Y": [pt["X"] - pt["Y"], *X.interval(boot["X"] - boot["Y"])], "roles": roles}  # fmt: skip


def collateral(rows: list[dict], cases: list[dict], n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """The clean answers kept per arm kind (none, whole; per dose the code vectors pooled, random, the centered vectors
    pooled), both readers; the whole change's lookup sent to B's locker (the real change's own effect)."""
    by = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    ent = {c["scene"]: c["bridge"] for c in cases}
    groups: dict[str, list[tuple[str, str]]] = {"none": [], "whole": []}
    for c in cases:
        for a in arm_names(c["slots"]["slot_a"]):
            kind = a if a in ("none", "whole") else a.split("_x")[0].rstrip("0123456789") + a[a.index("_x") :]
            groups.setdefault(kind, []).append((c["scene"], a))
    out: dict[str, Any] = {}
    for kind, keys in groups.items():
        es = [ent[s] for s, _ in keys]
        out[kind] = {READER_NAME[w]: share_ci([by[(s, w, a)]["kept"] for s, a in keys], es, n_boot) for w in X.READERS}
        out[kind]["n"] = len(keys)
    sw = [int(by[(c["scene"], X.LOOKUP, "whole")]["slot"] == c["slots"]["slot_b"]) for c in cases]
    out["whole_lookup_to_B"] = share_ci(sw, [c["bridge"] for c in cases], n_boot)
    return out


def geometry(codes: np.ndarray, mu: dict[int, np.ndarray] | None) -> dict[str, Any]:
    """The slot vectors' norms and pairwise cosines, raw and centered (Dan 12:10); each slot-specific part's norm
    ||c_k - mean over slots|| and its share of ||c_k||; per slot pair the cosine of the difference with the pointer
    means' (the same for raw and centered: centering moves every slot by the same vector)."""
    cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30))  # noqa: E731
    pairs = [(j, k) for j in SLOTS for k in SLOTS if j < k]
    cc = centered(codes)
    norm = [float(np.linalg.norm(c)) for c in codes]
    spec = [float(np.linalg.norm(c)) for c in cc]
    out: dict[str, Any] = {"norm": [round(v, 3) for v in norm],
                           "cos": {f"{j}-{k}": round(cos(codes[j], codes[k]), 4) for j, k in pairs},
                           "slot_specific_norm": [round(v, 3) for v in spec],
                           "slot_specific_share": [round(s / n, 4) for s, n in zip(spec, norm, strict=True)],
                           "cos_centered": {f"{j}-{k}": round(cos(cc[j], cc[k]), 4) for j, k in pairs},
                           "diff_over_norm": {f"{j}-{k}": round(float(np.linalg.norm(codes[k] - codes[j])
                                                                       / np.linalg.norm(codes[j])), 4)
                                              for j, k in pairs}}  # fmt: skip
    if mu is not None:
        out["cos_diff_vs_pointer_means"] = {f"{j}-{k}": round(cos(codes[k] - codes[j], mu[k] - mu[j]), 4)
                                            for j, k in pairs}  # fmt: skip
    return out


def variant_numbers(pairs: list[dict], n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One construction's cells per dose, its label by the rule's thresholds at RULE_DOSE and the per-slot split."""
    cells = {str(d): dose_cell(pairs, d, n_boot) for d in DOSES}
    rc = cells[str(RULE_DOSE)]
    lab = label(rc["X_minus_R"][0], rc["X_minus_Y"][0])
    per_slot = {}
    for k in SLOTS:
        mine = [p for p in pairs if p["x"] == k]
        if mine:
            per_slot[str(k)] = {"n": len(mine), **{kind: round(float(np.mean([p[f"{kind}_x{RULE_DOSE}"] == "X" for p in mine])), 4)
                                                   for kind in KINDS}}  # fmt: skip
    return {"cells": cells, "label": lab, "text": LABELS[lab], "per_slot": per_slot}


def run_numbers(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    gate = json.loads((src / "gate.json").read_text())
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "gate": gate}
    why = gate_status(gate)
    if why is not None:
        return {**base, "status": why, "label": None, "text": why}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = X.read_jsonl(src / "cases.jsonl")
    variants = {v: variant_numbers(pair_rows(rows, cases, prefix), n_boot) for v, prefix in VARIANTS.items()}
    lab = variants[HEADLINE]["label"]
    norms = X.read_jsonl(src / "norms.jsonl")
    med = {k: round(float(np.median([r[k] for r in norms])), 4)
           for k in ("norm_delta", "norm_U_delta", "cos_delta_codes_b_minus_a") if norms and norms[0].get(k) is not None}  # fmt: skip
    codes = np.load(src / "codes.npz")
    info = json.loads((src / "run_info.json").read_text())
    _, mu, _ = pointer_refs(base["target"])
    return {**base, "status": "tested", "label": lab, "text": LABELS[lab], "headline": HEADLINE, "variants": variants,
            "collateral": collateral(rows, cases, n_boot), "norms_median": med,
            "geometry": {**geometry(codes["codes"], mu), "n_mean": int(codes["n"]),
                         "mention_state_norm": [round(float(v), 3) for v in codes["norm_h"]],
                         "embedding_norm": [round(float(v), 3) for v in codes["norm_e"]]},
            "mean_pool_used": info["mean_pool_used"], "pointer_refs": info["pointer_refs"]}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def short(target: str) -> str:
    return MODEL_SHORT.get(target, target)


def model_slots(models: list[dict]) -> list[dict]:
    """The four figure slots in order: a run's numbers, or a grey status (pending / not designed); a run of any other
    target after them (never dropped)."""
    have = {m["target"]: m for m in models}
    out = [have.get(t) or {"target": t, "status": "pending" if t in RUNS else NOT_DESIGNED} for t in MODEL_ORDER]
    return out + [m for m in models if m["target"] not in MODEL_ORDER]


def figure(models: list[dict], path: Path) -> None:
    """Per model slot: X's share (lookups sent to X's locker) under X's vector, Y's version and random, at 1x and 2x, for
    the pre-specified (uncentered) construction and the centered one beside."""
    from scripts import story_style as SS

    plt = SS.setup()
    slots = model_slots(models)
    groups = [(v, d) for v in VARIANTS for d in DOSES]
    fig, axes = plt.subplots(1, len(slots), figsize=(SS.WIDTH * 1.8, 4.1), sharey=True, squeeze=False)
    cols = {"X": SS.COL["identity"], "Y": SS.COL["position"], "R": SS.COL["control"]}
    w = 0.26
    for ax, mdl in zip(axes[0], slots, strict=True):
        ax.set_title(short(mdl["target"]) + (f", L{mdl['layer']}" if "layer" in mdl else ""), loc="left")
        ax.set_ylim(0, 1)
        ax.set_xlim(-0.6, len(groups) - 0.4)
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([f"{d}x" + ("\ncentered" if v == "centered" else "\nas fixed") for v, d in groups])
        if mdl["status"] != "tested":
            SS.empty(ax, textwrap.fill(mdl["status"], 22))
            continue
        ax.axvline(len(DOSES) - 0.5, color="#999999", lw=0.8)
        for i, (var, d) in enumerate(groups):
            c = mdl["variants"][var]["cells"][str(d)]
            for j, kind in enumerate(KINDS):
                v = c[kind]
                ax.bar(i + (j - 1) * w, v[0], w, color=cols[kind], label=KIND_TEXT[kind] if i == 0 else None)
                ax.errorbar(
                    i + (j - 1) * w, v[0], yerr=[[v[0] - v[1]], [v[2] - v[0]]], color="#333333", lw=1, capsize=2
                )
        text = f"as fixed: {mdl['text']}; centered (beside): {mdl['variants']['centered']['text']}"
        ax.text(0.02, 0.97, textwrap.fill(text, 26), transform=ax.transAxes, va="top", fontsize=SS.LABEL_PT)
    axes[0][0].set_ylabel("lookups sent to X's locker")
    handles, labels = next(((h, lb) for ax in axes[0] for h, lb in [ax.get_legend_handles_labels()] if h), ([], []))
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, fontsize=SS.LABEL_PT)
    SS.title(fig, "53.8: does a mention's slot code move the lookup? (UNVERIFIED)",
             f"At the bridge word at L, 1x / 2x a real identity change's size; rule at {RULE_DOSE}x; headline: as fixed "
             "(uncentered); centered beside (Dan 12:10); 95% CIs over the bridge item.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.1, 1, 0.86))
    fig.savefig(path, dpi=100)
    plt.close(fig)


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    cases = X.read_jsonl(src / "cases.jsonl")
    reads = X.read_jsonl(src / "outcomes.jsonl")
    pick = sorted(random.Random(seed).sample(range(len(cases)), min(k, len(cases))))
    lines = [f"## {run}: {len(pick)} random scenes of {len(cases)} (seed {seed})", ""]
    for i in pick:
        c = cases[i]
        sl = c["slots"]
        slots = "; ".join(
            f"slot {j}: {x} (locker {d})" for j, (x, d) in enumerate(zip(sl["items"], sl["digits"], strict=True))
        )
        lines += [f"### {c['scene']}: A = {c['bridge']} (slot {sl['slot_a']}), B = {c['cf_bridge']} (slot {sl['slot_b']}); "
                  f"{slots}", "", f"O: {c['context']}", "", f"S_B: {c['cf_context']}", "",
                  "| reader | arm | top token | lookup's slot | clean answer kept |", "|---|---|---|---|---|"]  # fmt: skip
        for r in reads:
            if r["scene"] == c["scene"]:
                slot = "-" if r["slot"] is None else ("other" if r["slot"] < 0 else r["slot"])
                lines.append(f"| {READER_NAME[r['reader']]} | {r['arm']} | {r['top_text']!r} | {slot} | {r['kept']} |")
        lines.append("")
    return lines


def rule_table(models: list[dict], var: str) -> list[str]:
    """The rule's numbers at RULE_DOSE for one construction, one row per model slot (grey statuses kept)."""
    lines = [f"| model | layer | n (scene, X) | X's share at {RULE_DOSE}x | Y's version | random | X - random | X - Y | "
             f"label ({var}) |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in model_slots(models):
        name = short(mdl["target"])
        if mdl["status"] != "tested":
            lines.append(f"| {name} | {mdl.get('layer', '-')} | - | - | - | - | - | - | {mdl['status']} |")
            continue
        vn = mdl["variants"][var]
        c = vn["cells"][str(RULE_DOSE)]
        text = f"**{vn['text']}**" if var == HEADLINE else vn["text"]
        lines.append(f"| {name} | {mdl['layer']} | {c['n']} ({c['scenes']} scenes, {c['entities']} items) | "
                     f"{fmt(c['X'])} | {fmt(c['Y'])} | {fmt(c['R'])} | {fmt(c['X_minus_R'])} | {fmt(c['X_minus_Y'])} | "
                     f"{text} |")  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    models = [run_numbers(r, n_boot) for r in runs]
    out = RESULTS / f"{EXP}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 53.8: a binding-ID test for the lookup's identity code", "",
             f"Batch 53, test 53.8 (jobs/c3/batch53.yaml critic_1125, item 6; Dan 11:25, stretch; {NO_PREDICTION}). "
             "UNVERIFIED.", "", f"Dan's text, verbatim: \"{RULE_VERBATIM}\"", "", f"Rule as computed: {RULE}.", "",
             f"Centered arm (Dan 12:10, jobs/c3/batch53.yaml decisions_1210b item 1, verbatim; added before any run): "
             f"\"{CENTERED_VERBATIM}\" The headline is the pre-specified (uncentered) arm's label; the centered arm's "
             "label, by the same thresholds, is beside.", "",
             "Design (fixed before any run):", ""] + [f"- {k}: {v}" for k, v in DESIGN.items()] + [""]  # fmt: skip
    lines += ["Headline, the pre-specified arm (uncentered c_k):", "", *rule_table(models, HEADLINE), "",
              "Beside, the centered arm (c_k - mean over slots; Dan 12:10), same doses, controls and thresholds:", "",
              *rule_table(models, "centered")]  # fmt: skip
    tested = [m for m in models if m["status"] == "tested"]
    if tested:
        lines += ["", "Slot vectors (Dan 12:10: the cosines and the norm of the slot-specific part c_k - mean over "
                  "slots; with three slots the centered vectors sum to zero, so their cosines are about -0.5 when "
                  "their norms are alike):", "",
                  "| model | slot | norm c_k | norm of the slot-specific part | its share of norm c_k |",
                  "|---|---|---|---|---|"]  # fmt: skip
        for mdl in tested:
            g = mdl["geometry"]
            for k in SLOTS:
                lines.append(f"| {short(mdl['target'])} | {k} | {g['norm'][k]:.2f} | {g['slot_specific_norm'][k]:.2f} | "
                             f"{g['slot_specific_share'][k]:.3f} |")  # fmt: skip
        lines.append("")
        for mdl in tested:
            g = mdl["geometry"]
            lines.append(f"- {short(mdl['target'])}: cosines between slot vectors {g['cos']}; between their "
                         f"slot-specific parts {g['cos_centered']}; slot differences vs the pointer means' "
                         f"{g.get('cos_diff_vs_pointer_means', 'not available')}.")  # fmt: skip
        lines += ["", "Every dose: the lookup's answer under each arm kind, by role (X's locker / Y's / A's own = "
                  "original / other); shares with cluster-bootstrap CIs over the bridge item:", "",
                  "| model | construction | dose | arm | X | Y | original | other |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for mdl in tested:
            for var in VARIANTS:
                for d in DOSES:
                    c = mdl["variants"][var]["cells"][str(d)]
                    for kind in KINDS:
                        r = c["roles"][kind]
                        lines.append(f"| {short(mdl['target'])} | {var} | {d}x | {KIND_TEXT[kind]} | {fmt(r['X'])} | "
                                     f"{fmt(r['Y'])} | {fmt(r['original'])} | {fmt(r['other'])} |")  # fmt: skip
        lines += ["", "Collateral (the clean answers kept) and the real change's own effect:", "",
                  "| model | arm | n | lookup kept | recall kept |", "|---|---|---|---|---|"]  # fmt: skip
        for mdl in tested:
            col = mdl["collateral"]
            for kind, v in col.items():
                if kind != "whole_lookup_to_B":
                    lines.append(
                        f"| {short(mdl['target'])} | {kind} | {v['n']} | {fmt(v['lookup'])} | {fmt(v['recall'])} |"
                    )
            lines.append(f"| {short(mdl['target'])} | whole: lookup sent to B's locker | - | "
                         f"{fmt(col['whole_lookup_to_B'])} | - |")  # fmt: skip
        lines += [""]
        for mdl in tested:
            per_slot = {v: mdl["variants"][v]["per_slot"] for v in VARIANTS}
            lines.append(f"- {short(mdl['target'])}: per X slot at {RULE_DOSE}x (X / Y / random) {per_slot}; "
                         f"medians {mdl['norms_median']}; vectors {mdl['geometry']}; mean pool {mdl['mean_pool_used']} "
                         f"scenes; pointer refs {mdl['pointer_refs']}; gate {mdl['gate']['org_read_accuracy']} (pass "
                         f"{mdl['gate']['pass']}), eligible {mdl['gate']['eligible']} of {mdl['gate']['test_pool']}, "
                         f"used {mdl['gate']['used']}.")  # fmt: skip
    for mdl in models:
        if mdl["status"] != "tested":
            lines.append(f"- {short(mdl['target'])}: {mdl['status']}; O's read accuracy per "
                         f"reader {mdl['gate']['org_read_accuracy']} (gate {mdl['gate']['gate_min']:.2f} each, fixed in "
                         f"advance, not lowered), eligible {mdl['gate']['eligible']}.")  # fmt: skip
    lines += ["", f"Figure: {EXP}.png"]
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "question": NO_PREDICTION, "rule_verbatim": RULE_VERBATIM,
                                                  "rule": RULE, "centered_verbatim": CENTERED_VERBATIM,
                                                  "headline": HEADLINE, "design": DESIGN, "models": models},
                                                 indent=1) + "\n")  # fmt: skip
    figure(models, out / f"{EXP}.png")
    ex = ["# 53.8 examples (verify pack): the scene's slots, O and S_B, every arm's top token. UNVERIFIED.", ""]
    for mdl in tested:
        ex += example_lines(mdl["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x53_bindid/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the runs (default: every one of RUNS present)")
    ap.add_argument("--why", default="batch 53, test 53.8 (jobs/c3/batch53.yaml critic_1125, item 6)")
    ap.add_argument("--n-items", type=int, default=N_ITEMS)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.n_items)
    else:
        runs = a.runs or [r for r in RUNS.values() if (RESULTS / r / "gate.json").exists()]
        assert runs, "no 53.8 run with a gate.json"
        stage_verdict(runs, a.n_boot)


if __name__ == "__main__":
    main()
