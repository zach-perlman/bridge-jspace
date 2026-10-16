"""B4 (exp18 v3): on brew, do the verbalizers (the NLA at layer 42, the oracle lens at layer 44) report the colour
written into the vector whether or not the model uses it?

Each eligible brew item is edited three ways at every position after the start line, layers 36-40, each edit at the
norm of exp04's copy h_C - h_B at its layer and position: exp07's code for the intermediate (E_I[X] - E_I[I], which
the model computes with), J++'s direction v_X - v_I (which exp07 found the model ignores), and a random direction.
The readers read the edited vectors at two positions (the newline after "assistant", the last token).

Reads only results/exp18_brew_verbalizers/20261015-230148/{items,reads}.jsonl. No code from this repo; standard
library only. Run from the repo root:  python3 verification/b4_exp18.py

"Names X" is a string match, not a judge: a reading names a colour if the colour's English word appears as a whole word
(no letter or digit on either side), ignoring case and a plural "s"/"es" (the regex below, the same rule the run used;
part 0 re-applies it to every stored reading text). Chinese colour names are not counted. Per item, a colour counts as
named if the reading at either of the two positions names it (the rule fixed in the run's manifest).
"""

import json
import math
import random
import re
from pathlib import Path

RUN = Path("results/exp18_brew_verbalizers/20261015-230148")
READERS = {"nla": 42, "oracle": 44}  # reader -> the layer it reads
EDITS = ("code", "lens", "random")
CONDITIONS = ("clean", *EDITS)  # clean = B as written
N_BOOT = 10000


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.959964):
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return p, max(0.0, centre - half), min(1.0, centre + half)


def pct(k, n):
    p, lo, hi = wilson(k, n)
    return f"{100 * p:5.1f}% [{100 * lo:.1f}, {100 * hi:.1f}] ({k}/{n})"


def paired_boot(a, b, seed=0):
    """Mean of a - b over items, with a percentile 95% CI from resampling items (random.Random(seed))."""
    diffs = [x - y for x, y in zip(a, b, strict=True)]
    rng, n = random.Random(seed), len(diffs)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(N_BOOT))
    return sum(diffs) / n, means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT) - 1]


def named(word, text):
    return re.search(rf"(?<![^\W_]){re.escape(word)}(?:e?s)?(?![^\W_])", text, flags=re.IGNORECASE) is not None


items = jsonl(RUN / "items.jsonl")
reads = jsonl(RUN / "reads.jsonl")
by_name = {i["name"]: i for i in items}
eligible = [i for i in items if i["status"] == "eligible"]
took = [i["name"] for i in eligible if i["code_took"]]

print("== 0. Files and the naming rule")
print(f"   items: {len(items)} rows, eligible {len(eligible)}   README: 680 eligible (84 bank, 155 fresh, 441 test)")
for s in ("bank", "fresh", "test"):
    print(f"      {s}: eligible {sum(i['set'] == s for i in eligible)}")
verbal = [r for r in reads if r["reader"] in READERS]
roles_checked, disagree = 0, 0
for r in verbal:
    row = by_name[r["name"]]
    colours = {**{k: row["roles"][k] for k in ("I", "X", "A")}, "b": row["roles"]["b"], "null": row["null"]}
    for role, colour in colours.items():
        roles_checked += 1
        disagree += named(colour, r["text"]) != r[f"names_{role}"]
print(f"   re-applied the whole-word match to {len(verbal)} verbalizer readings x 5 colours: {disagree} of "
      f"{roles_checked} stored flags differ (expect 0)")
readers_layers = sorted({(r["reader"], r["layer"]) for r in verbal})
print(f"   reader/layer pairs in the file: {readers_layers}   (NLA reads layer 42, the oracle lens layer 44)")

print("\n== 1. How often each edit makes the model take X as its step (answer f(X)), all eligible items")
for e in EDITS:
    k = sum(i[f"{e}_took"] for i in eligible)
    lost = sum(i[f"{e}_answer"] != "A" for i in eligible)
    print(f"   {e:6s} took {pct(k, len(eligible))}   lost the clean answer A {pct(lost, len(eligible))}")
print("   README: code 57% (57.4), J++ direction 4% (4.1), random 0.6%; J++'s direction loses A on 24% of items")

# The not-took sample: the run drew it as random.Random(0).sample(eligible-but-not-took, 100), in items.jsonl order.
rest = [i["name"] for i in eligible if not i["code_took"]]
sample = random.Random(0).sample(rest, min(100, len(rest)))
read_names = {r["name"] for r in verbal}
print(f"\n   items read by the verbalizers: {len(read_names)} = {len(took)} where the code took + "
      f"{len(read_names) - len(took)} others   README: 390 + a sample of 100")
print(f"   the sample redrawn here (random.Random(0), 100 of the {len(rest)} not-took items) matches the file's: "
      f"{set(sample) == read_names - set(took)}")


def item_flags(reader, condition, names):
    """Per item: (names X, names I, names f(X)) at either read position."""
    layer = READERS[reader]
    hit = {}
    for r in verbal:
        if r["reader"] == reader and r["layer"] == layer and r["condition"] == condition and r["name"] in names:
            old = hit.get(r["name"], (False, False, False))
            hit[r["name"]] = (old[0] or r["names_X"], old[1] or r["names_I"], old[2] or r["names_b"])
    return hit


readme = {
    ("nla", "clean"): "29%", ("nla", "code"): "68%", ("nla", "lens"): "99%",
    ("oracle", "clean"): "24%", ("oracle", "code"): "64%", ("oracle", "lens"): "99%",
}  # fmt: skip
print(f"\n== 2. On the {len(took)} items where the code took: share of items whose readings name X (and I, f(X))")
flags = {(rd, c): item_flags(rd, c, set(took)) for rd in READERS for c in CONDITIONS}
for rd in READERS:
    for c in CONDITIONS:
        f = flags[rd, c]
        n = len(f)
        x, i_, b = (sum(v[j] for v in f.values()) for j in range(3))
        note = f"   README: {readme[rd, c]}" if (rd, c) in readme else ""
        print(f"   {rd:6s} {c:6s} names X {pct(x, n)}   names I {100 * i_ / n:5.1f}%   names f(X) {100 * b / n:5.1f}%{note}")

print("\n== 3. d = [names X] - [names I] per item; paired differences over the same items (bootstrap 95% CI)")
readme_d = {"nla": "-29 [-34, -24]", "oracle": "-36 [-41, -31]"}
for rd in READERS:
    d = {c: {n: float(v[0]) - float(v[1]) for n, v in flags[rd, c].items()} for c in CONDITIONS}
    names = sorted(set.intersection(*(set(d[c]) for c in CONDITIONS)))
    for a, b in (("code", "lens"), ("code", "clean"), ("lens", "clean"), ("random", "clean")):
        m, lo, hi = paired_boot([d[a][n] for n in names], [d[b][n] for n in names])
        note = f"   README: {readme_d[rd]} pts" if (a, b) == ("code", "lens") else ""
        print(f"   {rd:6s} d({a}) - d({b}): {100 * m:+5.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts (n={len(names)}){note}")
    fx = [float(flags[rd, "code"][n][2]) for n in names], [float(flags[rd, "lens"][n][2]) for n in names]
    m, lo, hi = paired_boot(*fx)
    print(f"   {rd:6s} names f(X), code minus J++ direction: {100 * m:+5.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts"
          + ("   README: NLA 9% vs 12%" if rd == "nla" else ""))

not_took = sorted(read_names - set(took))
print(f"\n== 4. Where the code edit did NOT take (the sample, n={len(not_took)}): share of items naming X")
for rd in READERS:
    for c in ("clean", "code"):
        f = item_flags(rd, c, set(not_took))
        x = sum(v[0] for v in f.values())
        ref = {("nla", "code"): "60%", ("oracle", "code"): "61%", ("nla", "clean"): "14%", ("oracle", "clean"): "15%"}
        print(f"   {rd:6s} {c:6s} names X {pct(x, len(f))}   README: {ref[rd, c]}")

print("\n== 5. Four items by seed 0 (from the items the verbalizers read), the reading at the last token")
texts = {(r["reader"], r["name"], r["condition"], r["position"]): r["text"] for r in verbal}
for n in random.Random(0).sample(sorted(read_names), 4):
    row = by_name[n]
    took_str = ", ".join(f"{e} {'took' if row[f'{e}_took'] else 'no'}" for e in EDITS)
    print(f"\n{n}: S {row['roles']['S']}, I {row['roles']['I']}, X {row['roles']['X']}, f(X) {row['roles']['b']}, "
          f"A {row['roles']['A']}   [{took_str}]")
    for rd in READERS:
        for c in ("code", "lens"):
            t = texts[rd, n, c, "last"].replace("\n", " | ")
            print(f"   {rd:6s} {c:5s}: {t[:200]}")
