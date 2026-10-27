"""Finding 5, recomputed from the raw rows: an order label for the 1st and 2nd sentence, the bridge's identity after.

Standalone: numpy and the standard library, no repo code. Reads results/pointer_swap/<run>/{manifest.json,outcomes.jsonl}
and the item files the manifest pins (sha256-checked), and compares every cell with
results/cross_model/20261023T091847Z/grid.csv (the grid README cites; --grid=STAMP for another). Run from the repo root
(numpy: the project env):
    uv run python verification/finding5_2026-10-23/recompute.py            # the table, OK / MISMATCH per cell
    uv run python verification/finding5_2026-10-23/recompute.py --example  # the worked examples of claim.md (seed 0)

Rule (scripts/finding5_confirm.py, committed at 6538445 before the fresh draws): memory -> prompt (RL), the donor's last
two tokens copied into the original at one layer (source dissoc, group last). k = the place of the donor's asked sentence
(item slots.position + 1). Per item: position = the answer is the original's k-th sentence's digit; identity = the
digit of the original's sentence about the donor's entity. A: k = 1-2, position - identity, its 95% lower bound > 0.
B: k = 3..N, identity - position >= 0 with its lower bound >= -0.05. Holds iff A and B. Layer: Qwen3.6-27B 50 (fixed);
else the last swept layer where the donor's own digit (role value) has its Wilson upper bound < 10%. Interval: the
original's asked entity resampled with replacement within its topic, 4,000 draws, numpy default_rng(0), 2.5-97.5th
percentile (the same draws as bridge_jspace.stats.cluster_bootstrap, so the bounds match to the digit).
"""

import csv
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
STAMP = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--grid=")), "20261023T091847Z")
GRID = REPO / "results/cross_model" / STAMP / "grid.csv"
FINDING = "Order label for the 1st and 2nd sentence, the bridge's identity after"
SETTINGS = (("draw 1", None, 5), ("draw 2", None, 5), ("draw 3", None, 5), ("8 sentences", "e8-digit", 8),
            ("12 sentences", "e12-word", 12))  # fmt: skip
# model -> runs of draw 1, 2, 3, 8 and 12 sentences (None: no run; README, "Runs", finding 5)
RUNS = {
    "Qwen3.6-27B": ("d3v4_swap_topics", "d3v4_seed2_swap_27b", "d3v4_seed3_swap_27b", "d3v5_len8_swap_27b",
                    "d3v5_len12_swap_27b"),
    "Qwen3.5-9B": ("qwen35_9b_d3v4_swap_r2", "qwen35_9b_d3v4_seed2_swap", "qwen35_9b_d3v4_seed3_swap",
                   "qwen35_9b_d3v5_len8_swap", "qwen35_9b_d3v5_len12_swap"),
    "Olmo-Hybrid-7B": ("olmo_hybrid_7b_d3v4_swap_fn", "olmo_hybrid_7b_d3v4_seed2_swap", None,
                       "olmo_hybrid_7b_d3v5_len8_swap", "olmo_hybrid_7b_d3v5_len12_swap"),
    "Qwen3.5-122B": ("qwen35_122b_d3v4_swap", "qwen35_122b_d3v4_seed2_swap", "qwen35_122b_d3v4_seed3_swap",
                     "qwen35_122b_d3v5_len8_swap", "qwen35_122b_d3v5_len12_swap"),
    "Qwen3-32B": ("qwen3_32b_d3v4_swap_r2", "qwen3_32b_d3v4_seed2_swap", "qwen3_32b_d3v4_seed3_swap",
                  "qwen3_32b_d3v5_len8_swap", "qwen3_32b_d3v5_len12_swap"),
    "OLMo-3-7B-I": ("olmo3_7b_instruct_d3v4_swap_fn", "olmo3_7b_instruct_d3v4_seed2_swap",
                    "olmo3_7b_instruct_d3v4_seed3_swap", "olmo3_7b_instruct_d3v5_len8_swap",
                    "olmo3_7b_instruct_d3v5_len12_swap"),
    "Muse 30B": ("muse30b_d3v4_swap", "muse30b_d3v4_seed2_swap", "muse30b_d3v4_seed3_swap", "muse30b_d3v5_len8_swap",
                 "muse30b_d3v5_len12_swap"),
    "Gemma 4 31B-it": ("gemma4it_d3v4_swap_v2_r2", "gemma4it_d3v4_seed2_swap", "gemma4it_d3v4_seed3_swap", None, None),
}  # fmt: skip


def wilson(k, n, z=1.96):
    p = k / n
    mid, half = (
        (p + z * z / (2 * n)) / (1 + z * z / n),
        z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n),
    )
    return p, mid - half, mid + half


def load(run, level, sentences):
    """(manifest, the RL rows of every source at the last two tokens of `level`, each with k and its entity, items)."""
    d = REPO / "results/pointer_swap" / run
    m = json.loads((d / "manifest.json").read_text())
    items = {}
    for pin in m["items"].values():
        raw = (REPO / pin["file"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin["sha256"], pin["file"]
        items |= {it["id"]: it for it in json.loads(raw)["items"]}
    rows = []
    for line in (d / "outcomes.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["family"] == "RL" and r["group"] == "last" and (level is None or r["level"] == level):
            it = items[r["name"]]
            assert len(it["entities"]) == sentences, (run, r["name"])
            rows.append(r | {"k": it["slots"]["position"] + 1, "entity": f"{it['domain']}:{it['query']}"})
    return m, rows, items


def diff(rows, a, b):
    """mean(1[role a] - 1[role b]) with the entity-cluster bootstrap 95% interval (within topic)."""
    groups = {}
    for r in rows:
        g = groups.setdefault(r["domain"], {}).setdefault(r["entity"], [0.0, 0])
        g[0] += (r["role"] == a) - (r["role"] == b)
        g[1] += 1
    rng, tot, cnt = np.random.default_rng(0), np.zeros(4000), np.zeros(4000)
    for dom in sorted(groups):
        keys = sorted(groups[dom])
        pick = rng.integers(0, len(keys), size=(4000, len(keys)))
        tot += np.array([groups[dom][k][0] for k in keys])[pick].sum(1)
        cnt += np.array([groups[dom][k][1] for k in keys], dtype=float)[pick].sum(1)
    lo, hi = np.quantile(tot / cnt, [0.025, 0.975])
    return sum(g[0] for gs in groups.values() for g in gs.values()) / len(rows), float(lo), float(hi)


def cell(model, setting, run, level, sentences):
    m, rows, _ = load(run, level, sentences)
    dis = [r for r in rows if r["source"] == "dissoc"]
    if model == "Qwen3.6-27B" and setting.startswith("draw"):
        layer = 50
    else:  # the donor-digit rule over the run's swept layers
        ok = []
        for la in m["layers"]:
            sel = [r for r in dis if r["layer"] == la]
            if wilson(sum(r["role"] == "value" for r in sel), len(sel))[2] < 0.10:
                ok.append(la)
        layer = max(ok)
    at = [r for r in dis if r["layer"] == layer]
    first2, rest = [r for r in at if r["k"] <= 2], [r for r in at if r["k"] >= 3]
    a, b = diff(first2, "position", "identity"), diff(rest, "identity", "position")
    pa, pb = a[1] > 0, b[0] >= 0 and b[1] >= -0.05
    verdict = "holds" if pa and pb else f"fails (partly: A {pa}, B {pb})" if pa or pb else "fails"
    rand = [r["role"] != "none" for r in rows if r["source"] == "rand" and r["layer"] == layer]
    rand = sum(rand) / len(rand) if rand else math.nan
    if model == "Muse 30B" and setting == "draw 1" and rand > 0.30:  # the Muse spec's random-patch gate
        verdict = "not interpretable"
    return layer, (len(first2), a), (len(rest), b), verdict, rand


def main():
    grid = {
        (g["model"], g["setting"]): g for g in csv.DictReader(GRID.read_text().splitlines()) if g["finding"] == FINDING
    }
    bad = done = 0
    print(f"{'model':15s} {'setting':12s} {'layer':>5s}  {'n':>4s} {'1st-2nd: pos - id':>23s}  {'n':>4s} "
          f"{'3rd on: id - pos':>23s}  {'random push':>11s}  {'verdict':28s} grid")  # fmt: skip
    for model, runs in RUNS.items():
        for (setting, level, sentences), run in zip(SETTINGS, runs, strict=True):
            if run is None:
                print(f"{model:15s} {setting:12s} {'-':>5s}  no run; grid: {grid[(model, setting)]['verdict']}")
                continue
            layer, (n1, a), (n2, b), verdict, rand = cell(model, setting, run, level, sentences)
            same = True
            for part, n, x in (("1st-2nd", n1, a), ("3rd on", n2, b)):
                g = grid[(model, f"{setting}, {part}")]
                glo, ghi = (float(v) for v in g["95% CI"].strip("[]").split(", "))
                same &= g["n"] == str(n) and g["verdict"].split(" (")[0] == verdict.split(" (")[0]
                same &= math.isclose(float(g["value"].split()[0]), round(100 * x[0], 1), abs_tol=1e-9)
                same &= math.isclose(glo, round(100 * x[1], 1), abs_tol=1e-9)
                same &= math.isclose(ghi, round(100 * x[2], 1), abs_tol=1e-9)
                same &= f"layer {layer} " in g["chance or control level"]
            bad += not same
            done += 1
            fmt = lambda x: f"{100 * x[0]:+6.1f} [{100 * x[1]:+6.1f}, {100 * x[2]:+6.1f}]"  # noqa: E731
            print(f"{model:15s} {setting:12s} {layer:5d}  {n1:4d} {fmt(a)}  {n2:4d} {fmt(b)}  {100 * rand:10.0f}%  "
                  f"{verdict:28s} {'OK' if same else 'MISMATCH'}")  # fmt: skip
    print(f"\n{done} model/setting cells (each a 1st-2nd and a 3rd-on row of grid.csv) recomputed, {done - bad} match, "
          f"{bad} mismatch. 'random push': % of answers a same-size random push at the last two tokens changes "
          "(reported; decisive only for Muse draw 1, > 30% = not interpretable)")  # fmt: skip
    return 1 if bad else 0


def example(seed=0):
    """Qwen3.6-27B's third draw (fresh scenes, rule fixed before the run), layer 50: one item with k <= 2 and one with
    k >= 3, each drawn with random.Random(seed) from the sorted item ids of its half."""
    _, rows, items = load("d3v4_seed3_swap_27b", None, 5)
    at = {r["name"]: r for r in rows if r["source"] == "dissoc" and r["layer"] == 50}
    for half in ((1, 2), (3, 4, 5)):
        name = random.Random(seed).choice(sorted(n for n, r in at.items() if r["k"] in half))
        it, r = items[name], at[name]
        don = it["sources"]["dissoc"]
        print(f"seed {seed}, k in {half}: item {name} (run d3v4_seed3_swap_27b, layer 50)")
        print(f"  original: {it['context']} {it['question']}  (answer {it['answer']})")
        print(f"  donor:    {don['context']} {don['question']}  (asks its sentence {r['k']}, answer {don['answer']})")
        print(f"  digits by outcome: {don['predictions']}")
        print(f"  patched answer: {r['top']!r} = {r['role']}")


if __name__ == "__main__":
    sys.exit(example() if "--example" in sys.argv else main())
