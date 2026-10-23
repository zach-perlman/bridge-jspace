"""natplus (Zach, 2026-10-23, prereg amendment 14): natural_v1 widened, for Neel's two critiques (diversity; narrowly
used concepts may not use the shared direction).

Changes from natural_v1 (scripts/natural_v1.py, whose competence, vocabulary and first-name code this reuses):
  - popularity strata: every bridge type has its natural_v1 bridges ("popular") plus lesser-known ones ("rare");
    item["popularity"] records it, and every analysis can split by it;
  - a fourth relation, animal -> class (Mammal, Bird, Reptile, Amphibian, Fish, Insect), popular only;
  - three wordings for every fact sentence and question, one drawn per scene (bind, prompt fact and questions share
    the draw so the question matches its fact);
  - coherent passages: the facts are spliced, at random sentence boundaries, into a window of consecutive sentences
    of one real WikiText paragraph (natural_v1 shuffled single sentences from anywhere); windows may repeat across
    scenes (the filler is unrelated to every question);
  - chat framing only (natural_v1's cloze and QA framings failed for some models), read by the candidate-rank read
    (ablate_v2 --read cand, natural_v1.py competence --read cand).
Kept: the 2x2 per chain (same bridge in all four words), fictional people for P starts, P-final answers from the
same vocabulary and never the real one, no bridge in M->M passages, levels 0 (3 entities, 2 real sentences) and 1
(6 entities, 6 real sentences).

python scripts/natplus.py --name natplus_v1 --seed 901 --scenes 2
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
RARE_COUNTRIES = {
    "Bhutan": ("Asia", [("country", "measures its progress by Gross National Happiness")]),
    "Mongolia": ("Asia", [("country", "was the homeland of Genghis Khan")]),
    "Uzbekistan": ("Asia", [("country", "is home to the old Silk Road city of Samarkand")]),
    "Laos": ("Asia", [("country", "is home to the Plain of Jars")]),
    "Uruguay": ("South America", [("country", "won the first FIFA World Cup in 1930")]),
    "Bolivia": ("South America", [("country", "is home to the Uyuni salt flat")]),
    "Ecuador": ("South America", [("country", "owns the Galapagos Islands")]),
    "Paraguay": ("South America", [("country", "is home to the Jesuit mission ruins of Trinidad")]),
    "Botswana": ("Africa", [("country", "is home to the Okavango Delta")]),
    "Namibia": ("Africa", [("country", "is home to the red Sossusvlei dunes")]),
    "Madagascar": ("Africa", [("country", "is the island home of the lemurs")]),
    "Tanzania": ("Africa", [("country", "is home to Mount Kilimanjaro")]),
    "Iceland": ("Europe", [("country", "is home to the Blue Lagoon geothermal spa")]),
    "Finland": ("Europe", [("country", "is where the phone maker Nokia was founded")]),
    "Hungary": ("Europe", [("country", "is where the Rubik's Cube was invented")]),
    "Croatia": ("Europe", [("country", "is home to the walled city of Dubrovnik")]),
}
RARE_PEOPLE = {
    "Sibelius": ("Finnish", [("composer", "wrote the Valse triste")]),
    "Dvorak": ("Czech", [("composer", "wrote the New World Symphony")]),
    "Smetana": ("Czech", [("composer", "wrote The Moldau")]),
    "Bartok": ("Hungarian", [("composer", "wrote the Concerto for Orchestra")]),
    "Liszt": ("Hungarian", [("composer", "wrote the Liebestraum piano pieces")]),
    "Kierkegaard": ("Danish", [("philosopher", "wrote Fear and Trembling")]),
    "Andersen": ("Danish", [("writer", "wrote The Little Mermaid")]),
    "Strindberg": ("Swedish", [("playwright", "wrote Miss Julie")]),
    "Lorca": ("Spanish", [("poet", "wrote Blood Wedding")]),
    "Puccini": ("Italian", [("composer", "wrote the opera Tosca")]),
    "Pirandello": ("Italian", [("playwright", "wrote Six Characters in Search of an Author")]),
    "Schiller": ("German", [("poet", "wrote the poem Ode to Joy")]),
    "Klimt": ("Austrian", [("painter", "painted The Kiss")]),
    "Pushkin": ("Russian", [("poet", "wrote Eugene Onegin")]),
    "Mendeleev": ("Russian", [("chemist", "created the periodic table of the elements")]),
    "Zola": ("French", [("writer", "wrote the open letter J'Accuse")]),
    "Ravel": ("French", [("composer", "wrote Bolero")]),
    "Escher": ("Dutch", [("artist", "drew impossible staircases and endless tessellations")]),
}
RARE_CITIES = {
    "Gothenburg": ("Sweden", [("city", "is the home city of Volvo cars")]),
    "Bilbao": ("Spain", [("city", "is home to a Guggenheim museum designed by Frank Gehry")]),
    "Dresden": ("Germany", [("city", "rebuilt its Frauenkirche church after wartime bombing")]),
    "Turin": ("Italy", [("city", "keeps a famous burial shroud in its cathedral")]),
    "Nagoya": ("Japan", [("city", "is famous for a castle with golden dolphins on its roof")]),
    "Chengdu": ("China", [("city", "is famous for its giant panda breeding base")]),
    "Jaipur": ("India", [("city", "is known as the Pink City")]),
    "Adelaide": ("Australia", [("city", "was named after the queen consort of William IV")]),
    "Calgary": ("Canada", [("city", "holds the Stampede rodeo every July")]),
    "Salzburg": ("Austria", [("city", "is where The Sound of Music was filmed")]),
    "Bruges": ("Belgium", [("city", "is famous for its medieval canals and lace")]),
    "Cusco": ("Peru", [("city", "was the capital of the Inca Empire")]),
    "Medellin": ("Colombia", [("city", "is known as the City of Eternal Spring")]),
}
ANIMALS = {
    "beaver": ("Mammal", [("animal", "builds dams across rivers")]),
    "bat": ("Mammal", [("animal", "hunts at night by echolocation")]),
    "dolphin": ("Mammal", [("animal", "lives in the sea and talks in clicks and whistles")]),
    "penguin": ("Bird", [("animal", "cannot fly and lives in Antarctica")]),
    "ostrich": ("Bird", [("animal", "lays the largest eggs of any living animal")]),
    "owl": ("Bird", [("animal", "turns its head almost all the way around and hoots at night")]),
    "crocodile": ("Reptile", [("animal", "lies still in rivers waiting to snap at prey")]),
    "chameleon": ("Reptile", [("animal", "changes color to blend in")]),
    "tortoise": ("Reptile", [("animal", "carries its shell and can live over a hundred years")]),
    "frog": ("Amphibian", [("animal", "croaks and starts life as a tadpole")]),
    "salamander": ("Amphibian", [("animal", "can regrow its lost legs")]),
    "axolotl": ("Amphibian", [("animal", "keeps its feathery gills as an adult in Mexican lakes")]),
    "shark": ("Fish", [("animal", "has rows of replaceable teeth and can smell blood from far away")]),
    "salmon": ("Fish", [("animal", "swims upstream to spawn")]),
    "seahorse": ("Fish", [("animal", "has males that carry the babies")]),
    "bee": ("Insect", [("animal", "makes honey")]),
    "ant": ("Insect", [("animal", "lives in colonies and carries crumbs back to its nest")]),
    "butterfly": ("Insect", [("animal", "starts life as a caterpillar")]),
}
N.FIRST_NAMES.update({"Sibelius": "Jean", "Dvorak": "Antonin", "Smetana": "Bedrich", "Bartok": "Bela", "Liszt": "Franz",
                      "Kierkegaard": "Soren", "Andersen": "Hans", "Strindberg": "August", "Lorca": "Federico",
                      "Puccini": "Giacomo", "Pirandello": "Luigi", "Schiller": "Friedrich", "Klimt": "Gustav",
                      "Pushkin": "Alexander", "Mendeleev": "Dmitri", "Zola": "Emile", "Ravel": "Maurice",
                      "Escher": "Maurits"})  # fmt: skip
# three wordings each; one index per scene, shared by the bind, its description, the prompt fact and the questions
TYPES = {
    "countries": {"facts": {**{k: (*v, "popular") for k, v in N.COUNTRIES.items()}, **{k: (*v, "rare") for k, v in RARE_COUNTRIES.items()}},
        "bind": ["{p} grew up in {x}.", "{p} was raised in {x}.", "{p} spent a whole childhood in {x}."],
        "pdesc": ["the country where {p} grew up", "the country where {p} was raised", "the country of {p}'s childhood"],
        "pfact": ["The delegation from {x} will hold its next meeting in {a}.", "The delegation from {x} announced that its next meeting will take place in {a}.",
                  "Next year, the delegation from {x} meets in {a}."],
        "unknown": "an unnamed country",
        "q1P": ["In which country did {p} grow up?", "Which country was {p} raised in?", "Where did {p} spend their childhood?"],
        "q1M": ["Which {noun} {rel}?"] * 3,
        "q2M": ["On which continent is {d}?", "Which continent is {d} on?", "{D} is on which continent?"],
        "q2P": ["On which continent will the delegation from {d} hold its next meeting?", "Which continent will host the next meeting of the delegation from {d}?",
                "Where, by continent, will the delegation from {d} meet next?"]},
    "people": {"facts": {**{k: (*v, "popular") for k, v in N.PEOPLE.items()}, **{k: (*v, "rare") for k, v in RARE_PEOPLE.items()}},
        "bind": ["{p} wrote a doctoral thesis on {x}.", "{p}'s dissertation was about {x}.", "{p} spent five years writing a thesis on {x}."],
        "pdesc": ["the person {p} wrote a doctoral thesis on", "the subject of {p}'s dissertation", "the person {p}'s thesis was about"],
        "pfact": ["In the new film series, {x} is played by {an} {a} actor.", "The upcoming biopic casts {an} {a} actor as {x}.",
                  "{X} will be portrayed by {an} {a} actor in a new film."],
        "unknown": "an unnamed historical figure",
        "q1P": ["Who did {p} write a doctoral thesis on?", "Who was {p}'s dissertation about?", "Who was the subject of {p}'s thesis?"],
        "q1M": ["Which {noun} {rel}?"] * 3,
        "q2M": ["What was the nationality of {d}?", "Which nationality was {d}?", "{D} was of which nationality?"],
        "q2P": ["What is the nationality of the actor who plays {d} in the new film?", "Which nationality is the actor cast as {d} in the new film?",
                "The actor portraying {d} in the new film is of which nationality?"]},
    "cities": {"facts": {**{k: (*v, "popular") for k, v in N.CITIES.items()}, **{k: (*v, "rare") for k, v in RARE_CITIES.items()}},
        "bind": ["{p} moved to {x} last spring.", "Last spring, {p} relocated to {x}.", "{p} has lived in {x} since last spring."],
        "pdesc": ["the city {p} moved to last spring", "the city {p} relocated to last spring", "the city {p} has lived in since last spring"],
        "pfact": ["This year, {x} was paired with a partner city in {a}.", "This year, {x} signed a twinning agreement with a city in {a}.",
                  "This year's partner city for {x} is in {a}."],
        "unknown": "an unnamed city",
        "q1P": ["Which city did {p} move to last spring?", "Which city did {p} relocate to last spring?", "Which city has {p} lived in since last spring?"],
        "q1M": ["Which {noun} {rel}?"] * 3,
        "q2M": ["In which country is {d}?", "Which country is {d} in?", "{D} is in which country?"],
        "q2P": ["In which country is this year's partner city of {d}?", "Which country is this year's twin city of {d} in?",
                "This year's partner city of {d} is in which country?"]},
    "animals": {"facts": {k: (*v, "popular") for k, v in ANIMALS.items()},
        "bind": ["{p}'s favorite animal is the {x}.", "{p} adopted a {x} at the zoo's sponsorship scheme.", "{p} wrote a school report on the {x}."],
        "pdesc": ["{p}'s favorite animal", "the animal {p} adopted at the zoo", "the animal {p} wrote a school report on"],
        "pfact": ["At the new zoo, the {x} is kept in the {al} house.", "The new zoo put the {x} in its {al} house.", "Visitors to the new zoo find the {x} in the {al} house."],
        "unknown": "an unnamed animal",
        "q1P": ["What is {p}'s favorite animal?", "Which animal did {p} adopt at the zoo?", "Which animal did {p} write a school report on?"],
        "q1M": ["Which {noun} {rel}?"] * 3,
        "q2M": ["What class of animal is {d}?", "Which class of animal does {d} belong to?", "{D} belongs to which class of animal?"],
        "q2P": ["In which house of the new zoo is {d} kept?", "Which house of the new zoo holds {d}?", "{D} is kept in which house of the new zoo?"]},
}
PEOPLE_NAMES = [n if n != "Adam Pryce" else "Aaron Pryce" for n in N.PEOPLE_NAMES]  # Adam Mickiewicz is not used, kept apart anyway


def the(t: str, x: str) -> str:
    return f"the {x}" if t == "animals" else x


def real_paragraphs(banned: set[str]) -> list[list[str]]:
    """Real WikiText paragraphs as lists of consecutive clean sentences naming no bridge, answer or fictional person."""
    out = []
    for row in pins.wikitext_rows():
        sents = []
        for s in re.split(r"(?<=[.!?])\s+", row.strip()):
            for a, b in ((" , ", ", "), (" .", "."), (" 's", "'s"), (" ( ", " ("), (" )", ")"), (" : ", ": "), (" ; ", "; "), (" '", "'"), (' " ', ' "')):
                s = s.replace(a, b)
            ok = (8 <= len(s.split()) <= 30 and s[0].isupper() and "@" not in s and "=" not in s and not s.endswith((":", ";"))
                  and s.count('"') % 2 == 0 and not any(re.search(r"\b" + re.escape(w) + r"\b", s, re.I) for w in banned))  # fmt: skip
            if not ok:  # a run of consecutive clean sentences ends here
                if len(sents) >= 2:
                    out.append(sents)
                sents = []
                continue
            sents.append(s)
        if len(sents) >= 2:
            out.append(sents)
    return out


def passage(rng: random.Random, genre: str, facts: list[str], para: list[str]) -> str:
    """The real sentences in order with the facts spliced in at random sentence boundaries (facts keep no fixed place)."""
    slots = sorted(rng.choices(range(len(para) + 1), k=len(facts)))
    facts = facts[:]
    rng.shuffle(facts)
    body, fi = [], 0
    for i in range(len(para) + 1):
        while fi < len(facts) and slots[fi] == i:
            body.append(facts[fi])
            fi += 1
        if i < len(para):
            body.append(para[i])
    head, tail = N.GENRES[genre]
    if genre == "notes":
        return head + "\n" + "\n".join("- " + s for s in body) + "\n" + tail
    return head + "\n" + " ".join(body) + "\n" + tail


def make(name: str, seed: int, n_scenes: int) -> None:
    from transformers import AutoTokenizer

    tokenizers = {n: AutoTokenizer.from_pretrained(pins.TARGETS[n]["repo"], revision=pins.TARGETS[n]["revision"])
                  for n in N.TOKENIZERS}  # fmt: skip
    for tname, t in TYPES.items():  # answers: distinct first tokens (both readings) in every tokenizer
        vocab = sorted({v[0] for v in t["facts"].values()})
        for tn, tok in tokenizers.items():
            ft = N.first_tokens(tok, vocab)
            for k in (0, 1):
                c = collections.Counter(v[k] for v in ft.values())
                clash = [w for w, v in ft.items() if c[v[k]] > 1]
                assert not clash, f"{tname} answers share a first token ({tn}, reading {k}): {clash}"
    rng = random.Random(seed)
    banned = {b for t in TYPES.values() for b in t["facts"]} | {v[0] for t in TYPES.values() for v in t["facts"].values()}
    banned |= {w for n in PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()} | {"Olympic", "Olympics", "continent", "zoo"}
    paras = real_paragraphs(banned)
    rng.shuffle(paras)
    items, k = [], 0
    for tname, t in TYPES.items():
        facts = t["facts"]
        vocab = sorted({v[0] for v in facts.values()})
        for level, knobs in N.LEVELS.items():
            for x in sorted(facts):
                for rep in range(n_scenes):
                    for group in ("P", "M"):
                        k += 1
                        w = rng.randrange(3)  # the wording of this scene
                        scene = f"np:{tname}:{group}-L{level}-{x}-{rep}"
                        real = facts[x][0]
                        others = sorted(set(facts) - {x})
                        rng.shuffle(others)
                        others.sort(key=lambda o: facts[o][0] == real)
                        ents = [x] + others[: knobs["entities"] - 1]
                        persons = rng.sample(PEOPLE_NAMES, len(ents))
                        pfinal = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}
                        binds = [t["bind"][w].format(p=p, x=e) for p, e in zip(persons, ents, strict=True)]
                        pfacts = [t["pfact"][w].format(x=e, X=e[0].upper() + e[1:], a=pfinal[e], al=pfinal[e].lower(), an=N.an(pfinal[e]))
                                  for e in ents]  # fmt: skip
                        genre = rng.choice(sorted(N.GENRES))
                        runs = [p for p in paras if len(p) >= knobs["filler"]]  # filler may repeat across scenes
                        run = rng.choice(runs)
                        st = rng.randrange(len(run) - knobs["filler"] + 1)
                        para = run[st : st + knobs["filler"]]
                        order_seed = rng.random()
                        full = passage(random.Random(order_seed), genre, binds + pfacts, para)
                        noun, rel = rng.choice(facts[x][1])
                        if group == "P":
                            d1, start = t["pdesc"][w].format(p=persons[0]), "P"
                            q1 = t["q1P"][w].format(p=persons[0])
                            guess_d = t["pdesc"][w].format(p=rng.choice(N.ABSENT_NAMES))
                        else:
                            d1, start = f"the {noun} {'who' if tname == 'people' else 'that'} {rel}", "M"
                            q1 = t["q1M"][w].format(noun=noun, rel=rel)
                            guess_d = t["unknown"]
                        for word in (("PP", "PM") if group == "P" else ("MP", "MM")):
                            fin = word[1]
                            ans = real if fin == "M" else pfinal[x]
                            ctx = full
                            if word == "MM":
                                keep = [s for s in binds + pfacts if not re.search(r"\b" + re.escape(x) + r"\b", s, re.I)]
                                ctx = passage(random.Random(order_seed), genre, keep, para)
                            q2 = t["q2" + fin][w]
                            cap = lambda s: s[0].upper() + s[1:]  # noqa: E731
                            whole = q2.format(d=d1, D=cap(d1))
                            step2 = q2.format(d=the(tname, x), D=cap(the(tname, x)))
                            guess = q2.format(d=guess_d, D=cap(guess_d))
                            same = [e for e in ents[1:] if (facts[e][0] if fin == "M" else pfinal[e]) == ans]
                            bridge_ans = x[0].upper() + x[1:] if tname == "animals" else x  # chat answers start capitalised
                            items.append({
                                "id": f"np:chat:{word}-L{level}-{k:04d}", "word": word, "domain": tname, "format": "prose",
                                "genre": genre, "framing": "chat", "wording": w, "popularity": facts[x][2], "context": ctx,
                                "question": whole, "answer": ans, "kind": "open", "answer_kind": "open",
                                "steps": [{"question": q1, "answer": bridge_ans, "kind": "open", "source": start,
                                           "alts": sorted({bridge_ans, N.FIRST_NAMES.get(x, bridge_ans)})},
                                          {"question": step2, "answer": ans, "kind": "open", "source": fin}],
                                "bridge": bridge_ans, "bridges": [bridge_ans], "start_desc": d1, "guess_question": guess,
                                "scene": scene, "level": level, "knobs": knobs, "numbers": "words", "c_op": None,
                                "chance_same_answer": round(len(same) / max(1, len(ents) - 1), 3),
                                "entities": ents, "real": real, "prompt_answer": pfinal[x],
                            })  # fmt: skip
    out = DATA / f"{name}_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"set": out.name, "seed": seed, "scenes_per_bridge": n_scenes, "n": len(items),
                                                   "git_commit": commit, "script": "scripts/natplus.py",
                                                   "by_type_popularity": collections.Counter(f"{it['domain']}/{it['popularity']}" for it in items)},
                                                  indent=2) + "\n")  # fmt: skip
    print(f"{out.name}: {len(items)} items", dict(collections.Counter((it["domain"], it["popularity"]) for it in items)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=901)
    ap.add_argument("--scenes", type=int, default=2)
    a = ap.parse_args()
    make(a.name, a.seed, a.scenes)
