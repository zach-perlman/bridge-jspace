"""x47_six (batch 47, test 47.2; Dan 28 Oct ~02:00; jobs/c3/batch47.yaml, design and rule fixed in advance; Q47.2 in
predictions/2026-10-28_dan.md): harder pointer scenes, is the order code categorical or ordinal?

As computed (fixed before any run; Dan may override before the run; the specs jobs/c3/x47_2_*.yaml repeat it):

Scenes (plan, CPU; x6_routes' generator: its pools, sentences, encoding, chat rendering and X0's top-token read). n = 6
single-token animals with lockers (slots 1-6, six distinct digits of 1-9), the six locker sentences first, then three
pick sentences (the asked person picks the bridge, two others pick two other locker items; order seeded); every item's
first mention is its locker sentence. Routes move (i, j), x6_routes' C1 at six slots: the bridge's locker sentence moves
from slot i to slot j (swapped with the sentence at slot j), and its number in S is a new digit not in O's list (7 of
the 9 digits; letters are not needed, dumbest way 3); everything else is O's. Read on O: identity (= nothing changed)
-> slot i's digit, position -> slot j's digit, value -> the new digit, other. Every ordered pair (30), 40 candidates per
pair, the first 20 eligible per pair (~600). C0 sanity (x6_routes' C0): S = O with the asked person picking another
person's item (legs differ), 150 candidates, the first 100 eligible; whole change only; its lookup switch reported
beside the three-locker reference (descriptive: it does not stop the run).

Run (GPU, SEALED: per-item outputs only, no verdict). Competence as X0 (8 greedy tokens and the top-token read on the
unedited O and S, both readers); gate: O's read accuracy >= 0.80 per reader over the move candidates. If six slots fail
the gate, the same at five slots (20 pairs; the slot subspace 4-d; (iv) on slots 2-5) and the manifest says so
("slots", "fallback"); if five fail too, "not tested" (no arms). Eligible: both readers say and read O's and S's answers
right. Split: per ordered pair the chosen scenes shuffled (seed 4721, keyed by the pair), the first half (floor) fit,
the rest test. Fit, in the job before any arm: the O and S states at the bridge word at L of every fit scene, labelled
by the bridge's slot in that prompt; x0_massmean's layout-free method (each state minus its layout group's mean,
x0_probe.layout = which sentences before the asked pick are locker sentences, here the asked pick's place among the
picks; groups of one dropped); mu_k = slot k's mean; the slot subspace W = x0_massmean.mass_mean (orthonormal, rank n -
1). The unit: the median over the test half of ||W W^T Delta||, Delta = h_S - h_O at the bridge word. Arms on the test
half, on O, at the bridge word at L, both readers: none; whole (Delta); (i) Delta - W W^T Delta and Delta minus a random
part of the same share (X0's random subspace, seed 888 + L); (iv) the same for U (the old 4-d pointer basis,
x0_massmean.subspaces' Alf on the fresh-scene probe states, not refit); (ii) from the scene's O slot i to every other
slot t: s * unit * (mu_t - mu_i) / ||mu_t - mu_i||; (iii) v = mean_k (mu_{k+1} - mu_k) = (mu_n - mu_1) / (n - 1) as s *
unit * v / ||v|| from start slot i < n (target i + 1), reversed from i > 1 (target i - 1), and as dumbest way 2 the
first step mu_2 - mu_1 and v without it, mean_{k>=2} (mu_{k+1} - mu_k), each as a shift from i < n (target i + 1); a
random direction of the same norm per scene (seed 4723, keyed by the scene) as the writes' control; s = 1 and 2.

Verdict (CPU; refuses until Q47.2's "Dan:" line is committed). Lookup answers classified by the slot whose digit they
are (or the new digit = value). Shares with cluster-bootstrap CIs over bridge items (10,000 resamples, seed 0). First
the whole change's routes split (dumbest way 1: position share < 0.05 -> "not interpretable"). PCA of the n centred
means: variance explained by 1, 2, 3 components; Spearman of the first component's projection against slot. Rule at s =
2 (decisive; s = 1 beside it), bars counted with EPS 1e-9 (a value at a bar is at it):
  ordinal       |Spearman| >= 0.9, v sends >= 0.25 of lookups to slot k + 1 from >= 4 of the 5 start slots (five slots:
                4 of 4), and the random direction sends <= 0.05 to k + 1 (pooled over the start slots);
  categorical   v sends >= 0.25 from slot 1 and < 0.10 from every other start slot, and on moves among slots 2-n the
                position share without U is within 0.10 of that without its random part;
  slot-specific the pairwise writes send >= 0.25 to their target on most (more than half) of the n (n - 1) pairs, and
                v does not on most start slots (>= 0.25 from at most 2 of 5).
The first label that holds in this order is the model's answer (every holding label listed); none: "none of the three".

uv run python scripts/x47_six.py plan                                                     # CPU, the target's tokenizer
BJ_TARGET=muse-glimmer-30b uv run python scripts/x47_six.py plan --out results/x47_six/plan-<stamp>   # + 5 rendered scenes
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_six.py run --name qwen35_9b_x47_2         # GPU (sealed)
uv run python scripts/x47_six.py verdict --runs qwen35_9b_x47_2 muse30_x47_2              # CPU, after Dan's Q47.2
uv run python scripts/x47_six.py examples --runs qwen35_9b_x47_2 muse30_x47_2             # CPU, after Dan's Q47.2
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
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

EXP = "x47_six"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml (47.2)"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.2"
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_2", "muse-glimmer-30b": "muse30_x47_2", "qwen3.6-27b": "x47_2_27b"}
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_six"}  # batch 52 C: verdict --coverage; RUNS unchanged
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x47_six/x47_2-20261028T113102Z"  # 47.2's rules first scored (the 9B and Muse)
SLOTS_TRY = (6, 5)  # six slots; five if six fail the gate (Dan: "drop to five and say so")
SEED, SPLIT_SEED, RAND_SEED = 4702, 4721, 4723
N_CAND, N_PER_PAIR, N_C0_CAND, N_C0 = 40, 20, 150, 100
DOSES, DECISIVE = (1, 2), 2
WORKS, NEAR_ZERO, RHO_MIN, OTHERS_BELOW, U_NEAR, ORDINAL_SHARE = 0.25, 0.05, 0.9, 0.10, 0.10, 0.8
EPS = 1e-9  # a value at a bar counts as at the bar
ROUTES = ("identity", "position", "value", "other")
REMOVALS = ("none", "whole", "no_slot", "no_slot_rand", "no_U", "no_U_rand")
SHIFTS = ("v", "vrev", "v12", "vno12")
LABELS = ("ordinal", "categorical", "slot-specific")
LABEL_TEXT = {"ordinal": "ordinal", "categorical": "categorical, first vs rest", "slot-specific": "slot-specific"}
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change h_S - h_O at the bridge word",
    "no_slot": "(i) the whole change without its part in the slot subspace W (fit on the held-out half)",
    "no_slot_rand": "(i) the whole change without a random part of W's share",
    "no_U": "(iv) the whole change without its part in the old 4-d pointer basis U",
    "no_U_rand": "(iv) the whole change without a random part of U's share",
    "write": "(ii) s units along mu_t - mu_i (i: the bridge's slot in O; t: the target)",
    "random": "a random direction of s units (the writes' control)",
    "v": "(iii) s units along v = mean_k (mu_{k+1} - mu_k), target i + 1",
    "vrev": "(iii) s units along -v, target i - 1",
    "v12": "(dumbest way 2) s units along mu_2 - mu_1 as a shift, target i + 1",
    "vno12": "(dumbest way 2) s units along v without the first step, target i + 1",
}
LOCKER_START = "The locker of"


# ---- scenes (text) -------------------------------------------------------------------------------------------------


def pairs(n: int) -> list[tuple[int, int]]:
    """Every ordered pair of distinct slots (1-based)."""
    return [(i, j) for i in range(1, n + 1) for j in range(1, n + 1) if i != j]


def sentences(context: str) -> list[str]:
    out = re.split(r"(?<=\.) ", context)
    assert " ".join(out) == context, f"the context does not split into sentences: {context!r}"
    return out


def first_mentions_are_lockers(context: str, items: list[str]) -> bool:
    """Every item's first mention (a whole-word match) is in its locker sentence."""
    sents = sentences(context)
    for x in items:
        first = next((k for k, s in enumerate(sents) if re.search(rf"\b{re.escape(x)}\b", s)), None)
        if first is None or not sents[first].startswith(f"{LOCKER_START} the {x} "):
            return False
    return True


def pick_index(context: str, person: str) -> int:
    """The sentence index of the person's pick sentence."""
    found = [k for k, s in enumerate(sentences(context)) if s.startswith(f"{person} picked the ")]
    assert len(found) == 1, f"{person}: {len(found)} pick sentences"
    return found[0]


def move_text(rng: random.Random, animals: list[str], people: list[str], n: int, i: int, j: int) -> dict:
    """One routes-move scene: O with the bridge's locker sentence at slot i; S with it at slot j (swapped with the
    sentence there) and the bridge's number a new digit not in O's list; the picks are O's."""
    order = rng.sample(animals, n)  # order[k - 1] has slot k
    vals = rng.sample(range(1, 10), n + 1)
    new = vals.pop()
    bridge, moved = order[i - 1], order[j - 1]
    asked, p1, p2 = rng.sample(people, 3)
    b, c = rng.sample([x for x in order if x != bridge], 2)
    picks = rng.sample([(asked, bridge), (p1, b), (p2, c)], 3)
    o_lock = list(zip(order, vals, strict=True))
    s_lock = list(o_lock)
    s_lock[i - 1], s_lock[j - 1] = (moved, vals[j - 1]), (bridge, new)
    return {"condition": "M", "slots": n, "move": [i, j], "items": order, "values": vals, "new": new, "asked": asked,
            "bridge": bridge, "cf_bridge": bridge, "picks": picks, "o": R.context(o_lock, picks),
            "s": R.context(s_lock, picks),
            "expect": {"identity": vals[i - 1], "position": vals[j - 1], "value": new, "original": vals[i - 1]}}  # fmt: skip


def c0_text(rng: random.Random, animals: list[str], people: list[str], legs: dict, n: int) -> dict | None:
    """One C0 scene (x6_routes' C0 at n slots): S = O with the asked person picking another person's item; None when
    the two items have as many legs (the recall could not switch)."""
    order = rng.sample(animals, n)
    vals = rng.sample(range(1, 10), n)
    i = rng.randrange(1, n + 1)
    bridge = order[i - 1]
    asked, p1, p2 = rng.sample(people, 3)
    b, c = rng.sample([x for x in order if x != bridge], 2)
    picks = rng.sample([(asked, bridge), (p1, b), (p2, c)], 3)
    if legs[bridge] == legs[b]:
        return None
    lock = list(zip(order, vals, strict=True))
    s_picks = [(q, b if q == asked else x) for q, x in picks]
    return {"condition": "C0", "slots": n, "move": [i, order.index(b) + 1], "items": order, "values": vals, "new": None,
            "asked": asked, "bridge": bridge, "cf_bridge": b, "picks": picks, "o": R.context(lock, picks),
            "s": R.context(lock, s_picks), "expect": {"switch": vals[order.index(b)], "original": vals[i - 1]}}  # fmt: skip


def text_checks(t: dict) -> list[str]:
    """What must hold for a scene's texts (empty if all hold): n distinct items and digits, the new digit not in O,
    every item's first mention its locker sentence in O and S, the question names no item, O and S differ only where
    the design changes them (moves: the two swapped locker sentences; C0: the asked pick sentence)."""
    bad = []
    n, o, s = t["slots"], t["o"], t["s"]
    if len(set(t["items"])) != n or len(set(t["values"])) != n:
        bad.append("items or digits repeat")
    if t["new"] is not None and (t["new"] in t["values"] or str(t["new"]) in o):
        bad.append("the new digit is in O")
    if not (first_mentions_are_lockers(o, t["items"]) and first_mentions_are_lockers(s, t["items"])):
        bad.append("an item's first mention is not its locker sentence")
    if any(re.search(rf"\b{re.escape(x)}\b", R.LOOKUP_Q.format(p=t["asked"])) for x in t["items"]):
        bad.append("the question names an item")
    so, ss = sentences(o), sentences(s)
    diff = [k for k, (a, b) in enumerate(zip(so, ss, strict=True)) if a != b]
    i, j = t["move"]
    want = sorted({i - 1, j - 1}) if t["condition"] == "M" else [pick_index(o, t["asked"])]
    if diff != want:
        bad.append(f"O and S differ in sentences {diff}, not {want}")
    return bad


# ---- scenes (tokenizer) --------------------------------------------------------------------------------------------


def encode_text(tok, t: dict, scene: str, legs: dict) -> tuple[dict | None, str]:
    """x6_routes.encode on the scene (the bridge one token at one index shared by O and S, the readers' prompts the
    same through it), with the slots' digit tokens, the new digit's token, and the asked pick's layout."""
    from scripts import suite_v1 as S

    bad = text_checks(t)
    assert not bad, f"{scene}: {bad}"
    case, why = R.encode(tok, t["o"], t["s"], t["asked"], t["bridge"], t["cf_bridge"], legs, t["expect"],
                         t["condition"], scene)  # fmt: skip
    if case is None:
        return None, why
    slot_tokens = [S.answer_token(tok, str(v), "digit") for v in t["values"]]
    if len(set(slot_tokens)) != len(slot_tokens):
        return None, "two slots' digits share a token"
    new_token = S.answer_token(tok, str(t["new"]), "digit") if t["new"] is not None else None
    if new_token is not None and new_token in slot_tokens:
        return None, "the new digit shares a token with a slot's"
    pick = pick_index(t["o"], t["asked"])
    case.update({"slots": t["slots"], "move": t["move"], "items": t["items"], "values": t["values"], "new": t["new"],
                 "slot_tokens": slot_tokens, "new_token": new_token, "asked": t["asked"], "pick_index": pick,
                 "layout": P.layout(t["o"], pick), "picks": [list(p) for p in t["picks"]]})  # fmt: skip
    return case, ""


def build_cases(tok, n: int, n_cand: int = N_CAND, n_c0: int = N_C0_CAND) -> tuple[list[dict], collections.Counter]:
    """n_cand encodable move scenes per ordered pair (each pair its own seeded stream) and n_c0 C0 scenes, at n slots;
    drops counted by reason."""
    legs, animals, people = R.pools(tok)
    assert len(animals) >= n, f"{len(animals)} one-token animals for {n} slots"
    assert len(people) >= 3, f"{len(people)} one-token people"
    out: list[dict] = []
    dropped: collections.Counter = collections.Counter()
    for i, j in pairs(n):
        rng = random.Random(f"{SEED}|{n}|M|{i}-{j}")
        got = tries = 0
        while got < n_cand:
            tries += 1
            assert tries <= 50 * n_cand, f"move {i}->{j}: cannot fill {n_cand} scenes ({dropped})"
            case, why = encode_text(tok, move_text(rng, animals, people, n, i, j), f"M{n}-{i}{j}-{tries:03d}", legs)
            if case is None:
                dropped[f"M: {why}"] += 1
                continue
            out.append(case)
            got += 1
    rng = random.Random(f"{SEED}|{n}|C0")
    got = tries = 0
    while got < n_c0:
        tries += 1
        assert tries <= 50 * n_c0, f"C0: cannot fill {n_c0} scenes ({dropped})"
        t = c0_text(rng, animals, people, legs, n)
        if t is None:
            dropped["C0: the bridge and the switched item have as many legs"] += 1
            continue
        case, why = encode_text(tok, t, f"C0{n}-{tries:04d}", legs)
        if case is None:
            dropped[f"C0: {why}"] += 1
            continue
        out.append(case)
        got += 1
    return out, dropped


GATE_NOTE = (
    "The job's competence step (X.competence, before any patch): on the unedited O and S of every candidate, both "
    "readers, 8 greedy tokens must say the gold digit and X0's top-token read (a digit's space token appended) must be "
    f"the gold token. The gate: O's read accuracy >= {X.GATE} per reader over all six-slot move candidates; if it misses, "
    "the same over the five-slot candidates (recorded as the fallback); if that misses too, not tested. Eligible: both "
    "readers say and read O's and S's answers right; the first 20 eligible per ordered pair and the first 100 C0. "
    "competence.jsonl and gate.json hold the per-candidate reads and the accuracies."
)
N_PLAN_EXAMPLES = 5


def plan_prompt(tok, c: dict, reader: str, prompt: str) -> str:
    """The reader's prompt as the model reads it (the read's space token appended) with the bridge token in
    ⟦bridge:…⟧ and the locker sentences at slots i and j in ⟦move:…⟧ (a move: the two swapped sentences; C0: the
    original item's and the newly picked item's lockers, where the pointer moves)."""
    ids = c["readers"][reader]["ids"][prompt]
    text = (
        tok.decode(ids[: c["pos"]])
        + "⟦bridge:"
        + tok.decode(ids[c["pos"] : c["pos"] + 1])
        + "⟧"
        + tok.decode(ids[c["pos"] + 1 :] + c["space"])
    )
    ctx = Q_CONTEXT[prompt](c)
    sents = sentences(ctx)
    i, j = c["move"]
    for s in (sents[i - 1], sents[j - 1]):
        assert text.count(s) == 1, f"{c['scene']}: {s!r} is not once in the decoded prompt"
        text = text.replace(s, f"⟦move:{s}⟧", 1)
    return text


Q_CONTEXT = {"org": lambda c: c["context"], "alt": lambda c: c["cf_context"]}


def plan_examples(tok, cases: list[dict], k: int = N_PLAN_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[dict]:
    """k random six-slot move scenes (seed 0) and the first C0 scene: both readers' O and S prompts as read, marked."""
    moves = [c for c in cases if c["condition"] == "M"]
    pick = random.Random(seed).sample(moves, min(k, len(moves)))
    c0 = [c for c in cases if c["condition"] == "C0"][:1]
    out = []
    for c in [*pick, *c0]:
        out.append({"scene": c["scene"], "condition": c["condition"], "move": c["move"], "bridge": c["bridge"],
                    "cf_bridge": c["cf_bridge"], "values": c["values"], "new": c["new"], "expect": c["expect"],
                    "pos": c["pos"], "readers": {w: {"question": rd["question"], "answer_O": rd["answer"],
                                                     "answer_S": rd["cf_answer"],
                                                     "O": plan_prompt(tok, c, w, "org"), "S": plan_prompt(tok, c, w, "alt")}
                                                 for w, rd in c["readers"].items()}})  # fmt: skip
    return out


def plan_markdown(blobs: dict[str, dict]) -> list[str]:
    """plan.md over the targets written so far: the counts table, the gate note, the rendered prompts."""
    lines = ["# 47.2 plan (CPU, the real tokenizers): scene counts per model, what the gate checks, rendered prompts", "",
             "Written by `scripts/x47_six.py plan` before any run (Dan's amendment 1: a competence report and rendered "
             "prompts before a new scene set runs). The competence report itself comes from the job's gate step. "
             "UNVERIFIED.", "", "| model | layer | slots | move candidates | pairs x per pair | C0 candidates | dropped | "
             "bridge animals | prompt tokens | bridge token index |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for target, b in blobs.items():
        for n in SLOTS_TRY:
            s = b[f"{n} slots"]
            lines.append(f"| {target} | {b['layer']} | {n} | {s['cases']['M']} | {s['pairs']} x {s['per_pair']} | "
                         f"{s['cases']['C0']} | {s['dropped'] or 'none'} | {s['entities']} | {s['prompt_tokens']} | "
                         f"{s['bridge_token_index']} |")  # fmt: skip
    lines += ["", f"The gate: {GATE_NOTE}", ""]
    for target, b in blobs.items():
        lines += [f"## {target}: {N_PLAN_EXAMPLES} random six-slot move scenes (seed {X.EXAMPLES_SEED}) and the first C0 "
                  "scene", ""]  # fmt: skip
        for e in b["rendered"]:
            i, j = e["move"]
            what = (f"the {e['bridge']}'s locker sentence moves from slot {i} to slot {j}; its number in S {e['new']}"
                    if e["condition"] == "M" else f"C0: the asked person picks the {e['cf_bridge']} (slot {j}) instead "
                    f"of the {e['bridge']} (slot {i})")  # fmt: skip
            lines += [f"### {e['scene']}: {what}", "", f"Slots' digits in O {e['values']}; expected {e['expect']}; the "
                      f"bridge at token {e['pos']}.", ""]  # fmt: skip
            for w, rd in e["readers"].items():
                lines += [f"**{'lookup' if w == X.LOOKUP else 'recall'}** ({rd['question']}): O answers {rd['answer_O']}, "
                          f"S answers {rd['answer_S']}", "", "O, as read:", "", "```", rd["O"], "```", "", "S (the source):",
                          "", "```", rd["S"], "```", ""]  # fmt: skip
    return lines


def stage_plan(out: Path | None = None) -> dict:
    """Tokenizer only: per slot count, the cases per condition and pair, the drops, the token checks, an example; with
    `out` (results/x47_six/plan-<stamp>/, shared by the targets), <target>.json and <target>.md with five rendered
    scenes (seed 0), and plan.md over every target written there so far."""
    from scripts import x45m

    tok = x45m.tokenizer()
    blob: dict = {"target": pins.TARGET, "layer": X.PREDICTED.get(pins.TARGET), "prefix": pins.RUN_PREFIX,
                  "gate": GATE_NOTE, "seeds": {"scenes": SEED, "examples": X.EXAMPLES_SEED}}  # fmt: skip
    for n in SLOTS_TRY:
        cases, dropped = build_cases(tok, n)
        moves = [c for c in cases if c["condition"] == "M"]
        per_pair = collections.Counter(f"{c['move'][0]}-{c['move'][1]}" for c in moves)
        for c in cases:
            ids = c["readers"][X.LOOKUP]["ids"]
            assert tok.decode([ids["org"][c["pos"]]]).strip() == c["bridge"], f"{c['scene']}: the bridge token"
            assert tok.decode([ids["alt"][c["pos"]]]).strip() == c["cf_bridge"], f"{c['scene']}: S's bridge token"
        lengths = collections.Counter(len(c["readers"][X.LOOKUP]["ids"]["org"]) for c in moves)
        ex = {cond: next(c for c in cases if c["condition"] == cond) for cond in ("M", "C0")}
        blob[f"{n} slots"] = {
            "cases": dict(collections.Counter(c["condition"] for c in cases)), "pairs": len(per_pair),
            "per_pair": sorted(set(per_pair.values())), "dropped": dict(dropped),
            "bridge_token_index": sorted({c["pos"] for c in moves}), "prompt_tokens": [min(lengths), max(lengths)],
            "layouts": dict(collections.Counter(c["layout"] for c in moves)),
            "entities": len({c["bridge"] for c in moves}),
            "examples": {cond: {"scene": c["scene"], "O": c["context"], "S": c["cf_context"], "expect": c["expect"],
                                "bridge_token": tok.decode([c["readers"][X.LOOKUP]["ids"]["org"][c["pos"]]])}
                         for cond, c in ex.items()}}  # fmt: skip
        if n == SLOTS_TRY[0]:
            blob["rendered"] = plan_examples(tok, cases)
    print(json.dumps({k: v for k, v in blob.items() if k != "rendered"}, indent=1, ensure_ascii=False))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{pins.TARGET}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
        blobs = {p.stem: json.loads(p.read_text()) for p in sorted(out.glob("*.json"))}
        (out / "plan.md").write_text("\n".join(plan_markdown(blobs)) + "\n")
        print("wrote", out)
    return blob


# ---- the fit (numpy) -----------------------------------------------------------------------------------------------


def layout_free(h: np.ndarray, groups: list[str]) -> tuple[np.ndarray, list[int]]:
    """x0_massmean.layout_free on given states: the rows whose layout group has more than one member, each minus its
    group's mean, and their indices."""
    size = collections.Counter(groups)
    keep = [r for r, g in enumerate(groups) if size[g] > 1]
    res = h[keep].astype(np.float64)
    for g in {groups[r] for r in keep}:
        rows = [k for k, r in enumerate(keep) if groups[r] == g]
        res[rows] -= res[rows].mean(0)
    return res, keep


def fit_slots(h: np.ndarray, slots: list[int], groups: list[str], n: int) -> dict:
    """The slot means mu_1..mu_n ([n, d], row k - 1 = slot k) of the layout-free states and the slot subspace W
    (x0_massmean.mass_mean: orthonormal, rank n - 1)."""
    res, keep = layout_free(h, groups)
    lab = [int(slots[r]) for r in keep]
    assert set(lab) == set(range(1, n + 1)), f"slots {sorted(set(lab))}, not 1..{n}"
    mu = np.stack([res[[k for k, s in enumerate(lab) if s == slot]].mean(0) for slot in range(1, n + 1)])
    w = MM.mass_mean(res, lab)
    return {"mu": mu, "W": w, "states": len(keep), "dropped_singletons": len(h) - len(keep),
            "per_slot": {str(k): lab.count(k) for k in range(1, n + 1)},
            "groups": dict(collections.Counter(groups[r] for r in keep))}  # fmt: skip


def shift_vectors(mu: np.ndarray) -> dict[str, np.ndarray]:
    """v = mean_k (mu_{k+1} - mu_k); v12 = mu_2 - mu_1 (the first step); vno12 = v without it, mean_{k>=2} steps."""
    steps = np.diff(mu, axis=0)
    return {"v": steps.mean(0), "v12": steps[0], "vno12": steps[1:].mean(0)}


def pca_reading(mu: np.ndarray) -> dict:
    """PCA of the centred slot means: each component's share of their variance, the cumulative share of the first 1,
    2, 3, the first component's projection per slot, and its Spearman correlation with slot (Pearson's on the ranks,
    ties at their mean rank)."""
    from scipy.stats import rankdata

    c = mu - mu.mean(0)
    _, s, vt = np.linalg.svd(c, full_matrices=False)
    share = s**2 / (s**2).sum()
    proj = c @ vt[0]
    rho = float(np.corrcoef(rankdata(proj), np.arange(1, len(mu) + 1))[0, 1])
    return {"shares": share.tolist(), "cumulative": np.cumsum(share)[:3].tolist(), "pc1": proj.tolist(),
            "spearman_pc1_slot": rho, "monotone": bool(abs(rho) >= RHO_MIN - EPS)}  # fmt: skip


def geometry(mu: np.ndarray) -> dict:
    """Dumbest way 2's numbers: the step norms ||mu_{k+1} - mu_k||, the shift vectors' norms, and cos(v, mu_2 - mu_1),
    cos(v, v without the first step)."""
    sv = shift_vectors(mu)
    cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))  # noqa: E731
    return {"step_norms": [float(np.linalg.norm(d)) for d in np.diff(mu, axis=0)],
            "norms": {k: float(np.linalg.norm(v)) for k, v in sv.items()},
            "cos_v_v12": cos(sv["v"], sv["v12"]), "cos_v_vno12": cos(sv["v"], sv["vno12"])}  # fmt: skip


# ---- the run (GPU) -------------------------------------------------------------------------------------------------


def gate_of(cases: list[dict], comp: list[dict], gate_min: float | None = None) -> tuple[dict, dict[str, list[dict]]]:
    """Per condition: O's read accuracy per reader over every case (the gate: >= gate_min for both) and the eligible
    cases in generation order (both readers say and read O's and S's answers right), as x6_routes."""
    gate_min = X.GATE if gate_min is None else gate_min
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate, ok = {}, {}
    for cond in ("M", "C0"):
        mine = [c for c in cases if c["condition"] == cond]
        acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in mine])) for w in X.READERS}
        ok[cond] = [c for c in mine if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                           for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
        gate[cond] = {"cases": len(mine), "org_read_accuracy": acc, "gate": gate_min, "eligible": len(ok[cond]),
                      "pass": bool(mine) and all(a >= gate_min - EPS for a in acc.values())}  # fmt: skip
    return gate, ok


def choose(ok_moves: list[dict], n: int, per_pair: int = N_PER_PAIR, seed: int = SPLIT_SEED):
    """Per ordered pair the first per_pair eligible scenes, shuffled by a stream keyed by the seed and the pair: the
    first half (floor) is the fit half, the rest the test half. Returns (fit, test, counts per pair)."""
    fit, test, counts = [], [], {}
    for i, j in pairs(n):
        mine = [c for c in ok_moves if tuple(c["move"]) == (i, j)]
        chosen = mine[:per_pair]
        order = list(range(len(chosen)))
        random.Random(f"{seed}|{n}|{i}-{j}").shuffle(order)
        half = len(chosen) // 2
        fit += [chosen[k] for k in sorted(order[:half])]
        test += [chosen[k] for k in sorted(order[half:])]
        counts[f"{i}-{j}"] = {"eligible": len(mine), "chosen": len(chosen), "fit": half, "test": len(chosen) - half}
    return fit, test, counts


def arm_list(i: int, n: int, doses: tuple[int, ...] = DOSES) -> list[dict]:
    """The arms of one test scene whose bridge sits at slot i in O, in read order."""
    arms: list[dict] = [{"arm": a} for a in REMOVALS]
    for s in doses:
        arms += [{"arm": "write", "s": s, "target": t} for t in range(1, n + 1) if t != i]
        arms.append({"arm": "random", "s": s})
        if i < n:
            arms += [{"arm": a, "s": s, "target": i + 1} for a in ("v", "v12", "vno12")]
        if i > 1:
            arms.append({"arm": "vrev", "s": s, "target": i - 1})
    return arms


def rand_dir(scene: str, d: int):
    """The scene's random unit direction (one per scene, written at every dose), seeded by RAND_SEED and the scene."""
    import torch

    seed = int(hashlib.sha256(f"{RAND_SEED}|{scene}".encode()).hexdigest()[:12], 16)
    r = torch.randn(d, generator=torch.Generator().manual_seed(seed))
    return r / r.norm()


def arm_vector(a: dict, i: int, x, parts: dict, unit: float, mu, shifts: dict, r):
    """The vector added at the bridge word for arm a (None: no edit). x: the scene's change [d]; parts: its parts
    removed by (i) and (iv) and their random parts; mu: the slot means [n, d]; shifts: unit shift vectors; r: the
    scene's random unit direction."""
    kind = a["arm"]
    if kind == "none":
        return None
    if kind == "whole":
        return x
    if kind in ("no_slot", "no_slot_rand", "no_U", "no_U_rand"):
        return x - parts[kind]
    size = a["s"] * unit
    if kind == "write":
        d = mu[a["target"] - 1] - mu[i - 1]
        return size * d / d.norm()
    if kind == "random":
        return size * r
    if kind == "vrev":
        return -size * shifts["v"]
    return size * shifts[kind]


def slot_of(top: int, case: dict) -> int | None:
    """The slot (1-based) whose digit is the top token in O; None for any other token."""
    return case["slot_tokens"].index(top) + 1 if top in case["slot_tokens"] else None


def read_record(c: dict, w: str, a: dict, lg, rd: dict, tok, digits) -> dict:
    top = int(lg.argmax())
    rec = {"scene": c["scene"], "condition": c["condition"], "slots": c["slots"], "i": c["move"][0], "j": c["move"][1],
           "entity": c["bridge"], "reader": w, "arm": a["arm"], "s": a.get("s"), "target": a.get("target"),
           "slot": slot_of(top, c), "kept": int(top == rd["tok_A"]), "top_text": tok.decode([top]),
           **X.read_row(lg, rd, digits)}  # fmt: skip
    if w == X.LOOKUP and c["condition"] == "M":
        rec["route"] = R.classify(top, c)
    return rec


def old_pointer(target: str) -> np.ndarray:
    """U: the 4-d pointer basis fit on the fresh scenes (x0_massmean.subspaces' Alf on x6_routes' probe states), not
    refit."""
    return MM.subspaces(R.STATES[target])[0]["Alf"]


def bridge_states(model, c: dict, layer: int) -> dict:
    """O's and S's states [d] at the bridge word at the layer (the lookup's prompts; the recall's are the same through
    the bridge)."""
    import torch

    ids = c["readers"][X.LOOKUP]["ids"]
    return {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][c["pos"]].float()
            for v in ("org", "alt")}  # fmt: skip


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    assert target in R.STATES, f"47.2 needs the old pointer basis U (x6_routes.STATES): no entry for {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    manifest = out / "manifest.json"  # rewritten as the run goes: gate, items, fit and unit (never a result)
    m: dict = {"exp": EXP, "run": name, "why": why, "test": "47.2", "spec": SPEC, "question": f"{QUESTION} ({PREDICTIONS})",
               "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
               "switches": switches(), "code": git_state(), "layer": layer, "read": "X0's chat read (the top token "
               "after a digit's space token appended to O)", "slots_try": list(SLOTS_TRY), "gate": X.GATE,
               "n": {"candidates_per_pair": N_CAND, "per_pair": N_PER_PAIR, "c0_candidates": N_C0_CAND, "c0": N_C0},
               "seeds": {"scenes": SEED, "split": SPLIT_SEED, "random_directions": RAND_SEED,
                         "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                         "examples": X.EXAMPLES_SEED},
               "doses": list(DOSES), "decisive_dose": DECISIVE, "arms": ARM_TEXT, "U_from": R.STATES[target],
               "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {
            "question": NO_PREDICTION,
            "batch": 52,
            "rules_first_scored": SCORED,
            "sealed": "none (batch 52 coverage)",
        }
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp_all, gates, n, cases, ok = [], {}, None, [], {}
    for slots in SLOTS_TRY:  # the fallback is decided here, by the competence gate, before any patch
        cases, dropped = build_cases(tok, slots)
        comp = X.competence(model, cases, digits, ws)
        comp_all += [{**r, "slots": slots} for r in comp]
        gate, ok = gate_of(cases, comp)
        gates[str(slots)] = {"dropped": dict(dropped), **gate}
        if gate["M"]["pass"]:
            n = slots
            break
    X.write_jsonl(out / "competence.jsonl", comp_all)
    (out / "gate.json").write_text(json.dumps({"slots": n, "gates": gates}, indent=2) + "\n")
    m.update({"slots": n, "tested": n is not None,
              "fallback": {"six_failed_gate": n != SLOTS_TRY[0], "used": n,
                           "note": "six slots failed the competence gate: five slots" if n == 5 else
                           "six slots passed the competence gate" if n == 6 else "five slots failed too: not tested"}})  # fmt: skip
    if n is None:
        manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print("not tested: the move scenes missed the gate at six and at five slots; see gate.json", flush=True)
        return out
    X.write_jsonl(out / "cases.jsonl", cases)
    fit_c, test_c, counts = choose(ok["M"], n)
    c0 = ok["C0"][:N_C0] if gates[str(n)]["C0"]["pass"] else []
    (out / "split.json").write_text(json.dumps({"seed": SPLIT_SEED, "per_pair": counts, "fit": [c["scene"] for c in fit_c],
                                                "test": [c["scene"] for c in test_c], "c0": [c["scene"] for c in c0]},
                                               indent=1) + "\n")  # fmt: skip
    m["items"] = {"fit": len(fit_c), "test": len(test_c), "c0": len(c0)}
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    u_old = torch.tensor(old_pointer(target), dtype=torch.float32, device=dev)
    rows: list[dict] = []
    with torch.no_grad():
        for c in progress(c0, "C0 (case)"):
            h = bridge_states(model, c, layer)
            edits = [{}, {layer: AddRows((h["alt"] - h["org"]).to(dev)[None], [c["pos"]])}]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                rows += [read_record(c, w, {"arm": a}, lg, rd, tok, digits)
                         for a, lg in zip(("none", "whole"), logits, strict=True)]  # fmt: skip
        hs, labels, groups = [], [], []
        for c in progress(fit_c, f"fit half: O and S states at L{layer} (case)"):
            h = bridge_states(model, c, layer)
            for v, slot in (("org", c["move"][0]), ("alt", c["move"][1])):
                hs.append(h[v].cpu().numpy())
                labels.append(slot)
                groups.append(c["layout"])
        h_fit = np.stack(hs)
        fit = fit_slots(h_fit, labels, groups, n)
        np.savez(out / "fit.npz", mu=fit["mu"].astype(np.float32), W=fit["W"].astype(np.float32),
                 h=h_fit.astype(np.float32), slot=np.array(labels), group=np.array(groups),
                 scene=np.array([c["scene"] for c in fit_c for _ in (0, 1)]), prompt=np.array(["O", "S"] * len(fit_c)))  # fmt: skip
        w_slot = torch.tensor(fit["W"], dtype=torch.float32, device=dev)
        x_fit = torch.tensor(h_fit[1::2] - h_fit[0::2], dtype=torch.float32, device=dev)
        deltas = []
        for c in progress(test_c, f"test half: Δ at L{layer} (case)"):
            h = bridge_states(model, c, layer)
            deltas.append(h["alt"] - h["org"])
        x = torch.stack(deltas).to(dev)
        slot_part, u_part = (x @ w_slot) @ w_slot.T, (x @ u_old) @ u_old.T
        share = {k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                 for k, v in (("slot", slot_part), ("U", u_part))}  # fmt: skip
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        parts = {"no_slot": slot_part, "no_slot_rand": SP.random_subspace_part(x, share["slot"], basis),
                 "no_U": u_part, "no_U_rand": SP.random_subspace_part(x, share["U"], basis)}  # fmt: skip
        unit = float(np.median(slot_part.norm(dim=-1).cpu().numpy()))
        mu = torch.tensor(fit["mu"], dtype=torch.float32, device=dev)
        shifts = {k: torch.tensor(v / np.linalg.norm(v), dtype=torch.float32, device=dev)
                  for k, v in shift_vectors(fit["mu"]).items()}  # fmt: skip
        m["fit"] = {k: fit[k] for k in ("states", "dropped_singletons", "per_slot", "groups")}
        m["fit"]["W_rank"] = int(fit["W"].shape[1])
        m["unit"] = {"value": unit, "rule": "the median over the test half of ||W W^T Delta|| (Delta = h_S - h_O at the "
                     "bridge word); a write at dose s has norm s * unit",
                     "fit_half_median": float(np.median(((x_fit @ w_slot).norm(dim=-1)).cpu().numpy()))}  # fmt: skip
        manifest.write_text(
            json.dumps(m, indent=2, ensure_ascii=False) + "\n"
        )  # the unit is fixed before any arm is read
        norms = []
        for k, c in enumerate(progress(test_c, f"arms at L{layer} (case)")):
            i = c["move"][0]
            arms = arm_list(i, n)
            r = rand_dir(c["scene"], x.shape[1]).to(dev)
            own = {a: v[k] for a, v in parts.items()}
            vecs = [arm_vector(a, i, x[k], own, unit, mu, shifts, r) for a in arms]
            edits = [{} if v is None else {layer: AddRows(v[None], [c["pos"]])} for v in vecs]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                rows += [read_record(c, w, a, lg, rd, tok, digits) for a, lg in zip(arms, logits, strict=True)]
            norms.append({"scene": c["scene"], "i": i, "j": c["move"][1], "norm": round(float(x[k].norm()), 4),
                          "slot_norm": round(float(slot_part[k].norm()), 4), "U_norm": round(float(u_part[k].norm()), 4),
                          "share_slot": round(float(share["slot"][k]), 5), "share_U": round(float(share["U"][k]), 5)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- the verdict (CPU) ---------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.2 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def shares(sw: dict[str, list[int]], ents: list[str], n_boot: int) -> tuple[dict[str, list[float]], dict]:
    """Each key's share with a cluster-bootstrap interval over bridge items (paired: the same draws for every key)."""
    rr = X.resampled_rates(sw, ents, n_boot)
    return {k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in sw.items()}, rr


def paired(rr: dict, pt: dict, a: str, b: str) -> list[float]:
    """a - b with its paired interval."""
    return [pt[a][0] - pt[b][0], *X.interval(rr[a] - rr[b])]


def index_rows(rows: list[dict]) -> dict[tuple, dict]:
    return {(r["scene"], r["reader"], r["arm"], r["s"], r["target"]): r for r in rows}


def removal_cells(lk: list[dict], at: dict, scenes: list[str], n_boot: int) -> dict:
    """On these scenes: the route shares per removal arm, (i)'s position cut beyond random (pos(no_slot_rand) -
    pos(no_slot)) and (iv)'s difference (pos(no_U) - pos(no_U_rand)), paired."""
    if not scenes:
        return {"n": 0}
    ent = [at[(s, X.LOOKUP, "whole", None, None)]["entity"] for s in scenes]
    sw = {f"{rt}|{a}": [int(at[(s, X.LOOKUP, a, None, None)]["route"] == rt) for s in scenes]
          for a in REMOVALS for rt in ROUTES}  # fmt: skip
    pt, rr = shares(sw, ent, n_boot)
    return {"n": len(scenes), "entities": len(set(ent)),
            "routes": {a: {rt: pt[f"{rt}|{a}"] for rt in ROUTES} for a in REMOVALS},
            "slot_cut_beyond_random": paired(rr, pt, "position|no_slot_rand", "position|no_slot"),
            "U_minus_random": paired(rr, pt, "position|no_U", "position|no_U_rand")}  # fmt: skip


def write_cells(lk: list[dict], at: dict, starts: dict[int, list[str]], n: int, n_boot: int) -> dict:
    """(ii) per dose and (i, t): the share of lookups at the target slot t under the write from i, and under the
    scene's random direction (the same scenes: every test scene whose bridge sits at i)."""
    out = {}
    for s in DOSES:
        for i, sc in starts.items():
            if not sc:
                continue
            ent = [at[(x, X.LOOKUP, "whole", None, None)]["entity"] for x in sc]
            for t in range(1, n + 1):
                if t == i:
                    continue
                sw = {"write": [int(at[(x, X.LOOKUP, "write", s, t)]["slot"] == t) for x in sc],
                      "random": [int(at[(x, X.LOOKUP, "random", s, None)]["slot"] == t) for x in sc]}  # fmt: skip
                pt, rr = shares(sw, ent, n_boot)
                out[f"{s}|{i}-{t}"] = {"s": s, "i": i, "t": t, "n": len(sc), **pt,
                                       "minus_random": paired(rr, pt, "write", "random")}  # fmt: skip
    return out


def shift_cells(lk: list[dict], at: dict, starts: dict[int, list[str]], n: int, n_boot: int) -> dict:
    """(iii) per dose, shift and start slot k: the share of lookups at the shift's target (k + 1; vrev k - 1) and the
    random direction's share at the same target on the same scenes; and the random direction's share at k + 1 pooled
    over the start slots 1..n-1 (the ordinal clause's control)."""
    out: dict = {}
    for s in DOSES:
        for arm in SHIFTS:
            for k, sc in starts.items():
                tgt = k - 1 if arm == "vrev" else k + 1
                if not sc or not 1 <= tgt <= n:
                    continue
                ent = [at[(x, X.LOOKUP, "whole", None, None)]["entity"] for x in sc]
                sw = {"shift": [int(at[(x, X.LOOKUP, arm, s, tgt)]["slot"] == tgt) for x in sc],
                      "random": [int(at[(x, X.LOOKUP, "random", s, None)]["slot"] == tgt) for x in sc]}  # fmt: skip
                pt, rr = shares(sw, ent, n_boot)
                out[f"{s}|{arm}|{k}"] = {"s": s, "arm": arm, "k": k, "target": tgt, "n": len(sc), **pt,
                                         "minus_random": paired(rr, pt, "shift", "random")}  # fmt: skip
        sc = [x for k in range(1, n) for x in starts.get(k, [])]
        if sc:
            ent = [at[(x, X.LOOKUP, "whole", None, None)]["entity"] for x in sc]
            nxt = {x: at[(x, X.LOOKUP, "whole", None, None)]["i"] + 1 for x in sc}
            sw = {"random": [int(at[(x, X.LOOKUP, "random", s, None)]["slot"] == nxt[x]) for x in sc],
                  "v": [int(at[(x, X.LOOKUP, "v", s, nxt[x])]["slot"] == nxt[x]) for x in sc]}  # fmt: skip
            pt, _ = shares(sw, ent, n_boot)
            out[f"{s}|pooled"] = {"s": s, "n": len(sc), **pt}
    return out


def collateral(rows: list[dict], n_boot: int) -> dict:
    """The recall's kept share (top token = O's answer) per arm and dose over the test half (writes and shifts pooled
    over their targets): the clean answer lost alongside the effect."""
    rc = [r for r in rows if r["condition"] == "M" and r["reader"] == X.RECALL]
    out = {}
    for key in dict.fromkeys((r["arm"], r["s"]) for r in rc):
        mine = [r for r in rc if (r["arm"], r["s"]) == key]
        pt, _ = shares({"kept": [r["kept"] for r in mine]}, [r["entity"] for r in mine], n_boot)
        out[f"{key[0]}|{key[1]}"] = {"arm": key[0], "s": key[1], "reads": len(mine), "kept": pt["kept"]}
    return out


def c0_cells(rows: list[dict], n_boot: int) -> dict:
    """C0: per reader, the switch share under the whole change and O's read accuracy unedited."""
    out = {}
    for w in X.READERS:
        mine = {r["scene"]: r for r in rows if r["condition"] == "C0" and r["reader"] == w and r["arm"] == "whole"}
        none = {r["scene"]: r for r in rows if r["condition"] == "C0" and r["reader"] == w and r["arm"] == "none"}
        if not mine:
            continue
        sc = sorted(mine)
        pt, _ = shares({"switched": [mine[x]["switched"] for x in sc], "none_kept": [none[x]["kept"] for x in sc]},
                       [mine[x]["entity"] for x in sc], n_boot)  # fmt: skip
        out[w] = {"n": len(sc), **pt}
    return out


def model_cells(rows: list[dict], n: int, n_boot: int = X.N_BOOT) -> dict:
    """Every cell of one run (test half, lookup unless said): the removal arms on all moves and on moves among slots
    2..n, the writes, the shifts, the recall's collateral, C0."""
    lk = [r for r in rows if r["condition"] == "M" and r["reader"] == X.LOOKUP]
    at = index_rows(lk)
    whole = sorted({r["scene"] for r in lk if r["arm"] == "whole"})
    move = {
        s: (at[(s, X.LOOKUP, "whole", None, None)]["i"], at[(s, X.LOOKUP, "whole", None, None)]["j"]) for s in whole
    }
    starts = {k: [s for s in whole if move[s][0] == k] for k in range(1, n + 1)}
    inner = [s for s in whole if min(move[s]) >= 2]
    return {"n": len(whole), "entities": len({at[(s, X.LOOKUP, "whole", None, None)]["entity"] for s in whole}),
            "per_start": {str(k): len(v) for k, v in starts.items()},
            "removal": removal_cells(lk, at, whole, n_boot), "removal_inner": removal_cells(lk, at, inner, n_boot),
            "writes": write_cells(lk, at, starts, n, n_boot), "shifts": shift_cells(lk, at, starts, n, n_boot),
            "collateral": collateral(rows, n_boot), "c0": c0_cells(rows, n_boot)}  # fmt: skip


def rule(cells: dict, pca: dict, n: int, s: int) -> dict:
    """47.2's clauses at dose s (point estimates; bars with EPS). See the module docstring."""
    starts = range(1, n)  # start slots with a k + 1
    v = {k: cells["shifts"][f"{s}|v|{k}"]["shift"][0] for k in starts if f"{s}|v|{k}" in cells["shifts"]}
    n_works = sum(x >= WORKS - EPS for x in v.values())
    need = math.ceil(ORDINAL_SHARE * (n - 1) - EPS)
    rand = cells["shifts"].get(f"{s}|pooled", {}).get("random", [math.nan])[0]
    others = [v[k] for k in starts if k != 1 and k in v]
    u_diff = cells["removal_inner"].get("U_minus_random", [math.nan])[0]
    pair = [c["write"][0] for c in cells["writes"].values() if c["s"] == s]
    n_pairs = sum(x >= WORKS - EPS for x in pair)
    out = {"s": s, "v_by_start": v, "v_works_from": n_works, "v_needs": need, "random_pooled": rand,
           "U_minus_random_inner": u_diff, "pairs_reaching": n_pairs, "pairs": len(pair),
           "complete": len(v) == n - 1 and len(pair) == n * (n - 1)}  # fmt: skip
    out["clauses"] = {
        "ordinal": bool(pca["monotone"] and n_works >= need and rand <= NEAR_ZERO + EPS),
        "categorical": bool(1 in v and v[1] >= WORKS - EPS and len(others) == n - 2
                            and all(x < OTHERS_BELOW - EPS for x in others) and abs(u_diff) <= U_NEAR + EPS),
        "slot-specific": bool(n_pairs > n * (n - 1) / 2 and not n_works > (n - 1) / 2),
    }  # fmt: skip
    out["holding"] = [lab for lab in LABELS if out["clauses"][lab]]
    out["label"] = LABEL_TEXT[out["holding"][0]] if out["holding"] else "none of the three"
    return out


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), not tested (the gate missed at six and five slots), or its readings."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.2 run {run!r} here, and it is not one of the specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "slots": m.get("slots"),
            "fallback": m.get("fallback"), "gates": json.loads((src / "gate.json").read_text())["gates"]
            if (src / "gate.json").exists() else None}  # fmt: skip
    if m.get("tested") is False:
        return {**base, "status": "not tested", "label": "not tested", "why": "the gate missed at six and five slots"}
    if not (src / "outcomes.jsonl").exists():
        return {**base, "status": "pending", "why": "no outcomes here (the run did not finish)"}
    n = int(m["slots"])
    rows = X.read_jsonl(src / "outcomes.jsonl")
    mu = np.load(src / "fit.npz")["mu"].astype(np.float64)
    pca, geo = pca_reading(mu), geometry(mu)
    cells = model_cells(rows, n, n_boot)
    rules = {s: rule(cells, pca, n, s) for s in DOSES}
    pos = cells["removal"]["routes"]["whole"]["position"]
    interpretable = pos[0] >= NEAR_ZERO - EPS
    label = rules[DECISIVE]["label"] if interpretable else "not interpretable"
    norms = X.read_jsonl(src / "norms.jsonl")
    share = {k: float(np.median([r[f"share_{k}"] for r in norms])) for k in ("slot", "U")}
    return {**base, "status": "tested", "n": cells["n"], "unit": m["unit"], "fit": m["fit"], "items": m["items"],
            "interpretable": interpretable, "whole_position": pos, "label": label, "pca": pca, "geometry": geo,
            "median_share": share, "rules": {str(s): r for s, r in rules.items()}, "cells": cells}  # fmt: skip


def c0_reference(target: str) -> float | None:
    """The three-locker one-pick lookup switch rate (x6_routes' C0 reference), None where there is none."""
    try:
        return R.c0_reference(target)
    except (FileNotFoundError, KeyError):
        return None


def ci(v: list) -> str:
    return "–" if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]")  # fmt: skip


def report_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    tested = [m for m in models if m["status"] == "tested"]
    lines = ["# 47.2: in six-locker scenes, is the order code ordinal, categorical (first vs rest), or slot-specific?", "",
             f"Batch 47, test 47.2 ({SPEC}; {QUESTION}, Dan: {answer}). The test half of each model's routes moves (the "
             "bridge's locker sentence moved from slot i to slot j), every edit at the bridge word at the layer fixed in "
             f"advance, read on O; cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             "## Dumbest way 1 first: the whole change's routes split", "",
             "| model | run | slots | n | arm | identity (= nothing) | position | value | other |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for a in ("none", "whole"):
            rt = m["cells"]["removal"]["routes"][a]
            lines.append(f"| {m['target']} | {m['run']} | {m['slots']} | {m['n']} | {a} | "
                         + " | ".join(ci(rt[x]) for x in ROUTES) + " |")  # fmt: skip
    lines += ["", f"Position share under the whole change below {NEAR_ZERO}: the test is not interpretable (the lookup "
              "answers by lexical match only).", "", "## Verdict", "",
              f"| model | run | status | slots | label at s = {DECISIVE} (decisive) | holding at s = {DECISIVE} | label at s = 1 "
              "| holding at s = 1 |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m.get('why', '')}) | {m.get('slots') or '–'} | "
                         f"{m.get('label', '–')} | | | |")  # fmt: skip
            continue
        r2, r1 = m["rules"][str(DECISIVE)], m["rules"]["1"]
        lines.append(f"| {m['target']} | {m['run']} | tested | {m['slots']} | **{m['label']}** | "
                     f"{', '.join(r2['holding']) or 'none'} | {r1['label'] if m['interpretable'] else 'not interpretable'}"
                     f" | {', '.join(r1['holding']) or 'none'} |")  # fmt: skip
    lines += ["", "## The fit (held-out half): PCA of the slot means", "",
              "| model | states | W rank | PC1 | PC1-2 | PC1-3 | Spearman(PC1, slot) | monotone (|ρ| >= 0.9) | step norms ‖μk+1 − μk‖ | cos(v, μ2 − μ1) | cos(v, v without step 1) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        p, g = m["pca"], m["geometry"]
        cum = [f"{x:.2f}" for x in p["cumulative"]] + ["–"] * (3 - len(p["cumulative"]))
        lines.append(f"| {m['target']} | {m['fit']['states']} | {m['fit']['W_rank']} | {' | '.join(cum)} | "
                     f"{p['spearman_pc1_slot']:.2f} | {'yes' if p['monotone'] else 'no'} | "
                     f"{', '.join(f'{x:.2f}' for x in g['step_norms'])} | {g['cos_v_v12']:.2f} | {g['cos_v_vno12']:.2f} |")  # fmt: skip
    lines += ["", "## (i) and (iv): the slot subspace W and the old U removed (lookup, position share)", "",
              "| model | moves | n | whole | without W | without random (W's share) | W's cut beyond random | without U | "
              "without random (U's share) | U − random | median share W / U |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for key, label in (("removal", "all"), ("removal_inner", f"among slots 2-{m['slots']}")):
            c = m["cells"][key]
            if not c["n"]:
                continue
            pos = {a: c["routes"][a]["position"] for a in REMOVALS}
            sh = m["median_share"]
            lines.append(f"| {m['target']} | {label} | {c['n']} | {ci(pos['whole'])} | {ci(pos['no_slot'])} | "
                         f"{ci(pos['no_slot_rand'])} | {ci(c['slot_cut_beyond_random'])} | {ci(pos['no_U'])} | "
                         f"{ci(pos['no_U_rand'])} | {ci(c['U_minus_random'])} | {sh['slot']:.3f} / {sh['U']:.3f} |")  # fmt: skip
    for s in DOSES:
        lines += ["", f"## (iii) shift vectors at s = {s} (share of lookups at the target slot, by start slot k)", "",
                  "| model | shift | k | target | n | shift | random (same scenes) | shift − random |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for m in tested:
            for c in (c for c in m["cells"]["shifts"].values() if c["s"] == s and "arm" in c):
                lines.append(f"| {m['target']} | {c['arm']} | {c['k']} | {c['target']} | {c['n']} | {ci(c['shift'])} | "
                             f"{ci(c['random'])} | {ci(c['minus_random'])} |")  # fmt: skip
            p = m["cells"]["shifts"].get(f"{s}|pooled")
            if p:
                lines.append(f"| {m['target']} | v, pooled over k = 1..{m['slots'] - 1} | all | k + 1 | {p['n']} | "
                             f"{ci(p['v'])} | {ci(p['random'])} | |")  # fmt: skip
    for s in DOSES:
        lines += [
            "",
            f"## (ii) pairwise writes at s = {s}: share at the target slot (rows: start i; columns: target t)",
            "",
        ]
        for m in tested:
            n = m["slots"]
            lines += [f"**{m['target']}** (random direction's share at t in brackets)", "",
                      "| i \\ t | " + " | ".join(str(t) for t in range(1, n + 1)) + " |", "|---|" + "---|" * n]  # fmt: skip
            for i in range(1, n + 1):
                cellv = [m["cells"]["writes"].get(f"{s}|{i}-{t}") for t in range(1, n + 1)]
                lines.append(f"| {i} | " + " | ".join("–" if c is None else f"{c['write'][0]:.2f} ({c['random'][0]:.2f})"
                                                      for c in cellv) + " |")  # fmt: skip
            lines.append("")
    lines += ["## Rule clauses per dose", "", "| model | s | v ≥ 0.25 from (of start slots) | needed (ordinal) | random "
              "pooled | U − random (2-n) | pairs ≥ 0.25 | ordinal | categorical | slot-specific |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for s in DOSES:
            r = m["rules"][str(s)]
            cl = r["clauses"]
            lines.append(f"| {m['target']} | {s} | {r['v_works_from']} of {m['slots'] - 1} | {r['v_needs']} | "
                         f"{r['random_pooled']:.3f} | {r['U_minus_random_inner']:.3f} | {r['pairs_reaching']} of "
                         f"{r['pairs']} | {'yes' if cl['ordinal'] else 'no'} | {'yes' if cl['categorical'] else 'no'} | "
                         f"{'yes' if cl['slot-specific'] else 'no'} |")  # fmt: skip
    lines += ["", "## Collateral: the recall keeps O's answer (test half, both doses' arms pooled over targets)", "",
              "| model | arm | s | reads | recall kept |", "|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        lines += [f"| {m['target']} | {c['arm']} | {c['s'] if c['s'] is not None else ''} | {c['reads']} | {ci(c['kept'])} |"
                  for c in m["cells"]["collateral"].values()]  # fmt: skip
    lines += ["", "## C0 sanity, gate, counts (descriptive)", ""]
    for m in models:
        if m["status"] == "pending":
            lines.append(f"- {m['target']} ({m['run']}): pending ({m['why']}).")
            continue
        g = m["gates"] or {}
        gtxt = "; ".join(f"{k} slots: moves O read accuracy {v['M']['org_read_accuracy']} (pass {v['M']['pass']}, "
                         f"eligible {v['M']['eligible']} of {v['M']['cases']}), C0 eligible {v['C0']['eligible']} of "
                         f"{v['C0']['cases']}" for k, v in g.items())  # fmt: skip
        if m["status"] != "tested":
            lines.append(f"- {m['target']} ({m['run']}): not tested. Gates: {gtxt}.")
            continue
        c0 = m["cells"]["c0"]
        ref = c0_reference(m["target"])
        c0txt = "; ".join(f"{'lookup' if w == X.LOOKUP else 'recall'} switch {ci(v['switched'])} (n = {v['n']})"
                          for w, v in c0.items()) or "no C0 items"  # fmt: skip
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}, {m['slots']} slots; {m['fallback']['note']}): gates: "
                     f"{gtxt}. Items: fit {m['items']['fit']}, test {m['items']['test']} ({m['cells']['entities']} bridge "
                     f"items; per start slot {m['cells']['per_start']}), C0 {m['items']['c0']}. Unit (median "
                     f"‖W W^T Δ‖, test half) {m['unit']['value']:.3f} (fit half {m['unit']['fit_half_median']:.3f}). C0: "
                     f"{c0txt}; the three-locker reference (one-pick lookup switch) "
                     f"{'none' if ref is None else f'{ref:.2f}'}.")  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """47.2's verdict (sealed until Q47.2), or with coverage (batch 52) the same rules on the given runs, no seal guard,
    "no prediction" in place of Dan's answer, written to x52_six-<UTC>/."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    out = RESULTS / f"{'x52_six' if coverage else 'x47_2'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = report_lines(models, answer, n_boot)
    if coverage:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ")
    (out / "x47_2.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str) + "\n"
    )
    (out / "x47_2.md").write_text("\n".join(lines) + "\n")
    ex = examples_lines([m["run"] for m in models if m["status"] == "tested"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- the verify-pack view (CPU) ------------------------------------------------------------------------------------


def marked(decode, ids: list[int], pos: int, suffix: list[int]) -> str:
    """The prompt as the model reads it (ids, then the read's space token) with the patched token in ⟦...⟧."""
    return decode(ids[:pos]) + "⟦" + decode(ids[pos : pos + 1]) + "⟧" + decode(ids[pos + 1 :] + suffix)


def arm_label(r: dict) -> str:
    return r["arm"] + (f" s={r['s']}" if r["s"] is not None else "") + (f" →{r['target']}" if r["target"] else "")


def examples_lines(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> list[str]:
    """Per run, k random test-half items (seed 0): each reader's O prompt exactly as read with the patch position
    marked, the source prompt S, the expected digit per route, and every arm's answer (top token, slot, route)."""
    lines = ["# 47.2 examples (verify pack): O as the model reads it, ⟦…⟧ the bridge word where every arm's vector is "
             "added at L; each arm's top token, the slot whose digit it is, and the lookup's route. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        dec = decode
        if dec is None:
            from bridge_jspace.review import checks as RC

            tk = RC.tokenizer(m["model"]["target"])
            dec = lambda ids, tk=tk: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
        test = json.loads((src / "split.json").read_text())["test"]
        rows = X.read_jsonl(src / "outcomes.jsonl")
        pick = sorted(random.Random(seed).sample(sorted(test), min(k, len(test))))
        lines += [f"## {run} ({m['model']['target']}, L{m['layer']}, {m['slots']} slots): {len(pick)} random test items "
                  f"of {len(test)} (seed {seed})", ""]  # fmt: skip
        for s in pick:
            c = cases[s]
            i, j = c["move"]
            lines += [f"### {s}: the {c['bridge']}'s locker sentence moves from slot {i} to slot {j}", "",
                      f"Slots' digits in O {c['values']}; expected: identity {c['expect']['identity']}, position "
                      f"{c['expect']['position']}, value {c['expect']['value']}.", ""]  # fmt: skip
            for w, rd in c["readers"].items():
                mine = [r for r in rows if r["scene"] == s and r["reader"] == w]
                lines += [f"**{'lookup' if w == X.LOOKUP else 'recall'}** ({rd['question']}): O's answer {rd['answer']}, "
                          f"S's {rd['cf_answer']}", "", "O, as read:", "", "```",
                          marked(dec, rd["ids"]["org"], c["pos"], c["space"]), "```", "", "S (the source):", "", "```",
                          marked(dec, rd["ids"]["alt"], c["pos"], c["space"]), "```", "",
                          "| arm | answer | slot | route | kept O's answer |", "|---|---|---|---|---|"]  # fmt: skip
                lines += [f"| {arm_label(r)} | {r['top_text']!r} | {r['slot'] or ''} | {r.get('route') or ''} | "
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
    ap.add_argument("--name", help="run: the run name (results/x47_six/<name>/)")
    ap.add_argument("--runs", nargs="+", default=[RUNS["qwen3.5-9b"], RUNS["muse-glimmer-30b"]],
                    help="verdict / examples: the 47.2 runs (9B and Muse; the 27B's if it ran)")  # fmt: skip
    ap.add_argument("--why", default="batch 47, test 47.2 (jobs/c3/batch47.yaml; Q47.2)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--out", default=None, help="plan: results/x47_six/plan-<stamp>/ (one folder for every target)")
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(Path(a.out) if a.out else None)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, a.coverage)
    else:
        stage_examples(a.runs)


if __name__ == "__main__":
    main()
