"""Items for exp09_bind_recall: one two-hop question whose bridge country is recalled (R) or bound in context (B).

  exp09_make_items.py [--per-city N] [--n-bound N] [--seed S]  -> data/bind_recall.json (write-once; pin its sha256)

Both families share the format, the countries (the 13 with exp01 probes) and the second hop (the country's capital).
Three people and three countries come first; every prompt names the bridge I, the target X and a third country Z:
  R  "{P1} lives in {.}. {P2} lives in {.}. {P3} lives in {.}. The capital of the country where {city} is located is"
     the bridge is recalled from the city; I, X and Z are context only
  B  "{P1} lives in {.}. {P2} lives in {.}. {P3} lives in {.}. The capital of the country where {Pq} lives is"
     the bridge is the queried person's country
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
    args = parser.parse_args()
    main(args.per_city, args.n_bound, args.seed)
