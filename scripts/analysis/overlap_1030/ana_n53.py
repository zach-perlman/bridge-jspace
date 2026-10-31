"""overlap agent (post hoc, exploratory; CPU): note 53 (paper's 90 two-hop prompts, energy-matched controls) split by
skeptic 2's excess overlap (n39b_overlap/overlap.json: mean over main-band layers of A's share of the bridge atoms' energy
minus the mean share of 20 random same-size spans), median split over the run's primary items (ties to low), as s2_n39ov.py.
Per half: arm-1 flips, net1 = r1 - r0 (r0 = arm 1's matched-norm null), K = (r3 - r0) / net1, keep_7E = (r7E - r0) / net1,
keep_7 = (r7 - r0) / net1, suff = (r5 - r0) / net1, E2 = (r5 - r5R_k) / net1 with 5R_k the reader's matched arm.
Intervals: item bootstrap and answer-category cluster bootstrap, 2000 draws, random.Random(0).
"""

import json
import random
import statistics as st
from collections import defaultdict

R = "/workspace/bridge-jspace/results/paper_swap_decomp/"
out = {}


def boot(units, fn, n=2000):
    keys = sorted(units)
    rng, vals = random.Random(0), []
    for _ in range(n):
        v = fn([u for k in (rng.choice(keys) for _ in keys) for u in units[k]])
        if v == v:
            vals.append(v)
    vals.sort()
    return [round(vals[int(0.025 * len(vals))], 3), round(vals[int(0.975 * len(vals)) - 1], 3)] if vals else None


for pre in ["", "qwen35_9b_", "nem35l_", "muse30_"]:
    ov = json.load(open(R + pre + "n39b_overlap/overlap.json"))["items"]
    rd = json.load(open(R + pre + "n53_v1/reading53.json"))
    e2 = rd.get("E2", {})
    k5 = e2.get("arm") or e2.get("matched_arm") or e2.get("R_k")
    rows = [json.loads(x) for x in open(R + pre + "n53_v1/rows.jsonl")]
    win = rd["window"]
    m = {}
    for r in rows:
        if r["lens"] == "jpp" and r["window"] == win and r.get("set", "primary") == "primary":
            m[(r["name"], r["arm"], r["null"])] = r["flip"]
    names = sorted({k[0] for k in m if k[1] == "bridge" and not k[2]})
    ex = {n: ov[n]["mean"]["A"] - ov[n]["mean"]["rand_mean"] for n in names if n in ov and "mean" in ov[n]}
    cat = {n: ov[n].get("answer_type", "?") if n in ov else "?" for n in names}
    cut = st.median(ex.values())
    arms = ["bridge", "bridge_noA", "bridge_randE", "bridge_randA", "bridge_onlyA", "bridge_onlyR", "bridge_onlyR2", "bridge_onlyR4"]

    def stats(sel):
        def f(us, which):
            r = {a: sum(u[a] for u in us) / len(us) for a in arms + ["null"]}
            net = r["bridge"] - r["null"]
            if net <= 0:
                return float("nan")
            if which == "K":
                return (r["bridge_noA"] - r["null"]) / net
            if which == "keep7E":
                return (r["bridge_randE"] - r["null"]) / net
            if which == "keep7":
                return (r["bridge_randA"] - r["null"]) / net
            if which == "suff":
                return (r["bridge_onlyA"] - r["null"]) / net
            if which.startswith("E2:"):
                return (r["bridge_onlyA"] - r[which[3:]]) / net
            return net

        us_item, us_cat = defaultdict(list), defaultdict(list)
        for n in sel:
            u = {a: m.get((n, a, False), 0) for a in arms}
            u["null"] = m.get((n, "bridge", True), 0)
            us_item[n].append(u)
            us_cat[cat[n]].append(u)
        allu = [u for v in us_item.values() for u in v]
        res = {"n": len(sel), "arm1_flips": sum(u["bridge"] for u in allu), "null_flips": sum(u["null"] for u in allu),
               "categories": dict(sorted(((c, len(v)) for c, v in us_cat.items()), key=lambda x: -x[1]))}
        whichs = ["net1", "K", "keep7E", "keep7", "suff"] + [f"E2:{a}" for a in ("bridge_onlyR", "bridge_onlyR2", "bridge_onlyR4")]
        for w in whichs:
            v = f(allu, w) if allu else float("nan")
            res[w] = None if v != v else round(v, 3)
            res[w + "_ci_item"] = boot(us_item, lambda xs, w=w: f(xs, w)) if allu else None
            res[w + "_ci_cat"] = boot(us_cat, lambda xs, w=w: f(xs, w)) if allu else None
        return res

    low = [n for n in names if ex.get(n, 0) <= cut]
    high = [n for n in names if ex.get(n, 0) > cut]
    out[pre or "27b_"] = {"window": win, "n": len(names), "cut": round(cut, 4), "E2_reader": {k: v for k, v in e2.items() if not isinstance(v, (dict, list))},
                          "all": stats(names), "low": stats(low), "high": stats(high)}
    o = out[pre or "27b_"]
    print(pre or "27b_", win, "n", len(names), "cut", round(cut, 3), "E2 reader:", o["E2_reader"])
    for h in ("all", "low", "high"):
        s = o[h]
        print(f"  {h:4s} n {s['n']:2d} arm1 flips {s['arm1_flips']:2d} null {s['null_flips']} net1 {s['net1']} K {s['K']} {s['K_ci_item']} "
              f"keep7E {s['keep7E']} {s['keep7E_ci_item']} keep7 {s['keep7']} suff {s['suff']} E2(R/R2/R4) {s['E2:bridge_onlyR']}/{s['E2:bridge_onlyR2']}/{s['E2:bridge_onlyR4']}")
json.dump(out, open("/tmp/ana_n53.json", "w"), indent=1)
