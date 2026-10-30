"""cpuwins A3b analysis (post hoc, exploratory)."""
import json, sys, collections
import numpy as np
rng = np.random.default_rng(3)
rows = [json.loads(l) for l in open(sys.argv[1])]
def boot_ratio(groups, fn, B=2000):
    keys = list(groups); out = []
    for _ in range(B):
        xs = [x for j in rng.choice(len(keys), len(keys)) for x in groups[keys[j]]]
        v = fn(xs)
        if v == v and np.isfinite(v): out.append(v)
    return [round(float(x), 2) for x in np.percentile(out, [2.5, 97.5])]
res = {}
for m in ["9B", "27B", "Lightning"]:
    ko = [r for r in rows if r["model"] == m and r["src"] == "ko57"]
    for c in ["paper10", "paper10_onlyA", "top30_keepRE", "ansJ", "paper10_rot"]:
        lost = [r for r in ko if r["conds"]["none"]["correct"] and c in r["conds"] and not r["conds"][c]["correct"]]
        g = collections.defaultdict(list)
        for r in lost:
            cc = r["conds"][c]
            # per lost item: picked X's value?, picked some other entity's value (count of other entities), n other entities
            g[r["bridge"]].append((cc["x_hit"], len([j for j in cc["pv_pos"] if j != r["bpos"]]) > 0, r["n_ent"] - 1, cc["rank_in_clean_top10"], r["bpos"]))
        xs = [x for v in g.values() for x in v]
        if not xs: continue
        def ratio(xs):  # P(X's value) / mean P(one given other entity's value)
            px = np.mean([x[0] for x in xs]); po = np.mean([x[1] for x in xs]) / np.mean([x[2] for x in xs])
            return px / po if po > 0 else np.nan
        R = {"n_lost": len(xs), "x_share": round(100 * np.mean([x[0] for x in xs]), 1), "any_other_entity_share": round(100 * np.mean([x[1] for x in xs]), 1),
             "per_entity_ratio_X_vs_other": round(float(ratio(xs)), 2), "ratio_ci": boot_ratio(g, ratio),
             "in_clean_top10": round(100 * np.mean([x[3] is not None for x in xs]), 1),
             "clean_runner_up": round(100 * np.mean([x[3] == 2 for x in xs]), 1),
             "clean_rank_hist": dict(collections.Counter(str(x[3]) for x in xs).most_common(6))}
        # position control: X share by bridge position
        bp = collections.defaultdict(list)
        for x in xs: bp[x[4]].append(x[0])
        R["x_share_by_bridge_pos"] = {k: [round(100 * np.mean(v), 1), len(v)] for k, v in sorted(bp.items())}
        res[f"{m}|{c}"] = R
    nat = [r for r in rows if r["model"] == m and r["src"] == "natural"]
    for fam in ["MM_fail", "MM_ok"]:
        xs = [r for r in nat if r["family"] == fam]
        cnt = collections.Counter(r["cat"] for r in xs)
        res[f"{m}|natural|{fam}"] = {"n": len(xs), **{k: round(100 * v / len(xs), 1) for k, v in cnt.items()},
                                      "ambiguous": sum(r["ambiguous"] for r in xs),
                                      "non_answer_examples": collections.Counter(r["read_top"] for r in xs if r["cat"] == "non_answer").most_common(5)}
json.dump(res, open(sys.argv[2], "w"), indent=1)
for k, v in res.items(): print(k, json.dumps(v))
