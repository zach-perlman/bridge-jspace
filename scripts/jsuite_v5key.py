"""jsuite_v5key (Zach, 2026-10-29, prereg amendment 60 note 29 and its addendum): the remembered attribute as a key.

Each scene: a passage of six lines "The delegation from <country> will wear <colour> badges." (X's country and five
other countries, one colour each), spliced into v4's filler. No entity is named in the passage. The question names X
(jsuite_v5kn) or describes it (jsuite_v5kd) and asks for the colour of X's country's delegation: X's country is a key
the model must recall and use, never say. The two sets share scenes (same passage, same X): items pair by id suffix.
Words (one item each per scene):
  MP  the key lookup: "What colour badges will the delegation from Achebe's home country wear?" -> X's colour
  MM  the say-twin: "Which country is Achebe from?" -> X's country (among the passage's six: recognition)
  controls (jsuite_v5knctl / jsuite_v5kdctl, closed book, context ""):
  H1  hop 1: named, the say question; described, the description -> the entity ("Which person wrote Arrow of God?")
  K0  the country -> colour prior: "What colour badges will the delegation from Nigeria wear?" (answer: the colour the
      scene assigned at random; it should sit at chance)
Steps: named MP [say, direct key lookup]; named MM [say, say]; described MP [description -> entity, named MP, direct
key lookup]; described MM [description -> entity, named say]. Every step carries its own cand_vocab (countries, colours,
or the relation's entity names) so no read falls back to a set-wide pool.
Design (Zach's answers, 29 Oct, and the addendum):
  - people (nationality -> its country), cities, companies, landmarks (country); films dropped;
  - entities whose name reveals the country are excluded (name_reveals_answer, or a country / nationality word in the
    name or its other names, word or stem match);
  - the five other countries never share a first token with each other or X's country (any of the three models'
    tokenizers, either case, with or without a leading space) and never appear in, or share a 4-letter stem with,
    X's name or description; colours the question names (stem match, e.g. "Golden" -> gold) are never drawn;
  - two scenes per (entity, description) (rep 0 and 1), one question wording (wording 0); X's line rotated through
    the six positions per relation; v4's filler genres and splice; descriptions sharing a 4-letter stem with X's name
    skipped (v4's stem filter); fillers re-dealt while they share a stem with the description;
  - flag_colour_match: the assigned colour is a colour of X's country's flag (or one of three iconic sport colours).

python scripts/jsuite_v5key.py [--seed 5001] [--prefix v5k]  -> data/tasks_v2/jsuite_v5kn_test_chat (MP MM),
    jsuite_v5knctl_test_chat (H1 K0), jsuite_v5kd_test_chat (MP MM), jsuite_v5kdctl_test_chat (H1 K0)
The rebuild (2026-10-29, after a red-team; the default build above is unchanged and reproduces byte for byte):
python scripts/jsuite_v5key.py --seed 5002 --suffix 2 --same-continent 2  -> jsuite_v5kn2 / v5kn2ctl / v5kd2 / v5kd2ctl:
    at least two of the five other countries from X's continent (as many as the pool holds; Oceania has Australia
    alone) and one from X's region where the pool has one; items add x_continent, x_region, n_same_continent,
    n_same_region, n_continent_available, n_region_available.
The 3+3 rebuild (amendment 61 addendum, Zach; overwrites the --same-continent build of v5kn2 / v5kd2, never run):
python scripts/jsuite_v5key.py --seed 5002 --suffix 2 --split33  -> the same four sets: three countries from X's continent
    (X + two, one from X's region where possible) and three from one other continent drawn at random among those with
    >= 3 eligible countries, so no continent is a majority; where X's continent has fewer (Oceania: Australia alone)
    the rest come from further continents, none past three. Items add other_continent, n_other_continent and split_ok
    (true only for an exact 3+3).
Note 35's compute arm (amendment 63, Zach, 2026-10-30; the four builds above are unchanged and reproduce byte for byte):
python scripts/jsuite_v5key.py --seed 5002 --suffix 2 --split33 --compute  -> jsuite_v5kn2c_test_chat (MC MC0) and
    jsuite_v5kn2cctl_test_chat (H1 C0), on jsuite_v5kn2's named scenes (same passage, same X; ids j3:chat:v5kn2c:MC-w0-<suffix>
    pair with kn2's by suffix). The four kn2 / kd2 sets are rebuilt in memory and checked against the files on disk (sha256)
    instead of rewritten; no extra random draw is made, so they cannot move.
  MC  "What is the capital of Achebe's home country?" (cities "...of the country where X is located", companies "...is based",
      landmarks "...stands") -> the capital of X's country; candidates: the capitals of the passage's six countries
  steps [the say question, the direct capital "What is the capital of Nigeria?"], with the passage, as MP's; the guess asks
      about "an unnamed figure" (chance 1/6)
  MC0 (amendment 63 addendum) the MC question, its steps and its guess closed book (context ""): steps H1's and C0's prompts;
      it sits in jsuite_v5kn2c beside MC (not in the controls set) so competence, v4_split and the knock-out read it as MC
  controls (closed book): H1 the say question (as kn2ctl's; v4_split's gate reads it), C0 the direct capital
  A scene is left out of MC (kn2 untouched) when two of its six capitals share a first token (any of the three tokenizers,
  either case, with or without a leading space), a capital shares a 4-letter stem with its own country's name or is that
  name, or a capital shares a 4-letter stem with X's name. Capitals: CAPITAL, written 2026-10-30 for every country in the
  vocabulary (England and the United Kingdom: London); CAPITAL_NOTE marks the contested or split ones (recorded, not dropped).
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT), str(ROOT / "src")]
import jsuite_v3 as V3  # noqa: E402
import jsuite_v3_tables as T3  # noqa: E402
import jsuite_v4 as V4  # noqa: E402

DATA = ROOT / "data" / "tasks_v2"
K = 6  # countries per scene
N_FILLER = 6
REPS = 2  # scenes per (entity, description)
RELS = ("people", "cities", "companies", "landmarks")
TOKENIZERS = ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")

# people's nationality (v3_bridges' answer) -> the country asked for
NAT2C = {"American": "United States", "Argentine": "Argentina", "Australian": "Australia", "Austrian": "Austria",
         "Belgian": "Belgium", "Brazilian": "Brazil", "Canadian": "Canada", "Chilean": "Chile", "Chinese": "China",
         "Colombian": "Colombia", "Czech": "Czech Republic", "Danish": "Denmark", "Dutch": "Netherlands", "Egyptian": "Egypt",
         "English": "England", "French": "France", "German": "Germany", "Greek": "Greece", "Hungarian": "Hungary",
         "Indian": "India", "Irish": "Ireland", "Italian": "Italy", "Jamaican": "Jamaica", "Japanese": "Japan",
         "Kenyan": "Kenya", "Mexican": "Mexico", "Nigerian": "Nigeria", "Norwegian": "Norway", "Polish": "Poland",
         "Portuguese": "Portugal", "Russian": "Russia", "South African": "South Africa", "Spanish": "Spain",
         "Swedish": "Sweden"}  # fmt: skip
EXTRA_ALIASES = {"England": ["United Kingdom", "the United Kingdom", "UK", "the UK", "Britain", "Great Britain"]}
# country -> words that name or give it away (demonyms, adjectives, old and short names); with the country's own name
# and aliases these are the reveal words (name exclusion, desc_cue, filler bans)
DEMONYM = {
    "Argentina": ["Argentine", "Argentinian", "Argentinean"], "Australia": ["Australian", "Aussie"],
    "Austria": ["Austrian"], "Belgium": ["Belgian"], "Brazil": ["Brazilian"], "Cambodia": ["Cambodian", "Khmer"],
    "Canada": ["Canadian"], "Chile": ["Chilean"], "China": ["Chinese"], "Colombia": ["Colombian"],
    "Czech Republic": ["Czech", "Czechia", "Bohemia", "Bohemian"], "Denmark": ["Danish", "Dane"], "Egypt": ["Egyptian"],
    "England": ["English", "British", "Britain", "Briton", "Anglo"], "Finland": ["Finnish", "Finn"], "France": ["French"],
    "Germany": ["German", "Deutsch", "Deutsche", "Deutschland"], "Greece": ["Greek", "Hellenic"],
    "Hungary": ["Hungarian", "Magyar"], "India": ["Indian"], "Indonesia": ["Indonesian"], "Ireland": ["Irish"],
    "Israel": ["Israeli"], "Italy": ["Italian", "Italia"], "Jamaica": ["Jamaican"], "Japan": ["Japanese", "Nippon"],
    "Jordan": ["Jordanian"], "Kenya": ["Kenyan"], "Malaysia": ["Malaysian", "Malay"], "Mexico": ["Mexican"],
    "Morocco": ["Moroccan"], "Netherlands": ["Dutch", "Holland"], "Nigeria": ["Nigerian"], "Norway": ["Norwegian"],
    "Peru": ["Peruvian"], "Poland": ["Polish", "Pole"], "Portugal": ["Portuguese"], "Russia": ["Russian", "Soviet"],
    "South Africa": ["South African"], "South Korea": ["Korea", "Korean"], "Spain": ["Spanish", "Spaniard"],
    "Sweden": ["Swedish", "Swede"], "Taiwan": ["Taiwanese"], "Tanzania": ["Tanzanian"], "Thailand": ["Thai", "Siam", "Siamese"],
    "Turkey": ["Turkish", "Turk", "Turkiye"], "United States": ["American", "America", "US", "USA", "U.S."],
    "Venezuela": ["Venezuelan"], "Vietnam": ["Vietnamese"],
}  # fmt: skip
COLOURS = ["Black", "Blue", "Brown", "Gold", "Green", "Grey", "Orange", "Pink", "Purple", "Red", "Silver", "White", "Yellow"]
COLOUR_ALIASES = {"Grey": ["Gray"]}
_RWB, _RW = ["Red", "White", "Blue"], ["Red", "White"]
_YG = ["Yellow", "Gold"]
# country -> its flag's colours (yellow and gold both count for a yellow / gold field), plus three iconic sport colours
# (Netherlands orange, Italy blue, Australia green and gold)
FLAG = {
    "Argentina": ["Blue", "White", *_YG], "Australia": [*_RWB, "Green", *_YG], "Austria": _RW, "Belgium": ["Black", "Red", *_YG],
    "Brazil": ["Green", "Blue", "White", *_YG], "Cambodia": _RWB, "Canada": _RW, "Chile": _RWB, "China": ["Red", *_YG],
    "Colombia": ["Blue", "Red", *_YG], "Czech Republic": _RWB, "Denmark": _RW, "Egypt": [*_RW, "Black", "Gold"],
    "England": _RW, "Finland": ["Blue", "White"], "France": _RWB, "Germany": ["Black", "Red", *_YG], "Greece": ["Blue", "White"],
    "Hungary": [*_RW, "Green"], "India": ["Orange", "White", "Green", "Blue"], "Indonesia": _RW, "Ireland": ["Green", "White", "Orange"],
    "Israel": ["Blue", "White"], "Italy": [*_RW, "Green", "Blue"], "Jamaica": ["Black", "Green", *_YG], "Japan": _RW,
    "Jordan": [*_RW, "Black", "Green"], "Kenya": [*_RW, "Black", "Green"], "Malaysia": [*_RWB, *_YG], "Mexico": [*_RW, "Green"],
    "Morocco": ["Red", "Green"], "Netherlands": [*_RWB, "Orange"], "Nigeria": ["Green", "White"], "Norway": _RWB, "Peru": _RW,
    "Poland": _RW, "Portugal": ["Red", "Green"], "Russia": _RWB, "South Africa": [*_RWB, "Green", "Black", *_YG],
    "South Korea": [*_RWB, "Black"], "Spain": ["Red", *_YG], "Sweden": ["Blue", *_YG], "Taiwan": _RWB,
    "Tanzania": ["Green", "Black", "Blue", *_YG], "Thailand": _RWB, "Turkey": _RW, "United States": _RWB,
    "Venezuela": [*_RWB, *_YG], "Vietnam": ["Red", *_YG],
}  # fmt: skip
# --same-continent (the rebuild, 2026-10-29, after a red-team): country -> continent and finer region (UN M49 sub-regions;
# Russia in Europe, Turkey in Asia; the Americas split into North and South America, with M49's Latin America and the
# Caribbean split into Central America, the Caribbean and South America; Oceania holds Australia alone)
CONTINENT = {
    **dict.fromkeys(["Denmark", "Finland", "Ireland", "Norway", "Sweden", "England", "Austria", "Belgium", "France", "Germany",
                     "Netherlands", "Greece", "Italy", "Portugal", "Spain", "Czech Republic", "Hungary", "Poland", "Russia"], "Europe"),
    **dict.fromkeys(["China", "Japan", "South Korea", "Taiwan", "Cambodia", "Indonesia", "Malaysia", "Thailand", "Vietnam", "India",
                     "Israel", "Jordan", "Turkey"], "Asia"),
    **dict.fromkeys(["Egypt", "Morocco", "Kenya", "Tanzania", "Nigeria", "South Africa"], "Africa"),
    **dict.fromkeys(["United States", "Canada", "Mexico", "Jamaica"], "North America"),
    **dict.fromkeys(["Argentina", "Brazil", "Chile", "Colombia", "Peru", "Venezuela"], "South America"),
    "Australia": "Oceania",
}  # fmt: skip
REGION = {
    **dict.fromkeys(["Denmark", "Finland", "Ireland", "Norway", "Sweden", "England"], "Northern Europe"),
    **dict.fromkeys(["Austria", "Belgium", "France", "Germany", "Netherlands"], "Western Europe"),
    **dict.fromkeys(["Greece", "Italy", "Portugal", "Spain"], "Southern Europe"),
    **dict.fromkeys(["Czech Republic", "Hungary", "Poland", "Russia"], "Eastern Europe"),
    **dict.fromkeys(["China", "Japan", "South Korea", "Taiwan"], "Eastern Asia"),
    **dict.fromkeys(["Cambodia", "Indonesia", "Malaysia", "Thailand", "Vietnam"], "South-eastern Asia"),
    "India": "Southern Asia", **dict.fromkeys(["Israel", "Jordan", "Turkey"], "Western Asia"),
    **dict.fromkeys(["Egypt", "Morocco"], "Northern Africa"),
    **dict.fromkeys(["Kenya", "Tanzania", "Nigeria", "South Africa"], "Sub-Saharan Africa"),
    **dict.fromkeys(["United States", "Canada"], "Northern America"), "Mexico": "Central America", "Jamaica": "Caribbean",
    **dict.fromkeys(["Argentina", "Brazil", "Chile", "Colombia", "Peru", "Venezuela"], "South America"),
    "Australia": "Australia and New Zealand",
}  # fmt: skip
SAY = {"people": "Which country is {x} from?", "cities": "Which country is {x} in?",
       "companies": "Which country is {x} based in?", "landmarks": "Which country is {x} in?"}  # fmt: skip
KEY_NAMED = {"people": "What colour badges will the delegation from {x}'s home country wear?",
             "cities": "What colour badges will the delegation from the country where {x} is located wear?",
             "companies": "What colour badges will the delegation from the country where {x} is based wear?",
             "landmarks": "What colour badges will the delegation from the country where {x} stands wear?"}  # fmt: skip
KEY_DESC = {**KEY_NAMED, "people": "What colour badges will the delegation from the home country of {x} wear?"}
DIRECT = "What colour badges will the delegation from {c} wear?"
LINE = "The delegation from {c} will wear {colour} badges."
UNKNOWN = {"people": "an unnamed figure", "cities": "an unnamed city", "companies": "an unnamed company",
           "landmarks": "an unnamed landmark"}  # fmt: skip
# --compute (amendment 63 note 35, 2026-10-30): one remembered fact, a third use. The capital table, written now for every
# country in the vocabulary (and the United Kingdom, England's alias: London); ASCII spellings, accented forms as aliases.
CAPITAL = {
    "Argentina": "Buenos Aires", "Australia": "Canberra", "Austria": "Vienna", "Belgium": "Brussels", "Brazil": "Brasilia",
    "Cambodia": "Phnom Penh", "Canada": "Ottawa", "Chile": "Santiago", "China": "Beijing", "Colombia": "Bogota",
    "Czech Republic": "Prague", "Denmark": "Copenhagen", "Egypt": "Cairo", "England": "London", "United Kingdom": "London",
    "Finland": "Helsinki", "France": "Paris", "Germany": "Berlin", "Greece": "Athens", "Hungary": "Budapest",
    "India": "New Delhi", "Indonesia": "Jakarta", "Ireland": "Dublin", "Israel": "Jerusalem", "Italy": "Rome",
    "Jamaica": "Kingston", "Japan": "Tokyo", "Jordan": "Amman", "Kenya": "Nairobi", "Malaysia": "Kuala Lumpur",
    "Mexico": "Mexico City", "Morocco": "Rabat", "Netherlands": "Amsterdam", "Nigeria": "Abuja", "Norway": "Oslo",
    "Peru": "Lima", "Poland": "Warsaw", "Portugal": "Lisbon", "Russia": "Moscow", "South Africa": "Pretoria",
    "South Korea": "Seoul", "Spain": "Madrid", "Sweden": "Stockholm", "Taiwan": "Taipei", "Tanzania": "Dodoma",
    "Thailand": "Bangkok", "Turkey": "Ankara", "United States": "Washington", "Venezuela": "Caracas", "Vietnam": "Hanoi",
}  # fmt: skip
CAPITAL_ALIASES = {"Brasilia": ["Brasília"], "Bogota": ["Bogotá"], "Washington": ["Washington, D.C.", "Washington D.C.", "Washington DC"]}
CAPITAL_NOTE = {  # contested or split capitals: recorded on the items (capital_note), not dropped
    "Israel": "Jerusalem: Israel's designated capital; its status is disputed and most embassies are in Tel Aviv",
    "Netherlands": "Amsterdam: the constitutional capital; the seat of government is The Hague",
    "South Africa": "Pretoria: the executive capital (Cape Town legislative, Bloemfontein judicial)",
    "Malaysia": "Kuala Lumpur: the official capital; the administrative centre is Putrajaya",
    "Tanzania": "Dodoma: the official capital; Dar es Salaam is the largest city and the former capital",
    "Indonesia": "Jakarta: the capital in use; a move to Nusantara is legislated",
}  # fmt: skip
COMPUTE = {"people": "What is the capital of {x}'s home country?",
           "cities": "What is the capital of the country where {x} is located?",
           "companies": "What is the capital of the country where {x} is based?",
           "landmarks": "What is the capital of the country where {x} stands?"}  # fmt: skip
COMPUTE_GUESS = {**COMPUTE, "people": "What is the capital of the home country of {x}?"}  # as MP's guess (KEY_DESC)
DIRECT_CAPITAL = "What is the capital of {c}?"


def word_re(w: str, stem: bool = False) -> re.Pattern:
    """A reveal word in text: short all-caps forms (US, UK, USA) case-sensitive and whole; others case-insensitive, whole
    (with a plural or possessive) or, with stem, as the start of any word ("Deutsch" in "Deutsche")."""
    if len(w) <= 3 or w.isupper() or "." in w:
        return re.compile(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])")
    return re.compile(r"(?i)\b" + re.escape(w) + (r"" if stem else r"(?:s|'s)?\b"))


def first_tokens(toks: dict, s: str) -> set[tuple[str, int]]:
    """(tokenizer, first token id) of s in either case, with and without a leading space."""
    out = set()
    for name, tok in toks.items():
        for f in (s, s.lower(), " " + s, " " + s.lower()):
            out.add((name, tok(f, add_special_tokens=False).input_ids[0]))
    return out


def load_tokenizers() -> dict:
    os.environ.setdefault("HF_HOME", "/workspace/hf_cache")
    from transformers import AutoTokenizer

    from bridge_jspace import pins

    return {t: AutoTokenizer.from_pretrained(pins.TARGETS[t]["repo"], revision=pins.TARGETS[t]["revision"], local_files_only=True)
            for t in TOKENIZERS}  # fmt: skip


def main(a) -> None:
    rng = random.Random(a.seed)
    tabs = T3.tables()
    table = json.loads((ROOT / "data" / "v3_bridges.json").read_text())
    rows = {(r["relation"], r["bridge"]): r for r in table}
    # countries: every country answer of the tables, and every people nationality's country
    country_of = {}
    for r in table:
        if r["relation"] == "people":
            assert r["answer"] in NAT2C, f"people answer without a country: {r['answer']}"
            country_of[(r["relation"], r["bridge"])] = NAT2C[r["answer"]]
        elif r["relation"] in RELS:
            country_of[(r["relation"], r["bridge"])] = r["answer"]
    countries = sorted(set(country_of.values()))
    aliases = collections.defaultdict(set)
    for r in table:
        if r["relation"] in ("cities", "companies", "landmarks"):
            aliases[r["answer"]] |= set(r["answer_aliases"])
    for c, al in EXTRA_ALIASES.items():
        aliases[c] |= set(al)
    aliases = {c: sorted(aliases.get(c, set())) for c in countries}
    assert set(DEMONYM) == set(countries) and set(FLAG) == set(countries), (set(countries) ^ set(DEMONYM), set(countries) ^ set(FLAG))
    assert all(set(v) <= set(COLOURS) for v in FLAG.values())
    assert set(CONTINENT) == set(countries) == set(REGION), set(countries) ^ set(CONTINENT) ^ set(REGION)
    assert all(CONTINENT[c] == CONTINENT[d] for c in countries for d in countries if REGION[c] == REGION[d])
    strip_the = lambda s: s[4:] if s.startswith("the ") else s  # noqa: E731
    reveal = {c: sorted({c, *(strip_the(x) for x in aliases[c]), *DEMONYM[c]}) for c in countries}
    # hop 1 on a country (alts): the name and its aliases without a leading article (a bare "the" token would accept any
    # reply starting with "the"); answer_aliases keep every alias (the greedy-reply scorer matches reply prefixes)
    calts = {c: sorted({c, *(strip_the(x) for x in aliases[c])}) for c in countries}

    # tokenizers: colours one token with a leading space, first tokens distinct; country pairs sharing a first token
    toks = load_tokenizers()
    ctoks = {c: first_tokens(toks, c) for c in COLOURS}
    for name, tok in toks.items():
        for c in COLOURS:
            assert len(tok(" " + c.lower(), add_special_tokens=False).input_ids) == 1, (name, c)
    for c1, c2 in itertools.combinations(COLOURS, 2):
        assert not (ctoks[c1] & ctoks[c2]), (c1, c2, ctoks[c1] & ctoks[c2])
    ktoks = {c: first_tokens(toks, c) for c in countries}
    conflict = {c: {d for d in countries if d != c and ktoks[c] & ktoks[d]} for c in countries}
    conflict_pairs = sorted({tuple(sorted((c, d))) for c in countries for d in conflict[c]})
    if a.compute:  # note 35: every country has a capital; capital pairs sharing a first token (no random draw here)
        assert set(countries) <= set(CAPITAL), set(countries) - set(CAPITAL)
        assert set(CAPITAL_NOTE) <= set(countries) and set(CAPITAL_ALIASES) <= set(CAPITAL.values())
        captoks = {c: first_tokens(toks, CAPITAL[c]) for c in countries}
        cap_conflict_pairs = sorted({tuple(sorted((CAPITAL[c], CAPITAL[d]))) for c in countries for d in countries
                                     if CAPITAL[c] != CAPITAL[d] and captoks[c] & captoks[d]})  # fmt: skip
        cap_vocab = sorted({CAPITAL[c] for c in countries})
        mc_drops = collections.Counter()  # reason -> scenes (a scene can have several)

        def mc_drop(x: str, order: list[str]) -> list[str]:
            """Note 35's rules: the reasons a scene is left out of MC (empty: kept)."""
            why = []
            if any(captoks[c] & captoks[d] for c, d in itertools.combinations(order, 2)):
                why.append("two capitals share a first token")
            if any(CAPITAL[c] == c or V4.stems(CAPITAL[c]) & V4.stems(c) for c in order):
                why.append("a capital shares a stem with its own country")
            if any(V4.stems(CAPITAL[c]) & V4.stems(x) for c in order):
                why.append("a capital shares a stem with X's name")
            return why

    # the entities: films dropped; names revealing a country excluded
    excluded = {}
    for rel in RELS:
        for (r_, b), row in rows.items():
            if r_ != rel:
                continue
            if row["name_reveals_answer"]:
                excluded[f"{rel}:{b}"] = "name_reveals_answer"
                continue
            hits = sorted({w for c in countries for w in reveal[c] for n in [b, *row.get("bridge_alts", [])] if word_re(w, stem=True).search(n)})
            if hits:
                excluded[f"{rel}:{b}"] = "name has " + ", ".join(hits)
    ent_vocab = {rel: sorted({x for (r_, b), row in rows.items() if r_ == rel for x in (b, *row.get("bridge_alts", []))}) for rel in RELS}

    # filler: v4's bans plus every country's reveal words, the colours and the frame's words
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731
    banned = {strip(b) for t in tabs.values() for b in t["facts"]} | {v[0] for t in tabs.values() for v in t["facts"].values()}
    banned |= {al for t in tabs.values() for r in t["meta"].values() for al in r["answer_aliases"]}
    banned |= {al for r in table for al in r.get("bridge_alts", [])}
    banned |= {w for n in V3.NP.PEOPLE_NAMES + V3.N.ABSENT_NAMES for w in n.split()}
    banned |= {w for xs in V3.CONT.values() for w in xs}
    banned |= {w for c in countries for w in reveal[c]} | {strip_the(x) for c in countries for x in aliases[c]}
    banned |= {c.lower() for c in COLOURS} | {x.lower() for v in COLOUR_ALIASES.values() for x in v}
    banned |= {"Olympic", "Olympics", "continent", "nationality", "director", "film", "films", "company", "landmark", "list",
               "handout", "festival", "tour", "podcast", "exhibition", "delegation", "delegations", "badge", "badges",
               "colour", "colours", "color", "colors", "country", "countries"}  # fmt: skip
    deck = V3.Deck(rng, V3.JF.clean_paras(banned))
    all_names = sorted({b for (_, b) in rows} | {al for r in table for al in r.get("bridge_alts", [])})
    name_res = [re.compile(r"(?i)\b" + re.escape(n) + r"\b") for n in all_names]
    reveal_res = {c: [word_re(w) for w in reveal[c]] for c in countries}

    def cue_in(text: str, cs) -> str | None:
        for c in cs:
            for w, rx in zip(reveal[c], reveal_res[c], strict=True):
                if rx.search(text):
                    return w
        return None

    items = {"n": [], "nctl": [], "d": [], "dctl": []}
    mc, mc_rel = {"nc": [], "ncctl": []}, collections.Counter()  # --compute: note 35's MC set and its controls
    skipped = collections.Counter()
    k = 0
    pos_counter = collections.Counter()
    for rel in RELS:
        t = tabs[rel]
        noun = "person" if rel == "people" else t["noun"]
        bridges = sorted(b for (r_, b) in rows if r_ == rel and f"{rel}:{b}" not in excluded)
        for x in bridges:
            row = rows[(rel, x)]
            key = country_of[(rel, x)]
            descs = [f"the {noun} {V4.PRON[rel]} {d['clause']}" for d in row["descriptions"]]
            for di, d in enumerate(row["descriptions"]):
                clause, desc = d["clause"], descs[di]
                if V4.stems(clause) & V4.stems(x):
                    skipped["X shares a stem with its description"] += 1
                    continue
                q_text = f"{x} {desc}"  # what the scene's named and described questions name
                bad_colours = sorted(c for c in COLOURS if re.search(r"(?i)\b" + c, q_text))
                desc_cue = cue_in(clause, [c for c in countries if c != key])
                desc_own = cue_in(clause, [key])
                for rep in range(REPS):
                    pool = [c for c in countries if c != key and c not in conflict[key] and not cue_in(q_text, [c])
                            and not (V4.stems(c) & (V4.stems(clause) | V4.stems(x)))]  # fmt: skip
                    others = None
                    other_cont = None
                    if a.split33:  # three from X's continent (X + two, one from X's region) + three from ONE other continent
                        cont = [c for c in pool if CONTINENT[c] == CONTINENT[key]]
                        reg = [c for c in cont if REGION[c] == REGION[key]]
                        by_cont = collections.defaultdict(list)
                        for c in pool:
                            by_cont[CONTINENT[c]].append(c)
                        elig = sorted(cn for cn, cs in by_cont.items() if cn != CONTINENT[key] and len(cs) >= 3)
                        for _ in range(2000):
                            oc = rng.choice(elig)
                            chosen = rng.sample(reg, 1) if reg else []
                            chosen += rng.sample([c for c in cont if c not in chosen], min(2, len(cont)) - len(chosen))
                            chosen += rng.sample(by_cont[oc], 3)
                            # X's continent short (Oceania): the rest from neither X's nor the other continent, none past three
                            rest = [c for c in pool if CONTINENT[c] not in (CONTINENT[key], oc)]
                            cand = chosen + rng.sample(rest, K - 1 - len(chosen))
                            counts = collections.Counter(CONTINENT[c] for c in [key, *cand])
                            if max(counts.values()) <= 3 and not any(b in conflict[a_] for a_, b in itertools.combinations(cand, 2)):
                                others, other_cont = cand, oc
                                break
                    elif a.same_continent:  # >= N of the five from X's continent (as many as the pool holds), one from its region
                        cont = [c for c in pool if CONTINENT[c] == CONTINENT[key]]
                        reg = [c for c in cont if REGION[c] == REGION[key]]
                        for _ in range(2000):
                            chosen = rng.sample(reg, 1) if reg else []
                            chosen += rng.sample([c for c in cont if c not in chosen], max(0, min(a.same_continent, len(cont)) - len(chosen)))
                            cand = chosen + rng.sample([c for c in pool if c not in chosen], K - 1 - len(chosen))
                            if not any(b in conflict[a_] for a_, b in itertools.combinations(cand, 2)):
                                others = cand
                                break
                    else:
                        for _ in range(500):
                            cand = rng.sample(pool, K - 1)
                            if not any(b in conflict[a_] for a_, b in itertools.combinations(cand, 2)):
                                others = cand
                                break
                    if others is None:
                        skipped["no country draw"] += 1
                        continue
                    cols = rng.sample([c for c in COLOURS if c not in bad_colours], K)
                    for _ in range(50):  # filler free of description words
                        para = deck.deal(N_FILLER)
                        if not (V4.stems(" ".join(para)) & V4.stems(clause)):
                            break
                    else:
                        skipped["filler leak"] += 1
                        continue
                    pos = pos_counter[rel] % K  # X's line rotated through the six positions
                    pos_counter[rel] += 1
                    order = others[:]
                    rng.shuffle(order)
                    order.insert(pos, key)
                    scene_keys = dict(zip(order, cols, strict=True))
                    colour = scene_keys[key]
                    genre = rng.choice(sorted(V3.N.GENRES))
                    lines = [LINE.format(c=V3.disp(c), colour=scene_keys[c].lower()) for c in order]
                    ctx = V4.splice(rng, genre, lines, para)
                    # checks: each country once, no other country or reveal word, no entity name, every colour once
                    for c in order:
                        assert len(re.findall(r"\b" + re.escape(V3.disp(c)) + r"\b", ctx)) == 1, (c, ctx)
                    assert not cue_in(ctx, [c for c in countries if c not in order]), (x, cue_in(ctx, countries))
                    assert not any(rx.search(ctx) for rx in name_res), (x, [n for n, rx in zip(all_names, name_res, strict=True) if rx.search(ctx)])
                    for c in COLOURS:
                        assert len(re.findall(r"(?i)\b" + c + r"\b", ctx)) == (1 if c in cols else 0), (c, ctx)
                    uid = f"{k:05d}"
                    k += 1
                    base = {"module": "facts", "start": "M", "domain": rel, "relation": rel, "format": "prose", "genre": genre,
                            "framing": "chat", "wording": 0, "rep": rep, "level": 2, "split": "test", "popularity": row["popularity"],
                            "half": "A", "context": ctx, "kind": "open", "answer_kind": "open", "bridge": x, "bridges": [x],
                            "desc_index": di, "skip_cue": None, "real": key, "entities": order, "passage_values": {},
                            "bridge_position": pos, "eponymous": False, "name_reveals_answer": row["name_reveals_answer"],
                            "bridge_in_passage": False, "bridge_mentions": 0, "entity_descs": {x: descs},
                            "knobs": {"entities": K, "filler": N_FILLER}, "set_version": "v4", "set_kind": "key", "key": key,
                            "key_vocab": countries, "scene_keys": scene_keys, "key_colour": colour,
                            "flag_colour_match": colour in FLAG[key], "question_colours": bad_colours}  # fmt: skip
                    if a.split33:
                        n_oc = sum(CONTINENT[c] == other_cont for c in others)
                        base.update({"other_continent": other_cont, "n_other_continent": n_oc,
                                     "split_ok": sum(CONTINENT[c] == CONTINENT[key] for c in others) == 2 and n_oc == 3})  # fmt: skip
                    if a.same_continent or a.split33:
                        base.update({"x_continent": CONTINENT[key], "x_region": REGION[key],
                                     "n_same_continent": sum(CONTINENT[c] == CONTINENT[key] for c in others),
                                     "n_same_region": sum(REGION[c] == REGION[key] for c in others),
                                     "n_continent_available": len(cont), "n_region_available": len(reg)})  # fmt: skip
                    say_n = SAY[rel].format(x=x)
                    say_step = {"question": say_n, "answer": key, "kind": "open", "source": "M", "alts": calts[key], "cand_vocab": countries}
                    direct = {"question": DIRECT.format(c=V3.disp(key)), "answer": colour, "kind": "open", "source": "P", "cand_vocab": COLOURS}
                    mp_n = KEY_NAMED[rel].format(x=x)
                    hop1 = {"question": t["q1M"][1].format(noun=noun, rel=clause), "answer": x, "kind": "open", "source": "M",
                            "alts": sorted({x, *row.get("bridge_alts", [])}), "cand_vocab": ent_vocab[rel]}  # fmt: skip
                    g_mp, g_mm = KEY_DESC[rel].format(x=UNKNOWN[rel]), SAY[rel].format(x=UNKNOWN[rel])
                    col_item = {"answer": colour, "answer_aliases": COLOUR_ALIASES.get(colour, []), "answer_vocab": COLOURS}
                    cty_item = {"answer": key, "answer_aliases": aliases[key], "answer_vocab": countries}
                    for tag, named, start_desc, q_mp, q_mm, steps_mp, steps_mm, cue, own in (
                        ("n", True, x, mp_n, say_n, [say_step, direct], [say_step, say_step], None, None),
                        ("d", False, desc, KEY_DESC[rel].format(x=desc), SAY[rel].format(x=desc),
                         [hop1, {"question": mp_n, "answer": colour, "kind": "open", "source": "P", "cand_vocab": COLOURS}, direct],
                         [hop1, say_step], desc_cue, desc_own),
                    ):  # fmt: skip
                        v = f"{a.prefix}{tag}{a.suffix}"
                        b2 = {**base, "start_desc": start_desc, "named": named, "desc_cue": cue, "desc_own_cue": own}
                        items[tag].append({**b2, "id": f"j3:chat:{v}:MP-w0-{uid}", "word": "MP", "final": "P", "final_source": "P",
                                           "control": "P", "scene": f"{v}:MP:{uid}", "question": q_mp, **col_item,
                                           "answer_in_passage": True, "memory_answer": key, "steps": steps_mp, "guess_question": g_mp})  # fmt: skip
                        items[tag].append({**b2, "id": f"j3:chat:{v}:MM-w0-{uid}", "word": "MM", "final": "M", "final_source": "M",
                                           "control": "M", "scene": f"{v}:MM:{uid}", "question": q_mm, **cty_item,
                                           "answer_in_passage": True, "memory_answer": key, "steps": steps_mm, "guess_question": g_mm})  # fmt: skip
                        ctrl = {**b2, "context": "", "answer_in_passage": False, "steps": [], "guess_question": None, "memory_answer": key}
                        h1 = {**cty_item} if named else {"answer": x, "answer_aliases": hop1["alts"], "answer_vocab": ent_vocab[rel]}
                        items[tag + "ctl"].append({**ctrl, "id": f"j3:chat:{v}:H1-w0-{uid}", "word": "H1", "final": "B", "final_source": "M",
                                                   "control": "H1", "scene": f"{v}:H1:{uid}", "question": say_n if named else hop1["question"], **h1})  # fmt: skip
                        items[tag + "ctl"].append({**ctrl, "id": f"j3:chat:{v}:K0-w0-{uid}", "word": "K0", "final": "P", "final_source": "P",
                                                   "control": "K0", "scene": f"{v}:K0:{uid}", "question": direct["question"], **col_item})  # fmt: skip
                    if a.compute:  # note 35's MC on this named scene (no random draw: kn2 / kd2 cannot move)
                        why = mc_drop(x, order)
                        mc_drops.update(why)
                        mc_rel[(rel, "dropped" if why else "kept")] += 1
                        if why:
                            continue
                        v = f"{a.prefix}n{a.suffix}c"
                        cap = CAPITAL[key]
                        caps = {c: CAPITAL[c] for c in order}
                        cvocab = sorted(set(caps.values()))  # the candidates: the passage's six countries' capitals
                        b2 = {**base, "start_desc": x, "named": True, "desc_cue": None, "desc_own_cue": None, "set_kind": "key_compute",
                              "capital": cap, "scene_capitals": caps, "capital_note": CAPITAL_NOTE.get(key),
                              "capitals_in_passage": sorted(c for c in cap_vocab if re.search(r"(?i)\b" + re.escape(c) + r"\b", ctx)),
                              "pairs_with": f"j3:chat:{a.prefix}n{a.suffix}:MP-w0-{uid}"}  # fmt: skip
                        cap_item = {"answer": cap, "answer_aliases": CAPITAL_ALIASES.get(cap, []), "answer_vocab": cvocab}
                        direct_c = {"question": DIRECT_CAPITAL.format(c=V3.disp(key)), "answer": cap, "kind": "open", "source": "M",
                                    "cand_vocab": cvocab}  # fmt: skip
                        mc["nc"].append({**b2, "id": f"j3:chat:{v}:MC-w0-{uid}", "word": "MC", "final": "M", "final_source": "M",
                                         "control": "M", "scene": f"{v}:MC:{uid}", "question": COMPUTE[rel].format(x=x), **cap_item,
                                         "answer_in_passage": False, "memory_answer": key, "steps": [say_step, direct_c],
                                         "guess_question": COMPUTE_GUESS[rel].format(x=UNKNOWN[rel])})  # fmt: skip
                        # MC0 (amendment 63 addendum): the same question, steps and guess closed book (context ""), so its
                        # steps are H1's and C0's prompts; a word of this set (not the controls set) so that competence,
                        # v4_split's gate and the knock-out read it exactly as MC
                        mc["nc"].append({**b2, "id": f"j3:chat:{v}:MC0-w0-{uid}", "word": "MC0", "final": "M", "final_source": "M",
                                         "control": "M", "scene": f"{v}:MC0:{uid}", "question": COMPUTE[rel].format(x=x), **cap_item,
                                         "context": "", "capitals_in_passage": [], "answer_in_passage": False, "memory_answer": key, "steps": [say_step, direct_c],
                                         "guess_question": COMPUTE_GUESS[rel].format(x=UNKNOWN[rel])})  # fmt: skip
                        ctrl = {**b2, "context": "", "answer_in_passage": False, "steps": [], "guess_question": None, "memory_answer": key}
                        mc["ncctl"].append({**ctrl, "id": f"j3:chat:{v}:H1-w0-{uid}", "word": "H1", "final": "B", "final_source": "M",
                                            "control": "H1", "scene": f"{v}:H1:{uid}", "question": say_n, **cty_item})  # fmt: skip
                        mc["ncctl"].append({**ctrl, "id": f"j3:chat:{v}:C0-w0-{uid}", "word": "C0", "final": "M", "final_source": "M",
                                            "control": "C0", "scene": f"{v}:C0:{uid}", "question": direct_c["question"], **cap_item})  # fmt: skip
    ids = [it["id"] for xs in items.values() for it in xs]
    assert len(ids) == len(set(ids)), "duplicate ids"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    data = Path(a.data_dir)
    dirs = {tag: data / f"jsuite_{a.prefix}{tag.removesuffix('ctl')}{a.suffix}{'ctl' if tag.endswith('ctl') else ''}_test_chat" for tag in items}
    verified = set()  # --compute: sets already on disk, rebuilt in memory and checked byte for byte instead of rewritten
    if a.compute:
        for tag, d in dirs.items():
            if d.exists():
                body = "".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items[tag])
                h_new, h_disk = hashlib.sha256(body.encode()).hexdigest(), hashlib.sha256((d / "items.jsonl").read_bytes()).hexdigest()
                assert h_new == h_disk, f"{d.name}: the rebuild ({h_new}) differs from the file on disk ({h_disk})"
                print(f"{d.name}: rebuilt in memory, identical to the file on disk (sha256 {h_disk})")
                verified.add(tag)
    for tag, d in dirs.items():
        assert tag in verified or not d.exists(), f"{d} exists; sets are written once"
    for tag, d in dirs.items():
        if tag not in verified:
            d.mkdir(parents=True)
    common = {"seed": a.seed, "scenes": k, "git_commit": commit, "script": "scripts/jsuite_v5key.py", "reps": REPS,
              "skipped": dict(skipped), "excluded_entities": excluded, "colours": COLOURS, "countries": countries,
              "nationality_to_country": NAT2C, "country_aliases": aliases, "country_first_token_conflicts": conflict_pairs,
              "flag_colours": FLAG, "tokenizers": list(TOKENIZERS)}  # fmt: skip
    if a.split33:
        mp = [it for it in items["n"] if it["word"] == "MP"]
        common.update({"split33": True, "split_ok": dict(collections.Counter(str(it["split_ok"]) for it in mp)),
                       "other_continent": dict(sorted(collections.Counter(it["other_continent"] for it in mp).items()))})  # fmt: skip
    if a.same_continent or a.split33:  # the rebuild's additions (absent from the default build's manifest, which stays as it was)
        mp = [it for it in items["n"] if it["word"] == "MP"]
        common.update({"same_continent": a.same_continent or 2, "continent": CONTINENT, "region": REGION,
                       "n_same_continent": dict(sorted(collections.Counter(it["n_same_continent"] for it in mp).items())),
                       "scenes_short_of_same_continent": sum(it["n_same_continent"] < (a.same_continent or 2) for it in mp),
                       "scenes_without_same_region": sum(it["n_same_region"] == 0 for it in mp)})  # fmt: skip
    for tag, xs in items.items():
        if tag in verified:
            continue
        body = "".join(json.dumps(it, ensure_ascii=False) + "\n" for it in xs)
        (dirs[tag] / "items.jsonl").write_text(body)
        man = {"set": dirs[tag].name, "n": len(xs), **common, "words": dict(collections.Counter(it["word"] for it in xs)),
               "relations": dict(collections.Counter(it["relation"] for it in xs if it["word"] in ("MP", "H1"))),
               "items_sha256": hashlib.sha256(body.encode()).hexdigest()}  # fmt: skip
        (dirs[tag] / "manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
        print(f"{man['set']}: n={man['n']} words={man['words']} relations={man['relations']} sha256={man['items_sha256']}")
    print("scenes", k, "skipped", dict(skipped), "excluded", len(excluded))
    print("country first-token conflicts (never in one scene):", conflict_pairs)
    for tag in ("n", "d"):
        for wd in ("MP", "MM"):
            x = next(i for i in items[tag] if i["word"] == wd)
            print(f"--- {tag} {wd}: {x['question']} -> {x['answer']}")
    print(items["n"][0]["context"])
    if a.compute:  # note 35's two sets
        ids = [it["id"] for xs in mc.values() for it in xs]
        assert len(ids) == len(set(ids)), "duplicate ids"
        kn = {it["id"].rsplit("-", 1)[1] for it in items["n"]}
        assert all(it["id"].rsplit("-", 1)[1] in kn for it in mc["nc"]), "an MC item without a kn scene"
        cdirs = {tag: data / f"jsuite_{a.prefix}n{a.suffix}c{'ctl' if tag.endswith('ctl') else ''}_test_chat" for tag in mc}
        for d in cdirs.values():
            assert not d.exists(), f"{d} exists; sets are written once"
        rels = sorted({r for r, _ in mc_rel})
        ccommon = {**common, "compute": True, "pairs_with": dirs["n"].name, "capitals": CAPITAL, "capital_aliases": CAPITAL_ALIASES,
                   "capital_notes": CAPITAL_NOTE, "capital_first_token_conflicts": cap_conflict_pairs,
                   "mc_scenes": sum(it["word"] == "MC" for it in mc["nc"]), "mc_scenes_dropped": sum(v for (_, s), v in mc_rel.items() if s == "dropped"),
                   "mc_drop_reasons": dict(sorted(mc_drops.items())),
                   "mc_by_relation": {r: {s: mc_rel[(r, s)] for s in ("kept", "dropped")} for r in rels},
                   "capital_notes_items": dict(collections.Counter(str(it["capital_note"] is not None) for it in mc["nc"] if it["word"] == "MC")),
                   "capitals_in_passage_items": sum(bool(it["capitals_in_passage"]) for it in mc["nc"] if it["word"] == "MC")}  # fmt: skip
        for tag, xs in mc.items():
            cdirs[tag].mkdir(parents=True)
            body = "".join(json.dumps(it, ensure_ascii=False) + "\n" for it in xs)
            (cdirs[tag] / "items.jsonl").write_text(body)
            man = {"set": cdirs[tag].name, "n": len(xs), **ccommon, "words": dict(collections.Counter(it["word"] for it in xs)),
                   "relations": dict(collections.Counter(it["relation"] for it in xs if it["word"] in ("MC", "H1"))),
                   **({"mc0": "MC0: MC closed book (context ''), amendment 63 addendum"} if tag == "nc" else {}),
                   "items_sha256": hashlib.sha256(body.encode()).hexdigest()}  # fmt: skip
            (cdirs[tag] / "manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
            print(f"{man['set']}: n={man['n']} words={man['words']} relations={man['relations']} sha256={man['items_sha256']}")
        print("MC scenes kept", ccommon["mc_scenes"], "dropped", ccommon["mc_scenes_dropped"], "reasons (a scene can have several)",
              ccommon["mc_drop_reasons"], "by relation", ccommon["mc_by_relation"])  # fmt: skip
        print("capital first-token conflicts (a scene with both is dropped):", cap_conflict_pairs)
        for x in mc["nc"][:2]:
            print(f"--- {x['word']}: {x['question']} -> {x['answer']} among {x['answer_vocab']}; steps {[s['question'] for s in x['steps']]}; context {len(x['context'])} chars")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=5001)
    ap.add_argument("--prefix", default="v5k")
    ap.add_argument("--data-dir", default=str(DATA))
    ap.add_argument("--suffix", default="", help="after the set letter in set names and ids: 2 -> jsuite_v5kn2, j3:chat:v5kn2:...")
    ap.add_argument("--same-continent", type=int, default=0,
                    help="at least N of the five other countries from X's continent (as many as exist) and one from its region")
    ap.add_argument("--split33", action="store_true",
                    help="the six countries: three from X's continent (X + two, one from its region where possible) and three "
                         "from one other continent (random among those with >= 3 eligible); no continent has more than three")
    ap.add_argument("--compute", action="store_true",
                    help="note 35: also build jsuite_<prefix>n<suffix>c (MC, named) and its controls set (H1 C0) on the named "
                         "scenes; the four sets already on disk are checked byte for byte, not rewritten")
    main(ap.parse_args())
