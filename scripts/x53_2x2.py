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
  qa_word  (Q-after, word)    the recall asks a relation with a word answer instead of the number (RELATION below): its
           question RELATION_Q (the person's pick described as in the main test), its instruction WORD_INSTRUCTION
           (suite_v1's "Answer with a single word and nothing else."); read right after "Answer:" (no space token: the
           word's first token carries its own space, as suite_v1); lookup unchanged. One Δ from the lookup's prompts.
           Only the scenes the relation answers (both bridges) are built.
  qb_word  (Q-before, word)   both changes; per-reader Δ.
The number cells and the word cells are separate runs (`run --cells number`, `run --cells word`; Dan 10:20, batch53.yaml
decision_531_words: the number cells now, the word cells after the relation is picked; "number written as a word" is
skipped).

Relation (the brief: chosen on the 9B before any test; Dan's 10:20 decision relaxes the token rule before any result to
the repo's convention for words): a word answer is read by its first token (the first token of " w" and of " W", as the
natural passages and Zach's sets); the first tokens must be distinct across the relation's answers (else the relation is
out) and no token of any variant of the answer word (as is, leading space, capitalised, both) may match the item's
bridge classes (x52_atoms.entity_matcher(spell=True): key, first token, symbol / character / translation alias, prefix,
initial, part; an item that clashes leaves the relation). Candidates, fixed before any run (LEXICAL, RELATION_Q):
animal class (mammal / bird / insect / arachnid / amphibian), animal young (puppy, kitten, ...), element state (gas /
solid; no element of the scenes is a liquid), Greek letter vowel / consonant. Pick (Dan): coverage on the 9B >= 150
scenes (both bridges answered, the O and S answers' first tokens differ: X0's drop rule), the most covering one; then
the 9B's accuracy >= 0.8 = the (Q-after, word) recall's O read accuracy over the relation's scenes, measured in the
9B's word run after both word cells' gates and before any test (relation.json; < 0.80 = the word cells not tested, and
the card says so: readability is covered by 51.12 on Zach's named passages and by 53.1b). On the 9B's tokenizer
(`plan`): animal class 191 scenes (mouse out: " M", Mammal's first token, is its initial), element state 107, Greek 121,
animal young 17: animal class. The 27B and Lightning take the 9B's relation and its accuracy check (the 9B's word run's
relation.json).

Per cell (the cell's own gate first; a failed gate = "not tested (gate x < 0.80)", numbers descriptive only, never
lowered):
  gate     X0's competence and gate on the cell's prompts (unedited O and S, 8 greedy tokens and the decisive read; gate
           = O read accuracy >= 0.80 per reader over all scenes; eligible = both readers say and read O and S right; >=
           150 eligible; the first 200 in scene order; Lightning: its 60 dev scenes left out of the eligible ones after
           the gate, as its main test nem35l_x52_conflict did, DEV_GATE). Word answers: said = the first word of the
           first line, lower-cased, the answer or its plural (x52_atoms.word_keys: "mammals"); read = the top token is
           the answer's first token after a space, lower-case or capitalised (" mamm" / " M").
  conflict X0's test at L (9B L12, 27B L32, Lightning L14 = x51_lightning.py layer): Δ = h_S - h_O at the bridge word;
           arms whole / without the J++ part (signed OMP, K = 25, J++ letter atoms; x0_necessity.fit) / without a random
           part of its share (x6_routes.removal_arms over X0's random basis, seed 888 + L); X0's cell numbers (excess =
           extra loss beyond random, cluster bootstrap over the bridge entity, 10,000, seed 0) and label per reader.
  51.12    x51_answer's arms (the same forwards): the readout check first (the lens rank of each reader's own answer word,
           A-style variants, at the edited token on O and S; not read = rank > 50 on both), then arm 1 no_jpp, arm 2
           no_jpp_A (A projected out of the J++ part), arm 3 no_A, each against its random twin; A = the J++ atoms of
           both readers' O and S answers: a digit answer by its number word's one-token variants (51.12's E1
           construction), a word answer by the first token of each variant (51.12's Z2 construction). Label per reader:
           x51_answer.rule
           and the readout case (51.12's labels: entity / answer / mixed / answer word not read; e1 <= 0 = can't tell).
           The cell's label is the recall's (51.12's decisive E1 reader); the lookup's beside.
  atoms    batch 52 A's inventory on 50 of the cell's items (seed 0, x52_atoms.pick): the K = 25 OMP atoms of Δ
           (x52_atoms.omp_atoms) classified by x52_atoms' classifier (E1 contexts, a word answer's classes by
           x52_atoms.word_answer_matcher; Q-after: the lookup's Δ in both readers' views; Q-before: each reader's own Δ
           in its own view); descriptive.

Dan 11:10 (batch53.yaml next_1110): "53.1 (Q-before, number) on Muse, and on Lightning if its gate passes ... Rule: the
conflict test's, verbatim; across: "the pointer does not depend on the question's position" if the lookup loses <= 0.10
in both cells on a model" (position_rule, per model, beside the brief's rule; Muse at L26, Lightning at its committed
L14 without its 60 dev scenes); "Stop: the 53.1 word cells (the wording fails)" (Muse and Lightning have no word run).

Rule across cells (verbatim, batch53.yaml): "position": (Q-before, number) is answer or mixed and (Q-after, word) is
entity; "readability": (Q-after, word) is answer or mixed and (Q-before, number) is entity; "both": each single change
gives mixed and (Q-before, word) gives answer; "neither": all four entity. Cross-check, decisive for the story: the
conflict test's lookup loses <= 0.10 beyond random in all four cells ("the pointer does not depend on the question");
reported per cell. A cell not tested or with another label: the patterns that need it can't be read.

uv run python scripts/x53_2x2.py plan                                                   # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_2x2.py run --cells number --name qwen35_9b_x53_2x2   # GPU
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_2x2.py run --cells word --name qwen35_9b_x53_2x2_words   # GPU
uv run python scripts/x53_2x2.py verdict                                                # CPU, every model's run
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
import textwrap
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
NUMBER_CELLS, WORD_CELLS = CELLS[:2], CELLS[2:]
# Dan 10:20 (batch53.yaml decision_531_words): the number cells now, the word cells later in a run of their own
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_2x2", "qwen3.6-27b": "x53_2x2_27b", "muse-glimmer-30b": "muse30_x53_2x2",
        "nemotron-3.5-lightning": "nem35l_x53_2x2", "qwen3.5-122b-a10b": "qwen35_122b_x53_2x2"}  # fmt: skip
# the stored main test per model ((Q-after, number) is checked against it): x45b_binding.MAIN_RUN, and the 122B's X0 r2
# at L33 (Dan 11:30, q122b_1130: 53.1 (Q-before, number) on the 122B); x45b_binding itself is left as it is
MAIN_RUN_122B = {"qwen3.5-122b-a10b": "qwen35_122b_x0_necessity_r2"}


def main_runs() -> dict[str, str]:
    from scripts import x45b_binding as B

    return {**B.MAIN_RUN, **MAIN_RUN_122B}


# Dan 11:10 (batch53.yaml next_1110): "Stop: the 53.1 word cells (the wording fails)"; Muse and Lightning have none
WORD_RUNS = {"qwen3.5-9b": "qwen35_9b_x53_2x2_words", "qwen3.6-27b": "x53_2x2_words_27b"}
WORDS_STOPPED = "stopped (Dan 11:10: the wording fails)"
# the verdict's models: the 9B and the 27B (Dan 10:20), Muse and Lightning's number cells (Dan 11:10, item 3), the 122B's
# (Dan 11:30, item 3)
MODEL_ORDER = ("qwen3.5-9b", "qwen3.6-27b", "qwen3.5-122b-a10b", "muse-glimmer-30b", "nemotron-3.5-lightning")
MODEL_SHORT = {
    "qwen3.5-9b": "9B",
    "qwen3.6-27b": "27B",
    "qwen3.5-122b-a10b": "122B",
    "muse-glimmer-30b": "Muse",
    "nemotron-3.5-lightning": "Lightning",
}
# Dan 11:10's rule across the number cells, per model (verbatim in POSITION_RULE_TEXT)
POSITION_HOLDS = "the pointer does not depend on the question's position"
POSITION_RULE_TEXT = ('Dan 11:10 (batch53.yaml next_1110, item 3), verbatim: "Rule: the conflict test\'s, verbatim; '
                      'across: "the pointer does not depend on the question\'s position" if the lookup loses <= 0.10 in '
                      'both cells on a model."')  # fmt: skip
# Lightning's main test (nem35l_x52_conflict) keeps the 60 scenes its layer was fixed on out of the selection
DEV_GATE = {"nemotron-3.5-lightning": "results/x51_lightning/nem35l_x52_layer_r2/gate.json"}
WORD_INSTRUCTION = "Answer with a single word and nothing else."  # suite_v1.INSTRUCTION (chat.QUESTION_INSTRUCTION)
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
# the recall's question per candidate ({d}: the pick as the main test describes it, "Iris's pick"), fixed before any run
RELATION_Q = {("animals", "class"): "What class of animal is {d}?",
              ("animals", "young"): "What is the young of {d} called?",
              ("elements", "state"): "What is the state of {d} at room temperature?",
              ("greek", "vowel"): "Is {d} a vowel or a consonant?"}  # fmt: skip
NINE_B = "qwen3.5-9b"
# The rule's pick on the 9B's tokenizer (`plan`: animal class 191 scenes, element state 107, Greek 121, animal young 17);
# the 9B's word run asserts it again and measures its accuracy (qa_word's recall gate, relation.json); the 27B and
# Lightning take the 9B's relation and its accuracy check from the 9B's word run.
RELATION = ("animals", "class")


def variants(w: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys((w, " " + w, w[:1].upper() + w[1:], " " + w[:1].upper() + w[1:])))


def ids(tok, text: str) -> list[int]:
    return list(tok(text, add_special_tokens=False).input_ids)


def first_tokens(tok, word: str) -> list[int]:
    """A word answer's read tokens: the first token of " w" and of " W" (the repo's convention for words: a multi-token
    answer is read by its first token)."""
    return list(dict.fromkeys(ids(tok, v)[0] for v in (" " + word, " " + word[:1].upper() + word[1:])))


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


def name_of(cand: tuple[str, str]) -> str:
    return "/".join(cand)


def candidates() -> list[tuple[str, str]]:
    return [(d, r) for d, rels in LEXICAL.items() for r in rels]


def shared_first_tokens(tok, cand: tuple[str, str]) -> list[tuple[str, str]]:
    """Pairs of the relation's distinct answers whose read tokens overlap (the rule: none)."""
    answers = sorted(set(LEXICAL[cand[0]][cand[1]].values()))
    reads = {a: set(first_tokens(tok, a)) for a in answers}
    return [(a, b) for i, a in enumerate(answers) for b in answers[i + 1 :] if reads[a] & reads[b]]


def admissible_answers(tok, cand: tuple[str, str]) -> tuple[dict[str, str], dict[str, Any]]:
    """The relation's items whose answer clashes with none of the item's bridge classes, and the dropped ones with why."""
    dom, rel = cand
    ok, bad = {}, {}
    for item, w in LEXICAL[dom][rel].items():
        why = clashes(tok, w, item, dom)
        if why:
            bad[item] = {"word": w, "why": [f"{t!r} {v}" for t, v in why]}
        else:
            ok[item] = w
    return ok, bad


def scene_answers(tok, cand: tuple[str, str], rc: dict, ok: dict[str, str] | None = None) -> tuple[dict | None, str]:
    """The recall item's O and S answers under the relation ({'O': w, 'S': w'}), or None and why: another domain, a
    bridge the relation does not answer (or whose answer clashes), the same read token for O and S."""
    if rc["domain"] != cand[0]:
        return None, "the relation's domain is another"
    ok = admissible_answers(tok, cand)[0] if ok is None else ok
    o, s = ok.get(rc["bridge"]), ok.get(rc["cf_bridge"])
    if o is None or s is None:
        return None, "a bridge without an admissible answer under the relation"
    if set(first_tokens(tok, o)) & set(first_tokens(tok, s)):
        return None, "the O and S answers share a read token"
    return {"O": o, "S": s}, ""


def coverage(tok, pairs: list[dict]) -> dict:
    """Per candidate: its answers' read tokens, the pairs of answers sharing one (the rule: none), the items dropped for
    a clash, the scenes it covers and whether it is admissible (no shared read token, >= N_MIN scenes)."""
    out: dict[str, Any] = {}
    for cand in candidates():
        ok, bad = admissible_answers(tok, cand)
        shared = shared_first_tokens(tok, cand)
        covered = [p[X.RECALL]["scene"] for p in pairs if scene_answers(tok, cand, p[X.RECALL], ok)[0] is not None]
        reads = {
            a: [tok.decode([t]) for t in first_tokens(tok, a)] for a in sorted(set(LEXICAL[cand[0]][cand[1]].values()))
        }
        out[name_of(cand)] = {"scenes": len(covered), "read_tokens": reads, "shared_first_tokens": shared,
                              "dropped_items": bad, "admissible": not shared and len(covered) >= X.N_MIN}  # fmt: skip
    return out


def choose(cov: dict) -> str:
    """The rule's pick on the tokenizer: the admissible candidate covering the most scenes (ties: the first in order);
    'none' if none (the 9B's accuracy is checked in the word run as the (Q-after, word) recall gate)."""
    best = max((c for c in candidates() if cov[name_of(c)]["admissible"]), key=lambda c: cov[name_of(c)]["scenes"],
               default=None)  # fmt: skip
    return name_of(best) if best else "none"


def scene_pairs(set_name: str = SET) -> list[dict]:
    """The main test's scenes with both readers (lookup PP, recall PM), in scene order."""
    from scripts import tasks_v2 as T

    by: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in X.READERS:
            by[it["scene"]][it["word"]] = it
    return [by[s] for s in sorted(by) if set(by[s]) == set(X.READERS)]


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
    capitalised (first_tokens: the repo's convention for words)."""
    from scripts import suite_v1 as S

    if kind == "digit":
        return [S.answer_token(tok, answer, "digit")]
    return first_tokens(tok, answer)


def cell_case(tok, pair: dict, cell: str, ok: dict[str, str] | None = None) -> tuple[dict | None, str | None]:
    """One scene in one cell (x51_answer's item shape), or the reason it is dropped: per reader the bridge one token at
    one index in O and S, the O and S answers' read tokens disjoint; Q-after: the readers' prompts equal through the
    bridge word (one Δ from the lookup's). Word cells: the recall asks RELATION (RELATION_Q, WORD_INSTRUCTION) and its
    answers are the relation's words (ok: its admissible answers, computed once by build); a scene the relation does
    not answer is dropped."""
    from scripts import suite_v1 as S

    position, atype = CELL[cell]
    readers = {}
    lk = pair[X.LOOKUP]
    words = None
    if atype == "word":
        words, why = scene_answers(tok, RELATION, pair[X.RECALL], ok)
        if words is None:
            return None, why
    for w in X.READERS:
        it = pair[w]
        kind = "word" if (atype == "word" and w == X.RECALL) else "digit"
        if kind == "word":
            assert words is not None
            it = {**it, "question": RELATION_Q[RELATION].format(d=it["start_desc"])}
            ans = {"org": words["O"], "alt": words["S"]}
        else:
            ans = {"org": it["answer"], "alt": it["cf_answer"]}
        said = dict(ans)
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
    ok = admissible_answers(tok, RELATION)[0] if CELL[cell][1] == "word" else None
    cases, dropped = [], collections.Counter()
    for p in pairs:
        if any(p[X.LOOKUP][k] != p[X.RECALL][k] for k in ("context", "cf_context", "bridge", "cf_bridge")):
            dropped["the readers' scenes differ"] += 1
            continue
        c, why = cell_case(tok, p, cell, ok)
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
        lines.append(f"- {k}: {v['scenes']} scenes, admissible {v['admissible']}; read tokens {v['read_tokens']}; "
                     f"answers sharing a read token {v['shared_first_tokens']}"
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


def said_right(said: str | None, gold: str, kind: str) -> bool:
    """A digit said as itself (X0); a word said as the answer or its plural (x52_atoms.word_keys: 'mammals')."""
    from scripts import x52_atoms as A52

    if kind == "digit":
        return said == gold
    return said is not None and said in A52.word_keys(gold)


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
                                 "right": said_right(said, gold, rd["kind"]),
                                 "read_right": int(logits[0].argmax()) in gold_set})  # fmt: skip
    return rows


def item_tokens(tok, it: dict) -> dict:
    """x51_answer.item_tokens with each reader's own answer kind: a digit answer's words are its number word's one-token
    variants (51.12's E1), a word answer's the first token of each variant (51.12's Z2); identical to x51_answer's on
    the number cells (tested)."""
    from scripts import suite_v1 as S
    from scripts import x51_answer as A51

    def word(rd: dict, x: str) -> str:
        return A51.number_word(x) if rd["kind"] == "digit" else str(x)

    def wids(rd: dict, ws: list[str]) -> list[int]:
        return A51.word_ids(tok, ws, rd["kind"] == "digit")

    a_ids: set[int] = set()
    a_words: list[str] = []
    for rd in it["readers"].values():
        ws = [word(rd, x) for x in rd["words_A"]]
        a_words += ws
        a_ids |= set(wids(rd, ws))
    a_words = list(dict.fromkeys(a_words))
    field = {"org": "answer", "alt": "cf_answer"}
    own_word = {v: {w: wids(rd, [word(rd, rd[f])]) for w, rd in it["readers"].items()} for v, f in field.items()}
    own = {v: {w: sorted(set(A51.variant_ids(tok, [rd[f]])) | set(own_word[v][w])) for w, rd in it["readers"].items()}
           for v, f in field.items()}  # fmt: skip
    bridge = {"org": A51.variant_ids(tok, [it["entity"]]), "alt": A51.variant_ids(tok, [it["cf_entity"]])}
    return {"A": sorted(a_ids), "A_words": a_words, "split_words": [w for w in a_words if len(S.ids(tok, w)) > 1],
            "own": own, "own_word": own_word, "bridge": bridge}  # fmt: skip


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


def manifest(name: str, target: str, layer: int, cells: tuple[str, ...], relation: str | None) -> dict:
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
    toks = [item_tokens(tok, it) for it in items]
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
        src = X.RESULTS / main_runs().get(pins.TARGET, "-")
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
    words = [c for c in cells if CELL[c][1] == "word"]
    assert not words or set(cells) <= set(WORD_CELLS), "the word cells run on their own (a run of their own name)"
    assert not words or target in WORD_RUNS, f"{target}: the word cells are {WORDS_STOPPED}"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    pairs = scene_pairs()
    m = manifest(name, target, layer, cells, None)
    word_ok, cov = True, None
    if words:
        from scripts import x45m

        cov = coverage(x45m.tokenizer(), pairs)
        rel_name = name_of(RELATION)
        if target == NINE_B:
            assert choose(cov) == rel_name, f"the relation rule picks {choose(cov)!r} on the 9B, not {rel_name!r}"
            nine = None
        else:  # the 9B's choice and accuracy check (its word run's relation.json; the job depends on the 9B's)
            path = RESULTS / WORD_RUNS[NINE_B] / "relation.json"
            assert path.exists(), f"{path}: the 9B's relation check is not here (run the 9B's word job first)"
            nine = json.loads(path.read_text())
            assert nine["relation"] == rel_name, f"the 9B's relation is {nine['relation']!r}, not {rel_name!r}"
        word_ok = nine is None or bool(nine["passes"])
        m |= {"relation": rel_name, "relation_question": RELATION_Q[RELATION], "word_instruction": WORD_INSTRUCTION,
              "relation_coverage": cov, "relation_9b": nine if nine is not None else "this run (relation.json)",
              "decision": "jobs/c3/batch53.yaml decision_531_words (Dan 10:20)"}  # fmt: skip
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
    if "qa_word" in gates and words:
        acc = gates["qa_word"]["org_read_accuracy"][X.RECALL]
        rel = {"relation": name_of(RELATION), "model": target, "accuracy_recall_qa_word": acc, "bar": X.GATE,
               "passes": acc >= X.GATE, "scenes": gates["qa_word"]["cases"], "coverage": cov}  # fmt: skip
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


def atom_context(tok, sc: dict, reader: str, vocab: dict[str, set[str]], kinds: dict[str, str]) -> dict:
    """x52_atoms.e1_context with each reader's answers matched by their kind: a digit answer by number_matcher (its
    number word, ordinal, digit), a word answer by word_answer_matcher (its keys, plural, first pieces); the answer kind
    also holds the relation's words in a word cell. Identical to e1_context on the number cells (tested)."""
    from scripts import x52_atoms as A52

    def answers(w: str) -> dict:
        a = sc["answers"][w]
        return A52.number_matcher(a) if kinds[w] == "digit" else A52.word_answer_matcher(tok, a)

    other = next(w for w in sc["answers"] if w != reader)
    in_scene = {sc["bridge"], sc["new"], *sc["items"]}
    dom = sc["domain"]
    kind_keys = set(A52.NUMBER_KIND)
    if "word" in kinds.values():
        kind_keys |= A52.word_keys_all(sorted(set(LEXICAL[RELATION[0]][RELATION[1]].values())))
    return {"bridge": A52.entity_matcher(tok, [sc["bridge"]], dom, spell=True),
            "new_bridge": A52.entity_matcher(tok, [sc["new"]], dom, spell=True),
            "scene_item": A52.entity_matcher(tok, sc["items"], dom), "person": A52.matcher(A52.word_keys_all(sc["persons"])),
            "answer_own": answers(reader), "answer_other": answers(other),
            "same_class": A52.entity_matcher(tok, sorted(vocab[dom] - in_scene), dom), "answer_kind": kind_keys,
            "prompt_keys": A52.prompt_keys(sc["text"])}  # fmt: skip


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
        kinds = {w: rd["kind"] for w, rd in cases[r["key"]]["readers"].items()}
        for view in X.READERS if after else (r["reader"],):
            ctx = atom_context(tok, sc, view, vocab, kinds)
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
        still = open_patterns(labels)
        return (f"can't tell: {', '.join(missing)} without a label (patterns the labelled cells leave open: "
                f"{', '.join(still) or 'none'})")  # fmt: skip
    if qb_n in am and qa_w == "entity":
        return "position"
    if qa_w in am and qb_n == "entity":
        return "readability"
    if qb_n == "mixed" and qa_w == "mixed" and qb_w == "answer":
        return "both"
    if all(v == "entity" for v in (qa_n, qb_n, qa_w, qb_w)):
        return "neither"
    return "none of the four patterns"


PATTERNS = ("position", "readability", "both", "neither")
LABEL_KEYS = ("entity", "answer", "mixed", "not_read", "na")


def open_patterns(labels: dict[str, str | None]) -> list[str]:
    """The patterns of the rule across cells that some labelling of the unlabelled cells would still give (every
    completion over 51.12's keys, the rule's own order); descriptive, beside a "can't tell"."""
    import itertools

    missing = [c for c in CELLS if labels.get(c) is None]
    found = set()
    for fill in itertools.product(LABEL_KEYS, repeat=len(missing)):
        found.add(across({**labels, **dict(zip(missing, fill, strict=True))}))
    return [p for p in PATTERNS if p in found]


def cross_check(cells: dict[str, dict]) -> dict:
    """The lookup's extra loss beyond random (the conflict test, arm 1) <= CROSS_MAX in all four cells (point
    estimates): holds when all four are at or below it; does not hold as soon as a tested cell is above it (the "all
    four" fails whatever the untested cells give); else can't tell."""
    per: dict[str, float | None] = {c: (r["lookup_extra"][0] if r.get("status") == "tested" else None)
                                    for c, r in cells.items()}  # fmt: skip
    known = {c: v for c, v in per.items() if v is not None and not math.isnan(v)}
    above = [c for c, v in known.items() if v > CROSS_MAX + EPS]
    held = False if above else (True if len(known) == len(per) else None)
    if held:
        text = "the pointer does not depend on the question (lookup <= 0.10 beyond random in all four cells)"
    elif held is False:
        text = "does not hold: the lookup loses > 0.10 beyond random in " + ", ".join(
            f"{CELL_TEXT[c]} ({known[c]:.2f})" for c in above)  # fmt: skip
    else:
        text = "can't tell (a cell without numbers; the tested ones <= 0.10)"
    return {"per_cell": per, "holds": held, "above": above, "text": text}


def model_verdict(target: str, n_boot: int) -> dict:
    """One model: the number cells from its number run, the word cells from its word run (each 'pending' while its run
    is not here)."""
    run, wrun = RUNS[target], WORD_RUNS.get(target)
    d = RESULTS / run
    dw = RESULTS / wrun if wrun else None
    if not (d / "manifest.json").exists() and not (dw and (dw / "manifest.json").exists()):
        return {"target": target, "run": run, "word_run": wrun, "status": "pending"}
    m = json.loads(((d if (d / "manifest.json").exists() else dw) / "manifest.json").read_text())  # type: ignore[operator]
    cells = {c: cell_result(d, c, target, n_boot) for c in NUMBER_CELLS}
    for c in WORD_CELLS:  # no word run for Muse and Lightning (Dan 11:10: the word cells stopped)
        cells[c] = cell_result(dw, c, target, n_boot) if dw else {"cell": c, "status": WORDS_STOPPED, "label": None}
    labels = {c: r.get("label") for c, r in cells.items()}
    rel = json.loads((dw / "relation.json").read_text()) if dw and (dw / "relation.json").exists() else None
    wm = json.loads((dw / "manifest.json").read_text()) if dw and (dw / "manifest.json").exists() else {}
    return {"target": target, "run": run, "word_run": wrun, "status": "run", "layer": m["layer"],
            "relation": wm.get("relation"), "relation_check": rel, "cells": cells, "across": across(labels),
            "cross_check": cross_check(cells), "position": position_rule(cells),
            "paired": paired_difference(d, cells, n_boot)}  # fmt: skip


ORDER_DEPENDENCE = "order dependence"


def paired_difference(d: Path, cells: dict[str, dict], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """Dan 11:25: the conflict test's lookup extra loss beyond random (X0's excess) in (Q-before, number) minus
    (Q-after, number), on the scenes both cells read, paired: one cluster bootstrap over the bridge entity (n_boot, seed)
    resamples both cells' rows with the same draws; 'order dependence' only if the 95% CI excludes 0."""
    if any(cells[c].get("status") != "tested" for c in NUMBER_CELLS):
        return {"text": "can't tell: a number cell not tested", "holds": None}
    sw: dict[str, dict[tuple[str, str], int]] = {}
    ent: dict[str, str] = {}
    for c in NUMBER_CELLS:
        for r in X.read_jsonl(d / c / "outcomes.jsonl"):
            if r["reader"] == X.LOOKUP and r["arm"] in ("whole", "no_jpp", "no_jpp_rand"):
                sw.setdefault(c, {})[(r["key"], r["arm"])] = int(r["sw"])
                ent[r["key"]] = r["entity"]
    keys = sorted({k for (k, _) in sw[NUMBER_CELLS[0]]} & {k for (k, _) in sw[NUMBER_CELLS[1]]})
    if not keys:
        return {"text": "can't tell: no scene read in both cells", "holds": None, "n": 0}
    series = {
        f"{c}|{a}": [sw[c][(k, a)] for k in keys] for c in NUMBER_CELLS for a in ("whole", "no_jpp", "no_jpp_rand")
    }
    ents = [ent[k] for k in keys]
    rr = X.resampled_rates(series, ents, n_boot, seed)

    def extra(rates: dict, c: str):
        with np.errstate(divide="ignore", invalid="ignore"):
            return (np.asarray(rates[f"{c}|no_jpp_rand"]) - np.asarray(rates[f"{c}|no_jpp"])) / np.asarray(
                rates[f"{c}|whole"])  # fmt: skip

    pt = {k: float(np.mean(v)) for k, v in series.items()}
    e = {c: float(extra(pt, c)) for c in NUMBER_CELLS}
    draws = extra(rr, "qb_num") - extra(rr, "qa_num")
    lo, hi = X.interval(draws)
    diff = e["qb_num"] - e["qa_num"]
    holds = bool(lo > 0 or hi < 0)
    text = (f"{ORDER_DEPENDENCE}: Q-before minus Q-after {diff:+.2f} [{lo:+.2f}, {hi:+.2f}]" if holds else
            f"the CI includes 0 ({diff:+.2f} [{lo:+.2f}, {hi:+.2f}]): no order dependence claimed")  # fmt: skip
    return {"n": len(keys), "entities": len(set(ents)), "lookup_extra_shared": e, "diff": [diff, lo, hi],
            "holds": holds, "text": f"{text} (the lookup's extra loss beyond random on the {len(keys)} scenes both "
            f"number cells read; cluster bootstrap over the bridge entity, {n_boot}, seed {seed})"}  # fmt: skip


def position_rule(cells: dict[str, dict]) -> dict:
    """Dan 11:10 across the two number cells of a model: the pointer does not depend on the question's position if the
    conflict test's lookup loses <= 0.10 beyond random (point estimates, X0's excess) in both; does not hold as soon as
    a tested number cell is above 0.10 (naming it: 'both' fails whatever the other gives); can't tell while a number
    cell is untested and none is above."""
    per: dict[str, float | None] = {c: (cells[c]["lookup_extra"][0] if cells[c].get("status") == "tested" else None)
                                    for c in NUMBER_CELLS}  # fmt: skip
    known = {c: v for c, v in per.items() if v is not None and not math.isnan(v)}
    above = [c for c, v in known.items() if v > CROSS_MAX + EPS]
    if above:
        holds, text = False, "does not hold: the lookup loses > 0.10 beyond random in " + ", ".join(
            f"{CELL_TEXT[c]} ({known[c]:.2f})" for c in above)  # fmt: skip
    elif len(known) == len(per):
        holds, text = True, f"{POSITION_HOLDS} (lookup <= 0.10 beyond random in both number cells)"
    else:
        untested = [CELL_TEXT[c] for c in NUMBER_CELLS if c not in known]
        holds, text = None, f"can't tell: {', '.join(untested)} not tested"
    return {"per_cell": per, "holds": holds, "above": above, "text": text}


def diag_lines(word_run: str) -> list[str]:
    """The newest word-cell diagnostic of this word run (diag_words-<UTC>/diag.json), as one descriptive line."""
    found = sorted(p for p in RESULTS.glob("diag_words-*/diag.json") if json.loads(p.read_text())["run"] == word_run)
    if not found:
        return []
    blob = json.loads(found[-1].read_text())
    parts = []
    for cell, c in blob["cells"].items():
        kinds = "; ".join(f"{k} {v}" for k, v in c["first_word_kinds"].items())
        parts.append(f"{CELL_TEXT[cell]} {kinds} (of {c['prompts']} recall prompts)")
    return [f"Descriptive context (results/{EXP}/{found[-1].parent.name}, CPU, no rule): what the recall's first word "
            "was: " + " | ".join(parts) + ".", ""]  # fmt: skip


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
             f"51.12's rule (x51_answer): {A51.RULE}", "", POSITION_RULE_TEXT + " As computed: the conflict test's "
             "lookup extra loss beyond random (X0's excess, point estimate) in (Q-after, number) and (Q-before, number); "
             "'does not hold' names a tested cell above 0.10; 'can't tell' while a cell is untested and none is above. "
             "Kept apart from the brief's rule across cells.", "",
             'Dan 11:25 (batch53.yaml critic_1125), verbatim: "Add the paired difference (Q-before minus Q-after) with '
             'its cluster-bootstrap CI, 27B now (CPU), Muse and Lightning when they land. Wording: "order dependence" '
             'only if that CI excludes 0." As computed: the lookup\'s extra loss beyond random (X0\'s excess) per cell '
             "on the scenes both number cells read; one cluster bootstrap over the bridge entity resamples both "
             "cells with the same draws.", "",
             "The evaluation logic of the cross-check (and of Dan 11:10's rule) was clarified after the data (Dan 11:25: "
             "the correct reading of 'in all four cells': 'does not hold' as soon as a tested cell exceeds 0.10).", "",
             "As computed: see scripts/x53_2x2.py's docstring (cells, relation, gate, conflict test, 51.12 arms, "
             "atoms). The cell's label is the recall's 51.12 label (51.12's decisive E1 reader); the lookup's beside. "
             f"Cluster bootstrap over the bridge entity ({X.N_BOOT}, seed {X.BOOT_SEED}).", ""]  # fmt: skip
    for mv in models:
        name = MODEL_SHORT.get(mv["target"], mv["target"])
        if mv["status"] != "run":
            lines += [f"## {name}: pending (no run {mv['run']} here)", ""]
            continue
        lines += [f"## {name} ({mv['run']}, L{mv['layer']}; relation for the word cells: {mv['relation']})", "",
                  *([MODEL_FLAGS[mv["target"]] + ".", ""] if mv["target"] in MODEL_FLAGS else []),
                  f"Across the number cells (Dan 11:10): **{mv['position']['text']}**.", "",
                  f"Paired difference (Dan 11:25): **{mv['paired']['text']}**.", "",
                  f"Rule across cells (the brief's): **{mv['across']}**. Cross-check: **{mv['cross_check']['text']}**.",
                  ""]  # fmt: skip
        if mv.get("relation_check"):
            rc = mv["relation_check"]
            cov = rc.get("coverage") or {}
            short = ", ".join(f"{k} {v['scenes']}" for k, v in cov.items() if not v["admissible"])
            dropped = sorted(cov.get(mv["relation"], {}).get("dropped_items", {}))
            lines += [f"Word cells: relation {mv['relation']} (question '{RELATION_Q[RELATION]}'), on the {rc['scenes']} "
                      f"scenes it answers, not 600 (Dan 10:20: coverage >= 150 on the 9B, then accuracy >= 0.80); "
                      f"checked and short of 150 scenes: {short or '-'}; items dropped for a clash with their own "
                      f"spelling, initial or symbol: {dropped or '-'}. The recall's O read accuracy on (Q-after, word) "
                      f"= {rc['accuracy_recall_qa_word']} on {rc['model']} (>= 0.80: {rc['passes']}; the 9B's decides).",
                      ""]  # fmt: skip
        lines += diag_lines(mv["word_run"]) if mv["word_run"] else []
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


def title_of(models: list[dict]) -> str:
    """The figure's title (<= 70 characters): Dan 11:10's rule across the number cells per model (holds / no / ? =
    can't tell / pending); the brief's rule across cells and the reasons are in the verdict."""
    parts = []
    for mv in models:
        h = mv.get("position", {}).get("holds", "pending") if mv["status"] == "run" else "pending"
        mark = {True: "yes", False: "no", None: "?"}.get(h, "pending")  # type: ignore[call-overload]
        parts.append(f"{MODEL_SHORT.get(mv['target'], mv['target'])} {mark}")
    t = "Both number cells <= 0.10: " + ", ".join(parts)
    return t if len(t) <= 70 else t[:67] + "..."


# Dan 11:55 (batch53.yaml decisions_1155, item 3): "When they land, the across-models line: "order dependence on n of 3
# models"" -- the three models whose Q-before run Dan named: the 27B, Muse and the 122B
ACROSS_MODELS = ("qwen3.6-27b", "muse-glimmer-30b", "qwen3.5-122b-a10b")
# per-model flags written beside the verdict (the coordinator, from Dan 11:30 / 11:55)
MODEL_FLAGS = {"qwen3.5-122b-a10b": "flags: L33 carried over (X0.md's rule for the 122B; relative depth 0.69); FP8 "
                                    "weights (Qwen3.5-122B-A10B-FP8, MoE, ~10B active); the J++ lens fit in bf16"}  # fmt: skip


def across_models(models: list[dict]) -> dict:
    """Dan 11:55's line over ACROSS_MODELS: n = the models whose paired difference (Dan 11:25) excludes 0; each model's
    case beside (order dependence / the CI includes 0 / can't tell, with why / pending)."""
    by = {m["target"]: m for m in models}
    per, n = {}, 0
    for t in ACROSS_MODELS:
        mv = by.get(t)
        if not mv or mv["status"] != "run":
            per[t] = "pending"
            continue
        p = mv["paired"]
        if p["holds"]:
            n += 1
            per[t] = f"order dependence ({p['diff'][0]:+.2f} [{p['diff'][1]:+.2f}, {p['diff'][2]:+.2f}])"
        elif p["holds"] is False:
            per[t] = f"the CI includes 0 ({p['diff'][0]:+.2f} [{p['diff'][1]:+.2f}, {p['diff'][2]:+.2f}])"
        else:
            g = next((mv["cells"][c] for c in NUMBER_CELLS if mv["cells"][c].get("status") != "tested"), {})
            per[t] = f"can't tell ({g.get('status', 'a number cell not tested')})"
    text = f"order dependence on {n} of {len(ACROSS_MODELS)} models (" + "; ".join(
        f"{MODEL_SHORT[t]}: {v}" for t, v in per.items()) + ")"  # fmt: skip
    return {"n": n, "of": len(ACROSS_MODELS), "per_model": per, "text": text}


def figure(models: list[dict], path: Path, extra: str = "") -> None:
    """One figure for the ledger card: per model a panel, per cell a row; the recall's three extra losses (arm 1
    without the J++ part, arm 2 with the answer directions kept, arm 3 the answer directions alone) and the lookup's arm
    1 (the cross-check, its <= 0.10 band shaded) as dots with 95% CIs; the cell's 51.12 label at the right."""
    from scripts import story_style as SS

    plt = SS.setup()
    run = [m for m in models if m["status"] == "run"] or models[:1]
    ncols = min(len(run), 2)  # two panels a row (four models: 2 x 2)
    nrows = math.ceil(len(run) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(SS.WIDTH, (0.9 + 0.75 * len(CELLS)) * nrows + 0.9), squeeze=False,
                             sharey=True)  # fmt: skip
    for ax in axes.flat[len(run) :]:
        ax.set_visible(False)
    marks = (("recall", "1", SS.COL["recall"], "o", "recall: without the J++ part"),
             ("recall", "2", SS.COL["recall"], "D", "recall: the J++ part, answer directions kept"),
             ("recall", "3", SS.COL["control"], "s", "recall: the answer directions alone"),
             ("lookup", "1", SS.COL["lookup"], "o", "lookup: without the J++ part (cross-check)"))  # fmt: skip
    for ax, mv in zip(axes.flat[: len(run)], run, strict=True):
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
                status = textwrap.fill(r["status"], 34 if len(run) > 1 else 60)  # fits a panel of two
                ax.text(0.45, y, status, va="center", ha="center", fontsize=SS.LABEL_PT - 1, color=SS.COL["muted"])
                continue
            for j, (w, k, col, mk, _) in enumerate(marks):
                v = r["readers"][w]["extra"][k]
                if v[0] is None or math.isnan(v[0]):
                    continue
                yy = y - 0.27 + 0.18 * j
                lo, hi = (v[1], v[2]) if not (math.isnan(v[1]) or math.isnan(v[2])) else (v[0], v[0])
                ax.errorbar(v[0], yy, xerr=[[v[0] - lo], [hi - v[0]]], fmt=mk, color=col, ms=6, lw=1.2, capsize=0)
            key = r["readers"]["recall"]["key"]  # in the row's lowest lane (the lookup's), clear of the recall's dots
            ax.text(1.0, y + 0.27, {"not_read": "not read", "na": "can't tell"}.get(key, key), va="center", ha="right",
                    fontsize=SS.LABEL_PT, color=SS.COL["muted"])  # fmt: skip
    from matplotlib.lines import Line2D

    handles = [Line2D([], [], marker=mk, color=col, ls="", label=t) for _, _, col, mk, t in marks]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=SS.LABEL_PT)
    SS.title(
        fig,
        title_of(run),
        (f"{extra} " if extra else "")
        + "? = can't tell; shaded: <= 0.10; right: the recall's 51.12 label. UNVERIFIED.",
    )
    fig.tight_layout(rect=(0, 0.12 / nrows, 1, 1 - 0.1 / nrows))
    fig.savefig(path, dpi=100)
    plt.close(fig)


def stage_verdict(n_boot: int = X.N_BOOT) -> Path:
    models = [model_verdict(t, n_boot) for t in MODEL_ORDER]
    across_m = across_models(models)
    out = RESULTS / f"x53_2x2-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    (out / "verdict.json").write_text(json.dumps({"models": models, "across_models": across_m}, indent=1,
                                                 default=float) + "\n")  # fmt: skip
    lines = verdict_lines(models)
    at = lines.index("Status: UNVERIFIED until a human adds it to VERIFIED.md.")
    lines[at:at] = [f"## Across models (Dan 11:55, over the {', '.join(MODEL_SHORT[t] for t in ACROSS_MODELS)})", "",
                    f"**{across_m['text']}**.", ""]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    figure(models, out / "x53_2x2.png", f"{across_m['text'].split(' (')[0].capitalize()} (Dan 11:55).")
    print("\n".join(lines[:40]), flush=True)
    print("wrote", out, flush=True)
    return out


# ---- the word cells' answer-format diagnostic (CPU, descriptive; coordinator 29 Oct after the 9B word run) -----------

N_SHOW_FAIL, DIAG_SEED, TAIL_TOKENS = 5, 0, 48


def first_word_kind(said: str | None, gold: str, item: str, scene_items: set[str], classes: set[str]) -> str:
    """What the recall's first word is: the gold class (or its plural), another class word, the asked pick itself (the
    animal, not its class), another item of the scene, or something else."""
    from scripts import x52_atoms as A52

    if said is None:
        return "no word"
    if said in A52.word_keys(gold):
        return "the class (right)"
    if any(said in A52.word_keys(c) for c in classes):
        return "another class word"
    if said in A52.word_keys(item):
        return "the asked pick itself (the animal)"
    if any(said in A52.word_keys(x) for x in scene_items):
        return "another animal of the scene"
    return "other"


def diag_rows(tok, cell: str, run_dir: Path) -> list[dict]:
    """Per recall prompt (O and S) of one word cell: the stored greedy text and said word, the first token of the greedy
    continuation (the read step's top token: greedy decoding takes it; re-encoded from the stored text), the gold class,
    the asked pick, and the first word's kind; the cases rebuilt on the tokenizer and matched scene by scene."""
    from scripts import x52_atoms as A52

    comp = [r for r in X.read_jsonl(run_dir / cell / "competence.jsonl") if r["reader"] == X.RECALL]
    cases, _ = build(tok, cell)
    by = {c["scene"]: c for c in cases}
    assert {r["scene"] for r in comp} == set(by), f"{cell}: the rebuilt scenes differ from the run's"
    classes = set(LEXICAL[RELATION[0]][RELATION[1]].values())
    out = []
    for r in comp:
        c = by[r["scene"]]
        rd = c["readers"][X.RECALL]
        v = r["variant"]
        gold = rd["said_A"] if v == "org" else rd["said_b"]
        item = c["entity"] if v == "org" else c["cf_entity"]
        sc = A52.e1_scene(c)
        scene_items = {sc["bridge"], sc["new"], *sc["items"]} - {item}
        first = ids(tok, r["greedy"])[:1]
        out.append({"cell": cell, "scene": r["scene"], "variant": v, "gold": gold, "item": item,
                    "greedy": r["greedy"], "said": r["said"], "right": r["right"], "read_right": r["read_right"],
                    "first_token": tok.decode(first) if first else "", "read_tokens": [tok.decode([t]) for t in
                    (rd["set_A"] if v == "org" else rd["set_b"])],
                    "kind": first_word_kind(r["said"], gold, item, scene_items, classes),
                    "tail": tok.decode(rd["ids"][v][-TAIL_TOKENS:])})  # fmt: skip
    return out


def stage_diag_words(run: str) -> Path:
    """The word cells' answer format on one run (Q-after vs Q-before): the first tokens the model produced, the kinds of
    its first words, the failures by gold class, and N_SHOW_FAIL random (Q-after) failures (seed DIAG_SEED) with their
    prompt tail; into results/x53_2x2/diag_words-<UTC>/ (note.md, diag.json). Descriptive; no rule."""
    import random

    from scripts import x45m

    tok = x45m.tokenizer()
    d = RESULTS / run
    m = json.loads((d / "manifest.json").read_text())
    assert m["model"]["target"] == pins.TARGET, f"{run} is {m['model']['target']}'s, BJ_TARGET is {pins.TARGET}"
    rows = {cell: diag_rows(tok, cell, d) for cell in WORD_CELLS}
    blob: dict[str, Any] = {"run": run, "target": pins.TARGET, "relation": m.get("relation"), "cells": {}}
    lines = [f"# 53.1 word cells: what the recall answered ({MODEL_SHORT.get(pins.TARGET, pins.TARGET)}, {run}; "
             "descriptive, UNVERIFIED)", "",
             "CPU only, from the run's stored competence rows (8 greedy tokens per unedited O / S prompt, the said word "
             "and the read); no rule, no rerun. The read step's top token is the greedy continuation's first token "
             "(greedy decoding takes it; re-encoded here from the stored text). Prompts rebuilt on the tokenizer and "
             "matched scene by scene. Descriptive context for the card only.", ""]  # fmt: skip
    for cell, rs in rows.items():
        n = len(rs)
        tokens = collections.Counter(r["first_token"] for r in rs)
        kinds = collections.Counter(r["kind"] for r in rs)
        by_gold = {g: {"n": sum(r["gold"] == g for r in rs), "read_wrong": sum(r["gold"] == g and not r["read_right"]
                                                                              for r in rs)}
                   for g in sorted({r["gold"] for r in rs})}  # fmt: skip
        blob["cells"][cell] = {"prompts": n, "read_right": sum(r["read_right"] for r in rs),
                               "said_right": sum(r["right"] for r in rs), "first_tokens": dict(tokens.most_common()),
                               "first_word_kinds": dict(kinds.most_common()), "by_gold": by_gold}  # fmt: skip
        lines += [f"## {CELL_TEXT[cell]}: recall, {n} prompts (O and S of each scene)", "",
                  f"Read right {blob['cells'][cell]['read_right']} / {n}; said right {blob['cells'][cell]['said_right']}"
                  f" / {n}.", "", "First word's kind: " + "; ".join(f"{k} {v}" for k, v in kinds.most_common()) + ".",
                  "", "Top first tokens: " + ", ".join(f"{t!r} {v}" for t, v in tokens.most_common(15)) + ".", "",
                  "Read wrong by gold class: " + "; ".join(f"{g} {v['read_wrong']} / {v['n']}" for g, v in by_gold.items())
                  + ".", ""]  # fmt: skip
    fails = [r for r in rows["qa_word"] if not r["read_right"]]
    pick = sorted(random.Random(DIAG_SEED).sample(range(len(fails)), min(N_SHOW_FAIL, len(fails))))
    before = {(r["scene"], r["variant"]): r for r in rows["qb_word"]}
    lines += [f"## {N_SHOW_FAIL} random (Q-after, word) failures (seed {DIAG_SEED}, of {len(fails)})", ""]
    shown = []
    for i in pick:
        r = fails[i]
        b = before.get((r["scene"], r["variant"]))
        shown.append({**r, "q_before": {k: b[k] for k in ("greedy", "read_right", "first_token")} if b else None})
        lines += [f"### {r['scene']} ({r['variant']}): asked pick {r['item']}, gold {r['gold']} (read tokens "
                  f"{r['read_tokens']})", "", "Prompt tail:", "", "```", r["tail"], "```", "",
                  f"(Q-after) greedy {r['greedy']!r}, first token {r['first_token']!r}, kind: {r['kind']}."
                  + (f" Same scene (Q-before): greedy {b['greedy']!r}, read right {b['read_right']}." if b else ""),
                  ""]  # fmt: skip
    blob["failures_shown"] = shown
    out = RESULTS / f"diag_words-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    (out / "diag.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "note.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["plan", "run", "verdict", "diag-words"])
    ap.add_argument("--name", help="run: the run name (results/x53_2x2/<name>/)")
    ap.add_argument("--cells", choices=("number", "word"), required=False,
                    help="run: the number cells (qa_num, qb_num) or the word cells (qa_word, qb_word), each a run of "
                         "its own (Dan 10:20)")  # fmt: skip
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        assert a.cells, "run needs --cells number|word"
        stage_run(a.name, NUMBER_CELLS if a.cells == "number" else WORD_CELLS)
    elif a.stage == "diag-words":
        stage_diag_words(a.name or WORD_RUNS[pins.TARGET])
    else:
        stage_verdict(a.n_boot)


if __name__ == "__main__":
    main()
