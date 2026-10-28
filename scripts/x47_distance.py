"""x47_distance (batch 47, test 47.16, amendment 5; Dan 28 Oct ~03:10; jobs/c3/batch47.yaml, design and rule fixed
in advance; Q47.16 in predictions/2026-10-28_dan.md): does the address survive distance?

As computed (fixed before any run; Dan may override before the run; the specs jobs/c3/x47_16_*.yaml repeat it):

Scenes (plan, CPU). x6_routes' C2 scenes (its generator, seed 2510: the same base scenes as the routes runs; the
first 420 C2 candidates) with k neutral filler sentences between the last locker sentence and the first pick sentence
in O and in S alike, k in {0, 5, 20, 50}. The fillers: a fixed pool of 60 sentences (FILLERS: no item, no person, no
digit or number word, no locker / pick / hall wording; the plan checks them against the target's item and people
pools); per base scene one seeded draw (seed 4716 keyed by the scene) of 50 fillers, of which the first k are
inserted, so the k = 5 block is a prefix of the k = 20 block and that of the k = 50 block (x6_routes --filler-tokens
fits one sentence; the block is rendered here, x6_routes untouched). Each variant is re-encoded with x6_routes.encode
(the bridge word one token at one index shared by O and S, the readers' prompts the same through it); the token count
of the block is reported per k and tokenizer (about 12 tokens per sentence: ~0 / 60 / 240 / 600).

Run (GPU, SEALED: per-item outputs only). In the order k = 0, 5, 20, 50: X0's competence on every candidate at k
(8 greedy tokens and the read, unedited O and S, both readers), the gate = O's read accuracy >= 0.80 per reader over
the candidates; at the first k whose gate fails the job records it ("stopped_at") and skips every larger k. Chosen:
the first 300 base scenes (generation order) eligible at every k that passed (both readers say and read O's and S's
answers right), so the k cells are paired. At each passed k, at the bridge word at L (X.PREDICTED), on O, both
readers: none; whole (Delta = h_S - h_O); without U (the pointer basis fit on the fresh scenes, x0_massmean
pointer_means / subspaces' Alf, not refit) and without a random part of U's share (X0's random subspace, seed 888 +
L); the pointer swap of x8_write at s = 2: h + 2 (mu_t - mu_j) for both other slots t (j = the bridge's locker slot in
O; mu = the layout-free class means behind U, not refit), each against a random direction of the same norm (seed 4717
keyed by the scene and t). O's bridge-word state at every k is saved (states.npz) for the probe and the code's
shift: beta_k = <U U^T (h_k - h_0), mu_{j-1} - mu_j> / ||mu_{j-1} - mu_j||^2 for j in {1, 2} (x8 order's B2
convention: a sentence between the lockers and the picks; the same base scene at k = 0 is the reference; j = 0 has no
B2 step and beta_next, the j + 1 step, is recorded beside for every j, descriptive).

Verdict (CPU; refuses until Q47.16's "Dan:" line is committed). Per k: lookup and recall accuracy unedited (the
gate's, over the candidates); the slot probe at the bridge word (x0_probe (b): target = the bridge's locker slot, 5
folds by bridge entity, chance / majority / layout beside); identity / position / value shares under the whole
change; the position share without U against without its random part (the cut beyond random); the swap's share to
the target (pooled over the two targets) against the random direction's; the recall's kept share per arm; mean beta
with a cluster-bootstrap CI. Shares with cluster-bootstrap CIs over bridge items (10,000 resamples, seed 0); point
estimates decide, EPS 1e-9 at the bars. Labels per model, in this order: "breaks at k" if the gate failed at some k
(that k reported; the larger ks were not run); "distance-robust address" if at every k the position share and the
probe are within 0.10 of k = 0 and the swap's target share within 0.15; "address near, identity far" if at k = 50 the
position share is >= 0.20 below k = 0 and the identity share >= 0.20 above it, with both readers' accuracy >= 0.8;
else "none of the three". Fig 8c at scale: "the code's shift stays <= 0.25" if mean beta <= 0.25 at every k > 0.

uv run python scripts/x47_distance.py plan                                                 # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_distance.py run --name qwen35_9b_x47_16    # GPU (sealed)
uv run python scripts/x47_distance.py verdict --runs qwen35_9b_x47_16 muse30_x47_16        # CPU, after Dan's Q47.16
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_massmean as MM
from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x47_six as Q

EXP = "x47_distance"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml (47.16)"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.16"
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_16", "muse-glimmer-30b": "muse30_x47_16"}
KS = (0, 5, 20, 50)
N_CAND, N_ITEMS = 420, 300
FILLER_SEED, RAND_SEED = 4716, 4717
S_WRITE = 2
NEAR, PROBE_NEAR, SWAP_NEAR, FAR, ACC_MIN, BETA_MAX = 0.10, 0.10, 0.15, 0.20, 0.8, 0.25
EPS = 1e-9  # a value at a bar counts as at the bar
ROUTES = ("identity", "position", "value", "original", "other")
DELTA_ARMS = ("none", "whole", "no_alf", "no_alf_rand")
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change h_S - h_O at the bridge word",
    "no_alf": "the whole change without its part in U (the fresh-scene pointer basis, not refit)",
    "no_alf_rand": "the whole change without a random part of U's share",
    "write": f"x8's pointer swap at s = {S_WRITE}: h + {S_WRITE} (mu_t - mu_j), j the bridge's slot in O, t the target",
    "random": "a random direction of the swap's norm (one per scene and target)",
}
LABELS = ("breaks", "distance-robust address", "address near, identity far", "none of the three")
FILLERS: tuple[str, ...] = (
    "The weather stayed mild and quiet for most of the afternoon.",
    "Everyone agreed that the meeting had gone on far too long.",
    "A light rain began to fall just after the doors were closed.",
    "Nobody could remember when the corridor lights had last been changed.",
    "The old radio in the corner played softly through the whole day.",
    "Somebody had left a pile of folded towels near the front desk.",
    "It was later than usual when the cleaning crew finally arrived.",
    "The windows on the north side had been open since early morning.",
    "The coffee in the break room had gone cold long before noon.",
    "A thin layer of dust covered the shelves along the back wall.",
    "The bus to the city centre was running a few minutes late again.",
    "Most of the chairs had been stacked neatly against the far wall.",
    "The paint on the garden fence was starting to peel in places.",
    "A faint smell of fresh bread drifted in from the bakery next door.",
    "The elevator made its usual soft hum as it climbed to the top floor.",
    "Someone had drawn the curtains before the sun had fully set.",
    "The printer upstairs had jammed again before lunch.",
    "The grass in the courtyard had grown tall over the summer.",
    "The library closed early because of the holiday weekend.",
    "A stack of unopened mail sat on the table by the entrance.",
    "The kettle took longer than expected to come to the boil.",
    "The streetlights flickered on as the evening grew darker.",
    "The parking lot was almost empty by the time the rain stopped.",
    "The kitchen clock had been running slow for several weeks.",
    "A gentle breeze moved the papers that lay on the desk.",
    "The train slowed as it passed through the small station.",
    "The heating in the office had been turned off for the night.",
    "The road along the river had been repaved earlier that spring.",
    "The umbrella stand by the door was already full when we arrived.",
    "The conference room smelled faintly of fresh paint.",
    "The clouds broke apart briefly to let some sunlight through.",
    "The vending machine in the lobby was out of order again.",
    "Fresh snow had covered the path leading up to the gate.",
    "The pages of the old notebook had turned yellow with age.",
    "The sound of distant traffic carried across the quiet park.",
    "The laundry had been left out on the line overnight.",
    "A new coat of varnish made the wooden floor shine.",
    "The market stalls were packed away before the storm arrived.",
    "The lamp on the bedside table gave off a warm glow.",
    "Several leaves had gathered in the corner of the balcony.",
    "The water in the fountain had been drained for the winter.",
    "The morning fog lifted slowly from the fields outside town.",
    "The ticket office opened a little later than it had promised.",
    "The curtains in the waiting room were a faded shade of green.",
    "The soup had simmered on the stove for most of the evening.",
    "The paint shop on the corner had changed its opening hours.",
    "The garden gate creaked whenever the wind grew stronger.",
    "The bookshop had rearranged its front window for the season.",
    "The tiles by the entrance had been polished that morning.",
    "The night shift ended just as the early buses started running.",
    "The porch light had been left on through the whole night.",
    "The kitchen window looked out over a row of tidy gardens.",
    "The last of the summer fruit had been sold by midday.",
    "The office plants had been watered before the long weekend.",
    "The village square was quiet after the market had closed.",
    "The ferry crossing took longer because of the strong tide.",
    "The corridor carpet had been replaced over the holidays.",
    "The sign above the shop door needed a fresh coat of paint.",
    "A delivery van had blocked the narrow lane for nearly an hour.",
    "The museum stayed open late on the opening evening of the month.",
)
NUMBER_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "first",
                "second", "third", "twice")  # fmt: skip
BANNED_WORDS = ("locker", "lockers", "pick", "picked", "picks", "hall", "halls")


# ---- fillers and scenes (text) -------------------------------------------------------------------------------------


def filler_checks(fillers: tuple[str, ...], items: list[str], people: list[str]) -> list[str]:
    """What must hold for the filler pool ([] if all hold): distinct, one sentence each (no '. ' inside, a final
    '.'), no digit, number word, banned word, item name or person name."""
    bad = []
    if len(set(fillers)) != len(fillers):
        bad.append("a filler repeats")
    words = set(NUMBER_WORDS) | set(BANNED_WORDS)
    for f in fillers:
        if not f.endswith(".") or ". " in f or "\n" in f:
            bad.append(f"not one sentence: {f!r}")
        if re.search(r"\d", f):
            bad.append(f"a digit: {f!r}")
        toks = set(re.findall(r"[A-Za-z]+", f))
        low = {t.lower() for t in toks}
        if low & words:
            bad.append(f"a number or banned word: {f!r}")
        if low & {x.lower() for x in items}:
            bad.append(f"an item name: {f!r}")
        if toks & set(people):
            bad.append(f"a person's name: {f!r}")
    return bad


def filler_block(base_scene: str, k: int, seed: int = FILLER_SEED) -> list[str]:
    """The base scene's k fillers: the first k of one seeded draw of max(KS) from the pool (prefixes nest)."""
    rng = random.Random(f"{seed}|{base_scene}")
    return rng.sample(FILLERS, max(KS))[:k]


def with_fillers(context: str, block: list[str]) -> str:
    """The block between the last locker sentence and the first pick sentence (x8_write.with_filler 'between')."""
    return W.with_filler(context, " ".join(block), "between") if block else context


def cases_at(tok, base: list[dict], k: int) -> tuple[list[dict], collections.Counter]:
    """Each base C2 case at k: O and S with the same filler block, re-encoded (x6_routes.encode); drops counted."""
    from scripts import suite_v1 as S

    legs = R.pools(tok)[0]
    out, dropped = [], collections.Counter()
    for c in base:
        assert c["condition"] == "C2", f"{c['scene']}: 47.16 runs on C2 scenes"
        block = filler_block(c["scene"], k)
        o, s = with_fillers(c["context"], block), with_fillers(c["cf_context"], block)
        asked = R.asked_of(c)
        case, why = R.encode(tok, o, s, asked, c["bridge"], c["cf_bridge"], legs, c["expect"], "C2",
                             f"{c['scene']}-k{k}", c["rendering"])  # fmt: skip
        if case is None:
            dropped[f"k = {k}: {why}"] += 1
            continue
        slots = W.slots_of(o)
        assert [x for x, _ in slots] == [x for x, _ in W.slots_of(c["context"])], f"{c['scene']}: the slots moved"
        pick = Q.pick_index(o, asked)
        case.update({"k": k, "base_scene": c["scene"], "fillers": block, "j": [x for x, _ in slots].index(c["bridge"]),
                     "slot_tokens": [S.answer_token(tok, str(d), "digit") for _, d in slots], "asked": asked,
                     "pick_index": pick, "layout": P.layout(o, pick), "move": list(W.pointer_move(case))})  # fmt: skip
        out.append(case)
    return out, dropped


def base_cases(tok, n: int = N_CAND) -> list[dict]:
    """The routes test's first n C2 candidates (x6_routes.scenes, seed 2510)."""
    cases, _ = R.scenes(tok, R.N_GEN)
    return [c for c in cases if c["condition"] == "C2"][:n]


def stage_plan(n: int = N_CAND, k_prompts: int = 5) -> dict:
    """Tokenizer only: the filler checks, per k the cases, drops, prompt and block token counts, the bridge index, and
    k_prompts rendered prompts (base scene 1 at every k, the lookup's O as read; base scene 2 at the largest k, the
    recall's)."""
    from scripts import x45m

    tok = x45m.tokenizer()
    _, animals, people = R.pools(tok)
    bad = filler_checks(FILLERS, animals, people)
    assert not bad, f"fillers: {bad}"
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    base = base_cases(tok, n)
    blob: dict = {"target": pins.TARGET, "layer": X.PREDICTED.get(pins.TARGET), "prefix": pins.RUN_PREFIX,
                  "fillers": len(FILLERS), "filler_tokens": W.filler_lengths(tok) | {
                      f: len(tok(" " + f, add_special_tokens=False)["input_ids"]) for f in FILLERS},
                  "base_cases": len(base), "entities": len({c["bridge"] for c in base}), "per_k": {}, "prompts": []}  # fmt: skip
    length0: dict[str, int] = {}
    for k in KS:
        cases, dropped = cases_at(tok, base, k)
        for c in cases:
            ids = c["readers"][X.LOOKUP]["ids"]
            assert tok.decode([ids["org"][c["pos"]]]).strip() == c["bridge"], f"{c['scene']}: the bridge token"
            if k == 0:
                length0[c["base_scene"]] = len(ids["org"])
        lengths = [len(c["readers"][X.LOOKUP]["ids"]["org"]) for c in cases]
        block = [len(c["readers"][X.LOOKUP]["ids"]["org"]) - length0[c["base_scene"]] for c in cases
                 if c["base_scene"] in length0]  # fmt: skip
        blob["per_k"][str(k)] = {"cases": len(cases), "dropped": dict(dropped), "prompt_tokens": [min(lengths), max(lengths)],
                                 "block_tokens": [min(block), int(np.median(block)), max(block)] if block else None,
                                 "bridge_token_index": [min(c["pos"] for c in cases), max(c["pos"] for c in cases)],
                                 "layouts": dict(collections.Counter(c["layout"] for c in cases))}  # fmt: skip
        if cases:
            c = cases[0]
            blob["prompts"].append({"scene": c["scene"], "k": k, "reader": "lookup", "O": c["context"],
                                    "O_as_read": Q.marked(decode, c["readers"][X.LOOKUP]["ids"]["org"], c["pos"], c["space"]),
                                    "S": c["cf_context"], "expect": c["expect"], "move": c["move"]})  # fmt: skip
        if k == max(KS) and len(cases) > 1 and len(blob["prompts"]) < k_prompts:
            c = cases[1]
            blob["prompts"].append({"scene": c["scene"], "k": k, "reader": "recall", "O": c["context"],
                                    "O_as_read": Q.marked(decode, c["readers"][X.RECALL]["ids"]["org"], c["pos"], c["space"]),
                                    "S": c["cf_context"], "expect": c["expect"], "move": c["move"]})  # fmt: skip
    print(json.dumps(blob, indent=1, ensure_ascii=False))
    write_plan(blob, [(f"{p['scene']} ({p['reader']}, k = {p['k']})", p["O_as_read"]) for p in blob["prompts"]])
    return blob


def write_plan(blob: dict, prompts: list[tuple[str, str]]) -> Path:
    """The plan's counts (plan.json) and its rendered prompts (prompts.md) in a new results/<exp>/plan-<time>/ folder
    (the competence report and the 5 rendered prompts the verify pack needs before an enqueue)."""
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [
        f"# {EXP} plan on {blob['target']} (tokenizer only): {len(prompts)} rendered prompts, ⟦…⟧ the bridge word",
        "",
    ]
    for scene, text in prompts:
        lines += [f"## {scene}", "", "```", text, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- the run (GPU) -------------------------------------------------------------------------------------------------


def gate_of(cases: list[dict], comp: list[dict], gate_min: float | None = None) -> tuple[dict, list[dict]]:
    """O's read accuracy per reader over every case at k (the gate: >= gate_min for both) and the eligible cases in
    generation order (both readers say and read O's and S's answers right), as x6_routes."""
    gate_min = X.GATE if gate_min is None else gate_min
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    said = {w: float(np.mean([right[(c["scene"], w, "org")]["right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    return {"cases": len(cases), "org_read_accuracy": acc, "org_said_accuracy": said, "gate": gate_min,
            "pass": bool(cases) and all(a >= gate_min - EPS for a in acc.values()), "eligible": len(ok)}, ok  # fmt: skip


def rand_dir(key: str, d: int):
    """A random unit direction seeded by RAND_SEED and the key (the scene at k and its target)."""
    import torch

    seed = int(hashlib.sha256(f"{RAND_SEED}|{key}".encode()).hexdigest()[:12], 16)
    r = torch.randn(d, generator=torch.Generator().manual_seed(seed))
    return r / r.norm()


def arm_list(j: int) -> list[dict]:
    """The arms of one scene whose bridge sits at slot j in O, in read order."""
    arms: list[dict] = [{"arm": a, "target": None} for a in DELTA_ARMS]
    for t in (t for t in W.SLOTS if t != j):
        arms += [{"arm": "write", "target": t}, {"arm": "random", "target": t}]
    return arms


def arm_vector(a: dict, x, parts: dict, j: int, mu, scene: str):
    """The vector added at the bridge word for arm a (None: no edit)."""
    kind = a["arm"]
    if kind == "none":
        return None
    if kind == "whole":
        return x
    if kind in ("no_alf", "no_alf_rand"):
        return x - parts[kind]
    step = S_WRITE * (mu[a["target"]] - mu[j])
    if kind == "write":
        return step
    return rand_dir(f"{scene}|{a['target']}", x.shape[0]).to(x.device) * step.norm()


def read_record(c: dict, w: str, a: dict, lg, rd: dict, tok, digits) -> dict:
    top = int(lg.argmax())
    rec = {"scene": c["scene"], "base_scene": c["base_scene"], "k": c["k"], "j": c["j"], "entity": c["bridge"],
           "reader": w, "arm": a["arm"], "target": a["target"], "top_text": tok.decode([top]),
           "kept": int(top == rd["tok_A"]), **X.read_row(lg, rd, digits)}  # fmt: skip
    if w == X.LOOKUP:
        rec["route"] = R.classify(top, c)
        if a["target"] is not None:
            rec["swap"] = W.classify(top, dict(enumerate(c["slot_tokens"])), c["j"], a["target"])
    return rec


def bridge_states(model, c: dict, layer: int) -> dict:
    return Q.bridge_states(model, c, layer)


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    assert target in R.STATES, f"47.16 needs the fresh-scene pointer basis U (x6_routes.STATES): none for {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    manifest = out / "manifest.json"  # rewritten as the run goes: gates, items (never a result)
    m: dict = {"exp": EXP, "run": name, "why": why, "test": "47.16", "spec": SPEC,
               "question": f"{QUESTION} ({PREDICTIONS})",
               "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
               "switches": switches(), "code": git_state(), "layer": layer,
               "read": "X0's chat read (the top token after a digit's space token appended to O)", "ks": list(KS),
               "gate": X.GATE, "n": {"candidates": N_CAND, "items": N_ITEMS}, "s_write": S_WRITE,
               "seeds": {"scenes": R.SEED, "fillers": FILLER_SEED, "random_directions": RAND_SEED,
                         "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                         "examples": X.EXAMPLES_SEED},
               "arms": ARM_TEXT, "U_from": R.STATES[target], "fillers": list(FILLERS),
               "filler_rule": "per base scene one seeded draw of 50 fillers; the first k inserted between the last "
                              "locker sentence and the first pick sentence of O and S (prefixes nest)",
               "stop_rule": "k in order; at the first k whose gate fails the larger ks are skipped",
               "beta": "x8 order's B2: <U U^T (h_k - h_0), mu_{j-1} - mu_j> / ||mu_{j-1} - mu_j||^2, j in {1, 2}; "
                       "beta_next (the j + 1 step) beside, descriptive",
               "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    _, animals, people = R.pools(tok)
    bad = filler_checks(FILLERS, animals, people)
    assert not bad, f"fillers: {bad}"
    base = base_cases(tok)
    cases_by_k, gates, ok_by_k, comp_all, stopped = {}, {}, {}, [], None
    for k in KS:
        cases, dropped = cases_at(tok, base, k)
        comp = X.competence(model, cases, digits, ws)
        comp_all += [{**r, "k": k} for r in comp]
        gate, ok = gate_of(cases, comp)
        gates[str(k)] = {"dropped": dict(dropped), **gate}
        cases_by_k[k] = cases
        if not gate["pass"]:
            stopped = k
            break
        ok_by_k[k] = ok
    passed = [k for k in KS if k in ok_by_k]
    skipped = [k for k in KS if k not in cases_by_k]
    X.write_jsonl(out / "competence.jsonl", comp_all)
    X.write_jsonl(out / "cases.jsonl", [c for k in cases_by_k for c in cases_by_k[k]])
    both = set.intersection(*({c["base_scene"] for c in ok_by_k[k]} for k in passed)) if passed else set()
    chosen_base = [c["scene"] for c in base if c["scene"] in both][:N_ITEMS]
    (out / "gate.json").write_text(json.dumps({"gates": gates, "stopped_at": stopped, "skipped": skipped,
                                               "passed": passed, "eligible_in_all": len(both),
                                               "chosen": chosen_base}, indent=2) + "\n")  # fmt: skip
    m.update({"stopped_at": stopped, "skipped": skipped, "passed": passed, "tested": bool(passed),
              "items": {"chosen": len(chosen_base), "entities": len({c["bridge"] for c in base if c["scene"] in chosen_base})}})  # fmt: skip
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    if not passed:
        print(f"not tested: the gate failed at k = {stopped}; see gate.json", flush=True)
        return out
    mu = {s: torch.tensor(v, dtype=torch.float32, device=dev) for s, v in MM.pointer_means(R.STATES[target]).items()}
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device=dev)
    m["norms"] = {
        "step": {f"{a}-{b}": round(float((mu[b] - mu[a]).norm()), 4) for a in W.SLOTS for b in W.SLOTS if a != b}
    }
    rows, norms, betas, saved = [], [], [], {}
    h0: dict[str, torch.Tensor] = {}
    with torch.no_grad():
        for k in passed:
            at = {c["base_scene"]: c for c in cases_by_k[k]}
            chosen = [at[b] for b in chosen_base]
            states = {
                c["scene"]: bridge_states(model, c, layer) for c in progress(chosen, f"k = {k}: states at L{layer}")
            }
            h_org = torch.stack([states[c["scene"]]["org"] for c in chosen]).to(dev)
            x = torch.stack([states[c["scene"]]["alt"] - states[c["scene"]]["org"] for c in chosen]).to(dev)
            saved[f"h_{k}"] = h_org.cpu().numpy().astype(np.float32)
            saved[f"scene_{k}"] = np.array([c["scene"] for c in chosen])
            saved[f"layout_{k}"] = np.array([c["layout"] for c in chosen])
            saved[f"pick_{k}"] = np.array([c["pick_index"] for c in chosen])
            ptr = (x @ alf) @ alf.T
            share = ptr.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
            parts = {"no_alf": ptr, "no_alf_rand": SP.random_subspace_part(x, share, basis)}
            for i, c in enumerate(progress(chosen, f"k = {k}: arms at L{layer} (case)")):
                j = c["j"]
                if k == 0:
                    h0[c["base_scene"]] = h_org[i]
                else:
                    dh = h_org[i] - h0[c["base_scene"]]
                    rec = {"scene": c["scene"], "base_scene": c["base_scene"], "k": k, "j": j, "entity": c["bridge"]}
                    if j >= 1:
                        rec.update({f"{a}_prev": v for a, v in R.code_shift(dh, alf, mu[j - 1] - mu[j]).items()})
                    if j + 1 in mu:
                        rec.update({f"{a}_next": v for a, v in R.code_shift(dh, alf, mu[j + 1] - mu[j]).items()})
                    betas.append(rec)
                arms = arm_list(j)
                own = {a: v[i] for a, v in parts.items()}
                vecs = [arm_vector(a, x[i], own, j, mu, c["scene"]) for a in arms]
                edits = [{} if v is None else {layer: AddRows(v[None], [c["pos"]])} for v in vecs]
                for w, rd in c["readers"].items():
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                    rows += [read_record(c, w, a, lg, rd, tok, digits) for a, lg in zip(arms, logits, strict=True)]
                norms.append({"scene": c["scene"], "base_scene": c["base_scene"], "k": k, "j": j,
                              "norm": round(float(x[i].norm()), 4), "share_alf": round(float(share[i]), 5),
                              "U_norm": round(float(ptr[i].norm()), 4),
                              "write_norm": {str(t): round(float((S_WRITE * (mu[t] - mu[j])).norm()), 4)
                                             for t in W.SLOTS if t != j}})  # fmt: skip
    saved.update({"base_scene": np.array(chosen_base),
                  "entity": np.array([at[b]["bridge"] for b in chosen_base]),
                  "j": np.array([at[b]["j"] for b in chosen_base])})  # fmt: skip
    np.savez_compressed(out / "states.npz", **saved)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "beta.jsonl", betas)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- the verdict (CPU) ---------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.16 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan:(.*)$", block, re.M)
    return found.group(1).strip() if found else ""


def probe_at(z, k: int, n_boot: int) -> dict:
    """x0_probe (b) at the bridge word on O's states at k: target = the bridge's locker slot, 5 folds by entity."""
    items = [{"entity": str(e), "locker_index": int(j), "pick_index": int(p), "layout": str(lay)}
             for e, j, p, lay in zip(z["entity"], z["j"], z[f"pick_{k}"], z[f"layout_{k}"], strict=True)]  # fmt: skip
    return P.score(z[f"h_{k}"].astype(np.float64), items, "locker sentence", n_boot)


def k_cells(rows: list[dict], k: int, n_boot: int) -> dict:
    """One k's cells: the lookup's route shares per Delta arm, U's cut of position beyond random, the swap's target
    share (write vs random, pooled over the two targets), the recall's kept share per arm."""
    lk = [r for r in rows if r["k"] == k and r["reader"] == X.LOOKUP]
    at = {(r["scene"], r["arm"], r["target"]): r for r in lk}
    scenes = sorted({r["scene"] for r in lk if r["arm"] == "whole"})
    ent = [at[(s, "whole", None)]["entity"] for s in scenes]
    sw = {f"{rt}|{a}": [int(at[(s, a, None)]["route"] == rt) for s in scenes] for a in DELTA_ARMS for rt in ROUTES}
    pt, rr = Q.shares(sw, ent, n_boot)
    pairs = [(s, t) for s in scenes for t in W.SLOTS if (s, "write", t) in at]
    swap = {a: [int(at[(s, a, t)]["swap"] == "target") for s, t in pairs] for a in ("write", "random")}
    sp, sr = Q.shares(swap, [at[(s, "whole", None)]["entity"] for s, _ in pairs], n_boot)
    rc = [r for r in rows if r["k"] == k and r["reader"] == X.RECALL]
    kept = {}
    for key in dict.fromkeys((r["arm"], r["target"]) for r in rc):
        mine = [r for r in rc if (r["arm"], r["target"]) == key]
        kept[f"{key[0]}" + (f"->{key[1]}" if key[1] is not None else "")] = Q.shares(
            {"kept": [r["kept"] for r in mine]}, [r["entity"] for r in mine], n_boot
        )[0]["kept"]
    return {"k": k, "n": len(scenes), "entities": len(set(ent)),
            "routes": {a: {rt: pt[f"{rt}|{a}"] for rt in ROUTES} for a in DELTA_ARMS},
            "U_cut_beyond_random": Q.paired(rr, pt, "position|no_alf_rand", "position|no_alf"),
            "swap": {"n": len(pairs), "write": sp["write"], "random": sp["random"],
                     "minus_random": Q.paired(sr, sp, "write", "random")},
            "recall_kept": kept}  # fmt: skip


def beta_cells(betas: list[dict], k: int, n_boot: int) -> dict | None:
    """Mean beta (B2) at k over the scenes with j >= 1, with a cluster-bootstrap CI; per j beside; beta_next too."""
    mine = [b for b in betas if b["k"] == k and "beta_prev" in b]
    if not mine:
        return None
    rr = X.resampled_rates({"beta": [b["beta_prev"] for b in mine]}, [b["entity"] for b in mine], n_boot)
    out = {"n": len(mine), "beta": [float(np.mean([b["beta_prev"] for b in mine])), *X.interval(rr["beta"])],
           "norm_ratio_median": float(np.median([b["norm_d_prev"] / b["norm_step_prev"] for b in mine])),
           "by_j": {str(j): float(np.mean([b["beta_prev"] for b in mine if b["j"] == j])) for j in (1, 2)
                    if any(b["j"] == j for b in mine)}}  # fmt: skip
    nxt = [b for b in betas if b["k"] == k and "beta_next" in b]
    if nxt:
        out["beta_next"] = float(np.mean([b["beta_next"] for b in nxt]))
    return out


def rule(cells: dict[int, dict], probes: dict[int, dict], gates: dict, stopped: int | None, betas: dict) -> dict:
    """47.16's labels on one model (point estimates; EPS at the bars). See the module docstring."""
    ks = sorted(cells)
    pos = {k: cells[k]["routes"]["whole"]["position"][0] for k in ks}
    ident = {k: cells[k]["routes"]["whole"]["identity"][0] for k in ks}
    prb = {k: probes[k]["probe"][0] for k in ks}
    swp = {k: cells[k]["swap"]["write"][0] for k in ks}
    robust = bool(ks and 0 in pos and all(abs(pos[k] - pos[0]) <= NEAR + EPS and abs(prb[k] - prb[0]) <= PROBE_NEAR + EPS
                                          and abs(swp[k] - swp[0]) <= SWAP_NEAR + EPS for k in ks))  # fmt: skip
    far = max(KS)
    acc = gates.get(str(far), {}).get("org_read_accuracy", {})
    near_far = bool(far in pos and 0 in pos and pos[0] - pos[far] >= FAR - EPS and ident[far] - ident[0] >= FAR - EPS
                    and acc and all(a >= ACC_MIN - EPS for a in acc.values()))  # fmt: skip
    label = (f"breaks at k = {stopped}" if stopped is not None else "distance-robust address" if robust
             else "address near, identity far" if near_far else "none of the three")  # fmt: skip
    beta_ok = {k: v["beta"][0] <= BETA_MAX + EPS for k, v in betas.items() if v}
    return {"label": label, "stopped_at": stopped, "robust": robust, "near_far": near_far,
            "position": pos, "identity": ident, "probe": prb, "swap_target": swp,
            "beta_within": beta_ok, "fig8c_holds": bool(beta_ok) and all(beta_ok.values())}  # fmt: skip


def routes_reference(target: str) -> dict | None:
    """The routes run's C2 lookup shares under the whole change (descriptive, beside k = 0), None without the run."""
    src = R.RESULTS / W.ROUTES_OF.get(target, "") / "outcomes.jsonl"
    if not src.exists():
        return None
    lk = [r for r in X.read_jsonl(src) if r["condition"] == "C2" and r["reader"] == X.LOOKUP and r["arm"] == "whole"]
    return {"run": W.ROUTES_OF[target], "n": len(lk),
            **{rt: float(np.mean([r["route"] == rt for r in lk])) for rt in ROUTES}} if lk else None  # fmt: skip


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.16 run {run!r} here, and it is not one of the specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "gates": gate.get("gates", {}),
            "stopped_at": gate.get("stopped_at"), "skipped": gate.get("skipped", []), "passed": gate.get("passed", [])}  # fmt: skip
    if m.get("tested") is False:
        r = rule({}, {}, base["gates"], base["stopped_at"], {})
        return {
            **base,
            "status": "not tested",
            "label": r["label"],
            "why": f"the gate failed at k = {base['stopped_at']}",
        }
    if not (src / "outcomes.jsonl").exists():
        return {**base, "status": "pending", "why": "no outcomes here (the run did not finish)"}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    z = np.load(src / "states.npz")
    betas = X.read_jsonl(src / "beta.jsonl")
    ks = sorted({r["k"] for r in rows})
    cells = {k: k_cells(rows, k, n_boot) for k in ks}
    probes = {k: probe_at(z, k, n_boot) for k in ks}
    bcells = {k: beta_cells(betas, k, n_boot) for k in ks if k > 0}
    r = rule(cells, probes, base["gates"], base["stopped_at"], bcells)
    return {**base, "status": "tested", **r, "cells": cells, "probes": probes, "betas": bcells, "items": m.get("items"),
            "routes_reference": routes_reference(base["target"]), "step_norms": m.get("norms", {}).get("step")}  # fmt: skip


def ci(v) -> str:
    return Q.ci(v)


def report_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    tested = [m for m in models if m["status"] == "tested"]
    lines = ["# 47.16: does the address survive distance?", "",
             f"Batch 47, test 47.16 ({SPEC}; {QUESTION}, Dan: {answer}). x6_routes' C2 scenes with k neutral sentences "
             "between the lockers and the picks; every edit at the bridge word at the layer fixed in advance, read on O; "
             f"the same base scenes at every k; cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", "## Verdict", "",
             "| model | run | status | label | stopped at | ks tested | Fig 8c at scale (beta <= 0.25 at every k > 0) |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | |")
            continue
        b = m.get("beta_within", {})
        lines.append(f"| {m['target']} | {m['run']} | {m['status']} | **{m['label']}** | {m.get('stopped_at')} | "
                     f"{m.get('passed')} | {('yes' if m.get('fig8c_holds') else 'no') if b else '–'} "
                     f"({', '.join(f'k={k}: {v}' for k, v in b.items())}) |")  # fmt: skip
    lines += ["", f"Rule (fixed in advance): breaks = the gate failed at some k (the test stops there); distance-robust "
              f"= position share and probe within {NEAR} of k = 0 at every k, swap success within {SWAP_NEAR}; address "
              f"near, identity far = position falls >= {FAR} and identity rises >= {FAR} by k = 50 with accuracy >= "
              f"{ACC_MIN}; beta <= {BETA_MAX} at every k > 0 (counts mentions, not tokens).", "",
              "## Per k: accuracy unedited (the gate, over the candidates), probe, routes under the whole change, "
              "U's cut, the swap, beta", "",
              "| model | k | lookup acc | recall acc | gate | n | probe | layout | identity | position | value | "
              "without U: position | without random | U's cut beyond random | swap -> target | random -> target | "
              "beta (B2) | n (j >= 1) |", "|---|" + "---|" * 17]  # fmt: skip
    for m in tested:
        for k in sorted(m["cells"]):
            g = m["gates"].get(str(k), {})
            c, p, b = m["cells"][k], m["probes"][k], m["betas"].get(k)
            rt = c["routes"]
            lines.append(f"| {m['target']} | {k} | {g.get('org_read_accuracy', {}).get(X.LOOKUP, float('nan')):.2f} | "
                         f"{g.get('org_read_accuracy', {}).get(X.RECALL, float('nan')):.2f} | {'pass' if g.get('pass') else 'fail'} | "
                         f"{c['n']} | {ci(p['probe'])} | {ci(p['layout'])} | {ci(rt['whole']['identity'])} | "
                         f"{ci(rt['whole']['position'])} | {ci(rt['whole']['value'])} | {ci(rt['no_alf']['position'])} | "
                         f"{ci(rt['no_alf_rand']['position'])} | {ci(c['U_cut_beyond_random'])} | {ci(c['swap']['write'])} | "
                         f"{ci(c['swap']['random'])} | {ci(b['beta']) if b else '–'} | {b['n'] if b else '–'} |")  # fmt: skip
        for k in m["skipped"]:
            lines.append(f"| {m['target']} | {k} | skipped | | | | | | | | | | | | | | | |")
    lines += ["", "## Collateral: the recall keeps O's answer, per arm and k", "",
              "| model | k | " + " | ".join(DELTA_ARMS) + " | write (pooled) | random (pooled) |", "|---|---|" + "---|" * 6]  # fmt: skip
    for m in tested:
        for k in sorted(m["cells"]):
            kept = m["cells"][k]["recall_kept"]
            pooled = {}
            for kind in ("write", "random"):
                vals = [v for key, v in kept.items() if key.startswith(kind + "->")]
                pooled[kind] = f"{np.mean([v[0] for v in vals]):.2f}" if vals else "–"
            lines.append(f"| {m['target']} | {k} | " + " | ".join(ci(kept[a]) for a in DELTA_ARMS)
                         + f" | {pooled['write']} | {pooled['random']} |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "",
              "## Gates, items, references (descriptive)", ""]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"- {m['target']} ({m['run']}): pending ({m['why']}).")
            continue
        gtxt = "; ".join(f"k = {k}: O read accuracy {v['org_read_accuracy']} (said {v['org_said_accuracy']}; pass "
                         f"{v['pass']}; eligible {v['eligible']} of {v['cases']}; dropped {v['dropped'] or 'none'})"
                         for k, v in m["gates"].items())  # fmt: skip
        if m["status"] != "tested":
            lines.append(f"- {m['target']} ({m['run']}): not tested ({m['why']}). Gates: {gtxt}.")
            continue
        ref = m["routes_reference"]
        rtxt = (f"the routes run {ref['run']} (C2, whole, n = {ref['n']}): identity {ref['identity']:.2f}, position "
                f"{ref['position']:.2f}, value {ref['value']:.2f}" if ref else "no routes run here")  # fmt: skip
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): gates: {gtxt}. Items: {m['items']}. Step norms "
                     f"||mu_t - mu_j|| {m['step_norms']}. k = 0 against {rtxt}.")  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"}
               for t in RUNS if t not in targets]  # fmt: skip
    out = RESULTS / f"x47_16-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = report_lines(models, answer, n_boot)
    (out / "x47_16.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str)
                                     + "\n")  # fmt: skip
    (out / "x47_16.md").write_text("\n".join(lines) + "\n")
    ex = examples_lines([m["run"] for m in models if m["status"] == "tested"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- the verify-pack view (CPU) ------------------------------------------------------------------------------------


def arm_label(r: dict) -> str:
    return r["arm"] + (f" →{r['target']}" if r["target"] is not None else "")


def examples_lines(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> list[str]:
    """Per run, k random chosen base scenes (seed 0), at every tested filler count: each reader's O prompt exactly as
    read with the bridge word marked, S, and every arm's answer."""
    lines = ["# 47.16 examples (verify pack): O as the model reads it, ⟦…⟧ the bridge word where every arm's vector is "
             "added at L; each arm's top token, the lookup's route and the swap's class. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        dec = decode
        if dec is None:
            from bridge_jspace.review import checks as RC

            tk = RC.tokenizer(m["model"]["target"])
            dec = lambda ids, tk=tk: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
        chosen = json.loads((src / "gate.json").read_text())["chosen"]
        rows = X.read_jsonl(src / "outcomes.jsonl")
        pick = sorted(random.Random(seed).sample(sorted(chosen), min(k, len(chosen))))
        lines += [f"## {run} ({m['model']['target']}, L{m['layer']}): {len(pick)} random base scenes of {len(chosen)} "
                  f"(seed {seed}), at k = {m['passed']}", ""]  # fmt: skip
        for b in pick:
            for kk in m["passed"]:
                c = cases[f"{b}-k{kk}"]
                lines += [f"### {b} at k = {kk}: bridge {c['bridge']} -> {c['cf_bridge']}, pointer move "
                          f"{c['move'][0]} -> {c['move'][1]}; expected digits {c['expect']}", ""]  # fmt: skip
                for w, rd in c["readers"].items():
                    mine = [r for r in rows if r["scene"] == c["scene"] and r["reader"] == w]
                    lines += [f"**{'lookup' if w == X.LOOKUP else 'recall'}** ({rd['question']}): O's answer "
                              f"{rd['answer']}, S's {rd['cf_answer']}", "", "O, as read:", "", "```",
                              Q.marked(dec, rd["ids"]["org"], c["pos"], c["space"]), "```", "", "S (the source):", "",
                              "```", Q.marked(dec, rd["ids"]["alt"], c["pos"], c["space"]), "```", "",
                              "| arm | answer | route | swap | kept O's answer |", "|---|---|---|---|---|"]  # fmt: skip
                    lines += [f"| {arm_label(r)} | {r['top_text']!r} | {r.get('route') or ''} | {r.get('swap') or ''} | "
                              f"{r['kept']} |" for r in mine]  # fmt: skip
                    lines.append("")
    return lines


def stage_examples(runs: list[str]) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    out = RESULTS / f"examples-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "examples.md").write_text("\n".join(examples_lines(runs)) + "\n")
    print("wrote", out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "examples"])
    ap.add_argument("--name", help="run: the run name (results/x47_distance/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / examples: the 47.16 runs")
    ap.add_argument("--why", default="batch 47, test 47.16 (jobs/c3/batch47.yaml; Q47.16)")
    ap.add_argument("--n-cand", type=int, default=N_CAND, help="plan: the base candidates to encode")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.n_cand)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    else:
        stage_examples(a.runs)


if __name__ == "__main__":
    main()
