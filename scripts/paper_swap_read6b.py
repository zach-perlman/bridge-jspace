"""paper_swap_read6b (prereg amendment 65 second addendum, note 39): A1 re-read with arm 6b as the guard.

From the rerun (scripts/paper_swap_6b.py rerun; arms 1, 3, 6b, 7 and arm 1's null in one job), per lens, at the main band
and at arm 1's median-onset window, on the rerun's primary items:
  K = (r3 - r0) / (r1 - r0); keep_6b = (r6b - r0) / (r1 - r0); keep_7 = (r7 - r0) / (r1 - r0)
  A1 valid only if keep_6b >= 2/3 AND keep_7 >= 2/3 (arm 7 unchanged); then K <= 1/3 "answer-carried", K >= 2/3
  "intermediate beyond the answer", else "partly"; otherwise "scrub not specific".
Beside it: note 39's old arm 6 from the stored run on the same items, "same-domain control, invalid as a guard", and the
stored run's K. Intervals: cluster bootstrap over answer categories (paper_swap_read's), B = 2000, seed 0. The rerun's
check of arms 1, 3, 7 and the null against the stored rows is printed first. Muse: descriptive only.

python scripts/paper_swap_read6b.py results/paper_swap_decomp/<note39 run> results/paper_swap_decomp/<rerun> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.paper_swap_read import Run, fmt, label_k  # noqa: E402

ARM6B = "bridge_off6b"


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
    # a Run-like view of the rerun: same flip table keys, the stored run's answer types for the clusters
    rr = Run.__new__(Run)
    rr.__dict__.update(prev.__dict__)
    rr.flip = {(o["lens"], o["window"], o["arm"], o["null"], o["name"]): bool(o["flip"]) for o in rows}
    names = sorted({o["name"] for o in rows})
    descriptive = man["target"] == "muse-glimmer-30b"
    out: dict = {"prev_run": str(prev.dir), "rerun": str(rr_dir), "target": man["target"], "n_items": len(names),
                 "n_categories": len({prev.atype[n] for n in names}), "stored_check": check, "A1_6b": {}}  # fmt: skip
    print(f"# note 39 A1 re-read with arm 6b: {rr_dir.name} ({man['target']}{', DESCRIPTIVE ONLY' if descriptive else ''}); "
          f"n {len(names)} primary items in {out['n_categories']} categories")
    print("stored check (rerun vs note 39 rows): " + "; ".join(f"{k}: same flip {v['same_flip']}/{v['n']}, rate {v['flip_rate_rerun']:.2f} vs "
                                                              f"{v['flip_rate_stored']:.2f}, max |d dlogp| {v['max_abs_dlogp_diff']:.3f}" for k, v in check.items() if isinstance(v, dict))
          + f"; overlap geometry max |diff| {check.get('overlap_geometry_max_abs_diff')}")
    for lens in man["lenses"]:
        onset = man["median_onset_windows"].get(lens)
        for tag, w in (("main_band", man["main_band"]), ("median_onset", onset)):
            if w is None:
                print(f"reading A1-6b [{lens} {tag}]: no median-onset window")
                continue
            K = rr.cluster_boot(names, rr.ratio(lens, w, "bridge_noA"))
            k6b = rr.cluster_boot(names, rr.ratio(lens, w, ARM6B))
            k7 = rr.cluster_boot(names, rr.ratio(lens, w, "bridge_randA"))
            valid = not math.isnan(K[0]) and k6b[0] >= 2 / 3 and k7[0] >= 2 / 3
            reading = label_k(K[0]) if valid else (f"scrub not specific (arm 6b keeps {k6b[0]:.2f}, arm 7 keeps {k7[0]:.2f}; "
                                                    f"K = {K[0]:.2f} would read {label_k(K[0])!r})")  # fmt: skip
            old6 = prev.cluster_boot(names, prev.ratio(lens, w, "bridge_offA"))
            oldK = prev.cluster_boot(names, prev.ratio(lens, w, "bridge_noA"))
            rates = {arm: rr.rate(lens, w, arm, False, names) for arm in ("bridge", "bridge_noA", ARM6B, "bridge_randA")}
            rates["null_bridge"] = rr.rate(lens, w, "bridge", True, names)
            out["A1_6b"][f"{lens}/{tag}"] = {"window": w, "rates": rates, "K": K, "keep_arm6b": k6b, "keep_arm7": k7, "valid": valid,
                                             "reading": reading, "old_arm6_same_domain_invalid_as_guard": old6, "stored_K": oldK}  # fmt: skip
            print(f"reading A1-6b [{lens} {tag} {w}]: {reading} (K {fmt(K)}; arm 6b keeps {fmt(k6b)}; arm 7 keeps {fmt(k7)}) | "
                  f"old arm 6 (same-domain control, invalid as a guard) keeps {fmt(old6)}; stored K {fmt(oldK)}")
            print("  rates " + ", ".join(f"{k} {v:.2f}" for k, v in rates.items()))
    (rr_dir / "reading6b.json").write_text(json.dumps(out, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
