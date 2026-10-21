"""tasks_v2: the breadth task generator (Zach, 2026-10-20; design decided with Zach the same day). Generator v7:
v3 (2026-10-20 evening, after an audit and a cold review), v6 (2026-10-21, after the three-step questions failed
calibration; tasks3_ab_v1, tasks3_ab2_v1) and v7 (the same night, after a review of v6), each decided with Zach.
calib_v2-v6 and the earlier smoke and ctrl sets were made by earlier versions (their manifests' git_commit) and
cannot be regenerated from this one.

Every task is a chain of steps; each step retrieves from the Prompt (P), from Memory (M) or is Computed from the input
(C). A family is its "word": 2-step PP, PM, MP, MM, CP, CM and the 3-step PPP, PPM, PMP, MPP, MPM, MMP (the reverse
lookups PMM and MMM were dropped in v6: nested by nature). Relations:
  start     P  a person's pick, stated in the prompt          "Clara picked Mars."
            M  a cue, recalled                                 "the red planet" -> Mars
            C  a string computation on the input               typo, reversal, letter count (v6: no Caesar shift,
                                                               which the model cannot do, nor acrostic)
  thing ->  P  its partner (one-way statements, both directions: "Mars's partner is Venus.") or its locker (a number)
            M  its number (memory: legs, position from the Sun, atomic number, alphabet position, sides, ...)
  number -> P  the bin, by a rule keyed by the property, one per number the domain has ("Animals with 4 legs go in
               bin 5."; v6: "Things numbered 4 go in bin 5" left P->M->P at 15%); asked "Which bin does Sam's pick go in?"
Contexts (v6/v7, CONTEXT_RELS): picks always, and only the relations the word's question reads: lockers for the 2-step
words (P->P and P->M read one identical context), partners + lockers for PPP/PPM and MPP/MPM (each last-step pair one
context), bins for PMP/MMP. Shared scenes: the words of a scene group (start letter x length: P2, M2, C2, P3, M3) are
asked on one scene, person and start thing; item["scene"] names it. Three-step words use THREE_STEP_DOMAINS (v8:
animals, vehicles, shapes, elements, and planets as a separately reported stratum; --three-step-domains overrides it).
Format classes (v8): text (prose, chat, document) and structured (json, table, code); three-step chains are much harder
through structured records, so every analysis and level pick splits by format_class.
Number style: each scene states its lockers and bins as digits ("is 7") or as number words ("is seven"); digit answers
are always asked for as a digit, so with number words a prompt lookup cannot copy its answer token verbatim (it still
copies the value and converts it: this removes token copying, not lookup by copying). Report P->M->P by number style:
its bin rules show the middle number next to the answer.
Entities: the start thing, its partner and C's bridge are drawn with sqrt_weights (between uniform answers and uniform
things); each item records chance_same_answer, the share of the scene's other things whose chain gives its answer, and
eligible() leaves out scenes where it is >= 0.5 (the answer does not depend on the bridge).
Downstream runs compare words at one level (eligible(): the hardest level where all compared words score >= 85%).
Domains: controlled tier (single-token names; with --counterfactuals each scene also gets suite_v1-style C and O,
token-aligned: C changes only the first bridge, and so every word's answer, O swaps two other people's picks) animals,
planets, elements, Greek letters; knock-out tier adds shapes, vehicles, instruments (multi-token names allowed).
Formats (only the facts change; the question is the same): prose, json (tool outputs), table (markdown), code (Python
dicts), chat (facts in an earlier user turn), document (facts inside a short record). Every relation's rows are
shuffled separately in json, table and code (no answer by row position); bin tables name the property (bin_by_legs).
Knobs (one ladder, LEVELS): entities (capped by the domain's size; item["n_things"] records it), look-alike distractors
(the queried person and one other get a look-alike name with another pick), filler (sentences, records or code lines,
by format), paraphrase (every whole-question template has two wordings) and hard cues (indirect cues for the M start).
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
WORDS3 = ("PPP", "PPM", "PMP", "MPP", "MPM", "MMP")  # v6: the reverse lookups (PMM, MMM) dropped (Zach, 2026-10-21)
FORMATS = ("prose", "json", "table", "code", "chat", "document")
C_OPS = ("typo", "reverse", "letters")  # v6: Caesar (31% even alone) and acrostic (33% when nested) dropped
NUMBER_WORDS = S.WORDS  # zero ... nine
ORDINAL_WORDS = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
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


# Cues name one thing of the domain alone and never state or imply its number: every animal cue says "the animal" (no
# "insect", "bird" or "big cat", which imply 6, 2 or 4 legs), no rank words ("closest", "lightest", "first", alpha's
# "leader"), no cartoon characters (drawn on two legs), no other thing of the domain; facts with more than one common
# answer are left out (wagon wheels, banjo strings). Second review, 2026-10-20.
ANIMALS = _table({
    "dog": (4, "the animal known for barking", "the animal people call man's best friend"),
    "cat": (4, "the animal known for purring", "the animal ancient Egyptians worshipped as the goddess Bastet"),
    "cow": (4, "the animal known for mooing", "the animal that gives us most of our milk"),
    "horse": (4, "the animal known for neighing", "the animal ridden in the Kentucky Derby"),
    "mouse": (4, "the animal known for squeaking", "the animal that cheese-baited traps are set for"),
    "wolf": (4, "the wild animal that hunts in packs and howls at the moon", "the animal that raised Romulus and Remus"),
    "pig": (4, "the animal known for oinking", "the animal bacon comes from"),
    "sheep": (4, "the animal known for its wool", "the animal whose young is called a lamb"),
    "lion": (4, "the animal called the king of the jungle", "the animal that lives in prides"),
    "frog": (4, "the animal known for croaking", "the animal that starts life as a tadpole"),
    "tiger": (4, "the animal with orange and black stripes", "the animal whose Bengal and Siberian kinds are endangered"),
    "bear": (4, "the animal that hibernates in a den and loves honey", "the animal whose polar kind lives in the Arctic"),
    "fox": (4, "the animal known for its bushy red tail", "the animal whose female is called a vixen"),
    "rabbit": (4, "the animal known for its long ears and hopping", "the animal that lives in a warren"),
    "goat": (4, "the animal known for climbing cliffs and bleating", "the animal whose young is called a kid"),
    "deer": (4, "the animal whose males grow antlers", "the animal venison comes from"),
    "zebra": (4, "the animal known for its black and white stripes", None),
    "elephant": (4, "the animal known for its trunk", "the animal whose tusks are ivory"),
    "giraffe": (4, "the animal known for its long neck", "the tallest animal on land"),
    "camel": (4, "the animal known for its humps", "the animal called the ship of the desert"),
    "duck": (2, "the animal known for quacking", "the animal roasted in the famous Peking dish"),
    "goose": (2, "the animal known for honking", "the animal whose male is called a gander"),
    "chicken": (2, "the animal known for clucking", "the animal that lays most of the eggs we eat"),
    "turkey": (2, "the animal known for gobbling", "the animal eaten at Thanksgiving"),
    "owl": (2, "the animal known for hooting", "the animal that can turn its head almost all the way around"),
    "parrot": (2, "the animal known for imitating human speech", "the animal a pirate keeps on his shoulder"),
    "penguin": (2, "the animal that waddles across the Antarctic ice", "the animal that huddles through the polar winter"),
    "eagle": (2, "the animal on the Great Seal of the United States", None),
    "swan": (2, None, None),
    "crow": (2, None, None),
    "bee": (6, "the animal known for making honey", "the animal that dances to show where flowers are"),
    "ant": (6, "the animal known for living in colonies and carrying crumbs", "the animal that farms aphids"),
    "butterfly": (6, "the animal that starts life as a caterpillar", None),
    "fly": (6, "the animal people swat in the kitchen", "the animal that maggots grow into"),
    "beetle": (6, None, None),
    "spider": (8, "the animal known for spinning webs", "the animal Charlotte is in Charlotte's Web"),
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
    "beryllium": (4, None, None),
    "boron": (5, None, None),
    "carbon": (6, "the element diamonds are made of", "the element every organic compound contains"),
    "nitrogen": (7, "the gas that makes up most of the air", "the element bacteria in bean roots take from the air"),
    "oxygen": (8, "the gas we need to breathe", "the element ozone is made of"),
    "fluorine": (9, "the element added to toothpaste to protect teeth", "the most electronegative element"),
})  # fmt: skip
GREEK = _table({  # no hard cues (the few there were all named letters 2-4); alpha and epsilon have no clean cue
    "alpha": (1, None, None),
    "beta": (2, "the Greek letter of the radioactive decay that emits electrons", None),
    "gamma": (3, "the Greek letter that names the most energetic rays", None),
    "delta": (4, "the Greek letter that names a river mouth", None),
    "epsilon": (5, None, None),
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
Q_BIN = ("Which bin does {d} go in?", "In which bin does {d} go?")
# v6 (Zach, 2026-10-21, after tasks3_ab_v1: "Things numbered 4 go in bin 5" left P->M->P at 15%; a rule keyed by the
# property brought it to 72-85%): one rule per number the domain has, in its own terms.
BIN_RULE = {"animals": "Animals with {n} legs go in bin {b}.", "vehicles": "Vehicles with {n} wheels go in bin {b}.",
            "instruments": "Instruments with {n} strings go in bin {b}.", "shapes": "Shapes with {n} sides go in bin {b}.",
            "planets": "The {o} planet from the Sun goes in bin {b}.", "elements": "Elements with atomic number {n} go in bin {b}.",
            "greek": "The {o} letter of the Greek alphabet goes in bin {b}."}  # fmt: skip
BIN_STEP = {"animals": "Which bin do animals with {n} legs go in?", "vehicles": "Which bin do vehicles with {n} wheels go in?",
            "instruments": "Which bin do instruments with {n} strings go in?", "shapes": "Which bin do shapes with {n} sides go in?",
            "planets": "Which bin does the {o} planet from the Sun go in?", "elements": "Which bin do elements with atomic number {n} go in?",
            "greek": "Which bin does the {o} letter of the Greek alphabet go in?"}  # fmt: skip
BIN_KEY = {"animals": "legs", "vehicles": "wheels", "instruments": "strings", "shapes": "sides",
           "planets": "position_from_sun", "elements": "atomic_number", "greek": "alphabet_position"}  # fmt: skip
# Each word's context states only what its question needs (v6, after tasks3_ab_v1: extra numbers in the context cost
# three-step questions 10-15 points); the scene (people, picks, things, start) stays shared within a group.
CONTEXT_RELS = {"PP": ("locker",), "PM": ("locker",), "MP": ("locker",), "MM": ("locker",), "CP": ("locker",),
                "CM": ("locker",), "PPP": ("partner", "locker"), "MPP": ("partner", "locker"), "PPM": ("partner", "locker"),
                "MPM": ("partner", "locker"), "PMP": ("bin",), "MMP": ("bin",)}  # fmt: skip
# v7 (review, 2026-10-21): PPM/MPM keep PPP/MPP's lockers, as PM keeps PP's, so each last-step pair (P vs M) reads one
# context; PMP/MMP read the bins only (as the suite's BRL reads its locker table).
THREE_STEP_DOMAINS = ("animals", "vehicles", "shapes", "elements", "planets")
SECONDARY_THREE_STEP = ("planets",)
# v8 (Zach, 2026-10-21, after calib_v7_3 on all seven domains): three-step words on the core four (animals, vehicles,
# shapes, elements) and planets as a separately reported stratum (good on PPP/MPP only); out: Greek letters (0-83% in
# every three-step word, text formats included) and instruments (two string counts: answers guessable).
TEXT_FORMATS = ("prose", "chat", "document")  # "easy" formats; json, table, code are "structured" (hard for 3 steps)


def format_class(it: dict) -> str:
    """text (prose, chat, document) or structured (json, table, code): three-step chains through structured records
    are much harder for the 27B (calib_v7_3: P->M->P 70-96% in text, 32-63% in code), so analyses split by it."""
    return "text" if it["format"] in TEXT_FORMATS else "structured"


def stratum(it: dict) -> str:
    """core, or secondary for three-step items on SECONDARY_THREE_STEP domains (reported separately)."""
    return "secondary" if len(it["word"]) == 3 and it["domain"] in SECONDARY_THREE_STEP else "core"


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
    "Alice": "Alina", "Anna": "Anita", "Beth": "Bertha", "Clara": "Claudia", "Diana": "Dinah", "Emma": "Emily",
    "Eva": "Evelyn", "Fiona": "Flora", "Grace": "Greta", "Iris": "Isla", "Julia": "June", "Kate": "Karen",
    "Laura": "Layla", "Lily": "Lisa", "Lucy": "Luna", "Maria": "Marta", "Mia": "Mina", "Nina": "Nora", "Olivia": "Olga",
    "Rose": "Ruth", "Sara": "Sandra", "Tara": "Talia", "Vera": "Velma", "Zoe": "Zelda", "Ella": "Elsa", "Ruby": "Rhea",
    "Amy": "Ada", "Eve": "Edna", "Ivy": "Ida", "Adam": "Aaron", "Ben": "Bert", "Carl": "Cole", "Dan": "Dean",
    "David": "Darren", "Eric": "Ernest", "Finn": "Fred", "Frank": "Floyd", "Henry": "Herbert", "Ivan": "Igor",
    "Jack": "Jason", "James": "Jared", "Leo": "Levi", "Luke": "Lance", "Mark": "Martin", "Max": "Mason", "Noah": "Nolan",
    "Oscar": "Otto", "Paul": "Percy", "Peter": "Philip", "Sam": "Seth", "Tom": "Ted", "Victor": "Vincent", "Will": "Wade",
    "Hugo": "Hank", "Owen": "Oliver", "Liam": "Lloyd", "Ryan": "Rex", "Sean": "Simon", "Kyle": "Keith",
}  # fmt: skip
assert set(NEAR) == set(S.PEOPLE), "NEAR must cover PEOPLE"
assert not set(NEAR.values()) & set(S.PEOPLE), "look-alikes must not be real people"
assert len(set(NEAR.values())) == len(NEAR), "look-alikes must be distinct"
ABSENT = ("Quinn", "Yusuf", "Wanda", "Xavier", "Odette", "Bartholomew")  # never in a scene (guess prompts)


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
    if op == "typo":  # two neighbouring letters swapped: never contains x, never another thing's name; names of 5+
        if len(x) < 5:  # letters only (short ones make real words: cat -> act, eta -> tea, lion -> loin)
            return None
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


def sqrt_weights(things: list[str], dom: Domain) -> list[float]:
    """1/sqrt(how many of these things share the thing's number): between uniform numbers (balanced answers, the few
    6- and 8-legged animals recur) and uniform things (diverse bridges, answers skewed to 4 legs). Zach, 2026-10-20."""
    per_value = collections.Counter(dom.values[t] for t in things)
    return [per_value[dom.values[t]] ** -0.5 for t in things]


def weighted_order(rng: random.Random, things: list[str], dom: Domain) -> list[str]:
    """A random order of the things, drawn without replacement with sqrt_weights (Efraimidis-Spirakis keys)."""
    keys = [rng.random() ** (1 / w) for w in sqrt_weights(things, dom)]
    return [t for _, t in sorted(zip(keys, things, strict=True), reverse=True)]


def scene(rng: random.Random, dom: Domain, group: str, knobs: dict, style: str) -> dict | None:
    """People, their picks (the start thing x is the queried person's), pairs of partners, lockers (never a thing's
    memory number), bins (no bin holds its own number) and look-alikes. x and its partner are drawn with sqrt_weights."""
    ok = start_ok(group, dom, knobs)
    cands = [t for t in dom.values if ok(t)]
    if not cands:  # e.g. hard cues asked of a domain that has none
        return None
    x = rng.choices(cands, weights=sqrt_weights(cands, dom))[0]
    n_ent = min(knobs["entities"], len(dom.values))
    rest = [t for t in dom.values if t != x]
    y = rng.choices(rest, weights=sqrt_weights(rest, dom))[0]
    others = rng.sample([t for t in rest if t != y], n_ent - 2)
    things = [x, y, *others]
    rng.shuffle(things)
    people = rng.sample(S.PEOPLE, len(things))
    pick = dict(zip(people, things, strict=True))
    person = people[things.index(x)]
    single = rng.choice(others) if len(others) % 2 else None
    pairable = [t for t in others if t != single]
    rng.shuffle(pairable)
    pairs = [(x, y), *zip(pairable[0::2], pairable[1::2], strict=True)]
    rng.shuffle(pairs)
    pairs = [(a, b) if rng.random() < 0.5 else (b, a) for a, b in pairs]
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


def confusable_picks(sc: dict) -> list[str]:
    """Picks of look-alike rows that could pass for the queried person: their own look-alike, and any other look-alike
    whose name starts with the same two letters (Owen's look-alike Oliver next to Olivia)."""
    p = sc["person"]
    return [t for name, t in sc["lookalike_picks"] if name == NEAR[p] or name[:2] == p[:2]]


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
            steps.append(step(BIN_STEP[dom_name(dom)].format(n=n, o=ORDINAL_WORDS[n]), str(b), "digit", "P"))
            return {"question": Q_BIN[para].format(d=desc), "answer": str(b), "kind": "digit", "steps": steps}
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


def dom_name(dom: Domain) -> str:
    return next(k for k, v in DOMAINS.items() if v is dom)


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
            alts.append(str(n))  # the bin step skipped (v6: no lockers in a bin question's context)
        else:
            alts.append(next((t for t, v in dom2.values.items() if v == lk), None))  # locker read as the number
        x = None
    if x is not None:
        alts.append(str(dom.values[x] if rest == "P" else sc["locker"][x]))  # the other relation
    if word[0] == "P":
        alts += [follow(word, dom, sc, t, dom2)[0] for t in confusable_picks(sc) if t != start]
    return [a for a in alts if a is not None]


# ---- formats ------------------------------------------------------------------------------------------------------
def render_facts(fmt: str, dom: Domain, sc: dict, rng: random.Random, n_filler: int, rels: tuple[str, ...]) -> str:
    """The scene's picks and the relations in rels (partner, locker, bin) in one format. The draws depend only on the
    scene's sizes and rels, so a generator seeded alike renders C and O with the clean prompt's layout."""
    st = sc["numbers"]
    d = dom_name(dom)
    picks = list(sc["pick"].items()) + sc["lookalike_picks"]
    pairs = list(sc["pairs"]) if "partner" in rels else []
    lockers = list(sc["locker"].items()) if "locker" in rels else []
    bins = [(n, sc["bin"][n]) for n in sorted(set(dom.values.values()))] if "bin" in rels else []
    both = [(a, b) for a, b in pairs] + [(b, a) for a, b in pairs]
    if fmt in ("prose", "chat", "document"):
        lines = [f"{p} picked {ref(dom, t)}." for p, t in picks]
        lines += [f"{cap(ref(dom, a))}'s partner is {ref(dom, b)}." for a, b in both]
        lines += [f"The locker of {ref(dom, t)} is {num(n, st)}." for t, n in lockers]
        lines += [BIN_RULE[d].format(n=num(n, st), b=num(b, st), o=ORDINAL_WORDS[n]) for n, b in bins]
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
           "bins": (BIN_KEY[d], "bin", [(val(n), val(b)) for n, b in bins])}  # fmt: skip
    rel = {k: v for k, v in rel.items() if v[2] or k == "picks"}
    for _, _, rows in rel.values():
        rng.shuffle(rows)
    rooms = [(r, rng.choice(PAINTS)) for r in rng.sample(ROOMS, n_filler)] if fmt in ("json", "table") else []
    if rooms:
        rel["rooms"] = ("room", "paint", rooms)
    order = list(rel)
    rng.shuffle(order)
    if fmt == "json":
        tool = {"bins": f"get_bins_by_{BIN_KEY[d]}"}
        return "\n".join(f"Tool output from {tool.get(k, 'get_' + k)}:\n" + json.dumps([{rel[k][0]: a, rel[k][1]: b} for a, b in rel[k][2]])
                         for k in order)  # fmt: skip
    if fmt == "table":
        return "\n\n".join(f"Table {k}:\n| {rel[k][0]} | {rel[k][1]} |\n|---|---|\n"
                           + "\n".join(f"| {a} | {b} |" for a, b in rel[k][2]) for k in order)  # fmt: skip
    if fmt == "code":
        name = {"bins": f"bin_by_{BIN_KEY[d]}"}  # the property named in code too (bin_by_legs), not abstract "bins"
        lines = [f"{name.get(k, k)} = {dict(rel[k][2])!r}" for k in order]
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
    render_seed = rng.random()  # every word's context (and C's and O's) is drawn from Random(render_seed)
    items = []
    for word in words:
        para = int(rng.random() < 0.5) if knobs["paraphrase"] else 0
        d2 = dom2 if word[1:] == "MM" else None
        ch = chain(word, dom, sc, x, desc, d2, para)
        if ch is None or ch["answer"] in wrong_routes(word, dom, sc, x, d2):
            return None
        others = [t for t in sc["things"] if t != x]
        chance = sum(follow(word, dom, sc, t, d2)[0] == ch["answer"] for t in others) / len(others)
        context = render_facts(fmt, dom, sc, random.Random(render_seed), knobs["filler"], CONTEXT_RELS[word])
        items.append({"chance_same_answer": round(chance, 3), "word": word, "domain": domain, "format": fmt, "knobs": knobs, "c_op": c_op,
                      "domain2": dom2_name if d2 else None, "numbers": style, "n_things": len(sc["things"]),
                      "context": context, "context_rels": list(CONTEXT_RELS[word]), "render_seed": render_seed,
                      "format_class": "text" if fmt in TEXT_FORMATS else "structured",
                      "stratum": "secondary" if len(word) == 3 and domain in SECONDARY_THREE_STEP else "core",
                      "question": ch["question"],
                      "answer": ch["answer"], "kind": ch["kind"], "steps": [first, *ch["steps"]], "tier": dom.tier,
                      "start_desc": desc})  # fmt: skip
    if tok is None:
        return items
    assert dom.tier == "controlled", domain
    cf = counterfactuals(tok, items, group, dom, sc, desc, dom2, render_seed, knobs["filler"])
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
                    render_seed: float, n_filler: int) -> list[dict] | None:  # fmt: skip
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

    def context_of(scene_: dict, i: int) -> str:
        return render_facts(items[i]["format"], dom, scene_, random.Random(render_seed), n_filler,
                            CONTEXT_RELS[items[i]["word"]])  # fmt: skip

    clean_ids = [S.ids(tok, render(tok, it)) for it in items]

    def aligned(i: int, context: str, question: str, limit: int) -> list[int] | None:
        got = S.changed(clean_ids[i], S.ids(tok, render(tok, {**items[i], "context": context, "question": question})))
        return got if got and len(got) <= limit else None

    others = [p for p in sc["people"] if p != person]
    cues = dom.hard_cues if items[0]["knobs"]["hard_cues"] else dom.cues
    la = confusable_picks(sc)
    for X in weighted_order(rng, [t for t in sc["things"] if t != x], dom):
        if not _single(tok, X) or X in la:
            continue
        if group == "P":
            q = next(p for p in others if sc["pick"][p] == X)
            cf_sc, limit = _swap_picks(sc, person, q), MAX_SWAP_CHANGED
            cf_contexts, new_desc = [context_of(cf_sc, i) for i in range(len(items))], desc
        else:
            new_desc = cues.get(X) if group == "M" else c_description(items[0]["c_op"], dom, X, rng)
            if new_desc is None:
                continue
            cf_sc, cf_contexts, limit = sc, [it["context"] for it in items], 10**6
        out = []
        for i, it in enumerate(items):
            assert it["question"].count(desc) == 1, it["question"]
            cf_q = it["question"].replace(desc, new_desc)
            cf_answer, cf_bridges = follow(it["word"], dom, cf_sc, X, d2[it["word"]])
            ok = cf_answer not in (None, it["answer"]) and all(
                follow(it["word"], dom, sc, t, d2[it["word"]])[0] != cf_answer for t in la
            )  # no look-alike route to the C answer
            ok = ok and S.answer_token(tok, cf_answer, it["kind"]) != S.answer_token(tok, it["answer"], it["kind"])
            cf_context = cf_contexts[i]
            changed = aligned(i, cf_context, cf_q, limit) if ok else None
            if not changed:
                break
            out.append({"cf_context": cf_context, "cf_question": cf_q, "cf_answer": cf_answer, "cf_bridge": X,
                        "cf_bridges": cf_bridges, "cf_changed_tokens": len(changed)})  # fmt: skip
        if len(out) == len(items):
            break
    else:
        return None
    for a, b in rng.sample(list(itertools.combinations(others, 2)), len(others) * (len(others) - 1) // 2):
        off_sc = _swap_picks(sc, a, b)
        off_contexts = [context_of(off_sc, i) for i in range(len(items))]
        offs = [aligned(i, off_contexts[i], it["question"], MAX_SWAP_CHANGED) for i, it in enumerate(items)]
        if all(offs):
            return [{**c, "off_context": oc, "off_changed_tokens": len(o), "bridge": x,
                     "bridges": follow(it["word"], dom, sc, x, d2[it["word"]])[1], "answer_kind": it["kind"],
                     "scene_facts": {k: sc[k] for k in ("pick", "pairs", "locker")}}
                    for c, o, oc, it in zip(out, offs, off_contexts, items, strict=True)]  # fmt: skip
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
    """Scene groups: the words that start alike and have the same length (v6: three-step words have their own scenes,
    on THREE_STEP_DOMAINS), e.g. P2 = PP, PM; P3 = PPP, PPM, PMP."""
    out: dict[str, list[str]] = {}
    for w in words:
        out.setdefault(f"{w[0]}{len(w)}", []).append(w)
    return out


def make(name: str, n: int, words: list[str], domains: list[str], formats: list[str], levels: list[int], seed: int,
         counterfactuals: bool = False, three_step_domains: list[str] | None = None) -> None:  # fmt: skip
    """n scenes per start group x level, each asked with every word of its group, spread evenly over the domain x
    format combinations that can carry the group, each word's digit answers capped at twice their uniform share.
    Write-once; a shortfall (fewer than n scenes) stops it."""
    unknown = [w for w in words if w not in CONTEXT_RELS]
    assert not unknown, f"unknown words {unknown} (v6 dropped PMM and MMM)"
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
            doms = [d for d in domains if group[1] == "2" or d in (three_step_domains or THREE_STEP_DOMAINS)]
            combos = [(d, f) for d in doms for f in formats]
            rng.shuffle(combos)
            answers = {w: collections.Counter() for w in gwords}
            got, dead, used = 0, set(), collections.Counter()
            while got < n and len(dead) < len(combos):
                for d, f in combos:
                    if got >= n or (d, f) in dead:
                        continue
                    for _ in range(60):  # a combination that yields nothing in 60 draws cannot carry this group
                        its = make_scene(rng, group[0], gwords, d, f, LEVELS[level], domains, tok)
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
            "levels": {k: LEVELS[k] for k in levels}, "seed": seed, "generator": "scripts/tasks_v2.py make (v8)",
            "git_commit": commit, "counterfactuals": counterfactuals, "n_items": len(items), "coverage": coverage,
            "three_step_domains": list(three_step_domains or THREE_STEP_DOMAINS)}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", out / "items.jsonl", len(items), "items")


def examples(seed: int) -> None:
    rng = random.Random(seed)
    for group, words in groups_of(list(WORDS2 + WORDS3)).items():
        for _ in range(200):
            doms = (
                ["animals", "planets", "elements", "greek"] if group[1] == "2" else ["animals", "vehicles", "elements"]
            )
            its = make_scene(rng, group[0], words, rng.choice(doms), "prose", LEVELS[1], list(DOMAINS))
            if its:
                break
        print(f"\n=== {group} scene ({its[0]['domain']}, numbers as {its[0]['numbers']}"
              f"{', ' + its[0]['c_op'] if its[0]['c_op'] else ''})")  # fmt: skip
        for it in its:
            print(f"  {it['word']:4s} context ({'+'.join(['picks', *it['context_rels']])}): {it['context'][:300]}")
            print(f"  {it['word']:4s} Q: {it['question']} -> {it['answer']}")
            print("        steps:", " | ".join(f"{s['source']}: {s['question']} -> {s['answer']}" for s in it["steps"]))
    for fmt in FORMATS:
        for k in range(200):
            its = make_scene(random.Random(seed + k), "P", ["PMP"], "animals", fmt, LEVELS[1], list(DOMAINS))
            if its:
                break
        print(f"\n=== format {fmt} (PMP, animals, level 1)\n{its[0]['context'][:900]}\nQ: {its[0]['question']}")


def load(name: str) -> list[dict]:
    return [json.loads(line) for line in (DATA / name / "items.jsonl").read_text().splitlines()]


ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
            "ninth": 9}  # fmt: skip
ALL_THINGS = {t.lower() for dom in DOMAINS.values() for t in dom.values}


PLURALS = {"mice": "mouse", "geese": "goose", "oxen": "ox"}
COMPOUNDS = {"honeybee": "bee", "bumblebee": "bee", "housefly": "fly", "bullfrog": "frog", "warthog": "pig"}
NAMES = {n.lower() for n in [*S.PEOPLE, *NEAR.values(), *ABSENT]}


def thing_of(token: str) -> str | None:
    """The thing a word names: itself, its plural (bees, foxes, mice), or a listed compound (honeybee); names of
    people never count (Oscar is not a car, Greta is not eta)."""
    if token in NAMES:
        return None
    for t in (token, PLURALS.get(token), COMPOUNDS.get(token), token[:-1] if token.endswith("s") else None,
              token[:-2] if token.endswith("es") else None):  # fmt: skip
        if t in ALL_THINGS:
            return t
    return None


def judge(text: str, answer: str, kind: str) -> bool:
    """Digit: the first number in the first line (digits, number words or ordinals). Word: the first thing named in
    the first line is the answer, reading a run of thing words as one name with its last word as the head ("deer
    tick" is a tick, "eagle owl" an owl)."""
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
    named = [thing_of(t) for t in re.findall(r"[a-z]+", line)]
    for k, th in enumerate(named):
        if th is None:
            continue
        while k + 1 < len(named) and named[k + 1] is not None:
            k += 1
        return named[k] == answer.lower()
    return False


def eligible(set_name: str, comp_run: str, words: list[str], n: int, level: str = "pick", max_chance: float = 0.5,
             fmt_class: str | None = None, strata: tuple[str, ...] = ("core",),
             domains: list[str] | None = None) -> list[dict]:  # fmt: skip
    """The items a downstream run compares: from scenes whose items of the compared words the competence run got right
    on every prompt (whole, each step, C and O; the guess prompt excluded), at one level for the whole comparison
    (level "pick": the hardest level where every compared word scores >= 85% whole; "all"; or a level number; Zach,
    2026-10-20: per compared words), the first n per word in file order. Each item gets "guessable": whether the model
    answered its guess prompt right (None if the run had none). Every compared word must get items. v8: fmt_class
    ("text" or "structured") restricts to one format class and picks the level from that class's accuracy; strata
    (default core only; ("core", "secondary") or ("secondary",) for planets' three-step items) and domains restrict
    further. A word below 85% at every level (M->P->M) is compared at an explicit level (e.g. "0"), labeled below band."""
    run_dir = pins.RESULTS_DIR / "tasks_v2" / comp_run
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    guessed: dict[str, bool] = {}
    for line in (run_dir / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["part"] == "guess":
            guessed[r["id"]] = r["correct"]
        else:
            ok[r["id"]].append(r["correct"])
    items = [
        it
        for it in load(set_name)
        if it["word"] in words
        and stratum(it) in strata
        and (fmt_class is None or format_class(it) == fmt_class)
        and (it["domain"] in domains if domains else len(it["word"]) == 2 or it["domain"] in THREE_STEP_DOMAINS)
    ]  # three-step items outside THREE_STEP_DOMAINS (from measurement sets) only when asked for by domains
    # v7 (review): an item whose answer half or more of the scene's other things would also give does not test the
    # bridge (instruments: every thing with 4 strings); it is left out (with its scene, below) of downstream runs
    bridge_free = {it["scene"] for it in items if it.get("chance_same_answer", 0) >= max_chance}
    if level == "pick":
        whole = collections.defaultdict(list)  # accuracy on the selected items only (format class, strata, domains)
        right = {r["id"]: r["correct"] for r in map(json.loads, (run_dir / "items.jsonl").read_text().splitlines())
                 if r["part"] == "whole"}  # fmt: skip
        for it in items:
            if it["id"] in right:
                whole[(it["word"], it["level"])].append(right[it["id"]])
        acc = {k: sum(v) / len(v) for k, v in whole.items()}
        levels = sorted({it["level"] for it in items})
        good = [lv for lv in levels if all(acc.get((w, lv), 0) >= BAND[0] for w in words)]
        assert good, f"no level has every one of {words} at >= {BAND[0]:.0%}"
        want = good[-1]
    else:
        want = None if level == "all" else int(level)
    scene_ok: dict[str, bool] = collections.defaultdict(lambda: True)
    for it in items:
        scene_ok[it["scene"]] &= bool(ok.get(it["id"])) and all(ok[it["id"]]) and it["scene"] not in bridge_free
    out, got = [], collections.Counter()
    for it in items:
        if got[it["word"]] >= n or not scene_ok[it["scene"]] or (want is not None and it["level"] != want):
            continue
        got[it["word"]] += 1
        out.append({**it, "guessable": guessed.get(it["id"]), "compared_level": want})
    missing = [w for w in words if not got[w]]
    assert not missing, f"no eligible items for {missing} at level {want}"
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
    ap.add_argument(
        "--three-step-domains",
        nargs="+",
        default=None,
        help="make: domains for three-step words (default THREE_STEP_DOMAINS; e.g. planets greek to measure them)",
    )
    ap.add_argument("--guess", action="store_true", help="competence: add the guess prompt (start made unknown)")
    args = ap.parse_args()
    if args.stage == "examples":
        examples(args.seed)
    elif args.stage == "make":
        make(
            args.set_name,
            args.n,
            args.words,
            args.domains,
            args.formats,
            args.levels,
            args.seed,
            args.counterfactuals,
            args.three_step_domains,
        )
    else:
        competence(args.set_name, args.name, args.why, args.guess)
