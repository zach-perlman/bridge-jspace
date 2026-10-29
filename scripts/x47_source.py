"""x47_source (batch 47, test 47.15, amendment 5; jobs/c3/batch47.yaml "47.15", rule fixed in advance; Q47.15 in
predictions/2026-10-28_dan.md): one question, two sources. Does the part of the bridge word's change that carries the
answer follow the source the answer comes from (the passage: a lookup; memory: a recall), or the question?

Scenes: the routes test's locker-first C2 scenes (x6_routes.scenes, seed 2510, the same generator stream: "Iris picked
A" -> B in S, B's and C's locker sentences swapped, B's digit new), plus one attribute sentence per item stating a FALSE
number of legs ("The frog has 7 legs."): per scene (seed 4715 and the scene id) three distinct digits of 1-9 outside O's
and S's locker digits and outside all three items' true legs (tasks_v2's animals; a scene without three such digits is
dropped and counted), in a seeded order independent of the locker order. Placement "after": lockers, picks, attributes
(the bridge word cannot address the attribute sentence: dumbest way 2); "before": lockers, attributes, picks (reported).
A base scene is kept only if it encodes in both placements (paired). O and S share the attribute sentences.

One question, "How many legs does <person>'s pick have?", under three conditions (readers): from the text ("Answer using
only the passage."), from memory ("Ignore the passage; answer from what you know.") and no instruction. The instruction
sits in the user turn right after the question and before X0's digit instruction ("Answer with a single digit and nothing
else."), so the three conditions share every token through the end of the passage (asserted per scene: the bridge is
one token at one index in O, S and every condition; the read is X0's chat read, the top token after a space appended to
the prompt, so the read position is the last token in every condition; its index per condition is recorded). The
no-instruction prompt is the routes test's recall prompt on the extended passage.

Answers: from the text, O -> A's false digit, S -> B's; from memory, O -> A's true legs, S -> B's. Gate (per placement,
over every candidate scene): O's unedited read right in >= 0.80 of the scenes under EACH instruction. Eligible: O and S
said and read right under both instructions; the first 300 in generator order whose bridge entities have class means
(the identity direction needs them; drops counted). The refusal share (dumbest way 3): under each instruction, the share
of unedited answers that follow the instruction, the other source, neither, and the share with no digit in 8 greedy
tokens. No-instruction: each unedited O and S answer classified text / memory / other (descriptive).

Edits at the bridge word at L = X.PREDICTED (27B L32, 9B L12, Muse L26), on O, read by all three conditions (the change
h_S - h_O is the same for the three: it depends on the shared prefix only):
  none           O unedited
  whole          h_S - h_O
  no_jpp         minus its J++ part (signed OMP, k = 25, over the J++ lens's letter-token atoms at L, as X0)
  no_jpp_rand    minus a random part of J++'s share (X0's random subspace, seed 888 + L)
  no_ui          minus its U + I part: the projection on span(U, I), U the 4 pointer directions (x0_massmean Alf, fit
                 on the probe's fresh scenes, never refit), I the identity direction mu_B - mu_A orthogonalized against
                 the scene's 25 J++ atoms (x6_routes --identity's idout; x6's alf+idout part)
  no_ui_rand     minus a random part of U + I's share
  keep_jpp / keep_jpp_rand, keep_ui / keep_ui_rand   only that part / only a random part of its share
  source         S unedited (the reference: what S itself answers under the condition)
Switch = the top token is S's answer under the condition: the changed item's (B's) false digit from the text, B's true
legs from memory; no instruction: per class (text / memory), B's digit of the class of the item's unedited O and S
answers (both in the class).

Rule (fixed in advance, per model, placement "after", point estimates; EPS 1e-9 at the bars): extra loss of a part under
a condition = (1 - S_no_part / S_whole) - (1 - S_no_rand / S_whole). A condition behaves "like a lookup" if the extra
loss without J++ <= 0.10 and without U + I >= 0.30; "like a recall" if without J++ >= 0.30 and without U + I <= 0.10;
"can't tell" if its whole-change cell is invalid (X0: S_whole < 0.30 or fewer than 30 switches); else "neither". "The
part follows the source" on a model: text like a lookup and memory like a recall; on the batch: on >= 2 of 3 models.
"The part follows the question": both instructions give the same label (lookup or recall) on the model; on the batch, on
>= 2 of 3 models (the same count, as computed). A model whose gate fails is not tested. Cluster-bootstrap CIs over the
bridge items (10,000 resamples, seed 0) beside every number. No-instruction check: within each class, the same numbers
and label, matched against the instructed twin's; and which source the model prefers unprompted (the class shares of the
unedited O answers over the chosen items).

SEALED: the run writes manifest, plan, cases, competence, gate (the gate and refusal shares: not a result), outcomes,
norms and the examples' greedy texts (10 random base scenes, seed 0, in both placements), no verdict. `verdict` refuses until predictions/2026-10-28_dan.md holds Dan's
Q47.15 answer at the committed HEAD. `competence` (CPU) prints the gate and refusal shares of a run (unsealed).

uv run python scripts/x47_source.py plan --out <dir>                 # CPU, the target's tokenizer: counts, 5 prompts per condition
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_source.py run --name qwen35_9b_x47_15 --why "..."   # GPU (sealed)
uv run python scripts/x47_source.py competence --name qwen35_9b_x47_15                            # CPU, the gate
uv run python scripts/x47_source.py verdict --runs x47_15_27b qwen35_9b_x47_15 muse30_x47_15     # CPU, after Dan's Q47.15
"""

from __future__ import annotations

import argparse
import collections
import json
import math
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
from scripts import x6_routes as R
from scripts import x47_atoms as A

EXP = "x47_source"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml"
TEST = "47.15"
PREDICTIONS = A.PREDICTIONS
QUESTION = "Q47.15"
CONDITION = "C2"  # the routes test's condition (another item moved); C0 (only the pick changes) is an option
SEED = 4715  # the false digits and the attribute sentences' order, per scene with the scene id
PLACEMENTS = ("after", "before")
DECISIVE = "after"
CONDS = ("text", "memory", "none")
INSTRUCTED = ("text", "memory")
INSTRUCTION = {"text": "Answer using only the passage.", "memory": "Ignore the passage; answer from what you know.",
               "none": ""}  # fmt: skip
QUESTION_TEXT = R.RECALL_Q  # "How many legs does {p}'s pick have?"
EDIT_ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_ui", "no_ui_rand", "keep_jpp", "keep_jpp_rand", "keep_ui",
             "keep_ui_rand")  # fmt: skip
ARMS = ("none", *EDIT_ARMS, "source")
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change h_S - h_O at the bridge word",
    "no_jpp": "without its J++ part (signed OMP, k = 25)",
    "no_jpp_rand": "without a random part of J++'s share",
    "no_ui": "without its U + I part (the pointer directions and the identity direction outside J++, together)",
    "no_ui_rand": "without a random part of U + I's share",
    "keep_jpp": "only the J++ part",
    "keep_jpp_rand": "only a random part of J++'s share",
    "keep_ui": "only the U + I part",
    "keep_ui_rand": "only a random part of U + I's share",
    "source": "S unedited (the reference)",
}
PARTS = (("jpp", "no_jpp", "no_jpp_rand"), ("ui", "no_ui", "no_ui_rand"))
KEEPS = (("jpp", "keep_jpp", "keep_jpp_rand"), ("ui", "keep_ui", "keep_ui_rand"))
LOOKUP_JPP_MAX, LOOKUP_UI_MIN = 0.10, 0.30  # "like a lookup": without J++ <= 0.10, without U + I >= 0.30
RECALL_JPP_MIN, RECALL_UI_MAX = 0.30, 0.10  # "like a recall": without J++ >= 0.30, without U + I <= 0.10
MODELS = ("qwen3.6-27b", "qwen3.5-9b", "muse-glimmer-30b")
RUNS = {"qwen3.6-27b": "x47_15_27b", "qwen3.5-9b": "qwen35_9b_x47_15", "muse-glimmer-30b": "muse30_x47_15"}
# batch 52 C coverage (amendment 2: the full grid on Lightning): run-stage targets beyond the design's; the
# verdict's own model list is unchanged (verdict --coverage reads these runs alone)
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_source"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x47_source/x47_15-20261028T142722Z"  # 47.15's rules first scored (27B, 9B, Muse)
MODELS_MIN = 2
EPS = 1e-9  # a value exactly at a bar counts as at the bar
N_PROMPTS = 5  # the plan's rendered prompts per condition
ANSWERS = ("S_text", "S_memory", "O_text", "O_memory", "other")  # what a read's top token is
RULE = ("per model (placement after): extra loss = (1 - S_no_part / S_whole) - (1 - S_no_rand / S_whole); a condition "
        "is like a lookup if without J++ <= 0.10 and without U + I >= 0.30, like a recall if without J++ >= 0.30 and "
        "without U + I <= 0.10, can't tell if its whole cell is invalid (S_whole < 0.30 or < 30 switches), else "
        "neither; the part follows the source if text is like a lookup and memory like a recall; follows the question "
        "if both give the same label (lookup or recall); each on the batch on >= 2 of 3 models; a model whose gate "
        "(0.80 per instruction) fails is not tested")  # fmt: skip
LOCKER = re.compile(r"^The locker of the (\w+) is (\d)\.$")


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def sentences(context: str) -> list[str]:
    """The context's sentences in order (x6's contexts: sentences ending in '.', joined by one space)."""
    return [s + "." for s in context.rstrip(".").split(". ")]


def locker_slots(context: str) -> list[tuple[str, int]]:
    """(item, digit) of each locker sentence in order."""
    return [(m.group(1), int(m.group(2))) for s in sentences(context) if (m := LOCKER.match(s))]


def attribute_plan(o: str, s: str, legs: dict[str, int], rng: random.Random) -> dict | None:
    """The scene's false digits (one per locker item, distinct, in 1-9, outside O's and S's locker digits and outside
    every item's true legs) and the attribute sentences' order; None if fewer than three digits remain."""
    items = [x for x, _ in locker_slots(o)]
    taken = {d for _, d in locker_slots(o)} | {d for _, d in locker_slots(s)} | {legs[x] for x in items}
    pool = [d for d in range(1, 10) if d not in taken]
    if len(pool) < len(items):
        return None
    return {
        "false": dict(zip(items, rng.sample(pool, len(items)), strict=True)),
        "order": rng.sample(items, len(items)),
    }


def attribute_sentence(item: str, n: int) -> str:
    return f"The {item} has {n} leg{'' if n == 1 else 's'}."


def with_attributes(context: str, attributes: list[str], placement: str) -> str:
    """The context with the attribute sentences after the pick sentences ("after") or between the locker sentences
    and the picks ("before")."""
    assert placement in PLACEMENTS, placement
    sents = sentences(context)
    lockers = [s for s in sents if LOCKER.match(s)]
    picks = [s for s in sents if R.PICK.fullmatch(s)]
    assert lockers + picks == sents, context
    assert len(lockers) == len(picks) == 3, context
    return " ".join(lockers + picks + attributes if placement == "after" else lockers + attributes + picks)


def question(asked: str, cond: str) -> str:
    q = QUESTION_TEXT.format(p=asked)
    return f"{q} {INSTRUCTION[cond]}" if INSTRUCTION[cond] else q


def encode(tok, o: str, s: str, asked: str, a_item: str, bridge: str, answers: dict[str, tuple[int, int]],
           scene: str, placement: str) -> tuple[dict | None, str]:  # fmt: skip
    """The three conditions' O and S prompts (chat rendering). The bridge (the asked person's pick) must be one token
    at one index in O and S and across the conditions, and the conditions must share every token through the end of
    the passage; else (None, why). answers: source -> (O's digit, S's digit)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    readers, pos, through = {}, None, None
    for cond in CONDS:
        q = question(asked, cond)
        ids, at, ends = {}, {}, {}
        for v, ctx, x in (("org", o, a_item), ("alt", s, bridge)):
            text = X.render(tok, {"format": "prose", "kind": "digit", "context": ctx, "question": q}, "chat", ctx)
            if text.count(ctx) != 1:
                return None, "the context is not once in the prompt"
            enc = raw_encoding(tok, text, offsets=True)
            sent = f"{asked} picked the {x}."
            if ctx.count(sent) != 1:
                return None, "the asked pick sentence is not once in the context"
            c0 = text.index(ctx)
            w0 = c0 + ctx.index(sent) + len(sent) - len(x) - 1  # the item ends the sentence before its period
            ids[v] = list(enc["input_ids"])
            at[v] = SP.tokens_in(enc["offset_mapping"], w0, w0 + len(x))
            ends[v] = max(SP.tokens_in(enc["offset_mapping"], c0, c0 + len(ctx)))
        if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
            return None, "the bridge is not one token at the same index in O and S"
        if pos is not None and at["org"][0] != pos:
            return None, "the conditions' bridge positions differ"
        pos = at["org"][0]
        if ends["org"] != ends["alt"] or (through is not None and ends["org"] != through):
            return None, "the passage does not end at one token index in O, S and every condition"
        through = ends["org"]
        tokens = {src: {v: S.answer_token(tok, str(d), "digit") for v, d in zip(("org", "alt"), answers[src], strict=True)}
                  for src in INSTRUCTED}  # fmt: skip
        own = cond if cond in INSTRUCTED else "text"  # none: no instructed answer; its answer fields follow the text
        readers[cond] = {"question": q, "instruction": INSTRUCTION[cond], "ids": ids,
                         "answer": str(answers[own][0]), "cf_answer": str(answers[own][1]),
                         "tok_A": tokens[own]["org"], "tok_b": tokens[own]["alt"], "tokens": tokens,
                         "read_index": len(ids["org"])}  # fmt: skip
    assert through is not None  # every condition encoded
    assert pos is not None
    base = readers["none"]["ids"]
    for cond in INSTRUCTED:
        for v in ("org", "alt"):
            if readers[cond]["ids"][v][: through + 1] != base[v][: through + 1]:
                return None, "the conditions' prompts differ within the passage"
    assert pos <= through
    return {"scene": f"{scene}-{placement}", "base_scene": scene, "placement": placement, "condition": CONDITION,
            "rendering": "chat", "domain": "animals", "bridge": a_item, "cf_bridge": bridge, "context": o,
            "cf_context": s, "pos": pos, "shared_through": through, "space": S.ids(tok, " "), "readers": readers}, ""  # fmt: skip


def build(tok, n_gen: int = R.N_GEN, placements: tuple[str, ...] = PLACEMENTS, condition: str = CONDITION):
    """Every case: the routes test's scenes of `condition` (x6_routes.scenes, its stream), each with its attribute
    sentences in each placement (paired: a base scene that fails in one placement is dropped in all). Drops counted."""
    legs, _, _ = R.pools(tok)
    cases, dropped = R.scenes(tok, n_gen)
    out = []
    for c in (c for c in cases if c["condition"] == condition):
        rng = random.Random(f"{SEED}|{c['scene']}")
        plan = attribute_plan(c["context"], c["cf_context"], legs, rng)
        if plan is None:
            dropped["no three false digits outside the locker digits and the true legs"] += 1
            continue
        attrs = [attribute_sentence(x, plan["false"][x]) for x in plan["order"]]
        a_item, bridge, asked = c["bridge"], c["cf_bridge"], R.asked_of(c)
        answers = {"text": (plan["false"][a_item], plan["false"][bridge]), "memory": (legs[a_item], legs[bridge])}
        mine = []
        for placement in placements:
            o = with_attributes(c["context"], attrs, placement)
            s = with_attributes(c["cf_context"], attrs, placement)
            case, why = encode(tok, o, s, asked, a_item, bridge, answers, c["scene"], placement)
            if case is None:
                dropped[f"{placement}: {why}"] += 1
                break
            case.update({"legs": {x: legs[x] for x in plan["false"]}, "false": plan["false"],
                         "attribute_order": plan["order"], "locker_order": [x for x, _ in locker_slots(c["context"])],
                         "answers": {k: list(v) for k, v in answers.items()}, "expect": c["expect"],
                         "base_pos": c["pos"]})  # fmt: skip
            mine.append(case)
        else:
            out += mine
    return out, dropped


def check_case(c: dict) -> None:
    """Dumbest way 1, on a built case: the bridge at one index in every condition and in O and S, the conditions
    sharing the passage's tokens, the four answer digits distinct, the false digits outside the locker digits and the
    true legs; in placement after, the bridge index is the routes scene's."""
    ids = {cond: rd["ids"] for cond, rd in c["readers"].items()}
    t = c["shared_through"]
    for cond in CONDS:
        assert len(ids[cond]["org"]) == len(ids[cond]["alt"]), f"{c['scene']} {cond}: O and S differ in length"
        for v in ("org", "alt"):
            assert ids[cond][v][: t + 1] == ids["none"][v][: t + 1], f"{c['scene']} {cond}: the passage differs"
        assert ids[cond]["org"][c["pos"]] != ids[cond]["alt"][c["pos"]], (
            f"{c['scene']} {cond}: the bridge token is the same in O and S"
        )
        # after the bridge, O and S are the same prompt (the other picks, the attribute sentences, the question): a
        # C2 source differs before it (B's and C's locker sentences), a C0 source nowhere else
        assert ids[cond]["org"][c["pos"] + 1 :] == ids[cond]["alt"][c["pos"] + 1 :], (
            f"{c['scene']} {cond}: O and S differ after the bridge"
        )
        assert c["readers"][cond]["read_index"] == len(ids[cond]["org"])
    a, b = c["bridge"], c["cf_bridge"]
    four = [c["false"][a], c["false"][b], c["legs"][a], c["legs"][b]]
    assert len(set(four)) == 4, f"{c['scene']}: the answer digits are not distinct: {four}"
    taken = {d for _, d in locker_slots(c["context"])} | {d for _, d in locker_slots(c["cf_context"])}
    assert not set(c["false"].values()) & (taken | set(c["legs"].values())), f"{c['scene']}: a false digit is taken"
    assert len(set(c["false"].values())) == len(c["false"])
    if c["placement"] == DECISIVE:
        assert c["pos"] == c["base_pos"], f"{c['scene']}: the bridge index is not the routes scene's"


def marked(decode, ids: list[int], pos: int) -> str:
    return R.marked(decode, ids, pos)


def example_scenes(cases: list[dict], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify pack's items: k random base scenes (seed) of the decisive placement, in that order."""
    mine = [c["base_scene"] for c in cases if c["placement"] == DECISIVE]
    return random.Random(seed).sample(mine, min(k, len(mine)))


def prompt_lines(cases: list[dict], decode, k: int = N_PROMPTS, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random base scenes (seed): per placement and condition, O and S exactly as the model reads them (the digit's
    space token appended), the bridge word in ⟦...⟧, with the answers."""
    by = {(c["base_scene"], c["placement"]): c for c in cases}
    lines = []
    for base in example_scenes(cases, k, seed):
        for p in PLACEMENTS:
            c = by[(base, p)]
            lines += [f"## {c['scene']}: bridge {c['bridge']} -> {c['cf_bridge']} at token {c['pos']} (passage through "
                      f"token {c['shared_through']}); false legs {c['false']}, true legs {c['legs']}; attribute order "
                      f"{c['attribute_order']}, locker order {c['locker_order']}", ""]  # fmt: skip
            for cond, rd in c["readers"].items():
                lines += [f"### {cond}: O answers {rd['answer']}, S answers {rd['cf_answer']}"
                          + (" (none: the text's digits by convention)" if cond == "none" else "")
                          + f"; read index {rd['read_index']}", "", "O:", "", "```",
                          marked(decode, rd["ids"]["org"] + c["space"], c["pos"]), "```", "", "S:", "", "```",
                          marked(decode, rd["ids"]["alt"] + c["space"], c["pos"]), "```", ""]  # fmt: skip
    return lines


def stage_plan(out: Path | None, n_gen: int = R.N_GEN, condition: str = CONDITION) -> dict:
    """Tokenizer only: the cases, drops, checks, where the identity means are known, and the rendered prompts."""
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    target = pins.TARGET
    cases, dropped = build(tok, n_gen, PLACEMENTS, condition)
    for c in cases:
        check_case(c)
    counts: dict[str, Any] = {"target": target, "layer": X.PREDICTED.get(target), "condition": condition, "n_gen": n_gen,
                              "cases": dict(collections.Counter(c["placement"] for c in cases)),
                              "base_scenes": len({c["base_scene"] for c in cases}), "dropped": dict(dropped),
                              "entities": len({c["bridge"] for c in cases}),
                              "bridge_index": {p: dict(collections.Counter(c["pos"] for c in cases if c["placement"] == p))
                                               for p in PLACEMENTS},
                              "read_index": {p: {cond: sorted({c["readers"][cond]["read_index"] for c in cases
                                                              if c["placement"] == p}) for cond in CONDS}
                                             for p in PLACEMENTS},
                              "false_digits": dict(collections.Counter(d for c in cases if c["placement"] == DECISIVE
                                                                       for d in c["false"].values())),
                              "checks": "check_case passed on every case (bridge index shared by O, S and the three "
                                        "conditions; the passage's tokens shared; answer digits distinct; false digits "
                                        "outside the locker digits and the true legs; placement after keeps the routes "
                                        "scene's bridge index)"}  # fmt: skip
    try:
        from scripts import x0_massmean as MM

        means = MM.entity_means(R.STATES[target])
        missing = sorted({e for c in cases for e in (c["bridge"], c["cf_bridge"]) if e not in means})
        counts["identity_means"] = {"states_run": R.STATES[target], "entities_without_mean": missing,
                                    "cases_dropped_per_placement": sum(1 for c in cases if c["placement"] == DECISIVE
                                                                        and (c["bridge"] in missing or c["cf_bridge"] in missing))}  # fmt: skip
    except Exception as e:  # the probe's states are not on this machine
        counts["identity_means"] = {"states_run": R.STATES.get(target), "unknown_here": str(e)[:200]}
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    lines = [f"# 47.15 plan on {target}: {len(cases)} cases ({counts['base_scenes']} base scenes x {len(PLACEMENTS)} "
             f"placements), {N_PROMPTS} random base scenes (seed {X.EXAMPLES_SEED}); prompts exactly as the model reads "
             "them (the read: the top token after the appended space; ⟦...⟧ the bridge word, where the change is added)",
             "", "```", json.dumps(counts, indent=1), "```", "", *prompt_lines(cases, decode)]  # fmt: skip
    print(json.dumps(counts, indent=1))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / "plan.json").write_text(json.dumps(counts, indent=1) + "\n")
        (out / "prompts.md").write_text("\n".join(lines) + "\n")
        X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
        print("wrote", out)
    return counts


# ---- reads ----------------------------------------------------------------------------------------------------------


def answer_of(top: int, tokens: dict) -> str:
    """What a read's top token is: S's text digit, S's memory digit, O's text digit, O's memory digit, or other."""
    for name, (src, v) in zip(
        ANSWERS[:4], (("text", "alt"), ("memory", "alt"), ("text", "org"), ("memory", "org")), strict=True
    ):
        if top == tokens[src][v]:
            return name
    return "other"


def source_class(top: int, tokens: dict, v: str) -> str:
    """The unedited answer's class on its own prompt (v: org reads A's digits, alt B's): text / memory / other."""
    return "text" if top == tokens["text"][v] else "memory" if top == tokens["memory"][v] else "other"


def read_fields(lg, rd: dict, decode) -> dict:
    import torch

    top = int(lg.argmax())
    p = torch.softmax(lg.float(), -1)
    t = rd["tokens"]
    own = next((cond for cond in INSTRUCTED if rd["instruction"] == INSTRUCTION[cond]), None)  # none: no own switch
    return {"top": top, "top_text": decode([top]), "answer": answer_of(top, t),
            "switched_text": int(top == t["text"]["alt"]), "switched_memory": int(top == t["memory"]["alt"]),
            "switched": int(top == t[own]["alt"]) if own else None,
            **{f"p_{k}": round(float(p[t[src][v]]), 4) for k, (src, v) in
               zip(ANSWERS[:4], (("text", "alt"), ("memory", "alt"), ("text", "org"), ("memory", "org")), strict=True)}}  # fmt: skip


def competence(model, cases: list[dict], ws, decode) -> list[dict]:
    """Unedited O and S of every condition: 8 greedy tokens (what the model says), the read's top token and its class;
    under an instruction, right (said the instructed answer) and read_right (the top token is it)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (scene)"):
            for cond, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                for i, v in enumerate(("org", "alt")):
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", c["space"], ws)
                    top = int(logits[0].argmax())
                    said = S.said(texts[i], "digit")
                    row = {"scene": c["scene"], "base_scene": c["base_scene"], "placement": c["placement"],
                           "reader": cond, "variant": v, "greedy": texts[i], "said": said, "no_digit": said is None,
                           "top": top, "top_text": decode([top]), "class": source_class(top, rd["tokens"], v),
                           "said_class": ("text" if said == str(c["answers"]["text"][i]) else
                                          "memory" if said == str(c["answers"]["memory"][i]) else "other")}  # fmt: skip
                    if cond in INSTRUCTED:
                        gold = rd["answer"] if v == "org" else rd["cf_answer"]
                        row.update(
                            {"right": said == gold, "read_right": top == (rd["tok_A"] if v == "org" else rd["tok_b"])}
                        )
                    rows.append(row)
    return rows


def follow_shares(mine: list[dict], right: dict) -> dict:
    """Dumbest way 3, per instruction and variant over the placement's candidate scenes: the share of unedited reads
    whose top token is the instructed source's digit, the other source's, neither; and the share of greedy texts with
    no digit."""
    out: dict[str, Any] = {}
    for cond in INSTRUCTED:
        other = "memory" if cond == "text" else "text"
        out[cond] = {}
        for v in ("org", "alt"):
            rows = [right[(c["scene"], cond, v)] for c in mine]
            n = max(len(rows), 1)
            out[cond][v] = {"n": len(rows), "instructed": sum(r["class"] == cond for r in rows) / n,
                            "other_source": sum(r["class"] == other for r in rows) / n,
                            "neither": sum(r["class"] == "other" for r in rows) / n,
                            "no_digit": sum(bool(r["no_digit"]) for r in rows) / n}  # fmt: skip
    return out


def gate_and_eligible(cases: list[dict], comp: list[dict], placements: tuple[str, ...] = PLACEMENTS,
                      gate_min: float = X.GATE) -> tuple[dict, dict[str, list[dict]]]:  # fmt: skip
    """Per placement: the gate (O's unedited read right in >= gate_min of the candidate scenes under each instruction),
    the refusal shares, and the eligible cases (O and S said and read right under both instructions), in order."""
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate, eligible = {}, {}
    for p in placements:
        mine = [c for c in cases if c["placement"] == p]
        acc = {cond: float(np.mean([right[(c["scene"], cond, "org")]["read_right"] for c in mine])) if mine else 0.0
               for cond in INSTRUCTED}  # fmt: skip
        ok = [c for c in mine if all(right[(c["scene"], cond, v)]["right"] and right[(c["scene"], cond, v)]["read_right"]
                                     for cond in INSTRUCTED for v in ("org", "alt"))]  # fmt: skip
        gate[p] = {"cases": len(mine), "org_read_accuracy": acc, "gate": gate_min,
                   "pass": bool(mine) and all(a >= gate_min - EPS for a in acc.values()), "eligible": len(ok),
                   "follows": follow_shares(mine, right)}  # fmt: skip
        eligible[p] = ok if gate[p]["pass"] else []
    return gate, eligible


def unedited_classes(comp: list[dict]) -> dict[str, dict]:
    """Per scene and condition, the class of the unedited O and S answers (text / memory / other)."""
    out: dict[str, dict] = collections.defaultdict(dict)
    for r in comp:
        out[r["scene"]].setdefault(r["reader"], {})[r["variant"]] = r["class"]
    return dict(out)


# ---- GPU ------------------------------------------------------------------------------------------------------------


def parts_and_arms(x, jdic, alf, means: dict, chosen: list[dict], basis) -> tuple[dict, dict, dict]:
    """The J++ part and the U + I part of each row of x (the changes), their random twins, the arms (EDIT_ARMS order),
    and per-row shares (J++, U + I, U alone, I alone, the random twins)."""
    import torch

    from scripts import statement_positions as SP

    jpp = X.fit(jdic, x, X.K_MAIN, "signed").float()
    _, u_out, _ = R.identity_dirs(means, [(c["bridge"], c["cf_bridge"]) for c in chosen], jdic, x, X.K_MAIN)
    ui = R.span_part(x, [torch.cat([alf, u_out[i : i + 1].T], 1) for i in range(len(chosen))])
    extra = {"alf": (x @ alf) @ alf.T, "idout": R.rank1_part(x, u_out)}
    parts = {"jpp": jpp, "ui": ui}
    share = lambda v: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)  # noqa: E731
    sh = {k: share(v) for k, v in {**parts, **extra}.items()}
    rand = {k: SP.random_subspace_part(x, sh[k], basis) for k in parts}
    sh.update({f"{k}_rand": share(v) for k, v in rand.items()})
    arms = {"whole": x, "no_jpp": x - jpp, "no_jpp_rand": x - rand["jpp"], "no_ui": x - ui, "no_ui_rand": x - rand["ui"],
            "keep_jpp": jpp, "keep_jpp_rand": rand["jpp"], "keep_ui": ui, "keep_ui_rand": rand["ui"]}  # fmt: skip
    assert tuple(arms) == EDIT_ARMS
    return parts, arms, sh


def stage_run(name: str, why: str, n_gen: int = R.N_GEN, n_items: int = R.N_ITEMS,
              placements: tuple[str, ...] = PLACEMENTS, gate_min: float = X.GATE, condition: str = CONDITION) -> Path:  # fmt: skip
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.15 renders chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"47.15 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": TEST,
         "spec": f"{SPEC} ({TEST}, amendment 5)", "question": f"{QUESTION} ({PREDICTIONS})", "layer": layer,
         "condition": condition, "scenes": f"x6_routes.scenes seed {R.SEED}, {n_gen} per condition, the {condition} ones",
         "placements": list(placements), "decisive_placement": DECISIVE, "conditions": list(CONDS),
         "instruction": INSTRUCTION, "instruction_position": "the user turn, after the question and before X0's digit "
         "instruction; the three conditions share every token through the end of the passage (asserted per scene)",
         "attributes": f"one false-legs sentence per locker item; digits 1-9 outside O's and S's locker digits and every "
         f"item's true legs, distinct; seed {SEED} with the scene id; order seeded, independent of the locker order",
         "arms": ARM_TEXT, "k": X.K_MAIN, "omp": "signed", "pointer": f"U = x0_massmean Alf of {R.STATES[target]} (never refit)",
         "identity": f"I = mu_B - mu_A (x0_massmean entity_means of {R.STATES[target]}) orthogonalized against the "
         "scene's 25 J++ atoms (x6_routes.identity_dirs idout); U + I part = x6_routes.span_part on [U, I]",
         "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at each part's share of ||Δ||^2",
         "gate": gate_min, "n_items": n_items, "items_rule": "per placement: the first n_items eligible scenes in "
         "generator order whose bridge entities both have class means; eligible = O and S said and read right under "
         "both instructions; a placement whose gate fails has no items",
         "read": "X0's chat read: the top token after a space token appended; switch = S's answer under the condition",
         "switch": {"text": "the changed item's false digit", "memory": "the changed item's true legs",
                    "none": "per class of the unedited O and S answers (verdict)"},
         "rule": RULE, "seeds": {"scenes": R.SEED, "attributes": SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer",
                                 "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "order": "scenes in generator order; per scene, condition: competence (O and S generated together, each read "
                  "alone); Δ per scene unbatched; reads per scene and condition: the unedited row then the arms in "
                  "EDIT_ARMS order in one batch, then S alone",
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    cases, dropped = build(tok, n_gen, placements, condition)
    for c in cases:
        check_case(c)
    ws = X.whitespace_mask(model)
    comp = competence(model, cases, ws, decode)
    gate, eligible = gate_and_eligible(cases, comp, placements, gate_min)
    ent_means = MM.entity_means(R.STATES[target])
    chosen, id_dropped = [], {}
    for p in placements:
        ok = [c for c in eligible[p] if c["bridge"] in ent_means and c["cf_bridge"] in ent_means]
        id_dropped[p] = len(eligible[p]) - len(ok)
        chosen += ok[:n_items]
    classes = unedited_classes(comp)
    picked = {c["scene"] for c in chosen}
    for c in cases:
        c["unedited_class"] = classes[c["scene"]]
        c["chosen"] = c["scene"] in picked
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    plan = {"dropped": dict(dropped), "gate": gate, "identity_dropped": id_dropped,
            "items": {p: sum(c["placement"] == p for c in chosen) for p in placements},
            "entities": {p: len({c["bridge"] for c in chosen if c["placement"] == p}) for p in placements}}  # fmt: skip
    (out / "gate.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(
        json.dumps({k: v for k, v in plan.items() if k != "gate"} | {"gate": {p: g["pass"] for p, g in gate.items()}}),
        flush=True,
    )
    if not chosen:
        raise SystemExit("no placement passed the gate fixed in advance (or none had eligible items); see gate.json")
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    alf = alf.to(jdic.device)
    means = {e: torch.tensor(v, dtype=torch.float32, device=jdic.device) for e, v in ent_means.items()}
    examples = set(example_scenes(chosen))
    rows, norms, greedy = [], [], []
    with torch.no_grad():
        deltas = []
        for c in progress(chosen, "Δ at the bridge word (item)"):
            ids = c["readers"]["none"]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][c["pos"]]
                 for v in ("org", "alt")}  # fmt: skip
            deltas.append((h["alt"] - h["org"]).float().to(jdic.device))
        x = torch.stack(deltas)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(x.device)
        _, arms, sh = parts_and_arms(x, jdic, alf, means, chosen, basis)
        for i, c in enumerate(progress(chosen, f"reads at layer {layer} (item)")):
            norms.append({"scene": c["scene"], "base_scene": c["base_scene"], "placement": c["placement"],
                          "norm": round(float(x[i].norm()), 4),
                          **{f"share_{k}": round(float(v[i]), 5) for k, v in sh.items()}})  # fmt: skip
            for cond, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in EDIT_ARMS]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                s_logits, _ = X.read_logits(model, rd["ids"]["alt"], [{}], "chat", c["space"], ws)
                for arm, lg in zip(ARMS, [*logits, s_logits[0]], strict=True):
                    rows.append({"scene": c["scene"], "base_scene": c["base_scene"], "placement": c["placement"],
                                 "entity": c["bridge"], "reader": cond, "arm": arm, **read_fields(lg, rd, decode)})  # fmt: skip
                if c["base_scene"] in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, edits)
                    s_text = model.generate_batch(
                        torch.tensor([rd["ids"]["alt"]], device=model.device), X.GEN_TOKENS, [{}]
                    )
                    greedy += [{"scene": c["scene"], "reader": cond, "arm": arm, "greedy": t}
                               for arm, t in zip(ARMS, [*texts, *s_text], strict=True)]  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    m["items"] = plan["items"]
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- the gate (CPU, unsealed) ---------------------------------------------------------------------------------------


def competence_lines(name: str) -> list[str]:
    """A run's gate and refusal shares (not a result: the gate decides whether the test is read at all)."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    g = json.loads((src / "gate.json").read_text())
    lines = [f"# 47.15 competence: {name} ({m['model']['target']}, L{m['layer']})", "",
             f"Gate {m['gate']} per instruction on O's unedited read over every candidate scene. Dropped at build: "
             f"{g['dropped'] or 'none'}. Identity means missing: {g['identity_dropped']}. Items: {g['items']} "
             f"(bridge entities {g['entities']}).", "",
             "| placement | cases | text O read right | memory O read right | pass | eligible |", "|---|---|---|---|---|---|"]  # fmt: skip
    for p, v in g["gate"].items():
        acc = v["org_read_accuracy"]
        lines.append(f"| {p} | {v['cases']} | {acc.get('text', float('nan')):.3f} | {acc.get('memory', float('nan')):.3f} | "
                     f"{'yes' if v['pass'] else 'no'} | {v['eligible']} |")  # fmt: skip
    lines += ["", "Refusal share (dumbest way 3; unedited reads over every candidate scene): the top token follows the "
              "instruction / the other source / neither; greedy text with no digit.", "",
              "| placement | instruction | prompt | n | instructed | other source | neither | no digit |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for p, v in g["gate"].items():
        for cond, by in v["follows"].items():
            for var, f in by.items():
                lines.append(f"| {p} | {cond} | {'O' if var == 'org' else 'S'} | {f['n']} | {f['instructed']:.3f} | "
                             f"{f['other_source']:.3f} | {f['neither']:.3f} | {f['no_digit']:.3f} |")  # fmt: skip
    return lines


def stage_competence(name: str) -> None:
    print("\n".join(competence_lines(name)))


# ---- verdict (CPU, sealed) ------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    return A.dan_answer(QUESTION, rev)


def item_table(rows: list[dict], placement: str, cond: str, key: str,
               keep: set[str] | None = None) -> tuple[list[str], list[str], dict[str, list[int]]]:  # fmt: skip
    """One condition's items of a placement (row order; `keep`: these scenes only), their bridge entities and each
    arm's 0/1 switch (switched_<key>); every item must have every arm."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["placement"] == placement and r["reader"] == cond and (keep is None or r["scene"] in keep):
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r[f"switched_{key}"])
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in ARMS if (s, a) not in by]
    assert not missing, f"{placement} {cond}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    return scenes, [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in ARMS}


def numbers(switched: dict[str, list[int]], entities: list[str], n_boot: int = X.N_BOOT,
            seed: int = X.BOOT_SEED) -> dict[str, Any]:  # fmt: skip
    """Each arm's switch rate, each part's loss without it and without its random twin, and the extra loss, with 95%
    percentile CIs from X0's paired cluster bootstrap over the bridge entities; the cell's validity (X0's)."""
    n = len(entities)
    hits = {a: int(sum(switched[a])) for a in ARMS}
    if n == 0:
        return {"n": 0, "entities": 0, "hits": hits, "valid": False, "rate": {}, "loss": {}, "extra": {}}
    boot = X.resampled_rates(switched, entities, n_boot, seed)
    s = {a: hits[a] / n for a in ARMS}
    out: dict[str, Any] = {"n": n, "entities": len(set(entities)), "hits": hits,
                           "valid": bool(s["whole"] >= X.VALID_S - EPS and hits["whole"] >= X.VALID_N),
                           "rate": {a: [s[a], *X.interval(boot[a])] for a in ARMS}, "loss": {}, "extra": {}}  # fmt: skip
    for part, no, rand in PARTS:
        l_no, l_rand = X.dependence(s["whole"], s[no]), X.dependence(s["whole"], s[rand])
        b_no, b_rand = X.dependence(boot["whole"], boot[no]), X.dependence(boot["whole"], boot[rand])
        out["loss"][part] = {
            "no_part": [float(l_no), *X.interval(b_no)],
            "no_rand": [float(l_rand), *X.interval(b_rand)],
        }
        out["extra"][part] = [float(l_no - l_rand), *X.interval(b_no - b_rand)]
    return out


def label(num: dict[str, Any]) -> str:
    """lookup / recall / neither on a condition's numbers (point estimates, EPS); can't tell on an invalid cell."""
    if not num.get("valid"):
        return "can't tell"
    j, u = num["extra"]["jpp"][0], num["extra"]["ui"][0]
    if j <= LOOKUP_JPP_MAX + EPS and u >= LOOKUP_UI_MIN - EPS:
        return "lookup"
    if j >= RECALL_JPP_MIN - EPS and u <= RECALL_UI_MAX + EPS:
        return "recall"
    return "neither"


def model_rule(labels: dict[str, str]) -> dict[str, Any]:
    """47.15 on one model's text and memory labels."""
    t, mm = labels["text"], labels["memory"]
    if t == "lookup" and mm == "recall":
        verdict = "follows the source"
    elif t == mm and t in ("lookup", "recall"):
        verdict = "follows the question"
    else:
        verdict = "neither"
    return {"status": "tested", "verdict": verdict, "labels": labels,
            "why": f"from the text: {t}; from memory: {mm}"}  # fmt: skip


def batch_rule(models: list[dict]) -> dict[str, Any]:
    """The batch: 'follows the source' on >= MODELS_MIN models; else 'follows the question' on >= MODELS_MIN; pending
    while enough models are missing to still reach a label; else neither."""
    n = {k: sum(m.get("verdict") == k for m in models) for k in ("follows the source", "follows the question")}
    pending = sum(m["status"] == "pending" for m in models)
    for k in ("follows the source", "follows the question"):
        if n[k] >= MODELS_MIN:
            return {"label": k, "counts": n, "pending": pending}
    if any(n[k] + pending >= MODELS_MIN for k in n):
        return {"label": "pending", "counts": n, "pending": pending}
    return {"label": "neither", "counts": n, "pending": pending}


def class_shares(rows: list[dict], cases: dict[str, dict], placement: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """No instruction, the chosen items of a placement: the class shares of the unedited O answers (arm none) and S
    answers (arm source), cluster-bootstrap CIs; the preferred source = the larger of text and memory on O."""
    out: dict[str, Any] = {}
    for arm, var in (("none", "org"), ("source", "alt")):
        mine = [r for r in rows if r["placement"] == placement and r["reader"] == "none" and r["arm"] == arm]
        ents = [r["entity"] for r in mine]
        if not mine:
            out[var] = {"n": 0}
            continue
        sw = {
            k: [int(cases[r["scene"]]["unedited_class"]["none"][var] == k) for r in mine]
            for k in ("text", "memory", "other")
        }
        boot = X.resampled_rates(sw, ents, n_boot)
        out[var] = {"n": len(mine), **{k: [float(np.mean(v)), *X.interval(boot[k])] for k, v in sw.items()}}
    o = out["org"]
    out["prefers"] = (
        ("text" if o["text"][0] > o["memory"][0] else "memory" if o["memory"][0] > o["text"][0] else "tie")
        if o["n"]
        else None
    )
    return out


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending (not here), not tested (the decisive placement's gate failed), or its numbers per
    placement and condition, the rule on the decisive placement, the no-instruction check and the preference."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in {**RUNS, **COVERAGE_RUNS}.items()}.get(run)
        assert target, f"no 47.15 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    g = json.loads((src / "gate.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    res: dict[str, Any] = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "gate": g, "placements": {}}
    for p in m["placements"]:
        if not g["gate"][p]["pass"]:
            res["placements"][p] = {"status": "not tested", "why": "the gate failed"}
            continue
        conds = {}
        for cond in INSTRUCTED:
            _, ents, sw = item_table(rows, p, cond, cond)
            conds[cond] = numbers(sw, ents, n_boot)
            conds[cond]["label"] = label(conds[cond])
        none: dict[str, Any] = {"classes": class_shares(rows, cases, p, n_boot)}
        for k in INSTRUCTED:
            keep = {s for s, c in cases.items() if c["placement"] == p and c.get("chosen")
                    and c["unedited_class"]["none"]["org"] == k and c["unedited_class"]["none"]["alt"] == k}  # fmt: skip
            _, ents, sw = item_table(rows, p, "none", k, keep)
            none[k] = numbers(sw, ents, n_boot)
            none[k]["label"] = label(none[k])
            none[k]["matches_instructed"] = none[k]["label"] == conds[k]["label"]
        res["placements"][p] = {"status": "tested", **model_rule({c: conds[c]["label"] for c in INSTRUCTED}),
                                "conditions": conds, "none": none}  # fmt: skip
    d = res["placements"][DECISIVE]
    res.update({"status": d["status"], "verdict": d.get("verdict"), "why": d["why"]})
    norms = X.read_jsonl(src / "norms.jsonl")
    res["shares_median"] = {k: round(float(np.median([n[f"share_{k}"] for n in norms if n["placement"] == DECISIVE])), 5)
                            for k in ("jpp", "ui", "alf", "idout", "jpp_rand", "ui_rand")
                            if any(f"share_{k}" in n for n in norms)}  # fmt: skip
    return res


def fmt(v) -> str:
    if not v or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def verdict_lines(models: list[dict], batch: dict, answer: str, n_boot: int) -> list[str]:
    lines = ["# 47.15: one question, two sources. Does the part follow the source or the question?", "",
             f"Batch 47, test 47.15 (jobs/c3/batch47.yaml, amendment 5; {QUESTION}, Dan: {answer}). Routes scenes "
             "(locker-first) with a false-legs sentence per item; one question under two instructions (from the text / "
             "from memory) and none; the change at the bridge word at L: whole, without J++ / without U + I, each "
             "against a random part of its share, and only J++ / only U + I. Extra loss = (1 − S_no_part / S_whole) − "
             f"(1 − S_no_rand / S_whole); cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.",
             "", f"Rule (fixed in advance): {RULE}.", "",
             f"**Batch: {batch['label']}** (follows the source on {batch['counts']['follows the source']}, the question "
             f"on {batch['counts']['follows the question']} of {len(models)} models; pending {batch['pending']}).", "",
             "| model | run | status | verdict (placement after) | text: n, S_whole | text: extra loss J++ | text: extra "
             "loss U + I | text label | memory: n, S_whole | memory: extra loss J++ | memory: extra loss U + I | memory "
             "label |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m.get('target', '-')} | {m['run']} | {m['status']} ({m['why']}) | | | | | | | | | |")
            continue
        d = m["placements"][DECISIVE]["conditions"]
        cells = []
        for cond in INSTRUCTED:
            c = d[cond]
            cells += [f"{c['n']}, {fmt(c['rate']['whole'])}", fmt(c["extra"]["jpp"]), fmt(c["extra"]["ui"]), c["label"]]
        lines.append(f"| {m['target']} | {m['run']} | tested | {m['verdict']} | " + " | ".join(cells) + " |")
    lines += ["", "Every arm's switch rate (the top token is S's answer under the condition), both placements:", "",
              "| model | placement | condition | " + " | ".join(ARMS) + " |", "|---|---|---|" + "---|" * len(ARMS)]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for p, pr in m["placements"].items():
            if pr["status"] != "tested":
                lines.append(
                    f"| {m['target']} | {p} | not tested ({pr['why']}) | " + " | ".join("" for _ in ARMS) + " |"
                )
                continue
            for cond in INSTRUCTED:
                c = pr["conditions"][cond]
                lines.append(f"| {m['target']} | {p} | {cond} | " + " | ".join(fmt(c["rate"][a]) for a in ARMS) + " |")
            for k in INSTRUCTED:
                c = pr["none"][k]
                lines.append(f"| {m['target']} | {p} | none, class {k} (n {c['n']}) | "
                             + " | ".join(fmt(c["rate"].get(a)) for a in ARMS) + " |")  # fmt: skip
    lines += ["", "Placement before (dumbest way 2, reported) and the no-instruction check (descriptive): the labels.", "",
              "| model | placement | text label | memory label | verdict | none: text class n, label, matches | none: "
              "memory class n, label, matches | none: O prefers (text / memory / other) |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for p, pr in m["placements"].items():
            if pr["status"] != "tested":
                lines.append(f"| {m['target']} | {p} | not tested | | | | | |")
                continue
            nn = pr["none"]
            cl = nn["classes"]["org"]
            pref = (
                f"{nn['classes']['prefers']} ({fmt(cl['text'])} / {fmt(cl['memory'])} / {fmt(cl['other'])})"
                if cl["n"]
                else "-"
            )
            lines.append(f"| {m['target']} | {p} | {pr['labels']['text']} | {pr['labels']['memory']} | {pr['verdict']} | "
                         f"{nn['text']['n']}, {nn['text']['label']}, {'yes' if nn['text']['matches_instructed'] else 'no'} | "
                         f"{nn['memory']['n']}, {nn['memory']['label']}, {'yes' if nn['memory']['matches_instructed'] else 'no'} | "
                         f"{pref} |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "",
              "Gates, refusal shares and shares (descriptive):", ""]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        g = m["gate"]
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): items {g['items']} (entities {g['entities']}); gate "
                     + "; ".join(f"{p}: text {v['org_read_accuracy'].get('text', 0):.3f}, memory "
                                 f"{v['org_read_accuracy'].get('memory', 0):.3f} ({'pass' if v['pass'] else 'fail'}; "
                                 f"eligible {v['eligible']} of {v['cases']})" for p, v in g["gate"].items())
                     + f"; identity means missing {g['identity_dropped']}; dropped at build {g['dropped'] or 'none'}; "
                     f"median shares of ||Δ||^2 (after) {m.get('shares_median')}; refusal (after, O): "
                     + ", ".join(f"{cond}: instructed {f['org']['instructed']:.2f}, other source "
                                 f"{f['org']['other_source']:.2f}, no digit {f['org']['no_digit']:.2f}"
                                 for cond, f in g["gate"][DECISIVE]["follows"].items()))  # fmt: skip
    return lines


def example_lines(run: str, decode, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify pack: k random items (seed) of the decisive placement; per condition O as read with the bridge word
    marked, S, and every arm's answer (the top token, what it is, switched) and greedy text."""
    src = RESULTS / run
    cases = [c for c in X.read_jsonl(src / "cases.jsonl") if c.get("chosen")]
    by = {c["scene"]: c for c in cases}
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    picked = example_scenes(cases, k, seed)
    lines = [f"## {run}: {len(picked)} random items of {sum(c['placement'] == DECISIVE for c in cases)} (seed {seed}), "
             f"placement {DECISIVE}", ""]  # fmt: skip
    for base in picked:
        c = by[f"{base}-{DECISIVE}"]
        lines += [f"### {c['scene']}: bridge {c['bridge']} -> {c['cf_bridge']} at token {c['pos']}; false legs "
                  f"{c['false']}, true legs {c['legs']}; unedited classes {c['unedited_class']}", ""]  # fmt: skip
        for cond, rd in c["readers"].items():
            lines += [f"**{cond}** ({rd['instruction'] or 'no instruction'}): O answers {rd['answer']}, S answers "
                      f"{rd['cf_answer']}" + (" (none: the text's digits by convention)" if cond == "none" else ""), "",
                      "O, as read:", "", "```", marked(decode, rd["ids"]["org"], c["pos"]), "```", "",
                      "S (the source):", "", "```", marked(decode, rd["ids"]["alt"], c["pos"]), "```", "",
                      "| arm | what | top token | is | switched (text / memory) | greedy |", "|---|---|---|---|---|---|"]  # fmt: skip
            for arm in ARMS:
                r = reads[(c["scene"], cond, arm)]
                lines.append(f"| {arm} | {ARM_TEXT[arm]} | {r['top_text']!r} | {r['answer']} | {r['switched_text']} / "
                             f"{r['switched_memory']} | {greedy.get((c['scene'], cond, arm))!r} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, decode_for=None, coverage: bool = False) -> Path:
    """47.15's verdict (sealed until Q47.15), or with coverage (batch 52 C) the same rules on the given coverage runs
    alone: no seal guard, "no prediction" in place of Dan's answer, no pending rows, written to x52_source-<UTC>/."""
    answer = (f"{NO_PREDICTION}; rules first scored in {SCORED}; the batch count covers the given runs only, not "
              "re-scored") if coverage else dan_answer()  # fmt: skip
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    known = set(COVERAGE_RUNS) if coverage else set(RUNS)
    assert set(targets) <= known, f"47.15 runs on {sorted(known)}, not {sorted(set(targets) - known)}"
    if not coverage:
        models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"}
                   for t in MODELS if t not in targets]  # fmt: skip
    batch = batch_rule(models)
    out = RESULTS / f"{'x52_source' if coverage else 'x47_15'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, batch, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ") for ln in lines]
    (out / "x47_15.json").write_text(json.dumps({"runs": runs, "dan": answer, "batch": batch, "models": models}, indent=1)
                                     + "\n")  # fmt: skip
    (out / "x47_15.md").write_text("\n".join(lines) + "\n")
    ex = ["# 47.15 verify pack: prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the "
          "bridge word, where the change (or the arm's part of it) is added at L. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"], (decode_for or A.default_decode)(m["target"]))
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "competence", "verdict"])
    ap.add_argument("--name", help="run / competence: the run name (results/x47_source/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 47.15 runs (27B, 9B, Muse)")
    ap.add_argument("--why", default=f"batch 47, test {TEST} ({SPEC}, amendment 5; {QUESTION})")
    ap.add_argument("--out", type=Path, help="plan: where to write plan.json, prompts.md and cases.jsonl")
    ap.add_argument("--n-gen", type=int, default=R.N_GEN, help="scenes generated per condition (x6_routes: 700)")
    ap.add_argument("--n-items", type=int, default=R.N_ITEMS)
    ap.add_argument("--condition", default=CONDITION, choices=("C0", "C2"))
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.out, a.n_gen, a.condition)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.n_gen, a.n_items, condition=a.condition)
    elif a.stage == "competence":
        assert a.name, "competence needs --name"
        stage_competence(a.name)
    else:
        stage_verdict(a.runs, a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
