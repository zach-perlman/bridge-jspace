"""tasks_v2: the breadth task generator (Zach, 2026-10-20; design decided with Zach the same day). This is generator v3
(the evening of 2026-10-20, after an audit and a cold code review; decided with Zach): calib_v2 and cf_smoke_1020 were
made by the earlier generator (commits acbbca7 and 93e11f5) and cannot be regenerated from this one.

Every task is a chain of steps; each step retrieves from the Prompt (P), from Memory (M) or is Computed from the input
(C). A family is its "word": 2-step PP, PM, MP, MM, CP, CM and all eight 3-step words PPP ... MMM. Relations:
  start     P  a person's pick, stated in the prompt          "Clara picked Mars."
            M  a cue, recalled                                 "the red planet" -> Mars
            C  a string computation on the input               typo, reversal, letter count, Caesar shift, acrostic
  thing ->  P  its partner (prompt; things come in pairs, "Mars and Venus are partners.") or its locker (a number)
            M  its number (memory: legs, position from the Sun, atomic number, alphabet position, sides, ...)
  number -> P  the bin for that number (prompt)
            M  the thing with that number in another domain (memory; the answer is then a word: P-M-M, M-M-M)
Shared scenes (as suite_v1's 2x2): the words that start the same way (P-, M- or C-start) are asked on one scene, one
person and one start thing, so P->P and P->M differ only in the question's last step; item["scene"] names the scene.
Number style (copy vs transform): each scene states its lockers and bins as digits ("is 7") or as number words ("is
seven"); digit answers are always asked for as a digit, so with number words a prompt lookup cannot copy its answer.
Domains: controlled tier (single-token names; with --counterfactuals each scene also gets suite_v1-style C and O,
token-aligned: C changes only the first bridge, and so every word's answer, O swaps two other people's picks) animals,
planets, elements, Greek letters; knock-out tier adds shapes, vehicles, instruments (multi-token names allowed).
Formats (only the facts change; the question is the same): prose, json (tool outputs), table (markdown), code (Python
dicts), chat (facts in an earlier user turn), document (facts inside a short record). Every relation's rows are
shuffled separately in json, table and code (no answer by row position).
Knobs (one ladder, LEVELS; each word calibrated to 85-95% on the target model): entities (capped by the domain's size;
item["n_things"] records it), look-alike distractors (the queried person and one other get a look-alike name with
another pick), filler (sentences, records or code lines, by format), paraphrase (every whole-question template has
two wordings) and hard cues (indirect cues for the M start: the memory side's difficulty).
Validity (rejected at generation): a thing's locker never equals its memory number, no bin holds its own number, and
no wrong route (skipping a step, the other relation, the look-alike's pick) gives any word's answer.
Each item also carries every step alone (same context) for per-step knock-outs, and competence --guess adds a
"guess" prompt with the start replaced by an unknown one (an absent person's pick, an unknown thing): items the model
still gets right are guessable from priors (recorded, not dropped).

python scripts/tasks_v2.py examples [--seed S]          one scene per start group, every format of one scene
python scripts/tasks_v2.py make --set NAME --n N ... [--counterfactuals]    data/tasks_v2/NAME/items.jsonl (write-once)
python scripts/tasks_v2.py competence --set NAME --name RUN --why W [--guess]
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import suite_v1 as S

DATA = pins.DATA_DIR / "tasks_v2"
WORDS2 = ("PP", "PM", "MP", "MM", "CP", "CM")
WORDS3 = tuple("".join(w) for w in itertools.product("PM", repeat=3))
FORMATS = ("prose", "json", "table", "code", "chat", "document")
C_OPS = ("typo", "reverse", "letters", "caesar", "acrostic")
NUMBER_WORDS = S.WORDS  # zero ... nine
DIGIT_INSTRUCTION = "Answer with a single digit and nothing else."


@dataclass(frozen=True)
class Domain:
    noun: str  # "planet"
    values: dict  # thing -> its number (memory)
    cues: dict  # thing -> an easy cue phrase that recalls it alone
    hard_cues: dict  # thing -> an indirect cue phrase (the memory-difficulty knob)
    prop_q: tuple[str, str]  # two wordings of the question for the number, "{x}" = description of the thing
    prop_phrase: str  # noun phrase for the number, "{x}" = description of the thing
    reverse_q: str | None  # question for number -> thing, "{n}" = a digit; None: the number does not pick one thing
    reverse_desc: tuple[str, str] | None  # two wordings with "{n}" = a described number (a noun phrase)
    article: bool  # "the cow" vs "Mars"
    tier: str  # "controlled" or "knockout"


def _table(rows: dict) -> tuple[dict, dict, dict]:
    """thing: (number, easy cue or None, hard cue or None) -> values, cues, hard cues."""
    return ({t: v for t, (v, _, _) in rows.items()}, {t: e for t, (_, e, _) in rows.items() if e},
            {t: h for t, (_, _, h) in rows.items() if h})  # fmt: skip


# Cues name one thing of the domain alone and never state or imply its number (no "closest to the Sun", "lightest",
# "first"); facts with more than one common answer are left out (wagon wheels, banjo strings).
ANIMALS = _table({
    "dog": (4, "the animal known for barking", "the animal people call man's best friend"),
    "cat": (4, "the animal known for purring", "the animal ancient Egyptians worshipped as the goddess Bastet"),
    "cow": (4, "the animal known for mooing", "the animal that gives us most of our milk"),
    "horse": (4, "the animal known for neighing", "the animal whose young is called a foal"),
    "mouse": (4, "the animal known for squeaking", "the kind of animal Mickey is"),
    "wolf": (4, "the wild ancestor of the dog", "the animal that raised Romulus and Remus"),
    "pig": (4, "the animal known for oinking", "the animal bacon comes from"),
    "sheep": (4, "the animal known for its wool", "the animal whose young is called a lamb"),
    "lion": (4, "the animal called the king of the jungle", "the big cat that lives in prides"),
    "frog": (4, "the animal known for croaking", "the animal that starts life as a tadpole"),
    "tiger": (4, "the big cat with orange and black stripes", "the national animal of India"),
    "bear": (4, "the kind of animal Winnie-the-Pooh is", "the animal whose polar kind lives in the Arctic"),
    "fox": (4, "the animal known for its bushy red tail", "the animal whose female is called a vixen"),
    "rabbit": (4, "the kind of animal Bugs Bunny is", "the animal that lives in a warren"),
    "goat": (4, "the animal known for climbing cliffs and bleating", "the animal whose young is called a kid"),
    "deer": (4, "the kind of animal Bambi is", "the animal whose male is called a stag"),
    "zebra": (4, "the animal known for its black and white stripes", None),
    "elephant": (4, "the animal known for its trunk", "the animal whose tusks are ivory"),
    "giraffe": (4, "the animal known for its long neck", "the tallest animal on land"),
    "camel": (4, "the animal known for its humps", "the animal called the ship of the desert"),
    "duck": (2, "the animal known for quacking", "the kind of animal Donald is"),
    "goose": (2, "the animal known for honking", "the bird whose male is called a gander"),
    "chicken": (2, "the animal known for clucking", "the bird that lays most of the eggs we eat"),
    "turkey": (2, "the animal known for gobbling", "the bird eaten at Thanksgiving"),
    "owl": (2, "the animal known for hooting", "the bird that can turn its head almost all the way around"),
    "parrot": (2, "the bird known for imitating human speech", "the bird a pirate keeps on his shoulder"),
    "penguin": (2, "the bird that cannot fly and lives in Antarctica", "the bird that huddles through the polar winter"),
    "eagle": (2, "the bird of prey on the Great Seal of the United States", None),
    "swan": (2, None, None),
    "crow": (2, None, None),
    "bee": (6, "the insect known for making honey", "the insect that dances to show where flowers are"),
    "ant": (6, "the insect known for living in colonies and carrying crumbs", "the insect that farms aphids"),
    "butterfly": (6, "the insect that starts life as a caterpillar", "the insect monarch migrations are made of"),
    "fly": (6, "the insect known for buzzing around food", "the insect that maggots grow into"),
    "beetle": (6, None, None),
    "spider": (8, "the animal known for spinning webs", "the kind of animal a tarantula is"),
    "scorpion": (8, "the animal known for the stinger on its tail", "the animal that glows under ultraviolet light"),
    "tick": (8, "the tiny animal that spreads Lyme disease", None),
})  # fmt: skip
PLANETS = _table({
    "Mercury": (1, "the smallest planet", "the planet named after the messenger god"),
    "Venus": (2, "the hottest planet", "the planet named after the goddess of love"),
    "Earth": (3, "the planet we live on", "the only planet known to have life"),
    "Mars": (4, "the red planet", "the planet whose moons are Phobos and Deimos"),
    "Jupiter": (5, "the largest planet", "the planet with the Great Red Spot"),
    "Saturn": (6, "the planet best known for its rings", "the planet whose largest moon is Titan"),
    "Uranus": (7, "the planet that spins on its side", None),
    "Neptune": (8, "the planet named after the god of the sea", "the planet whose largest moon is Triton"),
})  # fmt: skip
ELEMENTS = _table({
    "hydrogen": (1, "the element that makes up most of the Sun", "the element whose isotopes are deuterium and tritium"),
    "helium": (2, "the gas that makes party balloons float", "the gas that makes your voice squeaky"),
    "lithium": (3, "the light metal in rechargeable phone batteries", "the element in mood-stabilising drugs"),
    "beryllium": (4, "the element in emeralds", None),
    "boron": (5, None, None),
    "carbon": (6, "the element diamonds are made of", "the element used to date ancient bones"),
    "nitrogen": (7, "the gas that makes up most of the air", "the element bacteria in bean roots take from the air"),
    "oxygen": (8, "the gas we need to breathe", "the element ozone is made of"),
    "fluorine": (9, "the element added to toothpaste to protect teeth", "the most electronegative element"),
})  # fmt: skip
GREEK = _table({
    "alpha": (1, "the Greek letter for the leader of a wolf pack", "the Greek letter that names the brightest star of a constellation"),
    "beta": (2, "the Greek letter of the radioactive decay that emits electrons", "the Greek letter in the name of heart drugs called blockers"),
    "gamma": (3, "the Greek letter that names the most energetic rays", "the Greek letter of the rays that turned Bruce Banner into the Hulk"),
    "delta": (4, "the Greek letter that names a river mouth", "the Greek letter mathematicians use for a change in a quantity"),
    "epsilon": (5, "the Greek letter mathematicians use for a tiny positive amount", None),
    "zeta": (6, "the Greek letter of the Riemann function", None),
    "eta": (7, None, None),
    "theta": (8, "the Greek letter most used for angles", None),
    "iota": (9, None, None),
})  # fmt: skip
SHAPES = _table({
    "triangle": (3, "the shape of a yield sign", None), "square": (4, "the shape of a chessboard", None),
    "pentagon": (5, "the shape of the US defense headquarters", None),
    "hexagon": (6, "the shape of a honeycomb cell", None), "heptagon": (7, None, None),
    "octagon": (8, "the shape of a stop sign", None), "nonagon": (9, None, None),
})  # fmt: skip
VEHICLES = _table({
    "unicycle": (1, "the vehicle a circus performer balances on", None),
    "bicycle": (2, "the vehicle ridden in the Tour de France", None),
    "motorcycle": (2, "the vehicle Harley-Davidson is famous for", None),
    "tricycle": (3, "the vehicle a toddler pedals", None), "car": (4, "the vehicle most families drive", None),
})  # fmt: skip
INSTRUMENTS = _table({
    "violin": (4, "the instrument a fiddler plays", None), "viola": (4, None, None),
    "cello": (4, "the large instrument played between the knees", None),
    "guitar": (6, "the instrument Jimi Hendrix played", None), "ukulele": (4, "the small instrument from Hawaii", None),
})  # fmt: skip
DOMAINS = {
    "animals": Domain("animal", *ANIMALS, ("How many legs does {x} have?", "What is the number of legs of {x}?"),
                      "the number of legs of {x}", None, None, True, "controlled"),
    "planets": Domain("planet", *PLANETS, ("Counting from the Sun, which position is {x}?",
                                           "What is the position of {x} counting from the Sun?"),
                      "the position of {x} counting from the Sun", "Which planet is at position {n} counting from the Sun?",
                      ("Which planet's position counting from the Sun equals {n}?",
                       "Which planet is at the position from the Sun that equals {n}?"), False, "controlled"),
    "elements": Domain("element", *ELEMENTS, ("What is the atomic number of {x}?", "Which atomic number does {x} have?"),
                       "the atomic number of {x}", "Which element has atomic number {n}?",
                       ("Which element's atomic number equals {n}?", "Which element has an atomic number equal to {n}?"),
                       False, "controlled"),
    "greek": Domain("Greek letter", *GREEK, ("Which position in the Greek alphabet does {x} have?",
                                             "What is the position of {x} in the Greek alphabet?"),
                    "the position of {x} in the Greek alphabet", "Which Greek letter is at position {n} in the Greek alphabet?",
                    ("Which Greek letter's position in the Greek alphabet equals {n}?",
                     "Which Greek letter is at the position in the Greek alphabet that equals {n}?"), False, "controlled"),
    # polygons as a second domain would need "quadrilateral" for 4 sides: no reverse questions for shapes
    "shapes": Domain("shape", *SHAPES, ("How many sides does {x} have?", "What is the number of sides of {x}?"),
                     "the number of sides of {x}", None, None, True, "knockout"),
    "vehicles": Domain("vehicle", *VEHICLES, ("How many wheels does {x} have?", "What is the number of wheels of {x}?"),
                       "the number of wheels of {x}", None, None, True, "knockout"),
    "instruments": Domain("instrument", *INSTRUMENTS, ("How many strings does {x} have?",
                                                       "What is the number of strings of {x}?"),
                          "the number of strings of {x}", None, None, True, "knockout"),
}  # fmt: skip
REVERSE_DOMAINS = [d for d, dom in DOMAINS.items() if dom.reverse_q]
Q_LOCKER = ("Which locker belongs to {d}?", "What is the locker number of {d}?")
Q_BIN = ("Which bin holds things numbered the same as {n}?", "In which bin do things go when they are numbered the same as {n}?")  # fmt: skip

# Filler: no digits, number words, names, things of any domain, or the relation words (pick, partner, locker, bin).
FILLER = (
    *(f for f in S.FILLER if "pick" not in f),
    "The paint on the door was still wet.", "The new curtains arrived on Monday.", "The meeting ran long.",
    "The heater made a strange noise.", "The parking lot was nearly empty.", "The printer ran out of paper.",
    "The lake froze early this year.", "The hall smelled of fresh polish.", "The evening was warm and still.",
    "The lamp in the corner flickered.", "The fence was repaired in spring.", "The soup needed more salt.",
    "The trail was muddy after the storm.", "The clock in the hall ran slow.", "The roof leaked during the storm.",
)  # fmt: skip
CODE_FILLER = (*S.CODE_FILLER, "theme = 'dark'", "lang = 'en'", "cache = None", "notes = []", "author = 'staff'",
                               "editable = True", "draft_mode = False", "region = 'north'", "units = 'metric'",
                               "backup = False")  # fmt: skip
ROOMS = ("kitchen", "hallway", "attic", "cellar", "garage", "porch", "studio", "library", "office", "pantry", "bedroom",
         "bathroom", "lounge", "workshop", "laundry", "sunroom", "balcony", "nursery", "closet", "foyer", "den", "loft")  # fmt: skip
PAINTS = ("blue", "green", "white", "yellow", "grey", "red", "cream", "teal")

# A look-alike for every name in S.PEOPLE: a real name one or two letters away (never itself in S.PEOPLE).
NEAR = {
    "Alice": "Alicia", "Anna": "Hanna", "Beth": "Bess", "Clara": "Clare", "Diana": "Dina", "Emma": "Emmy", "Eva": "Ava",
    "Fiona": "Fenna", "Grace": "Gracie", "Iris": "Irina", "Julia": "Julie", "Kate": "Katie", "Laura": "Lauren",
    "Lily": "Lila", "Lucy": "Lucie", "Maria": "Marie", "Mia": "Mira", "Nina": "Nita", "Olivia": "Olive", "Rose": "Rosa",
    "Sara": "Sarah", "Tara": "Tyra", "Vera": "Verna", "Zoe": "Zoey", "Ella": "Ellie", "Ruby": "Rudy", "Amy": "Amie",
    "Eve": "Evie", "Ivy": "Ivey", "Adam": "Aden", "Ben": "Len", "Carl": "Karl", "Dan": "Don", "David": "Davis",
    "Eric": "Erik", "Finn": "Fynn", "Frank": "Franz", "Henry": "Henri", "Ivan": "Evan", "Jack": "Jake", "James": "Jamie",
    "Leo": "Lea", "Luke": "Luka", "Mark": "Marc", "Max": "Mac", "Noah": "Noam", "Oscar": "Oskar", "Paul": "Saul",
    "Peter": "Pieter", "Sam": "Pam", "Tom": "Tim", "Victor": "Viktor", "Will": "Bill", "Hugo": "Hugh", "Owen": "Oren",
    "Liam": "Lian", "Ryan": "Bryan", "Sean": "Shaun", "Kyle": "Kyla",
}  # fmt: skip
assert set(NEAR) == set(S.PEOPLE), "NEAR must cover PEOPLE"
assert not set(NEAR.values()) & set(S.PEOPLE), "look-alikes must not be real people"
ABSENT = ("Zara", "Quinn", "Yusuf", "Wanda", "Xavier", "Odette")  # never in a scene: the guess prompt's person


def ref(dom: Domain, x: str) -> str:
    return f"the {x}" if dom.article else x


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def num(n: int, style: str) -> str:
    return str(n) if style == "digits" else NUMBER_WORDS[n]


# ---- the computed step --------------------------------------------------------------------------------------------
ACROSTIC = {  # no thing of any domain, and no element or animal lure
    "a": ["Apple", "Arrow", "Anchor"], "b": ["Bread", "Bottle", "Button"], "c": ["Candle", "Cloud", "Cushion"],
    "d": ["Desk", "Drum", "Dune"], "e": ["Engine", "Echo", "Elbow"], "f": ["Feather", "Forest", "Fork"],
    "g": ["Garden", "Glove", "Gravel"], "h": ["Hammer", "Harbor", "Honey"], "i": ["Island", "Ink", "Igloo"],
    "j": ["Jacket", "Jungle", "Jar"], "k": ["Kettle", "Kite", "Knot"], "l": ["Ladder", "Lemon", "Lantern"],
    "m": ["Mango", "Marble", "Mirror"], "n": ["Needle", "Nest", "Noodle"], "o": ["Ocean", "Olive", "Oven"],
    "p": ["Pencil", "Pillow", "Pepper"], "q": ["Quilt", "Quarry", "Queen"], "r": ["River", "Rocket", "Ribbon"],
    "s": ["Salt", "Saddle", "Spoon"], "t": ["Table", "Tunnel", "Towel"], "u": ["Umbrella", "Uniform", "Usher"],
    "v": ["Valley", "Velvet", "Vase"], "w": ["Window", "Wallet", "Whistle"], "x": ["Xylophone"],
    "y": ["Yarn", "Yacht", "Yolk"], "z": ["Zipper", "Zone", "Zigzag"],
}  # fmt: skip


def c_description(op: str, dom: Domain, x: str, rng: random.Random) -> str | None:
    """A description of x that needs a string computation on the input; None if not unique in the domain."""
    if op == "typo":  # two neighbouring letters swapped: never contains x, never another thing's name
        i = rng.randrange(0, len(x) - 1)
        typo = x[:i] + x[i + 1] + x[i] + x[i + 2 :]
        if typo.lower() == x.lower() or any(typo.lower() == t.lower() for t in dom.values):
            return None
        return f"the {dom.noun} misspelled as '{typo}'"
    if op == "reverse":
        return f"the {dom.noun} whose name written backwards is '{x[::-1]}'"
    if op == "letters":
        same = [y for y in dom.values if len(y) == len(x) and y[0].lower() == x[0].lower()]
        return f"the {dom.noun} whose name has {len(x)} letters and starts with '{x[0]}'" if same == [x] else None
    if op == "caesar":
        shift = "".join(chr((ord(ch.lower()) - 97 + 1) % 26 + 97) if ch.isalpha() else ch for ch in x)
        return f"the {dom.noun} written as '{shift}', where each letter stands for the letter before it in the alphabet"
    if op == "acrostic":
        words = [rng.choice(ACROSTIC[ch.lower()]) for ch in x]
        return f"the {dom.noun} spelled by the first letters of {', '.join(words)}"
    raise ValueError(op)


# ---- scenes -------------------------------------------------------------------------------------------------------
def start_ok(group: str, dom: Domain, knobs: dict):
    """Which things can start a scene of this group: M needs a cue (a hard one when the knob is on)."""
    if group == "M":
        cues = dom.hard_cues if knobs["hard_cues"] else dom.cues
        return lambda t: t in cues
    return lambda t: True


def scene(rng: random.Random, dom: Domain, group: str, knobs: dict, style: str) -> dict | None:
    """People, their picks (the start thing x is the queried person's), pairs of partners, lockers (never a thing's
    memory number), bins (no bin holds its own number) and look-alikes. x is drawn so that its number is uniform over
    the numbers the domain's eligible things have (bee and spider as often as the 4-legged animals' total)."""
    ok = start_ok(group, dom, knobs)
    cands = [t for t in dom.values if ok(t)]
    if not cands:  # e.g. hard cues asked of a domain that has none
        return None
    per_value = collections.Counter(dom.values[t] for t in cands)
    x = rng.choices(cands, weights=[1 / per_value[dom.values[t]] for t in cands])[0]
    n_ent = min(knobs["entities"], len(dom.values))
    things = [x, *rng.sample([t for t in dom.values if t != x], n_ent - 1)]
    rng.shuffle(things)
    people = rng.sample(S.PEOPLE, len(things))
    pick = dict(zip(people, things, strict=True))
    person = people[things.index(x)]
    single = rng.choice([t for t in things if t != x]) if len(things) % 2 else None
    pairable = [t for t in things if t != single]
    rng.shuffle(pairable)
    pairs = list(zip(pairable[0::2], pairable[1::2], strict=True))
    partner = {a: b for a, b in pairs} | {b: a for a, b in pairs}
    while True:  # lockers: distinct while there are digits enough, never the thing's own number
        lockers = rng.sample(range(1, 10), len(things)) if len(things) <= 9 else [rng.randrange(1, 10) for _ in things]
        if all(lk != dom.values[t] for lk, t in zip(lockers, things, strict=True)):
            break
    while True:  # bins: a derangement of 1-9
        b = rng.sample(range(1, 10), 9)
        if all(b[i] != i + 1 for i in range(9)):
            break
    lookalike_picks = []
    if knobs["distractors"]:  # the queried person always, and one other person, get a look-alike with another pick
        for p in [person, *rng.sample([q for q in people if q != person], min(1, len(people) - 1))]:
            lookalike_picks.append((NEAR[p], rng.choice([t for t in things if t != pick[p]])))
    return {"things": things, "people": people, "pick": pick, "person": person, "x": x, "pairs": pairs,
            "partner": partner, "locker": dict(zip(things, lockers, strict=True)),
            "bin": dict(zip(range(1, 10), b, strict=True)), "lookalike_picks": lookalike_picks, "numbers": style}  # fmt: skip


def start_desc(group: str, dom: Domain, sc: dict, x: str, knobs: dict, c_op: str | None, rng) -> str | None:
    if group == "P":
        return f"{sc['person']}'s pick"
    if group == "M":
        return (dom.hard_cues if knobs["hard_cues"] else dom.cues).get(x)
    return c_description(c_op, dom, x, rng)


def step(question: str, answer: str, kind: str, source: str) -> dict:
    return {"question": question, "answer": answer, "kind": kind, "source": source}


def chain(word: str, dom: Domain, sc: dict, x: str, desc: str, dom2: Domain | None, para: int) -> dict | None:
    """The whole question (wording `para`), its answer and its steps after the first, from start thing x described
    as desc; None if the scene cannot carry the word."""
    steps, rest = [], word[1:]
    if len(rest) == 2 and rest[0] == "P":
        if x not in sc["partner"]:
            return None
        y = sc["partner"][x]
        steps.append(step(f"Which {dom.noun} is the partner of {ref(dom, x)}?", y, "word", "P"))
        x, desc, rest = y, f"the partner of {desc}", rest[1:]
    elif len(rest) == 2:
        n = dom.values[x]
        steps.append(step(dom.prop_q[0].format(x=ref(dom, x)), str(n), "digit", "M"))
        ndesc = dom.prop_phrase.format(x=desc)
        if rest[1] == "P":
            b = sc["bin"][n]
            steps.append(step(f"Which bin holds things numbered {n}?", str(b), "digit", "P"))
            return {"question": Q_BIN[para].format(n=ndesc), "answer": str(b), "kind": "digit", "steps": steps}
        z = next((t for t, v in dom2.values.items() if v == n), None) if dom2 else None
        if z is None:
            return None
        steps.append(step(dom2.reverse_q.format(n=n), z, "word", "M"))
        return {"question": dom2.reverse_desc[para].format(n=ndesc), "answer": z, "kind": "word", "steps": steps}
    if rest == "P":
        a = str(sc["locker"][x])
        steps.append(step(f"Which locker belongs to {ref(dom, x)}?", a, "digit", "P"))
        return {"question": Q_LOCKER[para].format(d=desc), "answer": a, "kind": "digit", "steps": steps}
    a = str(dom.values[x])
    steps.append(step(dom.prop_q[0].format(x=ref(dom, x)), a, "digit", "M"))
    return {"question": dom.prop_q[para].format(x=desc), "answer": a, "kind": "digit", "steps": steps}


def follow(word: str, dom: Domain, sc: dict, x: str, dom2: Domain | None) -> tuple[str | None, list[str]]:
    """The answer of the word's chain from start thing x in scene sc, and its bridges (the thing, then a 3-step
    word's middle value); None if the chain has no answer from x."""
    bridges, rest = [x], word[1:]
    if len(rest) == 2 and rest[0] == "P":
        if x not in sc["partner"]:
            return None, bridges
        x = sc["partner"][x]
        bridges.append(x)
        rest = rest[1:]
    elif len(rest) == 2:
        n = dom.values[x]
        bridges.append(str(n))
        if rest[1] == "P":
            return str(sc["bin"][n]), bridges
        return next((t for t, v in dom2.values.items() if v == n), None), bridges
    return str(sc["locker"][x] if rest == "P" else dom.values[x]), bridges


def wrong_routes(word: str, dom: Domain, sc: dict, x: str, dom2: Domain | None) -> list[str]:
    """Answers reachable by a wrong route: a skipped step, the other relation (locker for number or back), the
    queried person's look-alike's pick. The right answer must be none of them."""
    alts, rest, start = [], word[1:], x
    if len(rest) == 2 and rest[0] == "P":
        alts.append(str(sc["locker"][x] if rest[1] == "P" else dom.values[x]))  # the partner step skipped
        x, rest = sc["partner"][x], rest[1:]
    elif len(rest) == 2:
        n, lk = dom.values[x], sc["locker"][x]
        if rest[1] == "P":
            alts += [str(n), str(lk), str(sc["bin"][lk])]  # bin skipped; locker read as the number
        else:
            alts.append(next((t for t, v in dom2.values.items() if v == lk), None))  # locker read as the number
        x = None
    if x is not None:
        alts.append(str(dom.values[x] if rest == "P" else sc["locker"][x]))  # the other relation
    if word[0] == "P":
        for name, t in sc["lookalike_picks"]:
            if name == NEAR[sc["person"]] and t != start:
                alts.append(follow(word, dom, sc, t, dom2)[0])
    return [a for a in alts if a is not None]


# ---- formats ------------------------------------------------------------------------------------------------------
def render_facts(fmt: str, dom: Domain, sc: dict, rng: random.Random, n_filler: int) -> str:
    """The scene's facts (all relations, whichever the words use) in one format. The draws depend only on the scene's
    sizes, so the same rng state renders C and O with the clean prompt's layout."""
    st = sc["numbers"]
    picks = list(sc["pick"].items()) + sc["lookalike_picks"]
    lockers, bins, pairs = list(sc["locker"].items()), list(sc["bin"].items()), list(sc["pairs"])
    both = [(a, b) for a, b in pairs] + [(b, a) for a, b in pairs]
    if fmt in ("prose", "chat", "document"):
        lines = [f"{p} picked {ref(dom, t)}." for p, t in picks]
        lines += [f"{cap(ref(dom, a))} and {ref(dom, b)} are partners." for a, b in pairs]
        lines += [f"The locker of {ref(dom, t)} is {num(n, st)}." for t, n in lockers]
        lines += [f"Things numbered {num(n, st)} go in bin {num(b, st)}." for n, b in bins]
        fill = rng.sample(FILLER, n_filler)
        intro = fill[: min(3, n_filler)] if fmt == "document" else []
        lines += fill[len(intro) :]
        rng.shuffle(lines)
        text = " ".join(lines)
        if fmt == "document":
            return " ".join(["Club newsletter, autumn term.", *intro, "From the club's records:", text,
                             "That is all for this term."])  # fmt: skip
        return text
    val = (lambda n: n) if st == "digits" else (lambda n: NUMBER_WORDS[n])
    rel = {"picks": ("name", "pick", picks), "partners": ("item", "partner", both),
           "lockers": ("item", "locker", [(t, val(n)) for t, n in lockers]),
           "bins": ("number", "bin", [(val(n), val(b)) for n, b in bins])}  # fmt: skip
    for _, _, rows in rel.values():
        rng.shuffle(rows)
    rooms = [(r, rng.choice(PAINTS)) for r in rng.sample(ROOMS, n_filler)] if fmt in ("json", "table") else []
    if rooms:
        rel["rooms"] = ("room", "paint", rooms)
    order = list(rel)
    rng.shuffle(order)
    if fmt == "json":
        return "\n".join(f"Tool output from get_{k}:\n" + json.dumps([{rel[k][0]: a, rel[k][1]: b} for a, b in rel[k][2]])
                         for k in order)  # fmt: skip
    if fmt == "table":
        return "\n\n".join(f"Table {k}:\n| {rel[k][0]} | {rel[k][1]} |\n|---|---|\n"
                           + "\n".join(f"| {a} | {b} |" for a, b in rel[k][2]) for k in order)  # fmt: skip
    if fmt == "code":
        lines = [f"{k} = {dict(rel[k][2])!r}" for k in order]
        lines += rng.sample(CODE_FILLER, n_filler)
        rng.shuffle(lines)
        return "```python\n" + "\n".join(lines) + "\n```"
    raise ValueError(fmt)


def render(tok, item: dict) -> str:
    """The full prompt text for the item's question (or a step's, via item['_question'] and item['_kind']): one user
    turn, or for the chat format the facts in an earlier user turn; thinking off; 'Answer:' prefilled (as suite_v1).
    Digit answers are asked for as a digit, word answers as one word."""
    from bridge_jspace import chat

    q = item.get("_question", item["question"])
    kind = item.get("_kind", item["kind"])
    instr = DIGIT_INSTRUCTION if kind == "digit" else S.INSTRUCTION
    if item["format"] != "chat":
        return chat.chat_text(tok, f"{item['context']}\n{q} {instr}")
    msgs = [{"role": "user", "content": f"Here are my notes:\n{item['context']}"},
            {"role": "assistant", "content": "Got it."},
            {"role": "user", "content": f"{q} {instr}"}]  # fmt: skip
    return (
        tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False) + chat.PREFILL
    )


# ---- making scenes ------------------------------------------------------------------------------------------------
def make_scene(rng: random.Random, group: str, words: list[str], domain: str, fmt: str, knobs: dict, domains: list[str],
               tok=None) -> list[dict] | None:  # fmt: skip
    """One scene asked with every word of the group (all must be carried, none with a wrong route to its answer);
    with a tokenizer (controlled tier) also the scene's C and O. None if this draw cannot."""
    dom = DOMAINS[domain]
    style = "words" if rng.random() < 0.5 else "digits"
    sc = scene(rng, dom, group, knobs, style)
    if sc is None:
        return None
    x = sc["x"]
    c_op = rng.choice(C_OPS) if group == "C" else None
    desc = start_desc(group, dom, sc, x, knobs, c_op, rng)
    if desc is None:
        return None
    pool = [d for d in REVERSE_DOMAINS if d != domain and d in domains]
    dom2_name = rng.choice(pool) if pool and any(w[1:] == "MM" for w in words) else None
    dom2 = DOMAINS[dom2_name] if dom2_name else None
    first = {"P": step(f"What did {sc['person']} pick?", x, "word", "P"), "M": step(f"What is {desc}?", x, "word", "M"),
             "C": step(f"What is {desc}?", x, "word", "C")}[group]  # fmt: skip
    render_state = rng.getstate()
    context = render_facts(fmt, dom, sc, rng, knobs["filler"])
    items = []
    for word in words:
        para = int(rng.random() < 0.5) if knobs["paraphrase"] else 0
        d2 = dom2 if word[1:] == "MM" else None
        ch = chain(word, dom, sc, x, desc, d2, para)
        if ch is None or ch["answer"] in wrong_routes(word, dom, sc, x, d2):
            return None
        items.append({"word": word, "domain": domain, "format": fmt, "knobs": knobs, "c_op": c_op,
                      "domain2": dom2_name if d2 else None, "numbers": style, "n_things": len(sc["things"]),
                      "context": context, "question": ch["question"], "answer": ch["answer"], "kind": ch["kind"],
                      "steps": [first, *ch["steps"]], "tier": dom.tier, "start_desc": desc})  # fmt: skip
    if tok is None:
        return items
    assert dom.tier == "controlled", domain
    cf = counterfactuals(tok, items, group, dom, sc, desc, dom2, render_state, knobs["filler"])
    return None if cf is None else [{**it, **c} for it, c in zip(items, cf, strict=True)]


# ---- counterfactuals (controlled tier) ----------------------------------------------------------------------------
MAX_SWAP_CHANGED = 4  # a swap of two single-token names changes 2 tokens; 4 allows a name split in two in some format


def _single(tok, word: str) -> bool:
    return len(S.ids(tok, " " + word)) == 1


def _swap_picks(sc: dict, a: str, b: str) -> dict:
    pick = dict(sc["pick"])
    pick[a], pick[b] = pick[b], pick[a]
    return {**sc, "pick": pick}


def counterfactuals(tok, items: list[dict], group: str, dom: Domain, sc: dict, desc: str, dom2: Domain | None,
                    render_state, n_filler: int) -> list[dict] | None:  # fmt: skip
    """One C and one O for the whole scene, token-aligned with every word's prompt (suite_v1's convention), or None.
    C changes only the first bridge (x to X), and every word's answer: P swaps the queried person's pick with another
    person's; M puts X's cue in each question in place of x's; C computes the description from X instead. O swaps the
    picks of two other people (off every word's path). Bridges are single-token names; C and O render with the clean
    prompt's layout (the same draws for order and filler)."""
    rng = random.Random(f"cf|{items[0]['context']}|{desc}")
    x, person = sc["x"], sc["person"]
    if not _single(tok, x):
        return None
    d2 = {it["word"]: (dom2 if it["word"][1:] == "MM" else None) for it in items}

    def context_of(scene_: dict) -> str:
        gen = random.Random()
        gen.setstate(render_state)
        return render_facts(items[0]["format"], dom, scene_, gen, n_filler)

    clean_ids = [S.ids(tok, render(tok, it)) for it in items]

    def aligned(i: int, context: str, question: str, limit: int) -> list[int] | None:
        got = S.changed(clean_ids[i], S.ids(tok, render(tok, {**items[i], "context": context, "question": question})))
        return got if got and len(got) <= limit else None

    others = [p for p in sc["people"] if p != person]
    cues = dom.hard_cues if items[0]["knobs"]["hard_cues"] else dom.cues
    for X in rng.sample([t for t in sc["things"] if t != x], len(sc["things"]) - 1):
        if not _single(tok, X):
            continue
        if group == "P":
            q = next(p for p in others if sc["pick"][p] == X)
            cf_sc, limit = _swap_picks(sc, person, q), MAX_SWAP_CHANGED
            cf_context, new_desc = context_of(cf_sc), desc
        else:
            new_desc = cues.get(X) if group == "M" else c_description(items[0]["c_op"], dom, X, rng)
            if new_desc is None:
                continue
            cf_sc, cf_context, limit = sc, items[0]["context"], 10**6
        out = []
        for i, it in enumerate(items):
            assert it["question"].count(desc) == 1, it["question"]
            cf_q = it["question"].replace(desc, new_desc)
            cf_answer, cf_bridges = follow(it["word"], dom, cf_sc, X, d2[it["word"]])
            changed = aligned(i, cf_context, cf_q, limit) if cf_answer not in (None, it["answer"]) else None
            if not changed:
                break
            out.append({"cf_context": cf_context, "cf_question": cf_q, "cf_answer": cf_answer, "cf_bridge": X,
                        "cf_bridges": cf_bridges, "cf_changed_tokens": len(changed)})  # fmt: skip
        if len(out) == len(items):
            break
    else:
        return None
    for a, b in rng.sample(list(itertools.combinations(others, 2)), len(others) * (len(others) - 1) // 2):
        off_context = context_of(_swap_picks(sc, a, b))
        offs = [aligned(i, off_context, it["question"], MAX_SWAP_CHANGED) for i, it in enumerate(items)]
        if all(offs):
            return [{**c, "off_context": off_context, "off_changed_tokens": len(o), "bridge": x,
                     "bridges": follow(it["word"], dom, sc, x, d2[it["word"]])[1], "answer_kind": it["kind"],
                     "scene_facts": {k: sc[k] for k in ("pick", "pairs", "locker")}}
                    for c, o, it in zip(out, offs, items, strict=True)]  # fmt: skip
    return None


def prepare(item: dict, tok) -> dict:
    """suite_split.prepare for a tasks_v2 item with C and O: token ids of clean, C and O (a digit answer's space
    appended for the read), the changed positions, the position groups and the two answers' first tokens."""
    from bridge_jspace.tokens import raw_encoding

    variants = {"clean": item, "cf": {**item, "context": item["cf_context"], "question": item["cf_question"]},
                "off": {**item, "context": item["off_context"]}}  # fmt: skip
    rendered = {k: render(tok, v) for k, v in variants.items()}
    enc = {k: raw_encoding(tok, t, offsets=True) for k, t in rendered.items()}
    ids = {k: list(e["input_ids"]) for k, e in enc.items()}
    cf_changed, off_changed = S.changed(ids["clean"], ids["cf"]), S.changed(ids["clean"], ids["off"])
    assert cf_changed, f"{item['id']}: C not token-aligned"
    assert off_changed, f"{item['id']}: O not token-aligned"
    q_start = rendered["clean"].rindex("\n" + item["question"]) + 1
    after = max(cf_changed)
    offsets = enc["clean"]["offset_mapping"]
    space = S.ids(tok, " ") if item["answer_kind"] == "digit" else []
    tok_a, tok_b = (S.answer_token(tok, a, item["answer_kind"]) for a in (item["answer"], item["cf_answer"]))
    assert tok_a != tok_b, f"{item['id']}: the clean and C answers share their first token"
    return {
        "ids": ids,
        "read_ids": {k: v + space for k, v in ids.items()},
        "changed": {"cf": cf_changed, "off": off_changed},
        "groups": {
            "question": [i for i, (_, e) in enumerate(offsets) if e > q_start and i > after],
            "last": [len(ids["clean"]) - 1],
        },
        "tok_A": tok_a,
        "tok_b": tok_b,
        "family": item["word"],
        "name": item["id"],
    }


# ---- datasets, competence, calibration ---------------------------------------------------------------------------
LEVELS = {  # one difficulty ladder, all knobs up together (Zach, 2026-10-20: calibrate per word on this ladder)
    0: {"entities": 3, "distractors": False, "filler": 0, "paraphrase": False, "hard_cues": False},
    1: {"entities": 6, "distractors": True, "filler": 5, "paraphrase": False, "hard_cues": False},
    2: {"entities": 9, "distractors": True, "filler": 10, "paraphrase": True, "hard_cues": True},
    3: {"entities": 12, "distractors": True, "filler": 20, "paraphrase": True, "hard_cues": True},
}
BAND = (0.85, 0.95)


def groups_of(words: list[str]) -> dict[str, list[str]]:
    return {g: [w for w in words if w[0] == g] for g in "PMC" if any(w[0] == g for w in words)}


def make(name: str, n: int, words: list[str], domains: list[str], formats: list[str], levels: list[int], seed: int,
         counterfactuals: bool = False) -> None:  # fmt: skip
    """n scenes per start group x level, each asked with every word of its group, spread evenly over the domain x
    format combinations that can carry the group, each word's digit answers capped at twice their uniform share.
    Write-once; a shortfall (fewer than n scenes) stops it."""
    out = DATA / name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "items.jsonl").exists(), f"{out} exists; data sets are written once"
    rng = random.Random(seed)
    tok = None
    if counterfactuals:
        from bridge_jspace.tokens import load_tokenizer

        assert all(DOMAINS[d].tier == "controlled" for d in domains), "counterfactuals need controlled-tier domains"
        tok = load_tokenizer()
    items, seen, coverage = [], set(), {}
    cap_n = math.ceil(2 * n / 9)
    for level in levels:
        for group, gwords in groups_of(words).items():
            combos = [(d, f) for d in domains for f in formats]
            rng.shuffle(combos)
            answers = {w: collections.Counter() for w in gwords}
            got, dead, used = 0, set(), collections.Counter()
            while got < n and len(dead) < len(combos):
                for d, f in combos:
                    if got >= n or (d, f) in dead:
                        continue
                    for _ in range(60):  # a combination that yields nothing in 60 draws cannot carry this group
                        its = make_scene(rng, group, gwords, d, f, LEVELS[level], domains, tok)
                        if its is None or (its[0]["context"], tuple(it["question"] for it in its)) in seen:
                            continue
                        if any(it["kind"] == "digit" and answers[it["word"]][it["answer"]] >= cap_n for it in its):
                            continue
                        break
                    else:
                        dead.add((d, f))
                        continue
                    seen.add((its[0]["context"], tuple(it["question"] for it in its)))
                    for it in its:
                        answers[it["word"]][it["answer"]] += 1
                        it.update({"id": f"{it['word']}-L{level}-{got:04d}", "scene": f"{group}-L{level}-{got:04d}",
                                   "level": level})  # fmt: skip
                    items += its
                    used[f"{d}/{f}"] += 1
                    got += 1
            coverage[f"{group}/L{level}"] = {"scenes": got, "dead_combinations": sorted(f"{d}/{f}" for d, f in dead),
                                             "by_domain_format": dict(used)}  # fmt: skip
            assert got == n, f"{group} at L{level}: {got} of {n} scenes (dead: {sorted(dead)})"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    meta = {"set": name, "n_scenes_per_group_level": n, "words": words, "domains": domains, "formats": formats,
            "levels": {k: LEVELS[k] for k in levels}, "seed": seed, "generator": "scripts/tasks_v2.py make (v3)",
            "git_commit": commit, "counterfactuals": counterfactuals, "n_items": len(items), "coverage": coverage}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", out / "items.jsonl", len(items), "items")


def examples(seed: int) -> None:
    rng = random.Random(seed)
    for group, words in groups_of(list(WORDS2 + WORDS3)).items():
        for _ in range(200):
            its = make_scene(rng, group, words, rng.choice(["animals", "planets", "elements", "greek"]), "prose",
                             LEVELS[1], list(DOMAINS))  # fmt: skip
            if its:
                break
        print(f"\n=== {group}-start scene ({its[0]['domain']}, numbers as {its[0]['numbers']}"
              f"{', ' + its[0]['c_op'] if its[0]['c_op'] else ''})\n{its[0]['context']}")  # fmt: skip
        for it in its:
            print(f"  {it['word']:4s} Q: {it['question']} -> {it['answer']}")
            print("        steps:", " | ".join(f"{s['source']}: {s['question']} -> {s['answer']}" for s in it["steps"]))
    for fmt in FORMATS:
        for _ in range(200):
            its = make_scene(random.Random(seed), "P", ["PM"], "planets", fmt, LEVELS[1], list(DOMAINS))
            if its:
                break
        print(f"\n=== format {fmt} (PM, planets, level 1)\n{its[0]['context'][:900]}\nQ: {its[0]['question']}")


def load(name: str) -> list[dict]:
    return [json.loads(line) for line in (DATA / name / "items.jsonl").read_text().splitlines()]


ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
            "ninth": 9}  # fmt: skip
ALL_THINGS = {t.lower() for dom in DOMAINS.values() for t in dom.values}


def judge(text: str, answer: str, kind: str) -> bool:
    """Digit: the first number in the first line (digits, number words or ordinals). Word: the first thing of any
    domain named in the first line is the answer (so a list of candidates or a different first guess is wrong)."""
    line = S.first_line(text)
    if kind == "digit":
        for t in re.findall(r"[a-z]+|\d+", line):
            if t.isdigit():
                return t == answer
            if t in NUMBER_WORDS:
                return str(NUMBER_WORDS.index(t)) == answer
            if t in ORDINALS:
                return str(ORDINALS[t]) == answer
        return False
    named = [m for m in re.findall(r"[a-z]+", line) if m in ALL_THINGS]
    return bool(named) and named[0] == answer.lower()


def eligible(set_name: str, comp_run: str, words: list[str] | None, n: int, level: str = "pick") -> list[dict]:
    """The items downstream runs use: from scenes whose every item the competence run got right on every prompt
    (whole, each step, C and O; the guess prompt excluded), at the calibrated level (level "pick": the competence
    summary's pick per word; "all"; or a level number), the first n per word in file order. Each item gets
    "guessable": whether the model answered its guess prompt right (None if the run had none)."""
    run_dir = pins.RESULTS_DIR / "tasks_v2" / comp_run
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    guessed: dict[str, bool] = {}
    for line in (run_dir / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["part"] == "guess":
            guessed[r["id"]] = r["correct"]
        else:
            ok[r["id"]].append(r["correct"])
    items = load(set_name)
    scene_ok: dict[str, bool] = collections.defaultdict(lambda: True)
    for it in items:
        scene_ok[it["scene"]] &= bool(ok.get(it["id"])) and all(ok[it["id"]])
    pick = json.loads((run_dir / "summary.json").read_text())["pick"] if level == "pick" else {}
    out, got = [], collections.Counter()
    for it in items:
        w = it["word"]
        want = pick.get(w) if level == "pick" else (None if level == "all" else int(level))
        if (words and w not in words) or got[w] >= n or not scene_ok[it["scene"]]:
            continue
        if level != "all" and it["level"] != want:
            continue
        got[w] += 1
        out.append({**it, "guessable": guessed.get(it["id"])})
    return out


def guess_question(it: dict) -> str:
    """The whole question with its start replaced by an unknown one: an absent person's pick (P), an unknown thing of
    the domain (M, C). Right answers to it come from priors, not from the bridge."""
    dom = DOMAINS[it["domain"]]
    absent = ABSENT[sum(map(ord, it["scene"])) % len(ABSENT)]
    unknown = f"{absent}'s pick" if it["word"][0] == "P" else f"an unknown {dom.noun}"
    return it["question"].replace(it["start_desc"], unknown)


def prompts_for(tok, it: dict, guess: bool = False) -> list[dict]:
    """The whole question, every step alone, C and O (if the item has them) and with guess the guess prompt, as token
    ids with their answers."""
    out = [{"part": "whole", "question": it["question"], "answer": it["answer"], "kind": it["kind"]}]
    out += [{"part": f"step{i}", **{k: s[k] for k in ("question", "answer", "kind")}, "source": s["source"]}
            for i, s in enumerate(it["steps"], 1)]  # fmt: skip
    if "cf_context" in it:
        out += [{"part": "cf", "question": it["cf_question"], "answer": it["cf_answer"], "kind": it["kind"],
                 "_context": it["cf_context"]},
                {"part": "off", "question": it["question"], "answer": it["answer"], "kind": it["kind"],
                 "_context": it["off_context"]}]  # fmt: skip
    if guess:
        out.append({"part": "guess", "question": guess_question(it), "answer": it["answer"], "kind": it["kind"]})
    for p in out:
        variant = {**it, "context": p.pop("_context", it["context"]), "_question": p["question"], "_kind": p["kind"]}
        p["ids"] = S.ids(tok, render(tok, variant))
    return out


def competence(set_name: str, run: str, why: str, guess: bool) -> None:
    import statistics
    import time

    import torch

    from bridge_jspace.model import load_model

    pins.check_run_name(run)
    out = pins.RESULTS_DIR / "tasks_v2" / run
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"run": run, "why": why, "set": set_name, "model": pins.model_pin(),
                                                   "git_commit": commit, "guess": guess,
                                                   "generation": "greedy, 8 new tokens, batched by length",
                                                   "read": "suite_v1.read_answers: p and logit margin of the answer's first token",
                                                   "judge": "tasks_v2.judge: the first number / the first thing named in the first line",
                                                   "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    jobs = []
    for it in load(set_name):
        for p in prompts_for(tok, it, guess):
            jobs.append({**p, "id": it["id"], "scene": it["scene"], "word": it["word"], "domain": it["domain"],
                         "format": it["format"], "level": it["level"], "numbers": it["numbers"], "c_op": it["c_op"],
                         "answer_kind": p["kind"], "expected": p["answer"]})  # fmt: skip
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    t0 = time.time()
    for group in by_len.values():
        for start in range(0, len(group), 64):
            chunk = group[start : start + 64]
            texts = model.generate_batch(torch.tensor([j["ids"] for j in chunk], device="cuda"), 8, [{}] * len(chunk))
            for j, text in zip(chunk, texts, strict=True):
                j["text"], j["correct"] = text, judge(text, j["answer"], j["kind"])
    S.read_answers(model, tok, jobs)
    rows = [{k: v for k, v in j.items() if k not in ("ids", "forced")} for j in jobs]
    (out / "items.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    acc = lambda sel: round(statistics.mean(r["correct"] for r in sel), 3) if sel else None  # noqa: E731
    summary: dict = {"seconds": round(time.time() - t0), "by_word_level": {}, "by_domain": {}, "by_format": {},
                     "by_numbers": {}, "pick": {}}  # fmt: skip
    whole = [r for r in rows if r["part"] == "whole"]
    for word in dict.fromkeys(r["word"] for r in whole):
        for level in sorted({r["level"] for r in whole}):
            sel = [r for r in whole if r["word"] == word and r["level"] == level]
            mine = [r for r in rows if r["word"] == word and r["level"] == level]
            steps_ok = collections.defaultdict(list)
            for r in mine:
                if r["part"].startswith("step"):
                    steps_ok[r["id"]].append(r["correct"])
            cell = {"n": len(sel), "whole": acc(sel), "all_steps": acc([{"correct": all(v)} for v in steps_ok.values()]),
                    "median_margin": round(statistics.median(r["margin"] for r in sel), 2),
                    "whole_by_numbers": {s: acc([r for r in sel if r["numbers"] == s]) for s in ("digits", "words")}}  # fmt: skip
            for part in ("cf", "off", "guess"):
                got = [r for r in mine if r["part"] == part]
                if got:
                    cell[part] = acc(got)
            summary["by_word_level"][f"{word}/L{level}"] = cell
        in_band = [lv for lv in sorted({r["level"] for r in whole})
                   if BAND[0] <= summary["by_word_level"][f"{word}/L{lv}"]["whole"] <= BAND[1]]  # fmt: skip
        summary["pick"][word] = in_band[-1] if in_band else None  # the hardest level inside 85-95%
    for key in ("domain", "format", "numbers"):
        for v in dict.fromkeys(r[key] for r in whole):
            summary[f"by_{key}"][v] = acc([r for r in whole if r[key] == v])
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=1)[:5000])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["examples", "make", "competence"])
    ap.add_argument("--seed", type=int, default=701)
    ap.add_argument("--set", dest="set_name")
    ap.add_argument("--n", type=int, default=48, help="make: scenes per start group x level")
    ap.add_argument("--words", nargs="+", default=list(WORDS2 + WORDS3))
    ap.add_argument("--domains", nargs="+", default=list(DOMAINS))
    ap.add_argument("--formats", nargs="+", default=list(FORMATS))
    ap.add_argument("--levels", nargs="+", type=int, default=list(LEVELS))
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--counterfactuals", action="store_true", help="make: token-aligned C and O (controlled tier)")
    ap.add_argument("--guess", action="store_true", help="competence: add the guess prompt (start made unknown)")
    args = ap.parse_args()
    if args.stage == "examples":
        examples(args.seed)
    elif args.stage == "make":
        make(
            args.set_name, args.n, args.words, args.domains, args.formats, args.levels, args.seed, args.counterfactuals
        )
    else:
        competence(args.set_name, args.name, args.why, args.guess)
