"""cpuwins A3 (post hoc, exploratory): where do recalls lost under the knock-out go? MM items right clean, wrong under the
condition; paper10's output token (cand2 pick) categorised. Exclusive priority: X's own passage value > another entity's
passage value > clean top-10 rival > other relation answer > non-answer. Cluster bootstrap by bridge (2000)."""
import json, sys, collections
import numpy as np
rng = np.random.default_rng(1)
its = [json.loads(l) for l in open(sys.argv[1])]
CATS = ["x_pv", "other_pv", "rival", "answer", "non_answer"]
def cat(fl):
    if fl["gold"]: return "gold_tok"
    if fl["x_pv"]: return "x_pv"
    if fl["other_pv"]: return "other_pv"
    if fl["rival"] or fl["in_top10"]: return "rival"
    if fl["answer"]: return "answer"
    return "non_answer"
def boot_share(groups, c, B=2000):
    keys = list(groups)
    vals = []
    for _ in range(B):
        pick = rng.choice(len(keys), len(keys))
        xs = [x for j in pick for x in groups[keys[j]]]
        if xs: vals.append(100 * sum(x == c for x in xs) / len(xs))
    return [round(float(v), 1) for v in np.percentile(vals, [2.5, 97.5])]
res = {}
for m in ["9B", "27B", "Lightning"]:
    for word in ["MM", "MP"]:
        for cond in ["paper10", "paper10_onlyA", "top30", "top30_keepRE", "ansJ", "paper10_rot"]:
            g = collections.defaultdict(list); exm = collections.Counter()
            nclean = 0; ex_pv_in_top10 = 0; n_real = 0
            for it in its:
                if it["model"] != m or it["word"] != word: continue
                cs = it["conds"]
                if cond not in cs or not cs["none"]["correct"]: continue
                nclean += 1
                if cs[cond]["correct"]: continue
                c = cat(cs[cond]["flags"])
                g[it["bridge"]].append(c)
                if c == "x_pv" and cs[cond]["flags"]["in_top10"]: ex_pv_in_top10 += 1
                if cs[cond]["flags"]["real"]: n_real += 1
                if c == "non_answer": exm[cs[cond]["dec"]] += 1
            n = sum(len(v) for v in g.values())
            if n == 0: continue
            R = {"n_clean_right": nclean, "n_lost": n, "lost_pct": round(100 * n / nclean, 1)}
            for c in CATS + ["gold_tok"]:
                R[c] = round(100 * sum(x == c for v in g.values() for x in v) / n, 1)
                if c in CATS and cond in ("paper10", "top30_keepRE", "paper10_onlyA") : R[c + "_ci"] = boot_share(g, c)
            R["x_pv_and_in_clean_top10"] = ex_pv_in_top10
            if word == "MP": R["says_X_real_attr_pct_of_lost"] = round(100 * n_real / n, 1)
            R["non_answer_top"] = exm.most_common(6)
            res[f"{m}|{word}|{cond}"] = R
# chance: if a lost MM recall picked uniformly among the relation's non-gold answers
ch = {}
for m in ["9B", "27B", "Lightning"]:
    xs = [(1 / (it["n_vocab"] - 1), it["n_other_pv"] / (it["n_vocab"] - 1)) for it in its if it["model"] == m and it["word"] == "MM"]
    ch[m] = {"x_pv_chance_pct": round(100 * np.mean([a for a, _ in xs]), 1), "other_pv_chance_pct": round(100 * np.mean([b for _, b in xs]), 1)}
res["chance_uniform_over_answers"] = ch
json.dump(res, open(sys.argv[2], "w"), indent=1)
for k, v in res.items():
    print(k, json.dumps(v)[:700])
