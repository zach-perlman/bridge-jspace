"""paper_ko_read (prereg amendment 68 note 45): the readings of one paper_ko_decomp run, per set.

Analysis set: gated items whose unedited strict first-token read is right. loss(c) = share of them whose read is wrong
under condition c, in points; K(X) = (loss(keep_X) - loss(paper10_rot)) / (loss(paper10) - loss(paper10_rot)), keepR's
loss the mean over its 3 draws. Each K reading uses the items where every non-target word it involves is unprotected
(none of its dictionary rows in paper10's protected set, the clean top-10 tokens' rows; the target is protected by
construction and is never a filter; digit words have no dictionary rows, so they are never protected); the same on all
items is printed beside. ML pivot readings also leave out the cognates (E and T share a first-token form, per
tokenizer).
  A0: loss(paper10) - max(loss(rot), loss(pcasize)) >= 20 points, interval above 0; otherwise "the knock-out does not
      bite on this set" (the readings below are then printed but void)
  Validity: K(keepR) >= 2/3 and K(keep_ctl) >= 2/3, else "spans not specific"
  ML: "English pivot carries it" K(E) <= 1/3 and K(T) >= 2/3; "target word carries it" the reverse; "shared concept"
      both <= 1/3; "neither" both >= 2/3; else "mixed". R and L the same way ("the relation / language carries it"
      K <= 1/3, "not the relation / language" K >= 2/3, else "partly"). Necessity: loss(rm_X) - loss(rm_ctl) >= 15 points
      with its interval above 0 = "the English pivot (relation, language) is necessary", for X = E, R, L.
  MH: "answer" K(T) <= 1/3 and K(B) >= 2/3; "bridge" the reverse; else "mixed". Early window: "the intermediate is
      needed early" if K_early(B) <= 1/3 and K_early(T) >= 2/3.
  OO: descriptive (K of T, P, O).
  Splits: single- vs multi-token targets.
Intervals: cluster bootstrap (relation for ML, answer type for MH, operation for OO), B = 2000, seed 0, percentile 95%.

python scripts/paper_ko_read.py results/paper_ko_decomp/<run> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

import numpy as np


class Read:
    def __init__(self, run_dir: Path, n_boot: int):
        self.dir = run_dir
        self.items = [json.loads(x) for x in (run_dir / "items.jsonl").read_text().splitlines() if x.strip()]
        rows = [json.loads(x) for x in (run_dir / "rows.jsonl").read_text().splitlines() if x.strip()]
        self.ok = {(r["set"], r["name"], r["window"], r["cond"]): bool(r["correct"]) for r in rows}
        self.dlogp = {(r["set"], r["name"], r["window"], r["cond"]): r["dlogp"] for r in rows}
        self.by = {(r["set"], r["name"]): r for r in self.items}
        self.n_boot = n_boot

    def analysis(self, s: str) -> list[str]:
        return sorted(r["name"] for r in self.items if r["set"] == s and r["eligible"] and r.get("clean_correct"))

    def loss(self, s, names, cond, window="main") -> float:
        if cond == "keepR":
            return statistics.mean(self.loss(s, names, f"keepR{k}", window) for k in (1, 2, 3))
        v = [not self.ok[(s, n, window, cond)] for n in names if (s, n, window, cond) in self.ok]
        return 100 * sum(v) / len(v) if v else math.nan

    def K(self, s, word, window="main"):
        def f(ns):
            den = self.loss(s, ns, "paper10", window) - self.loss(s, ns, "paper10_rot", window)
            num = self.loss(s, ns, word if word.startswith("keepR") else f"keep_{word}", window) - self.loss(s, ns, "paper10_rot", window)
            return num / den if den > 0 else math.nan

        return f

    def boot(self, s, names, stat):
        clusters: dict = {}
        for n in names:
            clusters.setdefault(self.by[(s, n)]["cluster"], []).append(n)
        keys = sorted(clusters)
        point = stat(names) if names else math.nan
        if not names:
            return (math.nan, math.nan, math.nan)
        rng = np.random.default_rng(0)
        vals = []
        for _ in range(self.n_boot):
            v = stat([n for k in rng.integers(0, len(keys), len(keys)) for n in clusters[keys[k]]])
            if not (isinstance(v, float) and math.isnan(v)):
                vals.append(v)
        if not vals:
            return (point, math.nan, math.nan)
        lo, hi = np.percentile(vals, [2.5, 97.5])
        return (point, float(lo), float(hi))

    def unprotected(self, s, names, words) -> list[str]:
        return [n for n in names if not any(self.by[(s, n)]["protected_rows"].get(w) for w in words)]


def f(x) -> str:
    if isinstance(x, tuple):
        return f"{x[0]:.2f} [{x[1]:.2f}, {x[2]:.2f}]"
    return f"{x:.2f}" if isinstance(x, float) else str(x)


def label_pair(k_a: float, k_b: float, a_carries: str, b_carries: str, both_low: str, both_high: str) -> str:
    if math.isnan(k_a) or math.isnan(k_b):
        return "undefined (paper10 not above its rotation)"
    if k_a <= 1 / 3 and k_b >= 2 / 3:
        return a_carries
    if k_b <= 1 / 3 and k_a >= 2 / 3:
        return b_carries
    if k_a <= 1 / 3 and k_b <= 1 / 3:
        return both_low
    if k_a >= 2 / 3 and k_b >= 2 / 3:
        return both_high
    return "mixed"


def read_set(R: Read, s: str) -> dict:
    names = R.analysis(s)
    out: dict = {"n_analysis": len(names), "n_eligible": sum(r["eligible"] for r in R.items if r["set"] == s)}
    a0 = R.boot(s, names, lambda ns: R.loss(s, ns, "paper10") - max(R.loss(s, ns, "paper10_rot"), R.loss(s, ns, "paper10_pcasize")))
    out["losses_main"] = {c: R.loss(s, names, c) for c in ("paper10", "paper10_rot", "paper10_pcasize", "unembed10")}
    out["A0"] = {"paper10_minus_max_controls": a0, "met": a0[0] >= 20 and a0[1] > 0}
    out["A0"]["reading"] = "the knock-out bites" if out["A0"]["met"] else "the knock-out does not bite on this set"
    ctlw = {"ML": "E", "MH": "B", "OO": "P"}[s]
    vn = R.unprotected(s, names, [ctlw, "ctl"])
    kR, kc = R.boot(s, vn, R.K(s, "keepR")), R.boot(s, vn, R.K(s, "ctl"))
    valid = kR[0] >= 2 / 3 and kc[0] >= 2 / 3
    out["validity"] = {"n": len(vn), "K_keepR": kR, "K_keep_ctl": kc, "valid": valid,
                       "reading": "spans specific" if valid else "spans not specific"}  # fmt: skip
    void = "" if out["A0"]["met"] else " [void: A0 not met]"
    inval = "" if valid else " [spans not specific]"
    if s == "ML":
        pn = [n for n in R.unprotected(s, names, ["E"]) if not R.by[(s, n)].get("cognate")]
        kE, kT = R.boot(s, pn, R.K(s, "E")), R.boot(s, pn, R.K(s, "T"))
        out["pivot"] = {"n": len(pn), "K_E": kE, "K_T": kT, "reading": label_pair(kE[0], kT[0], "English pivot carries it",
                        "target word carries it", "shared concept", "neither") + void + inval}  # fmt: skip
        for w, nm in (("R", "relation"), ("L", "language")):
            wn = R.unprotected(s, names, [w])
            k = R.boot(s, wn, R.K(s, w))
            lab = "undefined" if math.isnan(k[0]) else f"the {nm} carries it" if k[0] <= 1 / 3 else f"not the {nm}" if k[0] >= 2 / 3 else "partly"
            out[f"K_{w}"] = {"n": len(wn), "K": k, "reading": lab + void + inval}
        out["K_I"] = {"n": len(R.unprotected(s, names, ["I"])), "K": R.boot(s, R.unprotected(s, names, ["I"]), R.K(s, "I"))}
        for w, nm in (("E", "the English pivot"), ("R", "the relation"), ("L", "the language")):
            wn = [n for n in names if not (w == "E" and R.by[(s, n)].get("cognate"))]
            d = R.boot(s, wn, lambda ns, w=w: R.loss(s, ns, f"rm_{w}") - R.loss(s, ns, "rm_ctl"))
            out[f"necessity_{w}"] = {"n": len(wn), "rm_minus_rm_ctl": d, "rm_rot": R.loss(s, wn, f"rm_{w}_rot"),
                                     "reading": (f"{nm} is necessary" if d[0] >= 15 and d[1] > 0 else f"{nm} not shown necessary") + void}  # fmt: skip
        out["all_items_beside"] = {"K_E": R.boot(s, names, R.K(s, "E")), "K_T": R.boot(s, names, R.K(s, "T"))}
    elif s == "MH":
        bn = R.unprotected(s, names, ["B"])
        kT, kB = R.boot(s, bn, R.K(s, "T")), R.boot(s, bn, R.K(s, "B"))
        out["main"] = {"n": len(bn), "K_T": kT, "K_B": kB,
                       "reading": label_pair(kT[0], kB[0], "answer", "bridge", "both carry it", "neither") + void + inval}  # fmt: skip
        kTe, kBe = R.boot(s, bn, R.K(s, "T", "early")), R.boot(s, bn, R.K(s, "B", "early"))
        early_net = R.boot(s, bn, lambda ns: R.loss(s, ns, "paper10", "early") - R.loss(s, ns, "paper10_rot", "early"))
        needed = not math.isnan(kBe[0]) and kBe[0] <= 1 / 3 and kTe[0] >= 2 / 3
        out["early"] = {"K_T": kTe, "K_B": kBe, "paper10_net_loss": early_net,
                        "reading": ("the intermediate is needed early" if needed else "the intermediate is not shown needed early") + void}  # fmt: skip
        d = R.boot(s, names, lambda ns: R.loss(s, ns, "rm_B") - R.loss(s, ns, "rm_ctl"))
        out["rm_B_minus_rm_ctl"] = d
        out["all_items_beside"] = {"K_T": R.boot(s, names, R.K(s, "T")), "K_B": R.boot(s, names, R.K(s, "B"))}
    else:
        out["descriptive"] = {w: R.boot(s, R.unprotected(s, names, [w] if w != "T" else []), R.K(s, w)) for w in ("T", "P", "O")}
    for split, keep in (("single_token_target", True), ("multi_token_target", False)):
        sn = [n for n in names if R.by[(s, n)]["single_token_target"] == keep]
        out[split] = {"n": len(sn), **{f"K_{w}": R.K(s, w)(sn) if sn else math.nan for w in {"ML": ("T", "E"), "MH": ("T", "B"), "OO": ("T", "P")}[s]}}
    out["protected_counts"] = {w: sum(bool(R.by[(s, n)]["protected_rows"].get(w)) for n in names) for w in R.by[(s, names[0])]["protected_rows"]} if names else {}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    R = Read(Path(a.run_dir), a.boot)
    man = json.loads((R.dir / "manifest.json").read_text())
    check = json.loads((R.dir / "check.json").read_text())
    res = {"run": str(R.dir), "target": man["target"], "byte_check_all_equal": check["all_equal"], "sets": {}}
    print(f"# note 45 reading: {R.dir.name} ({man['target']}); main band {man['main_band']}, early {man['early_window']}; "
          f"byte-identity check on MH: all equal {check['all_equal']}")
    for s in sorted({r["set"] for r in R.items}):
        o = read_set(R, s)
        res["sets"][s] = o
        print(f"\n## {s}: analysis n {o['n_analysis']} (gated {o['n_eligible']}); losses {json.dumps({k: round(v, 1) for k, v in o['losses_main'].items()})}")
        print(f"reading {s} A0: {o['A0']['reading']} (paper10 - max(rot, pcasize) {f(o['A0']['paper10_minus_max_controls'])} pts)")
        print(f"reading {s} validity: {o['validity']['reading']} (n {o['validity']['n']}; K keepR {f(o['validity']['K_keepR'])}; K ctl {f(o['validity']['K_keep_ctl'])})")
        if s == "ML":
            p = o["pivot"]
            print(f"reading ML pivot: {p['reading']} (n {p['n']}; K(E) {f(p['K_E'])}; K(T) {f(p['K_T'])})")
            for w in ("R", "L"):
                print(f"reading ML {w}: {o['K_' + w]['reading']} (n {o['K_' + w]['n']}; K {f(o['K_' + w]['K'])})")
            for w in ("E", "R", "L"):
                nec = o["necessity_" + w]
                print(f"reading ML necessity {w}: {nec['reading']} (rm_{w} - rm_ctl {f(nec['rm_minus_rm_ctl'])} pts; n {nec['n']})")
        elif s == "MH":
            print(f"reading MH: {o['main']['reading']} (n {o['main']['n']}; K(T) {f(o['main']['K_T'])}; K(B) {f(o['main']['K_B'])})")
            e = o["early"]
            print(f"reading MH early: {e['reading']} (K_early(T) {f(e['K_T'])}; K_early(B) {f(e['K_B'])}; early paper10 net {f(e['paper10_net_loss'])})")
        else:
            print("descriptive OO: " + ", ".join(f"K({w}) {f(v)}" for w, v in o["descriptive"].items()))
        print(f"  splits: single {json.dumps(o['single_token_target'], default=str)}; multi {json.dumps(o['multi_token_target'], default=str)}")
        print(f"  protected (analysis items): {o['protected_counts']}")
    (R.dir / "reading.json").write_text(json.dumps(res, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
