"""tasks_v2: the breadth task generator (Zach, 2026-10-20; design decided with Zach the same day).

Every task is a chain of steps; each step retrieves from the Prompt (P), from Memory (M) or is Computed from the input
(C). A family is its "word": 2-step PP, PM, MP, MM, CP, CM and all eight 3-step words PPP ... MMM. Relations:
  start     P  a person's pick, stated in the prompt          "Clara picked Mars."
            M  a cue, recalled                                 "the red planet" -> Mars
            C  a string computation on the input               typo, reversal, letter count, Caesar shift, acrostic
  thing ->  P  its partner (prompt)  or its locker (prompt, a digit)
            M  its number (memory: legs, position from the Sun, atomic number, alphabet position, sides, ...)
  number -> P  the bin for that number (prompt, a digit)
            M  the thing with that number in another domain (memory; the answer is then a word: P-M-M, M-M-M)
Domains: controlled tier (single-token names; later also aligned counterfactuals) animals, planets, elements, Greek
letters; knock-out tier adds shapes, vehicles, instruments (multi-token names allowed).
Formats (only the facts change; the question is the same): prose, json (tool outputs), table (markdown), code (Python
dicts), chat (facts in an earlier user turn), document (facts inside a short record among filler).
Knobs (for calibrating each family to 85-95% on the target model): entities 3/6/12, distractors (look-alike names and
facts nobody asks about), filler 0/5/20, surface paraphrase of the question.
Each item also carries every step alone (same context) for per-step knock-outs.

python scripts/tasks_v2.py examples [--seed S]          one item per word x format, printed
python scripts/tasks_v2.py make --set NAME --n N ...    write data/tasks_v2/NAME/items.jsonl (write-once)
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
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


@dataclass(frozen=True)
class Domain:
    noun: str  # "planet"
    values: dict  # thing -> its number (memory)
    cues: dict  # thing -> cue phrase that recalls it
    prop_q: str  # question for the number, "{x}" = description of the thing
    prop_phrase: str  # noun phrase for the number, "{x}" = description of the thing
    reverse_q: str | None  # question for number -> thing, "{n}" = a digit; None: the number does not pick one thing
    reverse_desc: str | None  # the same with "{n}" = a described number (a noun phrase)
    article: bool  # "the cow" vs "Mars"
    tier: str  # "controlled" or "knockout"


ANIMAL_CUES = {a: f"the animal known for {cue}" for a, (_, cue) in S.ANIMALS.items()}
DOMAINS = {
    "animals": Domain("animal", {a: legs for a, (legs, _) in S.ANIMALS.items()}, ANIMAL_CUES,
                      "How many legs does {x} have?", "the number of legs of {x}", None, None, True, "controlled"),
    "planets": Domain("planet", {"Mercury": 1, "Venus": 2, "Earth": 3, "Mars": 4, "Jupiter": 5, "Saturn": 6, "Uranus": 7,
                                 "Neptune": 8},
                      {"Mercury": "the planet closest to the Sun", "Venus": "the hottest planet",
                       "Earth": "the planet we live on", "Mars": "the red planet", "Jupiter": "the largest planet",
                       "Saturn": "the planet best known for its rings", "Uranus": "the planet that spins on its side",
                       "Neptune": "the planet farthest from the Sun"},
                      "Counting from the Sun, which position is {x}?", "the position of {x} counting from the Sun",
                      "Which planet is at position {n} counting from the Sun?",
                      "Which planet's position counting from the Sun equals {n}?", False, "controlled"),
    "elements": Domain("element", {"hydrogen": 1, "helium": 2, "lithium": 3, "beryllium": 4, "boron": 5, "carbon": 6,
                                   "nitrogen": 7, "oxygen": 8, "fluorine": 9},
                       {"hydrogen": "the lightest element", "helium": "the gas that makes party balloons float",
                        "lithium": "the metal in most phone batteries", "carbon": "the element diamonds are made of",
                        "nitrogen": "the gas that makes up most of the air", "oxygen": "the gas we need to breathe",
                        "fluorine": "the element in fluoride toothpaste"},
                       "What is the atomic number of {x}?", "the atomic number of {x}",
                       "Which element has atomic number {n}?", "Which element's atomic number equals {n}?", False, "controlled"),
    "greek": Domain("Greek letter", {"alpha": 1, "beta": 2, "gamma": 3, "delta": 4, "epsilon": 5, "zeta": 6, "eta": 7,
                                     "theta": 8, "iota": 9},
                    {"alpha": "the Greek letter that names the first test version of software",
                     "beta": "the Greek letter that names the second test version of software",
                     "gamma": "the Greek letter that names the most energetic rays", "delta": "the Greek letter that names a river mouth",
                     "epsilon": "the Greek letter mathematicians use for a tiny amount",
                     "theta": "the Greek letter most used for angles", "iota": "the Greek letter that means a very small amount"},
                    "Which position in the Greek alphabet does {x} have?", "the position of {x} in the Greek alphabet",
                    "Which Greek letter is at position {n} in the Greek alphabet?",
                    "Which Greek letter's position in the Greek alphabet equals {n}?", False, "controlled"),
    "shapes": Domain("shape", {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "heptagon": 7, "octagon": 8,
                               "nonagon": 9},
                     {"triangle": "the shape of a yield sign", "square": "the shape of a chessboard",
                      "pentagon": "the shape of the US defense headquarters", "hexagon": "the shape of a honeycomb cell",
                      "octagon": "the shape of a stop sign"},
                     "How many sides does {x} have?", "the number of sides of {x}",
                     "Which polygon has {n} sides?", "Which polygon has as many sides as {n}?", True, "knockout"),
    "vehicles": Domain("vehicle", {"unicycle": 1, "bicycle": 2, "motorcycle": 2, "tricycle": 3, "car": 4, "wagon": 4},
                       {"unicycle": "the vehicle a circus performer balances on", "bicycle": "the vehicle in the Tour de France",
                        "motorcycle": "the vehicle a biker rides", "tricycle": "the vehicle a toddler pedals",
                        "car": "the vehicle most families drive"},
                       "How many wheels does {x} have?", "the number of wheels of {x}", None, None, True, "knockout"),
    "instruments": Domain("instrument", {"violin": 4, "viola": 4, "cello": 4, "guitar": 6, "ukulele": 4, "banjo": 5},
                          {"violin": "the instrument a fiddler plays", "guitar": "the instrument Jimi Hendrix played",
                           "ukulele": "the small instrument from Hawaii", "banjo": "the instrument of bluegrass music",
                           "cello": "the large instrument played between the knees"},
                          "How many strings does {x} have?", "the number of strings of {x}", None, None, True, "knockout"),
}  # fmt: skip
REVERSE_DOMAINS = [d for d, dom in DOMAINS.items() if dom.reverse_q]

FILLER = S.FILLER
CODE_FILLER = S.CODE_FILLER


NEAR = {"Clara": "Clare", "Sara": "Sarah", "Mia": "Mira", "Eva": "Ava", "Emma": "Emmy", "Ella": "Ellie", "Anna": "Hanna",
        "Kate": "Katie", "Lucy": "Lucie", "Julia": "Julie", "Laura": "Lauren", "Lily": "Lila", "Rose": "Rosa", "Tom": "Tim",
        "Ben": "Ken", "Sam": "Pam", "Max": "Mac", "Leo": "Lea", "Jack": "Jake", "Luke": "Luca", "Adam": "Aden"}  # fmt: skip


def lookalike(name: str) -> str:
    if name in NEAR:
        return NEAR[name]
    vowels = "aeiou"
    for i, ch in enumerate(name[1:], 1):
        if ch in vowels:
            return name[:i] + vowels[(vowels.index(ch) + 1) % 5] + name[i + 1 :]
    return name + "e"


def ref(dom: Domain, x: str) -> str:
    return f"the {x}" if dom.article else x


# ---- the computed step --------------------------------------------------------------------------------------------
def c_description(op: str, dom: Domain, x: str, rng: random.Random) -> str | None:
    """A description of x that needs a string computation on the input; None if not unique in the domain."""
    if op == "typo":
        i = rng.randrange(1, len(x) - 1)
        typo = x[:i] + x[i] * 2 + x[i + 1 :]
        return f"the {dom.noun} misspelled as '{typo}'"
    if op == "reverse":
        return f"the {dom.noun} whose name written backwards is '{x[::-1]}'"
    if op == "letters":
        same = [y for y in dom.values if len(y) == len(x) and y[0].lower() == x[0].lower()]
        return f"the {dom.noun} whose name has {len(x)} letters and starts with '{x[0]}'" if same == [x] else None
    if op == "caesar":
        shift = "".join(chr((ord(ch.lower()) - 97 + 1) % 26 + 97) if ch.isalpha() else ch for ch in x)
        return f"the {dom.noun} written as '{shift}' with every letter moved one step forward in the alphabet"
    if op == "acrostic":
        words = [rng.choice(ACROSTIC.get(ch.lower(), [ch.upper() + "ix"])) for ch in x]
        return f"the {dom.noun} spelled by the first letters of {', '.join(words)}"
    raise ValueError(op)


ACROSTIC = {
    "a": ["Apple", "Arrow", "Anchor"], "b": ["Bread", "Bottle", "Button"], "c": ["Candle", "Cloud", "Copper"],
    "d": ["Desk", "Drum", "Dune"], "e": ["Engine", "Echo", "Elbow"], "f": ["Feather", "Forest", "Fork"],
    "g": ["Garden", "Glove", "Guitar"], "h": ["Hammer", "Harbor", "Honey"], "i": ["Island", "Ink", "Iron"],
    "j": ["Jacket", "Jungle", "Jar"], "k": ["Kettle", "Kite", "Knot"], "l": ["Ladder", "Lemon", "Lantern"],
    "m": ["Mango", "Marble", "Mirror"], "n": ["Needle", "Nest", "Noodle"], "o": ["Ocean", "Olive", "Oven"],
    "p": ["Pencil", "Pillow", "Pepper"], "q": ["Quilt", "Quarry", "Queen"], "r": ["River", "Rocket", "Ribbon"],
    "s": ["Salt", "Saddle", "Spoon"], "t": ["Table", "Tunnel", "Tiger"], "u": ["Umbrella", "Uniform", "Usher"],
    "v": ["Valley", "Velvet", "Violin"], "w": ["Window", "Wagon", "Whistle"], "x": ["Xylophone"],
    "y": ["Yarn", "Yacht", "Yolk"], "z": ["Zebra", "Zipper", "Zinc"],
}  # fmt: skip


# ---- scenes and chains --------------------------------------------------------------------------------------------
def scene(rng: random.Random, dom: Domain, n_ent: int, lookalikes: bool) -> dict:
    things = rng.sample(sorted(dom.values), min(n_ent, len(dom.values)))
    people = rng.sample(S.PEOPLE, len(things))
    partner = dict(zip(things, things[1:] + things[:1], strict=True))  # a cycle: every thing has one partner
    lockers = dict(zip(things, rng.sample(range(1, 10), len(things)) if len(things) <= 9 else
                       [rng.randrange(1, 10) for _ in things], strict=True))  # fmt: skip
    bins = dict(zip(range(1, 10), rng.sample(range(1, 10), 9), strict=True))
    extra = []
    if lookalikes:  # people whose names look like the real ones', with other picks
        for p in rng.sample(people, min(2, len(people))):
            extra.append((lookalike(p), rng.choice(things)))
    return {"things": things, "people": people, "pick": dict(zip(people, things, strict=True)), "partner": partner,
            "locker": lockers, "bin": bins, "lookalike_picks": extra}  # fmt: skip


def chain(word: str, dom: Domain, sc: dict, rng: random.Random, c_op: str | None, dom2: Domain | None) -> dict | None:
    """The question, its answer and every step alone for one word, or None if this scene cannot carry it."""
    person = rng.choice(sc["people"])
    x = sc["pick"][person]
    steps = []
    # step 1: to a thing
    if word[0] == "P":
        desc = f"{person}'s pick"
        steps.append({"question": f"What did {person} pick?", "answer": x, "kind": "word", "source": "P"})
    elif word[0] == "M":
        if x not in dom.cues:
            return None
        desc = dom.cues[x]
        steps.append({"question": f"What is {dom.cues[x]}?", "answer": x, "kind": "word", "source": "M"})
    else:
        cdesc = c_description(c_op, dom, x, rng)
        if cdesc is None:
            return None
        desc = cdesc
        steps.append({"question": f"What is {cdesc}?", "answer": x, "kind": "word", "source": "C"})
    rest = word[1:]
    # a 3-step word's middle step: P = the thing's partner, M = the thing's number
    if len(rest) == 2:
        if rest[0] == "P":
            y = sc["partner"][x]
            steps.append(
                {"question": f"What is {ref(dom, x)} paired with?", "answer": y, "kind": "word", "source": "P"}
            )
            x, desc = y, f"the partner of {desc}"
            last = rest[1]
            return _finish_thing(last, dom, sc, x, desc, steps)
        n = dom.values[x]
        steps.append({"question": dom.prop_q.format(x=ref(dom, x)), "answer": str(n), "kind": "digit", "source": "M"})
        ndesc = dom.prop_phrase.format(x=desc)
        if rest[1] == "P":
            b = sc["bin"][n]
            steps.append(
                {"question": f"Which bin holds things numbered {n}?", "answer": str(b), "kind": "digit", "source": "P"}
            )
            q = f"Which bin holds things numbered the same as {ndesc}?"
            return {"question": q, "answer": str(b), "kind": "digit", "steps": steps}
        if dom2 is None or n not in dom2.values.values():
            return None
        z = next(t for t, v in dom2.values.items() if v == n)
        steps.append({"question": dom2.reverse_q.format(n=n), "answer": z, "kind": "word", "source": "M"})
        return {"question": dom2.reverse_desc.format(n=ndesc), "answer": z, "kind": "word", "steps": steps}
    return _finish_thing(rest[0], dom, sc, x, desc, steps)


def _finish_thing(source: str, dom: Domain, sc: dict, x: str, desc: str, steps: list) -> dict:
    """The last step from a thing: P = its locker (prompt), M = its number (memory). Both digits."""
    if source == "P":
        n = sc["locker"][x]
        steps.append(
            {"question": f"Which locker belongs to {ref(dom, x)}?", "answer": str(n), "kind": "digit", "source": "P"}
        )
        return {"question": f"Which locker belongs to {desc}?", "answer": str(n), "kind": "digit", "steps": steps}
    n = dom.values[x]
    steps.append({"question": dom.prop_q.format(x=ref(dom, x)), "answer": str(n), "kind": "digit", "source": "M"})
    return {"question": dom.prop_q.format(x=desc), "answer": str(n), "kind": "digit", "steps": steps}


# ---- formats ------------------------------------------------------------------------------------------------------
def facts(word: str, dom: Domain, sc: dict) -> dict[str, list]:
    """The relations the prompt states (always all of them, so a word's facts are not a giveaway)."""
    return {"pick": list(sc["pick"].items()) + sc["lookalike_picks"], "partner": list(sc["partner"].items()),
            "locker": list(sc["locker"].items()), "bin": sorted(sc["bin"].items())}  # fmt: skip


def render_facts(fmt: str, dom: Domain, fx: dict, rng: random.Random, n_filler: int) -> str:
    if fmt in ("prose", "chat", "document"):
        lines = [f"{p} picked {ref(dom, t)}." for p, t in fx["pick"]]
        lines += [
            f"{ref(dom, a).capitalize() if dom.article else a} is paired with {ref(dom, b)}." for a, b in fx["partner"]
        ]
        lines += [f"The locker of {ref(dom, t)} is {n}." for t, n in fx["locker"]]
        lines += [f"Things numbered {n} go in bin {b}." for n, b in fx["bin"]]
        lines += rng.sample(FILLER, min(n_filler, len(FILLER))) if n_filler else []
        rng.shuffle(lines)
        text = " ".join(lines)
        if fmt == "document":
            intro = " ".join(rng.sample(FILLER, 3))
            return f"Club newsletter, autumn term. {intro} From the club's records: {text} That is all for this term."
        return text
    if fmt == "json":
        tools = {"get_picks": [{"name": p, "pick": t} for p, t in fx["pick"]],
                 "get_partners": [{"item": a, "partner": b} for a, b in fx["partner"]],
                 "get_lockers": [{"item": t, "locker": n} for t, n in fx["locker"]],
                 "get_bins": [{"number": n, "bin": b} for n, b in fx["bin"]]}  # fmt: skip
        if n_filler:
            tools["get_weather"] = [
                {"day": d, "sky": rng.choice(["clear", "rain", "fog"])}
                for d in ("Mon", "Tue", "Wed")[: max(1, n_filler // 5)]
            ]
        order = list(tools)
        rng.shuffle(order)
        return "\n".join(f"Tool output from {k}:\n{json.dumps(tools[k])}" for k in order)
    if fmt == "table":
        tabs = {"picks": ("name", "pick", fx["pick"]), "partners": ("item", "partner", fx["partner"]),
                "lockers": ("item", "locker", fx["locker"]), "bins": ("number", "bin", fx["bin"])}  # fmt: skip
        order = list(tabs)
        rng.shuffle(order)
        out = []
        for k in order:
            a, b, rows = tabs[k]
            out.append(f"Table {k}:\n| {a} | {b} |\n|---|---|\n" + "\n".join(f"| {x} | {y} |" for x, y in rows))
        return "\n\n".join(out)
    if fmt == "code":
        lines = [f"picks = {dict(fx['pick'])!r}", f"partners = {dict(fx['partner'])!r}",
                 f"lockers = {dict(fx['locker'])!r}", f"bins = {dict(fx['bin'])!r}"]  # fmt: skip
        lines += rng.sample(CODE_FILLER, min(n_filler, len(CODE_FILLER))) if n_filler else []
        rng.shuffle(lines)
        return "```python\n" + "\n".join(lines) + "\n```"
    raise ValueError(fmt)


PARAPHRASES = [("Which locker belongs to", "What is the locker number of"), ("What did", "Which item did"),
               ("Which bin holds things numbered", "What bin do things go in when they are numbered")]  # fmt: skip


def paraphrase(q: str, rng: random.Random) -> str:
    for a, b in PARAPHRASES:
        if q.startswith(a) and rng.random() < 0.5:
            return b + q[len(a) :]
    return q


def render(tok, item: dict) -> str:
    """The full prompt text for the item's question (or a step's, via item['_question']): one user turn, or for the
    chat format the facts in an earlier user turn; thinking off; 'Answer:' prefilled (as suite_v1)."""
    from bridge_jspace import chat

    q = item.get("_question", item["question"])
    if item["format"] != "chat":
        return S.render(tok, item["context"], q)
    msgs = [{"role": "user", "content": f"Here are my notes:\n{item['context']}"},
            {"role": "assistant", "content": "Got it."},
            {"role": "user", "content": f"{q} {S.INSTRUCTION}"}]  # fmt: skip
    return (
        tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False) + chat.PREFILL
    )


# ---- making items -------------------------------------------------------------------------------------------------
def make_item(rng: random.Random, word: str, domain: str, fmt: str, knobs: dict, idx: int) -> dict | None:
    dom = DOMAINS[domain]
    sc = scene(rng, dom, knobs["entities"], knobs["distractors"])
    c_op = rng.choice(C_OPS) if word[0] == "C" else None
    dom2 = None
    if len(word) == 3 and word[1:] in ("MM",):
        pool = [d for d in REVERSE_DOMAINS if d != domain]
        dom2 = DOMAINS[rng.choice(pool)] if pool else None
    ch = chain(word, dom, sc, rng, c_op, dom2)
    if ch is None:
        return None
    q = paraphrase(ch["question"], rng) if knobs["paraphrase"] else ch["question"]
    context = render_facts(fmt, dom, facts(word, dom, sc), rng, knobs["filler"])
    return {"id": f"{word}-{domain}-{fmt}-{idx:04d}", "word": word, "domain": domain, "format": fmt, "knobs": knobs,
            "c_op": c_op, "domain2": next((k for k, v in DOMAINS.items() if v is dom2), None), "context": context,
            "question": q, "answer": ch["answer"], "kind": ch["kind"], "steps": ch["steps"],
            "tier": dom.tier}  # fmt: skip


def examples(seed: int) -> None:
    rng = random.Random(seed)
    knobs = {"entities": 3, "distractors": False, "filler": 0, "paraphrase": False}
    for word in WORDS2 + WORDS3:
        for fmt in ("prose",):
            for _ in range(20):
                it = make_item(rng, word, rng.choice(list(DOMAINS)), fmt, knobs, 0)
                if it:
                    break
            print(
                f"=== {word} ({it['domain']}{', ' + it['c_op'] if it['c_op'] else ''}{', -> ' + it['domain2'] if it['domain2'] else ''})"
            )
            print("Q:", it["question"], "->", it["answer"])
            print("   steps:", " | ".join(f"{s['source']}: {s['question']} -> {s['answer']}" for s in it["steps"]))
    it = make_item(random.Random(seed), "PM", "planets", "prose", knobs, 0)
    for fmt in FORMATS:
        it2 = make_item(random.Random(seed), "PM", "planets", fmt, {**knobs, "filler": 5, "distractors": True}, 0)
        print(
            f"\n=== format {fmt} (PM, planets, filler 5, distractors)\n{it2['context'][:700]}\nQ: {it2['question']} -> {it2['answer']}"
        )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["examples"])
    ap.add_argument("--seed", type=int, default=701)
    args = ap.parse_args()
    examples(args.seed)
