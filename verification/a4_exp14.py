"""A4 (exp14, pinned run): on the cue phrase, does swapping the bridge still change the answer when the answer's lens
coordinates are held at their clean values, and does the answer swap with the bridge's held?

Reads only results/exp14_cue_answer_swaps/20261015-114825/{manifest.json, items.jsonl, outcomes.jsonl, leakage.jsonl}.
No code from this repo. Run from the repo root:  uv run python verification/a4_exp14.py

Kinds: "bridge" swaps the bridge pair (Brazil -> Mexico), "answer" the answer pair (Portuguese -> Spanish), both
aiming at the same new answer; "_pinned" holds the other pair's coordinates at their clean values. A flip is the
swap's answer in the greedy continuation and not the clean one. null = a random direction (the run's control).
"""

import json
import random
import statistics
from math import comb, sqrt
from pathlib import Path

import numpy as np

RUN = Path("results/exp14_cue_answer_swaps/20261015-114825")
CUE, LAST = ("cue", "24-40"), ("last", "40-56")
KINDS = ("bridge", "answer", "bridge_pinned", "answer_pinned")
# what the bridge is, assigned by hand from the 62 distinct bridges of the eligible questions: countries and cities are
# places; named people; everything else (animals, elements, months, organs, planets, ...) is other
BRIDGE_KIND = {
    "place": {"Australia", "Brazil", "Canada", "China", "Egypt", "England", "France", "Germany", "Greece", "Hungary",
              "Italy", "Japan", "Peru", "Philadelphia", "Poland", "Russia", "Seattle", "Spain", "Sweden", "Vatican"},
    "person": {"Darwin", "Einstein", "Lincoln", "Mozart", "Napoleon", "Newton", "Shakespeare"},
}  # fmt: skip
rng = np.random.default_rng(0)


def bridge_kind(bridge):
    return next((g for g, names in BRIDGE_KIND.items() if bridge in names), "other")


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


def pct(k, n):
    lo, hi = wilson(k, n)
    return f"{k:2d}/{n} = {100 * k / n:4.1f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


manifest = json.loads((RUN / "manifest.json").read_text())
print("decision rule, fixed before the run:\n  " + manifest["config"]["params"]["decision"])

items = {i["name"]: i for i in jsonl(RUN / "items.jsonl")}
eligible = sorted(n for n, i in items.items() if i["status"] == "eligible")
both = sorted(n for n in eligible if all(items[n]["swappable"][k] for k in KINDS))
print(f"\nquestions: {len(items)}, answered correctly (eligible): {len(eligible)}, with all four swaps: {len(both)}")

out = {
    (o["lens"], o["positions"], o["band"], o["kind"], o["null"], o["name"]): o for o in jsonl(RUN / "outcomes.jsonl")
}
print(
    "outcomes marked ambiguous:",
    sum(o["ambiguous"] for o in out.values()),
    "| with skipped layers:",
    sum(bool(o["layers_skipped"]) for o in out.values()),
)

# overlap: per question, mean over the band's layers of the cosine between the two swaps' difference vectors
cos = {}
for r in jsonl(RUN / "leakage.jsonl"):
    cos.setdefault((r["lens"], r["positions"], r["band"], r["name"]), []).append(r["diff_cosine"])

for lens in ("jpp", "jlens"):
    print(f"\n==================== {lens}")
    for cell in (CUE, LAST):
        print(f"\n== {lens}, {cell[0]} positions, layers {cell[1]}: of the {len(both)} questions with all four swaps")
        print("   kind            changed to the swap's answer   kept the clean answer   lost it, no swap answer")
        for kind in KINDS:
            for null in (False, True):
                rows = [out[(lens, *cell, kind, null, n)] for n in both]
                f = sum(o["flip"] for o in rows)
                k = sum(o["kept_clean"] for o in rows)
                tag = f"{kind}{' (random)' if null else ''}"
                print(f"   {tag:24s} {pct(f, len(rows)):28s}  {k:2d}/{len(rows)}               {len(rows) - f - k:2d}")

    # the main comparison: pinned bridge vs pinned answer on the cue phrase, same questions
    cut = statistics.median(statistics.mean(cos[(lens, *CUE, n)]) for n in both)
    high = [n for n in both if statistics.mean(cos[(lens, *CUE, n)]) >= cut]
    for label, names in (("all questions", both), (f"overlap at or above the median ({cut:.2f})", high)):
        b = np.array([out[(lens, *CUE, "bridge_pinned", False, n)]["flip"] for n in names], float)
        a = np.array([out[(lens, *CUE, "answer_pinned", False, n)]["flip"] for n in names], float)
        only_b, only_a = int(((b == 1) & (a == 0)).sum()), int(((a == 1) & (b == 0)).sum())
        idx = rng.integers(0, len(names), (10000, len(names)))
        lo, hi = np.percentile((b[idx] - a[idx]).mean(1) * 100, [2.5, 97.5])
        print(
            f"\n== {lens}, cue phrase, {label} (n={len(names)}): pinned bridge {int(b.sum())}, pinned answer {int(a.sum())}"
        )
        print(
            f"   difference {100 * (b.mean() - a.mean()):+.1f} points [{lo:+.1f}, {hi:+.1f}] (paired bootstrap); "
            f"only the bridge {only_b}, only the answer {only_a}, both {int(((a == 1) & (b == 1)).sum())}, "
            f"McNemar p = {mcnemar(only_b, only_a):.2g}"
        )

    # dose: per question, the pinned swap's edit size over its plain swap's; and the random direction's over the real
    print(f"\n== {lens}, cue phrase: edit size")
    for pinned, plain in (("bridge_pinned", "bridge"), ("answer_pinned", "answer")):
        r = [
            out[(lens, *CUE, pinned, False, n)]["edit_ratio"] / out[(lens, *CUE, plain, False, n)]["edit_ratio"]
            for n in both
        ]
        nr = [
            out[(lens, *CUE, pinned, True, n)]["edit_ratio"] / out[(lens, *CUE, pinned, False, n)]["edit_ratio"]
            for n in both
        ]
        print(
            f"   {pinned:14s} / {plain:7s}: median {statistics.median(r):.2f}, range {min(r):.2f}-{max(r):.2f}, "
            f"under half: {sum(x < 0.5 for x in r)} | random / real: median {statistics.median(nr):.2f}"
        )
    # the main comparison's own dose: the held answer swap's edit over the held bridge swap's, same question
    r = [
        out[(lens, *CUE, "answer_pinned", False, n)]["edit_ratio"]
        / out[(lens, *CUE, "bridge_pinned", False, n)]["edit_ratio"]
        for n in both
    ]
    print(
        f"   answer_pinned  / bridge_pinned: median {statistics.median(r):.2f}, range {min(r):.2f}-{max(r):.2f}, "
        f"under half: {sum(x < 0.5 for x in r)}"
    )

    # by what the bridge is (hand-assigned in BRIDGE_KIND; check it) and by the set's category
    print(f"\n== {lens}, cue phrase, held bridge swap by kind of bridge (changed / questions)")
    for g in ("place", "person", "other"):
        names = [n for n in both if bridge_kind(items[n]["intermediate"]) == g]
        k = sum(out[(lens, *CUE, "bridge_pinned", False, n)]["flip"] for n in names)
        print(f"   {g:7s} {pct(k, len(names))}")
    sizes = [sum(items[n]["category"] == c for n in both) for c in {items[n]["category"] for n in both}]
    print(
        f"   the set's categories: {len(sizes)}; with 1 question {sum(s == 1 for s in sizes)}, 2-6 "
        f"{sum(2 <= s <= 6 for s in sizes)}, more {sum(s > 6 for s in sizes)} (largest {max(sizes)})"
    )


def show(n, lens):
    i = items[n]
    print(f"\n{n}: bridge {i['intermediate']!r} -> {i['swap_to']!r}, answer {i['answer']!r} -> {i['swap_answer']!r}")
    print(f"   clean          {i['clean_continuation']!r}")
    for kind in KINDS:
        o = out[(lens, *CUE, kind, False, n)]
        print(f"   {kind:14s} {o['continuation']!r:42s} changed={o['flip']}, kept clean={o['kept_clean']}")


for lens in ("jpp", "jlens"):
    moved = [
        n
        for n in both
        if any(not out[(lens, *CUE, k, False, n)]["kept_clean"] for k in ("bridge_pinned", "answer_pinned"))
    ]
    print(
        f"\n== {lens}, cue phrase: every question a pinned swap changes or makes lose the clean answer ({len(moved)})"
    )
    for n in moved:
        show(n, lens)

print("\n== Four other questions by seed 0, J++, cue phrase: the greedy continuation per swap")
for n in random.Random(0).sample(both, 4):
    show(n, "jpp")
