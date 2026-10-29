"""x53_2x2 (batch 53, test 53.1; jobs/c3/batch53.yaml `brief:`, rules fixed there before any run; no prediction): the
2x2, question position x answer type, on our locker scenes (the main test: x0_necessity, d1_topics_v3, the alt "cf" =
two people swap picks, chat rendering, X0's gate 0.80 per reader, >= 150 eligible, the first 200 in scene order).

Cells (the lookup's question, "Which locker belongs to <person>'s pick?", and its digit read are the same in every
cell):

  qa_num   (Q-after, number)  the main test as is: user turn "<scene>\\n<question> <digit instruction>" (tasks_v2.render,
           byte for byte), the assistant turn prefilled "Answer:"; X0's chat read (top token after a digit's space
           token). The readers' prompts agree through the bridge word: one Δ, from the lookup's prompts (X0's design).
  qb_num   (Q-before, number) the same scenes with each reader's question placed before the scene: user turn
           "Question: <question> <digit instruction>\\n\\nScene:\\n<scene>" (Dan's "Question: ... Scene: ..."; 47.7 (a)'s
           question-first layout with the brief's "Scene:" label; the newline before the scene keeps its tokens those of
           Q-after, where it opens the turn: "Scene: <scene>" would change its first token, " Peter" for "Peter"); digits
           kept. Both readers' questions move, each in its own prompt (the conservative reading of "both questions": one
           question per prompt, as 47.7 (a) and batch 52's question-first item; one prompt holding both questions would
           need a new line after the scene saying which to answer). The readers' prompts now differ before the bridge
           word, so each reader's Δ comes from its own O / S prompts (47.7 (a)).
  qa_word  (Q-after, word)    the recall asks for a one-token word answer instead of the number (RELATION below); its
           question as in the main test, its instruction WORD_INSTRUCTION; read right after "Answer:" (no space token:
           the word's token carries its own space, as suite_v1); lookup unchanged. One Δ from the lookup's prompts.
  qb_word  (Q-before, word)   both changes; per-reader Δ.

Relation (the brief: chosen on the 9B before any test: one-token answers, the 9B's accuracy >= 0.8, the answer word
shares no token with any spelling, initial or symbol of the item = x52_atoms' bridge classes). Candidates, fixed before
any run, in order: lexical relations per domain (LEXICAL: animals' class and young, elements' state at room temperature,
Greek letters' vowel / consonant), then the number written as a word ("six" for 6). A candidate is admissible when every
answer it gives on the scenes is one token after a space, no token of any variant of the answer word (as is, leading
space, capitalised, both) matches the item's bridge classes (x52_atoms.entity_matcher(spell=True): key, first token,
symbol / character / translation alias, prefix, initial, part), and it covers >= X0's N_MIN (150) scenes (both bridges
answered, the O and S answers' first tokens differ: X0's drop rule); the 9B's accuracy is the (Q-after, word) recall's
org read accuracy over all its scenes (that cell's gate, measured in the run before any arm is read; < 0.80 = the word
cells not tested). `plan` computes the table on the tokenizer: on these scenes no lexical candidate (nor all of them
pooled) covers 150 scenes, so the rule picks the number word. Dumbest way this could be wrong: the number word is the
same relation as the digit, so the word cells change only what the reader outputs (a letter token, inside the lens's
dictionary, instead of a digit, outside it); the lens's answer directions A (51.12: the number words) are the same in
all four cells.

Per cell (the cell's own gate first; a failed gate = "not tested (gate x < 0.80)", numbers descriptive only, never
lowered):
  gate     X0's competence and gate on the cell's prompts (unedited O and S, 8 greedy tokens and the decisive read; gate
           = O read accuracy >= 0.80 per reader over all scenes; eligible = both readers say and read O and S right; >=
           150 eligible; the first 200 in scene order; Lightning: its 60 dev scenes left out of the eligible ones after
           the gate, as its main test nem35l_x52_conflict did, DEV_GATE). Word answers: said = the first word of the first line,
           lower-cased, equal to the number word; read = the top token is the word's first token with a leading space,
           lower-case or capitalised (" six" / " Six").
  conflict X0's test at L (9B L12, 27B L32, Lightning L14 = x51_lightning.py layer): Δ = h_S - h_O at the bridge word;
           arms whole / without the J++ part (signed OMP, K = 25, J++ letter atoms; x0_necessity.fit) / without a random
           part of its share (x6_routes.removal_arms over X0's random basis, seed 888 + L); X0's cell numbers (excess =
           extra loss beyond random, cluster bootstrap over the bridge entity, 10,000, seed 0) and label per reader.
  51.12    x51_answer's arms (the same forwards): the readout check first (the lens rank of each reader's own answer word,
           A-style variants, at the edited token on O and S; not read = rank > 50 on both), then arm 1 no_jpp, arm 2
           no_jpp_A (A projected out of the J++ part), arm 3 no_A, each against its random twin; A = the number words of
           both readers' O and S answers (51.12's E1 construction, all four cells). Label per reader: x51_answer.rule
           and the readout case (51.12's labels: entity / answer / mixed / answer word not read; e1 <= 0 = can't tell).
           The cell's label is the recall's (51.12's decisive E1 reader); the lookup's beside.
  atoms    batch 52 A's inventory on 50 of the cell's items (seed 0, x52_atoms.pick): the K = 25 OMP atoms of Δ
           (x52_atoms.omp_atoms) classified by x52_atoms' classifier (E1 contexts; Q-after: the lookup's Δ in both
           readers' views; Q-before: each reader's own Δ in its own view); descriptive.

Rule across cells (verbatim, batch53.yaml): "position": (Q-before, number) is answer or mixed and (Q-after, word) is
entity; "readability": (Q-after, word) is answer or mixed and (Q-before, number) is entity; "both": each single change
gives mixed and (Q-before, word) gives answer; "neither": all four entity. Cross-check, decisive for the story: the
conflict test's lookup loses <= 0.10 beyond random in all four cells ("the pointer does not depend on the question");
reported per cell. A cell not tested or with another label: the patterns that need it can't be read.

uv run python scripts/x53_2x2.py plan                                                   # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_2x2.py run --name qwen35_9b_x53_2x2        # GPU
uv run python scripts/x53_2x2.py verdict                                                # CPU, every model's run
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x53_2x2"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
SET = "d1_topics_v3"  # the main test's scenes (x45b_binding.MAIN_RUN's set)
NO_PREDICTION = "no prediction (batch 53: exploration day, rules fixed in the brief)"
CELLS = ("qa_num", "qb_num", "qa_word", "qb_word")
CELL = {"qa_num": ("after", "number"), "qb_num": ("before", "number"), "qa_word": ("after", "word"),
        "qb_word": ("before", "word")}  # fmt: skip
CELL_TEXT = {"qa_num": "(Q-after, number)", "qb_num": "(Q-before, number)", "qa_word": "(Q-after, word)",
             "qb_word": "(Q-before, word)"}  # fmt: skip
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_2x2", "qwen3.6-27b": "x53_2x2_27b", "nemotron-3.5-lightning": "nem35l_x53_2x2"}
MODEL_ORDER = ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")
MODEL_SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "nemotron-3.5-lightning": "Lightning"}
# Lightning's main test (nem35l_x52_conflict) keeps the 60 scenes its layer was fixed on out of the selection
DEV_GATE = {"nemotron-3.5-lightning": "results/x51_lightning/nem35l_x52_layer_r2/gate.json"}
WORD_INSTRUCTION = "Answer with the number written as a word and nothing else."
N_ATOMS = 50
CROSS_MAX = 0.10  # the cross-check: the lookup's extra loss beyond random <= 0.10 in every cell
GATE_TEXT = "not tested (gate {acc} < 0.80)"
EPS = 1e-9

# ---- the relation (tokenizer only) ----------------------------------------------------------------------------------

# Lexical candidates, fixed before any run (per domain: item -> its one answer word; items with no single common answer
# are left out, so a scene whose bridge or new bridge is not listed cannot carry the relation).
LEXICAL = {
    "animals": {
        "class": {**{a: "mammal" for a in ("lion", "sheep", "camel", "pig", "mouse", "wolf", "dog", "deer", "rabbit",
                                            "fox", "elephant", "goat", "cat", "cow", "tiger", "bear", "horse", "zebra",
                                            "giraffe")},
                  **{a: "bird" for a in ("crow", "chicken", "goose", "owl", "eagle", "duck", "turkey", "parrot",
                                          "penguin", "swan")},
                  **{a: "insect" for a in ("beetle", "butterfly", "bee", "fly", "ant")},
                  "frog": "amphibian", "spider": "arachnid", "scorpion": "arachnid", "tick": "arachnid"},
        "young": {"dog": "puppy", "cat": "kitten", "cow": "calf", "sheep": "lamb", "goat": "kid", "bear": "cub",
                  "lion": "cub", "tiger": "cub", "wolf": "pup", "elephant": "calf", "camel": "calf", "horse": "foal",
                  "deer": "fawn", "frog": "tadpole", "goose": "gosling", "chicken": "chick", "duck": "duckling",
                  "pig": "piglet", "owl": "owlet", "eagle": "eaglet", "butterfly": "caterpillar", "fly": "maggot",
                  "swan": "cygnet", "giraffe": "calf", "zebra": "foal", "fox": "kit", "rabbit": "kit"},
    },
    "elements": {"state": {"hydrogen": "gas", "helium": "gas", "nitrogen": "gas", "oxygen": "gas", "fluorine": "gas",
                           "carbon": "solid", "lithium": "solid", "beryllium": "solid", "boron": "solid"}},
    "greek": {"vowel": {"alpha": "vowel", "epsilon": "vowel", "eta": "vowel", "iota": "vowel", "beta": "consonant",
                        "gamma": "consonant", "delta": "consonant", "zeta": "consonant", "theta": "consonant"}},
}  # fmt: skip
NUMBER_WORD = "number word"  # the last candidate: the item's number written as a word (suite_v1.WORDS)
NINE_B = "qwen3.5-9b"
# The rule's pick on the 9B's tokenizer (plan: no lexical candidate covers 150 scenes); the 9B's run asserts it again and
# measures its accuracy (qa_word's recall gate, relation.json); the 27B and Lightning take the 9B's relation and its
# accuracy check from the 9B's run (a relation that failed on the 9B leaves their word cells not tested).
RELATION = NUMBER_WORD


def variants(w: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys((w, " " + w, w[:1].upper() + w[1:], " " + w[:1].upper() + w[1:])))


def ids(tok, text: str) -> list[int]:
    return list(tok(text, add_special_tokens=False).input_ids)


def one_token(tok, word: str) -> bool:
    return len(ids(tok, " " + word)) == 1


def clashes(tok, word: str, item: str, domain: str) -> list[tuple[str, str]]:
    """The tokens of the answer word's variants that x52_atoms' bridge classes match for this item (key, first token,
    alias, prefix, initial, part), with how they matched; [] = admissible."""
    from scripts import x52_atoms as A52

    m = A52.entity_matcher(tok, [item], domain, spell=True)
    out = []
    for v in variants(word):
        for t in ids(tok, v):
            via = A52.match(tok.decode([t]), t, m)
            if via:
                out.append((tok.decode([t]), via))
    return out


def number_word(digit: str) -> str:
    from scripts import x51_answer as A51

    return A51.number_word(digit)


def answer_of(candidate: tuple[str, str], domain: str, item: str, number: str) -> str | None:
    """The candidate's answer word for an item of the domain (None where it gives none)."""
    if candidate == (NUMBER_WORD, NUMBER_WORD):
        return number_word(number)
    dom, rel = candidate
    return LEXICAL[dom][rel].get(item) if dom == domain else None


def candidates() -> list[tuple[str, str]]:
    return [(d, r) for d, rels in LEXICAL.items() for r in rels] + [(NUMBER_WORD, NUMBER_WORD)]


def scene_pairs(set_name: str = SET) -> list[dict]:
    """The main test's scenes with both readers (lookup PP, recall PM), in scene order."""
    from scripts import tasks_v2 as T

    by: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in X.READERS:
            by[it["scene"]][it["word"]] = it
    return [by[s] for s in sorted(by) if set(by[s]) == set(X.READERS)]


def coverage(tok, pairs: list[dict]) -> dict:
    """Per candidate: its admissible items (one token, no clash) and the scenes it covers (both bridges answered by
    admissible items, the O and S answers' first tokens differ); pooled lexical coverage beside."""
    out: dict[str, Any] = {}
    pooled = set()
    for cand in candidates():
        name = "/".join(dict.fromkeys(cand))
        bad: dict[str, Any] = {}
        covered = []
        for p in pairs:
            rc = p[X.RECALL]
            words = {}
            for role, item, num in (("O", rc["bridge"], rc["answer"]), ("S", rc["cf_bridge"], rc["cf_answer"])):
                w = answer_of(cand, rc["domain"], item, num)
                if w is None:
                    break
                why = [] if one_token(tok, w) else ["not one token"]
                why += [f"{t!r} {v}" for t, v in clashes(tok, w, item, rc["domain"])]
                if why:
                    bad[item] = {"word": w, "why": why}
                    break
                words[role] = w
            if len(words) == 2 and ids(tok, " " + words["O"])[0] != ids(tok, " " + words["S"])[0]:
                covered.append(rc["scene"])
        if cand[0] != NUMBER_WORD:
            pooled |= set(covered)
        out[name] = {"scenes": len(covered), "dropped_items": bad, "admissible": len(covered) >= X.N_MIN}
    out["all lexical pooled"] = {"scenes": len(pooled), "admissible": len(pooled) >= X.N_MIN}
    return out


def choose(cov: dict) -> str:
    """The rule's choice on the tokenizer: the first admissible candidate in order (the 9B's accuracy is checked in the
    run as the (Q-after, word) gate)."""
    for cand in candidates():
        name = "/".join(dict.fromkeys(cand))
        if cov[name]["admissible"]:
            return name
    return "none"


# ---- prompts and cases (tokenizer only) -----------------------------------------------------------------------------


def user_content(question: str, context: str, kind: str, position: str) -> str:
    """The user turn: Q-after as tasks_v2.render writes the main test's prose items; Q-before with the question block
    first and the scene labelled."""
    from scripts import tasks_v2 as T

    instr = T.DIGIT_INSTRUCTION if kind == "digit" else WORD_INSTRUCTION
    if position == "after":
        return f"{context}\n{question} {instr}"
    assert position == "before", position
    return f"Question: {question} {instr}\n\nScene:\n{context}"  # a newline before the scene, as Q-after's turn start


def render(tok, question: str, context: str, kind: str, position: str) -> str:
    from bridge_jspace import chat

    return chat.chat_text(tok, user_content(question, context, kind, position), "chat")


def encode(tok, item: dict, context: str, bridge: str, kind: str, position: str) -> tuple[list[int], list[int]]:
    """The prompt's ids and the token positions of the asked person's bridge word in it (x0_necessity.encode_bridge's
    arithmetic on this cell's prompt)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    text = render(tok, item["question"], context, kind, position)
    assert text.count(context) == 1, f"{item['id']}: the context is not once in the prompt"
    enc = raw_encoding(tok, text, offsets=True)
    sentence = SP.tasks_statements({**item, "context": context, "bridge": bridge})["bind_bridge"]
    w0 = text.index(context) + SP.find_sentence(context, sentence) + sentence.rindex(bridge)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(bridge))


def targets(tok, answer: str, kind: str) -> list[int]:
    """The read's accepted tokens: a digit's token (X0) or the word's first token after a space, lower-case and
    capitalised (each asserted one token)."""
    from scripts import suite_v1 as S

    if kind == "digit":
        return [S.answer_token(tok, answer, "digit")]
    out = []
    for v in (" " + answer, " " + answer[:1].upper() + answer[1:]):
        t = ids(tok, v)
        assert len(t) == 1, f"{v!r} is not one token"
        out.append(t[0])
    return list(dict.fromkeys(out))


def cell_case(tok, pair: dict, cell: str) -> tuple[dict | None, str | None]:
    """One scene in one cell (x51_answer's item shape), or the reason it is dropped: per reader the bridge one token at
    one index in O and S, the O and S answers' read tokens disjoint; Q-after: the readers' prompts equal through the
    bridge word (one Δ from the lookup's)."""
    from scripts import suite_v1 as S

    position, atype = CELL[cell]
    readers = {}
    lk = pair[X.LOOKUP]
    for w in X.READERS:
        it = pair[w]
        kind = "word" if (atype == "word" and w == X.RECALL) else "digit"
        ans = {"org": it["answer"], "alt": it["cf_answer"]}
        said = {v: (number_word(a) if kind == "word" else a) for v, a in ans.items()}
        ids_o, p_o = encode(tok, it, it["context"], it["bridge"], kind, position)
        ids_s, p_s = encode(tok, it, it["cf_context"], it["cf_bridge"], kind, position)  # the main test's alt: cf
        if len(p_o) != 1 or p_s != p_o:
            return None, "the bridge is not one token at one position in O and S"
        diff = S.changed(ids_o, ids_s)
        if not diff or p_o[0] not in diff:
            return None, "O and S do not align at the bridge"
        set_a, set_b = targets(tok, said["org"], kind), targets(tok, said["alt"], kind)
        if set(set_a) & set(set_b):
            return None, "the O and S answers share a read token"
        readers[w] = {"id": it["id"], "question": it["question"], "answer": ans["org"], "cf_answer": ans["alt"],
                      "kind": kind, "said_A": said["org"], "said_b": said["alt"], "ids": {"org": ids_o, "alt": ids_s},
                      "pos": p_o[0], "set_A": set_a, "set_b": set_b, "tok_A": set_a[0], "tok_b": set_b[0],
                      "suffix": S.ids(tok, " ") if kind == "digit" else [], "words_A": [ans["org"], ans["alt"]],
                      "upstream": min(diff) < p_o[0]}  # fmt: skip
    if position == "after":
        p = readers[X.LOOKUP]["pos"]
        if readers[X.RECALL]["pos"] != p:
            return None, "the readers' bridge positions differ"
        for v in ("org", "alt"):
            if readers[X.LOOKUP]["ids"][v][: p + 1] != readers[X.RECALL]["ids"][v][: p + 1]:
                return None, "the readers' prompts differ before the bridge"
    for w, rd in readers.items():
        rd["src"] = X.LOOKUP if position == "after" else w
    return {"cell": cell, "set": "e1", "key": lk["scene"], "scene": lk["scene"], "domain": lk["domain"],
            "entity": lk["bridge"], "cf_entity": lk["cf_bridge"], "cf_bridge": lk["cf_bridge"], "context": lk["context"],
            "cf_context": lk["cf_context"], "pos": readers[X.LOOKUP]["pos"], "readers": readers}, None  # fmt: skip


def build(tok, cell: str, pairs: list[dict] | None = None) -> tuple[list[dict], dict]:
    pairs = scene_pairs() if pairs is None else pairs
    cases, dropped = [], collections.Counter()
    for p in pairs:
        if any(p[X.LOOKUP][k] != p[X.RECALL][k] for k in ("context", "cf_context", "bridge", "cf_bridge")):
            dropped["the readers' scenes differ"] += 1
            continue
        c, why = cell_case(tok, p, cell)
        if c is None:
            dropped[why] += 1
        else:
            cases.append(c)
    return cases, {"scenes": len(pairs), "cases": len(cases), "dropped": dict(dropped),
                   "domains": dict(collections.Counter(c["domain"] for c in cases))}  # fmt: skip


def stage_plan() -> Path:
    from scripts import x45m

    tok = x45m.tokenizer()
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    pairs = scene_pairs()
    cov = coverage(tok, pairs)
    blob: dict[str, Any] = {"target": pins.TARGET, "set": SET, "relation_coverage": cov, "relation": choose(cov),
                            "word_instruction": WORD_INSTRUCTION, "cells": {}}  # fmt: skip
    lines = [f"# x53_2x2 plan on {pins.TARGET} (tokenizer only; UNVERIFIED)", "",
             f"Relation: {blob['relation']} (rule in the module docstring). Coverage per candidate (scenes of {len(pairs)}; "
             f"admissible needs >= {X.N_MIN}):", ""]  # fmt: skip
    for k, v in cov.items():
        lines.append(f"- {k}: {v['scenes']} scenes, admissible {v['admissible']}"
                     + (f"; dropped items {v['dropped_items']}" if v.get("dropped_items") else ""))  # fmt: skip
    for cell in CELLS:
        cases, counts = build(tok, cell, pairs)
        blob["cells"][cell] = counts
        lines += ["", f"## {cell} {CELL_TEXT[cell]}: {counts}", ""]
        if cases:
            c = cases[0]
            for w, rd in c["readers"].items():
                text = tok.decode(rd["ids"]["org"])
                lines += [f"{w} (scene {c['scene']}, read tokens O {rd['set_A']} S {rd['set_b']}, src {rd['src']}):", "",
                          "```", text, "```", ""]  # fmt: skip
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "plan.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:12]), flush=True)
    print("wrote", out, flush=True)
    return out


# ---- GPU -----------------------------------------------------------------------------------------------------------


def said_word(text: str) -> str | None:
    m = re.search(r"[^\W\d_]+", next((ln for ln in text.lower().split("\n") if ln.strip()), ""))
    return m.group(0) if m else None


def read_row(lg, rd: dict, digits) -> dict:
    """X0's read_row with the read as a set of accepted tokens (a digit's one token; a word's lower-case and capitalised
    first tokens): switched = the top token is one of S's; p_org / p_alt summed over each set; ld = the best S token's
    logit minus the best O token's."""
    import torch

    top = int(lg.argmax())
    p = torch.softmax(lg.float(), -1)
    a, b = rd["set_A"], rd["set_b"]
    row = {"switched": int(top in b), "top": top, "role": "b" if top in b else "A" if top in a else "other",
           "p_org": round(float(p[a].sum()), 4), "p_alt": round(float(p[b].sum()), 4),
           "ld": round(float(lg[b].max() - lg[a].max()), 3)}  # fmt: skip
    if rd["kind"] == "digit":
        row["cand_switched"] = int(X.first_among(lg, rd["tok_b"], digits))
    return row


def competence(model, cases: list[dict], ws) -> list[dict]:
    """X0's competence on the cell's prompts: per case and reader, O and S unedited, 8 greedy tokens (said) and the
    decisive read."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    rows = []
    with torch.no_grad():
        for c in progress(cases, f"{c_name(cases)}: competence (case)"):
            for w, rd in c["readers"].items():
                texts = model.generate_batch(torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device),
                                             X.GEN_TOKENS, [{}, {}])  # fmt: skip
                for i, (v, gold, gold_set) in enumerate((("org", rd["said_A"], rd["set_A"]),
                                                         ("alt", rd["said_b"], rd["set_b"]))):  # fmt: skip
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", rd["suffix"], ws)
                    said = S.said(texts[i], "digit") if rd["kind"] == "digit" else said_word(texts[i])
                    rows.append({"scene": c["scene"], "reader": w, "variant": v, "greedy": texts[i], "said": said,
                                 "right": said == gold, "read_right": int(logits[0].argmax()) in gold_set})  # fmt: skip
    return rows


def c_name(cases: list[dict]) -> str:
    return cases[0]["cell"] if cases else "-"


def dev_scenes(target: str) -> set[str]:
    """The scenes a target's layer was fixed on, kept out of the selection as its main test keeps them (Lightning: the
    60 dev scenes of nem35l_x52_layer_r2, x0_necessity --exclude-dev); none elsewhere."""
    path = DEV_GATE.get(target)
    if path is None:
        return set()
    dev = set(json.loads((pins.REPO_ROOT / path).read_text())["dev"])
    assert dev, f"{path}: no dev scenes"
    return dev


def gate_of(
    cases: list[dict], comp: list[dict], exclude: set[str] | frozenset[str] = frozenset()
) -> tuple[dict, list[dict]]:
    """X0's gate on one cell: O read accuracy >= GATE per reader over all cases (said accuracy beside); eligible = both
    readers said and read O and S right, the excluded (dev) scenes left out after the gate, as X0 does; >= N_MIN
    eligible; the first N_ITEMS in scene order."""
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: round(float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])), 4) if cases else 0.0
           for w in X.READERS}  # fmt: skip
    said = {w: round(float(np.mean([right[(c["scene"], w, "org")]["right"] for c in cases])), 4) if cases else 0.0
            for w in X.READERS}  # fmt: skip
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    g = {"cases": len(cases), "org_read_accuracy": acc, "said_accuracy": said, "gate": X.GATE,
         "pass": bool(cases) and all(a >= X.GATE for a in acc.values()), "eligible": len(ok), "min": X.N_MIN}  # fmt: skip
    if exclude:
        g["excluded"] = sum(c["scene"] in exclude for c in ok)
        ok = [c for c in ok if c["scene"] not in exclude]
    g["enough"] = len(ok) >= X.N_MIN
    g["tested"] = g["pass"] and g["enough"]
    chosen = ok[: X.N_ITEMS] if g["tested"] else []
    g["chosen"] = len(chosen)
    g["order"] = [c["scene"] for c in chosen]
    return g, chosen


def gate_status(g: dict) -> str:
    """'tested', or the not-tested text with the failing accuracy (the lower reader's)."""
    if g.get("tested"):
        return "tested"
    if not g.get("pass"):
        return GATE_TEXT.format(acc=f"{min(g['org_read_accuracy'].values()):.2f}")
    return f"not tested ({g['eligible']} eligible < {g['min']})"


def manifest(name: str, target: str, layer: int, cells: tuple[str, ...], relation: str) -> dict:
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import suite_split as SUITE

    items = pins.DATA_DIR / "tasks_v2" / SET / "items.jsonl"
    return {"exp": EXP, "run": name, "test": "53.1", "spec": "jobs/c3/batch53.yaml (brief, 53.1)",
            "question": NO_PREDICTION, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in (SPEC, items)}, "set": SET,
            "layer": layer, "cells": list(cells), "cell_text": CELL_TEXT, "relation": relation,
            "word_instruction": WORD_INSTRUCTION, "gate": X.GATE, "n": {"items": X.N_ITEMS, "min": X.N_MIN},
            "k": X.K_MAIN, "omp": "signed", "arms": list(_arms()), "atoms": {"items": N_ATOMS, "seed": 0},
            "order": {"cells": "every cell's competence and gate first (the relation's 9B accuracy = qa_word's recall "
                               "gate), then each tested cell's Δ, readout, arms and atoms in CELLS order",
                      "reads": f"per item and reader: O unedited then the arms in order, batches of at most "
                               f"{SUITE.BATCH} rows (BJ_SUITE_BATCH)"},
            "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED, "atoms": 0},
            "design": "scripts/x53_2x2.py docstring", "verdict": "x53_2x2.py verdict (CPU)"}  # fmt: skip


def _arms() -> tuple[str, ...]:
    from scripts import x51_answer as A51

    return A51.ARMS


def run_cell(model, lens, cell: str, items: list[dict], layer: int, out: Path, ws) -> None:
    """Δ per source reader, the readout rows, the 51.12 arms (arm 1 = X0's conflict test), the reads and the atom
    inventory on N_ATOMS items, into out/."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x51_answer as A51
    from scripts import x52_atoms as A52
    from scripts.exp04_brew_parts import AddRows

    tok, dev = model.tokenizer, model.device
    toks = [A51.item_tokens(tok, it) for it in items]
    digit_list = X.digit_ids(tok)
    digits = torch.tensor(digit_list, device=dev)
    sources = sorted({rd["src"] for it in items for rd in it["readers"].values()})
    with torch.no_grad():
        deltas: dict[str, list] = {s: [] for s in sources}
        readout = []
        for it, tk in zip(progress(items, f"{cell}: Δ and the lens readout at L{layer} (item)"), toks, strict=False):
            for s in sources:
                rd = it["readers"][s]
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][rd["pos"]]
                     .float().clone() for v in ("org", "alt")}  # fmt: skip
                deltas[s].append(h["alt"] - h["org"])
                for v in ("org", "alt"):
                    lg = lens.readout(h[v][None], layer)[0].float()
                    readout.append(A51.readout_row(it, tk, s, v, lg, digit_list))
        X.write_jsonl(out / "readout.jsonl", readout)
        X.write_jsonl(out / "cases.jsonl", [{**it, "tokens": tk} for it, tk in zip(items, toks, strict=True)])
        letters = model.letter_token_ids()
        pos_of = {int(t): i for i, t in enumerate(letters.tolist())}
        outside = sorted({t for tk in toks for t in tk["A"]} - set(pos_of))
        assert not outside, f"A tokens outside the OMP dictionary (letter tokens): {outside[:10]}"
        jdic = lens.vectors(layer, letters).to(dev)
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        bases = [
            A51.answer_basis(lens.vectors(layer, torch.tensor(tk["A"], dtype=torch.long, device=dev))) for tk in toks
        ]
        picked = A52.pick(len(items))
        arms, norms, atom_rows = {}, [], []
        lt = letters.tolist()
        for s in sources:
            x = torch.stack(deltas[s]).to(dev)
            pj = X.fit(jdic, x, X.K_MAIN, "signed").to(dev)
            chosen, approx = A51.omp_support(jdic, x, X.K_MAIN)
            assert torch.allclose(approx, pj, atol=1e-4 * float(pj.abs().max()) + 1e-6), "OMP support does not match"
            arms[s], sh = A51.all_arms(x, pj, bases, basis)
            for i, (it, tk) in enumerate(zip(items, toks, strict=True)):
                a_pos = {pos_of[t] for t in tk["A"]}
                hits = [int(letters[j]) for j in chosen[i].tolist() if j in a_pos]
                norms.append({"key": it["key"], "entity": it["entity"], "source": s, "norm": round(float(x[i].norm()), 4),
                              **{f"share_{k}": round(float(v[i]), 6) for k, v in sh.items()},
                              "A_tokens": len(tk["A"]), "A_rank": int(bases[i].shape[1]), "A_ids": tk["A"],
                              "A_words": tk["A_words"], "n_answer_atoms_in_25": len(hits), "answer_atoms_in_25": hits})  # fmt: skip
            # batch 52 A's inventory on N_ATOMS items (seed 0): x52_atoms.omp_atoms on the same Δ and dictionary
            xa = x[picked]
            ch, coefs, gains, ap = A52.omp_atoms(jdic, xa, X.K_MAIN)
            assert torch.allclose(ap, pj[picked], atol=1e-4 * float(pj.abs().max()) + 1e-6), "x52 OMP does not match"
            sq = (xa.double().norm(dim=-1) ** 2).cpu()
            share = ((ap.double().norm(dim=-1) ** 2).cpu() / sq).tolist()
            for r, i in enumerate(picked):
                it = items[i]
                atom_rows.append({"cell": cell, "key": it["key"], "reader": s, "entity": it["entity"],
                                  "cf_entity": it["cf_entity"], "norm": round(float(sq[r] ** 0.5), 4),
                                  "share_k25": round(share[r], 6),
                                  "atoms": [{"rank": k + 1, "token_id": lt[j], "token": model.decoded[lt[j]],
                                             "coef": round(float(coefs[r, k]), 5), "share": round(float(gains[r, k]), 6)}
                                            for k, j in enumerate(ch[r].tolist())]})  # fmt: skip
        del jdic
        torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        X.write_jsonl(out / "atoms.jsonl", atom_rows)
        names = _arms()
        rows = []
        for i, it in enumerate(progress(items, f"{cell}: {len(names)} arms + O x readers at L{layer} (item)")):
            for w, rd in it["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[rd["src"]][a][i : i + 1], [rd["pos"]])} for a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
                for a, lg in zip(("none", *names), logits, strict=True):
                    row = read_row(lg, rd, digits)
                    rows.append({"key": it["key"], "scene": it["scene"], "entity": it["entity"], "reader": w, "arm": a,
                                 **row, "sw": row["switched"]})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    if cell == "qa_num":  # the main test as is: arm 1 against the stored X0 run item by item, where one exists
        from scripts import x45b_binding as B

        src = X.RESULTS / B.MAIN_RUN.get(pins.TARGET, "-")
        if (src / "outcomes.jsonl").exists():
            agree = A51.agreement("e1", rows, A51.stored_rows("e1", src, layer))
            (out / "agreement.json").write_text(json.dumps({"stored_run": src.name, **agree}, indent=1) + "\n")
    print(f"{cell}: {len(rows)} reads of {len(items)} items; {len(atom_rows)} atom lists", flush=True)


def stage_run(name: str, cells: tuple[str, ...]) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import loaded_hub_kernels
    from scripts import x6_routes as R

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in RUNS, f"53.1 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    from scripts import x45m

    tok0 = x45m.tokenizer()
    pairs = scene_pairs()
    cov = coverage(tok0, pairs)
    if target == NINE_B:
        assert choose(cov) == RELATION, f"the relation rule picks {choose(cov)!r} on the 9B, not {RELATION!r}"
        nine = None
    else:  # the 9B's choice and accuracy check (its run's relation.json; the job depends on the 9B's)
        path = RESULTS / RUNS[NINE_B] / "relation.json"
        assert path.exists(), f"{path}: the 9B's relation check is not here (run the 9B's job first)"
        nine = json.loads(path.read_text())
    word_ok = nine is None or bool(nine["passes"])
    m = manifest(name, target, layer, cells, RELATION)
    m["relation_coverage"] = cov
    m["relation_9b"] = nine if nine is not None else "this run (relation.json)"
    dev = dev_scenes(target)
    if dev:
        m["excluded_scenes"] = {"source": DEV_GATE[target], "scenes": sorted(dev)}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    ws = X.whitespace_mask(model)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    built, gates = {}, {}
    for cell in cells:  # every cell's gate before any test (the relation's accuracy is qa_word's recall gate)
        (out / cell).mkdir()
        cases, counts = build(tok, cell, pairs)
        comp = competence(model, cases, ws)
        g, chosen = gate_of(cases, comp, dev)
        g["counts"], g["status"] = counts, gate_status(g)
        g["hub_kernels"] = loaded_hub_kernels()
        X.write_jsonl(out / cell / "competence.jsonl", comp)
        print(cell, json.dumps({k: v for k, v in g.items() if k != "order"}), flush=True)
        built[cell], gates[cell] = chosen, g
    if "qa_word" in gates:
        acc = gates["qa_word"]["org_read_accuracy"][X.RECALL]
        rel = {"relation": RELATION, "model": target, "accuracy_recall_qa_word": acc, "bar": X.GATE,
               "passes": acc >= X.GATE, "coverage": cov}  # fmt: skip
        (out / "relation.json").write_text(json.dumps(rel, indent=1) + "\n")
        word_ok = word_ok and (target != NINE_B or rel["passes"])
    for cell in cells:  # the gates as they stand once the relation is checked, before any test
        if CELL[cell][1] == "word" and not word_ok:
            gates[cell] = {**gates[cell], "tested": False, "status": "not tested (the relation's 9B accuracy < 0.80)"}
        (out / cell / "gate.json").write_text(json.dumps(gates[cell], indent=1) + "\n")
    for cell in cells:
        if gates[cell]["tested"]:
            run_cell(model, lens, cell, built[cell], layer, out / cell, ws)
        else:
            print(f"{cell}: {gates[cell]['status']}", flush=True)
        torch.cuda.empty_cache()
    m["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- verdict (CPU) --------------------------------------------------------------------------------------------------


def conflict_numbers(rows: list[dict], reader: str, n_boot: int) -> dict:
    """X0's cell at L for one reader from the run's whole / no_jpp / no_jpp_rand reads (excess = extra loss beyond
    random, X0's label)."""
    mine = [r for r in rows if r["reader"] == reader]
    by = {(r["key"], r["arm"]): r["sw"] for r in mine}
    keys = list(dict.fromkeys(r["key"] for r in mine if r["arm"] == "whole"))
    ent = {r["key"]: r["entity"] for r in mine}
    sw = {a: [int(by[(k, b)]) for k in keys] for a, b in (("whole", "whole"), ("no_part", "no_jpp"),
                                                          ("no_rand", "no_jpp_rand"))}  # fmt: skip
    return X.cell(sw, [ent[k] for k in keys], n_boot)


def cell_result(run_dir: Path, cell: str, target: str, n_boot: int) -> dict:
    from scripts import x51_answer as A51

    d = run_dir / cell
    g = json.loads((d / "gate.json").read_text()) if (d / "gate.json").exists() else None
    if g is None:
        return {"cell": cell, "status": "pending", "label": None}
    rows = X.read_jsonl(d / "outcomes.jsonl")
    if not g["tested"]:
        return {"cell": cell, "status": g.get("status") or gate_status(g), "gate": g, "label": None}
    if not rows:
        return {"cell": cell, "status": "pending (gate passed; no reads here)", "gate": g, "label": None}
    readout = X.read_jsonl(d / "readout.jsonl")
    readers = {}
    for w in X.READERS:
        r = A51.reader_numbers(rows, w, n_boot)
        r["check"] = A51.readout_check(readout, w, n_boot)
        r["arm_label"], r["arm_key"] = r["label"], r["key"]
        if r["check"]["case"] == "not_read":
            r["label"], r["key"] = A51.LABELS["not_read"], "not_read"
        r["conflict"] = conflict_numbers(rows, w, n_boot)
        readers[A51.READER_NAME[w]] = r
    return {"cell": cell, "status": "tested", "gate": g, "readers": readers, "label": readers["recall"]["key"],
            "lookup_extra": readers["lookup"]["conflict"]["excess"], "atoms": atoms_summary(d, target, n_boot),
            "agreement": json.loads((d / "agreement.json").read_text()) if (d / "agreement.json").exists() else None}  # fmt: skip


def atoms_summary(d: Path, target: str, n_boot: int) -> dict:
    """x52_atoms' classifier on the cell's atom lists: per view (Q-after: the lookup's Δ in both readers' views;
    Q-before: each reader's own Δ in its own view) the class shares (x52_atoms.summarise)."""
    from scripts import x52_atoms as A52

    rows = X.read_jsonl(d / "atoms.jsonl")
    cases = {c["key"]: c for c in X.read_jsonl(d / "cases.jsonl")}
    if not rows:
        return {}
    tok = A52.tokenizer_of(target)
    vocab = {k: set(v) for k, v in A52.SAME_CLASS.items()}
    scenes = {k: A52.e1_scene(c) for k, c in cases.items()}
    for sc in scenes.values():
        vocab.setdefault(sc["domain"], set()).update([sc["bridge"], sc["new"], *sc["items"]])
    by_view: dict[str, list[dict]] = collections.defaultdict(list)
    after = CELL[d.name][0] == "after"
    for r in rows:
        sc = scenes[r["key"]]
        for view in X.READERS if after else (r["reader"],):
            ctx = A52.e1_context(tok, sc, view, vocab)
            atoms = [{**a, **dict(zip(("class", "via", "detail"), A52.classify(a["token"], a["token_id"], ctx),
                                      strict=True))} for a in r["atoms"]]  # fmt: skip
            by_view[view].append({"entity": r["entity"], "share_k25": r["share_k25"], "atoms": atoms})
    return {A52.READER_NAME[v]: A52.summarise(recs, n_boot) for v, recs in by_view.items()}


def across(labels: dict[str, str | None]) -> str:
    """The rule across cells (verbatim, batch53.yaml) on the cells' labels (51.12's keys: entity / answer / mixed /
    not_read / na); a pattern that needs a cell without a label can't be read."""
    qa_n, qb_n, qa_w, qb_w = (labels.get(c) for c in CELLS)
    am = ("answer", "mixed")
    if any(v is None for v in (qa_n, qb_n, qa_w, qb_w)):
        missing = [CELL_TEXT[c] for c in CELLS if labels.get(c) is None]
        return f"can't tell: {', '.join(missing)} without a label"
    if qb_n in am and qa_w == "entity":
        return "position"
    if qa_w in am and qb_n == "entity":
        return "readability"
    if qb_n == "mixed" and qa_w == "mixed" and qb_w == "answer":
        return "both"
    if all(v == "entity" for v in (qa_n, qb_n, qa_w, qb_w)):
        return "neither"
    return "none of the four patterns"


def cross_check(cells: dict[str, dict]) -> dict:
    """The lookup's extra loss beyond random (the conflict test, arm 1) <= CROSS_MAX in all four cells."""
    per: dict[str, float | None] = {c: (r["lookup_extra"][0] if r.get("status") == "tested" else None)
                                    for c, r in cells.items()}  # fmt: skip
    known = [v for v in per.values() if v is not None and not math.isnan(v)]
    held = all(v <= CROSS_MAX + EPS for v in known) if len(known) == len(per) else None
    return {"per_cell": per, "holds": held,
            "text": ("the pointer does not depend on the question (lookup <= 0.10 beyond random in all four cells)"
                     if held else "does not hold" if held is False else "can't tell (a cell without numbers)")}  # fmt: skip


def model_verdict(target: str, n_boot: int) -> dict:
    run = RUNS[target]
    d = RESULTS / run
    if not (d / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending"}
    m = json.loads((d / "manifest.json").read_text())
    cells = {c: cell_result(d, c, target, n_boot) for c in CELLS}
    labels = {c: r.get("label") for c, r in cells.items()}
    rel = json.loads((d / "relation.json").read_text()) if (d / "relation.json").exists() else None
    return {"target": target, "run": run, "status": "run", "layer": m["layer"], "relation": m["relation"],
            "relation_check": rel, "cells": cells, "across": across(labels), "cross_check": cross_check(cells)}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]")  # fmt: skip


def brief_53_1() -> str:
    """53.1 as the brief states it (jobs/c3/batch53.yaml `brief:`), verbatim."""
    import yaml

    brief = yaml.safe_load(SPEC.read_text())["brief"]
    return brief[brief.index("53.1 (top)") : brief.index("53.2 The monitor")].rstrip()


def verdict_lines(models: list[dict]) -> list[str]:
    from scripts import x51_answer as A51

    lines = ["# 53.1: the 2x2, question position x answer type (UNVERIFIED; no prediction)", "",
             "Batch 53, test 53.1 (jobs/c3/batch53.yaml). The brief's 53.1, verbatim:", "", "```", brief_53_1(), "```",
             "",
             f"51.12's rule (x51_answer): {A51.RULE}", "",
             "As computed: see scripts/x53_2x2.py's docstring (cells, relation, gate, conflict test, 51.12 arms, "
             "atoms). The cell's label is the recall's 51.12 label (51.12's decisive E1 reader); the lookup's beside. "
             f"Cluster bootstrap over the bridge entity ({X.N_BOOT}, seed {X.BOOT_SEED}).", ""]  # fmt: skip
    for mv in models:
        name = MODEL_SHORT.get(mv["target"], mv["target"])
        if mv["status"] != "run":
            lines += [f"## {name}: pending (no run {mv['run']} here)", ""]
            continue
        lines += [f"## {name} ({mv['run']}, L{mv['layer']}; relation for the word cells: {mv['relation']})", "",
                  f"Rule across cells: **{mv['across']}**. Cross-check: **{mv['cross_check']['text']}**.", ""]  # fmt: skip
        if mv.get("relation_check"):
            rc = mv["relation_check"]
            lines += [f"Relation check: the recall's O read accuracy on (Q-after, word) = {rc['accuracy_recall_this_model']}"
                      f" (>= 0.80: {rc['passes']}).", ""]  # fmt: skip
        lines += ["| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | "
                  "conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | "
                  "recall answer word not read |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for c, r in mv["cells"].items():
            g = r.get("gate") or {}
            acc = g.get("org_read_accuracy", {})
            gtxt = f"{acc.get('PP', '-')} / {acc.get('PM', '-')}" if acc else "-"
            if r["status"] != "tested":
                lines.append(f"| {CELL_TEXT[c]} | {gtxt} | - | {r['status']} | | | | | | |")
                continue
            lk, rc_ = r["readers"]["lookup"], r["readers"]["recall"]
            lines.append(f"| {CELL_TEXT[c]} | {gtxt} | {rc_['n']} | **{rc_['label']}** | {lk['label']} | "
                         f"{fmt(lk['conflict']['excess'])} ({lk['conflict']['label']}) | "
                         f"{fmt(rc_['conflict']['excess'])} ({rc_['conflict']['label']}) | {fmt(rc_['share2'])} | "
                         f"{fmt(rc_['extra']['3'])} | {fmt(rc_['check']['not_read'])} |")  # fmt: skip
        for c, r in mv["cells"].items():
            if r["status"] != "tested":
                continue
            lines += ["", f"### {CELL_TEXT[c]}", ""]
            for w, rr in r["readers"].items():
                ck = rr["check"]
                lines.append(f"- {w}: rates {', '.join(f'{a} {fmt(v)}' for a, v in rr['rate'].items())}; extra "
                             f"{', '.join(f'e{k} {fmt(v)}' for k, v in rr['extra'].items())}; readout: top-50 O "
                             f"{fmt(ck['top50_O'])}, S {fmt(ck['top50_S'])}, not read {fmt(ck['not_read'])} "
                             f"(case {ck['case']}); arm rule: {rr['arm_label']}; X0's validity bar {rr['valid']}")  # fmt: skip
            for v, s in (r.get("atoms") or {}).items():
                e = s["energy"]
                lines.append(f"- atoms ({v}'s view, n {s['n']}): energy shares bridge {fmt(e['bridge'])}, new bridge "
                             f"{fmt(e['new_bridge'])}, own answer {fmt(e['answer_own'])}, other answer "
                             f"{fmt(e['answer_other'])}, other {fmt(e['other'])}; part's share median "
                             f"{s['share_k25_median']:.3f}")  # fmt: skip
            if r.get("agreement"):
                ag = r["agreement"]
                lines.append(f"- against the stored main test ({ag['stored_run']}): " + "; ".join(
                    f"{w}: whole {v['whole']['agree_switch']}/{v['whole']['matched']}, arm 1 extra loss rerun "
                    f"{v['extra_loss_arm1']['rerun']:.3f} vs stored {v['extra_loss_arm1']['stored']:.3f}"
                    for w, v in ag.items() if isinstance(v, dict) and "whole" in v))  # fmt: skip
        lines.append("")
    lines += ["Status: UNVERIFIED until a human adds it to VERIFIED.md."]
    return lines


def figure(models: list[dict], path: Path) -> None:
    """One figure for the ledger card: per model a panel, per cell a row; the recall's three extra losses (arm 1
    without the J++ part, arm 2 with the answer directions kept, arm 3 the answer directions alone) and the lookup's arm
    1 (the cross-check, its <= 0.10 band shaded) as dots with 95% CIs; the cell's 51.12 label at the right."""
    from scripts import story_style as SS

    plt = SS.setup()
    run = [m for m in models if m["status"] == "run"] or models[:1]
    fig, axes = plt.subplots(1, len(run), figsize=(SS.WIDTH, 1.2 + 0.75 * len(CELLS)), squeeze=False, sharey=True)
    marks = (("recall", "1", SS.COL["recall"], "o", "recall: without the J++ part"),
             ("recall", "2", SS.COL["recall"], "D", "recall: the J++ part, answer directions kept"),
             ("recall", "3", SS.COL["control"], "s", "recall: the answer directions alone"),
             ("lookup", "1", SS.COL["lookup"], "o", "lookup: without the J++ part (cross-check)"))  # fmt: skip
    for ax, mv in zip(axes[0], run, strict=True):
        ax.axvspan(-0.2, CROSS_MAX, color=SS.COL["band"], zorder=0)
        ax.axvline(0, color="#999999", lw=0.8)
        ax.set_xlim(*SS.XLIM)
        ax.set_ylim(-0.6, len(CELLS) - 0.4)
        ax.set_yticks(range(len(CELLS)))
        ax.set_yticklabels([CELL_TEXT[c] for c in CELLS])
        ax.invert_yaxis()
        ax.set_xlabel("extra loss beyond a random part")
        ax.set_title(f"{MODEL_SHORT.get(mv['target'], mv['target'])}" + (f", L{mv['layer']}" if "layer" in mv else ""),
                     loc="left")  # fmt: skip
        if mv["status"] != "run":
            SS.empty(ax, "pending")
            continue
        for y, c in enumerate(CELLS):
            r = mv["cells"][c]
            if r["status"] != "tested":
                ax.text(0.4, y, r["status"], va="center", ha="center", fontsize=SS.LABEL_PT, color=SS.COL["muted"])
                continue
            for j, (w, k, col, mk, _) in enumerate(marks):
                v = r["readers"][w]["extra"][k]
                if v[0] is None or math.isnan(v[0]):
                    continue
                yy = y - 0.27 + 0.18 * j
                lo, hi = (v[1], v[2]) if not (math.isnan(v[1]) or math.isnan(v[2])) else (v[0], v[0])
                ax.errorbar(v[0], yy, xerr=[[v[0] - lo], [hi - v[0]]], fmt=mk, color=col, ms=6, lw=1.2, capsize=0)
            ax.text(1.0, y, r["readers"]["recall"]["key"], va="center", ha="right", fontsize=SS.LABEL_PT,
                    color=SS.COL["muted"])  # fmt: skip
    from matplotlib.lines import Line2D

    handles = [Line2D([], [], marker=mk, color=col, ls="", label=t) for _, _, col, mk, t in marks]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=SS.LABEL_PT)
    head = run[0]
    t = f"53.1 on {MODEL_SHORT.get(head['target'], head['target'])}: {head.get('across', 'pending')}"
    SS.title(
        fig, t[:70], "Shaded: the lookup's 'not needed' band (<= 0.10). Right: the recall's 51.12 label. UNVERIFIED."
    )
    fig.tight_layout(rect=(0, 0.12, 1, 0.9))
    fig.savefig(path, dpi=100)
    plt.close(fig)


def stage_verdict(n_boot: int = X.N_BOOT) -> Path:
    models = [model_verdict(t, n_boot) for t in MODEL_ORDER]
    out = RESULTS / f"x53_2x2-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    (out / "verdict.json").write_text(json.dumps(models, indent=1, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(verdict_lines(models)) + "\n")
    figure(models, out / "x53_2x2.png")
    print("\n".join(verdict_lines(models)[:40]), flush=True)
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x53_2x2/<name>/)")
    ap.add_argument("--cells", nargs="+", choices=CELLS, default=list(CELLS))
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, tuple(a.cells))
    else:
        stage_verdict(a.n_boot)


if __name__ == "__main__":
    main()
