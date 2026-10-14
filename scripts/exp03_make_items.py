"""Fresh brew items for exp03's held-out replication, in the format of WorkspaceBench's brew_intermediates bank.

  exp03_make_items.py [--n N] [--seed S]  -> data/brew_fresh.json (write-once; pin its sha256 in pins.py)

Each item is a ten-row colour table drawn from the bank's twelve-colour palette (every row turns into another row's
colour, never itself), shuffled, then "You stir the potion twice." and the start line last, worded as in the bank. The
start S, intermediate I = f(S) and answer A = f(I) are three distinct colours. Items are not gated here: exp03's runner
keeps an item only if the model's greedy answer is A (the bank also required 10/10 sampled answers to be correct).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

PALETTE = ("black", "blue", "brown", "gold", "gray", "green", "orange", "pink", "purple", "red", "teal", "white")
N_ROWS = 10
HEAD = (
    "Here is a colour-mixing problem. Answer with a single colour word and nothing else.\n"
    "Problem: A potion changes colour each time it is stirred, according to these rules:\n"
)


def article(colour: str) -> str:
    return "An" if colour[0] in "aeiou" else "A"


def make_item(rng: random.Random, index: int) -> dict:
    rows = rng.sample(PALETTE, N_ROWS)
    while True:
        table = {c: rng.choice([d for d in rows if d != c]) for c in rows}
        start = rng.choice(rows)
        inter, answer = table[start], table[table[start]]
        if answer != start:
            break
    rules = "".join(f"{article(c)} {c} potion turns {table[c]} when stirred.\n" for c in rows)
    prompt = (
        f"{HEAD}{rules}You stir the potion twice.\nThe potion starts out {start}.\n"
        "What colour is the potion at the end?"
    )
    return {
        "name": f"brewfresh-{index:04d}",
        "mode": "single",
        "depth": 2,
        "n_rows": N_ROWS,
        "start": start,
        "stirs": ["stir", "stir"],
        "intermediates": [inter],
        "untaken": [],
        "answer": answer,
        "off_trajectory": [c for c in rows if c not in (start, inter, answer)],
        "prompt": prompt,
        "table": {c: {"stir": table[c]} for c in rows},
    }


def main(n: int, seed: int) -> None:
    out = pins.DATA_DIR / "brew_fresh.json"
    assert not out.exists(), f"{out} exists; data files are written once"
    bank = {(it["prompt"]) for it in pins.brew_items()}
    rng = random.Random(seed)
    items = []
    while len(items) < n:
        item = make_item(rng, len(items))
        if item["prompt"] not in bank:
            items.append(item)
    out.write_text(
        json.dumps(
            {
                "family": "brew_fresh",
                "generator": f"scripts/exp03_make_items.py --n {n} --seed {seed}",
                "format": "WorkspaceBench brew_intermediates (single, depth 2, ten rows, start line last); ungated",
                "items": items,
            },
            indent=1,
        )
        + "\n"
    )
    print("wrote", out, len(items))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--n", type=int, default=200)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    main(args.n, args.seed)
