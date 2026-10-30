"""paper_swap_read5r (prereg amendment 67, note 39 arm 5R): is note 39's sufficiency (arm 5) answer-specific?

From the 5R rerun (scripts/paper_swap_5r.py: arms 1, 5, 5R and the nulls of 1 and 5 in one job), on its primary items,
per lens; r_X = arm X's first-token flip rate, r_0 = arm 1's matched-norm null:
  reading (pre-registered): "sufficiency is answer-specific" if (r5 - r5R) >= 1/3 of arm 1's net (r1 - r0), with the
  cluster-bootstrap interval of r5 - r5R above 0; otherwise "not answer-specific". Read at the main band (note 39's A3
  window); arm 1's median-onset window beside.
  descriptive: the same, and note 39's A3 ratio ((r5 - r5null) / (r1 - r0)) and 5R's ((r5R - r0) / (r1 - r0)), without
  the capital, language and country items.
Intervals: cluster bootstrap over answer categories (paper_swap_read's), B = 2000, seed 0. The rerun's check of arms 1
and 5 and the nulls against the stored note 39 rows is printed first. Muse: descriptive only.

python scripts/paper_swap_read5r.py results/paper_swap_decomp/<note39 run> results/paper_swap_decomp/<5R rerun> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.paper_swap_read import Run, fmt  # noqa: E402

ARM5R = "bridge_onlyR"
NATION = ("capital", "language", "country")


def block(rr: Run, lens: str, w: str, names: list[str]) -> dict:
    rate = lambda arm, null, ns: rr.rate(lens, w, arm, null, ns)  # noqa: E731

    def net1(ns):
        return rate("bridge", False, ns) - rate("bridge", True, ns)

    def diff(ns):
        return rate("bridge_onlyA", False, ns) - rate(ARM5R, False, ns)

    def ratio(ns):
        n1 = net1(ns)
        return diff(ns) / n1 if n1 > 0 else math.nan

    def a3(ns):
        n1 = net1(ns)
        return (rate("bridge_onlyA", False, ns) - rate("bridge_onlyA", True, ns)) / n1 if n1 > 0 else math.nan

    def r5r(ns):
        n1 = net1(ns)
        return (rate(ARM5R, False, ns) - rate("bridge", True, ns)) / n1 if n1 > 0 else math.nan

    d, q = rr.cluster_boot(names, diff), rr.cluster_boot(names, ratio)
    specific = not math.isnan(q[0]) and q[0] >= 1 / 3 and d[1] > 0
    return {
        "window": w, "n": len(names), "rates": {k: rate(a_, nl, names) for k, (a_, nl) in
                                               {"r1": ("bridge", False), "r0": ("bridge", True), "r5": ("bridge_onlyA", False),
                                                "r5null": ("bridge_onlyA", True), "r5R": (ARM5R, False)}.items()},
        "arm1_net": rr.cluster_boot(names, net1), "r5_minus_r5R": d, "r5_minus_r5R_over_arm1_net": q,
        "A3_ratio": rr.cluster_boot(names, a3), "arm5R_net_over_arm1_net": rr.cluster_boot(names, r5r),
        "reading": "sufficiency is answer-specific" if specific else "not answer-specific",
    }  # fmt: skip


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prev_dir")
    ap.add_argument("rerun_dir")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    prev = Run(Path(a.prev_dir), a.boot)
    rr_dir = Path(a.rerun_dir)
    man = json.loads((rr_dir / "manifest.json").read_text())
    check = json.loads((rr_dir / "check.json").read_text())
    rows = [json.loads(x) for x in (rr_dir / "rows.jsonl").read_text().splitlines() if x.strip()]
    rr = Run.__new__(Run)
    rr.__dict__.update(prev.__dict__)
    rr.flip = {(o["lens"], o["window"], o["arm"], o["null"], o["name"]): bool(o["flip"]) for o in rows}
    names = sorted({o["name"] for o in rows})
    rest = [n for n in names if prev.atype[n] not in NATION]
    descriptive = man["target"] == "muse-glimmer-30b"
    out: dict = {"prev_run": str(prev.dir), "rerun": str(rr_dir), "target": man["target"], "n_items": len(names),
                 "n_without_nation": len(rest), "stored_check": check, "blocks": {}}  # fmt: skip
    print(f"# note 39 arm 5R: {rr_dir.name} ({man['target']}{', DESCRIPTIVE ONLY' if descriptive else ''}); n {len(names)} primary items "
          f"in {len({prev.atype[n] for n in names})} categories; without capital/language/country: {len(rest)}")
    print("stored check (rerun vs note 39 rows): " + "; ".join(f"{k}: same flip {v['same_flip']}/{v['n']}, same rank {v['same_swap_rank']}, "
                                                              f"max |d dlogp| {v['max_abs_dlogp_diff']:.3f}" for k, v in check.items()))
    for lens in man["lenses"]:
        for tag, w in (("main_band", man["main_band"]), ("median_onset", man["median_onset_windows"].get(lens))):
            if w is None:
                continue
            for subset, ns in (("primary", names), ("without_capital_language_country", rest)):
                if not ns:
                    continue
                b = block(rr, lens, w, ns)
                out["blocks"][f"{lens}/{tag}/{subset}"] = b
                head = "reading 5R" if subset == "primary" and tag == "main_band" else "descriptive 5R"
                print(f"{head} [{lens} {tag} {w} {subset} n {b['n']}]: {b['reading']} (r5 - r5R {fmt(b['r5_minus_r5R'])}; over arm 1 net "
                      f"{fmt(b['r5_minus_r5R_over_arm1_net'])}; arm 1 net {fmt(b['arm1_net'])}; A3 ratio {fmt(b['A3_ratio'])}; "
                      f"5R net / arm 1 net {fmt(b['arm5R_net_over_arm1_net'])})")
    (rr_dir / "reading5r.json").write_text(json.dumps(out, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
