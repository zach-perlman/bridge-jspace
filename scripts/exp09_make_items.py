"""Items for exp09_bind_recall: one two-hop question whose bridge country is recalled (R) or bound in context (B).

  exp09_make_items.py [--per-city N] [--n-bound N] [--seed S]  -> data/bind_recall.json (write-once; pin its sha256)
  exp09_make_items.py --lookup N [--seed S]  -> data/bind_lookup.json: family L (write-once; pin its sha256)
  exp09_make_items.py --lookup N --seed S --lookup-version 2  -> data/bind_lookup_v2.json: L asked "... has the colour"
  exp09_make_items.py --recall-lookup N [--seed S]  -> data/recall_lookup.json: family RL, N items per city
  exp09_make_items.py --use-source N --seed S  -> data/use_source.json: families LM, RM, BT, RT (Phase 3), N items
                                                  each for the bound ones, 12 per city for the recalled ones

Both families share the format, the countries (the 13 with exp01 probes) and the second hop (the country's capital).
Three people and three countries come first; every prompt names the bridge I, the target X and a third country Z:
  R  "{P1} lives in {.}. {P2} lives in {.}. {P3} lives in {.}. The capital of the country where {city} is located is"
     the bridge is recalled from the city; I, X and Z are context only
  B  "{P1} lives in {.}. {P2} lives in {.}. {P3} lives in {.}. The capital of the country where {Pq} lives is"
     the bridge is the queried person's country
  L  as B, then a colour per country in the prompt ("{c}'s colour is {k}.", brew's palette), and
     "The colour of the country where {Pq} lives is": the bridge bound, the second hop an in-context lookup
  RL as R, then a colour per country in the prompt, and "The country where {city} is located has the colour": the
     bridge recalled, the second hop an in-context lookup (the fourth cell of source x use)
Phase 3 (Zach, 2026-10-19: what uses the bridge vs where the answer comes from; L and RL confound the two):
  LM as B, then a landmark per country in the prompt ("{c}'s landmark is {m}."), and "The city where the landmark of
     the country where {Pq} lives stands is": a lookup in the prompt uses the bridge, the answer (the landmark's city)
     is recalled. Landmarks are in cities outside the 13 countries, so no table entry contradicts the countries' own
  RM as LM with R's recalled bridge ("... the country where {city} is located stands is")
  BT as B, then a colour per capital of the three countries in the prompt ("{capital}'s colour is {k}."), and "The
     capital of the country where {Pq} lives has the colour": a recalled fact (the capital) uses the bridge, the
     answer is read off the prompt
  RT as BT with R's recalled bridge
exp09 builds the counterfactuals from these fields: C sets the bridge to X (R: a city of X; B: the queried person and
X's holder swap countries, so the same countries stay in the prompt), O swaps X's and Z's holders (off the path).
Facts are written here by hand; exp09's check stage keeps the single-token, token-aligned items.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins

CAPITALS = {
    "France": "Paris",
    "Spain": "Madrid",
    "Italy": "Rome",
    "Germany": "Berlin",
    "Japan": "Tokyo",
    "Russia": "Moscow",
    "Egypt": "Cairo",
    "Peru": "Lima",
    "China": "Beijing",
    "Canada": "Ottawa",
    "Greece": "Athens",
    "Australia": "Canberra",
    "Poland": "Warsaw",
}
CITIES = {  # cities that are not the capital
    "France": ["Lyon", "Marseille", "Nice", "Bordeaux", "Toulouse"],
    "Spain": ["Barcelona", "Seville", "Valencia", "Bilbao", "Malaga"],
    "Italy": ["Milan", "Naples", "Venice", "Florence", "Turin"],
    "Germany": ["Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart"],
    "Japan": ["Osaka", "Kyoto", "Yokohama", "Nagoya", "Sapporo"],
    "Russia": ["Kazan", "Novosibirsk", "Omsk", "Samara", "Sochi"],
    "Egypt": ["Alexandria", "Luxor", "Giza", "Aswan"],
    "Peru": ["Cusco", "Arequipa", "Trujillo", "Iquitos"],
    "China": ["Shanghai", "Shenzhen", "Guangzhou", "Wuhan", "Chengdu"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton"],
    "Greece": ["Thessaloniki", "Patras", "Heraklion"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Poland": ["Krakow", "Gdansk", "Wroclaw", "Poznan"],
}
NAMES = [
    "Alice",
    "Bob",
    "Carol",
    "David",
    "Emma",
    "Frank",
    "Grace",
    "Henry",
    "Jack",
    "Kate",
    "Laura",
    "Mark",
    "Nina",
    "Oscar",
    "Paul",
    "Rachel",
    "Sam",
    "Tom",
    "Victor",
    "Will",
]
QUESTION = {
    "R": "The capital of the country where {city} is located is",
    "B": "The capital of the country where {q} lives is",
}
QUESTION_L = "The colour of the country where {q} lives is"  # v1: the model continues it as a sentence (1/400)
QUESTION_L2 = "The country where {q} lives has the colour"  # v2: answered for 40 of the first 40 items
QUESTION_RL = "The country where {city} is located has the colour"
LANDMARKS = {  # landmark (as written after "is") -> its city; every city outside the 13 countries, a single word
    "Big Ben": "London",
    "the Taj Mahal": "Agra",
    "the Burj Khalifa": "Dubai",
    "the Space Needle": "Seattle",
    "the Hagia Sophia": "Istanbul",
    "Christ the Redeemer": "Rio",
    "the Charles Bridge": "Prague",
    "the Atomium": "Brussels",
    "the Little Mermaid": "Copenhagen",
    "the Rijksmuseum": "Amsterdam",
    "Marina Bay Sands": "Singapore",
    "the Gateway of India": "Mumbai",
    "Schönbrunn Palace": "Vienna",
    "Wat Arun": "Bangkok",
    "the Belém Tower": "Lisbon",
    "the Liberty Bell": "Philadelphia",
}
PER_CITY_USE_SOURCE = 12  # RM, RT: items per city, as RL (about a third line up token for token with their C)
WHERE = {"bound": "where {q} lives", "recalled": "where {city} is located"}
QUESTION_USE_SOURCE = {
    "LM": "The city where the landmark of the country " + WHERE["bound"] + " stands is",
    "RM": "The city where the landmark of the country " + WHERE["recalled"] + " stands is",
    "BT": "The capital of the country " + WHERE["bound"] + " has the colour",
    "RT": "The capital of the country " + WHERE["recalled"] + " has the colour",
}


def make(rng: random.Random, family: str, index: int, city: str | None = None) -> dict:
    countries = list(CAPITALS)
    if family == "R":
        bridge = next(c for c, cities in CITIES.items() if city in cities)
        target, third = rng.sample([c for c in countries if c != bridge], 2)
    else:
        bridge, target, third = rng.sample(countries, 3)
    people = rng.sample(NAMES, 3)
    held = [bridge, target, third]
    rng.shuffle(held)  # who lives where, in sentence order
    context = " ".join(f"{p} lives in {c}." for p, c in zip(people, held, strict=True))
    if family == "R":
        question, cue = QUESTION["R"].format(city=city), city
    else:
        cue = people[held.index(bridge)]
        question = QUESTION["B"].format(q=cue)
    return {
        "name": f"{family}-{index:04d}",
        "family": family,
        "prompt": f"{context} {question}",
        "people": people,
        "countries": held,
        "cue": cue,
        "bridge": bridge,
        "answer": CAPITALS[bridge],
        "target": target,
        "target_answer": CAPITALS[target],
        "third": third,
    }


def make_lookup(rng: random.Random, index: int, question: str = QUESTION_L) -> dict:
    """Family L: B's bindings, then each country's colour in the prompt, and the colour of the queried person's
    country as the question (the answer is read off the prompt's table, as in brew's second lookup)."""
    from scripts.exp03_make_items import PALETTE

    item = make(rng, "B", index)
    colours = dict(zip(item["countries"], rng.sample(PALETTE, 3), strict=True))
    order = rng.sample(item["countries"], 3)  # its own order, so no person-to-colour position matches the table
    table = " ".join(f"{c}'s colour is {colours[c]}." for c in order)
    people = " ".join(f"{p} lives in {c}." for p, c in zip(item["people"], item["countries"], strict=True))
    return {
        **item,
        "name": f"L-{index:04d}",
        "family": "L",
        "prompt": f"{people} {table} {question.format(q=item['cue'])}",
        "colours": colours,
        "answer": colours[item["bridge"]],
        "target_answer": colours[item["target"]],
    }


def make_recall_lookup(rng: random.Random, index: int, city: str) -> dict:
    """Family RL: R's prompt (the bridge recalled from the city), then each country's colour in the prompt (in its own
    order), and the colour of the city's country as the question."""
    from scripts.exp03_make_items import PALETTE

    item = make(rng, "R", index, city)
    colours = dict(zip(item["countries"], rng.sample(PALETTE, 3), strict=True))
    order = rng.sample(item["countries"], 3)
    table = " ".join(f"{c}'s colour is {colours[c]}." for c in order)
    people = " ".join(f"{p} lives in {c}." for p, c in zip(item["people"], item["countries"], strict=True))
    return {
        **item,
        "name": f"RL-{index:04d}",
        "family": "RL",
        "prompt": f"{people} {table} {QUESTION_RL.format(city=city)}",
        "colours": colours,
        "answer": colours[item["bridge"]],
        "target_answer": colours[item["target"]],
    }


def make_use_source(rng: random.Random, family: str, index: int, city: str | None = None) -> dict:
    """Phase 3: R's or B's bindings, a table in the prompt, and the question (LM, RM, BT, RT; module docstring).
    'mid' holds each country's middle value (its landmark, or its capital) and 'values' its answer."""
    from scripts.exp03_make_items import PALETTE

    recalled = family in ("RM", "RT")
    item = make(rng, "R" if recalled else "B", index, city)
    if family in ("LM", "RM"):
        mid = dict(zip(item["countries"], rng.sample(list(LANDMARKS), 3), strict=True))
        values = {c: LANDMARKS[m] for c, m in mid.items()}
        table = " ".join(f"{c}'s landmark is {mid[c]}." for c in rng.sample(item["countries"], 3))
    else:
        mid = {c: CAPITALS[c] for c in item["countries"]}
        colours = dict(zip(item["countries"], rng.sample(PALETTE, 3), strict=True))
        values = colours
        table = " ".join(f"{mid[c]}'s colour is {colours[c]}." for c in rng.sample(item["countries"], 3))
    people = " ".join(f"{p} lives in {c}." for p, c in zip(item["people"], item["countries"], strict=True))
    question = QUESTION_USE_SOURCE[family].format(q=item["cue"], city=item["cue"])
    return {
        **item,
        "name": f"{family}-{index:04d}",
        "family": family,
        "prompt": f"{people} {table} {question}",
        "mid": mid,
        "values": values,
        "answer": values[item["bridge"]],
        "target_answer": values[item["target"]],
    }


def main_use_source(n: int, seed: int) -> None:
    out = pins.DATA_DIR / "use_source.json"
    assert not out.exists(), f"{out} exists; data files are written once"
    rng = random.Random(seed)
    cities = [c for cs in CITIES.values() for c in cs]
    per_city = PER_CITY_USE_SOURCE
    items = []
    for family in ("LM", "BT"):
        items += [make_use_source(rng, family, k) for k in range(n)]
    for family in ("RM", "RT"):
        items += [
            make_use_source(rng, family, k, city) for k, city in enumerate(c for c in cities for _ in range(per_city))
        ]
    blob = {
        "family": "use_source",
        "generator": f"scripts/exp09_make_items.py --use-source {n} --seed {seed}",
        "format": "Phase 3: LM, RM (a lookup in the prompt uses the bridge, the answer recalled) and BT, RT (a recalled "
        "fact uses the bridge, the answer read off the prompt), bound (LM, BT) or recalled (RM, RT); ungated",
        "landmarks": LANDMARKS,
        "items": items,
    }
    out.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out, {f: sum(i["family"] == f for i in items) for f in ("LM", "BT", "RM", "RT")})


def main_recall_lookup(per_city: int, seed: int) -> None:
    out = pins.DATA_DIR / "recall_lookup.json"
    assert not out.exists(), f"{out} exists; data files are written once"
    rng = random.Random(seed)
    cities = [c for cs in CITIES.values() for c in cs]
    items = [make_recall_lookup(rng, k, city) for k, city in enumerate(c for c in cities for _ in range(per_city))]
    blob = {
        "family": "recall_lookup",
        "generator": f"scripts/exp09_make_items.py --recall-lookup {per_city} --seed {seed}",
        "format": "RL: R's bridge recalled from the city, then a colour per country in the prompt; the second hop an "
        "in-context lookup; ungated",
        "items": items,
    }
    out.write_text(json.dumps(blob, indent=1) + "\n")
    print("wrote", out, f"{len(items)} recall-lookup items")


def main_lookup(n: int, seed: int, version: int = 1) -> None:
    out = pins.DATA_DIR / ("bind_lookup.json" if version == 1 else f"bind_lookup_v{version}.json")
    question = QUESTION_L if version == 1 else QUESTION_L2
    assert not out.exists(), f"{out} exists; data files are written once"
    rng = random.Random(seed)
    items = [make_lookup(rng, i, question) for i in range(n)]
    blob = {
        "family": "bind_lookup" if version == 1 else f"bind_lookup_v{version}",
        "generator": f"scripts/exp09_make_items.py --lookup {n} --seed {seed}"
        + ("" if version == 1 else f" --lookup-version {version}"),
        "format": "L: B's bindings, then a colour per country in the prompt; the bridge bound, the second hop an "
        "in-context lookup; ungated",
        "items": items,
    }
    out.write_text(json.dumps(blob, indent=1) + "\n")
    print("wrote", out, f"{n} lookup items")


def main(per_city: int, n_bound: int, seed: int) -> None:
    out = pins.DATA_DIR / "bind_recall.json"
    assert not out.exists(), f"{out} exists; data files are written once"
    rng = random.Random(seed)
    items = []
    for city in [c for cities in CITIES.values() for c in cities]:
        items += [make(rng, "R", len(items), city) for _ in range(per_city)]
    n_recalled = len(items)
    items += [make(rng, "B", len(items) - n_recalled) for _ in range(n_bound)]
    out.write_text(
        json.dumps(
            {
                "family": "bind_recall",
                "generator": f"scripts/exp09_make_items.py --per-city {per_city} --n-bound {n_bound} --seed {seed}",
                "format": "R: bridge recalled from the city; B: bridge bound to a name in context; same countries, "
                "same second hop (capital); ungated",
                "capitals": CAPITALS,
                "cities": CITIES,
                "items": items,
            },
            indent=1,
        )
        + "\n"
    )
    print("wrote", out, f"{n_recalled} recalled, {n_bound} bound")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--per-city", type=int, default=6)
    parser.add_argument("--n-bound", type=int, default=400)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--lookup", type=int, default=0, help="write data/bind_lookup.json with this many L items")
    parser.add_argument("--recall-lookup", type=int, default=0, help="write data/recall_lookup.json, N items per city")
    parser.add_argument(
        "--lookup-version", type=int, default=1, choices=[1, 2], help="2: the question ending '... has the colour'"
    )
    parser.add_argument("--use-source", type=int, default=0, help="write data/use_source.json (Phase 3)")
    args = parser.parse_args()
    if args.use_source:
        main_use_source(args.use_source, args.seed)
    elif args.recall_lookup:
        main_recall_lookup(args.recall_lookup, args.seed)
    elif args.lookup:
        main_lookup(args.lookup, args.seed, args.lookup_version)
    else:
        main(args.per_city, args.n_bound, args.seed)
