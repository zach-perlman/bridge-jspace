"""nn_order_read (Zach, 2026-10-28, prereg amendment 58 note 12, reading a): is the answer precomputed at the description's
end because the question names the relation first? (CPU)

From a composition readout (nn_readout --items composition rows), among composition successes (RM_ok): per item, the
share of the band's read layers where the answer (or the bridge) is the lens's top candidate at the description's end;
relation-before items minus relation-after items, 95% bootstrap over bridges. Reading (a): "precomputed when the relation
comes first" if before - after >= 10 points for the answer (J++) with the interval above 0.
With --vs RUN2 (rendering A's readout, same ids): rendering 0 minus rendering A on the items rendering A re-rendered.

python scripts/nn_order_read.py NAME --band 12-16 --readout RUN [--vs RUN2] [--set jsuite_v3_test_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.nn_ans_read import order_ids  # noqa: E402


def item_scores(run: str, lo: int, hi: int) -> dict:
    """(lens, what) -> id -> (bridge key, band top-1 share), successes only."""
    acc = collections.defaultdict(list)
    key = {}
    for line in (ROOT / "results/nn_readout" / run / "rows.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["family"] == "RM_ok" and r["site"] == "desc_end" and lo <= r["layer"] <= hi:
            acc[(r["lens"], r["what"], r["id"])].append(100.0 * (r["rank"] == 1))
            key[r["id"]] = f"{r['rel']}:{r['bridge']}"
    out: dict = collections.defaultdict(dict)
    for (ln, what, i), v in acc.items():
        out[(ln, what)][i] = (key[i], sum(v) / len(v))
    return out


def contrast(a: dict, b: dict) -> tuple[float, list[float], int, int]:
    """mean(a) - mean(b), bootstrap over bridges (items of both groups resampled by bridge)."""
    by = collections.defaultdict(lambda: ([], []))
    for k, s in a.values():
        by[k][0].append(s)
    for k, s in b.values():
        by[k][1].append(s)
    m = lambda xs: sum(xs) / len(xs)  # noqa: E731
    diff = m([s for _, s in a.values()]) - m([s for _, s in b.values()])
    rng, keys, ds = random.Random(0), sorted(by), []
    for _ in range(1000):
        pick = [rng.choice(keys) for _ in keys]
        xa = [s for k in pick for s in by[k][0]]
        xb = [s for k in pick for s in by[k][1]]
        if xa and xb:
            ds.append(m(xa) - m(xb))
    ds.sort()
    return round(diff, 1), [round(ds[int(0.025 * len(ds))], 1), round(ds[int(0.975 * len(ds)) - 1], 1)], len(a), len(b)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--band", required=True)
    ap.add_argument("--readout", required=True)
    ap.add_argument("--vs", default=None)
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    a = ap.parse_args()
    lo, hi = (int(x) for x in a.band.split("-"))
    sc = item_scores(a.readout, lo, hi)
    after = order_ids(a.set, "after")
    out = {"readout": a.readout, "split": {}}
    for (ln, what), d in sorted(sc.items()):
        bef = {i: v for i, v in d.items() if i not in after}
        aft = {i: v for i, v in d.items() if i in after}
        diff, ci, nb, na = contrast(bef, aft)
        out["split"][f"{ln}/{what}"] = {"before": round(sum(s for _, s in bef.values()) / nb, 1), "after": round(sum(s for _, s in aft.values()) / na, 1),
                                        "n_before": nb, "n_after": na, "before_minus_after": diff, "ci": ci,
                                        "precomputed": what == "attr" and ln == "jlens" and diff >= 10 and ci[0] > 0}  # fmt: skip
        print(f"{ln:6s} {what:6s} before {out['split'][f'{ln}/{what}']['before']:5.1f} (n {nb})  after {out['split'][f'{ln}/{what}']['after']:5.1f} (n {na})  "
              f"before-after {diff:+5.1f} {ci}")  # fmt: skip
    if a.vs:
        sv = item_scores(a.vs, lo, hi)
        out["vs"] = {}
        for (ln, what), d in sorted(sc.items()):
            moved = {i: v for i, v in d.items() if i not in after and i in sv[(ln, what)]}  # re-rendered items, success in both
            other = {i: sv[(ln, what)][i] for i in moved}
            diff, ci, n0, _ = contrast(moved, other)
            out["vs"][f"{ln}/{what}"] = {"r0_minus_A": diff, "ci": ci, "n": n0}
            print(f"vs rendering A, re-rendered items: {ln:6s} {what:6s} r0 - A {diff:+5.1f} {ci} (n {n0})")
    d = ROOT / "results/nn_swap/nn_order_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{a.name}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
