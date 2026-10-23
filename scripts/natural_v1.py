"""natural_v1 (Zach, 2026-10-23, prereg amendment 10B): a natural-text pilot of the memory-vs-prompt split.

Hand-built two-hop chains for three bridge types. Hop 2 is a many-to-one property, never a name alias of the bridge
(Neel's replication: capital/country swaps were dominated by answer swaps), and hop-1 descriptions never name the
hop-2 answer:
  countries -> continent      "the country that hosted the 2016 Summer Olympics" -> Brazil -> South America
  people    -> nationality    "the composer who wrote The Magic Flute" -> Mozart -> Austrian
  cities    -> country        "the city that is home to the Sagrada Familia" -> Barcelona -> Spain
Per chain the same bridge in all four words. P start: a new fact about a fictional person in the passage ("Laura
Bennett grew up in Brazil."). M start: an indirect real description. M final: the real property. P final: a new fact in
the passage with an answer from the same vocabulary, never the real one ("The delegation from Brazil will hold its
next meeting in Asia."). P->P and P->M read one passage (as tasks_v2); M->P and M->M share a scene, but the M->M
passage leaves out every sentence naming the bridge (in tasks_v2 the bridge is always in the prompt). Passages are
templated genres (news, email, forum, notes) with real WikiText sentences as filler; level 0 has 3 entities and 2
filler sentences, level 1 has 6 and 6. Items are written in tasks_v2's format to two sets, one per framing:
  NAME_cloze: raw text (no chat template), the passage then a sentence stopping before the answer; the read is the
               answer's first token with its leading space (kind "word").
  NAME_chat:  the passage and question in one user turn, thinking off, no "Answer:" prefill; the read is the answer's
               first token as the model would start its message (kind "open").
Every answer's first token (both readings) is distinct within its vocabulary for every target tokenizer checked.

python scripts/natural_v1.py make --name natural_v1 --seed 801 --scenes 2
python scripts/natural_v1.py competence --set natural_v1_cloze --name RUN --why W     (first-token read; tasks_v2 rows)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
TOKENIZERS = ["qwen3.6-27b", "qwen3.5-9b", "muse-glimmer-30b", "qwen3.5-122b-a10b"]

# ---- facts (hand-built; each model's single-hop answers filter out anything it disagrees with) ---------------------
# bridge: (property, [(noun, relative clause), ...])
COUNTRIES = {
    "Brazil": ("South America", [("country", "hosted the 2016 Summer Olympics"), ("country", "won the 2002 FIFA World Cup")]),
    "Argentina": ("South America", [("country", "is the birthplace of the tango"), ("country", "won the 1986 FIFA World Cup")]),
    "Peru": ("South America", [("country", "is home to Machu Picchu")]),
    "Chile": ("South America", [("country", "is home to the Atacama Desert"), ("country", "was the homeland of the poet Pablo Neruda")]),
    "Colombia": ("South America", [("country", "was the homeland of the novelist Gabriel Garcia Marquez")]),
    "Venezuela": ("South America", [("country", "is home to Angel Falls")]),
    "Mexico": ("North America", [("country", "is home to the ancient city of Teotihuacan"), ("country", "hosted the 1968 Summer Olympics")]),
    "Canada": ("North America", [("country", "has a red maple leaf on its flag"), ("country", "hosted the 2010 Winter Olympics")]),
    "Egypt": ("Africa", [("country", "is home to the pyramids of Giza")]),
    "Kenya": ("Africa", [("country", "is home to the Maasai Mara reserve")]),
    "Nigeria": ("Africa", [("country", "has a film industry known as Nollywood")]),
    "Morocco": ("Africa", [("country", "is home to the city of Marrakesh")]),
    "Ethiopia": ("Africa", [("country", "is where the fossil skeleton Lucy was found")]),
    "Ghana": ("Africa", [("country", "is famous for kente cloth and the Ashanti kingdom")]),
    "Japan": ("Asia", [("country", "is home to Mount Fuji"), ("country", "hosted the 2020 Summer Olympics")]),
    "India": ("Asia", [("country", "is home to the Taj Mahal")]),
    "China": ("Asia", [("country", "built the Great Wall")]),
    "Thailand": ("Asia", [("country", "was formerly known as Siam")]),
    "Vietnam": ("Asia", [("country", "is home to Ha Long Bay")]),
    "Nepal": ("Asia", [("country", "is home to Lumbini, the birthplace of the Buddha")]),
    "Iran": ("Asia", [("country", "was formerly known as Persia")]),
    "France": ("Europe", [("country", "is home to the Eiffel Tower")]),
    "Italy": ("Europe", [("country", "is home to the Colosseum")]),
    "Spain": ("Europe", [("country", "is home to the Alhambra")]),
    "Greece": ("Europe", [("country", "hosted the first modern Olympic Games in 1896")]),
    "Norway": ("Europe", [("country", "is famous for its fjords and its Viking ships")]),
    "Poland": ("Europe", [("country", "was the homeland of Pope John Paul II")]),
    "Sweden": ("Europe", [("country", "is where IKEA was founded")]),
    "Ireland": ("Europe", [("country", "is where Guinness stout was first brewed")]),
    "Portugal": ("Europe", [("country", "was the homeland of the explorer Vasco da Gama")]),
}
PEOPLE = {
    "Picasso": ("Spanish", [("artist", "painted Guernica")]),
    "Cervantes": ("Spanish", [("writer", "wrote Don Quixote")]),
    "Mozart": ("Austrian", [("composer", "wrote The Magic Flute")]),
    "Freud": ("Austrian", [("doctor", "founded psychoanalysis")]),
    "Beethoven": ("German", [("composer", "wrote the Moonlight Sonata")]),
    "Goethe": ("German", [("writer", "wrote Faust")]),
    "Bach": ("German", [("composer", "wrote the Brandenburg Concertos")]),
    "Kant": ("German", [("philosopher", "wrote the Critique of Pure Reason")]),
    "Tolstoy": ("Russian", [("writer", "wrote War and Peace")]),
    "Dostoevsky": ("Russian", [("writer", "wrote Crime and Punishment")]),
    "Tchaikovsky": ("Russian", [("composer", "wrote Swan Lake")]),
    "Chekhov": ("Russian", [("playwright", "wrote The Cherry Orchard")]),
    "Galileo": ("Italian", [("astronomer", "discovered the four largest moons of Jupiter")]),
    "Dante": ("Italian", [("poet", "wrote the Divine Comedy")]),
    "Vivaldi": ("Italian", [("composer", "wrote The Four Seasons")]),
    "Michelangelo": ("Italian", [("artist", "painted the ceiling of the Sistine Chapel")]),
    "Verdi": ("Italian", [("composer", "wrote the opera Aida")]),
    "Hugo": ("French", [("writer", "wrote Les Miserables")]),
    "Monet": ("French", [("painter", "painted the Water Lilies series")]),
    "Descartes": ("French", [("philosopher", "wrote 'I think, therefore I am'")]),
    "Napoleon": ("French", [("emperor", "lost the Battle of Waterloo")]),
    "Rembrandt": ("Dutch", [("painter", "painted The Night Watch")]),
    "Vermeer": ("Dutch", [("painter", "painted Girl with a Pearl Earring")]),
    "Chopin": ("Polish", [("composer", "wrote the Minute Waltz")]),
    "Copernicus": ("Polish", [("astronomer", "proposed that the Earth moves around the Sun")]),
    "Nobel": ("Swedish", [("chemist", "invented dynamite")]),
    "Linnaeus": ("Swedish", [("botanist", "created the modern system for naming species")]),
    "Ibsen": ("Norwegian", [("playwright", "wrote A Doll's House")]),
    "Grieg": ("Norwegian", [("composer", "wrote In the Hall of the Mountain King")]),
}
CITIES = {
    "Barcelona": ("Spain", [("city", "is home to the Sagrada Familia")]),
    "Seville": ("Spain", [("city", "is famous for the Giralda tower")]),
    "Milan": ("Italy", [("city", "is home to the La Scala opera house")]),
    "Venice": ("Italy", [("city", "is famous for its canals and gondolas")]),
    "Florence": ("Italy", [("city", "is home to the Uffizi Gallery")]),
    "Naples": ("Italy", [("city", "lies at the foot of Mount Vesuvius")]),
    "Munich": ("Germany", [("city", "hosts the Oktoberfest")]),
    "Hamburg": ("Germany", [("city", "is home to the Elbphilharmonie concert hall")]),
    "Lyon": ("France", [("city", "is where the Lumiere brothers made the first films")]),
    "Osaka": ("Japan", [("city", "hosted the 1970 World Expo")]),
    "Kyoto": ("Japan", [("city", "is famous for the Golden Pavilion temple")]),
    "Shanghai": ("China", [("city", "has a waterfront promenade called the Bund")]),
    "Mumbai": ("India", [("city", "is the center of the Bollywood film industry")]),
    "Sydney": ("Australia", [("city", "is famous for its opera house with sail-shaped roofs")]),
    "Toronto": ("Canada", [("city", "is home to the CN Tower")]),
    "Vancouver": ("Canada", [("city", "hosted the 2010 Winter Olympics")]),
    "Istanbul": ("Turkey", [("city", "is home to the Hagia Sophia")]),
    "Casablanca": ("Morocco", [("city", "is home to the Hassan II Mosque")]),
    "Krakow": ("Poland", [("city", "is home to Wawel Castle")]),
    "Porto": ("Portugal", [("city", "lies on the Douro river and is famous for its wine cellars")]),
    "Geneva": ("Switzerland", [("city", "hosts the European headquarters of the United Nations")]),
    "Rio": ("Brazil", [("city", "is overlooked by the Christ the Redeemer statue")]),
}
FIRST_NAMES = {"Picasso": "Pablo", "Cervantes": "Miguel", "Mozart": "Wolfgang", "Freud": "Sigmund", "Beethoven": "Ludwig",
               "Goethe": "Johann", "Bach": "Johann", "Kant": "Immanuel", "Tolstoy": "Leo", "Dostoevsky": "Fyodor",
               "Tchaikovsky": "Pyotr", "Chekhov": "Anton", "Galileo": "Galileo", "Dante": "Dante", "Vivaldi": "Antonio",
               "Michelangelo": "Michelangelo", "Verdi": "Giuseppe", "Hugo": "Victor", "Monet": "Claude",
               "Descartes": "Rene", "Napoleon": "Napoleon", "Rembrandt": "Rembrandt", "Vermeer": "Johannes",
               "Chopin": "Frederic", "Copernicus": "Nicolaus", "Nobel": "Alfred", "Linnaeus": "Carl", "Ibsen": "Henrik",
               "Grieg": "Edvard"}  # fmt: skip  (a person's hop-1 answer may come as the first name)
TYPES = {
    "countries": {
        "facts": COUNTRIES,
        "bind": "{p} grew up in {x}.",
        "pfact": "The delegation from {x} will hold its next meeting in {a}.",
        "pdesc": "the country where {p} grew up",
        "unknown": "an unnamed country",
        "q1": {"P": ("In which country did {p} grow up?", "{p} grew up in"),
               "M": ("Which {noun} {rel}?", "The {noun} that {rel} is")},
        "q2": {"M": ("On which continent is {d}?", "{D} is on the continent of"),
               "P": ("On which continent will the delegation from {d} hold its next meeting?",
                     "The delegation from {d} will hold its next meeting on the continent of")},
    },
    "people": {
        "facts": PEOPLE,
        "bind": "{p} wrote a doctoral thesis on {x}.",
        "pfact": "In the new film series, {x} is played by {an} {a} actor.",
        "pdesc": "the person {p} wrote a doctoral thesis on",
        "unknown": "an unnamed historical figure",
        "q1": {"P": ("Who did {p} write a doctoral thesis on?", "{p} wrote a doctoral thesis on"),
               "M": ("Which {noun} {rel}?", "The {noun} who {rel} was")},
        "q2": {"M": ("What was the nationality of {d}?", "The nationality of {d} was"),
               "P": ("What is the nationality of the actor who plays {d} in the new film series?",
                     "In the new film series, {d} is played by an actor whose nationality is")},
    },
    "cities": {
        "facts": CITIES,
        "bind": "{p} moved to {x} last spring.",
        "pfact": "This year, {x} was paired with a partner city in {a}.",
        "pdesc": "the city {p} moved to last spring",
        "unknown": "an unnamed city",
        "q1": {"P": ("Which city did {p} move to last spring?", "Last spring, {p} moved to"),
               "M": ("Which {noun} {rel}?", "The {noun} that {rel} is")},
        "q2": {"M": ("In which country is {d}?", "{D} is in the country of"),
               "P": ("In which country is the partner city of {d}?",
                     "This year, {d} was paired with a partner city in the country of")},
    },
}
PEOPLE_NAMES = ["Laura Bennett", "Mark Ellison", "Nina Hart", "Paul Whitaker", "Ruth Calloway", "Adam Pryce",
                "Clara Dunmore", "Eli Thornton", "Grace Holloway", "Owen Marsh", "Hannah Kerr", "Simon Ashby",
                "Maya Linden", "Felix Ward", "Iris Pemberton", "Jonah Wells", "Tess Garland", "Nora Blake",
                "Alice Moreland", "Ben Crowley", "Fiona Lockwood", "Gavin Shore"]  # fmt: skip
ABSENT_NAMES = ["Martha Quill", "Desmond Fry", "Lena Hargrove"]  # never in a passage: for the guess prompts
GENRES = {
    "news": ("REGIONAL DESK - Organizers released new details ahead of next month's events.", "More updates will follow."),
    "email": ("Hi all,\n\nA few updates before Friday's meeting.", "Best,\nMarta"),
    "forum": ("Posted by travel_notes_88:", "Has anyone else heard about this?"),
    "notes": ("Meeting notes, 14 March.", "Next meeting in two weeks."),
}
LEVELS = {0: {"entities": 3, "filler": 2}, 1: {"entities": 6, "filler": 6}}
WORDS = ("PP", "PM", "MP", "MM")
CHAT_INSTRUCTION = "Answer with just the answer, nothing else."


def an(word: str) -> str:
    return "an" if word[0].upper() in "AEIOU" else "a"


def first_tokens(tok, answers: list[str]) -> dict[str, tuple[int, int]]:
    return {a: (tok(" " + a, add_special_tokens=False).input_ids[0], tok(a, add_special_tokens=False).input_ids[0])
            for a in answers}  # fmt: skip


def check_vocab(tokenizers: dict) -> None:
    """Every answer vocabulary (and each type's bridges) has distinct first tokens, both readings, every tokenizer."""
    for tname, t in TYPES.items():
        vocab = sorted({v[0] for v in t["facts"].values()})
        for name, tok in tokenizers.items():
            for label, words in (("answers", vocab), ("bridges", sorted(t["facts"]))):
                ft = first_tokens(tok, words)
                for k in (0, 1):
                    seen = collections.Counter(v[k] for v in ft.values())
                    clash = [w for w, v in ft.items() if seen[v[k]] > 1]
                    assert not clash or label == "bridges", f"{tname} {label} share a first token ({name}): {clash}"
                    if clash:
                        print(f"note: {tname} bridges sharing a first token ({name}, reading {k}): {clash}")


def filler_pool(rng: random.Random, banned: set[str]) -> list[str]:
    """Real WikiText sentences (8-30 words) that name no bridge, answer or fictional person."""
    pool = []
    for row in pins.wikitext_rows():
        for s in re.split(r"(?<=[.!?])\s+", row.strip()):
            if not (8 <= len(s.split()) <= 30) or not s[0].isupper() or s.count("@") or "=" in s:
                continue
            if any(re.search(r"\b" + re.escape(b) + r"\b", s, re.I) for b in banned):
                continue
            for x, y in ((" , ", ", "), (" .", "."), (" 's", "'s"), (" ( ", " ("), (" )", ")"), (" : ", ": "),
                         (" ; ", "; "), (" '", "'"), (' " ', ' "')):
                s = s.replace(x, y)
            if s.endswith((":", ";")) or s.count('"') % 2:
                continue
            pool.append(s)
    rng.shuffle(pool)
    return pool


def passage(rng: random.Random, genre: str, facts: list[str], filler: list[str]) -> str:
    """The genre's opening, the facts and the filler shuffled together (facts keep no fixed position), its closing."""
    body = facts + filler
    rng.shuffle(body)
    head, tail = GENRES[genre]
    if genre == "notes":
        return head + "\n" + "\n".join("- " + s for s in body) + "\n" + tail
    return head + "\n" + " ".join(body) + "\n" + tail


def make(name: str, seed: int, n_scenes: int) -> None:
    from transformers import AutoTokenizer

    tokenizers = {n: AutoTokenizer.from_pretrained(pins.TARGETS[n]["repo"], revision=pins.TARGETS[n]["revision"])
                  for n in TOKENIZERS}  # fmt: skip
    check_vocab(tokenizers)
    rng = random.Random(seed)
    banned = {b for t in TYPES.values() for b in t["facts"]} | {v[0] for t in TYPES.values() for v in t["facts"].values()}
    banned |= {w for n in PEOPLE_NAMES + ABSENT_NAMES for w in n.split()} | {"Olympic", "Olympics", "continent"}
    pool = filler_pool(rng, banned)
    items: dict[str, list[dict]] = {"cloze": [], "chat": []}
    k = 0
    for tname, t in TYPES.items():
        facts = t["facts"]
        vocab = sorted({v[0] for v in facts.values()})
        for level, knobs in LEVELS.items():
            for x in sorted(facts):
                for rep in range(n_scenes):
                    for group in ("P", "M"):
                        k += 1
                        scene = f"nat:{tname}:{group}-L{level}-{x}-{rep}"
                        real = facts[x][0]
                        # distractor entities: other answers first (chance_same_answer stays low)
                        others = sorted(set(facts) - {x})
                        rng.shuffle(others)
                        others.sort(key=lambda o: facts[o][0] == real)
                        ents = [x] + others[: knobs["entities"] - 1]
                        persons = rng.sample(PEOPLE_NAMES, len(ents))
                        # P-final facts: an answer from the vocabulary, never the entity's real property
                        pfinal = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}
                        binds = [t["bind"].format(p=p, x=e) for p, e in zip(persons, ents, strict=True)]
                        pfacts = [t["pfact"].format(x=e, a=pfinal[e], an=an(pfinal[e])) for e in ents]
                        genre = rng.choice(sorted(GENRES))
                        fill = [pool.pop() for _ in range(knobs["filler"])]
                        order_seed = rng.random()
                        full = passage(random.Random(order_seed), genre, binds + pfacts, fill)
                        noun, rel = rng.choice(facts[x][1])
                        if group == "P":
                            d1, start = t["pdesc"].format(p=persons[0]), "P"
                            q1 = tuple(s.format(p=persons[0]) for s in t["q1"]["P"])
                            guess_d = t["pdesc"].format(p=rng.choice(ABSENT_NAMES))
                        else:
                            d1, start = f"the {noun} {'who' if tname == 'people' else 'that'} {rel}", "M"
                            q1 = tuple(s.format(noun=noun, rel=rel) for s in t["q1"]["M"])
                            guess_d = t["unknown"]
                        for word in (("PP", "PM") if group == "P" else ("MP", "MM")):
                            fin = word[1]
                            ans = real if fin == "M" else pfinal[x]
                            ctx = full
                            if word == "MM":  # the bridge never in an M->M passage
                                keep = [s for s in binds + pfacts if not re.search(r"\b" + re.escape(x) + r"\b", s)]
                                ctx = passage(random.Random(order_seed), genre, keep, fill)
                            q2 = t["q2"][fin]
                            whole = (q2[0].format(d=d1), q2[1].format(d=d1, D=d1[0].upper() + d1[1:]))
                            step2 = (q2[0].format(d=x), q2[1].format(d=x, D=x))
                            guess = (q2[0].format(d=guess_d), q2[1].format(d=guess_d, D=guess_d[0].upper() + guess_d[1:]))
                            same = [e for e in ents[1:] if (facts[e][0] if fin == "M" else pfinal[e]) == ans]
                            for fr, j in (("cloze", 1), ("chat", 0)):
                                kind = "word" if fr == "cloze" else "open"
                                items[fr].append({
                                    "id": f"nat:{fr}:{word}-L{level}-{k:04d}", "word": word, "domain": tname, "format": "prose",
                                    "genre": genre, "framing": fr, "context": ctx, "question": whole[j], "answer": ans,
                                    "kind": kind, "answer_kind": kind,
                                    "steps": [{"question": q1[j], "answer": x, "kind": kind, "source": start,
                                               "alts": sorted({x, FIRST_NAMES.get(x, x)})},
                                              {"question": step2[j], "answer": ans, "kind": kind, "source": fin}],
                                    "bridge": x, "bridges": [x], "start_desc": d1, "guess_question": guess[j],
                                    "scene": scene, "level": level, "knobs": knobs, "numbers": "words", "c_op": None,
                                    "chance_same_answer": round(len(same) / max(1, len(ents) - 1), 3),
                                    "entities": ents, "real": real, "prompt_answer": pfinal[x],
                                })  # fmt: skip
    for fr, its in items.items():
        out = DATA / f"{name}_{fr}"
        assert not out.exists(), f"{out} exists; sets are written once"
        out.mkdir(parents=True)
        (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in its))
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        (out / "manifest.json").write_text(json.dumps({"set": f"{name}_{fr}", "seed": seed, "scenes_per_bridge": n_scenes,
                                                       "n": len(its), "git_commit": commit,
                                                       "by_word": collections.Counter(it["word"] for it in its),
                                                       "script": "scripts/natural_v1.py"}, indent=2) + "\n")  # fmt: skip
        print(f"{name}_{fr}: {len(its)} items", dict(collections.Counter((it["domain"], it["word"]) for it in its)))


def derive_qa(name: str) -> None:
    """NAME_qa from NAME_chat (2026-10-23): the same items and passages as raw text with a fixed two-example
    Question/Answer preamble, read after "Answer:" (kind "word"). The plain cloze stems failed on the 9B (whole question
    0-9% on three words: the read token was " the" or ":"); without the preamble the 9B wanted a blank line after
    "Answer:"."""
    src, dst = DATA / f"{name}_chat", DATA / f"{name}_qa"
    assert not dst.exists(), f"{dst} exists; sets are written once"
    items = []
    for line in (src / "items.jsonl").read_text().splitlines():
        it = json.loads(line)
        it.update(id=it["id"].replace("nat:chat:", "nat:qa:"), framing="qa", kind="word", answer_kind="word")
        it["steps"] = [{**st, "kind": "word"} for st in it["steps"]]
        items.append(it)
    dst.mkdir(parents=True)
    (dst / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    (dst / "manifest.json").write_text(json.dumps({"set": dst.name, "from": src.name, "n": len(items),
                                                   "script": "scripts/natural_v1.py derive-qa"}, indent=2) + "\n")
    print(f"{dst.name}: {len(items)} items")


def vocab_of(items: list[dict]) -> dict:
    """Per relation (domain): every answer, and every bridge with a person's first name (the candidate-rank read)."""
    v: dict = {}
    for it in items:
        v.setdefault((it["domain"], "answer"), set()).add(it["answer"])
        v.setdefault((it["domain"], "bridge"), set()).update(it["steps"][0].get("alts", [it["bridge"]]))
    for (dom, kind), vals in list(v.items()):
        if kind == "bridge":
            vals |= {FIRST_NAMES.get(x, x) for x in vals}
    return v


def competence(set_name: str, run: str, why: str, read: str = "top", limit: int = 0) -> None:
    """Whole question, each hop alone and the guess prompt, one forward each. read "top": correct = the answer's first
    token is the top token (a person's first name counts for hop 1); read "cand" (2026-10-23): the top among the
    relation's candidate answers (bridges for hop 1), so format tokens cannot fail it, as ablate_v2 --read cand. Both
    reads are recorded either way. Rows and summary in tasks_v2's competence format."""
    import statistics

    from bridge_jspace.model import load_model
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    pins.check_run_name(run)
    out = pins.RESULTS_DIR / "tasks_v2" / run
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"run": run, "why": why, "set": set_name, "model": pins.model_pin(),
                                                   "git_commit": commit, "guess": True,
                                                   "read": read, "reads": "top: the answer's first token is the top token; cand: the top among the relation's candidates",
                                                   "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    jobs = []
    for it in T.load(set_name)[: limit or None]:
        parts = [("whole", it["question"], it["answer"])] + [(f"step{i}", s["question"], s["answer"])
                                                             for i, s in enumerate(it["steps"], 1)]
        parts.append(("guess", it["guess_question"], it["answer"]))
        alts = {"step1": it["steps"][0].get("alts", [])}
        for part, q, a in parts:
            ids = S.ids(tok, T.render(tok, {**it, "_question": q, "_kind": it["kind"]}))
            alt_s = [tok.decode([S.answer_token(tok, x, it["kind"])]).strip() for x in alts.get(part, [])]
            jobs.append({"alts": alt_s, "alt_names": alts.get(part, []), "part": part, "id": it["id"], "scene": it["scene"], "word": it["word"], "domain": it["domain"],
                         "format": it["format"], "level": it["level"], "numbers": "words", "c_op": None, "ids": ids,
                         "answer_kind": it["kind"], "expected": a, "kind": it["kind"], "answer": a})  # fmt: skip
    t0 = time.time()
    S.read_answers(model, tok, jobs)
    import torch

    items_ = T.load(set_name)
    vocab, dom_of = vocab_of(items_), {it["id"]: it["domain"] for it in items_}
    own_vocab = {}
    for it in items_:
        if it.get("answer_vocab"):
            own_vocab[(it["id"], "whole")] = own_vocab[(it["id"], "guess")] = it["answer_vocab"]
        for i, st in enumerate(it["steps"], 1):
            if st.get("cand_vocab"):
                own_vocab[(it["id"], f"step{i}")] = st["cand_vocab"]
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    with torch.inference_mode():
        for group in by_len.values():
            for st in range(0, len(group), 64):
                chunk = group[st : st + 64]
                logits = model.hf(input_ids=torch.tensor([j["ids"] for j in chunk], device="cuda"), logits_to_keep=1).logits[:, -1].float()
                for row, j in enumerate(chunk):
                    want = S.answer_token(tok, j["expected"], j["kind"])
                    own = own_vocab.get((j["id"], j["part"]))  # natural3: per-step / whole-question vocabularies
                    pool = own or vocab[(dom_of[j["id"]], "bridge" if j["part"] == "step1" else "answer")]
                    ok_ids = {want} | ({S.answer_token(tok, FIRST_NAMES.get(j["expected"], j["expected"]), j["kind"])} if j["part"] == "step1" else set())
                    c = torch.tensor(sorted({S.answer_token(tok, v, j["kind"]) for v in pool} | ok_ids), device="cuda")
                    j["correct_cand"] = int(c[logits[row, c].argmax()]) in ok_ids
                    # cand2 (2026-10-23, amendment 20): every candidate in either case (animals' prompt answers are
                    # lowercase), and for hop 1 each of the item's own names for the bridge (natplus's rare people's
                    # first names were missing from FIRST_NAMES here, so their hop 1 failed the cand read)
                    both = lambda v, k=j["kind"]: {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k)}  # noqa: E731
                    ok2 = both(j["expected"]) | {t for x in j["alt_names"] for t in both(x)}
                    c2 = torch.tensor(sorted({t for v in pool for t in both(v)} | ok2), device="cuda")
                    j["correct_cand2"] = int(c2[logits[row, c2].argmax()]) in ok2
    for j in jobs:  # a person's hop 1 may be read as the first name (Wolfgang for Mozart): either first token counts
        j["correct_top"] = j["margin"] > 0 or j["read_top"] in j["alts"]
        j["correct"] = {"top": j["correct_top"], "cand": j["correct_cand"], "cand2": j["correct_cand2"]}[read]
    rows = [{k: v for k, v in j.items() if k not in ("ids", "forced")} for j in jobs]
    (out / "items.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    acc = lambda sel: round(statistics.mean(r["correct"] for r in sel), 3) if sel else None  # noqa: E731
    whole = [r for r in rows if r["part"] == "whole"]
    summary: dict = {"seconds": round(time.time() - t0), "by_word_level": {}, "by_domain": {}, "pick": {}}
    for w in dict.fromkeys(r["word"] for r in whole):
        for lv in sorted({r["level"] for r in whole}):
            sel = [r for r in whole if r["word"] == w and r["level"] == lv]
            ids_ = {r["id"] for r in sel}
            st = collections.defaultdict(list)
            for r in rows:
                if r["id"] in ids_ and r["part"].startswith("step"):
                    st[r["id"]].append(r["correct"])
            summary["by_word_level"][f"{w}/L{lv}"] = {
                "n": len(sel), "whole": acc(sel), "all_steps": acc([{"correct": all(v)} for v in st.values()]),
                "median_margin": round(statistics.median(r["margin"] for r in sel), 2) if sel else None,
                "guess": acc([r for r in rows if r["id"] in ids_ and r["part"] == "guess"]),
                "top_wrong": collections.Counter(r["read_top"] for r in sel if not r["correct"]).most_common(3)}  # fmt: skip
    for d in sorted({r["domain"] for r in whole}):
        summary["by_domain"][d] = {w: acc([r for r in whole if r["domain"] == d and r["word"] == w]) for w in dict.fromkeys(r["word"] for r in whole)}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=1)[:4000])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "competence", "derive-qa"])
    ap.add_argument("--name")
    ap.add_argument("--seed", type=int, default=801)
    ap.add_argument("--scenes", type=int, default=2, help="make: scenes per bridge, level and start group")
    ap.add_argument("--set", dest="set_name")
    ap.add_argument("--why")
    ap.add_argument("--read", choices=["top", "cand", "cand2"], default="top", help="competence: the read that sets correct")
    ap.add_argument("--limit", type=int, default=0, help="competence: only the first N items (smoke tests)")
    a = ap.parse_args()
    if a.stage == "make":
        make(a.name, a.seed, a.scenes)
    elif a.stage == "derive-qa":
        derive_qa(a.name)
    else:
        competence(a.set_name, a.name, a.why, a.read, a.limit)
