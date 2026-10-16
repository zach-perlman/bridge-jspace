"""A2 (exp11): at the prompt's last word, do the lenses put the bridge first among the 97 candidate entities more
often than its distractor, and does the bridge come first at an earlier layer than the answer?

Reads only results/exp11_bridge_vs_answer_by_layer/20261015-100110/{items,ranks}.jsonl. No code from this repo.
Run from the repo root:  uv run python verification/a2_exp11.py
"""

import json
import random
from pathlib import Path

import numpy as np

RUN = "results/exp11_bridge_vs_answer_by_layer/20261015-100110"
BAND = range(32, 49)  # layers 32..48 inclusive
FIRST = 1  # pool ranks in the file are 1-based: 1 = first among the candidates (97 entities, 112 answers)
rng = np.random.default_rng(0)


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


items = {i["name"]: i for i in jsonl(f"{RUN}/items.jsonl")}
eligible = sorted(n for n, i in items.items() if i["status"] == "eligible")  # answered correctly (greedy)
rows = {(r["name"], r["reader"]): r for r in jsonl(f"{RUN}/ranks.jsonl")}
print(f"questions: {len(items)}, answered correctly (eligible): {len(eligible)}")


def boot(values, n=10000):
    v = np.asarray(values, float)
    m = v[rng.integers(0, len(v), (n, len(v)))].mean(1)
    return v.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)


def band_share(r, field):
    """Share of layers 32-48 at which `field` is first; None if the word has no single-token rank (multi-token)."""
    if r[field] is None:
        return None
    return np.mean([rank == FIRST for layer, rank in zip(r["layers"], r[field], strict=True) if layer in BAND])


print("\n== 1. Share of layers 32-48 with the word first among its candidates (mean over questions, 95% CI)")
for reader in ("logit", "jlens", "jpp"):
    out = {}
    for field in ("bridge_pool", "distractor_pool", "answer_pool"):
        v = [s for n in eligible if (s := band_share(rows[n, reader], field)) is not None]
        out[field] = v
        m, lo, hi = boot(v)
        print(f"   {reader:6s} {field:16s} n={len(v):2d}  {m:.2f} [{lo:.2f}, {hi:.2f}]")
    diff = [
        band_share(rows[n, reader], "bridge_pool") - band_share(rows[n, reader], "distractor_pool") for n in eligible
    ]
    m, lo, hi = boot(diff)
    print(f"   {reader:6s} bridge minus distractor, same questions: {m:+.2f} [{lo:+.2f}, {hi:+.2f}]")


def onset(names, reader, field):
    """First layer at which at least half of `names` have `field` first; None if never."""
    with_word = [n for n in names if rows[n, reader][field] is not None]
    layers = rows[with_word[0], reader]["layers"]
    share = np.mean([[rank == FIRST for rank in rows[n, reader][field]] for n in with_word], axis=0)
    hits = [layer for layer, s in zip(layers, share, strict=True) if s >= 0.5]
    return hits[0] if hits else None


print("\n== 2. Same position (last word): first layer at which half the questions have the word first")
for reader in ("jlens", "jpp"):
    b, a = onset(eligible, reader, "bridge_pool"), onset(eligible, reader, "answer_pool")
    lags = []
    for _ in range(2000):  # resample questions, recompute both onsets
        sample = list(rng.choice(eligible, len(eligible)))
        bb, aa = onset(sample, reader, "bridge_pool"), onset(sample, reader, "answer_pool")
        if bb is not None and aa is not None:
            lags.append(aa - bb)
    lo, hi = np.percentile(lags, [2.5, 97.5])
    print(
        f"   {reader:6s} bridge from layer {b}, answer from layer {a}: answer {a - b} layers later "
        f"[{lo:.0f}, {hi:.0f}] (bootstrap over questions, {len(lags)}/2000 resamples reach half for both)"
    )

print("\n== 3. Six questions by seed 0, J-lens, rank among the candidates at every 4th layer (1 = first)")
for n in random.Random(0).sample(eligible, 6):
    r = rows[n, "jlens"]
    print(f"\n{n}: bridge {items[n]['intermediate']!r}, distractor {items[n]['swap_to']!r}")
    picks = [i for i, layer in enumerate(r["layers"]) if layer % 4 == 0 and 20 <= layer <= 60]
    print("   layer      " + " ".join(f"{r['layers'][i]:>4}" for i in picks))
    for field in ("bridge_pool", "distractor_pool", "answer_pool"):
        vals = " ".join(f"{r[field][i]:>4}" for i in picks) if r[field] is not None else "  (multi-token answer)"
        print(f"   {field.split('_')[0]:10s} {vals}")
