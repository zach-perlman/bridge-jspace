"""jsuite_threehop (Zach, 2026-10-24, prereg amendment 25): module 3 of the combined suite, three-hop chains.

natural3's design (scripts/natural3.py: cities and people -> country -> continent, all 8 words PPP ... MMM, route
uniqueness, per-step candidate vocabularies) with South Africa removed from every table: as a middle country its name
contains the answer "Africa", and its first token is South America's (nat3_v1: 24 PMM/MMM items answerable from the
name). Dropped: the country itself, Cape Town, Mandela and Tutu. A wrapper, so natural3.py is unchanged; the set's
manifest records the wrapper and what it dropped.

python scripts/jsuite_threehop.py --name jsuite_v1_threehop --seed 2501 [--scenes 2]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import natural3 as N3  # noqa: E402

DROP_COUNTRY = "South Africa"


def main(name: str, seed: int, scenes: int) -> None:
    dropped = {"country": [DROP_COUNTRY], "cities": [c for c, v in N3.CITIES.items() if v[0] == DROP_COUNTRY],
               "people": [p for p, v in N3.PEOPLE.items() if v[0] == DROP_COUNTRY]}  # fmt: skip
    for c in dropped["cities"]:
        del N3.CITIES[c]
    for p in dropped["people"]:
        del N3.PEOPLE[p]
    del N3.CONT[DROP_COUNTRY]
    N3.make(name, seed, scenes)
    man = N3.DATA / f"{name}_chat" / "manifest.json"
    m = json.loads(man.read_text())
    m.update({"wrapper": "scripts/jsuite_threehop.py", "dropped": dropped})
    man.write_text(json.dumps(m, indent=2) + "\n")
    print("dropped:", dropped)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=2501)
    ap.add_argument("--scenes", type=int, default=2)
    a = ap.parse_args()
    main(a.name, a.seed, a.scenes)
