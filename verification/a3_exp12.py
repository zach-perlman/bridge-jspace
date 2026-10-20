"""A3 (exp12): where the lens misses the bridge at the prompt's last word, is it on top at an earlier word instead?

Reads only results/exp12_position_map/20261015-100735/{items.jsonl, layers.json, grids_<lens>.npz} and the cue spans
in data/cue_spans.json (written by the coding agent, not yet human-reviewed: check them in the table at the end).
No code from this repo. Run from the repo root:  uv run python verification/a3_exp12.py
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


def in_cue(m, cue):
    """Per token of the prompt: does it overlap the cue span (by character offsets)?"""
    prompt = "".join(m["tokens"])
    start = prompt.index(cue)
    lengths = np.array([len(t) for t in m["tokens"]])
    ends = np.cumsum(lengths)
    return (ends - lengths < start + len(cue)) & (ends > start)


meta = {m["name"]: m for m in jsonl(RUN / "items.jsonl")}
eligible = sorted(n for n, m in meta.items() if m["status"] == "eligible")
layers = json.loads((RUN / "layers.json").read_text())
cues = json.loads(Path("data/cue_spans.json").read_text())["cues"]
rng = np.random.default_rng(0)
table = {}

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
    seen_d = sum((z[f"{n}|distractor_pool"][rows] == FIRST)[:, -1].mean() >= 0.5 for n in eligible)
    print(
        f"   seen at the last word (>= half the band): bridge {len(eligible) - m}, distractor {seen_d} of {len(eligible)}"
    )
    print(f"   bridge first at >= half the band at some earlier word:     {k_b}/{m} = {k_b / m:.2f} {wilson(k_b, m)}")
    print(f"   distractor, same search (best of the earlier words):        {k_d}/{m} = {k_d / m:.2f} {wilson(k_d, m)}")
    print(
        f"   paired on the same questions: only the bridge {only_b}, only the distractor {only_d}, "
        f"McNemar p = {mcnemar(only_b, only_d):.2g}"
    )
    print(f"   where the bridge is found (offset from the last word, 0 = last word): {dict(sorted(where.items()))}")

    # the bridge's rate above the distractor's, same questions (what the search finds beyond its base rate)
    fb = np.array([found[n] for n in missed], float)
    fd = np.array([ctrl[n] for n in missed], float)
    idx = rng.integers(0, m, (10000, m))
    lo, hi = np.percentile((fb[idx] - fd[idx]).mean(1) * 100, [2.5, 97.5])
    print(
        f"   bridge minus distractor: {100 * (fb.mean() - fd.mean()):+.1f} points [{lo:+.1f}, {hi:+.1f}] "
        f"(paired bootstrap); both found {sum(found[n] and ctrl[n] for n in missed)}, "
        f"neither {sum(not found[n] and not ctrl[n] for n in missed)}"
    )

    # cue span: is some earlier word where the word is first (>= half the band) inside it? the span's share of words
    hit_in_cue = {
        (n, field): bool(
            (((z[f"{n}|{field}"][rows] == FIRST)[:, :-1].mean(0) >= 0.5) & in_cue(meta[n], cues[n])[:-1]).any()
        )
        for n in missed
        for field in ("bridge_pool", "distractor_pool")
    }
    cover = [in_cue(meta[n], cues[n])[2:-1].mean() for n in missed]  # earlier words, "Fact" ":" left out
    kb = [n for n in missed if found[n]]
    kd = [n for n in missed if ctrl[n]]
    print(
        f"   a word inside the cue span: bridge {sum(hit_in_cue[n, 'bridge_pool'] for n in kb)}/{len(kb)}, "
        f"distractor {sum(hit_in_cue[n, 'distractor_pool'] for n in kd)}/{len(kd)}; "
        f"the cue span is {100 * np.mean(cover):.0f}% of the earlier words on average"
    )
    group = {n: "multihop" if meta[n]["category"] == "multihop" else "other" for n in missed}
    for g in ("multihop", "other"):
        names = [n for n in missed if group[n] == g]
        print(f"   {g:8s}: missed {len(names)}, bridge found earlier {sum(found[n] for n in names)}")

    for n in missed:
        b = (z[f"{n}|bridge_pool"][rows] == FIRST)[:, :-1].mean(0)
        hits = [meta[n]["tokens"][i] for i in np.where(b >= 0.5)[0]]
        table.setdefault(n, {})[lens] = hits

    if lens == "jlens":
        print("\n== Five missed questions by seed 0 (J-lens): share of layers 32-48 with the word first, per position")
        for n in random.Random(0).sample(missed, 5):
            mm = meta[n]
            b = (z[f"{n}|bridge_pool"][rows] == FIRST).mean(0)
            d = (z[f"{n}|distractor_pool"][rows] == FIRST).mean(0)
            print(f"\n{n}: bridge {mm['intermediate']!r}, distractor {mm['swap_to']!r}")
            for tok, off, sb, sd in list(zip(mm["tokens"], mm["offsets"], b, d, strict=True))[-8:]:
                print(f"   {off:>3} {tok!r:14} bridge {sb:.2f}  distractor {sd:.2f}")

print("\n== Every question missed at the last word: the words where the bridge is first (>= half of layers 32-48)")
print("   and the cue span; check by hand that the span is the words that point to the bridge")
for n in sorted(table):
    mm = meta[n]
    prompt = "".join(mm["tokens"]).removeprefix("Fact: ")
    words = {lens: " | ".join(repr(t) for t in table[n].get(lens, [])) or "-" for lens in ("jlens", "jpp")}
    missed_by = "+".join(lens for lens in ("jlens", "jpp") if lens in table[n])
    print(f"\n{n} [{mm['category']}; missed by {missed_by}]: bridge {mm['intermediate']!r}")
    print(f"   prompt: {prompt!r}\n   cue:    {cues[n]!r}")
    print(f"   J-lens: {words['jlens']}\n   J++:    {words['jpp']}")
