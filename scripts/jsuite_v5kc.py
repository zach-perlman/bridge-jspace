"""jsuite_v5kc (Zach, 2026-10-29, prereg amendment 60 note 30): a true knowledge conflict.

Each scene: a passage of six attributed claims about six entities of one relation ("The club's notes say Achebe was
South African."), spliced into v4's filler. The bridge X's stated value is FALSE (a random other value of the relation's
answer vocabulary, never X's true value and never another value stated in the scene); the other five entities' stated
values are their TRUE values. Every scene also has a true-control passage: the same layout, filler and positions with
X's claim true. Every word's answer is X's TRUE value (memory); an answer is later labelled passage (X's false value),
memory (the true value) or other (scripts/nn_v5_read.py).
Words (one item each; the six share the scene and its id suffix):
  CN  conflict passage, plain question, X named          ("Which nationality was Achebe?")
  CA  conflict passage, "According to the passage, ...", X named
  DN  conflict passage, plain question, X described      ("Which nationality was the person who wrote Arrow of God?")
  DA  conflict passage, "According to the passage, ...", X described
  TN  true-control passage, plain question, X named
  TD  true-control passage, plain question, X described
Controls set (<name>ctl, read by competence_variants; same suffixes, no passage):
  H1  closed-book description -> entity ("Which person wrote Arrow of God?")
  H2  closed-book named recall ("Which nationality was Achebe?")
Steps (rendered with the item's passage): named words [the named plain question]; described words [description ->
entity (alts = bridge_alts), the named plain question]. Guess: the item's question about the relation's unnamed figure
(jsuite_v3_tables' "unknown").
Design (amendment 60 and the build brief, 29 Oct):
  - relations people (nationality), cities, companies, landmarks (country); films dropped; six entities per scene;
  - descriptions are v4's ("the {noun} who/that {clause}", noun "person" for people); v4's stem filter (X never shares a
    4-letter stem with its description; the other five share none with the description or X); fillers re-dealt while
    they share a stem with the description;
  - the cue check: a description is dropped if it names a country, nationality or place mapped to a country other
    than X's own. Base lexicon (from the tables): every answer and answer alias of the four relations and every city
    bridge (+ alts), each mapped to its country (nationalities through DEMONYM). Extended lexicon (orchestrator, before
    any data): PLACES below, ~200 hand-written country names, demonyms, cities, regions and landmark place-names, plus
    the landmark bridges (+ alts). Matching is a case-insensitive whole-word match (all-caps acronyms such as US, UK,
    USA, U.S. case-sensitive, so the pronoun "us" is not a cue). Kept descriptions record desc_has_own (names X's
    own country or nationality), desc_place_cue (the first own-country place matched, else null) and desc_cues;
  - two scenes per kept (X, description) pair (rep 0 and 1: other distractors, false value, filler and position);
  - the other five entities have distinct true values, none equal to X's true value (so X's true value is absent from
    the conflict passage and the passage's six values are distinct);
  - X's claim rotated through the six positions per (relation, rep), as v4;
  - two plural landmarks (the Petronas Towers, the Nazca Lines) take "stand" / "do ... stand" for agreement.
Fields are v4's with the same meanings, plus set_kind "kc", false_value (None on T words), frame, named, true_control,
entity_reals, desc_has_own, desc_place_cue, desc_cues. Differences from v4: "scene" is shared by every word of a scene
("v5kc:<suffix>", so ablate_v2 --tasks-scene-words can keep a scene by its T words); "start" is "M" for described
words and "N" for named ones; final "M" / final_source "M" (the answer is the remembered value); control "C" on the
conflict words, "K" on the true-control words. Control items carry their scene's fields (passage_values, false_value)
though their context is empty, as v4's.

--variant kc2 (Zach approved after a red-team, 29 Oct; a new set, jsuite_v5kc2, ids "j3:chat:v5kc2:...", seed 5102;
the default variant kc is unchanged and rebuilds jsuite_v5kc byte for byte):
  1. companies: "The club's notes say <E> was founded in <country>." / "Which country was <E> founded in?" (every
     company's table country checked as its founding country; none dropped; borderline cases are in FOUNDED_NOTES);
  2. X's false value is drawn first, from the values on the same continent as X's true value (CONTINENT; people
     through DEMONYM), falling back to any other value when the vocabulary has none ("false_same_continent" false);
     the other five entities then avoid both X's true and false values;
  3. the cue check also drops descriptions with a non-place cue to another country: REDTEAM_CUES, the red-team's list
     (scratch/redteam_items/a_lex.py EXTRA, copied here) without "Nobel" (international) and its null "World Cup";
     desc_cues lists every cue matched, desc_own_cue whether any of them is X's own country's;
  4. set_variant "kc2" and false_same_continent (None on T words) on every item; everything else as kc.

python scripts/jsuite_v5kc.py [--variant kc] [--seed 5101] [--name jsuite_v5kc]
    -> data/tasks_v2/jsuite_v5kc_test_chat (CN CA DN DA TN TD) and data/tasks_v2/jsuite_v5kcctl_test_chat (H1 H2)
python scripts/jsuite_v5kc.py --variant kc2   (seed 5102, name jsuite_v5kc2)
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
import jsuite_v3 as V3  # noqa: E402
import jsuite_v3_tables as T3  # noqa: E402
import jsuite_v4 as V4  # noqa: E402

DATA = ROOT / "data" / "tasks_v2"
K = 6  # entities per scene
N_FILLER = 6
RELS = ("people", "cities", "companies", "landmarks")
REPS = 2
CLAIM = {"people": "The club's notes say {e} was {a}.", "cities": "The club's notes say {e} is in {a}.",
         "companies": "The club's notes say {e} is based in {a}.", "landmarks": "The club's notes say {e} stands in {a}."}  # fmt: skip
QUESTION = {"people": "Which nationality was {d}?", "cities": "Which country is {d} in?",
            "companies": "Which country is {d} based in?", "landmarks": "Which country does {d} stand in?"}  # fmt: skip
CLAIM_KC2 = {**CLAIM, "companies": "The club's notes say {e} was founded in {a}."}
QUESTION_KC2 = {**QUESTION, "companies": "Which country was {d} founded in?"}
# kc2's companies: the table's country is each company's founding country (checked by hand, 29 Oct). Borderline, kept:
FOUNDED_NOTES = {
    "Red Bull": "Red Bull GmbH was founded in Austria (1984, Mateschitz with a Thai partner); the drink adapts Thailand's Krating Daeng",
    "Samsung": "founded 1938 in Daegu, Korea under Japanese rule (present-day South Korea)",
    "Hyundai": "founded 1947 in Seoul, before the South Korean state (1948)",
    "Nokia": "founded 1865 in the Grand Duchy of Finland (Russian Empire)",
    "Tata": "founded 1868 in Bombay, British India",
    "Gazprom": "formed 1989 from the Soviet gas ministry in Moscow; a Russian joint-stock company from 1993",
    "Corona": "a brand of Grupo Modelo, founded 1925 in Mexico City (now owned by AB InBev)",
}  # fmt: skip
CONTINENT = {  # every country in the four vocabularies (people: their DEMONYM country); Turkey as Asia (UN geoscheme)
    **{c: "Europe" for c in ("United Kingdom", "Ireland", "France", "Germany", "Italy", "Spain", "Portugal", "Netherlands",
                             "Belgium", "Denmark", "Sweden", "Norway", "Finland", "Poland", "Czech Republic", "Austria",
                             "Hungary", "Greece", "Russia")},
    **{c: "Asia" for c in ("China", "Japan", "South Korea", "Taiwan", "India", "Thailand", "Vietnam", "Cambodia", "Malaysia",
                           "Indonesia", "Israel", "Jordan", "Turkey")},
    **{c: "Africa" for c in ("Egypt", "Morocco", "Nigeria", "Kenya", "South Africa", "Tanzania")},
    **{c: "North America" for c in ("United States", "Canada", "Mexico", "Jamaica")},
    **{c: "South America" for c in ("Argentina", "Brazil", "Chile", "Colombia", "Peru", "Venezuela")},
    "Australia": "Oceania",
}  # fmt: skip
# the red-team's extra cues (scratch/redteam_items/a_lex.py, EXTRA, 29 Oct), copied; "Nobel" left out (international)
REDTEAM_CUES = {
    "Tokyo": "Japan", "Osaka": "Japan", "Seoul": "South Korea", "Delhi": "India", "New Delhi": "India", "Calcutta": "India",
    "Kolkata": "India", "Bengal": "India", "Bengali": "India", "Cairo": "Egypt", "Nile": "Egypt", "Pharaoh": "Egypt",
    "Lagos": "Nigeria", "Mecca": "Saudi Arabia", "Toronto": "Canada", "Quebec": "Canada", "Ottawa": "Canada", "NHL": "Canada",
    "Mexico City": "Mexico", "Aztec": "Mexico", "Maya": "Mexico", "Mayan": "Mexico", "Inca": "Peru", "Cuzco": "Peru",
    "Cusco": "Peru", "Santiago": "Chile", "Bogota": "Colombia", "Escobar": "Colombia", "Caracas": "Venezuela",
    "Havana": "Cuba", "Canberra": "Australia", "Melbourne": "Australia", "Wellington": "New Zealand", "Beijing": "China",
    "Peking": "China", "Hong Kong": "China", "Taipei": "Taiwan", "Hollywood": "United States", "Disney": "United States",
    "Harvard": "United States", "Facebook": "United States", "FBI": "United States", "Confederate": "United States",
    "Washington": "United States", "Academy Award": "United States", "Academy Awards": "United States",
    "Oscar": "United States", "Humphrey Bogart": "United States", "Indiana Jones": "United States",
    "iPhone": "United States", "iPhones": "United States", "Premier League": "United Kingdom",
    "Jaguar Land Rover": "United Kingdom", "King William IV": "United Kingdom", "Allied": "United Kingdom",
    "Sight and Sound": "United Kingdom", "Byzantine": "Turkey", "Ottoman": "Turkey", "Ballon d'Or": "France",
    "Palme d'Or": "France", "Interpol": "France", "Catholic": "Vatican City", "Pope": "Vatican City", "Inquisition": "Spain",
    "Columbus": "Italy", "Pizarro": "Spain", "Alexander the Great": "Greece", "Eureka": "Greece", "Herod": "Israel",
    "Muslim": "Saudi Arabia", "Kafka": "Czech Republic", "Hiram Bingham": "United States", "Ulysses": "Greece",
    "Hamlet": "Denmark", "Carmen": "Spain", "Magic Flute": "Austria", "Sound of Music": "Austria",
    "Truth and Reconciliation": "South Africa", "Salt March": "India", "Analects": "China", "Kong": "United States",
    "Tintin": "Belgium", "Tango": "Argentina", "mariachi": "Mexico", "Galaxy": "South Korea", "Vishnu": "India",
    "Buddha": "India", "Buddhist": "India",
}  # fmt: skip
PLURAL_X = {"the Petronas Towers", "the Nazca Lines"}  # landmark names that take a plural verb
ACCORDING = "According to the passage, "

DEMONYM = {"American": "United States", "Argentine": "Argentina", "Australian": "Australia", "Austrian": "Austria",
           "Belgian": "Belgium", "Brazilian": "Brazil", "Canadian": "Canada", "Chilean": "Chile", "Chinese": "China",
           "Colombian": "Colombia", "Czech": "Czech Republic", "Danish": "Denmark", "Dutch": "Netherlands",
           "Egyptian": "Egypt", "English": "United Kingdom", "French": "France", "German": "Germany", "Greek": "Greece",
           "Hungarian": "Hungary", "Indian": "India", "Irish": "Ireland", "Italian": "Italy", "Jamaican": "Jamaica",
           "Japanese": "Japan", "Kenyan": "Kenya", "Mexican": "Mexico", "Nigerian": "Nigeria", "Norwegian": "Norway",
           "Polish": "Poland", "Portuguese": "Portugal", "Russian": "Russia", "South African": "South Africa",
           "Spanish": "Spain", "Swedish": "Sweden"}  # fmt: skip  # the people answers' countries
ALIAS_COUNTRY = {"British": "United Kingdom", "Argentinian": "Argentina", "US": "United States", "Netherlands": "Netherlands",
                 "Korea": "South Korea", "the Republic of Ireland": "Ireland"}  # fmt: skip  # aliases not named by their answer

# the extended cue lexicon (orchestrator, 29 Oct, before any data): place -> country. Kind "name" = a country name or
# demonym (counts toward desc_has_own when it is X's own), "place" = a city, region or landmark place-name
# (desc_place_cue). Ambiguous common words (Nice, Bath, Reading, Cork, Java, Split, Victoria, Georgia) are left out.
NAMES = {
    "Nigeria": "Nigeria", "Jamaica": "Jamaica", "England": "United Kingdom", "Britain": "United Kingdom",
    "United Kingdom": "United Kingdom", "UK": "United Kingdom", "Scotland": "United Kingdom", "Scottish": "United Kingdom",
    "Wales": "United Kingdom", "Welsh": "United Kingdom", "Switzerland": "Switzerland", "Swiss": "Switzerland",
    "New Zealand": "New Zealand", "Iran": "Iran", "Persia": "Iran", "Persian": "Iran", "Iraq": "Iraq",
    "North Korea": "North Korea", "Korean": "South Korea", "Thai": "Thailand", "Turkish": "Turkey", "Moroccan": "Morocco",
    "Peruvian": "Peru", "Finnish": "Finland", "Taiwanese": "Taiwan", "Cambodian": "Cambodia", "Israeli": "Israel",
    "Jordanian": "Jordan", "Malaysian": "Malaysia", "Vietnamese": "Vietnam", "Indonesian": "Indonesia",
    "Tanzanian": "Tanzania", "Venezuelan": "Venezuela", "Soviet": "Russia", "USSR": "Russia", "Ethiopia": "Ethiopia",
    "Ethiopian": "Ethiopia", "Ghana": "Ghana", "Cuba": "Cuba", "Cuban": "Cuba", "Saudi Arabia": "Saudi Arabia",
    "Pakistan": "Pakistan", "Philippines": "Philippines", "Singapore": "Singapore", "Ukraine": "Ukraine",
    "Ukrainian": "Ukraine", "Romania": "Romania", "Iceland": "Iceland", "Croatia": "Croatia", "Serbia": "Serbia",
    "USA": "United States", "U.S.": "United States", "America": "United States", "Holland": "Netherlands",
    "Czechia": "Czech Republic",
}  # fmt: skip
PLACES = {
    # United Kingdom, Ireland
    "London": "United Kingdom", "Oxford": "United Kingdom", "Cambridge": "United Kingdom", "Manchester": "United Kingdom",
    "Liverpool": "United Kingdom", "Edinburgh": "United Kingdom", "Glasgow": "United Kingdom", "Belfast": "United Kingdom",
    "Westminster": "United Kingdom", "Wimbledon": "United Kingdom", "Stratford-upon-Avon": "United Kingdom",
    "Birmingham": "United Kingdom", "Bristol": "United Kingdom", "Galway": "Ireland",
    # France
    "Paris": "France", "Parisian": "France", "Bordeaux": "France", "Versailles": "France", "Normandy": "France",
    "Provence": "France", "Brittany": "France", "Burgundy": "France", "Toulouse": "France", "Strasbourg": "France",
    "Montmartre": "France", "Giverny": "France", "Arles": "France", "Cannes": "France",
    # Germany, Austria, Switzerland
    "Berlin": "Germany", "Hamburg": "Germany", "Frankfurt": "Germany", "Cologne": "Germany", "Bonn": "Germany",
    "Leipzig": "Germany", "Bavaria": "Germany", "Bavarian": "Germany", "Prussia": "Germany", "Prussian": "Germany",
    "Weimar": "Germany", "Stuttgart": "Germany", "Nuremberg": "Germany", "Heidelberg": "Germany", "Bayreuth": "Germany",
    "Innsbruck": "Austria", "Tyrol": "Austria", "Viennese": "Austria", "Geneva": "Switzerland", "Zurich": "Switzerland",
    "Basel": "Switzerland", "Bern": "Switzerland", "Davos": "Switzerland",
    # Italy, Vatican
    "Rome": "Italy", "Roman": "Italy", "Romans": "Italy", "Milan": "Italy", "Florence": "Italy", "Florentine": "Italy",
    "Venetian": "Italy", "Naples": "Italy", "Pisa": "Italy", "Bologna": "Italy", "Genoa": "Italy", "Verona": "Italy",
    "Sicily": "Italy", "Sardinia": "Italy", "Tuscany": "Italy", "Pompeii": "Italy", "Vatican": "Vatican City",
    # Spain, Portugal
    "Madrid": "Spain", "Granada": "Spain", "Valencia": "Spain", "Bilbao": "Spain", "Catalonia": "Spain",
    "Andalusia": "Spain", "Pamplona": "Spain", "Ibiza": "Spain", "Malaga": "Spain", "Algarve": "Portugal",
    # Low Countries, Nordics
    "Hague": "Netherlands", "Delft": "Netherlands", "Utrecht": "Netherlands", "Haarlem": "Netherlands",
    "Brussels": "Belgium", "Antwerp": "Belgium", "Ghent": "Belgium", "Flanders": "Belgium", "Waterloo": "Belgium",
    "Bergen": "Norway", "Uppsala": "Sweden", "Gothenburg": "Sweden", "Odense": "Denmark",
    # Central and Eastern Europe, Greece, Russia, Turkey
    "Krakow": "Poland", "Gdansk": "Poland", "Auschwitz": "Poland", "Bohemia": "Czech Republic",
    "Moravia": "Czech Republic", "Brno": "Czech Republic", "Sparta": "Greece", "Crete": "Greece", "Delphi": "Greece",
    "Olympia": "Greece", "Athenian": "Greece", "Siberia": "Russia", "Kremlin": "Russia", "Petrograd": "Russia",
    "Leningrad": "Russia", "Stalingrad": "Russia", "Volga": "Russia", "Constantinople": "Turkey", "Ankara": "Turkey",
    "Anatolia": "Turkey", "Byzantium": "Turkey", "Ottoman": "Turkey",
    # Africa
    "Cairo": "Egypt", "Giza": "Egypt", "Luxor": "Egypt", "Nile": "Egypt", "Sinai": "Egypt", "Marrakesh": "Morocco",
    "Fez": "Morocco", "Lagos": "Nigeria", "Abuja": "Nigeria", "Mombasa": "Kenya", "Cape Town": "South Africa",
    "Soweto": "South Africa", "Durban": "South Africa", "Pretoria": "South Africa", "Robben Island": "South Africa",
    "Zanzibar": "Tanzania", "Serengeti": "Tanzania", "Dar es Salaam": "Tanzania", "Addis Ababa": "Ethiopia",
    # South and East Asia
    "Delhi": "India", "New Delhi": "India", "Bombay": "India", "Calcutta": "India", "Kolkata": "India", "Bengal": "India",
    "Punjab": "India", "Kashmir": "India", "Goa": "India", "Agra": "India", "Varanasi": "India", "Ganges": "India",
    "Madras": "India", "Chennai": "India", "Bangalore": "India", "Kerala": "India", "Bollywood": "India", "Mughal": "India",
    "Peking": "China", "Hong Kong": "China", "Tibet": "China", "Canton": "China", "Guangzhou": "China",
    "Shenzhen": "China", "Yangtze": "China", "Tiananmen": "China", "Nanjing": "China", "Wuhan": "China",
    "Taipei": "Taiwan", "Tokyo": "Japan", "Osaka": "Japan", "Nagasaki": "Japan", "Edo": "Japan", "Hokkaido": "Japan",
    "Okinawa": "Japan", "Yokohama": "Japan", "Kobe": "Japan", "Fuji": "Japan", "Seoul": "South Korea",
    "Busan": "South Korea", "Pyongyang": "North Korea", "Siam": "Thailand", "Phuket": "Thailand",
    "Chiang Mai": "Thailand", "Hanoi": "Vietnam", "Saigon": "Vietnam", "Phnom Penh": "Cambodia", "Angkor": "Cambodia",
    "Jakarta": "Indonesia", "Bali": "Indonesia", "Sumatra": "Indonesia", "Kuala Lumpur": "Malaysia",
    # Middle East
    "Jerusalem": "Israel", "Tel Aviv": "Israel", "Galilee": "Israel", "Nazareth": "Israel", "Amman": "Jordan",
    "Tehran": "Iran", "Baghdad": "Iraq", "Babylon": "Iraq", "Mesopotamia": "Iraq",
    # Oceania
    "Melbourne": "Australia", "Brisbane": "Australia", "Perth": "Australia", "Canberra": "Australia",
    "Tasmania": "Australia", "Queensland": "Australia", "Outback": "Australia", "Auckland": "New Zealand",
    # North America
    "New York": "United States", "Manhattan": "United States", "Brooklyn": "United States", "Harlem": "United States",
    "Hollywood": "United States", "Broadway": "United States", "Wall Street": "United States",
    "Silicon Valley": "United States", "Los Angeles": "United States", "San Francisco": "United States",
    "Boston": "United States", "Philadelphia": "United States", "Washington": "United States", "Detroit": "United States",
    "Seattle": "United States", "New Orleans": "United States", "Nashville": "United States", "Memphis": "United States",
    "Miami": "United States", "Texas": "United States", "California": "United States", "Florida": "United States",
    "Alaska": "United States", "Hawaii": "United States", "Pearl Harbor": "United States",
    "Mississippi": "United States", "Gettysburg": "United States", "Toronto": "Canada", "Ottawa": "Canada",
    "Quebec": "Canada", "Ontario": "Canada", "Alberta": "Canada", "Calgary": "Canada", "Oaxaca": "Mexico",
    "Yucatan": "Mexico", "Acapulco": "Mexico", "Tijuana": "Mexico", "Aztec": "Mexico", "Havana": "Cuba",
    # South America
    "Rio": "Brazil", "Bahia": "Brazil", "Brasilia": "Brazil", "Copacabana": "Brazil", "Patagonia": "Argentina",
    "Pampas": "Argentina", "Valparaiso": "Chile", "Atacama": "Chile", "Cusco": "Peru", "Cuzco": "Peru", "Inca": "Peru",
    "Incan": "Peru", "Bogota": "Colombia", "Caracas": "Venezuela",
}  # fmt: skip


def term_re(term: str) -> re.Pattern:
    """A whole-word match: case-insensitive, except all-caps acronyms (US, UK, USA, U.S.), so 'us' is not a cue."""
    flags = 0 if re.sub(r"[^A-Za-z]", "", term).isupper() else re.I
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", flags)


def count(text: str, term: str) -> int:
    return len(term_re(term).findall(text))


def lexicons(table: list[dict]) -> tuple[dict, dict]:
    """(base, extended): term -> (country, kind) with kind 'name' (a country or nationality) or 'place'."""
    base: dict[str, tuple[str, str]] = {}

    def add(lex: dict, term: str, country: str, kind: str) -> None:
        term = term[4:] if term.startswith("the ") else term
        assert lex.get(term, (country, kind))[0] == country, (term, lex[term], country)
        lex.setdefault(term, (country, kind))

    for r in table:
        if r["relation"] not in RELS:
            continue
        country = DEMONYM[r["answer"]] if r["relation"] == "people" else r["answer"]
        add(base, r["answer"], country, "name")
        for al in r["answer_aliases"]:
            add(base, al, ALIAS_COUNTRY.get(al, country), "name")
        if r["relation"] == "cities":
            for b in [r["bridge"], *r.get("bridge_alts", [])]:
                add(base, b, country, "place")
    ext = dict(base)
    for term, c in NAMES.items():
        add(ext, term, c, "name")
    for term, c in PLACES.items():
        add(ext, term, c, "place")
    for r in table:
        if r["relation"] == "landmarks":
            for b in [r["bridge"], *r.get("bridge_alts", [])]:
                add(ext, b, r["answer"], "place")
    return base, ext


def redteam_lexicon(ext: dict) -> dict:
    """kc2: the extended lexicon plus REDTEAM_CUES (kind 'cue'; a term already present keeps its entry)."""
    full = dict(ext)
    for term, c in REDTEAM_CUES.items():
        assert full.get(term, (c, "cue"))[0] == c, (term, full[term], c)
        full.setdefault(term, (c, "cue"))
    return full


def cues(text: str, lex: dict) -> list[tuple[str, str, str]]:
    """Every lexicon term in the text: (term, country, kind), in text order."""
    hits = []
    for term, (c, kind) in lex.items():
        m = term_re(term).search(text)
        if m:
            hits.append((m.start(), term, c, kind))
    return [(t, c, k) for _, t, c, k in sorted(hits)]


def lower1(q: str) -> str:
    return q[0].lower() + q[1:]


def question(rel: str, d: str, plural: bool, tpl: dict = QUESTION) -> str:
    q = tpl[rel].format(d=d)
    return q.replace("Which country does ", "Which country do ", 1) if plural else q


def claim(rel: str, e: str, a: str, tpl: dict = CLAIM) -> str:
    s = tpl[rel].format(e=e, a=V3.disp(a))
    return s.replace(" stands in ", " stand in ", 1) if e in PLURAL_X else s


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(a) -> None:
    kc2 = a.variant == "kc2"
    tag = "v5kc2" if kc2 else "v5kc"
    CL, QU = (CLAIM_KC2, QUESTION_KC2) if kc2 else (CLAIM, QUESTION)
    rng = random.Random(a.seed)
    tabs = T3.tables()
    table = json.loads((ROOT / "data" / "v3_bridges.json").read_text())
    alias_of = {r["answer"]: r.get("answer_aliases") or [] for r in table}
    rows = {(r["relation"], r["bridge"]): r for r in table}
    base_lex, ext_lex = lexicons(table)
    lex = redteam_lexicon(ext_lex) if kc2 else ext_lex
    # v4's filler: the same banned words, the same deck
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731
    banned = {strip(b) for t in tabs.values() for b in t["facts"]} | {v[0] for t in tabs.values() for v in t["facts"].values()}
    banned |= {al for t in tabs.values() for r in t["meta"].values() for al in r["answer_aliases"]}
    banned |= {w for n in V3.NP.PEOPLE_NAMES + V3.N.ABSENT_NAMES for w in n.split()}
    banned |= {w for xs in V3.CONT.values() for w in xs}
    banned |= {"Olympic", "Olympics", "continent", "nationality", "director", "film", "films", "company", "landmark", "list",
               "handout", "festival", "tour", "podcast", "exhibition", "delegation", "supplier", "adaptation", "biopic", "actor",
               "journalist", "twin", "twinning", "studio", "documentary", "office"}  # fmt: skip
    deck = V3.Deck(rng, V3.JF.clean_paras(banned))
    items, skipped = [], collections.Counter()
    desc_log = []  # every (X, description) pair and the filter that dropped it, if any
    k = 0
    for rel in RELS:
        t = tabs[rel]
        noun = "person" if rel == "people" else t["noun"]
        vocab = sorted({v[0] for v in t["facts"].values()})
        real = {b: t["facts"][b][0] for b in t["facts"]}
        cty = (lambda v: DEMONYM[v]) if rel == "people" else (lambda v: v)  # noqa: E731
        assert all(cty(v) in CONTINENT for v in vocab), rel
        bridges = sorted(b for (r, b) in rows if r == rel)
        desc_of = {b: [f"the {noun} {V4.PRON[rel]} {d['clause']}" for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        clause_of = {b: [d["clause"] for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        pos_counter = collections.Counter()
        for x in bridges:
            real_x = real[x]
            own = DEMONYM[real_x] if rel == "people" else real_x
            for di, clause in enumerate(clause_of[x]):
                desc = desc_of[x][di]
                rec = {"relation": rel, "bridge": x, "real": real_x, "desc": desc, "dropped": None, "cues": []}
                desc_log.append(rec)
                if V4.stems(clause) & V4.stems(x):
                    skipped["X shares a stem with its description"] += 1
                    rec["dropped"] = "stem"
                    continue
                hits = cues(clause, lex)
                rec["cues"] = [[tm, c, kd, tm in base_lex] for tm, c, kd in hits]
                other_base = [h for h in hits if h[1] != own and h[0] in base_lex]
                other_ext = [h for h in hits if h[1] != own and h[0] in ext_lex]
                other_rt = [h for h in hits if h[1] != own]
                if other_base:
                    skipped["description names another country (base lexicon)"] += 1
                    rec["dropped"] = "cue_base"
                    continue
                if other_ext:
                    skipped["description names another country (extended lexicon only)"] += 1
                    rec["dropped"] = "cue_extended"
                    continue
                if other_rt:
                    skipped["description has a non-place cue to another country (red-team list only)"] += 1
                    rec["dropped"] = "cue_redteam"
                    continue
                has_own = any(kd == "name" for _, _, kd in hits)
                place_cue = next((tm for tm, _, kd in hits if kd == "place"), None)
                for rep in range(REPS):
                    false_same = None
                    if kc2:  # the false value first, from X's continent; the others then avoid it
                        same = [v for v in vocab if v != real_x and CONTINENT[cty(v)] == CONTINENT[own]]
                        false = rng.choice(same or [v for v in vocab if v != real_x])
                        false_same = bool(same)
                        excl = {real_x, false}
                    else:
                        excl = {real_x}
                    ok = [b for b in bridges if b != x and real[b] not in excl and not (V4.stems(clause) & V4.stems(b))
                          and not (V4.stems(x) & V4.stems(b))]  # fmt: skip
                    others = None
                    for _ in range(500):  # five others with distinct true values, none X's (kc2: nor X's false value)
                        cand = rng.sample(ok, K - 1)
                        if len({real[b] for b in cand}) == K - 1:
                            others = cand
                            break
                    if others is None:
                        skipped["no distractor draw"] += 1
                        continue
                    taken = {real[b] for b in others}
                    if not kc2:
                        false = rng.choice([v for v in vocab if v != real_x and v not in taken])
                    assert false != real_x and false not in taken
                    for _ in range(50):  # filler free of description words
                        para = deck.deal(N_FILLER)
                        if not (V4.stems(" ".join(para)) & V4.stems(clause)):
                            break
                    else:
                        skipped["filler leak"] += 1
                        continue
                    pos = pos_counter[(rel, rep)] % K  # X's claim rotated through the six positions
                    pos_counter[(rel, rep)] += 1
                    order = others[:]
                    rng.shuffle(order)
                    order.insert(pos, x)
                    genre = rng.choice(sorted(V3.N.GENRES))
                    lay_seed = rng.random()  # the layout, shared by the conflict and the true-control passage
                    vals_c = {e: (false if e == x else real[e]) for e in order}
                    vals_t = {e: real[e] for e in order}
                    ctx_c = V4.splice(random.Random(lay_seed), genre, [claim(rel, e, vals_c[e], CL) for e in order], para)
                    ctx_t = V4.splice(random.Random(lay_seed), genre, [claim(rel, e, vals_t[e], CL) for e in order], para)
                    # checks: each entity once; X's true value (and aliases) absent from the conflict passage; the false
                    # value once; the true control differs only in X's claim
                    assert all(count(ctx_c, e) == 1 for e in order), (x, ctx_c)
                    assert count(ctx_c, real_x) == 0 and not any(count(ctx_c, al) for al in alias_of[real_x]), (x, ctx_c)
                    assert count(ctx_c, false) == 1 and count(ctx_t, false) == 0 and count(ctx_t, real_x) == 1, (x, false)
                    assert ctx_t == ctx_c.replace(claim(rel, x, false, CL), claim(rel, x, real_x, CL)), x
                    assert ctx_c.count(claim(rel, x, false, CL)) == 1
                    plural = x in PLURAL_X
                    q_named = question(rel, x, plural, QU)
                    q_desc = question(rel, desc, False, QU)
                    q_guess = question(rel, t["unknown"], False, QU)
                    q1 = t["q1M"][1].format(noun=noun, rel=clause)
                    alts = sorted({x, *rows[(rel, x)].get("bridge_alts", [])})
                    uid = f"{k:05d}"
                    base = {"module": "facts", "start": "M", "domain": rel, "relation": rel, "format": "prose", "genre": genre,
                            "framing": "chat", "wording": 0, "rep": rep, "level": 2, "split": "test", "popularity": t["facts"][x][2],
                            "half": "A", "context": ctx_c, "kind": "open", "answer_kind": "open", "answer_vocab": vocab,
                            "bridge": x, "bridges": [x], "start_desc": desc, "desc_index": di, "skip_cue": None, "real": real_x,
                            "entities": order, "entity_reals": vals_t, "passage_values": vals_c, "bridge_position": pos,
                            "eponymous": False, "name_reveals_answer": rows[(rel, x)].get("name_reveals_answer", False),
                            "bridge_in_passage": True, "bridge_mentions": 1, "entity_descs": {e: desc_of[e] for e in order},
                            "knobs": {"entities": K, "filler": N_FILLER}, "set_version": "v4", "set_kind": "kc",
                            "false_value": false, "frame": "plain", "named": False, "true_control": False,
                            "desc_has_own": has_own, "desc_place_cue": place_cue, "desc_cues": [h[0] for h in hits],
                            "scene": f"{tag}:{uid}", "final": "M", "final_source": "M", "answer": real_x,
                            "answer_aliases": alias_of.get(real_x, []), "memory_answer": real_x}  # fmt: skip
                    if kc2:
                        base.update({"set_variant": "kc2", "false_same_continent": false_same,
                                     "desc_own_cue": any(c == own for _, c, _ in hits)})  # fmt: skip
                    hop1 = {"question": q1, "answer": x, "kind": "open", "source": "M", "alts": alts}
                    step_named = {"question": q_named, "answer": real_x, "kind": "open", "source": "M", "cand_vocab": vocab}
                    for word in ("CN", "CA", "DN", "DA", "TN", "TD"):
                        named = word in ("CN", "CA", "TN")
                        according = word in ("CA", "DA")
                        tc = word[0] == "T"
                        q = q_named if named else q_desc
                        g = q_guess
                        if according:
                            q, g = ACCORDING + lower1(q), ACCORDING + lower1(g)
                        items.append({**base, "id": f"j3:chat:{tag}:{word}-w0-{uid}", "word": word, "start": "N" if named else "M",
                                      "control": "K" if tc else "C", "context": ctx_t if tc else ctx_c,
                                      "passage_values": vals_t if tc else vals_c, "false_value": None if tc else false,
                                      "frame": "according" if according else "plain", "named": named, "true_control": tc,
                                      "start_desc": x if named else desc, "question": q, "answer_in_passage": tc,
                                      "steps": [step_named] if named else [hop1, step_named], "guess_question": g,
                                      **({"false_same_continent": None if tc else false_same} if kc2 else {})})  # fmt: skip
                    ctrl = {**base, "context": "", "answer_in_passage": False, "steps": [], "guess_question": None}
                    items.append({**ctrl, "id": f"j3:chat:{tag}:H1-w0-{uid}", "word": "H1", "final": "B", "final_source": "M",
                                  "control": "H1", "question": q1, "answer": x, "answer_aliases": alts, "answer_vocab": bridges})  # fmt: skip
                    items.append({**ctrl, "id": f"j3:chat:{tag}:H2-w0-{uid}", "word": "H2", "start": "N", "control": "H2",
                                  "named": True, "start_desc": x, "question": q_named})  # fmt: skip
                    k += 1
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    main_words = ("CN", "CA", "DN", "DA", "TN", "TD")
    out = Path(a.data) / f"{a.name}_test_chat"
    ctl = Path(a.data) / f"{a.name}ctl_test_chat"
    for d in (out, ctl):
        assert not d.exists(), f"{d} exists; sets are written once"
        d.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] in main_words))
    (ctl / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] not in main_words))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "scripts/jsuite_v5kc.py"], capture_output=True, text=True,
                           cwd=ROOT).stdout.strip()  # fmt: skip
    drops = collections.Counter((r["relation"], r["dropped"]) for r in desc_log)
    cn = [it for it in items if it["word"] == "CN"]
    man = {"set": out.name, "ctl_set": ctl.name, "variant": a.variant, "id_tag": tag, "seed": a.seed, "reps": REPS,
           "n": len(items), "scenes": k, "git_commit": commit, "script": "scripts/jsuite_v5kc.py",
           "script_uncommitted": bool(dirty), "script_sha256": sha256(Path(__file__)),
           "words": dict(collections.Counter(it["word"] for it in items)), "skipped": dict(skipped),
           "relations": dict(collections.Counter(it["relation"] for it in cn)),
           "descriptions": {f"{r}:{d}": n for (r, d), n in sorted(drops.items(), key=str)},
           "dropped_descriptions": [{k2: r[k2] for k2 in ("relation", "bridge", "desc", "dropped", "cues")}
                                    for r in desc_log if r["dropped"] in ("cue_base", "cue_extended", "cue_redteam")],
           "lexicon_sizes": {"base": len(base_lex), "extended": len(ext_lex), "used": len(lex)},
           "sha256": {out.name: sha256(out / "items.jsonl"), ctl.name: sha256(ctl / "items.jsonl")}}  # fmt: skip
    if kc2:
        man["false_same_continent"] = {r: dict(collections.Counter(it["false_same_continent"] for it in cn if it["relation"] == r))
                                       for r in RELS}  # fmt: skip
        man["founded_notes"] = FOUNDED_NOTES
    (out / "manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    (ctl / "manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k2: v for k2, v in man.items() if k2 != "dropped_descriptions"}, indent=1, ensure_ascii=False))
    for nm, h in man["sha256"].items():
        print(f"sha256 {nm}/items.jsonl {h}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variant", choices=("kc", "kc2"), default="kc", help="kc: jsuite_v5kc as first built; kc2: the rebuild")
    ap.add_argument("--seed", type=int, default=None, help="default 5101 (kc), 5102 (kc2)")
    ap.add_argument("--name", default=None, help="default jsuite_v5kc (kc), jsuite_v5kc2 (kc2)")
    ap.add_argument("--data", default=str(DATA), help="output root (default data/tasks_v2; a scratch dir for dry runs)")
    args = ap.parse_args()
    args.seed = args.seed if args.seed is not None else {"kc": 5101, "kc2": 5102}[args.variant]
    args.name = args.name or {"kc": "jsuite_v5kc", "kc2": "jsuite_v5kc2"}[args.variant]
    main(args)
