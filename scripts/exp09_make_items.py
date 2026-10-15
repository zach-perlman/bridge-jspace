"""Items for exp09_bind_recall: one two-hop question whose bridge country is recalled (R) or bound in context (B).

  exp09_make_items.py [--per-city N] [--n-bound N] [--seed S]  -> data/bind_recall.json (write-once; pin its sha256)

Both families share the format, the countries and the second hop (the country's capital):
  R  "{N1} lives in {cA}. {N2} lives in {cB}. The capital of the country where {city} is located is"
     the bridge (the city's country) is recalled; the two context countries are other countries
  B  "{N1} lives in {c1}. {N2} lives in {c2}. The capital of the country where {Nq} lives is"
     the bridge is the country bound to the queried name Nq (N1 or N2, either order); the other is in context too
Every item also has a target X for the edits: a country of the set that is neither the bridge nor in its prompt.
Facts are written here by hand; exp09's check stage keeps the items whose city, names and countries are single tokens.
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
    "Turkey": "Ankara",
    "Portugal": "Lisbon",
    "Kenya": "Nairobi",
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
    "Turkey": ["Istanbul", "Izmir", "Antalya", "Bursa"],
    "Portugal": ["Porto", "Braga", "Faro", "Coimbra"],
    "Kenya": ["Mombasa", "Kisumu", "Nakuru"],
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
    n1, n2 = rng.sample(NAMES, 2)
    if family == "R":
        bridge = next(c for c, cities in CITIES.items() if city in cities)
        c1, c2 = rng.sample([c for c in countries if c != bridge], 2)
        question = QUESTION["R"].format(city=city)
        cue = city
    else:
        c1, c2 = rng.sample(countries, 2)
        queried = rng.choice([n1, n2])
        bridge = c1 if queried == n1 else c2
        question = QUESTION["B"].format(q=queried)
        cue = queried
    other = [c for c in (c1, c2) if c != bridge]
    target = rng.choice([c for c in countries if c not in (bridge, c1, c2)])
    return {
        "name": f"{family}-{index:04d}",
        "family": family,
        "prompt": f"{n1} lives in {c1}. {n2} lives in {c2}. {question}",
        "cue": cue,
        "bridge": bridge,
        "answer": CAPITALS[bridge],
        "context_countries": [c1, c2],
        "in_context_other": other[0] if family == "B" else None,
        "target": target,
        "target_answer": CAPITALS[target],
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
