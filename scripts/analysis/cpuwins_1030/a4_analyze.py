"""cpuwins A4 (post hoc, exploratory): per-item dose-response. MM items right clean. x = E_A = paper10 row's retained.A
(share of the removal's energy, summed over band layers and positions, lying in the answer words' J++ span); controls:
retained.R (a rank-matched random span's share) and edit_rel (removal size). y = lost under paper10 (cand2), and
d_logp = clean - paper10 log p(gold first token). Spearman, AUROC, partial (clean logp, relation); bridge bootstrap."""
import json, sys, collections
import numpy as np
rng = np.random.default_rng(2)
its = [json.loads(l) for l in open(sys.argv[1])]
def rankdata(a):
    a = np.asarray(a, float); o = a.argsort(); r = np.empty(len(a)); r[o] = np.arange(len(a))
    # average ties
    s = a[o]; i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]: j += 1
        r[o[i:j + 1]] = (i + j) / 2; i = j + 1
    return r
def spear(x, y): return float(np.corrcoef(rankdata(x), rankdata(y))[0, 1])
def auroc(s, y):
    s = np.asarray(s, float); y = np.asarray(y, int); r = rankdata(s) + 1
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)) if n1 and n0 else np.nan
def resid(v, Z):
    Z = np.hstack([Z, np.ones((len(v), 1))]); b, *_ = np.linalg.lstsq(Z, v, rcond=None); return v - Z @ b
def boot(fn, g, B=2000):
    ug = np.unique(g); idx = {u: np.where(g == u)[0] for u in ug}; out = []
    for _ in range(B):
        ii = np.concatenate([idx[u] for u in rng.choice(ug, len(ug))]); v = fn(ii)
        if v == v: out.append(v)
    return [round(float(x), 3) for x in np.percentile(out, [2.5, 97.5])]
res = {}
for m in ["9B", "27B", "Lightning"]:
    for word in ["MM", "MP"]:
        S = [it for it in its if it["model"] == m and it["word"] == word and it["conds"]["none"]["correct"] and it["conds"]["paper10"].get("retained")]
        EA = np.array([it["conds"]["paper10"]["retained"]["A"] for it in S]); ER = np.array([it["conds"]["paper10"]["retained"].get("R", np.nan) or np.nan for it in S])
        ED = np.array([it["conds"]["paper10"]["edit_rel"] for it in S])
        lost = np.array([not it["conds"]["paper10"]["correct"] for it in S], int)
        dl = np.array([it["conds"]["none"]["logp"] - it["conds"]["paper10"]["logp"] for it in S])
        lp0 = np.array([it["conds"]["none"]["logp"] for it in S])
        rels = sorted({it["rel"] for it in S}); Zrel = np.array([[it["rel"] == r for r in rels[1:]] for it in S], float)
        g = np.array([it["bridge"] for it in S])
        R = {"n": len(S), "n_bridges": len(set(g)), "lost_pct": round(100 * lost.mean(), 1), "E_A_mean": round(float(EA.mean()), 3),
             "E_A_sd": round(float(EA.std()), 3), "E_A_p10_p90": [round(float(x), 3) for x in np.percentile(EA, [10, 90])],
             "E_R_mean": round(float(np.nanmean(ER)), 3)}
        R["spear_EA_dlogp"] = round(spear(EA, dl), 3); R["spear_EA_dlogp_ci"] = boot(lambda ii: spear(EA[ii], dl[ii]), g)
        R["auc_EA_lost"] = round(auroc(EA, lost), 3); R["auc_EA_lost_ci"] = boot(lambda ii: auroc(EA[ii], lost[ii]), g)
        if not np.isnan(ER).any():
            R["spear_ER_dlogp"] = round(spear(ER, dl), 3); R["spear_ER_dlogp_ci"] = boot(lambda ii: spear(ER[ii], dl[ii]), g)
            R["auc_ER_lost"] = round(auroc(ER, lost), 3)
            R["spear_EA_minus_ER_dlogp"] = round(spear(EA - ER, dl), 3); R["spear_EA_minus_ER_dlogp_ci"] = boot(lambda ii: spear((EA - ER)[ii], dl[ii]), g)
        R["spear_editrel_dlogp"] = round(spear(ED, dl), 3)
        R["spear_EA_cleanlogp"] = round(spear(EA, lp0), 3)
        R["spear_cleanlogp_dlogp"] = round(spear(lp0, dl), 3)
        # partial Spearman: residualise ranks on clean logp rank, edit_rel rank, relation dummies
        Z = np.column_stack([rankdata(lp0), rankdata(ED), Zrel])
        def pspear(ii):
            Zi = Z[ii]; a = resid(rankdata(EA[ii]), Zi); b = resid(rankdata(dl[ii]), Zi); return float(np.corrcoef(a, b)[0, 1])
        R["partial_spear_EA_dlogp"] = round(pspear(np.arange(len(S))), 3); R["partial_spear_EA_dlogp_ci"] = boot(pspear, g)
        # within-relation Spearman
        R["within_rel"] = {r: (lambda ii: [round(spear(EA[ii], dl[ii]), 3), int(len(ii))])(np.array([j for j, it in enumerate(S) if it["rel"] == r])) for r in rels}
        # quintile dose-response
        q = np.quantile(EA, [0, .2, .4, .6, .8, 1.0]); b = np.clip(np.searchsorted(q, EA, side="right") - 1, 0, 4)
        R["quintiles"] = [{"EA_mid": round(float(EA[b == k].mean()), 3), "lost_pct": round(100 * float(lost[b == k].mean()), 1),
                           "dlogp_median": round(float(np.median(dl[b == k])), 2), "n": int((b == k).sum())} for k in range(5)]
        res[f"{m}|{word}"] = R
        print(m, word, json.dumps(R)[:900], flush=True)
json.dump(res, open(sys.argv[2], "w"), indent=1)
