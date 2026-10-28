"""x51_addr (batch 51, test 51.11; Dan 28 Oct 19:00, jobs/c3/batch51.yaml addendum_3, design and rules fixed in advance;
Q51.11 in predictions/2026-10-28_dan.md): what is the address, independent of how we built it? Part 1 the dimension vs
the number of slots, part 2 whether three methods find the same code, part 3 the geometry (categories, an order or a
line), part 4 the finding's wording by outcome. 9B parts 1-3, Muse parts 1-3, 27B part 2 only.

As computed (fixed before any run; Dan may override before the enqueue; the specs jobs/c3/x51_11_*.yaml repeat it):

Scenes (CPU, the target's tokenizer). x47_six's generator (its pools, sentences, encoding, chat rendering, X0's read) at
S in {3, 4, 6, 8} locker sentences, the S locker sentences first, then three pick sentences (the asked person picks the
bridge, two others two other locker items; seeded). A position counterfactual pair: in S the bridge's locker sentence
and the sentence at slot j trade places, each keeping its own digit (x7_pcf's "same item moved, digits kept"), so the
lookup's answer is the same in O and S (asserted per pair: the answer digit fixed) and only the bridge sentence's slot
changes (i -> j). The counterfactual target = O's digit at slot j (the position route's answer). Per S and ordered slot
pair (i, j) a seeded candidate stream (SEED, S, i, j), CAP[S] candidates. Slots are positions: every locker sentence of
O and S must span the same number of tokens and no token may straddle two sentences; per S the modal (sentence length,
slot start indices) is kept and other scenes are dropped and counted (S = 3 and 6 are regenerated with this generator:
the stored routes / 47.2 scenes carry a new digit in S, a value counterfactual). Entities: the bridge animal, split
60 / 20 / 20 (train / select / test) over the generator's animal pool (x48_das.split_entities, seed 0), the same split
for every S and part.

Part 1 (GPU, per S in the order 6, 3, 4, 8): candidates read per ordered pair in generator order, in chunks of 8: X0's
competence (both readers say and read O's and S's answers right = eligible), then the whole change h_S - h_O at the
bridge word at L on O (the lookup's read): a pair is kept when it sends the lookup to the position answer (49.8 / 51.3);
per ordered pair until ceil(360 / pairs) position pairs, its candidates run out, or 48 candidates read without one
(given up); if the S has < 300 pairs then, the remaining candidates of the live ordered pairs round-robin until 300.
Gate: O's read accuracy >= 0.80 per reader over every candidate read at that S, else the S is not tested. U and P are
fit on every eligible train-entity scene read at that S (every move, whatever its whole-change route, as 47.2 and
x7_pcf fit theirs); R on the position-routed train pairs (as 49.8 / 51.3): U_S = x47_six.fit_slots (the layout-free
class means of the O states by slot i and the S states by slot j, x0_massmean.mass_mean, rank S - 1; mu_1..mu_S); P_S =
x7_pcf.top_pcs of those scenes' Delta (centered PCA, label-free), top 7; hbar = their states' mean; R_S,k = DAS for
k in {1, 2, 3, 4, 5, 7}: 51.3's loop (x51_das.train_fit: x48_das's Adam lr 1e-3, batch 16, micro-batches of 8 halved
on CUDA OOM, <= 300 steps, early stopping on the select split's IIA every 25 steps, patience 4), the target O's digit at
slot j (h <- h_O + R R^T (h_S - h_O) at the bridge word at L of the O prompt); an R trained on
shuffled targets per k ("shuffled-pair R": the training rows' targets permuted once, its dev targets too); an untrained
random R per k (QR of a seeded Gaussian). Reads on the select and test pairs, both readers, X0's chat read with AddRows
at the bridge word: none, whole, U_S U_S^T Delta (its native rank), and per k P_k P_k^T Delta, R_k R_k^T Delta, the
shuffled R, the random R. own-IIA = the lookup's top token is the position answer. d*(S) = the smallest k whose test
own-IIA >= 0.80 while the random R of that k <= 0.15 (the random bar per k); none: d*(S) > 7. Rules (point estimates on
the test entities' pairs, EPS 1e-9 at the bars; d* > 7 read as infinity): ordinal = d* <= 2 at every S; one per slot =
d*(S) >= S - 2 at every S and d*(8) >= 5; growing = 3 <= d*(8) <= 5 and d* non-decreasing in S; else in between; the
first holding label in this order is the answer (every holding one listed).

Part 2 (GPU; S = 6 decisive, S = 3 beside; the 27B: S = 6 only, built in the job without shuffled twins). Bases at the
working dimension: U_6 (rank 5), P_6 top-d*(6), R_6 at d*(6) (d* from part 1's reads; d* > 7: k = 7, flagged). Items:
test-entity scenes eligible on O and S (X0's competence), per start slot the first P2_PER_START in a round-robin over the
targets. Per item and target t != j (j the bridge's slot): the swap 2 (mu_t - mu_j) (x8_write's pointer swap at 2x) and
its projections 2 B B^T (mu_t - mu_j) for B in {U, P, R}, each beside a random direction of its norm (seeded per item,
target and basis); cross-removal: the swapped state's B-coordinates reset to hbar's, h <- (h + v) - X X^T (h + v - hbar)
for X in {U, P, R} and every swap (the removal acts on the state after the swap, so a swap inside X is removed with
it; removal before the swap would leave a swap inside X intact), and per item each removal alone. Share = the lookup
answers slot t's digit. reach_B = share(swap through B) / share(whole swap); cut(X -> B) = 1 - share(X removed, swap
through B) / share(swap through B), the six X != B. Rules: one code = every reach >= 0.6 and every cut >= 0.6; partly
overlapping = every reach >= 0.6 and every cut < 0.3; different = reach_P or reach_R < 0.3; else in between. U's
projection of mu_t - mu_j is mu_t - mu_j itself (the means span U by construction), so reach_U = 1 identically and
the U column equals the whole swap. Geometry: pairwise mean cos^2 of the principal angles (||A^T B||_F^2 / min rank)
against max rank / d and 20 seeded random pairs of the same ranks.

Part 3 (GPU; S = 6, the means of part 1's fit). Items: held-out (select and test) scenes eligible on O and S with the
bridge in slot 1 or slot 6, the first 100 per end. From slot 1: dose x (mu_3 - mu_1) / 2 and dose x (mu_5 - mu_1) / 2;
from slot 6: toward 4 and toward 2; doses 2 (decisive, the addendum's arm) and 4 (dumbest way: half a 2x swap is one
real change's size); the full swaps 2 (mu_far - mu_start); a random direction of each vector's norm. Read: the slot the
lookup answers, classed original / midpoint / far / near (start +- 1 toward far, when not the midpoint) / another slot
/ not a slot. Rules at dose 2 (4 beside), shares pooled per end over its two midpoint arms: metric order = midpoint >=
0.3 from both ends; categories = midpoint < 0.1 from both ends while the full swaps reach >= 0.4 of their target
(pooled); first vs the rest = >= 0.3 from slot 1 and < 0.3 from slot 6; else none of the three. Every vector's norm is
recorded beside the real change's size (the median ||U U^T Delta|| over the test pairs) and ||h_O||. Means (CPU, S = 6
and 8): pairwise distances ||mu_i - mu_j|| by |i - j|, their spread, PC shares and PC1 per slot (x47_six.pca_reading).

Part 4: the addendum's wording table, the first row whose parts match (a part the model lacks matches only "any").

SEALED: run writes no verdict; `verdict` and `view` (CPU) refuse until Dan's Q51.11 line is committed at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x51_addr.py plan --out results/x51_addr/plan-<UTC>           # CPU, tokenizer
BJ_TARGET=qwen3.5-9b BJ_DAS_GDN=torch uv run python scripts/x51_addr.py run --part 1 --name qwen35_9b_x51_11_p1
BJ_TARGET=qwen3.5-9b BJ_DAS_GDN=torch uv run python scripts/x51_addr.py run --part 2 --name qwen35_9b_x51_11_p2 \\
    --part1 qwen35_9b_x51_11_p1
BJ_TARGET=qwen3.6-27b BJ_DAS_GDN=torch uv run python scripts/x51_addr.py run --part 2 --name x51_11_p2_27b   # builds S6
uv run python scripts/x51_addr.py verdict          # CPU, after Q51.11 (every run of RUNS that is here)
uv run python scripts/x51_addr.py view
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
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
from scripts import x7_pcf as PCF
from scripts import x47_six as SIX
from scripts import x48_das as D
from scripts import x49_das_pos as Q
from scripts import x51_das as Z

EXP = "x51_addr"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = D.PREDICTIONS
QUESTION = "Q51.11"
LOOKUP, RECALL = X.LOOKUP, X.RECALL
READER_NAME = D.READER_NAME
RENDERING = "chat"
RUNS: dict[str, dict[int, str]] = {
    "qwen3.5-9b": {1: "qwen35_9b_x51_11_p1", 2: "qwen35_9b_x51_11_p2", 3: "qwen35_9b_x51_11_p3"},
    "muse-glimmer-30b": {1: "muse30_x51_11_p1", 2: "muse30_x51_11_p2", 3: "muse30_x51_11_p3"},
    "qwen3.6-27b": {2: "x51_11_p2_27b"},
}
SLOTS = (6, 3, 4, 8)  # part 1's run order: 6 first (parts 2 and 3 read it), 8 last (the longest prompts)
RULE_SLOTS = (3, 4, 6, 8)
KS = (1, 2, 3, 4, 5, 7)
POS_TARGET, POS_MIN = 360, 300
CAP = {3: 300, 4: 200, 6: 120, 8: 80}  # candidates generated per ordered slot pair (the read stops at the quota)
CHUNK = 8
GIVE_UP = 48  # an ordered pair with no position pair after this many candidates read is not read further
OWN_BAR, RAND_BAR = 0.80, 0.15
SWAP_DOSE = 2
P2_SLOTS, P2_MAIN = (6, 3), 6
P2_PER_START = {3: 40, 4: 30, 6: 20, 8: 15}
P3_S, P3_N, P3_DOSES, P3_DECISIVE = 6, 100, (2, 4), 2
BASES = ("U", "P", "R")
REACH, CUT_ONE, CUT_PARTLY, DIFFERENT = 0.6, 0.6, 0.3, 0.3
MID_WORKS, MID_NONE, FULL_REACH = 0.3, 0.1, 0.4
N_RANDOM_SUBSPACES = 20
SEED, INIT_SEED, SHUFFLE_SEED, RAND_SEED, DIR_SEED, GEO_SEED = 5110, 5111, 5112, 5113, 5114, 5115
EPS = 1e-9  # a value at a bar counts as at the bar
P1_LABELS = {"ordinal": "an ordinal (low-dimensional) code", "one_per_slot": "one dimension per slot",
             "growing": "low-dimensional but growing", "in_between": "in between"}  # fmt: skip
P2_LABELS = {"one_code": "one code, three bases", "partly": "partly overlapping codes", "different": "different codes",
             "in_between": "in between (none of the three)"}  # fmt: skip
P3_LABELS = {"metric": "a metric order (the code is a line or a curve)", "categories": "categories",
             "first_rest": "first vs the rest", "none": "none of the three"}  # fmt: skip
WORDING = (  # part 4, verbatim (None = "any")
    ("ordinal", "one_code", "metric", "The lookup's position route runs through a **two-dimensional slot code** at the "
     "bridge word that orders the locker sentences; any of three methods finds it; it can be removed, added alone and "
     "swapped, and the lens cannot read it."),
    ("one_per_slot", "one_code", "categories", "… through a **one-code-per-slot address** at the bridge word (one "
     "dimension per locker sentence), found alike by class means, by counterfactual differences and by a learned "
     "subspace; removable, swappable, not readable by the lens."),
    ("growing", "partly", None, "… through a **low-dimensional slot code** (about k dimensions for S slots) that several "
     "bases span in part; the hand-built directions are one basis of it."),
    (None, "different", None, "Our four directions are one of several subspaces that move the lookup by slot; the code "
     "is not a single subspace at this layer (and the address claims are re-graded to the mass-mean construction only)."),
)  # fmt: skip
FOUR_NOTE = (
    'In every case the sentence no longer says "four directions"; "four" becomes a note on the first construction.'
)
SPLITS_HELD = ("select", "test")


# ---- scenes (tokenizer only) ----------------------------------------------------------------------------------------


def position_text(rng: random.Random, animals: list[str], people: list[str], n: int, i: int, j: int) -> dict:
    """One position counterfactual (x47_six.move_text with the digits kept): O with the bridge's locker sentence at
    slot i; S = O with it and the sentence at slot j trading places, each keeping its own digit; the picks are O's."""
    order = rng.sample(animals, n)  # order[k - 1] has slot k
    vals = rng.sample(range(1, 10), n)
    bridge = order[i - 1]
    asked, p1, p2 = rng.sample(people, 3)
    b, c = rng.sample([x for x in order if x != bridge], 2)
    picks = rng.sample([(asked, bridge), (p1, b), (p2, c)], 3)
    o_lock = list(zip(order, vals, strict=True))
    s_lock = list(o_lock)
    s_lock[i - 1], s_lock[j - 1] = o_lock[j - 1], o_lock[i - 1]
    return {"condition": "M", "slots": n, "move": [i, j], "items": order, "values": vals, "new": None, "asked": asked,
            "bridge": bridge, "cf_bridge": bridge, "picks": picks, "o": R.context(o_lock, picks),
            "s": R.context(s_lock, picks),
            "expect": {"identity": vals[i - 1], "position": vals[j - 1], "value": vals[i - 1], "original": vals[i - 1]}}  # fmt: skip


def locker_spans(tok, case: dict) -> dict[str, list[list[int]]]:
    """Per prompt (O, S; the lookup's, as encoded), each locker sentence's token indices (statement_positions.tokens_in
    over its character span in the rendered prompt)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    out = {}
    q = case["readers"][LOOKUP]["question"]
    for v, ctx in (("org", case["context"]), ("alt", case["cf_context"])):
        text = X.render(tok, {"format": "prose", "kind": "digit", "context": ctx, "question": q}, RENDERING, ctx)
        enc = raw_encoding(tok, text, offsets=True)
        assert list(enc["input_ids"]) == case["readers"][LOOKUP]["ids"][v], (
            f"{case['scene']}: {v} re-encodes differently"
        )
        base, at, spans = text.index(ctx), 0, []
        for s in SIX.sentences(ctx)[: case["slots"]]:
            a = base + at
            spans.append(SP.tokens_in(enc["offset_mapping"], a, a + len(s)))
            at += len(s) + 1
        out[v] = spans
    return out


def alignment(spans: dict[str, list[list[int]]]) -> tuple[str, tuple | None]:
    """('', (sentence length, slot start indices)) when every locker sentence of O and S spans the same number of
    tokens, consecutively, no token shared by two sentences, and O and S lay out alike; else (why, None)."""
    lens = {len(t) for v in spans.values() for t in v}
    if len(lens) != 1 or 0 in lens:
        return "the locker sentences differ in token length", None
    for v in spans.values():
        if any(a[-1] >= b[0] for a, b in itertools.pairwise(v)):
            return "a token straddles two locker sentences", None
    starts = {v: tuple(t[0] for t in s) for v, s in spans.items()}
    if starts["org"] != starts["alt"]:
        return "O and S lay the slots out differently", None
    return "", (lens.pop(), starts["org"])


def ordered_pairs(n: int) -> list[tuple[int, int]]:
    return SIX.pairs(n)


def candidates(tok, n: int, cap: int | None = None) -> tuple[list[dict], collections.Counter, dict]:
    """Per ordered slot pair a seeded stream of `cap` (CAP[n]) encodable scenes (x47_six.encode_text: the bridge one
    token at one index in O and S, distinct digit tokens) whose locker sentences align; then only the modal layout
    (sentence length, slot starts) over the S is kept. Drops counted by reason; the layout record."""
    cap = CAP[n] if cap is None else cap
    legs, animals, people = R.pools(tok)
    assert len(animals) >= n, f"{len(animals)} one-token animals for {n} slots"
    assert len(people) >= 3, f"{len(people)} one-token people"
    out, dropped, layouts = [], collections.Counter(), collections.Counter()
    for i, j in ordered_pairs(n):
        rng = random.Random(f"{SEED}|{n}|{i}-{j}")
        got = tries = 0
        while got < cap:
            tries += 1
            assert tries <= 50 * cap, f"{n} slots, move {i}->{j}: cannot fill {cap} scenes ({dropped})"
            case, why = SIX.encode_text(
                tok, position_text(rng, animals, people, n, i, j), f"P{n}-{i}{j}-{tries:04d}", legs
            )
            if case is None:
                dropped[why] += 1
                continue
            why, lay = alignment(locker_spans(tok, case))
            if lay is None:
                dropped[why] += 1
                continue
            case["layout_tokens"] = [lay[0], list(lay[1])]
            layouts[lay] += 1
            out.append(case)
            got += 1
    modal = layouts.most_common(1)[0][0]
    kept = [c for c in out if (c["layout_tokens"][0], tuple(c["layout_tokens"][1])) == modal]
    if len(kept) < len(out):
        dropped["not the modal slot layout"] += len(out) - len(kept)
    return kept, dropped, {"sentence_tokens": modal[0], "slot_starts": list(modal[1]), "layouts_seen": len(layouts)}


def entity_split(tok) -> dict[str, str]:
    """The bridge entities' split over the generator's whole animal pool (x48_das.split_entities, seed 0): one split for
    every S and part."""
    return D.split_entities(R.pools(tok)[1])


def position_pair(c: dict) -> dict:
    """A scene as a position pair: the lookup's counterfactual target = O's digit at slot j (tok_b), S's own answer
    kept beside (s_answer / tok_s); asserts the answer digit fixed across the pair (a position counterfactual, not a
    value one), the bridge's sentence moved with its digit, and the recall's answer the same in O and S."""
    i, j = c["move"]
    lk, rc = c["readers"][LOOKUP], c["readers"][RECALL]
    lo, ls = Q.lockers(c["context"]), Q.lockers(c["cf_context"])
    assert lo[i - 1] == ls[j - 1] == (c["bridge"], c["values"][i - 1]), f"{c['scene']}: the bridge's sentence"
    assert ls[i - 1] == lo[j - 1], f"{c['scene']}: not a swap of two sentences"
    assert lk["answer"] == lk["cf_answer"], f"{c['scene']}: the answer digit changes across the pair"
    assert lk["tok_A"] == lk["tok_b"], f"{c['scene']}: the answer token changes across the pair"
    assert rc["tok_A"] == rc["tok_b"], f"{c['scene']}: the recall's answer changes"
    pos_tok = c["route_tokens"]["position"]
    assert pos_tok == c["slot_tokens"][j - 1] != lk["tok_A"], f"{c['scene']}: the position answer"
    readers = {LOOKUP: {**lk, "s_answer": lk["cf_answer"], "tok_s": lk["tok_b"], "cf_answer": str(c["values"][j - 1]),
                        "tok_b": pos_tok}, RECALL: dict(rc)}  # fmt: skip
    keep = ("scene", "condition", "slots", "bridge", "cf_bridge", "domain", "pos", "space", "context", "cf_context",
            "values", "slot_tokens", "expect", "route_tokens", "layout", "split")  # fmt: skip
    return {**{k: c[k] for k in keep if k in c}, "entity": c["bridge"], "slot_o": i, "slot_s": j, "move": f"{i}->{j}",
            "readers": readers}  # fmt: skip


def ids_digest(c: dict) -> str:
    return hashlib.sha256(json.dumps([c["readers"][w]["ids"] for w in X.READERS]).encode()).hexdigest()[:16]


# ---- plan (CPU) -----------------------------------------------------------------------------------------------------


def stored_47_rates(target: str) -> dict | None:
    """47.2's stored whole-change position share per ordered pair at six slots (new-digit moves; descriptive, for the
    plan's read estimate) and its eligible share; None without the run."""
    src = SIX.RESULTS / SIX.RUNS.get(target, "-")
    if not (src / "outcomes.jsonl").exists():
        return None
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl")
            if r["condition"] == "M" and r["reader"] == LOOKUP and r["arm"] == "whole"]  # fmt: skip
    by: dict[tuple[int, int], list[int]] = collections.defaultdict(list)
    for r in rows:
        by[(r["i"], r["j"])].append(int(r["route"] == "position"))
    g = json.loads((src / "gate.json").read_text())["gates"]["6"]["M"]
    return {"run": src.name, "eligible_share": g["eligible"] / g["cases"],
            "position": {f"{i}-{j}": float(np.mean(v)) for (i, j), v in sorted(by.items())}}  # fmt: skip


def plan_counts(tok, n: int, split: dict[str, str], rates: dict | None) -> tuple[dict, list[dict]]:
    cases, dropped, lay = candidates(tok, n)
    per_pair = collections.Counter(f"{c['move'][0]}-{c['move'][1]}" for c in cases)
    quota = math.ceil(POS_TARGET / len(ordered_pairs(n)))
    lengths = sorted({len(c["readers"][LOOKUP]["ids"]["org"]) for c in cases})
    by_split = collections.Counter(split[c["bridge"]] for c in cases)
    blob: dict[str, Any] = {
        "slots": n, "ordered_pairs": len(ordered_pairs(n)), "candidates": len(cases), "per_pair": sorted(set(per_pair.values())),
        "dropped": dict(dropped), "layout": lay, "prompt_tokens": [lengths[0], lengths[-1]],
        "bridge_token_index": sorted({c["pos"] for c in cases}),
        "bridge_entities": len({c["bridge"] for c in cases}), "candidates_per_split": dict(by_split),
        "quota_per_pair": quota, "pairs_target": quota * len(ordered_pairs(n)), "pairs_min": POS_MIN,
        "worst_case_reads": len(cases),
        "p2_items_test_per_start": {str(s): sum(c["move"][0] == s and split[c["bridge"]] == "test" for c in cases)
                                    for s in range(1, n + 1)} if n in P2_SLOTS else None,
        "p3_items_held_per_end": {str(s): sum(c["move"][0] == s and split[c["bridge"]] in SPLITS_HELD for c in cases)
                                  for s in (1, n)} if n == P3_S else None,
    }  # fmt: skip
    if rates is not None and n == 6:
        exp = 0.0
        for key in per_pair:
            r = rates["position"].get(key, 0.0) * rates["eligible_share"]
            exp += min(per_pair[key], quota / r if r > 0 else GIVE_UP)
        blob["expected_reads_at_47_2_rates"] = {"run": rates["run"], "reads": round(exp), "eligible_share": round(rates["eligible_share"], 3),
                                                "position_by_pair": rates["position"]}  # fmt: skip
    return blob, cases


def rendered(tok, c: dict) -> dict:
    """A scene's lookup prompts as the model reads them: O with the bridge token, its locker sentence (own) and the
    sentence at slot j (target) marked; S with the moved sentence marked."""
    i, j = c["move"]
    so, ss = SIX.sentences(c["context"]), SIX.sentences(c["cf_context"])
    lk = c["readers"][LOOKUP]
    return {"scene": c["scene"], "slots": c["slots"], "move": f"{i}->{j}", "split": c.get("split"), "values": c["values"],
            "answer": lk["answer"], "position_answer": c["values"][j - 1],
            "O": Q.marked(tok, lk["ids"]["org"], c["pos"], c["space"], {"own": so[i - 1], "target": so[j - 1]}),
            "S": Q.marked(tok, lk["ids"]["alt"], c["pos"], c["space"], {"moved": ss[j - 1]})}  # fmt: skip


def stage_plan(out: Path | None = None) -> dict:
    """Tokenizer only: per S the candidates per ordered pair, drops, the slot layout (sentence tokens, slot starts),
    the split, quotas, the reads' worst case (and at 47.2's stored rates at S = 6), part 2 / 3 item supply; five
    rendered pairs at S = 6 and one per other S (seed 0)."""
    from scripts import x45m

    tok = x45m.tokenizer()
    split = entity_split(tok)
    rates = stored_47_rates(pins.TARGET)
    blob: dict[str, Any] = {"target": pins.TARGET, "layer": X.PREDICTED.get(pins.TARGET), "prefix": pins.RUN_PREFIX,
                            "runs": RUNS.get(pins.TARGET), "split": dict(collections.Counter(split.values())),
                            "entities": len(split), "ks": list(KS), "slots_order": list(SLOTS), "S": {}, "rendered": []}  # fmt: skip
    rng = random.Random(X.EXAMPLES_SEED)
    for n in SLOTS:
        b, cases = plan_counts(tok, n, split, rates)
        blob["S"][str(n)] = b
        for c in cases:
            c["split"] = split[c["bridge"]]
        pick = rng.sample(cases, 5 if n == 6 else 1)
        blob["rendered"] += [rendered(tok, c) for c in pick]
        print(json.dumps(b), flush=True)
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{pins.TARGET}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
        blobs = [json.loads(p.read_text()) for p in sorted(out.glob("*.json"))]
        (out / "plan.md").write_text("\n".join(plan_lines(blobs)) + "\n")
        print("wrote", out)
    return blob


def plan_lines(blobs: list[dict]) -> list[str]:
    lines = ["# 51.11 plan (CPU, each target's tokenizer): position counterfactual scenes at S = 3, 4, 6, 8", "",
             "Written by `scripts/x51_addr.py plan` before any run. A pair: the bridge's locker sentence and the sentence "
             "at slot j trade places, digits kept (the lookup's answer unchanged; the target is O's digit at slot j). "
             "Candidates are generated per ordered slot pair; the GPU reads them in order (competence, then the whole "
             "change) until each ordered pair has its quota of pairs whose whole change sends the lookup to the position "
             "answer. Pair counts are known only after the read. UNVERIFIED.", "",
             "| model | L | S | ordered pairs | candidates (per pair) | dropped | locker sentence tokens | slot starts | "
             "prompt tokens | bridge index | quota / target | candidates per split | est. reads (47.2 rates) |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for b in blobs:
        for n in RULE_SLOTS:
            s = b["S"][str(n)]
            est = s.get("expected_reads_at_47_2_rates", {}).get("reads", "-")
            lines.append(f"| {b['target']} | {b['layer']} | {n} | {s['ordered_pairs']} | {s['candidates']} ({s['per_pair']}) | "
                         f"{s['dropped'] or 'none'} | {s['layout']['sentence_tokens']} | {s['layout']['slot_starts']} | "
                         f"{s['prompt_tokens']} | {s['bridge_token_index']} | {s['quota_per_pair']} / {s['pairs_target']} | "
                         f"{s['candidates_per_split']} | {est} |")  # fmt: skip
    for b in blobs:
        s6, s3 = b["S"]["6"], b["S"]["3"]
        lines += ["", f"## {b['target']} (runs {b['runs']})", "",
                  f"- entities {b['entities']}, split {b['split']} (seed 0, the generator's animal pool); k {b['ks']}",
                  f"- part 2 items: test-entity candidates per start slot, S = 6 {s6['p2_items_test_per_start']}, S = 3 "
                  f"{s3['p2_items_test_per_start']} (the run keeps the first {P2_PER_START[6]} / {P2_PER_START[3]} eligible)",
                  f"- part 3 items: held-out candidates with the bridge at slot 1 / 6 (S = 6): {s6['p3_items_held_per_end']} "
                  f"(the run keeps the first {P3_N} eligible per end)", ""]  # fmt: skip
        if "expected_reads_at_47_2_rates" in s6:
            e = s6["expected_reads_at_47_2_rates"]
            lines += [f"- 47.2's stored whole-change position share per ordered pair (new-digit moves, {e['run']}): "
                      f"{e['position_by_pair']}; eligible {e['eligible_share']}", ""]  # fmt: skip
        lines += ["### Rendered pairs (seed 0): the lookup's O and S as the model reads them", "",
                  "⟦bridge:…⟧ the bridge token (every edit at L); in O ⟦own:…⟧ the bridge's locker sentence and ⟦target:…⟧ "
                  "the sentence at slot j (its digit = the counterfactual target); in S ⟦moved:…⟧ the bridge's sentence "
                  "at slot j, its digit kept.", ""]  # fmt: skip
        for e in b["rendered"]:
            lines += [f"#### {e['scene']} (S = {e['slots']}, {e['move']}, {e['split']}): O answers {e['answer']}, S answers "
                      f"{e['answer']}, the position answer {e['position_answer']}", "", "O:", "", "```", e["O"], "```", "",
                      "S:", "", "```", e["S"], "```", ""]  # fmt: skip
    return lines


# ---- the GPU helpers -----------------------------------------------------------------------------------------------


def rand_dir(key: str, d: int):
    """A seeded random unit direction [d] (DIR_SEED and the key)."""
    import torch

    seed = int(hashlib.sha256(f"{DIR_SEED}|{key}".encode()).hexdigest()[:12], 16)
    r = torch.randn(d, generator=torch.Generator().manual_seed(seed))
    return r / r.norm()


def eligible_of(comp: list[dict], c: dict) -> bool:
    right = {(r["reader"], r["variant"]): r for r in comp if r["scene"] == c["scene"]}
    return all(right[(w, v)]["right"] and right[(w, v)]["read_right"] for w in X.READERS for v in ("org", "alt"))


def read_scenes(
    model, chunk: list[dict], layer: int, ws, digits, whole: bool = True
) -> tuple[list[dict], list[dict], dict]:
    """X0's competence on a chunk; per eligible scene (whole=True) the bridge states and the whole change's lookup
    read on O. Returns (records, competence rows, {scene: (h_O, h_S)} for every eligible scene read; CPU fp32)."""
    import torch

    from scripts.exp04_brew_parts import AddRows

    comp = X.competence(model, chunk, digits, ws)
    recs, states = [], {}
    for c in chunk:
        mine = [r for r in comp if r["scene"] == c["scene"]]
        ok = eligible_of(mine, c)
        rec: dict[str, Any] = {"scene": c["scene"], "slots": c["slots"], "move": list(c["move"]), "entity": c["bridge"],
                               "split": c.get("split"), "eligible": int(ok), "ids": ids_digest(c),
                               "org_read": {w: int(next(r["read_right"] for r in mine if r["reader"] == w and r["variant"] == "org"))
                                            for w in X.READERS}}  # fmt: skip
        if ok and whole:
            h_o, h_s = Z.bridge_states(model, [c], layer, "")
            rd = c["readers"][LOOKUP]
            with torch.no_grad():
                lg = X.read_logits(model, rd["ids"]["org"], [{layer: AddRows((h_s - h_o).to(model.device), [c["pos"]])}],
                                   RENDERING, c["space"], ws)[0][0]  # fmt: skip
            top = int(lg.argmax())
            rec.update({"top": top, "route": R.classify(top, c)})
            states[c["scene"]] = (h_o[0], h_s[0])
        recs.append(rec)
    return recs, comp, states


def build_pairs(model, cases: list[dict], n: int, layer: int, ws, digits, desc: str = "") -> dict[str, Any]:
    """Part 1's read: per ordered pair in generator order, chunks of CHUNK candidates (read_scenes) until it has the
    quota of position pairs, its candidates run out, or GIVE_UP candidates are read without one; then, below POS_MIN
    pairs, the remaining candidates of the live ordered pairs round-robin until POS_MIN. Returns the pairs (generation
    order), the eligible train-entity scenes (U's and P's fit), the states of both, every record, the competence rows,
    the gate."""
    from bridge_jspace.utils import progress

    by: dict[tuple[int, int], list[dict]] = {p: [] for p in ordered_pairs(n)}
    for c in cases:
        by[tuple(c["move"])].append(c)  # type: ignore[index]
    quota = math.ceil(POS_TARGET / len(by))
    at = dict.fromkeys(by, 0)
    found: dict[tuple[int, int], list[str]] = {p: [] for p in by}
    recs: list[dict] = []
    comp: list[dict] = []
    states: dict[str, tuple] = {}
    route: dict[str, str] = {}

    def step(p: tuple[int, int]) -> None:
        chunk = by[p][at[p] : at[p] + CHUNK]
        at[p] += len(chunk)
        r, cp, st = read_scenes(model, chunk, layer, ws, digits)
        recs.extend(r)
        comp.extend(cp)
        for rec in r:
            if rec["eligible"]:
                route[rec["scene"]] = rec["route"]
                if rec["route"] == "position" or rec["split"] == "train":
                    states[rec["scene"]] = st[rec["scene"]]
        found[p] += [c["scene"] for c in chunk if route.get(c["scene"]) == "position"]

    def live(p: tuple[int, int]) -> bool:
        return at[p] < len(by[p]) and not (at[p] >= GIVE_UP and not found[p])

    for p in progress(list(by), desc or f"S = {n}: pairs (ordered pair)"):
        while len(found[p]) < quota and live(p):
            step(p)
    topped = 0
    while sum(map(len, found.values())) < POS_MIN and any(live(p) for p in by):
        for p in by:
            if live(p) and sum(map(len, found.values())) < POS_MIN:
                step(p)
                topped += 1
    order = {c["scene"]: k for k, c in enumerate(cases)}
    keep = sorted((s for v in found.values() for s in v), key=order.__getitem__)
    case_of = {c["scene"]: c for c in cases}
    pairs = [position_pair(case_of[s]) for s in keep]
    fit_scenes = [{"scene": s, "slot_o": case_of[s]["move"][0], "slot_s": case_of[s]["move"][1], "layout": case_of[s]["layout"],
                   "route": route[s]} for s in sorted(route, key=order.__getitem__) if case_of[s]["split"] == "train"]  # fmt: skip
    acc = {READER_NAME[w]: float(np.mean([r["org_read"][w] for r in recs])) if recs else None for w in X.READERS}
    gate = {"candidates_read": len(recs), "org_read_accuracy": acc, "gate": X.GATE,
            "eligible": sum(r["eligible"] for r in recs),
            "pass": bool(recs) and all(a is not None and a >= X.GATE - EPS for a in acc.values())}  # fmt: skip
    routes = collections.Counter(r.get("route") for r in recs if r["eligible"])
    info = {"quota_per_pair": quota, "pairs": len(pairs), "topup_chunks": topped, "whole_change_routes": dict(routes),
            "position_share_of_eligible": round(routes["position"] / max(1, gate["eligible"]), 4),
            "per_pair": {f"{i}-{j}": {"read": at[(i, j)], "pairs": len(found[(i, j)]), "candidates": len(by[(i, j)]),
                                      "gave_up": bool(at[(i, j)] >= GIVE_UP and not found[(i, j)])} for i, j in by},
            "ordered_pairs_covered": sum(bool(v) for v in found.values()), "ordered_pairs": len(by),
            "missing_ordered_pairs": [f"{i}-{j}" for (i, j), v in found.items() if not v],
            "all_ordered_pairs": all(found.values()), "at_least_300": len(pairs) >= POS_MIN,
            "fit_scenes": len(fit_scenes)}  # fmt: skip
    return {"pairs": pairs, "fit_scenes": fit_scenes, "states": states, "records": recs, "competence": comp, "gate": gate,
            "info": info}  # fmt: skip


def fit_bundle(fit_scenes: list[dict], h_o, h_s, n: int) -> dict[str, np.ndarray]:
    """On the eligible train-entity scenes read at this S (every move, not only the position-routed ones; as 47.2 and
    x7_pcf fit theirs): U (x47_six.fit_slots: the layout-free slot means' mass-mean basis of the O states by slot i and
    the S states by slot j, rank n - 1) and the means mu [n, d]; P (x7_pcf.top_pcs of their Delta, top max(KS),
    centered, no labels); hbar (their states' mean). h_o / h_s: [len(fit_scenes), d] in fit_scenes' order."""
    assert fit_scenes, "no eligible train-entity scenes"
    h = np.stack([x for k in range(len(fit_scenes)) for x in (h_o[k].numpy(), h_s[k].numpy())]).astype(np.float64)
    slots = [s for f in fit_scenes for s in (f["slot_o"], f["slot_s"])]
    groups = [f["layout"] for f in fit_scenes for _ in (0, 1)]
    fit = SIX.fit_slots(h, slots, groups, n)
    p = PCF.top_pcs((h_s - h_o).double().numpy(), max(KS))
    return {"mu": fit["mu"], "U": fit["W"], "P": p, "hbar": h.mean(0), "fit_states": np.array(fit["states"]),
            "per_slot": np.array([fit["per_slot"][str(k)] for k in range(1, n + 1)])}  # fmt: skip


def arm_names(shuffled: bool) -> list[str]:
    out = ["none", "whole", "U"]
    for k in KS:
        out += [f"P_k{k}", f"R_k{k}", *([f"shuf_k{k}"] if shuffled else []), f"rand_k{k}"]
    return out


def bases_of(fit: dict, mats: dict) -> dict[str, Any]:
    """Every basis read on the pairs, keyed by arm: U, P_k (the top k of P), R_k / shuf_k / rand_k (torch, CPU)."""
    import torch

    out = {"U": torch.tensor(fit["U"], dtype=torch.float32)}
    for k in KS:
        out[f"P_k{k}"] = torch.tensor(fit["P"][:, :k], dtype=torch.float32)
    return out | {key: m.float() for key, m in mats.items()}


def bundle_dir_ok(d: Path) -> bool:
    return (d / "done.json").exists()


def build_s(model, tok, out_s: Path, n: int, layer: int, ws, digits, split: dict[str, str], train: bool, shuffled: bool,
            steps: int, micro: int) -> dict[str, Any]:  # fmt: skip
    """Part 1 at one S into out_s: candidates, the read (pairs, gate), the fit, DAS per k (train), the reads on the
    held-out pairs (train). Writes status.json first and done.json last; returns the status."""
    import torch

    out_s.mkdir(parents=True, exist_ok=False)
    status: dict[str, Any] = {"slots": n, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "train": train,
                              "shuffled": shuffled}  # fmt: skip
    (out_s / "status.json").write_text(json.dumps(status, indent=1) + "\n")
    cases, dropped, lay = candidates(tok, n)
    for c in cases:
        c["split"] = split[c["bridge"]]
    built = build_pairs(model, cases, n, layer, ws, digits)
    X.write_jsonl(out_s / "reads.jsonl", built["records"])
    X.write_jsonl(out_s / "competence.jsonl", built["competence"])
    pairs = built["pairs"]
    info = {"slots": n, "candidates": len(cases), "dropped": dict(dropped), "layout": lay, "gate": built["gate"], **built["info"],
            "pairs_per_split": dict(collections.Counter(p["split"] for p in pairs)),
            "entities_per_split": {s: len({p["entity"] for p in pairs if p["split"] == s}) for s in ("train", "select", "test")},
            "moves_per_split": {s: dict(collections.Counter(p["move"] for p in pairs if p["split"] == s)) for s in ("train", "select", "test")}}  # fmt: skip
    (out_s / "pairs.json").write_text(json.dumps(info, indent=1) + "\n")
    X.write_jsonl(out_s / "cases.jsonl", pairs)
    status["gate"] = built["gate"]
    if not built["gate"]["pass"]:
        status.update({"tested": False, "why": "the competence gate missed (O's read accuracy < 0.80 for a reader)"})
        (out_s / "status.json").write_text(json.dumps(status, indent=1) + "\n")
        (out_s / "done.json").write_text(json.dumps({"tested": False}) + "\n")
        return status
    missing = [s for s in ("train", "select", "test") if not info["pairs_per_split"].get(s)]
    assert not (train and missing), f"S = {n}: no {missing} pairs ({info['pairs_per_split']})"
    st = built["states"]
    fs = built["fit_scenes"]
    X.write_jsonl(out_s / "fit_scenes.jsonl", fs)
    f_o, f_s = torch.stack([st[f["scene"]][0] for f in fs]), torch.stack([st[f["scene"]][1] for f in fs])
    fit = fit_bundle(fs, f_o, f_s, n)
    del f_o, f_s
    h_o = torch.stack([st[p["scene"]][0] for p in pairs]) if pairs else None
    h_s = torch.stack([st[p["scene"]][1] for p in pairs]) if pairs else None
    delta = h_s - h_o if pairs else None
    if pairs:
        torch.save(
            {"scenes": [p["scene"] for p in pairs], "h_O": h_o, "h_S": h_s, "layer": layer},
            out_s / f"states_L{layer}.pt",
        )
    u_t = torch.tensor(fit["U"], dtype=torch.float32)
    test = [k for k, p in enumerate(pairs) if p["split"] == "test"]
    unit = float(np.median(((delta[test] @ u_t).norm(dim=-1)).numpy())) if test else math.nan
    np.savez(out_s / "fit.npz", **{k: v.astype(np.float32) if v.dtype.kind == "f" else v for k, v in fit.items()},
             unit=np.array(unit, dtype=np.float32))  # fmt: skip
    status["unit"] = {
        "value": unit,
        "rule": "the median over the test pairs of ||U U^T Delta|| (the real change's size)",
    }
    status["fit"] = {"scenes": len(fs), "states_used": int(fit["fit_states"]), "per_slot": fit["per_slot"].tolist(),
                     "position_routed_share": round(float(np.mean([f["route"] == "position" for f in fs])), 4)}  # fmt: skip
    if train:
        mats, stops = train_all(model, layer, pairs, delta, n, shuffled, steps, micro, out_s)
        np.savez(out_s / "R.npz", **{k: v.numpy().astype(np.float32) for k, v in mats.items()})
        (out_s / "stops.json").write_text(json.dumps(stops, indent=1) + "\n")
        bases = bases_of(fit, mats)
        rows = read_pairs(model, layer, pairs, delta, bases, arm_names(shuffled), ws, digits, f"S = {n}: reads (pair)")
        for r in rows:
            r["S"] = n
        X.write_jsonl(out_s / "outcomes.jsonl", rows)
        status["stops"] = {k: {kk: v[kk] for kk in ("best_step", "best_dev_iia", "stopped_at", "micro", "oom_micro_tried")}
                           for k, v in stops.items()}  # fmt: skip
    status.update({"tested": True, "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    (out_s / "status.json").write_text(json.dumps(status, indent=1) + "\n")
    (out_s / "done.json").write_text(json.dumps({"tested": True}) + "\n")
    return status


def train_all(model, layer: int, pairs: list[dict], delta, n: int, shuffled: bool, steps: int, micro: int,
              out_s: Path) -> tuple[dict[str, Any], dict[str, dict]]:  # fmt: skip
    """Per k: R_k (51.3's train_fit on the train pairs, early stopping on the select pairs), its shuffled-target twin
    (shuffled), the untrained random R."""
    d = delta.shape[1]

    def rows_of(split: str) -> list[dict]:
        return [{"ids": p["readers"][LOOKUP]["ids"]["org"] + p["space"], "pos": p["pos"], "delta": delta[k],
                 "target": p["readers"][LOOKUP]["tok_b"]} for k, p in enumerate(pairs) if p["split"] == split]  # fmt: skip

    tr, dv = rows_of("train"), rows_of("select")
    mats: dict[str, Any] = {}
    stops: dict[str, dict] = {}
    log: list[dict] = []
    for k in KS:
        mats[f"rand_k{k}"] = D.random_basis(d, k, RAND_SEED + k)
        for shuf in (False, True) if shuffled else (False,):
            key = f"{'shuf' if shuf else 'R'}_k{k}"
            tlog: list[dict] = []
            mats[key], stops[key] = Z.train_fit(model, layer, tr, dv, k, INIT_SEED + 100 * k + (10 if shuf else 0), steps,
                                                micro, (SHUFFLE_SEED + k) if shuf else None, tlog,
                                                f"S = {n} L{layer} DAS {key} ({len(tr)} rows, dev {len(dv)})")  # fmt: skip
            log += [{"S": n, "R": key, "shuffled": shuf, "n_rows": len(tr), **r} for r in tlog]
            X.write_jsonl(out_s / "train.jsonl", log)
    return mats, stops


def read_pairs(model, layer: int, pairs: list[dict], delta, bases: dict, arms: list[str], ws, digits,
               desc: str) -> list[dict]:  # fmt: skip
    """Every arm on the held-out (select, test) pairs, both readers (x49_das_pos.read_rows: X0's chat read, AddRows at
    the bridge; the lookup's switch = the position answer, its route; the recall's move)."""
    import torch

    from bridge_jspace.utils import progress

    dev = model.device
    held = [k for k, p in enumerate(pairs) if p["split"] in SPLITS_HELD]
    x = delta[held].to(dev).float()
    parts = {key: (x @ b.to(dev)) @ b.to(dev).T for key, b in bases.items() if key in arms}
    rows: list[dict] = []
    with torch.no_grad():
        for r, k in enumerate(progress(held, desc)):
            rows += Q.read_rows(model, layer, pairs[k], x[r], {key: v[r] for key, v in parts.items()}, arms, ws, digits)
    return rows


def load_bundle(d: Path) -> dict[str, Any]:
    """A finished S folder (part 1's, or built by part 2 / 3): its status, pairs, fit, R matrices and reads."""
    import torch

    assert bundle_dir_ok(d), f"{d}: not finished (no done.json)"
    st = json.loads((d / "status.json").read_text())
    b: dict[str, Any] = {"dir": d, "status": st, "tested": st.get("tested", False)}
    if not b["tested"]:
        return b
    b["pairs"] = X.read_jsonl(d / "cases.jsonl")
    f = np.load(d / "fit.npz")
    b["fit"] = {k: f[k] for k in f.files}
    if (d / "R.npz").exists():
        r = np.load(d / "R.npz")
        b["mats"] = {k: torch.tensor(r[k]) for k in r.files}
    if (d / "outcomes.jsonl").exists():
        b["rows"] = X.read_jsonl(d / "outcomes.jsonl")
    return b


# ---- part 1's numbers (CPU) -------------------------------------------------------------------------------------------


def curve(rows: list[dict], n_boot: int = 0) -> dict[str, Any]:
    """The lookup's switch (= the position answer) on the test pairs per arm, every k the rows hold; with n_boot
    cluster-bootstrap CIs over bridge entities ([mean, lo, hi]), else points; the recall's move per arm beside; the
    select own-IIA."""
    scenes, ent, t = Q.split_table(rows, "test")
    _, _, sel = Q.split_table(rows, "select")

    def pt(v: list) -> list[float]:
        return D.ci_of(v, ent, n_boot) if n_boot else [float(np.mean(v)) if v else math.nan] * 3

    arms = sorted(t[LOOKUP])
    ks = sorted(int(a[3:]) for a in arms if a.startswith("R_k"))
    shuf = any(a.startswith("shuf_") for a in arms)
    out: dict[str, Any] = {"n": len(scenes), "entities": len(set(ent)), "ks": list(ks),
                           "whole": pt(t[LOOKUP]["whole"]["switched"]), "none": pt(t[LOOKUP]["none"]["switched"]),
                           "U": pt(t[LOOKUP]["U"]["switched"]),
                           "recall_moved": {a: round(float(np.mean(t[RECALL][a]["moved"])), 4) for a in arms}}  # fmt: skip
    for key in ("R", "rand", "P", *(("shuf",) if shuf else ())):
        out[key] = {k: pt(t[LOOKUP][f"{key}_k{k}"]["switched"]) for k in ks}
    out["select_R"] = {k: round(float(np.mean(sel[LOOKUP][f"R_k{k}"]["switched"])), 4) for k in ks}
    return out


def d_star(own: dict[int, float], rand: dict[int, float]) -> dict[str, Any]:
    """d* = the smallest k with own-IIA >= 0.80 and the random R of that k <= 0.15 (None: no k up to the largest k
    read); beside, the smallest k with own >= 0.80 regardless of the random bar and the ks the random bar blocked."""
    ks = tuple(sorted(own))
    hit = [k for k in ks if own[k] >= OWN_BAR - EPS]
    ok = [k for k in hit if rand[k] <= RAND_BAR + EPS]
    return {"d_star": ok[0] if ok else None, "own_only": hit[0] if hit else None,
            "random_blocked": [k for k in hit if k not in ok], "max_k": ks[-1]}  # fmt: skip


def part1_rule(ds: dict[int, int | None]) -> dict[str, Any]:
    """Part 1's labels on d*(S) (None = > max k, read as infinity); a missing S makes it not decidable."""
    missing = [s for s in RULE_SLOTS if s not in ds]
    if missing:
        return {"label": None, "text": f"not decidable: S = {missing} not tested", "holding": [], "clauses": {},
                "not_found": [s for s, v in ds.items() if v is None]}  # fmt: skip
    d = {s: math.inf if ds[s] is None else ds[s] for s in RULE_SLOTS}
    clauses = {
        "ordinal": all(d[s] <= 2 for s in RULE_SLOTS),
        "one_per_slot": all(d[s] >= s - 2 for s in RULE_SLOTS) and d[8] >= 5,
        "growing": 3 <= d[8] <= 5 and all(d[a] <= d[b] for a, b in itertools.pairwise(RULE_SLOTS)),
    }
    holding = [k for k in ("ordinal", "one_per_slot", "growing") if clauses[k]]
    label = holding[0] if holding else "in_between"
    return {"label": label, "text": P1_LABELS[label], "holding": holding, "clauses": clauses,
            "not_found": [s for s in RULE_SLOTS if ds[s] is None]}  # fmt: skip


def part1_numbers(src: Path, n_boot: int) -> dict[str, Any]:
    out: dict[str, Any] = {"run": src.name, "S": {}}
    m = json.loads((src / "manifest.json").read_text())
    out["target"], out["layer"] = m["model"]["target"], m["layer"]
    ds: dict[int, int | None] = {}
    for n in RULE_SLOTS:
        d = src / f"S{n}"
        if not bundle_dir_ok(d):
            out["S"][n] = {"status": "missing" if not d.exists() else "unfinished"}
            continue
        b = load_bundle(d)
        info = json.loads((d / "pairs.json").read_text())
        if not b["tested"]:
            out["S"][n] = {"status": "not tested", "why": b["status"].get("why"), "gate": info["gate"]}
            continue
        cv = curve(b["rows"], n_boot=n_boot)
        dd = d_star({k: v[0] for k, v in cv["R"].items()}, {k: v[0] for k, v in cv["rand"].items()})
        dp = d_star({k: v[0] for k, v in cv["P"].items()}, {k: v[0] for k, v in cv["rand"].items()})
        ds[n] = dd["d_star"]
        out["S"][n] = {"status": "tested", "curve": cv, "d_star": dd, "d_star_P": dp, "pairs": info,
                       "unit": b["status"].get("unit"), "stops": b["status"].get("stops")}  # fmt: skip
    out["rule"] = part1_rule(ds)
    out["d_star"] = ds
    return out


# ---- part 2 (GPU, then CPU) ---------------------------------------------------------------------------------------


def working_bases(b: dict[str, Any], n: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """U (rank n - 1), P top-d*, R at d* (d* from the bundle's test reads; > max k: max k, flagged); torch CPU."""
    import torch

    cv = curve(b["rows"])
    dd = d_star({k: v[0] for k, v in cv["R"].items()}, {k: v[0] for k, v in cv["rand"].items()})
    k = dd["d_star"] if dd["d_star"] is not None else dd["max_k"]
    bases = {"U": torch.tensor(b["fit"]["U"], dtype=torch.float32), "P": torch.tensor(b["fit"]["P"][:, :k], dtype=torch.float32),
             "R": b["mats"][f"R_k{k}"].float()}  # fmt: skip
    assert bases["U"].shape[1] == n - 1, f"U's rank {bases['U'].shape[1]} at S = {n}"
    flag = None if dd["d_star"] is not None else f"d*({n}) > {dd['max_k']}: the working dimension is k = {k}"
    return bases, {"d_star": dd, "k": k, "flag": flag}


def mean_cos2(a, b) -> float:
    """||A^T B||_F^2 / min(rank A, rank B) for orthonormal columns: the mean cos^2 of the principal angles."""
    import torch

    q_a, q_b = R.orthonormal(a.double()), R.orthonormal(b.double())
    return float((torch.linalg.matrix_norm(q_a.T @ q_b) ** 2) / min(q_a.shape[1], q_b.shape[1]))


def geometry_readouts(bases: dict[str, Any], d: int) -> dict[str, Any]:
    """Pairwise mean cos^2 of the principal angles between U, P, R, the random expectation max rank / d and the mean
    over N_RANDOM_SUBSPACES seeded random pairs of subspaces of the same ranks; the angles in degrees."""
    out: dict[str, Any] = {"d": d, "ranks": {k: int(v.shape[1]) for k, v in bases.items()}}
    for a, b in itertools.combinations(BASES, 2):
        ra, rb = bases[a].shape[1], bases[b].shape[1]
        rnd = [mean_cos2(D.random_basis(d, ra, GEO_SEED + 2 * s), D.random_basis(d, rb, GEO_SEED + 2 * s + 1))
               for s in range(N_RANDOM_SUBSPACES)]  # fmt: skip
        out[f"{a}-{b}"] = {"mean_cos2": round(mean_cos2(bases[a], bases[b]), 6), "random_expectation": round(max(ra, rb) / d, 6),
                           "random_mean": round(float(np.mean(rnd)), 6), "random_max": round(float(np.max(rnd)), 6),
                           "angles_deg": D.principal_angles(R.orthonormal(bases[a].double()), R.orthonormal(bases[b].double()))}  # fmt: skip
    return out


def interleaved(cases: list[dict], start: int) -> list[dict]:
    """The scenes whose bridge starts at slot `start`, round-robin over the targets in generation order."""
    lanes = [
        [c for c in cases if c["move"] == [start, t]]
        for t in sorted({c["move"][1] for c in cases if c["move"][0] == start})
    ]
    return [c for row in itertools.zip_longest(*lanes) for c in row if c is not None]


def pick_items(model, cases: list[dict], starts: dict[int, int], splits: tuple[str, ...], ws, digits,
               desc: str) -> tuple[list[dict], dict]:  # fmt: skip
    """Per start slot the first starts[s] scenes (round-robin over targets) of the given entity splits eligible on O and
    S (X0's competence, read here in chunks of CHUNK); counts beside."""
    from bridge_jspace.utils import progress

    items, info = [], {}
    for s, want in progress(list(starts.items()), desc):
        pool = [c for c in interleaved(cases, s) if c["split"] in splits]
        got, read, at = [], 0, 0
        while len(got) < want and at < len(pool):
            chunk = pool[at : at + CHUNK]
            at += len(chunk)
            comp = X.competence(model, chunk, digits, ws)
            read += len(chunk)
            got += [c for c in chunk if eligible_of(comp, c)]
        items += got[:want]
        info[str(s)] = {"pool": len(pool), "read": read, "eligible": len(got), "kept": min(want, len(got))}
    return items, info


def read_arms(model, layer: int, c: dict, arms: list[tuple[dict, Any]], ws, digits, extra: dict) -> list[dict]:
    """Both readers on O under every (meta, vector | None) added at the bridge word at L; the lookup's answered slot
    (x47_six.slot_of), the recall's move off O's answer."""
    import torch

    from scripts.exp04_brew_parts import AddRows

    edits = [{} if v is None else {layer: AddRows(v.to(model.device).float()[None], [c["pos"]])} for _, v in arms]
    rows = []
    with torch.no_grad():
        for w, rd in c["readers"].items():
            logits: Any = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, c["space"], ws)[0]
            for (meta, v), lg in zip(arms, logits, strict=True):
                top = int(lg.argmax())
                rows.append({"scene": c["scene"], "entity": c["bridge"], "split": c["split"], "S": c["slots"],
                             "start": c["move"][0], "reader": w, **meta, "norm": None if v is None else round(float(v.norm()), 4),
                             "top": top, "slot": SIX.slot_of(top, c), "moved": int(top != rd["tok_A"]),
                             "top_text": model.tokenizer.decode([top]), **extra})  # fmt: skip
    return rows


def part2_arms(c: dict, n: int, mu, bases: dict, h, hbar) -> list[tuple[dict, Any]]:
    """Part 2's arms on one item (bridge at slot j): none; each removal alone; per target t != j the swap 2 (mu_t -
    mu_j) whole and through U / P / R, a random direction of each one's norm, and every removal after every swap."""
    j = c["move"][0]

    def proj(b: str, v):
        return bases[b] @ (bases[b].T @ v)

    def removed(x: str, v):
        return v - proj(x, h + v - hbar)

    zero = 0 * h
    arms: list[tuple[dict, Any]] = [({"arm": "none", "removed": None, "basis": None, "target": None}, None)]
    arms += [({"arm": "remove", "removed": x, "basis": None, "target": None}, removed(x, zero)) for x in BASES]
    for t in range(1, n + 1):
        if t == j:
            continue
        step = mu[t - 1] - mu[j - 1]
        sw = {"whole": SWAP_DOSE * step, **{b: SWAP_DOSE * proj(b, step) for b in BASES}}
        for b, v in sw.items():
            arms.append(({"arm": "swap", "removed": None, "basis": b, "target": t}, v))
            arms.append(({"arm": "random", "removed": None, "basis": b, "target": t},
                         rand_dir(f"p2|{c['scene']}|{t}|{b}", v.shape[0]) * v.norm()))  # fmt: skip
            arms += [({"arm": "swap", "removed": x, "basis": b, "target": t}, removed(x, v)) for x in BASES]
    return arms


def part2_one(model, out_s: Path, n: int, b: dict, layer: int, ws, digits, items: list[dict]) -> dict[str, Any]:
    """Part 2 at one S: the working bases, the geometry, the reads on the items."""
    import torch

    from bridge_jspace.utils import progress

    bases, work = working_bases(b, n)
    mu = torch.tensor(b["fit"]["mu"], dtype=torch.float32)
    hbar = torch.tensor(b["fit"]["hbar"], dtype=torch.float32)
    geo = geometry_readouts(bases, int(mu.shape[1]))
    (out_s / "readouts.json").write_text(json.dumps({"working": work, "geometry": geo}, indent=1) + "\n")
    X.write_jsonl(out_s / "swap_items.jsonl", [{k: c[k] for k in ("scene", "bridge", "split", "move", "pos")} | {"ids": ids_digest(c)}
                                              for c in items])  # fmt: skip
    rows: list[dict] = []
    for c in progress(items, f"part 2 S = {n} (item)"):
        h_o, _ = Z.bridge_states(model, [c], layer, "")
        arms = part2_arms(c, n, mu, bases, h_o[0], hbar)
        rows += read_arms(model, layer, c, arms, ws, digits, {"h_norm": round(float(h_o[0].norm()), 4)})
    X.write_jsonl(out_s / "swap_outcomes.jsonl", rows)
    return {"working": work, "items": len(items)}


def cell_values(rows: list[dict], removed: str | None, basis: str) -> tuple[list[tuple], list[int]]:
    """The lookup's hit (answered slot == target) per (item, target) for one cell, keyed for pairing."""
    mine = sorted(((r["scene"], r["target"]), int(r["slot"] == r["target"]), r["entity"]) for r in rows
                  if r["reader"] == LOOKUP and r["arm"] == "swap" and r["removed"] == removed and r["basis"] == basis)  # fmt: skip
    return [(k, e) for k, _, e in mine], [v for _, v, _ in mine]


def ratio_ci(a: list[int], b: list[int], ents: list[str], n_boot: int) -> list[float]:
    """mean(a) / mean(b) with the paired cluster-bootstrap interval (nan where mean(b) is 0)."""
    if not a or float(np.mean(b)) == 0:
        return [math.nan] * 3
    if not n_boot:
        return [float(np.mean(a) / np.mean(b))] * 3
    r = X.resampled_rates({"a": a, "b": b}, ents, n_boot)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = r["a"] / np.where(r["b"] > 0, r["b"], np.nan)
    return [float(np.mean(a) / np.mean(b)), *X.interval(q)]


def part2_cells(rows: list[dict], n_boot: int) -> dict[str, Any]:
    """The table (rows: removed none / U / P / R; columns: the swap through whole / U / P / R): the share of lookups at
    the target, per cell with CIs; the random directions' shares; reach_B and the six cuts with paired CIs; each
    removal alone (the share answering another slot than the original); the recall's move per cell."""
    keys, _ = cell_values(rows, None, "whole")
    ents = [e for _, e in keys]
    table: dict[str, dict[str, list[float]]] = {}
    vals: dict[tuple, list[int]] = {}
    for x in (None, *BASES):
        table[x or "none"] = {}
        for bcol in ("whole", *BASES):
            k2, v = cell_values(rows, x, bcol)
            assert k2 == keys, f"cell ({x}, {bcol}): the (item, target) set differs"
            vals[(x, bcol)] = v
            table[x or "none"][bcol] = D.ci_of(v, ents, n_boot) if n_boot else [float(np.mean(v))] * 3
    rnd = {}
    for bcol in ("whole", *BASES):
        mine = sorted(((r["scene"], r["target"]), int(r["slot"] == r["target"])) for r in rows
                      if r["reader"] == LOOKUP and r["arm"] == "random" and r["basis"] == bcol)  # fmt: skip
        assert [k for k, _ in mine] == [k for k, _ in keys], f"random {bcol}: the (item, target) set differs"
        v = [h for _, h in mine]
        rnd[bcol] = D.ci_of(v, ents, n_boot) if n_boot else [float(np.mean(v))] * 3
    reach = {bcol: ratio_ci(vals[(None, bcol)], vals[(None, "whole")], ents, n_boot) for bcol in BASES}
    cuts = {}
    for x in BASES:
        for bcol in BASES:
            if x == bcol:
                continue
            r = ratio_ci(vals[(x, bcol)], vals[(None, bcol)], ents, n_boot)
            cuts[f"{x}->{bcol}"] = [1 - r[0], 1 - r[2], 1 - r[1]]
    diag = {x: ratio_ci(vals[(x, x)], vals[(None, x)], ents, n_boot) for x in BASES}
    alone = {}
    for x in BASES:
        mine = [r for r in rows if r["reader"] == LOOKUP and r["arm"] == "remove" and r["removed"] == x]
        alone[x] = round(float(np.mean([r["slot"] != r["start"] for r in mine])), 4) if mine else None
    recall = {f"{x or 'none'}|{bcol}": round(float(np.mean([r["moved"] for r in rows if r["reader"] == RECALL and r["arm"] == "swap"
                                                              and r["removed"] == x and r["basis"] == bcol])), 4)
              for x in (None, *BASES) for bcol in ("whole", *BASES)}  # fmt: skip
    norms = {bcol: round(float(np.median([r["norm"] for r in rows if r["reader"] == LOOKUP and r["arm"] == "swap"
                                          and r["removed"] is None and r["basis"] == bcol])), 4) for bcol in ("whole", *BASES)}  # fmt: skip
    return {"n": len(keys), "items": len({k[0] for k, _ in keys}), "entities": len(set(ents)), "table": table, "random": rnd,
            "reach": reach, "cuts": cuts, "self_removal_left": diag, "removal_alone_moves": alone, "recall_moved": recall,
            "median_norm": norms}  # fmt: skip


def finite(x: float | None) -> bool:
    return x is not None and not math.isnan(x)


def part2_rule(reach: dict[str, float], cuts: dict[str, float]) -> dict[str, Any]:
    """Part 2's labels on point estimates: one code; partly overlapping; different; else in between. A reach or cut
    that is nan (nothing to divide by) satisfies no bar."""
    r_ok = all(finite(reach[b]) and reach[b] >= REACH - EPS for b in BASES)
    one = r_ok and all(finite(c) and c >= CUT_ONE - EPS for c in cuts.values())
    partly = r_ok and all(finite(c) and c < CUT_PARTLY - EPS for c in cuts.values())
    different = any(finite(reach[b]) and reach[b] < DIFFERENT - EPS for b in ("P", "R"))
    clauses = {"one_code": one, "partly": partly, "different": different}
    holding = [k for k in ("one_code", "partly", "different") if clauses[k]]
    label = holding[0] if holding else "in_between"
    return {"label": label, "text": P2_LABELS[label], "holding": holding, "clauses": clauses}


def part2_numbers(src: Path, n_boot: int) -> dict[str, Any]:
    m = json.loads((src / "manifest.json").read_text())
    out: dict[str, Any] = {"run": src.name, "target": m["model"]["target"], "layer": m["layer"], "S": {}}
    for n in P2_SLOTS:
        d = src / f"S{n}"
        if not (d / "swap_outcomes.jsonl").exists():
            out["S"][n] = {"status": json.loads((d / "p2_status.json").read_text()).get("why", "missing")
                           if (d / "p2_status.json").exists() else "missing"}  # fmt: skip
            continue
        rows = X.read_jsonl(d / "swap_outcomes.jsonl")
        cells = part2_cells(rows, n_boot)
        if not cells["table"]["none"]["whole"][0] > 0:
            rule = {
                "label": None,
                "text": "not interpretable: the whole swap sends no lookup to its target",
                "holding": [],
            }
        else:
            rule = part2_rule({b: v[0] for b, v in cells["reach"].items()}, {k: v[0] for k, v in cells["cuts"].items()})
        out["S"][n] = {"status": "tested", "cells": cells, "rule": rule,
                       "readouts": json.loads((d / "readouts.json").read_text())}  # fmt: skip
    main = out["S"].get(P2_MAIN, {})
    out["rule"] = main.get("rule") or {"label": None, "text": f"S = {P2_MAIN}: {main.get('status', 'missing')}"}
    return out


# ---- part 3 (GPU, then CPU) ---------------------------------------------------------------------------------------


def ends(n: int) -> dict[int, tuple[int, int]]:
    """Start slot -> its two far slots: from 1 toward 3 and 5; from n toward n - 2 and n - 4."""
    return {1: (3, 5), n: (n - 2, n - 4)}


def mid_class(slot: int | None, start: int, far: int) -> str:
    """The answered slot's class for a move start -> far: original, midpoint, far, near (start +- 1 toward far when it
    is not the midpoint), another slot, or not a slot."""
    if slot is None:
        return "not a slot"
    mid = (start + far) // 2
    step = 1 if far > start else -1
    return ("original" if slot == start else "midpoint" if slot == mid else "far" if slot == far
            else "near" if slot == start + step else "another slot")  # fmt: skip


def part3_arms(c: dict, n: int, mu) -> list[tuple[dict, Any]]:
    """From the bridge's slot s (1 or n): none; per far slot dose x (mu_far - mu_s) / 2 at each dose; the full swap
    2 (mu_far - mu_s); a random direction of each vector's norm."""
    s = c["move"][0]
    arms: list[tuple[dict, Any]] = [({"arm": "none", "far": None, "dose": None}, None)]
    for far in ends(n)[s]:
        half = (mu[far - 1] - mu[s - 1]) / 2
        vecs = [("mid", dose, dose * half) for dose in P3_DOSES] + [("full", SWAP_DOSE, SWAP_DOSE * 2 * half)]
        for kind, dose, v in vecs:
            arms.append(({"arm": kind, "far": far, "dose": dose}, v))
            arms.append(({"arm": f"{kind}_random", "far": far, "dose": dose},
                         rand_dir(f"p3|{c['scene']}|{far}|{kind}|{dose}", v.shape[0]) * v.norm()))  # fmt: skip
    return arms


def part3_run(model, out_s: Path, b: dict, layer: int, ws, digits, items: list[dict]) -> None:
    import torch

    from bridge_jspace.utils import progress

    n = int(b["status"]["slots"])
    mu = torch.tensor(b["fit"]["mu"], dtype=torch.float32)
    X.write_jsonl(out_s / "p3_items.jsonl", [{k: c[k] for k in ("scene", "bridge", "split", "move", "pos")} | {"ids": ids_digest(c)}
                                            for c in items])  # fmt: skip
    rows = []
    for c in progress(items, f"part 3 S = {n} (item)"):
        h_o, _ = Z.bridge_states(model, [c], layer, "")
        rows += read_arms(model, layer, c, part3_arms(c, n, mu), ws, digits, {"h_norm": round(float(h_o[0].norm()), 4)})
    for r in rows:
        if r["far"] is not None:
            r["class"] = mid_class(r["slot"], r["start"], r["far"])
    X.write_jsonl(out_s / "p3_outcomes.jsonl", rows)


def means_geometry(mu: np.ndarray) -> dict[str, Any]:
    """The slot means' geometry: pairwise distances, their mean by |i - j|, their spread (std / mean; a simplex: 0), the
    correlation of distance with |i - j|, x47_six.pca_reading (PC shares, PC1 per slot, Spearman with slot)."""
    n = len(mu)
    dist = np.linalg.norm(mu[:, None] - mu[None], axis=-1)
    iu = [(i, j) for i in range(n) for j in range(i + 1, n)]
    dv = np.array([dist[i, j] for i, j in iu])
    lag = np.array([j - i for i, j in iu])
    by_lag = {int(g): float(dv[lag == g].mean()) for g in sorted(set(lag))}
    return {"distances": np.round(dist, 4).tolist(), "by_lag": by_lag,
            "by_lag_over_lag1": {g: v / by_lag[1] for g, v in by_lag.items()}, "spread": float(dv.std() / dv.mean()),
            "corr_distance_lag": float(np.corrcoef(dv, lag)[0, 1]), "pca": SIX.pca_reading(mu)}  # fmt: skip


def part3_rule(mid: dict[int, float], full: float, n: int) -> dict[str, Any]:
    """Part 3's labels on point estimates (mid: the midpoint share per end, pooled over its two arms)."""
    a, z = mid[1], mid[n]
    clauses = {"metric": a >= MID_WORKS - EPS and z >= MID_WORKS - EPS,
               "categories": a < MID_NONE - EPS and z < MID_NONE - EPS and full >= FULL_REACH - EPS,
               "first_rest": a >= MID_WORKS - EPS and z < MID_WORKS - EPS}  # fmt: skip
    holding = [k for k in ("metric", "categories", "first_rest") if clauses[k]]
    label = holding[0] if holding else "none"
    return {"label": label, "text": P3_LABELS[label], "holding": holding, "clauses": clauses}


def part3_numbers(src: Path, p1: Path | None, n_boot: int) -> dict[str, Any]:
    m = json.loads((src / "manifest.json").read_text())
    out: dict[str, Any] = {"run": src.name, "target": m["model"]["target"], "layer": m["layer"]}
    d = src / f"S{P3_S}"
    rows = X.read_jsonl(d / "p3_outcomes.jsonl")
    lk = [r for r in rows if r["reader"] == LOOKUP]
    n = P3_S
    cells: dict[str, Any] = {}
    for start in (1, n):
        for kind in ("mid", "mid_random", "full", "full_random"):
            for dose in sorted({r["dose"] for r in lk if r["arm"] == kind}):
                mine = [r for r in lk if r["arm"] == kind and r["dose"] == dose and r["start"] == start]
                if not mine:
                    continue
                ent = [r["entity"] for r in mine]
                cl = ("original", "midpoint", "far", "near", "another slot", "not a slot")
                cells[f"{start}|{kind}|{dose}"] = {"start": start, "arm": kind, "dose": dose, "n": len(mine),
                                                   **{c: (D.ci_of([int(r["class"] == c) for r in mine], ent, n_boot) if n_boot
                                                          else [float(np.mean([r["class"] == c for r in mine]))] * 3) for c in cl},
                                                   "median_norm": round(float(np.median([r["norm"] for r in mine])), 4)}  # fmt: skip
    none = {start: round(float(np.mean([r["slot"] == start for r in lk if r["arm"] == "none" and r["start"] == start])), 4)
            for start in (1, n)}  # fmt: skip
    rules = {}
    for dose in P3_DOSES:
        mid = {s: cells[f"{s}|mid|{dose}"]["midpoint"][0] for s in (1, n)}
        full = float(np.mean([r["class"] == "far" for r in lk if r["arm"] == "full"]))
        rules[dose] = {**part3_rule(mid, full, n), "mid": mid, "full_far": full}
    st = json.loads((d / "p3_status.json").read_text())
    out.update({"cells": cells, "none_original": none, "rules": rules, "rule": rules[P3_DECISIVE], "status": st,
                "h_norm_median": round(float(np.median([r["h_norm"] for r in lk])), 4)})  # fmt: skip
    means = {}
    for s_, path in ((6, (p1 or src) / "S6" / "fit.npz"), (8, (p1 / "S8" / "fit.npz") if p1 else None)):
        if path is not None and path.exists():
            means[s_] = means_geometry(np.load(path)["mu"].astype(np.float64))
    out["means"] = means
    return out


# ---- part 4 ---------------------------------------------------------------------------------------------------------


def wording(l1: str | None, l2: str | None, l3: str | None) -> dict[str, Any]:
    """The first row of the addendum's table whose parts match (None in a row = any; a part the model lacks or could
    not decide matches only 'any')."""
    for k, (r1, r2, r3, text) in enumerate(WORDING, 1):
        if (r1 is None or r1 == l1) and r2 == l2 and (r3 is None or r3 == l3):
            return {"row": k, "text": text, "note": FOUR_NOTE}
    return {"row": None, "text": "no row of the wording table matches these labels; the wording is not fixed by the "
            "addendum", "note": FOUR_NOTE}  # fmt: skip


# ---- the run (GPU) --------------------------------------------------------------------------------------------------


def stage_run(name: str, part: int, why: str, part1: str | None = None, slots: tuple[int, ...] | None = None,
              steps: int = D.STEPS, micro: int = D.MICRO) -> Path:  # fmt: skip
    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    slots = SLOTS if slots is None else slots
    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.11 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"51.11 does not run on {target}"
    assert part in RUNS[target], f"51.11 part {part} does not run on {target} ({RUNS[target]})"
    layer = X.PREDICTED[target]
    src1 = RESULTS / part1 if part1 else None
    if src1 is not None:
        m1 = json.loads((src1 / "manifest.json").read_text())
        assert m1["part"] == 1, f"{part1}: not a part 1 run"
        assert m1["model"]["target"] == target, f"{part1}: a {m1['model']['target']} run"
        assert m1["layer"] == layer, f"{part1}: layer {m1['layer']}, not {layer}"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    files = [SPEC]
    if src1 is not None:
        files += sorted(p for p in src1.glob("S*/*") if p.suffix in (".npz", ".json", ".jsonl"))
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "part": part, "test": "51.11", "spec": "jobs/c3/batch51.yaml (addendum_3, 51.11)",
        "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer,
        "read": "X0's chat read (the top token after a digit's space token appended to O); edits added at the bridge word at L",
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in files}, "part1": part1,
        "slots": list(slots) if part == 1 else (list(P2_SLOTS) if part == 2 else [P3_S]), "ks": list(KS),
        "pairs": {"target": POS_TARGET, "min": POS_MIN, "cap_per_ordered_pair": CAP, "chunk": CHUNK},
        "training": {"method": "x51_das.train_fit (48.1's loop, early stopping on the select split's IIA every "
                               f"{Z.EVAL_EVERY} steps, patience {Z.PATIENCE}, micro-batch halved on CUDA OOM)",
                     "lr": D.LR, "max_steps": steps, "batch": D.BATCH, "micro_batch": micro,
                     "target": "O's digit at slot j (the position answer) at the read position of O"},
        "bars": {"own_iia": OWN_BAR, "random": RAND_BAR, "reach": REACH, "cut_one_code": CUT_ONE, "cut_partly": CUT_PARTLY,
                 "different": DIFFERENT, "midpoint_works": MID_WORKS, "midpoint_none": MID_NONE, "full_reach": FULL_REACH},
        "doses": {"swap": SWAP_DOSE, "midpoint": list(P3_DOSES), "midpoint_decisive": P3_DECISIVE},
        "seeds": {"scenes": SEED, "split": D.SPLIT_SEED, "init": f"{INIT_SEED} + 100 k (shuffled + 10)",
                  "shuffle": f"{SHUFFLE_SEED} + k", "random_R": f"{RAND_SEED} + k", "batches": f"{D.BATCH_SEED} + the R's seed",
                  "random_directions": DIR_SEED, "random_subspaces": GEO_SEED, "bootstrap": X.BOOT_SEED,
                  "examples": X.EXAMPLES_SEED},
        "n_boot": X.N_BOOT, "as_computed": "see scripts/x51_addr.py's docstring (repeated in the job specs)",
        "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer",
    }  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    import torch

    R.warm_cusolver()
    model = load_model()
    if (patched := D.torch_gdn(model.hf)) is not None:
        m["gdn_kernel"] = f"torch reference ({D.GDN_ENV}=torch; {patched}.torch_chunk_gated_delta_rule replaced)"
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    for p in model.hf.parameters():  # the DAS gradient reaches R only
        p.requires_grad_(False)
    tok = model.tokenizer
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    split = entity_split(tok)
    m["entity_split"] = dict(collections.Counter(split.values()))
    failed: dict[str, str] = {}

    def bundle(n: int, train: bool, shuffled: bool) -> dict[str, Any]:
        """S = n from part 1 (loaded) or built here into out/S{n}."""
        if src1 is not None:
            return load_bundle(src1 / f"S{n}")
        build_s(model, tok, out / f"S{n}", n, layer, ws, digits, split, train, shuffled, steps, micro)
        return load_bundle(out / f"S{n}")

    if part == 1:
        for n in slots:
            try:
                build_s(model, tok, out / f"S{n}", n, layer, ws, digits, split, True, True, steps, micro)
            except Exception as e:  # one S failing (e.g. OOM at S = 8) keeps the others; the job still fails at the end
                failed[str(n)] = f"{type(e).__name__}: {e}"
                print(f"S = {n} failed: {failed[str(n)]}", flush=True)
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
    elif part == 2:
        for n in P2_SLOTS if src1 is not None else (P2_MAIN,):  # the 27B (no part 1): S = 6 only, built here
            out_s = out / f"S{n}"
            try:
                b = bundle(n, True, False)
            except AssertionError as e:
                if n == P2_MAIN:
                    raise
                out_s.mkdir(exist_ok=True)
                (out_s / "p2_status.json").write_text(json.dumps({"why": f"part 1's S = {n} not usable: {e}"}) + "\n")
                continue
            out_s.mkdir(exist_ok=True)
            if not b["tested"]:
                (out_s / "p2_status.json").write_text(json.dumps({"why": f"S = {n} not tested (gate)"}) + "\n")
                assert n != P2_MAIN, f"S = {P2_MAIN} missed the gate: part 2 not tested"
                continue
            cases, _, _ = candidates(tok, n)
            for c in cases:
                c["split"] = split[c["bridge"]]
            items, info = pick_items(model, cases, {s: P2_PER_START[n] for s in range(1, n + 1)}, ("test",), ws, digits,
                                     f"part 2 S = {n}: items (start slot)")  # fmt: skip
            res = part2_one(model, out_s, n, b, layer, ws, digits, items)
            (out_s / "p2_status.json").write_text(json.dumps({"items": info, **res}, indent=1) + "\n")
    else:
        n = P3_S
        b = bundle(n, False, False)
        assert b["tested"], f"S = {n} missed the gate: part 3 not tested"
        out_s = out / f"S{n}"
        out_s.mkdir(exist_ok=True)
        cases, _, _ = candidates(tok, n)
        for c in cases:
            c["split"] = split[c["bridge"]]
        items, info = pick_items(model, cases, {1: P3_N, n: P3_N}, SPLITS_HELD, ws, digits, "part 3: items (end)")
        part3_run(model, out_s, b, layer, ws, digits, items)
        (out_s / "p3_status.json").write_text(json.dumps({"items": info, "unit": float(b["fit"]["unit"]),
                                                          "mu_from": str(b["dir"].relative_to(pins.REPO_ROOT))}, indent=1) + "\n")  # fmt: skip
    m["failed_slots"] = failed
    m["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    if failed:
        raise SystemExit(f"part {part}: S = {sorted(failed)} failed ({failed}); the other S folders are complete")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict and view (CPU, sealed) ---------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed Q51.11 answer (x48_das.dan_answer: the 'Dan:' / 'Dan (27B):' lines and bullet continuations of
    the Q51.11 block at `rev`), '' if none."""
    return D.dan_answer(QUESTION, rev)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def model_verdict(target: str, n_boot: int) -> dict[str, Any]:
    runs = RUNS[target]
    have = {p: RESULTS / r for p, r in runs.items() if (RESULTS / r / "manifest.json").exists()}
    v: dict[str, Any] = {"target": target, "runs": runs, "present": {p: s.name for p, s in have.items()}}
    p1 = have.get(1)
    v["part1"] = part1_numbers(p1, n_boot) if p1 else None
    v["part2"] = part2_numbers(have[2], n_boot) if 2 in have else None
    v["part3"] = (part3_numbers(have[3], p1, n_boot) if 3 in have and (have[3] / f"S{P3_S}" / "p3_outcomes.jsonl").exists()
                  else None)  # fmt: skip
    lab = {k: (v[f"part{k}"] or {}).get("rule", {}).get("label") if v[f"part{k}"] else None for k in (1, 2, 3)}
    v["labels"] = lab
    v["lacks"] = [k for k in (1, 2, 3) if k not in runs]
    v["wording"] = wording(lab[1], lab[2], lab[3])
    return v


def fmt(v: list | None) -> str:
    return D.fmt(v) if v is not None else "-"


def verdict_lines(v: dict[str, Any]) -> list[str]:
    lacks = (f" The design gives this model no part {', '.join(map(str, v['lacks']))}: those labels read 'lacks the part'."
             if v["lacks"] else "")  # fmt: skip
    lines = [f"## {v['target']}", "", f"Runs: {v['runs']}; present here: {v['present']}.{lacks}", ""]
    p1 = v["part1"]
    if p1:
        lines += [f"### Part 1: dimension vs the number of slots ({p1['run']}, L{p1['layer']})", "",
                  f"**{p1['rule']['text']}** (holding: {', '.join(p1['rule']['holding']) or 'none'}; d* not found at S = "
                  f"{p1['rule'].get('not_found') or 'none'})", "",
                  "| S | status | pairs (train / select / test) | ordered pairs covered | test n (entities) | whole | U (rank S-1) | "
                  "d*(S) | d* without the random bar | k blocked by random > 0.15 | d* through P |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for n in RULE_SLOTS:
            s = p1["S"][n]
            if s["status"] != "tested":
                lines.append(f"| {n} | {s['status']} {s.get('why') or ''} | | | | | | | | | |")
                continue
            c, pi = s["curve"], s["pairs"]
            lines.append(f"| {n} | tested | {pi['pairs']} ({pi['pairs_per_split']}) | {pi['ordered_pairs_covered']} / "
                         f"{pi['ordered_pairs']} | {c['n']} ({c['entities']}) | {fmt(c['whole'])} | {fmt(c['U'])} | "
                         f"{s['d_star']['d_star'] or '> ' + str(max(KS))} | {s['d_star']['own_only'] or '-'} | "
                         f"{s['d_star']['random_blocked'] or '-'} | {s['d_star_P']['d_star'] or '> ' + str(max(KS))} |")  # fmt: skip
        lines += ["", "Own-IIA on the test pairs by k (R; P's top k; the random R; the shuffled-target R):", "",
                  "| S | arm | " + " | ".join(f"k = {k}" for k in KS) + " |", "|---|---|" + "---|" * len(KS)]  # fmt: skip
        for n in RULE_SLOTS:
            s = p1["S"][n]
            if s["status"] != "tested":
                continue
            for key in ("R", "P", "rand", "shuf"):
                if key in s["curve"]:
                    lines.append(f"| {n} | {key} | " + " | ".join(fmt(s["curve"][key][k]) for k in KS) + " |")
        lines += ["", "Dumbest ways (verify pack): per S the locker-sentence layout (tokens per sentence, slot starts), the "
                  "ordered pairs with no position pair, the whole change's routes among eligible scenes; every pair's "
                  "answer digit is asserted equal in O and S at build; d* is read on the test entities only; the random "
                  "bar is per k (the rand rows above)."]  # fmt: skip
        for n in RULE_SLOTS:
            s = p1["S"][n]
            if s["status"] == "tested":
                pi = s["pairs"]
                lines.append(f"- S = {n}: layout {pi['layout']}; missing ordered pairs {pi['missing_ordered_pairs'] or 'none'}; "
                             f"routes {pi['whole_change_routes']} (position share {pi['position_share_of_eligible']}); gate "
                             f"{pi['gate']['org_read_accuracy']}")  # fmt: skip
        lines.append("")
    p2 = v["part2"]
    if p2:
        lines += [f"### Part 2: do three methods find the same code? ({p2['run']}, L{p2['layer']})", "",
                  f"**S = {P2_MAIN}: {p2['rule']['text']}**", ""]  # fmt: skip
        for n, s in p2["S"].items():
            if s.get("status") != "tested":
                lines += [f"S = {n}: {s.get('status')}", ""]
                continue
            c, w = s["cells"], s["readouts"]["working"]
            lines += [f"S = {n}{' (decisive)' if n == P2_MAIN else ' (beside)'}: {c['n']} (item, target) reads on {c['items']} "
                      f"items ({c['entities']} entities); bases U rank {n - 1}, P and R at k = {w['k']} "
                      f"({w['flag'] or 'd* = ' + str(w['d_star']['d_star'])}); label {s['rule']['text']}", "",
                      "| removed \\ swap through | whole | U | P | R |", "|---|---|---|---|---|"]  # fmt: skip
            for x, row in c["table"].items():
                lines.append(f"| {x} | " + " | ".join(fmt(row[b]) for b in ("whole", *BASES)) + " |")
            lines.append(
                "| random direction (same norm) | " + " | ".join(fmt(c["random"][b]) for b in ("whole", *BASES)) + " |"
            )
            lines += ["", "reach (projected / whole): " + "; ".join(f"{b} {fmt(r)}" for b, r in c["reach"].items())
                      + ". Cuts (1 - removed / not): " + "; ".join(f"{k} {fmt(r)}" for k, r in c["cuts"].items())
                      + ". Self-removal left: " + "; ".join(f"{k} {fmt(r)}" for k, r in c["self_removal_left"].items())
                      + f". Removal alone moves the lookup off its slot: {c['removal_alone_moves']}. Median swap norms "
                      f"{c['median_norm']}. The recall moved per cell: {c['recall_moved']}.", "",
                      "Geometry (mean cos² of the principal angles; random: max rank / d and the mean of "
                      f"{N_RANDOM_SUBSPACES} seeded pairs): " + "; ".join(
                          f"{k} {g['mean_cos2']:.3f} (random {g['random_expectation']:.4f} / {g['random_mean']:.4f})"
                          for k, g in s["readouts"]["geometry"].items() if isinstance(g, dict) and "mean_cos2" in g), ""]  # fmt: skip
    p3 = v["part3"]
    if p3:
        r2 = p3["rule"]
        lines += [f"### Part 3: categories, an order or a line? ({p3['run']}, L{p3['layer']}, S = {P3_S})", "",
                  f"**{r2['text']}** at dose {P3_DECISIVE} (midpoint share from slot 1 {r2['mid'][1]:.2f}, from slot "
                  f"{P3_S} {r2['mid'][P3_S]:.2f}; full swaps at their target {r2['full_far']:.2f}); at dose 4: "
                  f"{p3['rules'][4]['text']} (from 1 {p3['rules'][4]['mid'][1]:.2f}, from {P3_S} {p3['rules'][4]['mid'][P3_S]:.2f})"
                  + (" - the label differs with the dose (a dose effect)" if p3["rules"][4]["label"] != r2["label"] else ""), "",
                  f"Unedited O answers its own slot: {p3['none_original']}. Real change size (median ||U U^T Δ||, test pairs) "
                  f"{p3['status'].get('unit'):.3f}; median ||h_O|| {p3['h_norm_median']:.1f}. Items {p3['status'].get('items')}.", "",
                  "| start | arm | dose | n | median norm | original | midpoint | far | near | another slot | not a slot |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for c in p3["cells"].values():
            lines.append(f"| {c['start']} | {c['arm']} | {c['dose']} | {c['n']} | {c['median_norm']} | " + " | ".join(
                fmt(c[k]) for k in ("original", "midpoint", "far", "near", "another slot", "not a slot")) + " |")  # fmt: skip
        for s_, g in p3["means"].items():
            lines += ["", f"Slot means at S = {s_}: mean distance by |i - j| {', '.join(f'{k}: {x:.2f}' for k, x in g['by_lag'].items())} "
                      f"(over lag 1: {', '.join(f'{k}: {x:.2f}' for k, x in g['by_lag_over_lag1'].items())}); spread (std / mean; "
                      f"a simplex 0) {g['spread']:.3f}; corr(distance, |i - j|) {g['corr_distance_lag']:.3f}; PC shares "
                      f"{[round(x, 3) for x in g['pca']['shares'][:3]]}, PC1 per slot {[round(x, 2) for x in g['pca']['pc1']]}, "
                      f"Spearman {g['pca']['spearman_pc1_slot']:.2f}"]  # fmt: skip
        lines.append("")
    w = v["wording"]
    ds = (p1 or {}).get("d_star", {})
    lines += ["### Part 4: the finding's wording", "",
              f"Labels: part 1 {v['labels'][1] or 'lacks the part / not decided'}, part 2 {v['labels'][2] or 'lacks the part / not decided'}, "
              f"part 3 {v['labels'][3] or 'lacks the part / not decided'}. Row {w['row'] or '-'}: {w['text']}"
              + (f" (k for S slots, d*(S): {ds})" if w["row"] == 3 else ""), "", w["note"], ""]  # fmt: skip
    return lines


def figure_part1(p1: dict[str, Any], path: Path) -> None:
    """Own-IIA vs k on the test pairs, one curve per S, its random R dashed, the 0.80 bar."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    fig, ax = plt.subplots(figsize=(6, 4))
    cols = {3: "#1f4e79", 4: "#4f81bd", 6: "#c0504d", 8: "#7f6000"}
    for n in RULE_SLOTS:
        s = p1["S"][n]
        if s["status"] != "tested":
            continue
        ax.plot(
            KS,
            [s["curve"]["R"][k][0] for k in KS],
            "o-",
            color=cols[n],
            label=f"S = {n} (d* {s['d_star']['d_star'] or '>7'})",
        )
        ax.plot(KS, [s["curve"]["rand"][k][0] for k in KS], "--", color=cols[n], lw=0.8)
    ax.axhline(OWN_BAR, color=MUTED, ls=":", lw=0.8)
    ax.axhline(RAND_BAR, color=MUTED, ls=":", lw=0.6)
    ax.set_xticks(KS)
    ax.set_xlabel("k (DAS subspace dimension)")
    ax.set_ylim(0, 1)
    percent_axis(ax)
    style_axes(ax)
    ax.legend(fontsize=7, frameon=False)
    ax.set_title(
        f"51.11 part 1, {p1['target']} L{p1['layer']}: own-IIA on held-out entities (random R dashed)", fontsize=9
    )
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def figure_part3(p3: dict[str, Any], mu: np.ndarray, path: Path) -> None:
    """The slot means in their first two PCs; the midpoint swaps (dose 2) as arrows from the start slot toward the
    vector's end, labelled with the share answering the midpoint / far / original slot."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, style_axes

    c = mu - mu.mean(0)
    _, _, vt = np.linalg.svd(c, full_matrices=False)
    xy = c @ vt[:2].T
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(xy[:, 0], xy[:, 1], "o-", color=INK, lw=0.6)
    for k, (x, y) in enumerate(xy, 1):
        ax.annotate(f"slot {k}", (x, y), fontsize=8, xytext=(3, 3), textcoords="offset points")
    for start, fars in ends(len(mu)).items():
        for far in fars:
            end = xy[start - 1] + (xy[far - 1] - xy[start - 1]) * P3_DECISIVE / 2
            ax.annotate("", xy=end, xytext=xy[start - 1], arrowprops={"arrowstyle": "->", "color": "#c0504d"})
            cl = p3["cells"].get(f"{start}|mid|{P3_DECISIVE}")
            if cl:
                ax.annotate(f"{start}->{far}/2: mid {cl['midpoint'][0]:.2f} far {cl['far'][0]:.2f} orig {cl['original'][0]:.2f}",
                            end, fontsize=6.5, color="#c0504d")  # fmt: skip
    style_axes(ax)
    ax.set_title(f"51.11 part 3, {p3['target']}: slot means (PC1-2), midpoint swaps at dose {P3_DECISIVE} (shares pooled per end)",
                 fontsize=8)  # fmt: skip
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(targets: list[str] | None = None, n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    targets = targets or list(RUNS)
    out = RESULTS / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.11: what is the address, independent of how we built it?", "",
             f"Batch 51 addendum 3 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). Every number on held-out entities "
             f"(test split; part 3: select and test); cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", "As computed: scripts/x51_addr.py's docstring (repeated in the job specs).", ""]  # fmt: skip
    models = []
    for t in targets:
        v = model_verdict(t, n_boot)
        models.append(v)
        lines += verdict_lines(v)
        if v["part1"]:
            figure_part1(v["part1"], out / f"{t}_part1.png")
            lines += [f"Figure: {t}_part1.png", ""]
        if v["part3"]:
            src = (RESULTS / v["present"][1]) if 1 in v["present"] else RESULTS / v["present"][3]
            figure_part3(
                v["part3"], np.load(src / f"S{P3_S}" / "fit.npz")["mu"].astype(np.float64), out / f"{t}_part3.png"
            )
            lines += [f"Figure: {t}_part3.png", ""]
    (out / "verdict.json").write_text(json.dumps({"dan": answer, "models": models}, indent=1, default=str) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


class Decoder:
    """A tokenizers.Tokenizer seen through .decode(ids) with the special tokens kept (as the model reads them)."""

    def __init__(self, tk) -> None:
        self.tk = tk

    def decode(self, ids: list[int]) -> str:
        return self.tk.decode([int(t) for t in ids], skip_special_tokens=False)


def view_lines(src: Path, k_prompts: int = 5, k_rows: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED,
               tk=None) -> list[str]:  # fmt: skip
    """One run's verify pack: k_prompts random pairs / items (seed 0) as the model reads them, and k_rows random rows
    per arm (seed 0) of every outcomes file. tk: anything with .decode(ids) (default: the target's pinned tokenizer)."""
    m = json.loads((src / "manifest.json").read_text())
    if tk is None:
        from bridge_jspace.review import checks as RC

        tk = Decoder(RC.tokenizer(m["model"]["target"]))
    lines = [f"## {src.name} (part {m['part']}, {m['model']['target']}, L{m['layer']})", ""]
    for d in sorted(p for p in src.iterdir() if p.is_dir() and p.name.startswith("S")):
        if (d / "cases.jsonl").exists():
            pairs = X.read_jsonl(d / "cases.jsonl")
            pick = sorted(random.Random(seed).sample(range(len(pairs)), min(k_prompts, len(pairs))))
            lines += [f"### {d.name}: {len(pick)} random pairs of {len(pairs)} (seed {seed})", ""]
            for i in pick:
                p = pairs[i]
                lk = p["readers"][LOOKUP]
                so, ss = SIX.sentences(p["context"]), SIX.sentences(p["cf_context"])
                o = Q.marked(
                    tk,
                    lk["ids"]["org"],
                    p["pos"],
                    p["space"],
                    {"own": so[p["slot_o"] - 1], "target": so[p["slot_s"] - 1]},
                )
                s = Q.marked(tk, lk["ids"]["alt"], p["pos"], p["space"], {"moved": ss[p["slot_s"] - 1]})
                lines += [f"#### {p['scene']} ({p['split']}): {p['move']}; O and S answer {lk['answer']}, the position answer "
                          f"{lk['cf_answer']}", "", "O:", "", "```", o, "```", "", "S:", "", "```", s, "```", ""]  # fmt: skip
        for name in ("outcomes.jsonl", "swap_outcomes.jsonl", "p3_outcomes.jsonl"):
            if not (d / name).exists():
                continue
            rows = X.read_jsonl(d / name)
            for a in dict.fromkeys(r["arm"] for r in rows):
                mine = [r for r in rows if r["arm"] == a]
                pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
                lines += [f"### {d.name} {name}, arm {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                          "| scene | split | reader | detail | top token | switched / slot | moved |", "|---|---|---|---|---|---|---|"]  # fmt: skip
                for j in pick:
                    r = mine[j]
                    det = {
                        k: r[k]
                        for k in ("removed", "basis", "target", "far", "dose", "class", "norm")
                        if r.get(k) is not None
                    }
                    hit = r.get("switched", r.get("slot"))
                    lines.append(f"| {r['scene']} | {r['split']} | {READER_NAME[r['reader']]} | {det} | {r['top_text']!r} | "
                                 f"{hit} | {r['moved']} |")  # fmt: skip
                lines.append("")
    return lines


def stage_view(targets: list[str] | None = None, tk=None) -> Path:
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.11 verify pack: pairs exactly as the model reads them (⟦bridge:…⟧ the bridge word where every edit is "
             "added at L; ⟦own:…⟧ / ⟦target:…⟧ / ⟦moved:…⟧ the swapped locker sentences) and random rows per arm. "
             "UNVERIFIED.", ""]  # fmt: skip
    for t in targets or list(RUNS):
        for r in RUNS[t].values():
            if (RESULTS / r / "manifest.json").exists():
                lines += view_lines(RESULTS / r, tk=tk)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--part", type=int, choices=[1, 2, 3])
    ap.add_argument("--name", help="run: the run name (results/x51_addr/<name>/)")
    ap.add_argument("--part1", default=None, help="run --part 2 / 3: the model's part 1 run (its S folders are read)")
    ap.add_argument(
        "--slots", type=int, nargs="+", default=None, help=f"run --part 1: the S values, in order ({SLOTS})"
    )
    ap.add_argument("--out", type=Path, default=None, help="plan: write plan.md and <target>.json here")
    ap.add_argument(
        "--targets", nargs="+", default=None, help="verdict / view: the targets (default: every one in RUNS)"
    )
    ap.add_argument("--why", default="batch 51, test 51.11 (jobs/c3/batch51.yaml addendum_3; Q51.11)")
    ap.add_argument("--steps", type=int, default=D.STEPS)
    ap.add_argument("--micro", type=int, default=D.MICRO)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.out)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        assert a.part, "run needs --part"
        stage_run(a.name, a.part, a.why, a.part1, tuple(a.slots) if a.slots else None, a.steps, a.micro)
    elif a.stage == "verdict":
        stage_verdict(a.targets, a.n_boot)
    else:
        stage_view(a.targets)


if __name__ == "__main__":
    main()
