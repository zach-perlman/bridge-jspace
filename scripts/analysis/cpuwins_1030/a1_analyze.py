"""cpuwins A1 analysis (post hoc, exploratory). Input: cpuwins_a1_items.jsonl from a1_extract.py.
Question: on v4 recall (MM) items that pass the v4 gate (closed-book hop 1 right, hop 2 alone right, no-description
guess wrong), does the gold answer's readout at the DESCRIPTION'S LAST TOKEN (before the question ends) predict whether
the composed answer is right (MM_ok) or wrong (MM_fail)? AUROC, cluster bootstrap over bridges (2000), label-permutation
null, grouped-by-bridge CV logistic regressions vs single-hop-confidence baselines."""
import json, sys, collections
import numpy as np

rng = np.random.default_rng(0)
items = [json.loads(l) for l in open(sys.argv[1])]

def auroc(s, y):
    s, y = np.asarray(s, float), np.asarray(y, int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    # Mann-Whitney with ties
    allv = np.concatenate([pos, neg])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    rp = ranks[: len(pos)].sum()
    return (rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

def boot(s, y, g, B=2000):
    s, y, g = np.asarray(s, float), np.asarray(y, int), np.asarray(g)
    ug = np.unique(g)
    idx = {u: np.where(g == u)[0] for u in ug}
    out = []
    for _ in range(B):
        pick = rng.choice(ug, len(ug), replace=True)
        ii = np.concatenate([idx[u] for u in pick])
        out.append(auroc(s[ii], y[ii]))
    out = np.array(out)
    out = out[~np.isnan(out)]
    return np.percentile(out, [2.5, 97.5])

def perm_p(s, y, B=2000):
    a0 = auroc(s, y)
    y = np.asarray(y)
    c = 0
    for _ in range(B):
        c += auroc(s, rng.permutation(y)) >= a0
    return (c + 1) / (B + 1)

def logreg_fit(X, y, lam=1.0, it=200):
    n, d = X.shape
    w = np.zeros(d + 1)
    Xb = np.hstack([X, np.ones((n, 1))])
    for _ in range(it):  # Newton
        p = 1 / (1 + np.exp(-Xb @ w))
        gr = Xb.T @ (p - y) + lam * np.r_[w[:-1], 0]
        H = Xb.T @ (Xb * (p * (1 - p))[:, None]) + lam * np.diag(np.r_[np.ones(d), 0]) + 1e-9 * np.eye(d + 1)
        step = np.linalg.solve(H, gr)
        w -= step
        if np.abs(step).max() < 1e-8:
            break
    return w

def cv_auc(X, y, g, seeds=5, k=5, lam=1.0):
    X, y, g = np.asarray(X, float), np.asarray(y, int), np.asarray(g)
    ug = np.unique(g)
    aucs, oof_all = [], []
    for sd in range(seeds):
        r = np.random.default_rng(100 + sd)
        perm = r.permutation(ug)
        fold = {u: i % k for i, u in enumerate(perm)}
        f = np.array([fold[u] for u in g])
        oof = np.zeros(len(y))
        for kk in range(k):
            tr, te = f != kk, f == kk
            mu, sdv = X[tr].mean(0), X[tr].std(0) + 1e-9
            w = logreg_fit((X[tr] - mu) / sdv, y[tr], lam)
            Xt = np.hstack([(X[te] - mu) / sdv, np.ones((te.sum(), 1))])
            oof[te] = Xt @ w
        aucs.append(auroc(oof, y))
        oof_all.append(oof)
    return float(np.mean(aucs)), np.mean(oof_all, 0)

def feat(it, key, stat="mrr"):
    return it["f"][key][stat]

def layer_feats(it, key, lo, hi):
    f = it["f"][key]
    return [-np.log(rk / f["k"]) for la, rk in zip(f["layers_all"], f["ranks_all"]) if lo <= la <= hi]

WIN = {"9B": ((4, 16), (21, 30)), "27B": ((16, 40), (49, 62)), "Lightning": ((6, 26), (34, 50))}
res = {}
for m in ["9B", "27B", "Lightning"]:
    for word in ["MM", "MP"]:
        its = [it for it in items if it["model"] == m and it["family"].startswith(word + "_")]
        y = np.array([it["family"].endswith("_ok") for it in its], int)
        g = np.array([it["bridge"] for it in its])
        R = {"n_ok": int(y.sum()), "n_fail": int((1 - y).sum()), "n_bridges": len(set(g))}
        scores = {}
        for site in ["desc_end", "final"]:
            for lens in ["jlens", "logit"]:
                for what in ["attr", "bridge", "other", "third", "ctx"]:
                    for stat in ["top1", "mrr"]:
                        scores[f"{site}|{lens}|{what}|{stat}"] = [feat(it, f"{site}|{lens}|{what}", stat) for it in its]
        for part in ["step1", "step2", "whole", "guess"]:
            scores[f"beh|{part}|margin"] = [it["comp"].get(part, {}).get("margin", np.nan) for it in its]
            scores[f"beh|{part}|p"] = [it["comp"].get(part, {}).get("p_answer", np.nan) for it in its]
        # relation-only baseline (leave-one-bridge-out ok rate of the relation)
        rel = [it["rel"] for it in its]
        lob = []
        for i, it in enumerate(its):
            ys = [y[j] for j in range(len(its)) if rel[j] == rel[i] and g[j] != g[i]]
            lob.append(np.mean(ys) if ys else 0.5)
        scores["base|relation_rate_LOBO"] = lob
        # answer-value prior (leave-one-bridge-out ok rate of items sharing the gold answer string)
        ans = [it["comp"].get("whole", {}).get("expected") for it in its]
        lob2 = []
        for i in range(len(its)):
            ys = [y[j] for j in range(len(its)) if ans[j] == ans[i] and g[j] != g[i]]
            lob2.append(np.mean(ys) if ys else np.mean(y))
        scores["base|answer_value_rate_LOBO"] = lob2
        aucs = {}
        for k_, s in scores.items():
            s = np.asarray(s, float)
            ok = ~np.isnan(s)
            if ok.sum() < 10 or len(set(y[ok])) < 2:
                continue
            a = auroc(s[ok], y[ok])
            lo, hi = boot(s[ok], y[ok], g[ok], B=1000)
            aucs[k_] = {"auc": round(float(a), 3), "ci": [round(float(lo), 3), round(float(hi), 3)], "n": int(ok.sum())}
        # permutation p for the headline
        for k_ in ["desc_end|jlens|attr|mrr", "desc_end|jlens|attr|top1"]:
            aucs[k_]["perm_p"] = perm_p(np.asarray(scores[k_], float), y, B=2000)
        R["auc"] = aucs
        # grouped CV logistic regressions on layer-resolved features
        wd, wf = WIN[m]
        cv = {}
        fJ = np.array([layer_feats(it, "desc_end|jlens|attr", *wd) for it in its])
        fL = np.array([layer_feats(it, "desc_end|logit|attr", *wd) for it in its])
        fB = np.array([layer_feats(it, "desc_end|jlens|bridge", *wd) for it in its])
        fT = np.array([layer_feats(it, "desc_end|jlens|third", *wd) for it in its])
        beh = np.array([[it["comp"].get(p, {}).get("margin", 0.0) or 0.0 for p in ("step1", "step2")] for it in its])
        for name, X in {"J++ desc_end attr (layers)": fJ, "logit desc_end attr (layers)": fL, "J++ desc_end bridge (layers)": fB,
                        "J++ desc_end third (chance target)": fT, "behaviour: hop1+hop2 margins": beh,
                        "behaviour + J++ attr": np.hstack([beh, fJ]), "behaviour + logit attr": np.hstack([beh, fL]),
                        "J++ attr + logit attr": np.hstack([fJ, fL])}.items():
            a, _ = cv_auc(X, y, g)
            cv[name] = round(a, 3)
        # shuffled-label CV control
        ysh = rng.permutation(y)
        cv["J++ attr, shuffled labels"] = round(cv_auc(fJ, ysh, g)[0], 3)
        R["cv_auc"] = cv
        # descriptive means
        R["desc"] = {k_: {"ok": round(float(np.nanmean(np.asarray(scores[k_], float)[y == 1])), 3),
                          "fail": round(float(np.nanmean(np.asarray(scores[k_], float)[y == 0])), 3)}
                     for k_ in ["desc_end|jlens|attr|top1", "desc_end|logit|attr|top1", "desc_end|jlens|other|top1",
                                "desc_end|jlens|third|top1", "desc_end|jlens|bridge|top1", "final|jlens|attr|top1", "final|jlens|other|top1"]}
        res[f"{m}|{word}"] = R
        print(m, word, R["n_ok"], R["n_fail"], R["n_bridges"], flush=True)
json.dump(res, open(sys.argv[2], "w"), indent=1)
