"""Per-layer write table from a read_write run's outcomes.jsonl: lens / random flips (%) per family, layer and scale, and
the copy's flips. Writes nothing; print it. python scripts/rw_per_layer.py RUN"""

import collections
import json
import sys

run = sys.argv[1]
rows = [json.loads(line) for line in open(f"results/read_write/{run}/outcomes.jsonl")]
agg = collections.defaultdict(list)
for r in rows:
    if r["null"]:
        continue
    agg[(r["family"], r["layer"], r["part"])].append(r["role"] == "b")
layers = sorted({r["layer"] for r in rows}, key=lambda x: (isinstance(x, str), x))
for fam in ("BL", "BR", "RL", "RR", "R", "B"):
    print(fam)
    for la in layers:
        cells = []
        for sc in ("0.5", "1", "2", "4", "8", "16"):
            l, rnd = agg.get((fam, la, f"lens_x{sc}")), agg.get((fam, la, f"random_x{sc}"))
            if l:
                cells.append(f"x{sc} {100 * sum(l) / len(l):3.0f}/{100 * sum(rnd) / len(rnd):<3.0f}")
        c = agg.get((fam, la, "copy"))
        print(f"  L{la}: " + "  ".join(cells) + (f"  | copy {100 * sum(c) / len(c):.0f}" if c else ""))
