"""A1 (exp10): do the J-lens and J++ read the bridge in the middle layers, where the logit lens does not?

Reads only the raw files: results/exp10_lens_sanity/20261013-205936/*.jsonl and data/lens_eval_multihop.json.
No code from this repo is imported. Run from the repo root:  uv run python verification/a1_exp10.py
"""

import json
import random
from math import comb, sqrt
from pathlib import Path

RUN = "results/exp10_lens_sanity/20261013-205936"
BAND = range(32, 49)  # layers 32..48 inclusive
TOP = 10  # ranks in the file are 0-based: rank < 10 means "in the top 10 of the vocabulary"
NUMBER_WORDS = set(
    [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
        "hundred",
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "eleventh",
        "twelfth",
    ]
)


def kind(forms):
    forms = [f.strip() for f in forms]
    if any(f.isdigit() or f.lower() in NUMBER_WORDS for f in forms):
        return "number"
    if all(len(f) == 1 and f.isalpha() for f in forms):
        return "letter"
    return "word"


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(c - h, 0.0), min(c + h, 1.0)


def mcnemar(b, c):
    """Exact two-sided McNemar p for b vs c discordant pairs."""
    n = b + c
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2**n) if n else 1.0


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


items = {i["name"]: i for i in json.loads(Path("data/lens_eval_multihop.json").read_text())["items"]}
meta = {m["name"]: m for m in jsonl(f"{RUN}/multihop_items.jsonl")}
rows = jsonl(f"{RUN}/multihop_ranks.jsonl")

single = sorted(n for n, m in meta.items() if m["all_single_token"])
kinds = {n: kind(items[n]["intermediates"]) for n in single}
print(
    f"items: {len(meta)}; single-token bridges: {len(single)}; by kind:",
    {k: sum(v == k for v in kinds.values()) for k in ("word", "number", "letter")},
)

# hit[reader][question] = some listed form of the bridge is in the top 10 at some layer 32..48
hit = {}
for r in rows:
    if r["name"] in kinds:
        h = any(rank < TOP for layer, rank in zip(r["layers"], r["ranks"], strict=True) if layer in BAND)
        hit.setdefault(r["reader"], {}).setdefault(r["name"], False)
        hit[r["reader"]][r["name"]] |= h

subsets = {
    "word bridges": [n for n in single if kinds[n] == "word"],
    "word bridges, answered correctly": [n for n in single if kinds[n] == "word" and meta[n]["model_correct"]],
    "all single-token bridges": single,
}
for label, names in subsets.items():
    print(f"\n== {label} (n={len(names)}): bridge in the top 10 at some layer 32-48")
    for reader in ("logit", "jlens", "jpp"):
        k = sum(hit[reader][n] for n in names)
        lo, hi = wilson(k, len(names))
        print(f"   {reader:6s} {k:3d}/{len(names)} = {k / len(names):.2f}  [{lo:.2f}, {hi:.2f}]")
    for a, b in (("jpp", "logit"), ("jlens", "logit"), ("jpp", "jlens")):
        only_a = sum(hit[a][n] and not hit[b][n] for n in names)
        only_b = sum(hit[b][n] and not hit[a][n] for n in names)
        print(f"   paired {a} vs {b}: only {a} {only_a}, only {b} {only_b}, McNemar p = {mcnemar(only_a, only_b):.2g}")

print("\n== 8 word-bridge questions by seed 0, to read by hand (best rank = 0 means first in the vocabulary)")
for n in random.Random(0).sample(subsets["word bridges"], 8):
    print(
        f"\n{n}: {items[n]['prompt'].strip()!r}\n   bridge forms {items[n]['intermediates']}, "
        f"model answers correctly: {meta[n]['model_correct']}"
    )
    for r in (r for r in rows if r["name"] == n):
        band = [(rank, layer) for layer, rank in zip(r["layers"], r["ranks"], strict=True) if layer in BAND]
        best, at = min(band)
        print(
            f"   {r['reader']:6s} form {r['intermediate']!r:16} best rank in 32-48: {best:6d} (layer {at}); "
            f"best anywhere: {r['min_rank']} (layer {r['argmin_layer']})"
        )
