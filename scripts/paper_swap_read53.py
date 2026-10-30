"""paper_swap_read53 (prereg amendment 72, note 53): note 39 with energy-matched controls, read.

From one paper_swap_n53 run (main band, J++; arms 1, 3, 5, 7 (3 seeds), 7E, 5R, 5R2, 5R4, 1nf, 3nf, 5nf and the nulls of
1, 5, 1nf and 5nf, in one job), on its primary items. r_X = arm X's first-token flip rate at the main band, r_0 = arm 1's
matched-norm null; net1 = r_1 - r_0. Pre-registered readings (note 53):
  E1  A1 re-read with arm 7E as the guard: K = (r_3 - r_0) / net1, keep_7E = (r_7E - r_0) / net1.
      "answer-carried survives energy matching" if keep_7E >= 2/3 and K <= 1/3; "scrub not specific at matched energy" if
      keep_7E < 2/3; if keep_7E >= 2/3 and K > 1/3, K's note 39 label ("partly" / "intermediate beyond the answer").
      Void if note 39's A0 (net1 >= 0.30) is not met in this run.
  E2  "sufficiency is answer-specific at matched energy" if (r_5 - r_5R_k) >= 1/3 of net1 with the interval of r_5 - r_5R_k
      above 0 (paper_swap_read5r's rule); otherwise "not answer-specific at matched energy". 5R_k = the smallest of the
      nested 5R, 5R2, 5R4 whose bridge-energy share is >= A's; "not matched" if none is.
  E3  (descriptive) r_1nf / r_1 and r_5nf / r_5: the swap's share that survives when the final position is not edited.
  The A1 guard spread over the three arm-7 seeds (keep_7 per seed, K's A1 label with each seed as the guard).
Implementation choices, fixed before any result:
  - Bridge-energy share of a span: per item and main-band layer, the mean over the two unit bridge atoms of the squared
    norm of their projection onto it (atoms.jsonl share_*); per item, the mean over the band's layers. For E2 the
    comparison is per model: the median over items of 5R_x's share against the median of A's (as the overlap summaries
    and the skeptic's energy figures). Beside it (descriptive): each item matched to its own smallest 5R_x (items no 5R_x
    reaches use 5R4, counted).
  - E1's guard is arm 7E alone, as written (arm 6b is not rerun). Arm 3 has no null of its own (note 39's: arm 1's).
  - E3: raw flip-rate ratios as written, with the null-netted ratios beside ((r_1nf - r_1nf,null) / net1 and
    (r_5nf - r_5nf,null) / (r_5 - r_5null)) and K at nf ((r_3nf - r_1nf,null) / (r_1nf - r_1nf,null)).
  - Intervals: note 39's cluster bootstrap over answer categories (paper_swap_read's), B = 2000, seed 0, percentile 95%.
    An item bootstrap (each item its own cluster, same B and seed) is printed beside, descriptive.
The run's check of the clean row and arms 1, 3, 5, 7 and the nulls against note 39's stored rows, and of 5R against the
5R run's, is printed first. Muse: descriptive only.

python scripts/paper_swap_read53.py results/paper_swap_decomp/<note39 run> results/paper_swap_decomp/<n53 run> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.paper_swap_read import Run, fmt, label_k  # noqa: E402

ARM7E = "bridge_randE"
SEEDS7 = {1: "bridge_randA", 2: "bridge_randA2", 3: "bridge_randA3"}
NESTED = ((1, "bridge_onlyR", "R"), (2, "bridge_onlyR2", "R2"), (4, "bridge_onlyR4", "R4"))


def view(prev: Run, rows: list[dict], per_item: bool = False) -> Run:
    """A Run over this job's rows: the stored run's answer types for the clusters (or one cluster per item)."""
    rr = Run.__new__(Run)
    rr.__dict__.update(prev.__dict__)
    rr.flip = {(o["lens"], o["window"], o["arm"], o["null"], o["name"]): bool(o["flip"]) for o in rows}
    if per_item:
        rr.atype = {o["name"]: o["name"] for o in rows}
    return rr


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prev_dir")
    ap.add_argument("run_dir")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    prev = Run(Path(a.prev_dir), a.boot)
    rd = Path(a.run_dir)
    man = json.loads((rd / "manifest.json").read_text())
    check = json.loads((rd / "check.json").read_text())
    rows = [json.loads(x) for x in (rd / "rows.jsonl").read_text().splitlines() if x.strip()]
    atoms = [json.loads(x) for x in (rd / "atoms.jsonl").read_text().splitlines() if x.strip()]
    e7 = {o["name"]: o for o in map(json.loads, (rd / "energy7e.jsonl").read_text().splitlines()) if o}
    rr, ri = view(prev, rows), view(prev, rows, per_item=True)
    names = sorted({o["name"] for o in rows})
    lens, w = "jpp", man["main_band"]
    descriptive = man["target"] == "muse-glimmer-30b"
    tag = ", DESCRIPTIVE ONLY" if descriptive else ""
    rate = lambda arm, null, ns: rr.rate(lens, w, arm, null, ns)  # noqa: E731
    out: dict = {"prev_run": str(prev.dir), "run": str(rd), "target": man["target"], "window": w, "n_items": len(names),
                 "n_categories": len({prev.atype[n] for n in names}), "stored_check": check}  # fmt: skip
    print(f"# note 53: {rd.name} ({man['target']}{tag}); main band {w}, J++; n {len(names)} primary items in {out['n_categories']} categories")
    for src, ch in (("note 39", check["note39"]), ("note 39 5R", check["note39_5r"])):
        print(f"stored check vs {src} rows: " + "; ".join(
            f"{k}: identical {v['identical_rows']}/{v['n']}, same flip {v['same_flip']}, rate {v['flip_rate_rerun']:.2f} vs "
            f"{v['flip_rate_stored']:.2f}, max |d dlogp| {v['max_abs_dlogp_diff']:.3g}" + (f", differing fields {v['differing_fields']}" if v["differing_fields"] else "")
            for k, v in ch.items()))  # fmt: skip

    def net1(ns):
        return rate("bridge", False, ns) - rate("bridge", True, ns)

    def over_net1(num):
        def f(ns):
            d = net1(ns)
            return num(ns) / d if d > 0 else math.nan

        return f

    def keep(arm):
        return over_net1(lambda ns: rate(arm, False, ns) - rate("bridge", True, ns))

    both = lambda stat: (rr.cluster_boot(names, stat), ri.cluster_boot(names, stat))  # noqa: E731
    a0 = rr.cluster_boot(names, net1)
    a0_met = a0[0] >= 0.30
    rates = {arm: rate(arm, False, names) for arm in sorted({o["arm"] for o in rows})}
    rates.update({f"null_{arm}": rate(arm, True, names) for arm in ("bridge", "bridge_onlyA", "bridge_nf", "bridge_onlyA_nf")})
    out["rates"], out["A0"] = rates, {"net1": a0, "met": a0_met}
    print("  rates " + ", ".join(f"{k} {v:.2f}" for k, v in rates.items()))
    print(f"  A0 (arm 1 net of its null >= 0.30): {fmt(a0)} -> {'met' if a0_met else 'NOT met: E1 void'}")

    # energy shares, per item = mean over the band's layers
    by_item: dict = {}
    for r in atoms:
        if r["lens"] == lens:
            by_item.setdefault(r["name"], []).append(r)
    sh = {n: {k[6:]: statistics.mean(r[k] for r in rs) for k in rs[0] if k.startswith("share_")} for n, rs in by_item.items() if n in names}
    med = {k: statistics.median(sh[n][k] for n in sh) for k in next(iter(sh.values()))}
    kq = sorted(e7[n]["k_E_over_n_A"] for n in names if n in e7)
    out["energy"] = {"median_share": med, "arm7E_k_over_nA": {"median": statistics.median(kq), "min": kq[0], "max": kq[-1]},
                     "arm7E_not_reached": sum(not e7[n]["reached"] for n in names if n in e7)}  # fmt: skip
    print("  bridge-energy share (median over items of the band mean): " + ", ".join(f"{k} {v:.3f}" for k, v in med.items())
          + f"; 7E size / |A| median {statistics.median(kq):.2f} [{kq[0]:.2f}, {kq[-1]:.2f}], not reached {out['energy']['arm7E_not_reached']}")

    # E1
    K, Ki = both(keep("bridge_noA"))
    k7e, k7ei = both(keep(ARM7E))
    if math.isnan(K[0]):
        e1 = "undefined (arm 1 not above its null)"
    elif not a0_met:
        e1 = f"void (A0 not met: arm 1 net {a0[0]:.2f} < 0.30)"
    elif k7e[0] < 2 / 3:
        e1 = "scrub not specific at matched energy"
    elif K[0] <= 1 / 3:
        e1 = "answer-carried survives energy matching"
    else:
        e1 = f"{label_k(K[0])} (arm 7E keeps >= 2/3, K > 1/3)"
    out["E1"] = {"K": K, "keep_7E": k7e, "K_item_boot": Ki, "keep_7E_item_boot": k7ei, "reading": e1}
    print(f"reading E1 [{lens} main {w} n {len(names)}{tag}]: {e1} (K {fmt(K)}; arm 7E keeps {fmt(k7e)}; arm 1 net {fmt(a0)}) | "
          f"item bootstrap: K {fmt(Ki)}, 7E keeps {fmt(k7ei)}")

    # guard spread over the three arm-7 seeds
    g: dict = {}
    for s, arm in SEEDS7.items():
        kk, kki = both(keep(arm))
        lab = (label_k(K[0]) if kk[0] >= 2 / 3 else "scrub not specific") if not math.isnan(K[0]) else "undefined"
        g[s] = {"arm": arm, "keep": kk, "keep_item_boot": kki, "A1_with_this_seed_as_guard": lab}
    pts = [g[s]["keep"][0] for s in g]
    out["guard_spread"] = {"seeds": g, "min": min(pts), "max": max(pts), "mean": statistics.mean(pts), "n_pass": sum(p >= 2 / 3 for p in pts)}
    print(f"reading E1-guard-spread [{lens} main {w} n {len(names)}{tag}]: arm 7 keeps over 3 seeds "
          + "; ".join(f"s{s} {fmt(g[s]['keep'])}" for s in g)
          + f"; range {min(pts):.2f}-{max(pts):.2f}, {out['guard_spread']['n_pass']}/3 seeds >= 2/3; A1 labels "
          + ", ".join(f"s{s} {g[s]['A1_with_this_seed_as_guard']!r}" for s in g))

    # E2
    def suff(arm_r, ns_rr=rr, names_=names):
        def diff(ns):
            return rate("bridge_onlyA", False, ns) - rate(arm_r, False, ns)

        d = ns_rr.cluster_boot(names_, diff)
        q = ns_rr.cluster_boot(names_, over_net1(diff))
        return d, q, (not math.isnan(q[0]) and q[0] >= 1 / 3 and d[1] > 0)

    e2: dict = {"nested": {}}
    for mult, arm, key in NESTED:
        d, q, ok = suff(arm)
        di, qi, _ = suff(arm, ri)
        e2["nested"][f"5R{'' if mult == 1 else mult}"] = {"arm": arm, "median_share": med[key], "matched": med[key] >= med["scrub"],
                                                          "r5_minus_r5R": d, "over_net1": q, "specific": ok,
                                                          "r5_minus_r5R_item_boot": di}  # fmt: skip
    pick = next(((m, arm, key) for m, arm, key in NESTED if med[key] >= med["scrub"]), None)
    if pick is None:
        e2["reading"], e2["k"] = "not matched", None
        b = e2["nested"]["5R4"]
        print(f"reading E2 [{lens} main {w} n {len(names)}{tag}]: not matched (median share: A {med['scrub']:.3f}, 5R {med['R']:.3f}, "
              f"5R2 {med['R2']:.3f}, 5R4 {med['R4']:.3f}); nearest 5R4: r5 - r5R4 {fmt(b['r5_minus_r5R'])}, over arm 1 net {fmt(b['over_net1'])}")
    else:
        m, arm, key = pick
        lab = f"5R{'' if m == 1 else m}"
        b = e2["nested"][lab]
        e2["k"] = lab
        e2["reading"] = "sufficiency is answer-specific at matched energy" if b["specific"] else "not answer-specific at matched energy"
        print(f"reading E2 [{lens} main {w} n {len(names)}{tag}]: {e2['reading']} (5R_k = {lab}: median share {med[key]:.3f} vs A "
              f"{med['scrub']:.3f}; r5 - r5R_k {fmt(b['r5_minus_r5R'])}; over arm 1 net {fmt(b['over_net1'])}; arm 1 net {fmt(a0)}) | "
              f"item bootstrap r5 - r5R_k {fmt(b['r5_minus_r5R_item_boot'])}")
    for lab, b in e2["nested"].items():
        print(f"  descriptive E2 {lab}: median share {b['median_share']:.3f} (A {med['scrub']:.3f}, matched {b['matched']}); r5 - r5R "
              f"{fmt(b['r5_minus_r5R'])}; over arm 1 net {fmt(b['over_net1'])}; would read "
              f"{'answer-specific' if b['specific'] else 'not answer-specific'}")
    # per-item matching (descriptive): each item's own smallest 5R_x reaching its A share (else 5R4)
    own = {n: next((arm for _, arm, key in NESTED if sh[n][key] >= sh[n]["scrub"]), "bridge_onlyR4") for n in names}
    unmatched = sum(sh[n]["R4"] < sh[n]["scrub"] for n in names)

    def diff_own(ns):
        v = [rr.flip[(lens, w, "bridge_onlyA", False, n)] - rr.flip[(lens, w, own[n], False, n)] for n in ns]
        return sum(v) / len(v) if v else math.nan

    dpo, qpo = rr.cluster_boot(names, diff_own), rr.cluster_boot(names, over_net1(diff_own))
    e2["per_item_matched"] = {"r5_minus_r5Rown": dpo, "over_net1": qpo, "unmatched_items_used_5R4": unmatched,
                              "counts": {arm: sum(v == arm for v in own.values()) for _, arm, _ in NESTED}}  # fmt: skip
    print(f"  descriptive E2 per-item matched: r5 - r5R_own {fmt(dpo)}; over arm 1 net {fmt(qpo)}; items by 5R_x "
          f"{e2['per_item_matched']['counts']}, {unmatched} not reached by 5R4")
    out["E2"] = e2

    # E3
    def ratio_raw(num, den):
        def f(ns):
            d = rate(den, False, ns)
            return rate(num, False, ns) / d if d > 0 else math.nan

        return f

    def net_nf(ns):
        return rate("bridge_nf", False, ns) - rate("bridge_nf", True, ns)

    def r5net_nf(ns):
        d = rate("bridge_onlyA", False, ns) - rate("bridge_onlyA", True, ns)
        return (rate("bridge_onlyA_nf", False, ns) - rate("bridge_onlyA_nf", True, ns)) / d if d > 0 else math.nan

    def k_nf(ns):
        d = net_nf(ns)
        return (rate("bridge_noA_nf", False, ns) - rate("bridge_nf", True, ns)) / d if d > 0 else math.nan

    e3 = {"arm1nf_over_arm1": rr.cluster_boot(names, ratio_raw("bridge_nf", "bridge")),
          "arm5nf_over_arm5": rr.cluster_boot(names, ratio_raw("bridge_onlyA_nf", "bridge_onlyA")),
          "arm1nf_net_over_arm1_net": rr.cluster_boot(names, over_net1(net_nf)),
          "arm5nf_net_over_arm5_net": rr.cluster_boot(names, r5net_nf), "K_nf": rr.cluster_boot(names, k_nf)}  # fmt: skip
    out["E3"] = e3
    print(f"reading E3 [{lens} main {w} n {len(names)}, descriptive]: arm 1nf / arm 1 {fmt(e3['arm1nf_over_arm1'])}; "
          f"arm 5nf / arm 5 {fmt(e3['arm5nf_over_arm5'])} | netted: 1nf {fmt(e3['arm1nf_net_over_arm1_net'])}, "
          f"5nf {fmt(e3['arm5nf_net_over_arm5_net'])}; K at nf {fmt(e3['K_nf'])} (rates 1nf {rates.get('bridge_nf', math.nan):.2f}, "
          f"3nf {rates.get('bridge_noA_nf', math.nan):.2f}, 5nf {rates.get('bridge_onlyA_nf', math.nan):.2f})")
    (rd / "reading53.json").write_text(json.dumps(out, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
