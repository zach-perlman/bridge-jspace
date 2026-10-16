"""B2 (exp04): without a lens, where does brew carry its intermediate, and is the part of the copy that carries it
inside the J-space?

Brew: the prompt gives a colour table and a start colour S; the answer A is two lookups away (S -> I -> A). The
counterfactual C changes two rules so that S -> X and X -> c. Copying C's activations into the original run at one
layer, at the positions after the start line, gives:
  b = f(X) in the ORIGINAL table: the copy carried X as the step and the second lookup read the original table
  c = C's own answer: the copy already carried the answer
  I = the original intermediate: the model stopped after one lookup
  A = the original answer: no effect
The control O changes two rules off the path; its copy should change nothing.

Reads only results/exp04_brew_patch/{patch_map,patch_map_fresh,parts_window,parts_window_fresh}/
{items,outcomes}.jsonl and manifest.json, plus data/brew_fresh.json for the examples. No code from this repo.
Standard library only. Run from the repo root:  python3 verification/b2_exp04.py
"""

import json
import math
import random
from pathlib import Path

ROOT = Path("results/exp04_brew_patch")
SETS = {"bank": ("patch_map", "parts_window"), "fresh": ("patch_map_fresh", "parts_window_fresh")}
WINDOW = [36, 38, 40, 42, 44, 46, 48, 50]  # parts_window manifest: the map's after_start window
N_BOOT = 10000
rng = random.Random(0)


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def pct(x):
    return f"{100 * x:.0f}%"


def ci(t):
    return f"{pct(t[0])} [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"


def boot_mean(values, idx_sets):
    """Mean over items and its 95% bootstrap CI (resampling items, shared resamples)."""
    n = len(values)
    means = sorted(sum(values[i] for i in idx) / n for idx in idx_sets)
    return sum(values) / n, means[int(0.025 * len(means))], means[int(0.975 * len(means)) - 1]


def pts(t):
    return f"{100 * t[0]:+.0f} [{100 * t[1]:+.0f}, {100 * t[2]:+.0f}] pts"


data = {}
for set_name, (map_run, parts_run) in SETS.items():
    items = {i["name"]: i for i in jsonl(ROOT / map_run / "items.jsonl")}
    eligible = sorted(n for n, i in items.items() if i["status"] == "eligible")
    parts_items = {i["name"]: i["status"] for i in jsonl(ROOT / parts_run / "items.jsonl")}
    data[set_name] = {
        "items": items,
        "eligible": eligible,
        "parts_eligible": sorted(n for n, s in parts_items.items() if s == "eligible"),
        "map": jsonl(ROOT / map_run / "outcomes.jsonl"),
        "parts": jsonl(ROOT / parts_run / "outcomes.jsonl"),
        "parts_manifest": json.loads((ROOT / parts_run / "manifest.json").read_text()),
    }

print("== 0. Items")
for set_name, d in data.items():
    statuses = {}
    for i in d["items"].values():
        statuses[i["status"]] = statuses.get(i["status"], 0) + 1
    print(f"   {set_name}: {len(d['items'])} items, eligible {len(d['eligible'])}   {statuses}")
    print(f"      parts run uses the same eligible items: {d['parts_eligible'] == d['eligible']}")
    print(f"      parts run's window (from its manifest): {d['parts_manifest']['layers']}")
print("   README: bank 82 eligible (13 fail on C, 4 on O, 1 no X); fresh 154 (25 clean wrong, 18 C, 2 O, 1 no X)")
print("   Eligible = the model answers the original (A), C (c) and O (A) correctly; only these are scored below.")

print("\n== 1. The map: copy C's activations after the start line at one layer (Wilson 95% CIs over items)")
print("   b = f(X) (the step), c = C's answer, I = one lookup only; 'O changed' = the off-path copy's answer != A")
readme_map = {
    "bank": "README: f(X) 11% at 36, 48% [37, 58] at 46-50; c from 52 (71%, then 93-99% from 56); O <= 2% anywhere",
    "fresh": "README: f(X) 10% at 36, 52% [44, 60] at 48; c from 52 (68%, then 88-100% from 56); O <= 6% (layer 50)",
}
for set_name, d in data.items():
    elig = set(d["eligible"])
    rows = [r for r in d["map"] if r["group"] == "after_start" and r["name"] in elig]
    layers = sorted({r["layer"] for r in rows})
    print(f"\n   {set_name} (n={len(elig)})")
    print("   layer   f(X)=b           c                I      O changed")
    window = []
    for layer in layers:
        cf = [r for r in rows if r["layer"] == layer and r["source"] == "cf"]
        off = [r for r in rows if r["layer"] == layer and r["source"] == "off"]
        b = wilson(sum(r["role"] == "b" for r in cf), len(cf))
        c = wilson(sum(r["role"] == "c" for r in cf), len(cf))
        i = wilson(sum(r["role"] == "I" for r in cf), len(cf))
        o = wilson(sum(r["role"] != "A" for r in off), len(off))
        # the manifest's window rule: b above c and above O's changed rate, Wilson intervals not overlapping
        if b[1] > c[2] and b[1] > o[2]:
            window.append(layer)
        if layer >= 28:
            print(f"   {layer:>5}   {ci(b):15s}  {ci(c):15s}  {pct(i[0]):>5}  {ci(o)}")
    max_o = max(
        sum(r["role"] != "A" for r in rows if r["layer"] == layer and r["source"] == "off") / len(elig)
        for layer in layers
    )
    print("   (layers 0-26 omitted: f(X) is 0% there; printed from 28)")
    print(f"   window by the manifest's rule: {window}   README: 36-50 (both sets)")
    print(f"   largest O changed rate at any layer: {pct(max_o)}")
    print(f"   {readme_map[set_name]}")

print("\n== 2. The split, at the window (layers 36-50, positions after the start line)")
print("   Step score = per item, the share of the 8 window layers at which that copy gives f(X); then the mean over")
print("   items (= the share of item x layer cells, since every item has all 8 layers). CIs: bootstrap over items.")
print("   Parts of the copy δ = h_C - h_B:  lens2 = δ projected on the lens vectors of I and X (rest: not_lens2);")
print("   jspace = δ's 25-atom signed decomposition over the lens's token vectors (rest: not_jspace).")
print("   Each part also has a null: the same edit size along a random direction.")
readme_parts = {
    ("bank", "jpp"): "README: full 31%; lens2 0% vs rest 31% (+31 [+24, +38]); jspace 0% vs rest 26% (+26 [+20, +32])",
    ("bank", "jlens"): "README: jspace 0% vs rest 24% (+24 [+18, +30] in summary.md); lens2 0% vs rest 30%",
    ("fresh", "jpp"): "README: full 31%; lens2 0% vs rest 31% (+31 [+26, +36]); jspace 0% vs rest 28% (+28 [+24, +33])",
    ("fresh", "jlens"): "README: lens2 0% vs rest 31% (+31 [+26, +36]); jspace 0% vs rest 26% (+26 [+22, +31])",
}
step = {}
for set_name, d in data.items():
    names = d["eligible"]
    n = len(names)
    idx_sets = [[rng.randrange(n) for _ in range(n)] for _ in range(N_BOOT)]
    cells = {}
    for r in d["parts"]:
        if r["source"] != "cf" or r["layer"] not in WINDOW:
            continue
        cells.setdefault((r["lens"], r["part"], r["null"]), {}).setdefault(r["name"], {})[r["layer"]] = r["role"]

    def score(key, names=names, cells=cells):
        per = cells[key]
        assert all(len(per[nm]) == len(WINDOW) for nm in names), f"{key}: missing window layers"
        return [sum(per[nm][layer] == "b" for layer in WINDOW) / len(WINDOW) for nm in names]

    # reproduction: the full copy must match the map's after_start rows item x layer
    map_roles = {
        (r["name"], r["layer"]): r["role"]
        for r in d["map"]
        if r["group"] == "after_start" and r["source"] == "cf" and r["layer"] in WINDOW and r["name"] in set(names)
    }
    full = cells[(None, "full", False)]
    same = sum(full[nm][layer] == map_roles[nm, layer] for nm in names for layer in WINDOW)
    print(f"\n   {set_name} (n={n}): full copy reproduces the map's cells: {same}/{n * len(WINDOW)}")
    full_score = score((None, "full", False))
    print(f"      full copy: {ci(boot_mean(full_score, idx_sets))}")
    for lens in ("jpp", "jlens"):
        print(f"      {lens}:")
        for part, rest in (("lens2", "not_lens2"), ("jspace", "not_jspace")):
            p, r_ = score((lens, part, False)), score((lens, rest, False))
            pn, rn = score((lens, part, True)), score((lens, rest, True))
            step[set_name, lens, part] = (p, r_)
            print(
                f"        {part:7s} {ci(boot_mean(p, idx_sets)):15s} null {pct(sum(pn) / n):>4} | "
                f"{rest:10s} {ci(boot_mean(r_, idx_sets)):15s} null {pct(sum(rn) / n):>4}"
            )
            diff = [b - a for a, b in zip(p, r_, strict=True)]
            p_minus_null = [a - b for a, b in zip(p, pn, strict=True)]
            print(
                f"          rest - part {pts(boot_mean(diff, idx_sets))};  part - its null "
                f"{pts(boot_mean(p_minus_null, idx_sets))}"
            )
        print(f"      {readme_parts[set_name, lens]}")
print("\n   Verdict rule (manifest): 'outside' if rest - part has CI above 0 and part - its null does not.")

print("\n== 3. Collateral: how often the copy stops the model at the first lookup (answers I) at each window layer")
readme_i = {
    "bank": "README: 20-29% at layers 36-46, 16% at 48-50",
    "fresh": "README: 27-43% at layers 36-46, 6-7% at 48-50; at the window, rest gives I in 28-30% of cells, "
    "the J-space part 1-2%, lens2 < 1%, nulls < 2%",
}
for set_name, d in data.items():
    names = set(d["eligible"])
    full = [r for r in d["parts"] if r["part"] == "full" and r["source"] == "cf" and r["name"] in names]
    by_layer = [
        sum(r["role"] == "I" for r in full if r["layer"] == layer) / len(names) for layer in WINDOW
    ]
    print(f"   {set_name}: full copy gives I: " + " ".join(f"{layer}:{pct(v)}" for layer, v in zip(WINDOW, by_layer)))
    for lens in ("jpp", "jlens"):
        shares = []
        for part in ("not_jspace", "jspace", "lens2"):
            for null in (False, True):
                rows = [
                    r
                    for r in d["parts"]
                    if r["lens"] == lens and r["part"] == part and r["null"] == null and r["name"] in names
                ]
                tag = part + (" null" if null else "")
                shares.append(f"{tag} {100 * sum(r['role'] == 'I' for r in rows) / len(rows):.1f}%")
        print(f"      {lens} share of window cells giving I: " + ", ".join(shares))
    print(f"   {readme_i[set_name]}")

print("\n== 4. Five eligible fresh items (random, seed 0), what the copy at layer 48 makes the model answer")
fresh_data = {i["name"]: i for i in json.loads(Path("data/brew_fresh.json").read_text())["items"]}
d = data["fresh"]
by = {(r["name"], r["lens"], r["part"], r["null"], r["layer"]): r for r in d["parts"] if r["source"] == "cf"}
for name in random.Random(0).sample(d["eligible"], 5):
    roles = d["items"][name]["roles"]
    item = fresh_data[name]
    path = (roles["S"], roles["I"], roles["X"])
    path_rules = [f"{k}->{item['table'][k]['stir']}" for k in path if k in item["table"]]
    print(f"\n   {name}: start S={roles['S']}, rules for S, I and X {', '.join(path_rules)}")
    print(
        f"      I={roles['I']}  answer A={roles['A']}  | C: S->{roles['X']} (X), X->{roles['c']} (c)  | "
        f"f(X) in the original table = {roles['b']}"
    )
    for label, key in (
        ("full copy        ", (name, None, "full", False, 48)),
        ("J++ J-space part ", (name, "jpp", "jspace", False, 48)),
        ("J++ rest         ", (name, "jpp", "not_jspace", False, 48)),
    ):
        r = by[key]
        print(f"      {label} -> {r['continuation']!r:12s} ({r['role']})")
