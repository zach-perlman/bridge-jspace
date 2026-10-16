"""A3 (exp12): where the lens misses the bridge at the prompt's last word, is it on top at an earlier word instead?

Reads only results/exp12_position_map/20261015-100735/{items.jsonl, layers.json, grids_<lens>.npz}. No code from
this repo. Run from the repo root:  uv run python verification/a3_exp12.py
"""

import json
import random
from collections import Counter
from math import comb, sqrt
from pathlib import Path

import numpy as np

RUN = Path("results/exp12_position_map/20261015-100735")
BAND = range(32, 49)  # layers 32..48 inclusive
FIRST = 1  # pool ranks are 1-based: 1 = first among the 97 entities


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(c - h, 0.0), min(c + h, 1.0)


def mcnemar(b, c):
    n = b + c
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2**n) if n else 1.0


meta = {m["name"]: m for m in jsonl(RUN / "items.jsonl")}
eligible = sorted(n for n, m in meta.items() if m["status"] == "eligible")
layers = json.loads((RUN / "layers.json").read_text())

for lens in ("jlens", "jpp"):
    z = np.load(RUN / f"grids_{lens}.npz")
    rows = [i for i, layer in enumerate(layers[lens]) if layer in BAND]
    # grid[name|field] is [layers, positions]: the word's rank among the 97 entities at each layer and prompt position
    missed = []
    for n in eligible:
        top = z[f"{n}|bridge_pool"][rows] == FIRST  # [band layers, positions]
        if top[:, -1].mean() < 0.5:  # last position = the prompt's last word (trailing space stripped)
            missed.append(n)
    found, ctrl, where = {}, {}, Counter()
    for n in missed:
        b = (z[f"{n}|bridge_pool"][rows] == FIRST)[:, :-1].mean(0)  # share of band layers, per earlier position
        d = (z[f"{n}|distractor_pool"][rows] == FIRST)[:, :-1].mean(0)
        found[n], ctrl[n] = bool(b.max() >= 0.5), bool(d.max() >= 0.5)
        if found[n]:
            where[meta[n]["offsets"][int(np.argmax(b))]] += 1
    k_b, k_d, m = sum(found.values()), sum(ctrl.values()), len(missed)
    only_b = sum(found[n] and not ctrl[n] for n in missed)
    only_d = sum(ctrl[n] and not found[n] for n in missed)
    print(
        f"\n== {lens}: {m} of {len(eligible)} questions have the bridge first at under half of layers 32-48 at the last word"
    )
    print(f"   bridge first at >= half the band at some earlier word:     {k_b}/{m} = {k_b / m:.2f} {wilson(k_b, m)}")
    print(f"   distractor, same search (best of the earlier words):        {k_d}/{m} = {k_d / m:.2f} {wilson(k_d, m)}")
    print(
        f"   paired on the same questions: only the bridge {only_b}, only the distractor {only_d}, "
        f"McNemar p = {mcnemar(only_b, only_d):.2g}"
    )
    print(f"   where the bridge is found (offset from the last word, 0 = last word): {dict(sorted(where.items()))}")

    if lens == "jlens":
        print("\n== Five missed questions by seed 0 (J-lens): share of layers 32-48 with the word first, per position")
        for n in random.Random(0).sample(missed, 5):
            mm = meta[n]
            b = (z[f"{n}|bridge_pool"][rows] == FIRST).mean(0)
            d = (z[f"{n}|distractor_pool"][rows] == FIRST).mean(0)
            print(f"\n{n}: bridge {mm['intermediate']!r}, distractor {mm['swap_to']!r}")
            for tok, off, sb, sd in list(zip(mm["tokens"], mm["offsets"], b, d, strict=True))[-8:]:
                print(f"   {off:>3} {tok!r:14} bridge {sb:.2f}  distractor {sd:.2f}")
