"""B1 (exp02 v4): on recalled two-hop bridges, does swapping only the J-space part of the bridge's probe flip the
answer, more than the probe's remainder, the remainder with the J-space held, and a direction as aligned with the
probe as the J-space part but random otherwise?

Reads only results/exp02_swaps/{main_v4_jpp,main_v4_jlens,matched_v4_jpp,matched_v4_jlens}/{items,outcomes}.jsonl,
results/exp02_swaps/gate_v4/summary.json and data/probe_swap.json (the prompts). No code from this repo.
Standard library only. Run from the repo root:  python3 verification/b1_exp02.py
"""

import json
import math
import random
from pathlib import Path

RUNS = "results/exp02_swaps"
LENSES = {"jpp": "J++", "jlens": "J-lens"}
CONDITIONS = {  # condition -> what it swaps (the script's docstring in scripts/exp02_swaps.py)
    "raw_jlens": "raw lens vectors of bridge and target",
    "full_probe": "full probe (no lens)",
    "jpart": "J-space part of the probe",
    "remainder": "remainder (probe - J-part)",
    "remainder_clamped": "remainder, J-space held",
}
README = {  # README exp02 section, layers 24-40, all positions (flip rate, Wilson 95% CI)
    ("jpp", "raw_jlens"): "49% [38, 60]",
    ("jpp", "full_probe"): "27% [19, 38]",
    ("jpp", "jpart"): "52% [41, 63]",
    ("jpp", "remainder"): "8% [4, 16]",
    ("jpp", "remainder_clamped"): "1% [0, 7]",
    ("jlens", "raw_jlens"): "40% [30, 51]",
    ("jlens", "full_probe"): "27% [19, 38]",
    ("jlens", "jpart"): "35% [25, 46]",
    ("jlens", "remainder"): "12% [6, 21]",
    ("jlens", "remainder_clamped"): "4% [1, 11]",
}
N_BOOT = 10000


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return p, max(0.0, centre - half), min(1.0, centre + half)


def pct(k, n):
    p, lo, hi = wilson(k, n)
    return f"{100 * p:3.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


def paired_boot(a, b, seed=0):
    """Mean of a - b over items, with a percentile bootstrap CI resampling items (random.Random(seed))."""
    diffs = [x - y for x, y in zip(a, b, strict=True)]
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(N_BOOT))
    return sum(diffs) / n, means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT) - 1]


def pts(m, lo, hi):
    return f"{100 * m:+.0f} pts [{100 * lo:+.0f}, {100 * hi:+.0f}]"


prompts = {i["name"]: i["prompt"] for i in json.loads(Path("data/probe_swap.json").read_text())["items"]}
items = {i["name"]: i for i in jsonl(f"{RUNS}/main_v4_jpp/items.jsonl")}
eligible = sorted(n for n, i in items.items() if i["status"] == "eligible")
print(f"questions: {len(items)}, eligible (clean greedy continuation has the answer, not the swap answer): "
      f"{len(eligible)}")


def outcomes(run):
    """(name, condition, null) -> outcome row, eligible questions only; checks one row per key."""
    rows = {}
    for o in jsonl(f"{RUNS}/{run}/outcomes.jsonl"):
        assert o["band"] == "24-40", o["band"]
        key = (o["name"], o["condition"], o["null"])
        assert key not in rows, f"duplicate row {key}"
        rows[key] = o
    names = {k[0] for k in rows}
    assert names == set(eligible), f"{run}: outcome questions differ from the eligible set"
    return rows


main = {lens: outcomes(f"main_v4_{lens}") for lens in LENSES}
matched = {lens: outcomes(f"matched_v4_{lens}") for lens in LENSES}

gate = json.loads(Path(f"{RUNS}/gate_v4/summary.json").read_text())["decision"]
print(f"\nNOTE: the gate run (gate_v4) FAILED its own rule: band {gate['band']}, full-probe flip rate "
      f"{100 * gate['full_probe_flip_rate']:.0f}% < threshold {100 * gate['threshold']:.0f}% (go={gate['go']}). "
      "main was run anyway by the human's choice (main's manifest says so).")

print("\n== 1. Flip rate per swap, layers 24-40, every position from 1 (n = eligible questions; Wilson 95% CI)")
print("   flip = swapped greedy continuation has the swap answer and not the clean answer (criterion C)")
print("   kept = still has the clean answer; neither = collateral damage (neither answer)")
for lens, title in LENSES.items():
    print(f"\n   {title}")
    for cond, desc in CONDITIONS.items():
        for null in (False, True):
            rows = [main[lens][n, cond, null] for n in eligible]
            k_flip = sum(r["flip"] for r in rows)
            k_kept = sum(r["kept_clean"] for r in rows)
            k_neither = sum(not r["flip"] and not r["kept_clean"] for r in rows)
            label = f"{desc}{' -- random-direction null' if null else ''}"
            readme = "" if null else f"   README: {README[lens, cond]}"
            print(f"   {label:58s} flip {pct(k_flip, len(rows))}  kept {pct(k_kept, len(rows))}  "
                  f"neither {100 * k_neither / len(rows):3.0f}%{readme}")

print("\n   Check: the full probe uses no lens, so its rows should be identical in the two runs:")
same = sum(main["jpp"][n, "full_probe", False]["flip"] == main["jlens"][n, "full_probe", False]["flip"]
           for n in eligible)
print(f"   full-probe flip labels identical in J++ and J-lens runs: {same}/{len(eligible)}")

print(f"\n== 2. Paired difference, J-space part minus remainder (same questions; bootstrap {N_BOOT}, seed 0)")
readme_diff = {"jpp": "+44 [+32, +56]", "jlens": "+23 [+13, +35]"}
for lens, title in LENSES.items():
    a = [main[lens][n, "jpart", False]["flip"] for n in eligible]
    b = [main[lens][n, "remainder", False]["flip"] for n in eligible]
    print(f"   {title:6s} {pts(*paired_boot(a, b))}   README: {readme_diff[lens]} pts (README used B=2000)")

print("\n== 3. Matched-alignment control (matched_v4_*): per entity and layer a unit direction with the J-part's")
print("   cosine to the probe, the rest random. Same questions, same band.")
readme_matched = {"jpp": ("14% [8, 24]", "+38 [+27, +49]"), "jlens": ("10% [5, 19]", "+25 [+16, +34]")}
for lens, title in LENSES.items():
    jp = [matched[lens][n, "jpart", False]["flip"] for n in eligible]
    mt = [matched[lens][n, "jpart_matched", False]["flip"] for n in eligible]
    mt_null = [matched[lens][n, "jpart_matched", True]["flip"] for n in eligible]
    mt_kept = sum(matched[lens][n, "jpart_matched", False]["kept_clean"] for n in eligible)
    repro = sum(matched[lens][n, "jpart", False]["flip"] == main[lens][n, "jpart", False]["flip"] for n in eligible)
    print(f"   {title}: J-part {pct(sum(jp), len(jp))} | matched {pct(sum(mt), len(mt))} "
          f"(README {readme_matched[lens][0]}), kept {pct(mt_kept, len(mt))} | matched null "
          f"{pct(sum(mt_null), len(mt_null))}")
    print(f"          J-part minus matched: {pts(*paired_boot(jp, mt))}   README: {readme_matched[lens][1]} pts")
    print(f"          J-part labels reproduce main_v4_{lens} item for item: {repro}/{len(eligible)}")
    ej = sorted(matched[lens][n, "jpart", False]["edit_ratio"] for n in eligible)[len(eligible) // 2]
    em = sorted(matched[lens][n, "jpart_matched", False]["edit_ratio"] for n in eligible)[len(eligible) // 2]
    print(f"          median edit (|delta|/|h| at the last position): J-part {ej:.3f}, matched {em:.3f}")

print("\n== 4. Five eligible questions by seed 0 (random.Random(0).sample), J++ run, J-space-part swap")
for n in random.Random(0).sample(eligible, 5):
    i = items[n]
    r = main["jpp"][n, "jpart", False]
    print(f"\n{n}: {prompts[n].rstrip()!r}")
    print(f"   bridge {i['intermediate']!r} -> swapped to {i['swap_to']!r}; "
          f"answer {i['answer']!r}, swap answer {i['swap_answer']!r}")
    print(f"   clean continuation:   {i['clean_continuation']!r}")
    print(f"   J-part swapped:       {r['continuation']!r}   flip={r['flip']} kept_clean={r['kept_clean']}")
