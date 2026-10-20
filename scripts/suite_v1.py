"""suite_v1: part B's consolidated prompt suite (Zach, 2026-10-19: consolidate, balance, avoid linearly related bridge
-> answer pairs such as France -> Paris, high quality, enough items per family for useful intervals).

Every family asks one question whose answer needs an intermediate variable (the bridge), in the chat format
(bridge_jspace.chat: one user turn, thinking off, "Answer:" prefilled), with a counterfactual C that changes only the
bridge (to X) and an off-path control O that changes something the answer does not depend on. C and O line up with the
clean prompt token for token (checked here), so exp04/exp09's copy-and-split runs apply unchanged.

The 2x2 core (one pool of 16 animals; the same context in all four families, only the question differs):
  BL  bound -> lookup:    "Jack's pet is a cow. ... The cow's locker is 5. ... Which locker belongs to Jack's pet?"
  BR  bound -> recall:    same context, "How many legs does Jack's pet have?"
  RL  recalled -> lookup: same context, "Which locker belongs to the animal known for mooing?"
  RR  recalled -> recall: same context, "How many legs does the animal known for mooing have?"
  Lockers are odd digits, legs even (2, 4, 6, 8): the two answer sets never overlap, and legs is many-to-one (many
  animals have 4), so an answer cannot stand in for its bridge the way Paris stands in for France. C: the queried
  person's pet swapped with another's (B*), or the cue replaced by another animal's (R*); O: the lockers of the two
  animals off the path swapped. BL/BR and RL/RR items come in pairs with the same prompts up to the question.
Tie-breakers (Zach, 2026-10-19; set "tiebreak", seed 102): in the 2x2, what uses the bridge also decides where the
answer comes from (a lookup answers from the prompt, a recall from memory). Two three-step families pull them apart,
built in pairs on one scene (same people and pets, same C):
  BLR bound -> lookup -> recall: "Jack's pet is a cow. ... The cow's friend is a spider. ... How many legs does the
      friend of Jack's pet have?" The pet is used by a lookup; the answer (8) comes from memory.
  BRL bound -> recall -> lookup: "Jack's pet is a cow. ... Animals with 4 legs use locker 7. ... Which locker does
      Jack's pet use?" The pet is used by a recall (4 legs); the answer (7) is read from the prompt.
  C swaps the queried person's pet with another's, as in BL/BR; O swaps the friends (BLR) or the lockers of two leg
  counts (BRL) off the pet's path. Each step alone is asked as hop1-hop3.
Generality (both hops in the prompt):
  NAMES  "Alice's partner is Ben. ... Ben's sister is Grace. ... Who is the sister of Alice's partner?"
  CODE   a two-dictionary Python lookup, "What does this Python code print?"
  (BREW, brew's colour-table chain, keeps its own item files and pipeline: data/brew_test.json, brew_fresh.json.)

Wording B (set "wording_b", seeds 201 and 202, data/suite_v1_b/): every family again in other words (WORDINGS), so
no result rests on one template: "Jack owns a cow. ... The cow uses locker 5. ... Which locker does the animal that
Jack owns use?"; "Alice is married to Ben. ... Ben's sister is called Grace."; CODE with key/lookup/values and a result
variable.

Difficulty pilot (set "dev", seed 9001, data/suite_v1_dev/; never a headline run's items): every family at two knobs,
entities per scene (3 or 5) and unrelated filler sentences woven among the facts (0 or 8), 100 items per cell, to see
which knob moves accuracy before choosing harder levels on fresh items.

Stages:  make --set S (write-once; tokenizer only)   verify (regenerates the main set, must equal its files)
         check --set S (alignment, uniqueness, balance)
         manifest --set S --name N --why W [--limit K]   competence --name N (every item: clean, C, O and each step
         alone, unedited; greedy text and one forced forward reading the answer token's probability; GPU)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins

DATA = pins.DATA_DIR / "suite_v1"
RESULTS = pins.RESULTS_DIR / "suite_v1"
FAMILIES = ("BL", "BR", "RL", "RR", "NAMES", "CODE")
TIEBREAK = ("BLR", "BRL")
N_PER_FAMILY = 400  # competence on every item; mechanistic runs sample >= 150 eligible (README: interval widths)
SEED = 101
TIEBREAK_SEED = 102
DEV = pins.DATA_DIR / "suite_v1_dev"
DEV_SEED = 9001
DEV_LEVELS = {"e3f0": (3, 0), "e5f0": (5, 0), "e3f8": (3, 8), "e5f8": (5, 8)}  # entities per scene, filler sentences
N_DEV = 100
DATA_B = pins.DATA_DIR / "suite_v1_b"  # wording B of every family (WORDINGS), its own seeds
WORDING_B_SEEDS = (201, 202)  # the 2x2, NAMES and CODE; the tie-breakers
# Computed bridges (Zach, 2026-10-20, quick experiment L3 after Neel's feedback: is a computed intermediate, never
# written in the prompt and not a recalled entity, carried in the J-space?): set "computed", data/computed_v1/.
COMPUTED = ("ARITH", "TYPO", "TRANS")
# Tool outputs (Zach, 2026-10-20, after Neel's "too toy"): BL and BR as an agent sees them, two JSON tool results
TOOL = ("TBL", "TBR")
DATA_T = pins.DATA_DIR / "suite_v1_tool"
TOOL_SEED = 601
DATA_C = pins.DATA_DIR / "computed_v1"
COMPUTED_SEED = 301
N_COMPUTED = 200
# Animal names in German and French (single words; the generator keeps those whose counterfactual lines up)
FOREIGN = {
    "de": {"dog": "Hund", "cat": "Katze", "frog": "Frosch", "cow": "Kuh", "horse": "Pferd", "mouse": "Maus",
           "wolf": "Wolf", "pig": "Schwein", "sheep": "Schaf", "lion": "Löwe", "duck": "Ente", "goose": "Gans",
           "chicken": "Huhn", "turkey": "Truthahn", "bee": "Biene", "spider": "Spinne"},
    "fr": {"dog": "chien", "cat": "chat", "frog": "grenouille", "cow": "vache", "horse": "cheval", "mouse": "souris",
           "wolf": "loup", "pig": "cochon", "sheep": "mouton", "lion": "lion", "duck": "canard", "goose": "oie",
           "chicken": "poulet", "turkey": "dinde", "bee": "abeille", "spider": "araignée"},
}  # fmt: skip
LANG_NAME = {"de": "German", "fr": "French"}
INSTRUCTION = chat.QUESTION_INSTRUCTION
# Animals: single tokens after a space, consonant-initial (so "a cow" / "a duck" keep the article and the alignment),
# each with a 2-token cue naming it alone (bleating: sheep or goat; stripes: tiger or zebra; mane: lion or horse;
# buzzing: bee or fly were dropped). Legs as commonly stated.
ANIMALS = {  # animal: (legs, cue for "the animal known for {cue}")
    "dog": (4, "barking"),
    "cat": (4, "purring"),
    "frog": (4, "croaking"),
    "cow": (4, "mooing"),
    "horse": (4, "neighing"),
    "mouse": (4, "squeaking"),
    "wolf": (4, "howling"),
    "pig": (4, "oinking"),
    "sheep": (4, "its wool"),
    "lion": (4, "its roar"),
    "duck": (2, "quacking"),
    "goose": (2, "honking"),
    "chicken": (2, "clucking"),
    "turkey": (2, "gobbling"),
    "bee": (6, "making honey"),
    "spider": (8, "spinning webs"),
}
LEG_WEIGHTS = {
    2: 0.35,
    4: 0.45,
    6: 0.1,
    8: 0.1,
}  # the bridge's legs: every value present, bridges not dominated by bee/spider
LOCKERS: tuple[int, ...] = (1, 3, 5, 7, 9)
FEMALE = ['Alice', 'Anna', 'Beth', 'Clara', 'Diana', 'Emma', 'Eva', 'Fiona', 'Grace', 'Iris', 'Julia', 'Kate', 'Laura', 'Lily', 'Lucy', 'Maria', 'Mia', 'Nina', 'Olivia', 'Rose', 'Sara', 'Tara', 'Vera', 'Zoe', 'Ella', 'Ruby', 'Amy', 'Eve', 'Ivy']  # fmt: skip
MALE = [
    "Adam",
    "Ben",
    "Carl",
    "Dan",
    "David",
    "Eric",
    "Finn",
    "Frank",
    "Henry",
    "Ivan",
    "Jack",
    "James",
    "Leo",
    "Luke",
    "Mark",
    "Max",
    "Noah",
    "Oscar",
    "Paul",
    "Peter",
    "Sam",
    "Tom",
    "Victor",
    "Will",
    "Hugo",
    "Owen",
    "Liam",
    "Ryan",
    "Sean",
    "Kyle",
]
PEOPLE = FEMALE + MALE
CODE_KEYS = ("cat", "dog", "cow", "fox", "owl", "pig", "bee", "ant", "rat", "bat", "hen", "elk")
CODE_VALUES = ("apple", "pear", "lime", "berry", "banana", "fig", "book", "lamp", "door", "tree", "ship", "coin", "key",
               "ring", "cup", "hat", "box", "pen", "car", "map", "star", "boat", "drum", "rose")  # fmt: skip
DIGITS = tuple(range(1, 10))
# Filler for the difficulty pilot: no digits, number words, names, animals or any word the questions use.
FILLER = ("The weather was mild all week.", "The bus was late again.", "The kitchen smelled of fresh bread.",
          "The garden gate needs new paint.", "The radio played old songs.", "The hallway lights were dim.",
          "The river was calm that morning.", "The market was busy on Saturday.", "The window faced the hills.",
          "The library closed early.", "The coffee was too strong.", "The road was wet after the rain.",
          "The museum had a new exhibit.", "The wind picked up in the evening.", "The train left on time.",
          "The bakery sold out of rolls.", "The park was quiet at dawn.", "The school held a concert.",
          "The street was lined with trees.", "The office was cold.", "The festival drew a large crowd.",
          "The sky turned grey by noon.", "The shop on the corner reopened.", "The tea had gone cold.")  # fmt: skip
CODE_FILLER = ("mode = 'fast'", "title = 'notes'", "debug = False", "items = []", "label = 'draft'", "ready = True",
               "status = 'open'", "color = 'blue'", "path = 'data'", "retries = None", "verbose = False",
               "owner = 'admin'")  # fmt: skip
# Two wordings of every family (Zach, 2026-10-19: no result should hang on one template). A is the main set's; B says
# the same facts and asks the same questions in other words (set "wording_b", data/suite_v1_b/). Same vocabulary, same
# token alignment of C and O, same structure.
WORDINGS: dict[str, dict[str, str]] = {
    "A": {
        "own": "{p}'s pet is a {a}.", "locker": "The {a}'s locker is {d}.",
        "BL": "Which locker belongs to {p}'s pet?", "BR": "How many legs does {p}'s pet have?",
        "RL": "Which locker belongs to the animal known for {cue}?",
        "RR": "How many legs does the animal known for {cue} have?",
        "hop_pet": "Which animal is {p}'s pet?", "hop_cue": "Which animal is known for {cue}?",
        "hop_locker": "Which locker belongs to the {a}?", "hop_legs": "How many legs does a {a} have?",
        "friend": "The {a}'s friend is a {f}.", "BLR": "How many legs does the friend of {p}'s pet have?",
        "hop_friend": "Which animal is the {a}'s friend?",
        "row": "Animals with {k} legs use locker {d}.", "BRL": "Which locker does {p}'s pet use?",
        "hop_row": "Which locker do animals with {k} legs use?",
        "partner": "{f}'s partner is {m}.", "sister": "{m}'s sister is {s}.",
        "NAMES": "Who is the sister of {f}'s partner?", "hop_partner": "Who is {f}'s partner?",
        "hop_sister": "Who is {m}'s sister?",
        "x": "x", "first": "first", "second": "second", "call": "print(second[first[x]])",
        "call1": "print(first[x])", "call2": "print(second['{v}'])", "CODE": "What does this Python code print?",
    },
    "B": {
        "own": "{p} owns a {a}.", "locker": "The {a} uses locker {d}.",
        "BL": "Which locker does the animal that {p} owns use?",
        "BR": "How many legs does the animal that {p} owns have?",
        "RL": "Which locker does the animal famous for {cue} use?",
        "RR": "How many legs does the animal famous for {cue} have?",
        "hop_pet": "What animal does {p} own?", "hop_cue": "Which animal is famous for {cue}?",
        "hop_locker": "Which locker does the {a} use?", "hop_legs": "What is the number of legs of a {a}?",
        "friend": "The {a}'s neighbour is a {f}.",
        "BLR": "How many legs does the neighbour of the animal that {p} owns have?",
        "hop_friend": "Which animal is the {a}'s neighbour?",
        "row": "Locker {d} is for animals with {k} legs.", "BRL": "Which locker does the animal that {p} owns use?",
        "hop_row": "Which locker is for animals with {k} legs?",
        "partner": "{f} is married to {m}.", "sister": "{m}'s sister is called {s}.",
        "NAMES": "Who is the sister of the man {f} is married to?", "hop_partner": "Who is {f} married to?",
        "hop_sister": "What is {m}'s sister called?",
        "x": "key", "first": "lookup", "second": "values", "call": "result = values[lookup[key]]\nprint(result)",
        "call1": "result = lookup[key]\nprint(result)", "call2": "result = values['{v}']\nprint(result)",
        "CODE": "What is the output of this program?",
    },
}  # fmt: skip


def tokenizer():
    from bridge_jspace.tokens import load_tokenizer

    return load_tokenizer()


def render(tok, context: str, question: str) -> str:
    """The prompt as every run feeds it: the context, the question and the instruction in one user turn, thinking off,
    the assistant turn prefilled "Answer:"."""
    return chat.chat_text(tok, f"{context}\n{question} {INSTRUCTION}")


def ids(tok, text: str) -> list[int]:
    return tok(text, add_special_tokens=False).input_ids


def layout(rng: random.Random, n_facts: int, n_fill: int, pool: tuple[str, ...]) -> list[int | str]:
    """Where filler goes among a scene's facts, fixed for all its prompts (clean, C, O, each step): fact indices in
    order with filler strings between them. No filler: the facts in order, and no draw from rng."""
    if not n_fill:
        return list(range(n_facts))
    fill = rng.sample(pool, n_fill)
    slots = sorted(rng.choices(range(n_facts + 1), k=n_fill))  # filler goes before fact i (n_facts: after the last)
    out: list[int | str] = []
    j = 0
    for i in range(n_facts + 1):
        while j < n_fill and slots[j] == i:
            out.append(fill[j])
            j += 1
        if i < n_facts:
            out.append(i)
    return out


def weave(facts: list[str], lay: list[int | str]) -> list[str]:
    return [facts[e] if isinstance(e, int) else e for e in lay]


# ---- the 2x2 core ---------------------------------------------------------------------------------------------------


def pick_bridge(rng: random.Random) -> str:
    legs = rng.choices(list(LEG_WEIGHTS), weights=list(LEG_WEIGHTS.values()))[0]
    return rng.choice([a for a, (n, _) in ANIMALS.items() if n == legs])


def core_scene(rng: random.Random, n: int = 3, n_fill: int = 0, w: dict[str, str] = WORDINGS["A"]) -> dict:
    """n people with n pets (the bridge I, the counterfactual X with other legs than I, a third Z, n - 3 more), each
    pet's locker (distinct odd digits), sentences in seeded orders, optional filler; the clean, C (B and R versions)
    and O contexts. At n = 3 without filler it draws exactly what suite_v1's main set drew (make's verify stage)."""
    assert 3 <= n <= len(LOCKERS)
    bridge = pick_bridge(rng)
    x = rng.choice([a for a in ANIMALS if ANIMALS[a][0] != ANIMALS[bridge][0]])
    z = rng.choice([a for a in ANIMALS if a not in (bridge, x)])
    more = rng.sample([a for a in ANIMALS if a not in (bridge, x, z)], n - 3) if n > 3 else []
    people = rng.sample(PEOPLE, n)
    pets = [bridge, x, z, *more]
    animals = list(pets)
    rng.shuffle(pets)  # who owns which, in sentence order
    lockers = dict(zip(animals, rng.sample(LOCKERS, n), strict=True))
    table_order = rng.sample(animals, n)
    lay = layout(rng, 2 * n, n_fill, FILLER)

    def context(owner_pets: list[str], locks: dict[str, int]) -> str:
        own = [w["own"].format(p=p, a=a) for p, a in zip(people, owner_pets, strict=True)]
        table = [w["locker"].format(a=a, d=locks[a]) for a in table_order]
        return " ".join(weave(own + table, lay))

    holder = people[pets.index(bridge)]
    swapped = list(pets)
    i, j = pets.index(bridge), pets.index(x)
    swapped[i], swapped[j] = swapped[j], swapped[i]
    off_locks = dict(lockers)
    off_locks[x], off_locks[z] = lockers[z], lockers[x]
    return {
        "bridge": bridge,
        "x": x,
        "z": z,
        "holder": holder,
        "people": people,
        "pets": pets,
        "lockers": lockers,
        "context": context(pets, lockers),
        "cf_context_b": context(swapped, lockers),  # B*: the holder now owns X
        "off_context": context(pets, off_locks),  # X's and Z's lockers swapped: off I's path
    }


def core_items(
    rng: random.Random, n: int, n_ent: int = 3, n_fill: int = 0, w: dict[str, str] = WORDINGS["A"]
) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {f: [] for f in ("BL", "BR", "RL", "RR")}
    seen = set()
    k = 0
    while len(out["BL"]) < n:
        s = core_scene(rng, n_ent, n_fill, w)
        if s["context"] in seen:
            continue
        seen.add(s["context"])
        b, x, holder = s["bridge"], s["x"], s["holder"]
        cue_b, cue_x = ANIMALS[b][1], ANIMALS[x][1]
        legs_b, legs_x = ANIMALS[b][0], ANIMALS[x][0]
        lock_b, lock_x = s["lockers"][b], s["lockers"][x]
        base = {"scene": f"S-{k:04d}", "bridge": b, "cf_bridge": x, "third": s["z"], "context": s["context"],
                "off_context": s["off_context"], "people": s["people"], "pets": s["pets"], "lockers": s["lockers"]}  # fmt: skip
        hop1_b = {"question": w["hop_pet"].format(p=holder), "answer": b, "kind": "animal"}
        hop1_r = {"question": w["hop_cue"].format(cue=cue_b), "answer": b, "kind": "animal"}
        hop2_l = {"question": w["hop_locker"].format(a=b), "answer": str(lock_b), "kind": "digit"}
        hop2_r = {"question": w["hop_legs"].format(a=b), "answer": str(legs_b), "kind": "digit"}
        q = {
            "BL": (w["BL"].format(p=holder), None, lock_b, lock_x, hop1_b, hop2_l, holder),
            "BR": (w["BR"].format(p=holder), None, legs_b, legs_x, hop1_b, hop2_r, holder),
            "RL": (w["RL"].format(cue=cue_b), w["RL"].format(cue=cue_x), lock_b, lock_x, hop1_r, hop2_l, cue_b),
            "RR": (w["RR"].format(cue=cue_b), w["RR"].format(cue=cue_x), legs_b, legs_x, hop1_r, hop2_r, cue_b),
        }
        for fam, (question, cf_question, ans, cf_ans, h1, h2, cue) in q.items():
            bound = fam.startswith("B")
            out[fam].append(
                {
                    "id": f"{fam}-{len(out[fam]):04d}",
                    "family": fam,
                    **base,
                    "cue": cue,
                    "question": question,
                    "cf_context": s["cf_context_b"] if bound else s["context"],
                    "cf_question": question if bound else cf_question,
                    "answer": str(ans),
                    "cf_answer": str(cf_ans),
                    "answer_kind": "digit",
                    "hop1": h1,
                    "hop2": h2,
                }
            )
        k += 1
    return out


# ---- tie-breakers: what uses the bridge vs where the answer comes from --------------------------------------------


LEG_COUNTS: tuple[int, ...] = (2, 4, 6, 8)


def tiebreak_items(
    rng: random.Random, n: int, n_ent: int = 3, n_fill: int = 0, w: dict[str, str] = WORDINGS["A"]
) -> dict[str, list[dict]]:
    """BLR and BRL items in pairs: one scene (people, pets, holder, I and X with other legs, Z), then BLR's friends
    table or BRL's legs-to-locker table. Both C's swap the holder's and X's owner's pets, so the pair shares its bridge
    and its edit; BLR also needs I's and X's friends to differ in legs, so that C changes its answer."""
    out: dict[str, list[dict]] = {f: [] for f in TIEBREAK}
    seen = set()
    while len(out["BLR"]) < n:
        bridge = pick_bridge(rng)
        x = rng.choice([a for a in ANIMALS if ANIMALS[a][0] != ANIMALS[bridge][0]])
        z = rng.choice([a for a in ANIMALS if a not in (bridge, x)])
        more = rng.sample([a for a in ANIMALS if a not in (bridge, x, z)], n_ent - 3) if n_ent > 3 else []
        animals = [bridge, x, z, *more]
        people = rng.sample(PEOPLE, n_ent)
        pets = list(animals)
        rng.shuffle(pets)
        holder = people[pets.index(bridge)]
        # BLR: friends are animals outside the scene's pets, so "the friend of X's pet" never names a pet
        others = [a for a in ANIMALS if a not in animals]
        f_i = pick_bridge(rng)
        while f_i not in others:
            f_i = pick_bridge(rng)
        f_x = rng.choice([a for a in others if a != f_i and ANIMALS[a][0] != ANIMALS[f_i][0]])
        rest = rng.sample([a for a in others if a not in (f_i, f_x)], n_ent - 2)
        friend = dict(zip(animals, [f_i, f_x, *rest], strict=True))
        friend_order = rng.sample(animals, n_ent)
        # BRL: every leg count gets a locker, in a seeded order
        table = dict(zip(LEG_COUNTS, rng.sample(LOCKERS, len(LEG_COUNTS)), strict=True))
        table_order = rng.sample(LEG_COUNTS, len(LEG_COUNTS))
        legs_i, legs_x = ANIMALS[bridge][0], ANIMALS[x][0]
        k_off = rng.choice([k for k in LEG_COUNTS if k not in (legs_i, legs_x)])
        lay_r = layout(rng, 2 * n_ent, n_fill, FILLER)
        lay_l = layout(rng, n_ent + len(LEG_COUNTS), n_fill, FILLER)

        def own(owner_pets, people=people):
            return [w["own"].format(p=p, a=a) for p, a in zip(people, owner_pets, strict=True)]

        def blr_context(owner_pets, fr, friend_order=friend_order, lay=lay_r):
            return " ".join(weave(own(owner_pets) + [w["friend"].format(a=a, f=fr[a]) for a in friend_order], lay))

        def brl_context(owner_pets, tab, table_order=table_order, lay=lay_l):
            rows = [w["row"].format(k=k, d=tab[k]) for k in table_order]
            return " ".join(weave(own(owner_pets) + rows, lay))

        swapped = list(pets)
        i, j = pets.index(bridge), pets.index(x)
        swapped[i], swapped[j] = swapped[j], swapped[i]
        off_friend = dict(friend)
        off_friend[x], off_friend[z] = friend[z], friend[x]
        off_table = dict(table)
        off_table[legs_x], off_table[k_off] = table[k_off], table[legs_x]  # X's row and another, both off I's path
        ctx = blr_context(pets, friend)
        if ctx in seen:
            continue
        seen.add(ctx)
        base = {"scene": f"T-{len(out['BLR']):04d}", "bridge": bridge, "cf_bridge": x, "third": z, "people": people,
                "pets": pets, "holder": holder, "cue": holder, "answer_kind": "digit"}  # fmt: skip
        hop1 = {"question": w["hop_pet"].format(p=holder), "answer": bridge, "kind": "animal"}
        out["BLR"].append({
            "id": f"BLR-{len(out['BLR']):04d}", "family": "BLR", **base, "friends": friend,
            "context": ctx, "cf_context": blr_context(swapped, friend), "off_context": blr_context(pets, off_friend),
            "question": (q := w["BLR"].format(p=holder)), "cf_question": q,
            "mid": f_i, "cf_mid": f_x, "answer": str(ANIMALS[f_i][0]), "cf_answer": str(ANIMALS[f_x][0]),
            "hop1": hop1,
            "hop2": {"question": w["hop_friend"].format(a=bridge), "answer": f_i, "kind": "animal"},
            "hop3": {"question": w["hop_legs"].format(a=f_i), "answer": str(ANIMALS[f_i][0]), "kind": "digit"},
        })  # fmt: skip
        out["BRL"].append({
            "id": f"BRL-{len(out['BRL']):04d}", "family": "BRL", **base, "leg_lockers": {str(k): v for k, v in table.items()},
            "context": brl_context(pets, table), "cf_context": brl_context(swapped, table),
            "off_context": brl_context(pets, off_table),
            "question": (q := w["BRL"].format(p=holder)), "cf_question": q,
            "mid": str(legs_i), "cf_mid": str(legs_x), "answer": str(table[legs_i]), "cf_answer": str(table[legs_x]),
            "hop1": hop1,
            "hop2": {"question": w["hop_legs"].format(a=bridge), "answer": str(legs_i), "kind": "digit"},
            "hop3": {"question": w["hop_row"].format(k=legs_i), "answer": str(table[legs_i]),
                     "kind": "digit"},
        })  # fmt: skip
    return out


# ---- generality families --------------------------------------------------------------------------------------------


def names_items(
    rng: random.Random, n: int, n_ent: int = 3, n_fill: int = 0, w: dict[str, str] = WORDINGS["A"]
) -> list[dict]:
    out, seen = [], set()
    while len(out) < n:
        f = rng.sample(FEMALE, 2 * n_ent)
        m = rng.sample(MALE, n_ent)
        askers, sisters = f[:n_ent], f[n_ent:]
        partner = dict(zip(askers, m, strict=True))
        sister = dict(zip(m, sisters, strict=True))
        q = rng.randrange(n_ent)
        o = rng.choice([i for i in range(n_ent) if i != q])
        z = next(i for i in range(n_ent) if i not in (q, o))
        a_order, s_order = rng.sample(range(n_ent), n_ent), rng.sample(range(n_ent), n_ent)
        lay = layout(rng, 2 * n_ent, n_fill, FILLER)

        def context(part, sis, askers=askers, m=m, a_order=a_order, s_order=s_order, lay=lay) -> str:
            first = [w["partner"].format(f=askers[i], m=part[askers[i]]) for i in a_order]
            second = [w["sister"].format(m=m[i], s=sis[m[i]]) for i in s_order]
            return " ".join(weave(first + second, lay))

        cf_part = dict(partner)
        cf_part[askers[q]], cf_part[askers[o]] = partner[askers[o]], partner[askers[q]]
        off_sis = dict(sister)
        off_sis[m[o]], off_sis[m[z]] = sister[m[z]], sister[m[o]]
        ctx = context(partner, sister)
        if ctx in seen:
            continue
        seen.add(ctx)
        bridge, x = m[q], m[o]
        out.append(
            {
                "id": f"NAMES-{len(out):04d}",
                "family": "NAMES",
                "context": ctx,
                "cf_context": context(cf_part, sister),
                "off_context": context(partner, off_sis),
                "question": w["NAMES"].format(f=askers[q]),
                "cf_question": w["NAMES"].format(f=askers[q]),
                "cue": askers[q],
                "bridge": bridge,
                "cf_bridge": x,
                "third": m[z],
                "answer": sister[bridge],
                "cf_answer": sister[x],
                "answer_kind": "name",
                "hop1": {"question": w["hop_partner"].format(f=askers[q]), "answer": bridge, "kind": "name"},
                "hop2": {"question": w["hop_sister"].format(m=bridge), "answer": sister[bridge], "kind": "name"},
            }
        )
    return out


def code_items(
    rng: random.Random,
    n: int,
    keys: list[str],
    values: list[str],
    n_ent: int = 3,
    n_fill: int = 0,
    w: dict[str, str] = WORDINGS["A"],
) -> list[dict]:
    out, seen = [], set()
    while len(out) < n:
        k = rng.sample(keys, n_ent)
        v = rng.sample(values, n_ent)
        d = rng.sample(DIGITS, n_ent)
        first = dict(zip(k, v, strict=True))
        second = dict(zip(v, d, strict=True))
        q = rng.randrange(n_ent)
        o = rng.choice([i for i in range(n_ent) if i != q])
        z = next(i for i in range(n_ent) if i not in (q, o))
        o1, o2 = rng.sample(range(n_ent), n_ent), rng.sample(range(n_ent), n_ent)
        lay = layout(rng, 3, n_fill, CODE_FILLER)

        def code(x, sec, call=w["call"], k=k, v=v, first=first, o1=o1, o2=o2, lay=lay) -> str:
            f_txt = ", ".join(f"'{k[i]}': '{first[k[i]]}'" for i in o1)
            s_txt = ", ".join(f"'{v[i]}': {sec[v[i]]}" for i in o2)
            lines = weave([f"{w['x']} = '{x}'", f"{w['first']} = {{{f_txt}}}", f"{w['second']} = {{{s_txt}}}"], lay)
            return "```python\n" + "\n".join(lines) + f"\n{call}\n```"

        off_sec = dict(second)
        off_sec[v[o]], off_sec[v[z]] = second[v[z]], second[v[o]]
        ctx = code(k[q], second)
        if ctx in seen:
            continue
        seen.add(ctx)
        question = w["CODE"]
        out.append(
            {
                "id": f"CODE-{len(out):04d}",
                "family": "CODE",
                "context": ctx,
                "cf_context": code(k[o], second),
                "off_context": code(k[q], off_sec),
                "question": question,
                "cf_question": question,
                "cue": k[q],
                "bridge": v[q],
                "cf_bridge": v[o],
                "third": v[z],
                "answer": str(second[v[q]]),
                "cf_answer": str(second[v[o]]),
                "answer_kind": "digit",
                "hop1": {"question": question, "answer": v[q], "kind": "fruit", "context": code(k[q], second, w["call1"])},
                "hop2": {"question": question, "answer": str(second[v[q]]), "kind": "digit",
                         "context": code(k[q], second, w["call2"].format(v=v[q]))},
            }
        )  # fmt: skip
    return out


# ---- computed bridges ------------------------------------------------------------------------------------------------


def typo(word: str, rng: random.Random) -> str:
    """A one-edit misspelling: two inner letters swapped, or one inner letter dropped or doubled."""
    i = rng.randrange(1, max(2, len(word) - 1))
    kind = rng.choice(("swap", "drop", "double")) if len(word) > 3 else "double"
    if kind == "swap" and i + 1 < len(word) and word[i] != word[i + 1]:
        return word[:i] + word[i + 1] + word[i] + word[i + 2 :]
    if kind == "drop":
        return word[:i] + word[i + 1 :]
    return word[:i] + word[i] + word[i:]


def computed_items(rng: random.Random, tok, n: int) -> dict[str, list[dict]]:
    """ARITH: (a + b) x c, the bridge a + b (one digit) never written; TYPO and TRANS: a misspelled or German/French
    animal name, the bridge the English animal (never written), then its legs. C changes the bridge (aligned token for
    token, a different answer); O changes the asker's name in the context (off the path)."""
    out: dict[str, list[dict]] = {f: [] for f in COMPUTED}

    def n_tok(text: str) -> int:
        return len(ids(tok, text))

    seen: set[str] = set()
    while len(out["ARITH"]) < n:
        a, b, c = rng.randint(1, 8), rng.randint(1, 8), rng.randint(2, 9)
        s_ = a + b
        b2 = rng.randint(1, 8)
        s2 = a + b2
        if s_ > 9 or s2 > 9 or s2 == s_ or str(s_ * c)[0] == str(s2 * c)[0]:
            continue
        p, p2 = rng.sample(PEOPLE, 2)
        key = f"{a}+{b}x{c}{p}"
        if key in seen:
            continue
        seen.add(key)
        q, q2 = f"What is ({a} + {b}) × {c}?", f"What is ({a} + {b2}) × {c}?"
        out["ARITH"].append({
            "id": f"ARITH-{len(out['ARITH']):04d}", "family": "ARITH", "scene": f"A-{len(out['ARITH']):04d}",
            "context": f"Here is a sum for {p}.", "cf_context": f"Here is a sum for {p}.",
            "off_context": f"Here is a sum for {p2}.", "question": q, "cf_question": q2,
            "bridge": str(s_), "cf_bridge": str(s2), "cue": f"{a} + {b}", "answer": str(s_ * c), "cf_answer": str(s2 * c),
            "answer_kind": "digit",
            "hop1": {"question": f"What is {a} + {b}?", "answer": str(s_), "kind": "digit"},
            "hop2": {"question": f"What is {s_} × {c}?", "answer": str(s_ * c), "kind": "digit"},
        })  # fmt: skip
    for fam in ("TYPO", "TRANS"):
        tries = 0
        while len(out[fam]) < n and tries < 200_000:
            tries += 1
            bridge = pick_bridge(rng)
            x = rng.choice([a for a in ANIMALS if ANIMALS[a][0] != ANIMALS[bridge][0]])
            p, p2 = rng.sample(PEOPLE, 2)
            if fam == "TYPO":
                w, w2 = typo(bridge, rng), typo(x, rng)
                if w in ANIMALS or w2 in ANIMALS or w == bridge or w2 == x:
                    continue
                shown, shown2, lang = w, w2, None
                q = f"How many legs does a {w} have?"
                q2 = f"How many legs does a {w2} have?"
                h1 = f"Which animal is '{w}' a misspelling of?"
                ctx = f"Here is a quick question from {p}."
                off = f"Here is a quick question from {p2}."
            else:
                lang = rng.choice(("de", "fr"))
                shown, shown2 = FOREIGN[lang][bridge], FOREIGN[lang][x]
                if shown.lower() == bridge or shown2.lower() == x:  # 'lion', 'wolf': the English word itself
                    continue
                q = f"How many legs does the animal called « {shown} » in {LANG_NAME[lang]} have?"
                q2 = f"How many legs does the animal called « {shown2} » in {LANG_NAME[lang]} have?"
                h1 = f"Which animal is called « {shown} » in {LANG_NAME[lang]}? Answer in English."
                ctx = f"Here is a question from {p}, who is reading a {LANG_NAME[lang]} book."
                off = f"Here is a question from {p2}, who is reading a {LANG_NAME[lang]} book."
            if n_tok(" " + shown) != n_tok(" " + shown2) or n_tok(q) != n_tok(q2):
                continue
            key = f"{fam}{q}{p}"
            if key in seen:
                continue
            seen.add(key)
            out[fam].append({
                "id": f"{fam}-{len(out[fam]):04d}", "family": fam, "scene": f"{fam[0]}-{len(out[fam]):04d}",
                "context": ctx, "cf_context": ctx, "off_context": off, "question": q, "cf_question": q2,
                "bridge": bridge, "cf_bridge": x, "cue": shown, "shown": shown, "cf_shown": shown2, "lang": lang,
                "answer": str(ANIMALS[bridge][0]), "cf_answer": str(ANIMALS[x][0]), "answer_kind": "digit",
                "hop1": {"question": h1, "answer": bridge, "kind": "animal"},
                "hop2": {"question": f"How many legs does a {bridge} have?", "answer": str(ANIMALS[bridge][0]),
                         "kind": "digit"},
            })  # fmt: skip
    return out


# ---- tool outputs -------------------------------------------------------------------------------------------------------


def tool_items(rng: random.Random, tok, n: int) -> dict[str, list[dict]]:
    """TBL / TBR on one context: get_profiles (three people's pets) and get_vets (each pet's vet) as JSON. TBL asks
    which vet looks after a person's pet (a lookup in the second result), TBR how many legs it has (a recalled fact).
    C swaps the person's and X's owner's pets in get_profiles; O swaps X's and Z's vets in get_vets."""
    animals = [a for a in ANIMALS if len(ids(tok, a)) == 1]  # inside JSON quotes: no leading space
    out: dict[str, list[dict]] = {f: [] for f in TOOL}
    seen: set[str] = set()
    while len(out["TBL"]) < n:
        bridge = pick_bridge(rng)
        if bridge not in animals:
            continue
        x = rng.choice([a for a in animals if ANIMALS[a][0] != ANIMALS[bridge][0]])
        z = rng.choice([a for a in animals if a not in (bridge, x)])
        names = rng.sample(PEOPLE, 6)
        people, vets = names[:3], names[3:]
        pets = [bridge, x, z]
        rng.shuffle(pets)
        vet_of = dict(zip([bridge, x, z], vets, strict=True))
        vet_order = rng.sample([bridge, x, z], 3)
        holder = people[pets.index(bridge)]

        def context(owner_pets, vet_map, people=people, vet_order=vet_order) -> str:
            prof = ", ".join(f'{{"name": "{p}", "pet": "{a}"}}' for p, a in zip(people, owner_pets, strict=True))
            vt = ", ".join(f'{{"pet": "{a}", "vet": "{vet_map[a]}"}}' for a in vet_order)
            return f"Tool output from get_profiles:\n[{prof}]\nTool output from get_vets:\n[{vt}]"

        swapped = list(pets)
        i, j = pets.index(bridge), pets.index(x)
        swapped[i], swapped[j] = swapped[j], swapped[i]
        off_vets = dict(vet_of)
        off_vets[x], off_vets[z] = vet_of[z], vet_of[x]
        ctx = context(pets, vet_of)
        if ctx in seen:
            continue
        seen.add(ctx)
        base = {"scene": f"TOOL-{len(out['TBL']):04d}", "bridge": bridge, "cf_bridge": x, "third": z, "people": people,
                "pets": pets, "vets": vet_of, "cue": holder, "context": ctx, "cf_context": context(swapped, vet_of)}  # fmt: skip
        hop1 = {"question": f"Which animal is {holder}'s pet?", "answer": bridge, "kind": "animal"}
        out["TBL"].append({
            "id": f"TBL-{len(out['TBL']):04d}", "family": "TBL", **base, "off_context": context(pets, off_vets),
            "question": (q := f"Which vet looks after {holder}'s pet?"), "cf_question": q,
            "answer": vet_of[bridge], "cf_answer": vet_of[x], "answer_kind": "name", "hop1": hop1,
            "hop2": {"question": f"Which vet looks after the {bridge}?", "answer": vet_of[bridge], "kind": "name"},
        })  # fmt: skip
        out["TBR"].append({
            "id": f"TBR-{len(out['TBR']):04d}", "family": "TBR", **base, "off_context": context(pets, off_vets),
            "question": (q := f"How many legs does {holder}'s pet have?"), "cf_question": q,
            "answer": str(ANIMALS[bridge][0]), "cf_answer": str(ANIMALS[x][0]), "answer_kind": "digit", "hop1": hop1,
            "hop2": {"question": f"How many legs does a {bridge} have?", "answer": str(ANIMALS[bridge][0]), "kind": "digit"},
        })  # fmt: skip
    return out


# ---- stages ---------------------------------------------------------------------------------------------------------


def generate(which: str, tok) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note) for a set. Each set has its own seed, so adding one never changes
    another's items."""
    assert all(len(ids(tok, " " + a)) == 1 for a in ANIMALS), "an animal is not one token"
    assert all(len(ids(tok, " " + c)) == 2 for _, c in ANIMALS.values()), "a cue is not two tokens"
    assert all(len(ids(tok, " " + p)) == 1 for p in PEOPLE), "a name is not one token"
    keys = [w for w in CODE_KEYS if len(ids(tok, w)) == 1]  # inside quotes: no leading space
    values = [w for w in CODE_VALUES if len(ids(tok, w)) == 1]
    if which == "main":
        rng = random.Random(SEED)
        fams = {**core_items(rng, N_PER_FAMILY), "NAMES": names_items(rng, N_PER_FAMILY),
                "CODE": code_items(rng, N_PER_FAMILY, keys, values)}  # fmt: skip
        return {f: (DATA / f"{f}.json", it, f"scripts/suite_v1.py make (seed {SEED})") for f, it in fams.items()}
    if which == "tiebreak":
        fams = tiebreak_items(random.Random(TIEBREAK_SEED), N_PER_FAMILY)
        note = f"scripts/suite_v1.py make --set tiebreak (seed {TIEBREAK_SEED})"
        return {f: (DATA / f"{f}.json", it, note) for f, it in fams.items()}
    if which == "tool":
        fams = tool_items(random.Random(TOOL_SEED), tok, N_PER_FAMILY)
        note = f"scripts/suite_v1.py make --set tool (seed {TOOL_SEED})"
        return {f: (DATA_T / f"{f}.json", it, note) for f, it in fams.items()}
    if which == "computed":
        fams = computed_items(random.Random(COMPUTED_SEED), tok, N_COMPUTED)
        note = f"scripts/suite_v1.py make --set computed (seed {COMPUTED_SEED})"
        return {f: (DATA_C / f"{f}.json", it, note) for f, it in fams.items()}
    if which == "wording_b":
        w = WORDINGS["B"]
        rng = random.Random(WORDING_B_SEEDS[0])
        fams = {**core_items(rng, N_PER_FAMILY, w=w), "NAMES": names_items(rng, N_PER_FAMILY, w=w),
                "CODE": code_items(rng, N_PER_FAMILY, keys, values, w=w),
                **tiebreak_items(random.Random(WORDING_B_SEEDS[1]), N_PER_FAMILY, w=w)}  # fmt: skip
        note = f"scripts/suite_v1.py make --set wording_b (seeds {WORDING_B_SEEDS})"
        return {f: (DATA_B / f"{f}.json", it, note) for f, it in fams.items()}
    assert which == "dev"
    out = {}
    for k, (level, (n_ent, n_fill)) in enumerate(DEV_LEVELS.items()):
        rng = random.Random(DEV_SEED * 10 + k)
        fams = {**core_items(rng, N_DEV, n_ent, n_fill), "NAMES": names_items(rng, N_DEV, n_ent, n_fill),
                "CODE": code_items(rng, N_DEV, keys, values, n_ent, n_fill), **tiebreak_items(rng, N_DEV, n_ent, n_fill)}  # fmt: skip
        note = f"scripts/suite_v1.py make --set dev (seed {DEV_SEED * 10 + k}: {n_ent} entities, {n_fill} filler)"
        for f, it in fams.items():
            for item in it:
                item["level"] = level
            out[f"{f}_{level}"] = (DEV / f"{f}_{level}.json", it, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    if which == "main":
        return {f: DATA / f"{f}.json" for f in FAMILIES}
    if which == "tiebreak":
        return {f: DATA / f"{f}.json" for f in TIEBREAK}
    if which == "wording_b":
        return {f: DATA_B / f"{f}.json" for f in FAMILIES + TIEBREAK}
    if which == "computed":
        return {f: DATA_C / f"{f}.json" for f in COMPUTED}
    if which == "tool":
        return {f: DATA_T / f"{f}.json" for f in TOOL}
    return {f"{f}_{lv}": DEV / f"{f}_{lv}.json" for lv in DEV_LEVELS for f in FAMILIES + TIEBREAK}


def stage_make(which: str) -> None:
    tok = tokenizer()
    for label, (path, items, note) in generate(which, tok).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        blob = {"family": label, "generator": note, "format": (__doc__ or "").split("\n\n")[1], "items": items}
        path.write_text(json.dumps(blob, indent=1) + "\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    """Every set regenerated from this code equals its files (the generators gained knobs and wordings; at each set's
    settings they must draw exactly as before)."""
    tok = tokenizer()
    for which in ("main", "tiebreak", "dev", "wording_b", "computed", "tool"):
        for label, (path, items, _) in generate(which, tok).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = json.loads(path.read_text())["items"] == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def load_file(path: Path) -> list[dict]:
    return json.loads(path.read_text())["items"]


def data_dir(wording: str) -> Path:
    return {"A": DATA, "B": DATA_B, "C": DATA_C, "T": DATA_T}[wording]


def load(fam: str, wording: str = "A") -> list[dict]:
    if wording == "A" and fam in TOOL + COMPUTED:  # these families live only in their own sets
        wording = "T" if fam in TOOL else "C"
    return load_file(data_dir(wording) / f"{fam}.json")


def changed(a: list[int], b: list[int]) -> list[int] | None:
    if len(a) != len(b):
        return None
    return [i for i, (p, q) in enumerate(zip(a, b, strict=True)) if p != q]


def stage_check(which: str) -> None:
    """Alignment of C and O with the clean prompt, uniqueness, answer sanity and balance, per family."""
    tok = tokenizer()
    report: dict[str, Any] = {}
    for label, path in set_files(which).items():
        items = load_file(path)
        stats = collections.Counter()
        answers, bridges, changed_n = collections.Counter(), collections.Counter(), collections.Counter()
        prompts, lengths = set(), []
        for it in items:
            clean = ids(tok, render(tok, it["context"], it["question"]))
            cf = ids(tok, render(tok, it["cf_context"], it["cf_question"]))
            off = ids(tok, render(tok, it["off_context"], it["question"]))
            c, o = changed(clean, cf), changed(clean, off)
            stats["aligned"] += bool(c) and bool(o)
            stats["cf_differs"] += it["answer"] != it["cf_answer"]
            changed_n[(len(c) if c else None, len(o) if o else None)] += 1
            prompts.add(render(tok, it["context"], it["question"]))
            lengths.append(len(clean))
            answers[it["answer"]] += 1
            bridges[it["bridge"]] += 1
        stats["unique_prompts"] = len(prompts)
        report[label] = {"n": len(items), **stats, "changed_tokens(cf,off)": {str(k): v for k, v in changed_n.items()},
                         "prompt_tokens(min,median,max)": (min(lengths), statistics.median(lengths), max(lengths)),
                         "answers": dict(sorted(answers.items())), "bridges": dict(bridges.most_common()),
                         "distinct_bridges": len(bridges)}  # fmt: skip
        print(label, json.dumps(report[label]))
        assert stats["aligned"] == stats["cf_differs"] == stats["unique_prompts"] == len(items), label
    folder = {"dev": DEV, "wording_b": DATA_B, "computed": DATA_C, "tool": DATA_T}.get(which, DATA)
    out = folder / ("check.json" if which in ("main", "wording_b", "computed", "tool") else f"check_{which}.json")
    out.write_text(json.dumps(report, indent=1) + "\n")


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def first_line(text: str) -> str:
    return next((ln for ln in text.lower().split("\n") if ln.strip()), "")


def said(text: str, kind: str) -> str | None:
    line = first_line(text)
    if kind == "digit":
        for t in re.findall(r"[a-z]+|\d+", line):
            if t.isdigit():
                return t
            if t in WORDS:
                return str(WORDS.index(t))
        return None
    vocab = {"animal": ANIMALS, "name": PEOPLE, "fruit": CODE_VALUES}[kind]
    lower = {w.lower(): w for w in vocab}
    return next((lower[t] for t in re.findall(r"[a-z]+", line) if t in lower), None)


def stage_manifest(name: str, why: str, which: str, limit: int | None) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    from bridge_jspace.data import sha256_of

    manifest = {
        "exp": "suite_v1",
        "run": name,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "set": which,
        "items": {label: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for label, f in set_files(which).items()},
        "limit": limit,
        "format": "chat template, thinking off, 'Answer:' prefilled; the context, a newline, the question and "
        f"'{INSTRUCTION}' in one user turn",
        "prompts": "clean, C (cf_context + cf_question), O (off_context + question), hop1-hop3 (each step alone, "
        "with the item's context or the hop's own code)",
        "judge": "the first answer of the item's kind in the first non-empty line of the greedy continuation (digits "
        "and number words for digits; the family's name / animal / fruit vocabulary otherwise)",
        "generation": "greedy, 8 new tokens, prompts of one token length batched 64 at a time",
        "answer_read": "one more forward per prompt, a digit answer's space token appended (the greedy reply's first "
        "token): p of the answer's first token, its logit minus the best other token's, and whether that read's top "
        "token is the greedy judge's answer",
        "eligibility": "clean, C and O all answered (as exp09); all_steps: every prompt of the item answered; reliable "
        "family: Wilson 95% lower bound of clean >= 0.85",
    }  # fmt: skip
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


HOPS = ("hop1", "hop2", "hop3")


def answer_token(tok, answer: str, kind: str) -> int:
    """The answer's first token where the read happens: after 'Answer:' plus the space token for a digit, right after
    'Answer:' (with its leading space) otherwise."""
    return ids(tok, answer)[0] if kind == "digit" else ids(tok, " " + answer)[0]


def read_answers(model, tok, prompts: list[dict]) -> None:
    """One forward per prompt (digit prompts with the space token appended), batched by length: p(answer's first
    token), its logit margin over the best other token, and the top token."""
    import torch

    space = ids(tok, " ")
    assert len(space) == 1
    by_len: dict[int, list[dict]] = {}
    for p in prompts:
        p["forced"] = p["ids"] + (space if p["answer_kind"] == "digit" else [])
        by_len.setdefault(len(p["forced"]), []).append(p)
    with torch.inference_mode():
        for group in by_len.values():
            for start in range(0, len(group), 64):
                chunk = group[start : start + 64]
                x = torch.tensor([p["forced"] for p in chunk], device="cuda")
                logits = model.hf(input_ids=x, logits_to_keep=1).logits[:, -1].float()
                logp = logits.log_softmax(-1)
                for row, p in enumerate(chunk):
                    t = answer_token(tok, p["expected"], p["answer_kind"])
                    other = logits[row].clone()
                    other[t] = -float("inf")
                    p["p_answer"] = round(float(logp[row, t].exp()), 5)
                    p["margin"] = round(float(logits[row, t] - other.max()), 3)
                    p["read_top"] = tok.decode([int(logits[row].argmax())]).strip()


def stage_competence(name: str) -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.stats import wilson
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    for f, pin in manifest["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []
    labels = list(manifest["items"])
    for label in labels:
        items = load_file(pins.REPO_ROOT / manifest["items"][label]["file"])[: manifest.get("limit")]
        for it in items:
            spec = {
                "clean": (it["context"], it["question"], it["answer"], it["answer_kind"]),
                "cf": (it["cf_context"], it["cf_question"], it["cf_answer"], it["answer_kind"]),
                "off": (it["off_context"], it["question"], it["answer"], it["answer_kind"]),
            }
            for h in HOPS:
                if h in it:
                    spec[h] = (it[h].get("context", it["context"]), it[h]["question"], it[h]["answer"], it[h]["kind"])
            for kind, (ctx, q, ans, akind) in spec.items():
                prompts.append({"label": label, "family": it["family"], "id": it["id"], "kind": kind, "expected": ans,
                                "answer_kind": akind, "bridge": it["bridge"], "ids": ids(tok, render(tok, ctx, q))})  # fmt: skip
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = {}
    for p in prompts:
        by_len.setdefault(len(p["ids"]), []).append(p)
    for group in by_len.values():
        for start in range(0, len(group), 64):
            chunk = group[start : start + 64]
            texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
            for p, text in zip(chunk, texts, strict=True):
                p["continuation"] = text
                p["said"] = said(text, p["answer_kind"])
                p["correct"] = p["said"] == p["expected"]
    t_gen = time.time() - t0
    read_answers(model, tok, prompts)
    t_read = time.time() - t0 - t_gen
    print(f"generated in {t_gen:.0f}s, read in {t_read:.0f}s", flush=True)
    rows = [{k: v for k, v in p.items() if k not in ("ids", "forced")} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary: dict[str, Any] = {"families": {}, "seconds_generate": round(t_gen), "seconds_read": round(t_read)}
    for label in labels:
        fr = [r for r in rows if r["label"] == label]
        per_item: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in fr:
            per_item[r["id"]][r["kind"]] = r["correct"]
        kinds = [k for k in ("clean", "cf", "off", *HOPS) if any(k in v for v in per_item.values())]
        cells = {}
        for kind in kinds:
            k = sum(v[kind] for v in per_item.values())
            cells[kind] = dict(zip(("rate", "lo", "hi"), wilson(k, len(per_item)), strict=True)) | {"k": k}
        elig = [i for i, v in per_item.items() if v["clean"] and v["cf"] and v["off"]]
        all_steps = [i for i, v in per_item.items() if all(v.values())]
        hops_ok = [v for v in per_item.values() if all(v[h] for h in HOPS if h in v)]
        clean_rows = [r for r in fr if r["kind"] == "clean"]
        by_bridge = collections.defaultdict(list)
        for r in fr:
            if r["kind"] in HOPS:
                by_bridge[r["bridge"]].append(r["correct"])
        summary["families"][label] = {
            "n": len(per_item),
            "cells": cells,
            "eligible": len(elig),
            "all_steps": len(all_steps),
            "clean_given_all_hops": (sum(v["clean"] for v in hops_ok), len(hops_ok)),
            "reliable": cells["clean"]["lo"] >= 0.85,
            "clean_median_p_answer": statistics.median(r["p_answer"] for r in clean_rows),
            "clean_median_margin": statistics.median(r["margin"] for r in clean_rows),
            # the read sees the answer's first token: a multi-digit answer agrees if the greedy answer starts with it
            "read_agrees_with_greedy": statistics.mean(
                (r["said"] or "").lower().startswith(r["read_top"].lower()) if r["answer_kind"] == "digit" and r["read_top"]
                else r["read_top"].lower() == (r["said"] or "").lower()
                for r in fr
            ),
            "hop_accuracy_by_bridge": {b: round(statistics.mean(v), 3) for b, v in sorted(by_bridge.items())},
        }  # fmt: skip
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "| family | n | clean | C | O | hop1 | hop2 | hop3 | eligible | all steps | median p(answer) | median margin | read = greedy |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]  # fmt: skip
    for label, s in summary["families"].items():
        c = s["cells"]

        def fmt(kind, c=c, n=s["n"]):
            x = c.get(kind)
            return f"{x['k']}/{n} {100 * x['rate']:.0f}% [{100 * x['lo']:.0f},{100 * x['hi']:.0f}]" if x else "-"

        lines.append(f"| {label} | {s['n']} | {fmt('clean')} | {fmt('cf')} | {fmt('off')} | {fmt('hop1')} | "
                     f"{fmt('hop2')} | {fmt('hop3')} | {s['eligible']} | {s['all_steps']} | "
                     f"{s['clean_median_p_answer']:.3f} | {s['clean_median_margin']:.1f} | "
                     f"{100 * s['read_agrees_with_greedy']:.1f}% |")  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument(
        "--set", dest="which", choices=["main", "tiebreak", "dev", "wording_b", "computed", "tool"], default="main"
    )
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items per family (a smoke run)")
    args = ap.parse_args()
    if args.stage == "make":
        stage_make(args.which)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check(args.which)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.which, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
