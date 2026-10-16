"""B3 (exp07, exp08, exp04 positions_window): on brew, the lens reads the intermediate I at a few positions, but
writing along its direction does not take the step; a code fit on other items, nearly orthogonal to it, does.

Reads only raw result files (no code from this repo; standard library only):
  results/exp07_step_code/code_v1/{items,outcomes,diagnostics}.jsonl     WRITE: edits at the window, one layer at a time
  results/exp08_brew_read/read_v1/reads.jsonl                            READ: colour ranks per position, clean prompts
  results/exp04_brew_patch/positions_window/{items,outcomes}.jsonl       POSITIONS: C's copy at subsets of positions
  results/exp04_brew_patch/{patch_map_fresh,patch_map}/items.jsonl       the items' colours (I, X, f(X)), for examples
Run from the repo root:  python3 verification/b3_exp07_exp08.py

Conventions in the files: an outcome's "role" is the continuation's first palette colour as a role of the item
(b = f(X), the step; X; I; A = the original answer; c; ...). exp08's colour ranks are 0-based among the 12 palette
colours (0 = top-1), one entry per position after the start line (21 positions; 14 = the newline after
"assistant").
"""

import json
import math
import random
from pathlib import Path

EXP07 = "results/exp07_step_code/code_v1"
EXP08 = "results/exp08_brew_read/read_v1"
POS = "results/exp04_brew_patch/positions_window"
MAPS = {"fresh": "results/exp04_brew_patch/patch_map_fresh", "bank": "results/exp04_brew_patch/patch_map"}
WINDOW = range(36, 51, 2)  # layers 36..50, every second
STEP = "b"  # role label of f(X)
ASSISTANT_NL = 14  # position index of the newline after "assistant"
LAST = 20  # the final ":" (the prompt's last token)
N_BOOT = 10000


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def boot_mean(values, seed=0):
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(N_BOOT))
    return sum(values) / n, means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT) - 1]


def pct(x):
    return f"{100 * x:.0f}%"


def pts(m, lo, hi):
    return f"{100 * m:+.0f} [{100 * lo:+.0f}, {100 * hi:+.0f}] pts"


def median(values):
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


eligible = {
    s: sorted(r["name"] for r in jsonl(f"{EXP07}/items.jsonl") if r["set"] == s and r["status"] == "eligible")
    for s in ("fresh", "bank")
}
print(f"eligible items: fresh {len(eligible['fresh'])}, bank {len(eligible['bank'])}  (README: 154, 82)")
roles = {s: {r["name"]: r.get("roles") for r in jsonl(f"{MAPS[s]}/items.jsonl")} for s in MAPS}

# ---------------------------------------------------------------- 1. WRITE (exp07)
out7 = jsonl(f"{EXP07}/outcomes.jsonl")
cell7 = {(o["set"], o["name"], o["layer"], o["direction"], o["dose"], o["lens"]): o for o in out7}


def step_scores(s, direction, lens=None, dose="copy"):
    """Per item: share of the 8 window layers at which the edit gives f(X)."""
    return {
        n: sum(cell7[s, n, layer, direction, dose, lens]["role"] == STEP for layer in WINDOW) / len(WINDOW)
        for n in eligible[s]
    }


EDITS = [
    ("copy (h_C - h_B)", "copy", None),
    ("code E_I[X] - E_I[I]", "code", None),
    ("random direction", "random", None),
    ("J++ lens direction v_X - v_I", "lens", "jpp"),
    ("J-lens lens direction", "lens", "jlens"),
]
README_WRITE = {
    "fresh": {"copy": "31%", "code": "34%", "random": "0%", "lens/jpp": "1%", "lens/jlens": "1%"},
    "bank": {"copy": "31%", "code": "25%", "random": "-", "lens/jpp": "1%", "lens/jlens": "-"},
}
print("\n== 1. WRITE (exp07): share of window layers (36-50) at which the edit gives f(X), all edits at the copy's size")
for s in ("fresh", "bank"):
    print(f"   {s} (n={len(eligible[s])}); rate = item x layer cells, Wilson CI over cells / bootstrap CI over items")
    scores = {}
    for label, direction, lens in EDITS:
        sc = step_scores(s, direction, lens)
        scores[direction, lens] = sc
        k = sum(round(v * len(WINDOW)) for v in sc.values())
        n = len(sc) * len(WINDOW)
        lo, hi = wilson(k, n)
        m, blo, bhi = boot_mean(list(sc.values()))
        key = direction if lens is None else f"{direction}/{lens}"
        print(
            f"     {label:30s} {k:4d}/{n} = {pct(k / n):>4s}  Wilson [{pct(lo)}, {pct(hi)}]  items [{pct(blo)}, {pct(bhi)}]"
            f"   README: {README_WRITE[s].get(key, '-')}"
        )
    for a, b, readme in (
        (("code", None), ("lens", "jpp"), {"fresh": "+33 [+27, +38]", "bank": "-"}),
        (("code", None), ("lens", "jlens"), {"fresh": "+33 [+28, +38]", "bank": "-"}),
        (("code", None), ("random", None), {"fresh": "+34 [+29, +39]", "bank": "-"}),
        (("copy", None), ("random", None), {"fresh": "+31 [+26, +36]", "bank": "-"}),
    ):
        diff = [scores[a][n] - scores[b][n] for n in eligible[s]]
        label = f"{a[0]} - {b[0]}{' (' + b[1] + ')' if b[1] else ''}"
        print(f"     paired {label:22s} {pts(*boot_mean(diff))}   README: {readme[s]}")

diag = jsonl(f"{EXP07}/diagnostics.jsonl")
for lens in ("jpp", "jlens"):
    cos = [d["value"] for d in diag if d["what"] == "cos code~lens" and d["lens"] == lens]
    share = [d["value"] for d in diag if d["what"] == "code jspace share" and d["lens"] == lens]
    print(
        f"   cosine(code, {lens} lens direction), median over item x layer: {median(cos):.3f} (n={len(cos)})"
        f"   README: 0.02;  code's J-space share median {median(share):.2f}  README: 0.09-0.11"
    )

# ---------------------------------------------------------------- 2. READ (exp08)
reads = jsonl(f"{EXP08}/reads.jsonl")
rk = {(r["set"], r["reader"], r["layer"], r["name"]): r["colour_rank"] for r in reads}
print("\n== 2. READ (exp08, clean prompts): is the colour top-1 among the 12 palette colours?")
print("   (a) layer 36, the newline after 'assistant' (position 14): share of items")
README_READ = {("fresh", "jpp"): "61% (X 2-6%)", ("fresh", "jlens"): "47%", ("bank", "jpp"): "55%",
               ("bank", "jlens"): "54%"}  # fmt: skip
for s in ("fresh", "bank"):
    for reader in ("jpp", "jlens", "logit", "code"):
        if (s, reader, 36, eligible[s][0]) not in rk:
            continue
        i_first = sum(rk[s, reader, 36, n]["I"][ASSISTANT_NL] == 0 for n in eligible[s])
        x_first = sum(rk[s, reader, 36, n]["X"][ASSISTANT_NL] == 0 for n in eligible[s])
        n = len(eligible[s])
        lo, hi = wilson(i_first, n)
        readme = README_READ.get((s, reader), "88%" if (s, reader) == ("fresh", "code") else "-")
        print(
            f"     {s:5s} {reader:6s} I first {i_first:3d}/{n} = {pct(i_first / n):>4s} [{pct(lo)}, {pct(hi)}]"
            f"   X first {pct(x_first / n):>4s}   README: {readme}"
        )
print("   (b) pooled over the window: per item, share of (window layer, position) cells with the colour top-1")
README_POOL = {"jpp": "15% vs 8%, +7 [+5, +9]", "jlens": "12% vs 8%, +5 [+2, +7]",
               "logit": "12% vs 7%, +5 [+2, +7]", "code": "41% vs 4%, +36 [+32, +40]"}  # fmt: skip
for reader in ("jpp", "jlens", "logit", "code"):
    per_i, per_x = [], []
    for n in eligible["fresh"]:
        cells_i = [v == 0 for layer in WINDOW for v in rk["fresh", reader, layer, n]["I"]]
        cells_x = [v == 0 for layer in WINDOW for v in rk["fresh", reader, layer, n]["X"]]
        per_i.append(sum(cells_i) / len(cells_i))
        per_x.append(sum(cells_x) / len(cells_x))
    diff = [a - b for a, b in zip(per_i, per_x, strict=True)]
    print(
        f"     fresh {reader:6s} I {pct(sum(per_i) / len(per_i)):>4s}  X {pct(sum(per_x) / len(per_x)):>4s}"
        f"  I - X {pts(*boot_mean(diff))}   README: {README_POOL[reader]}"
    )
print("   (c) the best (layer, position) cell for I vs the same search for X (J++, fresh; 168 cells searched)")
best = {}
for role in ("I", "X"):
    best[role] = max(
        (sum(rk["fresh", "jpp", layer, n][role][p] == 0 for n in eligible["fresh"]) / len(eligible["fresh"]), layer, p)
        for layer in WINDOW
        for p in range(21)
    )
print(
    f"     I: {pct(best['I'][0])} at layer {best['I'][1]}, position {best['I'][2]};"
    f"  X: {pct(best['X'][0])} at layer {best['X'][1]}, position {best['X'][2]}   README: I 61% (L36, pos 14), X at most 13-16%"
)
print("   (d) positive control: the answer A top-1 at the last token, layer 62 (fresh)")
for reader in ("jpp", "jlens", "logit"):
    a_first = sum(rk["fresh", reader, 62, n]["A"][LAST] == 0 for n in eligible["fresh"])
    x_first = sum(rk["fresh", reader, 62, n]["X"][LAST] == 0 for n in eligible["fresh"])
    n = len(eligible["fresh"])
    print(
        f"     {reader:6s} A {pct(a_first / n):>4s}  X {pct(x_first / n):>3s}"
        f"   README: {dict(jpp='95%', jlens='92%', logit='86%')[reader]} (X 0-1%)"
    )

# ---------------------------------------------------------------- 3. POSITIONS (exp04 positions_window)
pos_out = jsonl(f"{POS}/outcomes.jsonl")
pcell = {(o["set"], o["name"], o["layer"], o["group"], o["source"]): o["role"] for o in pos_out}
pos_elig = {s: sorted(r["name"] for r in jsonl(f"{POS}/items.jsonl") if r["set"] == s and r["status"] == "eligible")
            for s in ("fresh", "bank")}  # fmt: skip
assert pos_elig == eligible, "positions_window's eligible items differ from exp07's"


def pos_scores(s, group, source):
    return {
        n: sum(pcell[s, n, layer, group, source] == STEP for layer in WINDOW) / len(WINDOW) for n in pos_elig[s]
    }


GROUPS = [
    ("the 4 reading positions (' the', '\\n' after assistant, '\\n\\n' after </think>, ':')", "reading", "cf"),
    ("the other 17", "all_but_reading", "cf"),
    ("all 21", "all", "cf"),
    ("O's copy (off-path control) at the 4", "reading", "off"),
    ("'\\n' after assistant alone", "assistant_nl", "cf"),
    ("'\\n\\n' after </think> alone", "think_nl", "cf"),
]
README_POS = {"fresh": ["33%", "0%", "31%", "0%", "3%", "0%"], "bank": ["31%", "-", "31%", "-", "-", "-"]}
print("\n== 3. POSITIONS (exp04 positions_window): copy C's activations only at some positions; share of window")
print("   layers giving f(X)")
for s in ("fresh", "bank"):
    sc = {}
    for (label, group, source), readme in zip(GROUPS, README_POS[s], strict=True):
        sc[group, source] = pos_scores(s, group, source)
        v = list(sc[group, source].values())
        k, n = sum(round(x * len(WINDOW)) for x in v), len(v) * len(WINDOW)
        lo, hi = wilson(k, n)
        print(f"     {s:5s} {label:78s} {pct(k / n):>4s} [{pct(lo)}, {pct(hi)}]   README: {readme}")
    for a, b in ((("reading", "cf"), ("reading", "off")), (("all", "cf"), ("all_but_reading", "cf"))):
        diff = [sc[a][n] - sc[b][n] for n in pos_elig[s]]
        print(f"     {s:5s} paired {a[0]}/{a[1]} - {b[0]}/{b[1]}: {pts(*boot_mean(diff))}")

# ---------------------------------------------------------------- 4. Examples
print("\n== 4. Five fresh items by seed 0; edits at layer 48 (copy's size); J++'s read at layer 36, position 14")
for n in random.Random(0).sample(eligible["fresh"], 5):
    r = roles["fresh"][n]
    edits = {
        label: cell7["fresh", n, 48, d, "copy", lens] for label, d, lens in (
            ("copy", "copy", None), ("code", "code", None), ("J++ lens dir", "lens", "jpp"))
    }  # fmt: skip
    ranks = rk["fresh", "jpp", 36, n]
    top = [role for role in ("I", "X", "S", "A") if ranks[role][ASSISTANT_NL] == 0]
    top_label = f"{top[0]} ({r[top[0]]})" if top else "another palette colour"
    print(f"\n   {n}: start {r['S']}, I = {r['I']}, X = {r['X']}, f(X) = {r['b']}, original answer {r['A']}")
    print("      layer 48: " + "; ".join(f"{k} -> {e['colour']} ({e['role']})" for k, e in edits.items()))
    print(f"      J++ top-1 colour at L36, newline after 'assistant': {top_label}; rank of I {ranks['I'][ASSISTANT_NL]}")
