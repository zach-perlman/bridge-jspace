"""x47_cue (batch 47, test 47.3, the old 45h; jobs/c3/batch47.yaml, design and rule fixed in advance; Q47.3 in
predictions/2026-10-28_dan.md): a computed bridge. The routes test (x6_routes, condition C2) with the asked pick stated
as a description instead of the name: "Iris picked the one known for honey." The bridge must be recalled from the cue.

Cues. One word per animal, the last word of the pick sentence and one token on the model's tokenizer. Third-person
sound verbs ("croaks", "barks", "quacks") are two or more tokens on both tokenizers, so every cue sits in one frame,
FRAME = "<person> picked the one known for <cue>.": per animal an ordered list of candidates (CUES, a sound or behaviour
first where one exists), and the animal's cue on a model is its first candidate that is one token there; an animal
with none, or not one token itself, is dropped (counted in cues.json). No cue names an animal, a slot, a number or a
class that fixes the leg count ("bird", "insect"); every candidate word belongs to one animal.

Competence step (in the job, recorded): per cue CUE_PEOPLE x len(CUE_TEMPLATES) = 10 unedited prompts that ask which
animal "the one known for <cue>" is (one word, chat, 8 greedy tokens); a cue is kept if the model names its animal in
at least 0.90 of them. The scenes use the kept animals only; a model left with fewer than 3, or with one leg count, is
"not tested (cue competence)".

Scenes (C2 of x6_routes, animals, seed 2510): three items A, B, C, their locker sentences first ("The locker of the frog
is 5.", stated by name), then three pick sentences; the asked person's is the FRAME with A's cue, the two others name
B and C. O: as drawn. S: the asked pick is B's cue, and B's and C's locker sentences trade places with B's digit -> e
(new). The cue is one token at the same index in O and S (else dropped and counted). The change h_S - h_O is added at
the cue token at the layer fixed in advance (27B 32, 9B 12, Muse 26), on O. Readers: lookup "Which locker belongs to
<p>'s pick?" (routes: identity b, position c, value e, original a, other) and recall "How many legs does <p>'s pick
have?" (switch: S's answer, B's legs). X0's chat read (the top token after the digit's space).

Gate 0.80 per reader (O's read accuracy over every generated scene), never lowered: a failed gate is "not tested".
Eligible: both readers say and read O's and S's answers right; the first N_ITEMS in scene order.

Arms at the cue token: whole; without J++ (signed OMP, k = 25, letter-token J++ atoms at L) / without a random part of
its share (X0's random subspace, seed 888 + L); without U (x0_massmean's Alf from the model's x0_probe_v4 run, not
refit) / its random part; without U' (P_cf refit here, x7_pcf's method: the centered rank-4 PCA of the cue token's
difference over pairs where A's locker sentence trades places with B's or C's, digits kept, built from the fit half of
the generated scenes; seed 0, by scene) / its random part. Rule (c) reads U' on the chosen scenes of the other half.
Beside them (descriptive): the elimination check (O with A's cue swapped for the cue of a kept animal not in the scene:
does the lookup still answer A's locker, i.e. find A as the one item nobody else picked?).

SEALED: the run writes per-item outputs only (cues and their competence prompts, cases, competence, the gate, the fit
pairs and P_cf, outcomes, norms, the elimination reads); no verdict. `verdict` refuses until predictions/2026-10-28_dan.md
holds Dan's Q47.3 answer at HEAD; it applies the rule (RULE, AS_COMPUTED) and writes the verify-pack view (10 random
scenes, seed 0, each reader's prompt as the model reads it with the cue token marked, every arm's answer).

uv run python scripts/x47_cue.py plan                                         # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_cue.py run --name qwen35_9b_x47_cue   # GPU, sealed
uv run python scripts/x47_cue.py verdict --runs x47_cue_27b qwen35_9b_x47_cue muse30_x47_cue   # CPU, after Q47.3
uv run python scripts/x47_cue.py view --runs x47_cue_27b                      # CPU, the view alone (sealed too)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x7_pcf as PC

EXP = "x47_cue"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.3"
RUNS = {"qwen3.6-27b": "x47_cue_27b", "qwen3.5-9b": "qwen35_9b_x47_cue", "muse-glimmer-30b": "muse30_x47_cue"}

FRAME = "{p} picked the one known for {cue}."
# per animal, the cue candidates in order of preference (a sound or behaviour first where one exists); the first that
# is one token on the model's tokenizer is the animal's cue. Words unique across animals (asserted); none names an
# animal, a slot, a number or a class that fixes the leg count. Animals of the domain left out: no one-word cue that
# names them alone (bear, beetle, butterfly, camel, crow, deer, duck, fly, goose, tiger: "stripes" is the zebra's).
CUES: dict[str, tuple[str, ...]] = {
    "ant": ("colonies",), "bee": ("honey",), "cat": ("purring", "curiosity"), "chicken": ("clucking", "eggs"),
    "cow": ("mooing", "milk"), "dog": ("barking", "loyalty"), "eagle": ("soaring",),
    "elephant": ("trumpeting", "ivory", "memory"), "fox": ("cunning",), "frog": ("croaking", "ponds"),
    "goat": ("bleating", "climbing"), "horse": ("neighing", "galloping", "racing"), "lion": ("roaring", "mane"),
    "mouse": ("squeaking", "cheese"), "owl": ("hooting", "wisdom"), "pig": ("oinking", "bacon"),
    "rabbit": ("hopping", "carrots"), "sheep": ("wool",), "spider": ("webs",), "tick": ("Lyme",),
    "turkey": ("gobbling", "Thanksgiving"), "wolf": ("howling", "packs"), "zebra": ("stripes",),
}  # fmt: skip
# the competence prompts: (statement, question) with the person p and the cue; one-word answer (S.INSTRUCTION)
CUE_TEMPLATES = (
    ("{p} picked the one known for {cue}.", "Which animal did {p} pick?"),
    ("{p} picked the one known for {cue}.", "What animal is {p}'s pick?"),
    ("{p} picked the one known for {cue}.", "Name the animal {p} picked."),
    ("{p} chose the one known for {cue}.", "Which animal did {p} choose?"),
    ("{p}'s pick is the one known for {cue}.", "Which animal is it?"),
)
CUE_PEOPLE, CUE_BAR, CUE_SEED, CUE_MIN = 2, 0.90, 4703, 3
# words the pick sentence must not hold: anything about slots, order or numbers (the description must not leak the
# position)
SLOT_WORDS = frozenset(
    {
        "first",
        "second",
        "third",
        "fourth",
        "last",
        "next",
        "previous",
        "before",
        "after",
        "slot",
        "slots",
        "position",
        "locker",
        "lockers",
        "number",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "zero",
    }
)  # fmt: skip ("one" is the frame's "the one")
SEED, N_GEN, N_ITEMS = R.SEED, 700, 300  # the routes generator's seed and sizes (C2 only)
SPLIT_SEED, RANK, DECOY_SEED = 0, PC.RANK, 4704
GATE = 0.80  # fixed in advance (batch 47's common settings): never lowered
ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "no_pcf", "no_pcf_rand")
PART_ARMS = {"jpp": ("no_jpp", "no_jpp_rand"), "alf": ("no_alf", "no_alf_rand"), "pcf": ("no_pcf", "no_pcf_rand")}
FOLLOW = ("identity", "position", "value")  # the lookup follows the change (its "switch" in the extra loss)
GAP_MIN, LOOKUP_MAX, THROUGH_MIN, VALUE_MAX, PCF_CUT = 0.3, 0.10, 0.20, 0.05, 0.30
EPS = 1e-9  # a value exactly at a bar counts as at the bar
N_VIEW, VIEW_SEED = 10, 0
# the elimination read's top token in O's terms (it is classified with the scene's route tokens)
DECOY_CLASS = {"original": "A's locker (found by elimination)", "identity": "B's locker", "position": "C's locker",
               "value": "S's new digit", "other": "other"}  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
RULE = ("(a) \"the split holds for a recalled bridge\": gap >= 0.3 and lookup extra loss <= 0.10; (a') \"a recalled "
        "bridge is handed through the lens\": lookup extra loss >= 0.20 (then the lens's rule, \"flexible computation "
        "routes through the J-space\", holds here and not for stated bridges; report it as the more interesting "
        "outcome, not as a failure); (b) \"never the value\": value <= 0.05; (c) \"a pointer at the cue token\": U' "
        "removal cuts position answers >= 0.30 beyond random. Report Zach's M->P numbers beside (toy suite: 12 / -2 / "
        "0).")  # fmt: skip
AS_COMPUTED = (
    "Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole over the chosen scenes (J++: signed "
    "OMP, k = 25). Recall switch: the top token is S's answer (B's legs). Lookup switch: the lookup follows the change, "
    "its answer is identity (b), position (c) or value (e). S's own answer is the value, which the routes test has never "
    "seen the lookup give; the main test's switch (identity and position coincide there) is the closest reading of the "
    "rule's 'lookup extra loss'. gap = the recall's "
    "extra loss minus the lookup's, on the same cluster-bootstrap draws. (a) gap >= 0.3 and lookup extra loss <= 0.10; "
    "(a') lookup extra loss >= 0.20; (b) the lookup's value share under the whole change <= 0.05; (c) on the chosen "
    "scenes of P_cf's test half, the position share without a random part of U''s share minus the position share "
    "without U' >= 0.30 (shares of scenes, not of the whole change's position answers). Point estimates decide (EPS "
    "1e-9); cluster bootstrap over the bridge item A (10,000 resamples, seed 0), 95% intervals beside; X0's validity bar "
    "(S_whole >= 0.30 and >= 30 switches) reported per reader, not in the rule; an extra loss with no switch under the "
    "whole change is undefined and its clause does not hold. Each model on its own; a model whose gate (0.80 per "
    "reader) or cue competence fails is not tested."
)  # fmt: skip
# Zach's M->P numbers on the toy suite (tasks_v2 full2, J++ top-10 knock-out at each model's C1 band): M->P points lost
# minus the rotated control's (rule.loss.MP - rule.control_distance.MP). No file prints the triple; this reading of it
# (27B 12.87 - 0.99, 9B 6.98 - 9.30, Muse 0 - 0) is ours.
ZACH_MP = {
    "qwen3.6-27b": {"points": 12, "band": "L32-40", "n": 101, "src": "results/ablate_v2/c1_v2/full2_ko_v1.json"},
    "qwen3.5-9b": {"points": -2, "band": "L12-16", "n": 43, "src": "results/ablate_v2/c1_v2/qwen35_9b_full2_ko_v1.json"},
    "muse-glimmer-30b": {"points": 0, "band": "L36-42", "n": 69, "src": "results/ablate_v2/c1_v2/muse30_full2_ko_v1.json"},
}  # fmt: skip


# ---- cues and scenes (tokenizer only) -----------------------------------------------------------------------------


def cue_list(tok) -> tuple[dict[str, str], dict[str, str]]:
    """Per animal of CUES that is one token on this tokenizer (with 0-9 legs: the routes pool), its first one-token
    cue; and the dropped animals with the reason (the pool's animals without a candidate among them)."""
    words = [w for c in CUES.values() for w in c]
    assert len(words) == len(set(words)), "a cue candidate belongs to two animals"
    _, animals, _ = R.pools(tok)
    cues, dropped = {}, {a: "no candidate cue (no one-word cue names it alone)" for a in animals if a not in CUES}
    for a, cands in sorted(CUES.items()):
        if a not in animals:
            dropped[a] = "the animal is not one token"
            continue
        one = [c for c in cands if R.one_token(tok, c)]
        if one:
            cues[a] = one[0]
        else:
            dropped[a] = f"no one-token cue among {list(cands)}"
    return cues, dropped


def render(tok, context: str, question: str, kind: str) -> str:
    """tasks_v2's prompt (prose: one user turn, chat template, thinking off, 'Answer:' prefilled); digit or one word."""
    from scripts import tasks_v2 as T

    return T.render(tok, {"format": "prose", "kind": kind, "context": context, "question": question})


def cue_prompts(tok, cues: dict[str, str], seed: int = CUE_SEED) -> list[dict]:
    """The competence prompts: per cue, CUE_PEOPLE people (seeded per cue) x CUE_TEMPLATES."""
    from bridge_jspace.tokens import raw_encoding

    _, _, people = R.pools(tok)
    out = []
    for a, cue in sorted(cues.items()):
        for p in random.Random(f"{seed}|{cue}").sample(people, CUE_PEOPLE):
            for t, (st, q) in enumerate(CUE_TEMPLATES):
                text = render(tok, st.format(p=p, cue=cue), q.format(p=p), "animal")
                out.append({"animal": a, "cue": cue, "person": p, "template": t, "text": text,
                            "ids": raw_encoding(tok, text)["input_ids"]})  # fmt: skip
    return out


# other words that name an animal of the domain (its young, its sex, a common kind), read as that animal
ALIASES = {"honeybee": "bee", "bumblebee": "bee", "hen": "chicken", "rooster": "chicken", "puppy": "dog",
           "kitten": "cat", "kitty": "cat", "cattle": "cow", "pony": "horse", "bunny": "rabbit", "lamb": "sheep",
           "piglet": "pig", "hog": "pig", "mice": "mouse", "geese": "goose"}  # fmt: skip


def named(text: str) -> str | None:
    """The first animal of the domain the first line of a reply names (its plural with -s / -es, or an ALIASES word)."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    names = {a.lower(): a for a in T.DOMAINS["animals"].values}
    names.update({f"{a}s": b for a, b in list(names.items())} | {f"{a}es": b for a, b in list(names.items())})
    names.update(ALIASES)
    names.update({f"{a}s": b for a, b in ALIASES.items()})
    return next((names[w] for w in re.findall(r"[a-z]+", S.first_line(text).lower()) if w in names), None)


def cue_table(rows: list[dict], cues: dict[str, str]) -> tuple[dict[str, dict], dict[str, str]]:
    """Per cue: prompts, how many name its animal, the share, kept (share >= CUE_BAR); and the kept cues."""
    table = {}
    for a, cue in sorted(cues.items()):
        mine = [r for r in rows if r["animal"] == a]
        right = sum(r["right"] for r in mine)
        share = right / len(mine) if mine else 0.0
        table[a] = {"cue": cue, "prompts": len(mine), "right": right, "share": round(share, 4),
                    "kept": bool(mine) and share >= CUE_BAR - EPS,
                    "named": dict(collections.Counter(str(r["named"]) for r in mine))}  # fmt: skip
    return table, {a: t["cue"] for a, t in table.items() if t["kept"]}


def feasible(kept: dict[str, str]) -> tuple[bool, str]:
    """Whether the generator can draw scenes from the kept animals (>= CUE_MIN, two leg counts at least)."""
    from scripts import tasks_v2 as T

    legs = {T.DOMAINS["animals"].values[a] for a in kept}
    if len(kept) < CUE_MIN:
        return False, f"{len(kept)} animals kept, fewer than {CUE_MIN}"
    if len(legs) < 2:
        return False, f"the kept animals all have {legs} legs (A and B must differ)"
    return True, f"{len(kept)} animals kept, legs {sorted(legs)}"


def sentence(p: str, x: str, asked: str, cue: str | None) -> str:
    return FRAME.format(p=p, cue=cue) if p == asked else f"{p} picked the {x}."


def context(lockers: list[tuple[str, int]], picks: list[tuple[str, str]], asked: str, cue: str) -> str:
    """The locker sentences (by name) first, then the pick sentences; the asked person's pick is the FRAME."""
    return " ".join(
        [f"The locker of the {x} is {d}." for x, d in lockers] + [sentence(p, x, asked, cue) for p, x in picks]
    )


def cue_position(tok, text: str, ctx: str, asked: str, cue: str) -> tuple[list[int], list[int]]:
    """The rendered prompt's ids and the token positions of the cue in the asked person's pick sentence."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    enc = raw_encoding(tok, text, offsets=True)
    sent = FRAME.format(p=asked, cue=cue)
    assert text.count(ctx) == 1, "the context is not once in the prompt"
    assert ctx.count(sent) == 1, "the pick sentence is not once in the context"
    w0 = text.index(ctx) + ctx.index(sent) + sent.rindex(cue)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(cue))


def encode(tok, scene: dict, legs: dict, expect: dict) -> tuple[dict | None, str]:
    """Both readers' O and S prompts (scene: lockers / picks of O and S, the asked person, the cues); the cue one token
    that is exactly the cue, at the same index in O and S and for both readers, the prompts identical before it."""
    from scripts import suite_v1 as S

    readers, pos = {}, None
    o, s = scene["context"], scene["cf_context"]
    for w, q, ans in ((X.LOOKUP, R.LOOKUP_Q, (expect["original"], expect["value"])),
                      (X.RECALL, R.RECALL_Q, (legs[scene["bridge"]], legs[scene["cf_bridge"]]))):  # fmt: skip
        question = q.format(p=scene["asked"])
        ids, at = {}, {}
        for v, ctx, cue in (("org", o, scene["cue"]), ("alt", s, scene["cf_cue"])):
            ids[v], at[v] = cue_position(tok, render(tok, ctx, question, "digit"), ctx, scene["asked"], cue)
        if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
            return None, "the cue is not one token at the same index in O and S"
        p = at["org"][0]
        if (
            tok.decode([ids["org"][p]]).strip() != scene["cue"]
            or tok.decode([ids["alt"][p]]).strip() != scene["cf_cue"]
        ):
            return None, "the cue token is not exactly the cue"
        if pos is not None and p != pos:
            return None, "the readers' cue positions differ"
        pos = p
        org_ans, alt_ans = (str(v) for v in ans)
        readers[w] = {"question": question, "answer": org_ans, "cf_answer": alt_ans, "ids": ids,
                      "tok_A": S.answer_token(tok, org_ans, "digit"), "tok_b": S.answer_token(tok, alt_ans, "digit")}  # fmt: skip
    for v in ("org", "alt"):
        if readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1]:
            return None, "the readers' prompts differ before the cue"
    if readers[X.LOOKUP]["tok_A"] == readers[X.LOOKUP]["tok_b"]:
        return None, "O's and S's lookup answers share their first token"
    routes = {k: S.answer_token(tok, str(v), "digit") for k, v in expect.items()}
    return {**scene, "condition": "C2", "domain": "animals", "pos": pos, "space": S.ids(tok, " "),
            "expect": {k: int(v) for k, v in expect.items()}, "route_tokens": routes, "readers": readers}, ""  # fmt: skip


def decoy(tok, case: dict, kept: dict[str, str], seed: int = DECOY_SEED) -> dict | None:
    """The elimination check's prompt: O's lookup with A's cue swapped for the cue of a kept animal not in the scene
    (seeded per scene), the cue token at the same index; None if no kept animal is free or it does not align."""
    free = sorted(set(kept) - {case["bridge"], case["cf_bridge"], case["third"]})
    if not free:
        return None
    d = random.Random(f"{seed}|{case['scene']}").choice(free)
    ctx = context(case["lockers"], case["picks"], case["asked"], kept[d])
    ids, at = cue_position(
        tok, render(tok, ctx, R.LOOKUP_Q.format(p=case["asked"]), "digit"), ctx, case["asked"], kept[d]
    )
    org = case["readers"][X.LOOKUP]["ids"]["org"]
    if len(ids) != len(org) or at != [case["pos"]] or ids[: case["pos"]] != org[: case["pos"]]:
        return None
    return {"animal": d, "cue": kept[d], "ids": ids}


def split(scenes: list[str], seed: int = SPLIT_SEED) -> set[str]:
    """P_cf's fit half: half of the scene ids (a seeded permutation of the sorted ids); the rest is the test half."""
    keys = sorted(scenes)
    perm = np.random.default_rng(seed).permutation(len(keys))
    return {keys[i] for i in perm[: len(keys) // 2]}


def scenes(tok, kept: dict[str, str], n: int | None = None, seed: int = SEED) -> tuple[list[dict], collections.Counter]:
    """n (default N_GEN) C2 scenes from the kept animals (x6_routes' draws), each with its half and its elimination
    prompt; drops counted by reason. Fewer than n if the draws run out (100 n attempts)."""
    from scripts import tasks_v2 as T

    n = N_GEN if n is None else n
    legs = T.DOMAINS["animals"].values
    _, _, people = R.pools(tok)
    animals = sorted(kept)
    rng = random.Random(seed)
    out, dropped = [], collections.Counter()
    i = 0
    while len(out) < n and i < 100 * n:
        i += 1
        A, B, C = rng.sample(animals, 3)
        if legs[A] == legs[B]:
            dropped["A and B have the same number of legs"] += 1
            continue
        a, b, c, _, e = rng.sample(range(1, 10), 5)
        asked, p1, p2 = rng.sample(people, 3)
        order = rng.sample([A, B, C], 3)
        val = {A: a, B: b, C: c}
        picks = rng.sample([(asked, A), (p1, B), (p2, C)], 3)
        sw = {B: C, C: B}
        lockers = [(x, val[x]) for x in order]
        cf_lockers = [(sw.get(x, x), e if sw.get(x, x) == B else val[sw.get(x, x)]) for x in order]
        cf_picks = [(q, B if q == asked else x) for q, x in picks]
        sc = {"scene": f"C2-{i:04d}", "bridge": A, "cf_bridge": B, "third": C, "asked": asked, "cue": kept[A],
              "cf_cue": kept[B], "lockers": lockers, "cf_lockers": cf_lockers, "picks": picks, "cf_picks": cf_picks,
              "context": context(lockers, picks, asked, kept[A]),
              "cf_context": context(cf_lockers, cf_picks, asked, kept[B])}  # fmt: skip
        case, why = encode(tok, sc, legs, {"identity": b, "position": c, "value": e, "original": a})
        if case is None:
            dropped[why] += 1
            continue
        out.append(case)
    fit = split([c["scene"] for c in out])
    for c in out:
        c["half"] = "fit" if c["scene"] in fit else "test"
        c["decoy"] = decoy(tok, c, kept)
    return out, dropped


def pick_words(case: dict) -> list[str]:
    """The words of O's and S's asked pick sentences (the slot-leak check)."""
    return [w.lower() for cue in (case["cue"], case["cf_cue"])
            for w in re.findall(r"[A-Za-z']+", FRAME.format(p=case["asked"], cue=cue))]  # fmt: skip


def pcf_pairs(tok, cases: list[dict]) -> tuple[list[dict], collections.Counter]:
    """P_cf's pairs on the given (fit-half) scenes: O and O with A's locker sentence trading places with B's, then with
    C's, every digit kept (the lookup's answer does not change); the lookup prompt's ids, the cue at the same index."""
    out, why = [], collections.Counter()
    for c in cases:
        q = R.LOOKUP_Q.format(p=c["asked"])
        org = c["readers"][X.LOOKUP]["ids"]["org"]
        items, val = [x for x, _ in c["lockers"]], dict(c["lockers"])
        for partner in (c["cf_bridge"], c["third"]):
            sw = {c["bridge"]: partner, partner: c["bridge"]}
            moved = [(sw.get(x, x), val[sw.get(x, x)]) for x in items]  # the two sentences trade slots, digits kept
            ctx = context(moved, c["picks"], c["asked"], c["cue"])
            ids, at = cue_position(tok, render(tok, ctx, q, "digit"), ctx, c["asked"], c["cue"])
            if len(ids) != len(org) or at != [c["pos"]]:
                why["the cue is not at the same index"] += 1
                continue
            out.append({"scene": c["scene"], "partner": partner, "slots": [items.index(c["bridge"]), items.index(partner)],
                        "pos": c["pos"], "context": ctx, "ids": {"org": org, "alt": ids}})  # fmt: skip
    why["pairs"] = len(out)
    return out, why


def mark(decode, ids: list[int], pos: int) -> str:
    return R.marked(decode, ids, pos)


def stage_plan() -> dict:
    """Tokenizer only: the cue list (one-token candidates, dropped animals), the scenes with every one-token cue kept
    (before the competence step), drops by reason, the halves, P_cf's pairs, the slot-leak check, one example."""
    from scripts import x45m

    tok = x45m.tokenizer()
    cues, dropped = cue_list(tok)
    cases, why = scenes(tok, cues)
    leak = [c["scene"] for c in cases if SLOT_WORDS & set(pick_words(c))]
    _, pwhy = pcf_pairs(tok, [c for c in cases if c["half"] == "fit"])
    c = cases[0]
    decode = tok.decode
    out = {"target": pins.TARGET, "frame": FRAME, "candidates": len(CUES), "cues": cues, "n_cues": len(cues),
           "dropped": dropped, "n_dropped": len(dropped), "prompts_per_cue": CUE_PEOPLE * len(CUE_TEMPLATES),
           "scenes": len(cases), "scenes_dropped": dict(why),
           "halves": dict(collections.Counter(x["half"] for x in cases)),
           "bridge_items": dict(collections.Counter(x["bridge"] for x in cases)),
           "decoy": sum(x["decoy"] is not None for x in cases), "slot_leak": leak, "pcf_pairs": dict(pwhy),
           "example": {"scene": c["scene"], "O": c["context"], "S": c["cf_context"], "expect": c["expect"],
                       "lookup_O_marked": mark(decode, c["readers"][X.LOOKUP]["ids"]["org"], c["pos"]),
                       "decoy": c["decoy"] and {"animal": c["decoy"]["animal"], "cue": c["decoy"]["cue"]}}}  # fmt: skip
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


# ---- GPU ----------------------------------------------------------------------------------------------------------


def generate(model, prompts: list[dict], desc: str) -> list[str]:
    """GEN_TOKENS greedy tokens per prompt, prompts of one length batched together."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_split as P

    texts: list[str | None] = [None] * len(prompts)
    by_len: dict[int, list[int]] = collections.defaultdict(list)
    for i, p in enumerate(prompts):
        by_len[len(p["ids"])].append(i)
    chunks = [idx[s : s + P.BATCH] for idx in by_len.values() for s in range(0, len(idx), P.BATCH)]
    with torch.no_grad():
        for chunk in progress(chunks, desc):
            ids = torch.tensor([prompts[i]["ids"] for i in chunk], device=model.device)
            for i, t in zip(chunk, model.generate_batch(ids, X.GEN_TOKENS, [{} for _ in chunk]), strict=True):
                texts[i] = t
    return [t or "" for t in texts]


def cue_competence(model, prompts: list[dict]) -> list[dict]:
    """The competence step: which animal the model names for each prompt."""
    texts = generate(model, prompts, "cue competence (prompt batch)")
    return [{**{k: p[k] for k in ("animal", "cue", "person", "template")}, "greedy": t, "named": named(t),
             "right": named(t) == p["animal"]} for p, t in zip(prompts, texts, strict=True)]  # fmt: skip


def competence(model, cases: list[dict], ws) -> list[dict]:
    """Unedited O and S of both readers: 8 greedy tokens (what the model says) and the decisive read (X0's)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (scene)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                for i, (v, gold, tok_gold) in enumerate((("org", rd["answer"], rd["tok_A"]),
                                                         ("alt", rd["cf_answer"], rd["tok_b"]))):  # fmt: skip
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", c["space"], ws)
                    said = S.said(texts[i], "digit")
                    rows.append({"scene": c["scene"], "reader": w, "variant": v, "greedy": texts[i], "said": said,
                                 "right": said == gold, "read_right": int(logits[0].argmax()) == tok_gold,
                                 "top": int(logits[0].argmax())})  # fmt: skip
    return rows


def gate_of(cases: list[dict], comp: list[dict]) -> tuple[dict, list[dict]]:
    """The read gate (O's read accuracy >= GATE per reader over every generated scene) and the eligible scenes (both
    readers say and read O's and S's answers right), in scene order."""
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    gate = {"cases": len(cases), "org_read_accuracy": acc, "gate": GATE,
            "pass": all(a >= GATE - EPS for a in acc.values()), "eligible": len(ok)}  # fmt: skip
    return gate, ok


def manifest(name: str, target: str, layer: int) -> dict:
    from bridge_jspace.utils import git_state

    return {"exp": EXP, "run": name, "test": "47.3", "spec": "jobs/c3/batch47.yaml (47.3)",
            "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "inputs": {str(SPEC.relative_to(SPEC.parents[2])): X.sha256_of(SPEC)} if SPEC.exists() else {},
            "layer": layer, "frame": FRAME, "cue_candidates": {a: list(c) for a, c in CUES.items()},
            "cue_templates": [list(t) for t in CUE_TEMPLATES], "cue_people": CUE_PEOPLE, "cue_bar": CUE_BAR,
            "cue_min": CUE_MIN, "n_gen": N_GEN, "n_items": N_ITEMS, "gate": GATE, "arms": list(ARMS), "k": X.K_MAIN,
            "omp": "signed", "pointer_U": f"x0_massmean Alf of results/x0_probe/{R.STATES[target]} (not refit)",
            "pcf": f"x7_pcf's method at the cue token: centered PCA, rank {RANK}, over the fit half's pairs (A's locker "
                   "sentence trades places with B's and with C's, digits kept); the rule reads the test half",
            "read": "X0's chat read: the top token after the digit's space token", "rule": RULE,
            "as_computed": AS_COMPUTED,
            "seeds": {"scenes": SEED, "cue_people": CUE_SEED, "split": SPLIT_SEED, "decoy": DECOY_SEED,
                      "random_subspace": f"{X.SUBSPACE_SEED} + layer", "bootstrap": X.BOOT_SEED, "view": VIEW_SEED},
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip


def stage_run(name: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in RUNS, f"47.3 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, target, layer)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device

    # the competence step: the cues the model names from the cue alone
    cues, dropped = cue_list(tok)
    prompts = cue_prompts(tok, cues)
    crow = cue_competence(model, prompts)
    table, kept = cue_table(crow, cues)
    ok_cues, why_cues = feasible(kept)
    X.write_jsonl(out / "cue_competence.jsonl", crow)
    (out / "cues.json").write_text(json.dumps({"candidates": {a: list(c) for a, c in CUES.items()}, "one_token": cues,
                                               "dropped": dropped, "table": table, "kept": kept, "bar": CUE_BAR,
                                               "status": "ok" if ok_cues else "not tested", "why": why_cues},
                                              indent=1, ensure_ascii=False) + "\n")  # fmt: skip
    if not ok_cues:
        print(f"not tested (cue competence): {why_cues}", flush=True)
        return out

    # the scenes, the gate and the eligible scenes
    cases, why = scenes(tok, kept)
    ws = X.whitespace_mask(model)
    comp = competence(model, cases, ws)
    gate, ok = gate_of(cases, comp)
    chosen = ok[:N_ITEMS]
    gate.update({"chosen": len(chosen), "dropped": dict(why), "halves": dict(collections.Counter(c["half"] for c in cases)),
                 "chosen_halves": dict(collections.Counter(c["half"] for c in chosen)),
                 "order": [c["scene"] for c in chosen]})  # fmt: skip
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    (out / "gate.json").write_text(json.dumps(gate, indent=1) + "\n")
    if not gate["pass"] or not chosen:
        print(f"not tested (gate): {gate['org_read_accuracy']} (bar {GATE}), eligible {gate['eligible']}", flush=True)
        return out

    def state(ids: list[int]):
        return model.run(torch.tensor([ids], device=dev), record=(layer,))[1][layer]

    with torch.no_grad():
        # U' (P_cf) refit on the fit half's pairs
        pairs, pwhy = pcf_pairs(tok, [c for c in cases if c["half"] == "fit"])
        h_org, diffs = {}, []
        for p in progress(pairs, f"P_cf pairs at L{layer} (pair)"):
            if p["scene"] not in h_org:
                h_org[p["scene"]] = state(p["ids"]["org"])[p["pos"]].float()
            diffs.append((state(p["ids"]["alt"])[p["pos"]].float() - h_org[p["scene"]]).double().cpu().numpy())
        pcf, mean, var = PC.fit_basis(np.stack(diffs), RANK)
        alf_np = MM.subspaces(R.STATES[target])[0]["Alf"]
        np.savez_compressed(out / "pcf.npz", P=pcf.astype(np.float32), mean=mean.astype(np.float32), var=np.array(var))
        X.write_jsonl(out / "pcf_pairs.jsonl", [{k: v for k, v in p.items() if k != "ids"} for p in pairs])
        (out / "pcf_fit.json").write_text(json.dumps({"pairs": dict(pwhy), "variance_explained": var[: PC.SHOW],
                                                      "cos2_with_U": PC.principal_cos2(pcf, alf_np),
                                                      "random_mean_cos2": RANK / pcf.shape[0], "U_rank": int(alf_np.shape[1])},
                                                     indent=1) + "\n")  # fmt: skip

        # the change at the cue token, its parts and the arms
        deltas = []
        for c in progress(chosen, f"the change at the cue token, L{layer} (scene)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            deltas.append((state(ids["alt"])[c["pos"]] - state(ids["org"])[c["pos"]]).float())
        x = torch.stack(deltas).to(dev)
        jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids()).to(dev)
        alf = torch.tensor(alf_np, dtype=torch.float32, device=dev)
        pt = torch.tensor(pcf, dtype=torch.float32, device=dev)
        parts = {"jpp": X.fit(jdic, x, X.K_MAIN, "signed").to(dev), "alf": (x @ alf) @ alf.T, "pcf": (x @ pt) @ pt.T}
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        more, sh = R.removal_arms(x, parts, basis)
        arms = {"whole": x, **more}
        assert tuple(arms) == ARMS, tuple(arms)
        digits = torch.tensor(X.digit_ids(tok), device=dev)
        rows, norms, decoys = [], [], []
        for i, c in enumerate(progress(chosen, f"reads at L{layer} (scene)")):
            norms.append({"scene": c["scene"], "half": c["half"], "norm": round(float(x[i].norm()), 4),
                          **{f"share_{k}": round(float(v[i]), 5) for k, v in sh.items()}})  # fmt: skip
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in ARMS]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for a, lg in zip(("none", *ARMS), logits, strict=True):
                    top = int(lg.argmax())
                    route = R.classify(top, c) if w == X.LOOKUP else None
                    rows.append({"scene": c["scene"], "half": c["half"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                                 "reader": w, "arm": a, "route": route,
                                 "follow": int(route in FOLLOW) if w == X.LOOKUP else None, **X.read_row(lg, rd, digits)})  # fmt: skip
            if c["decoy"] is not None:
                lg, _ = X.read_logits(model, c["decoy"]["ids"], [{}], "chat", c["space"], ws)
                top = int(lg[0].argmax())
                decoys.append({"scene": c["scene"], "entity": c["bridge"], "decoy": c["decoy"]["animal"],
                               "decoy_cue": c["decoy"]["cue"], "top": top, "class": R.classify(top, c)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "decoy.jsonl", decoys)
    m["items"] = len(chosen)
    m["items_per_half"] = dict(collections.Counter(c["half"] for c in chosen))
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.3 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def switch(r: dict) -> int:
    """The reader's switch: the lookup follows the change (identity, position or value); the recall answers S's."""
    return int(r["route"] in FOLLOW) if r["reader"] == X.LOOKUP else int(r["switched"])


def share_ci(sw: dict[str, list[int]], ents: list[str], n_boot: int) -> dict[str, list[float]]:
    rr = X.resampled_rates(sw, ents, n_boot)
    return {k: [float(np.mean(v)) if v else math.nan, *X.interval(rr[k])] for k, v in sw.items()}


def cut(by: dict, scenes: list[str], ents: list[str], part: str, route: str, n_boot: int) -> dict:
    """How much more removing the part cuts the lookup's `route` share than removing its random part (paired)."""
    no, rand = PART_ARMS[part]
    sw = {a: [int(by[(s, X.LOOKUP, a)]["route"] == route) for s in scenes] for a in ("whole", no, rand)}
    if not scenes:
        return {"n": 0, "cut": [math.nan, math.nan, math.nan]}
    rr = X.resampled_rates(sw, ents, n_boot)
    pt = {a: float(np.mean(v)) for a, v in sw.items()}
    return {"n": len(scenes), "entities": len(set(ents)), "whole": pt["whole"], "without": pt[no], "without_rand": pt[rand],
            "cut": [pt[rand] - pt[no], *X.interval(rr[rand] - rr[no])]}  # fmt: skip


def rule(lookup: dict, gap: list[float], value: list[float], pcf_cut: list[float]) -> dict:
    """47.3's clauses on one model (point estimates, EPS at the bars; an undefined number holds nothing): lookup is the
    lookup's X0 cell, gap the recall's extra loss minus the lookup's, value the lookup's value share under the whole
    change, pcf_cut U''s position cut beyond random on the test half."""
    lk, g, v, c = lookup["excess"][0], gap[0], value[0], pcf_cut[0]
    ok = lambda z: not (z is None or math.isnan(z))  # noqa: E731
    return {"a": ok(g) and ok(lk) and g >= GAP_MIN - EPS and lk <= LOOKUP_MAX + EPS,
            "a_prime": ok(lk) and lk >= THROUGH_MIN - EPS,
            "b": ok(v) and v <= VALUE_MAX + EPS,
            "c": ok(c) and c >= PCF_CUT - EPS}  # fmt: skip


def names_item(text: str) -> bool:
    """A reply that names an animal and holds no digit or number word (the lookup naming its item, not the locker)."""
    from scripts import suite_v1 as S

    return named(text) is not None and S.said(text, "digit") is None


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending, not tested (cue competence or gate), or its numbers and the rule's clauses."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        return {"run": run, "target": target, "status": "pending", "why": "no run here"}
    m = json.loads((src / "manifest.json").read_text())
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"]}
    cues = json.loads((src / "cues.json").read_text()) if (src / "cues.json").exists() else None
    if cues is None:
        return {**base, "status": "pending", "why": "no cues.json yet"}
    base["cues"] = cues
    if cues["status"] != "ok":
        return {**base, "status": "not tested", "why": f"cue competence: {cues['why']}"}
    if not (src / "gate.json").exists():
        return {**base, "status": "pending", "why": "no gate.json yet"}
    gate = json.loads((src / "gate.json").read_text())
    base["gate"] = gate
    if not gate["pass"] or not gate.get("chosen"):
        return {**base, "status": "not tested", "why": f"gate: O's read accuracy {gate['org_read_accuracy']} (bar "
                f"{GATE}), eligible {gate['eligible']}"}  # fmt: skip
    rows = X.read_jsonl(src / "outcomes.jsonl")
    if not rows:
        return {**base, "status": "pending", "why": "the gate passed but outcomes.jsonl has no rows yet"}
    by = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    scenes = list(dict.fromkeys(r["scene"] for r in rows if r["arm"] == "whole" and r["reader"] == X.LOOKUP))
    ent = {r["scene"]: r["entity"] for r in rows}
    half = {r["scene"]: r["half"] for r in rows}
    ents = [ent[s] for s in scenes]
    cells, draws, routes = {}, {}, {}
    for w in X.READERS:
        sw = {a: [switch(by[(s, w, a)]) for s in scenes] for a in ARMS}
        cells[w] = X.cell({"whole": sw["whole"], "no_part": sw["no_jpp"], "no_rand": sw["no_jpp_rand"]}, ents, n_boot)
        rr = X.resampled_rates(sw, ents, n_boot)  # the draws depend on the entities and the seed only: paired
        draws[w] = X.dependence(rr["whole"], rr["no_jpp"]) - X.dependence(rr["whole"], rr["no_jpp_rand"])
        routes[READER_NAME[w]] = share_ci(sw, ents, n_boot)
    gap = [cells[X.RECALL]["excess"][0] - cells[X.LOOKUP]["excess"][0], *X.interval(draws[X.RECALL] - draws[X.LOOKUP])]
    by_route = {
        f"{rt}|{a}": [int(by[(s, X.LOOKUP, a)]["route"] == rt) for s in scenes] for a in ARMS for rt in R.ROUTES
    }
    shares = share_ci(by_route, ents, n_boot)
    value = shares["value|whole"]
    test = [s for s in scenes if half[s] == "test"]
    fit = [s for s in scenes if half[s] == "fit"]
    pcf_test = cut(by, test, [ent[s] for s in test], "pcf", "position", n_boot)
    clauses = rule(cells[X.LOOKUP], gap, value, pcf_test["cut"])
    comp = X.read_jsonl(src / "competence.jsonl")
    lk_org = [r for r in comp if r["reader"] == X.LOOKUP and r["variant"] == "org"]
    norms = X.read_jsonl(src / "norms.jsonl")
    decoys = X.read_jsonl(src / "decoy.jsonl")
    pcf_fit = json.loads((src / "pcf_fit.json").read_text()) if (src / "pcf_fit.json").exists() else {}
    return {**base, "status": "tested", "n": len(scenes), "entities": len(set(ents)), "clauses": clauses,
            "lookup": cells[X.LOOKUP], "recall": cells[X.RECALL], "gap": gap, "value": value,
            "pcf_cut_test": pcf_test,
            "descriptive": {
                "route_shares": {a: {rt: shares[f"{rt}|{a}"] for rt in R.ROUTES} for a in ARMS},
                "reader_switch": routes,
                "pcf_cut_fit_half_in_sample": cut(by, fit, [ent[s] for s in fit], "pcf", "position", n_boot),
                "U_cut_position": cut(by, scenes, ents, "alf", "position", n_boot),
                "jpp_cut_identity": cut(by, scenes, ents, "jpp", "identity", n_boot),
                "median_share": {k: float(np.median([x[f"share_{k}"] for x in norms])) for k in PART_ARMS},
                "names_item_instead_of_digit": {"n": len(lk_org), "count": sum(names_item(r["greedy"]) for r in lk_org)},
                "elimination": {"n": len(decoys), **dict(collections.Counter(DECOY_CLASS[d["class"]] for d in decoys))},
                "pcf_fit": pcf_fit}}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def view(run: str, decode=None, k: int = N_VIEW, seed: int = VIEW_SEED) -> list[str]:
    """The verify-pack view: k random scenes of the run (seed, over its chosen scenes sorted), each reader's O prompt
    as the model reads it (the digit's space appended) with the cue token in ⟦…⟧ (where h_S - h_O is added), S's prompt
    with the same token marked, every arm's top token (the lookup's route), and the elimination read."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    decoys = {d["scene"]: d for d in X.read_jsonl(src / "decoy.jsonl")}
    scenes = sorted({r["scene"] for r in rows})
    lines = [f"## {run} ({m['model']['target']}, L{m['layer']}): {min(k, len(scenes))} random scenes of {len(scenes)} "
             f"(random.Random({seed}) over the sorted scenes)", ""]  # fmt: skip
    for s in sorted(random.Random(seed).sample(scenes, min(k, len(scenes)))):
        c = cases[s]
        lines += [f"### {s} ({c['half']} half): O's pick {c['bridge']} ({c['cue']!r}) -> S's {c['cf_bridge']} "
                  f"({c['cf_cue']!r}); routes {c['expect']}", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            space = c.get("space") or []
            lines += [f"**{READER_NAME[w]}**: O's answer {rd['answer']}, S's {rd['cf_answer']}", "", "O, as read:", "",
                      "```", mark(decode, rd["ids"]["org"] + space, c["pos"]), "```", "", "S (the source):", "", "```",
                      mark(decode, rd["ids"]["alt"] + space, c["pos"]), "```", "",
                      "| arm | top token | route | switched (S's answer) |", "|---|---|---|---|"]  # fmt: skip
            for a in ("none", *ARMS):
                r = next(x for x in rows if x["scene"] == s and x["reader"] == w and x["arm"] == a)
                lines.append(f"| {a} | {decode([r['top']])!r} | {r['route'] or ''} | {r['switched']} |")
            lines.append("")
        if s in decoys:
            d = decoys[s]
            lines += [f"Elimination read (A's cue -> {d['decoy_cue']!r}, the {d['decoy']}, not in the scene): lookup "
                      f"top {decode([d['top']])!r} ({DECOY_CLASS[d['class']]}).", ""]  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, decode=None) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [mm["target"] for mm in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    out = RESULTS / f"x47_3-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    lines = ["# 47.3: a computed bridge, the routes test with a described item (UNVERIFIED)", "",
             f"Batch 47, test 47.3 (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). The asked pick is "
             f"\"{FRAME.format(p='<p>', cue='<cue>')}\"; the change h_S - h_O at the cue token at the layer fixed in "
             f"advance, C2 (another item moved). Cluster bootstrap over the bridge item ({n_boot}, seed {X.BOOT_SEED}).",
             "", f"Rule (fixed in advance): {RULE}", "", f"As computed: {AS_COMPUTED}", "",
             "| model | run | status | n (items) | lookup extra loss | recall extra loss | gap | value (whole) | U' cut, "
             "test half (n) | (a) | (a') | (b) | (c) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} ({mm['why']}) | | | | | | | | | | |")
            continue
        c = mm["clauses"]
        lines.append(f"| {mm['target']} | {mm['run']} | tested | {mm['n']} ({mm['entities']}) | {fmt(mm['lookup']['excess'])} "
                     f"| {fmt(mm['recall']['excess'])} | {fmt(mm['gap'])} | {fmt(mm['value'])} | "
                     f"{fmt(mm['pcf_cut_test']['cut'])} ({mm['pcf_cut_test']['n']}) | {yn(c['a'])} | {yn(c['a_prime'])} | "
                     f"{yn(c['b'])} | {yn(c['c'])} |")  # fmt: skip
    lines += ["", "Zach's M->P numbers beside (toy suite, J++ top-10 knock-out at each model's C1 band, M->P points lost "
              "minus the rotated control's; our reading of the triple 12 / -2 / 0): "
              + "; ".join(f"{t} {z['points']:+d} ({z['band']}, n {z['n']}, {z['src']})" for t, z in ZACH_MP.items())
              + ".", ""]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            continue
        d = mm["descriptive"]
        lk, rc = mm["lookup"], mm["recall"]
        lines += [f"## {mm['target']} ({mm['run']}, L{mm['layer']})", "",
                  f"Cues kept {len(mm['cues']['kept'])} of {len(mm['cues']['one_token'])} one-token "
                  f"({len(mm['cues']['dropped'])} animals dropped before: {mm['cues']['dropped']}); gate "
                  f"{mm['gate']['org_read_accuracy']}, eligible {mm['gate']['eligible']}, chosen {mm['gate']['chosen']} "
                  f"(halves {mm['gate']['chosen_halves']}).", "",
                  f"Validity (X0's bar): lookup {yn(lk['valid'])} (S_whole {lk['S_whole'][0]:.2f}, {lk['switched_whole']} "
                  f"switches), recall {yn(rc['valid'])} (S_whole {rc['S_whole'][0]:.2f}, {rc['switched_whole']}).", "",
                  "| arm | " + " | ".join(R.ROUTES) + " | lookup follows | recall follows S |",
                  "|---|" + "---|" * (len(R.ROUTES) + 2)]  # fmt: skip
        for a in ARMS:
            lines.append(f"| {a} | " + " | ".join(fmt(d["route_shares"][a][rt]) for rt in R.ROUTES)
                         + f" | {fmt(d['reader_switch']['lookup'][a])} | {fmt(d['reader_switch']['recall'][a])} |")  # fmt: skip
        el, ni = d["elimination"], d["names_item_instead_of_digit"]
        lines += ["", f"Cuts beyond the random part (position share without the random part minus without the part): "
                  f"U' on the fit half (in sample) {fmt(d['pcf_cut_fit_half_in_sample']['cut'])}; U (expected not to "
                  f"transfer) {fmt(d['U_cut_position']['cut'])}; identity without J++ "
                  f"{fmt(d['jpp_cut_identity']['cut'])}. Median shares of the change: {d['median_share']}.",
                  f"P_cf fit: {d['pcf_fit'].get('pairs')}; variance explained {d['pcf_fit'].get('variance_explained')}; "
                  f"cos² with U {d['pcf_fit'].get('cos2_with_U')} (random {d['pcf_fit'].get('random_mean_cos2')}).",
                  f"Lookup on O naming an animal instead of a digit (greedy, unedited): {ni['count']} of {ni['n']}. "
                  f"Elimination check (A's cue swapped for an absent animal's; original = A's locker): {el}.", ""]  # fmt: skip
    (out / "x47_3.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str)
                                    + "\n")  # fmt: skip
    (out / "x47_3.md").write_text("\n".join(lines) + "\n")
    ex = ["# 47.3 view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the cue token where the change is "
          "added. UNVERIFIED.", ""]  # fmt: skip
    for mm in models:
        if mm["status"] == "tested":
            ex += view(mm["run"], decode)
    (out / "view.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(runs: list[str], decode=None) -> Path:
    """The verify-pack view alone (sealed as the verdict): view.md over the runs that hold outcomes."""
    assert dan_answer(), (
        f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    )
    out = RESULTS / f"x47_3-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.3 view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the cue token where the change is "
             "added. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        if (RESULTS / run / "outcomes.jsonl").exists():
            lines += view(run, decode)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x47_cue/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the runs (27B, 9B, Muse)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name)
    elif a.stage == "view":
        stage_view(a.runs)
    else:
        stage_verdict(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
