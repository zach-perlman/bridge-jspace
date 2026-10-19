"""B1 swap flip rates by bridge kind (place, person, other), per run and condition, Wilson 95% CIs (one row per item).

python3 scripts/b1_by_kind.py RUN:BAND [RUN:BAND ...]   e.g. main_v4_jpp:24-40 own_chat_stmt_h200:32-48
"""

import collections
import json
import math
import sys
from pathlib import Path

PLACE = {"Australia", "Brazil", "Canada", "China", "Egypt", "England", "France", "Germany", "Greece", "Hungary", "Italy",
         "Japan", "Peru", "Poland", "Russia", "Spain", "Sweden", "Vatican", "Philadelphia", "Seattle", "India", "Mexico",
         "Singapore"}  # fmt: skip
PERSON = {"Darwin", "Einstein", "Lincoln", "Mozart", "Napoleon", "Newton", "Shakespeare"}
KINDS = ("place", "person", "other")


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n == 0:
        return (math.nan, math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def main() -> None:
    items = {i["name"]: i for i in json.loads(Path("data/probe_swap.json").read_text())["items"]}

    def kind(name: str) -> str:
        bridge = items[name]["intermediate"]
        return "place" if bridge in PLACE else "person" if bridge in PERSON else "other"

    for spec in sys.argv[1:]:
        run, band = spec.split(":")
        rows: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
        for line in Path(f"results/exp02_swaps/{run}/outcomes.jsonl").read_text().splitlines():
            o = json.loads(line)
            if o["band"] == band and not o["null"]:
                rows[o["condition"]][kind(o["name"])][o["name"]] = bool(o["flip"])
        print(f"{run} ({band})")
        for cond, by in rows.items():
            cells = []
            for k in KINDS:
                v = list(by[k].values())
                p, lo, hi = wilson(sum(v), len(v))
                cells.append(f"{k} {sum(v)}/{len(v)} {100 * p:.0f}% [{100 * lo:.0f},{100 * hi:.0f}]")
            print(f"  {cond:18s}", "  ".join(cells))


if __name__ == "__main__":
    main()
