"""natural3 (Zach, 2026-10-23, prereg amendment 15): three-step natural chains, every P/M combination.

Two chain types, start entities balanced across continents (an all-European start set would make every memory-final
answer "Europe"):
  cities:  city -> its country -> that country's continent     Barcelona -> Spain -> Europe
  people:  person -> home country -> that country's continent    Mozart -> Austria -> Europe
Hop sources:
  hop 1  P: a fictional person moved to the city / wrote a thesis on the person;  M: an indirect real description
  hop 2  M: the real country;  P: a new fact in the passage, never the real one (the city's partner city this year is
         in country Y; the person is played by an actor from country Y in a new film)
  hop 3  M: the country's real continent;  P: the country's delegation meets next on continent Z (never the real one)
All 8 words (PPP ... MMM). The answer is always a continent (5 values; first tokens distinct).
Passages (as natplus: genre wrapper, facts spliced into a window of consecutive real WikiText sentences) carry only the
relations the word reads, for the chain's entities and the scene's distractor chains: bindings for P hop 1, partner /
actor facts for P hop 2, delegation facts for P hop 3. The start entity appears only if hop 1 or hop 2 is P; the
middle country only if hop 2 or hop 3 is P (an entity a memory hop must recall is never in the prompt unless a later
prompt hop is keyed by it, which is the toy suite's structure too).
Validity (as tasks_v2.wrong_routes): the answer differs from every route that swaps hop 2 or hop 3 to the other
source where that fact exists, and from skipping hop 2 (the start city's / person's own continent); the prompt facts
are redrawn until this holds, else the item is dropped. chance_same_answer = share of the scene's distractor chains
whose same route gives the same answer.
Skip-prone words: adjacent memory hops can be one memorized composite (city -> continent, description -> country):
PMM, MMM, MMP. The clean words are PPP, MPP, PMP, PPM, MPM.
Items carry per-step candidate vocabularies (cand_vocab) and the whole question's (answer_vocab) for the
candidate-rank read; per-word eligibility (ablate_v2 --tasks-per-word).

python scripts/natural3.py --name nat3_v1 --seed 1101 --scenes 2
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import natplus as NP  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
CONT = {  # country -> continent (every middle country, real or drawn for a prompt fact)
    "Spain": "Europe", "Italy": "Europe", "Germany": "Europe", "France": "Europe", "Poland": "Europe", "Portugal": "Europe",
    "Sweden": "Europe", "Belgium": "Europe", "Austria": "Europe", "Norway": "Europe",
    "Japan": "Asia", "China": "Asia", "India": "Asia", "Iran": "Asia",
    "Brazil": "South America", "Peru": "South America", "Colombia": "South America", "Chile": "South America",
    "Argentina": "South America", "Venezuela": "South America",
    "Canada": "North America", "Mexico": "North America",
    "Morocco": "Africa", "Mali": "Africa", "Egypt": "Africa", "Kenya": "Africa", "South Africa": "Africa", "Nigeria": "Africa",
}  # fmt: skip
CONTINENTS = sorted(set(CONT.values()))
CITIES = {  # city -> (country, [(noun, relative clause)])
    "Barcelona": ("Spain", [("city", "is home to the Sagrada Familia")]),
    "Milan": ("Italy", [("city", "is home to the La Scala opera house")]),
    "Munich": ("Germany", [("city", "hosts the Oktoberfest")]),
    "Lyon": ("France", [("city", "is where the Lumiere brothers made the first films")]),
    "Krakow": ("Poland", [("city", "is home to Wawel Castle")]),
    "Porto": ("Portugal", [("city", "lies on the Douro river and is famous for its wine cellars")]),
    "Gothenburg": ("Sweden", [("city", "is the home city of Volvo cars")]),
    "Bruges": ("Belgium", [("city", "is famous for its medieval canals and lace")]),
    "Osaka": ("Japan", [("city", "hosted the 1970 World Expo")]),
    "Kyoto": ("Japan", [("city", "is famous for the Golden Pavilion temple")]),
    "Nagoya": ("Japan", [("city", "is famous for a castle with golden dolphins on its roof")]),
    "Shanghai": ("China", [("city", "has a waterfront promenade called the Bund")]),
    "Chengdu": ("China", [("city", "is famous for its giant panda breeding base")]),
    "Mumbai": ("India", [("city", "is the center of the Bollywood film industry")]),
    "Jaipur": ("India", [("city", "is known as the Pink City")]),
    "Rio": ("Brazil", [("city", "is overlooked by the Christ the Redeemer statue")]),
    "Cusco": ("Peru", [("city", "was the capital of the Inca Empire")]),
    "Medellin": ("Colombia", [("city", "is known as the City of Eternal Spring")]),
    "Valparaiso": ("Chile", [("city", "is a port famous for its colorful hillside houses and funiculars")]),
    "Mendoza": ("Argentina", [("city", "is the heart of Malbec wine country at the foot of the Andes")]),
    "Toronto": ("Canada", [("city", "is home to the CN Tower")]),
    "Vancouver": ("Canada", [("city", "hosted the 2010 Winter Olympics")]),
    "Calgary": ("Canada", [("city", "holds the Stampede rodeo every July")]),
    "Guadalajara": ("Mexico", [("city", "is the birthplace of mariachi music")]),
    "Monterrey": ("Mexico", [("city", "is overlooked by the Saddle Mountain, Cerro de la Silla")]),
    "Casablanca": ("Morocco", [("city", "is home to the Hassan II Mosque")]),
    "Timbuktu": ("Mali", [("city", "is famous for its ancient manuscripts and mud mosques")]),
    "Alexandria": ("Egypt", [("city", "was home to the ancient Pharos lighthouse")]),
    "Mombasa": ("Kenya", [("city", "is the old Swahili port city with Fort Jesus")]),
    "Cape Town": ("South Africa", [("city", "lies beneath Table Mountain")]),
}
PEOPLE = {  # person -> (home country, [(noun, relative clause)])
    "Picasso": ("Spain", [("artist", "painted Guernica")]),
    "Mozart": ("Austria", [("composer", "wrote The Magic Flute")]),
    "Beethoven": ("Germany", [("composer", "wrote the Moonlight Sonata")]),
    "Galileo": ("Italy", [("astronomer", "discovered the four largest moons of Jupiter")]),
    "Hugo": ("France", [("writer", "wrote Les Miserables")]),
    "Chopin": ("Poland", [("composer", "wrote the Minute Waltz")]),
    "Nobel": ("Sweden", [("chemist", "invented dynamite")]),
    "Ibsen": ("Norway", [("playwright", "wrote A Doll's House")]),
    "Gandhi": ("India", [("leader", "led the Salt March against British rule")]),
    "Tagore": ("India", [("poet", "wrote Gitanjali")]),
    "Confucius": ("China", [("philosopher", "is quoted throughout the Analects")]),
    "Hokusai": ("Japan", [("artist", "made the woodblock print The Great Wave")]),
    "Kurosawa": ("Japan", [("director", "made the film Seven Samurai")]),
    "Khayyam": ("Iran", [("poet", "wrote the Rubaiyat")]),
    "Mandela": ("South Africa", [("leader", "spent 27 years imprisoned on Robben Island")]),
    "Tutu": ("South Africa", [("archbishop", "chaired the Truth and Reconciliation Commission")]),
    "Achebe": ("Nigeria", [("writer", "wrote Things Fall Apart")]),
    "Mahfouz": ("Egypt", [("writer", "won the 1988 Nobel Prize in Literature for his Arabic novels")]),
    "Kahlo": ("Mexico", [("painter", "painted The Two Fridas")]),
    "Cohen": ("Canada", [("songwriter", "wrote the song Hallelujah")]),
    "Gretzky": ("Canada", [("hockey player", "is known as The Great One")]),
    "Borges": ("Argentina", [("writer", "wrote the story collection Ficciones")]),
    "Neruda": ("Chile", [("poet", "wrote Twenty Love Poems and a Song of Despair")]),
    "Pele": ("Brazil", [("footballer", "won three World Cups as a player")]),
    "Bolivar": ("Venezuela", [("general", "is called El Libertador")]),
    "Marquez": ("Colombia", [("novelist", "wrote One Hundred Years of Solitude")]),
}
FIRST = {**N.FIRST_NAMES, "Gandhi": "Mahatma", "Tagore": "Rabindranath", "Confucius": "Confucius", "Hokusai": "Katsushika",
         "Kurosawa": "Akira", "Khayyam": "Omar", "Mandela": "Nelson", "Tutu": "Desmond", "Achebe": "Chinua",
         "Mahfouz": "Naguib", "Kahlo": "Frida", "Cohen": "Leonard", "Gretzky": "Wayne", "Borges": "Jorge",
         "Neruda": "Pablo", "Pele": "Pele", "Bolivar": "Simon", "Marquez": "Gabriel"}  # fmt: skip
TYPES = {
    "cities": {"starts": CITIES,
        "bind": ["{p} moved to {x} last spring.", "Last spring, {p} relocated to {x}."],
        "d0P": ["the city {p} moved to last spring", "the city {p} relocated to last spring"],
        "q1P": ["Which city did {p} move to last spring?", "Which city did {p} relocate to last spring?"],
        "p2": ["This year, {x} was paired with a partner city in {y}.", "This year, {x} signed a twinning agreement with a city in {y}."],
        "d1M": ["the country that contains {d}", "the country containing {d}"],
        "d1P": ["the country of this year's partner city of {d}", "the country of the city twinned this year with {d}"],
        "q2M": ["Which country contains {x}?", "Which country is {x} in?"],
        "q2P": ["Which country is this year's partner city of {x} in?", "In which country is the city twinned with {x} this year?"]},
    "people": {"starts": PEOPLE,
        "bind": ["{p} wrote a doctoral thesis on {x}.", "{p}'s dissertation was about {x}."],
        "d0P": ["the person {p} wrote a doctoral thesis on", "the subject of {p}'s dissertation"],
        "q1P": ["Who did {p} write a doctoral thesis on?", "Who was {p}'s dissertation about?"],
        "p2": ["In the new film series, {x} is played by an actor from {y}.", "The upcoming biopic casts an actor from {y} as {x}."],
        "d1M": ["the home country of {d}", "the country of origin of {d}"],
        "d1P": ["the home country of the actor who plays {d} in the new film", "the country of the actor cast as {d} in the new film"],
        "q2M": ["What is the home country of {x}?", "Which country did {x} come from?"],
        "q2P": ["Which country is the actor who plays {x} in the new film from?", "Where is the actor cast as {x} in the new film from?"]},
}
P3 = ["The delegation from {y} will hold its next meeting in {z}.", "Next year, the delegation from {y} meets in {z}."]
Q3M = ["On which continent is {d}?", "On which continent does {d} lie?"]
Q3P = ["On which continent will the delegation from {d} hold its next meeting?", "Which continent will host the next meeting of the delegation from {d}?"]
WORDS = ["".join(w) for w in itertools.product("PM", repeat=3)]
CLEAN = ("PPP", "MPP", "PMP", "PPM", "MPM")


def chain_answer(word: str, x: str, starts: dict, p2: dict, p3: dict) -> str | None:
    """The continent a word's route reaches from start x, with prompt facts p2 (start -> country), p3 (country ->
    continent); None if a needed prompt fact is missing."""
    y = starts[x][0] if word[1] == "M" else p2.get(x)
    if y is None:
        return None
    return CONT[y] if word[2] == "M" else p3.get(y)


def make(name: str, seed: int, n_scenes: int) -> None:
    from transformers import AutoTokenizer

    tokenizers = {n: AutoTokenizer.from_pretrained(pins.TARGETS[n]["repo"], revision=pins.TARGETS[n]["revision"])
                  for n in N.TOKENIZERS}  # fmt: skip
    for label, vocab in (("continents", CONTINENTS), ("countries", sorted(CONT))):
        for tn, tok in tokenizers.items():
            ft = N.first_tokens(tok, vocab)
            for k in (0, 1):
                c = collections.Counter(v[k] for v in ft.values())
                clash = [w for w, v in ft.items() if c[v[k]] > 1]
                assert not clash, f"{label} share a first token ({tn}, reading {k}): {clash}"
    rng = random.Random(seed)
    banned = set(CONT) | set(CONTINENTS) | set(CITIES) | set(PEOPLE) | {"continent", "delegation"}
    banned |= {w for n in NP.PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()}
    paras = [[re.sub(r"(\d) ?: ?(\d)", r"\1:\2", s_) for s_ in run] for run in NP.real_paragraphs(banned)]
    items, k, dropped = [], 0, collections.Counter()
    for tname, t in TYPES.items():
        starts = t["starts"]
        start_vocab = sorted({s for s in starts} | {FIRST.get(s, s) for s in starts})
        for level, knobs in N.LEVELS.items():
            for x in sorted(starts):
                for rep in range(n_scenes):
                    for word in WORDS:
                        k += 1
                        w = rng.randrange(2)
                        real_y = starts[x][0]
                        # the scene: x and k-1 distractor starts, real countries on other continents first
                        others = sorted(set(starts) - {x})
                        rng.shuffle(others)
                        others.sort(key=lambda o: CONT[starts[o][0]] == CONT[real_y])
                        ents = [x] + others[: knobs["entities"] - 1]
                        persons = rng.sample(NP.PEOPLE_NAMES, len(ents))
                        for _ in range(200):  # draw prompt facts until the word's answer is unique among the routes
                            p2, p3 = {}, {}
                            if word[1] == "P":
                                p2[x] = rng.choice([c for c in CONT if c != real_y])
                                for e in ents[1:]:  # distractors: other countries, other continents where hop 3 recalls
                                    pool = [c for c in CONT if c != starts[e][0] and c != p2[x]]
                                    pref = [c for c in pool if word[2] == "P" or CONT[c] != CONT[p2[x]]]
                                    p2[e] = rng.choice(pref or pool)
                            x_mid = real_y if word[1] == "M" else p2[x]
                            if word[2] == "P":
                                p3[x_mid] = rng.choice([z for z in CONTINENTS if z != CONT[x_mid]])
                                for e in ents[1:]:
                                    e_mid = starts[e][0] if word[1] == "M" else p2[e]
                                    if e_mid not in p3:
                                        p3[e_mid] = rng.choice([z for z in CONTINENTS if z not in (CONT[e_mid], p3[x_mid])])
                            ans = chain_answer(word, x, starts, p2, p3)
                            routes = [chain_answer(word[0] + a + b, x, starts, p2, p3)  # hop 2 / hop 3 at the other source
                                      for a in "PM" for b in "PM" if word[0] + a + b != word]  # fmt: skip
                            if word[1:] != "MM":
                                routes.append(CONT[real_y])  # hop 2 skipped: the start's own continent
                            if ans not in [r for r in routes if r is not None]:
                                break
                        else:
                            dropped[word] += 1
                            continue
                        y_mid = real_y if word[1] == "M" else p2[x]
                        facts = []
                        if word[0] == "P":
                            facts += [t["bind"][w].format(p=p, x=e) for p, e in zip(persons, ents, strict=True)]
                        else:  # distractor bindings only: the start is never bound when hop 1 is a memory hop
                            facts += [t["bind"][w].format(p=p, x=e) for p, e in zip(persons[1:], ents[1:], strict=True)]
                        if word[1] == "P":
                            facts += [t["p2"][w].format(x=e, y=p2[e]) for e in ents]
                        if word[2] == "P":
                            facts += [P3[w].format(y=y, z=p3[y]) for y in sorted(p3)]
                        # the start appears only if hop 1 or 2 is a prompt hop; the middle country only if hop 2 or 3 is
                        if word[:2] == "MM":
                            facts = [f for f in facts if not re.search(r"\b" + re.escape(x) + r"\b", f)]
                        if word[1:] == "MM":
                            facts = [f for f in facts if not re.search(r"\b" + re.escape(y_mid) + r"\b", f)]
                        genre = rng.choice(sorted(N.GENRES))
                        run_ = rng.choice([p for p in paras if len(p) >= knobs["filler"]])
                        st = rng.randrange(len(run_) - knobs["filler"] + 1)
                        ctx = NP.passage(random.Random(rng.random()), genre, facts, run_[st : st + knobs["filler"]])
                        noun, rel = rng.choice(starts[x][1])
                        d0 = t["d0P"][w].format(p=persons[0]) if word[0] == "P" else f"the {noun} {'that' if tname == 'cities' else 'who'} {rel}"
                        d1 = t["d1" + word[1]][w].format(d=d0)
                        q = (Q3M if word[2] == "M" else Q3P)[w].format(d=d1)
                        q1 = t["q1P"][w].format(p=persons[0]) if word[0] == "P" else f"Which {noun} {rel}?"
                        q2 = t["q2" + word[1]][w].format(x=x)
                        q3 = (Q3M if word[2] == "M" else Q3P)[w].format(d=y_mid)
                        same = [e for e in ents[1:] if chain_answer(word, e, starts, p2, p3) == ans]
                        items.append({
                            "id": f"n3:chat:{word}-L{level}-{k:05d}", "word": word, "domain": tname, "format": "prose",
                            "genre": genre, "framing": "chat", "wording": w, "clean_word": word in CLEAN, "context": ctx,
                            "question": q, "answer": ans, "kind": "open", "answer_kind": "open", "answer_vocab": CONTINENTS,
                            "steps": [{"question": q1, "answer": x, "kind": "open", "source": word[0], "alts": sorted({x, FIRST.get(x, x)}),
                                       "cand_vocab": start_vocab},
                                      {"question": q2, "answer": y_mid, "kind": "open", "source": word[1], "cand_vocab": sorted(CONT)},
                                      {"question": q3, "answer": ans, "kind": "open", "source": word[2], "cand_vocab": CONTINENTS}],
                            "bridge": x, "bridges": [x, y_mid], "start_desc": d0,
                            "guess_question": (Q3M if word[2] == "M" else Q3P)[w].format(d="an unnamed country"),
                            "scene": f"n3:{tname}:{word}-L{level}-{x}-{rep}", "level": level, "knobs": knobs, "numbers": "words",
                            "c_op": None, "chance_same_answer": round(len(same) / max(1, len(ents) - 1), 3),
                            "entities": ents, "real_country": real_y, "middle": y_mid,
                        })  # fmt: skip
    out = DATA / f"{name}_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"set": out.name, "seed": seed, "scenes_per_start": n_scenes, "n": len(items),
                                                   "dropped_no_unique_route": dropped, "git_commit": commit,
                                                   "script": "scripts/natural3.py"}, indent=2) + "\n")  # fmt: skip
    print(f"{out.name}: {len(items)} items; dropped {dict(dropped)}", dict(collections.Counter((it["domain"], it["word"]) for it in items)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=1101)
    ap.add_argument("--scenes", type=int, default=2)
    a = ap.parse_args()
    make(a.name, a.seed, a.scenes)
