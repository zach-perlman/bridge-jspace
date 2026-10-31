"""nn_provenance_read (prereg amendment 63, note 34): the provenance probe's probes, controls and readings, from a
scripts/nn_provenance.py run. CPU only (numpy / scipy; the box's venv has no sklearn, so the L2 logistic regression is fit here
by L-BFGS on sklearn's objective, C * sum(log-loss) + ||w||^2 / 2, intercept unpenalised).

Probe items: the run's CN / DN items labelled memory (1) or passage (0); named (CN), described (DN) and pooled scored
separately. Features (one site; the band: each feature averaged over the band's layers; descriptive: each layer read):
  F  the residual h
  J  h's coordinates in the J++ basis of the item's relation's answer tokens. The relations' bases differ, so one pooled
     probe takes them in a block layout: each relation's m_rel coordinates in its own columns, zeros elsewhere (sum of the
     m_rel columns). R and U the same (R: the first m_rel columns of rotation(d, 888 + layer); U: the unembedding rows).
  Jall / Rall / Uall   one basis over the union of the relations' tokens (beside-check of the block layout; not pre-registered)
  Z  the J++ logit of the true value minus the false value's, as a score (no training)
Probe: standardised features (training rows' mean and sd), L2 logistic regression, C from {0.01, 0.1, 1, 10} by inner
5-fold CV grouped by bridge (mean held-out AUC over inner folds with both classes; ties: the smaller C), outer 5-fold CV
grouped by bridge (bridges shuffled with random.Random(0), dealt round-robin; inner: random.Random(1000 + outer fold)).
AUC of the held-out scores pooled over the outer folds; 95% interval: bootstrap over bridges, 2000 resamples, seed 0
(nn_v5_read.boot_ci's quantiles).
Control: F with labels shuffled within relation (5 permutations, random.Random(seed 0-4)), the whole procedure. Beside
(not pre-registered): on the pooled subset, also shuffled within relation x word (keeps the word -> label link).
Reading (amendment 63 addendum: lens vs random, the same dimension, both trained; band; s1 and s3; each subset):
  "lens no better than random": AUC_J <= AUC_R + 0.05
  "lens better": AUC_J >= AUC_R + 0.10, J's interval above R's (not overlapping)
  otherwise "unclear". s2 descriptive. (Note 34's first rule, AUC_F vs AUC_J, is no longer a reading.)
F is descriptive beside the memory-strength baseline B: the scene's closed-book named recall (kc2ctl H2) cand2 answer
margin, computed by scripts/nn_provenance.py, as a score (no training). "F adds beyond memory strength": AUC_F >= AUC_B +
0.10, F's interval above B's. Beside (labelled): B_correct, H2 right / wrong from the controls run (correct_cand2).
Time course (descriptive): AUC_F and AUC_J (R beside) at every layer read at s1 and s3; beside it, by lens layer at s3,
the share of items whose eventual answer (memory: X's true value; passage: its false value) is the J++ top-1 among the
relation's values, and the first layer where that share is >= 50%.
Claim read: per item and layer, the number of the fixed list's words among the J++ top-20 letter tokens at s2 (note 26's
fold, whole token), and whether there is at least one; the band's measure: the mean over its layers. Conflict (CN, DN)
minus true control (TN, TD), paired by scene; points; bootstrap over bridges. The same for the 25 control tokens.
  "conflict seen": contrast >= 10 points, interval above 0, the control's contrast <= 1/3 of it; "not seen": the
  interval holds 0; otherwise "weak".

python scripts/nn_provenance_read.py RUN [--eligible-only] [--no-layers] [--jobs 8]   (RUN: a name under results/nn_provenance or a path)
python scripts/nn_provenance_read.py --claim RUN_9B RUN_27B RUN_LIGHTNING   (the three models' readings side by side, from their
       probe_read.json; the addendum states no cross-model rule, so no combined verdict)
"""

from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")

import argparse  # noqa: E402
import collections  # noqa: E402
import json  # noqa: E402
import multiprocessing  # noqa: E402
import random  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402
from scipy.special import expit, log_expit  # noqa: E402
from scipy.stats import rankdata  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
RES = ROOT / "results" / "nn_provenance"
CS = (0.01, 0.1, 1.0, 10.0)
K_OUTER = K_INNER = 5
N_BOOT = 2000
N_PERM = 5
SITES = ("s1", "s2", "s3")
SETS = ("F", "J", "R", "U")
ALT = ("Jall", "Rall", "Uall")
SUBSETS = {"named": ("CN",), "described": ("DN",), "pooled": ("CN", "DN")}
PAIRS = (("CN", "TN"), ("DN", "TD"))
G: dict = {}  # the run's arrays, set before the worker pool forks


# ---- the probe -------------------------------------------------------------------------------------------------------
def auc(s: np.ndarray, y: np.ndarray) -> float:
    y = y.astype(bool)
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot_ci(values_by_group: dict, fn, n=N_BOOT, seed=0):
    """nn_v5_read.boot_ci: resample the groups (bridges) with replacement; the 2.5% and 97.5% quantiles."""
    keys, rng, out = sorted(values_by_group), random.Random(seed), []
    for _ in range(n):
        v = fn([x for k in (rng.choice(keys) for _ in keys) for x in values_by_group[k]])
        if v == v:
            out.append(v)
    out.sort()
    return [round(out[int(0.025 * len(out))], 4), round(out[int(0.975 * len(out)) - 1], 4)] if out else None


def auc_ci(s, y, groups):
    ok = ~np.isnan(s)
    by = collections.defaultdict(list)
    for k in np.flatnonzero(ok):
        by[groups[k]].append(k)

    def fn(idx):
        idx = np.asarray(idx)
        return auc(s[idx], y[idx])

    return boot_ci(by, fn)


def group_folds(groups: np.ndarray, k: int, seed: int) -> np.ndarray:
    ug = sorted(set(groups.tolist()))
    random.Random(seed).shuffle(ug)
    k = min(k, len(ug))
    f = {g: i % k for i, g in enumerate(ug)}
    return np.array([f[g] for g in groups.tolist()])


def prep(Xtr: np.ndarray):
    """Standardise on the training rows; when there are more features than rows, the exact reduction to the rows' span
    (an L2 solution lies in it): coordinates on Q, Xs.T = Q R."""
    Xtr = Xtr.astype(np.float64)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd < 1e-12] = 1.0
    Xs = (Xtr - mu) / sd
    if Xs.shape[1] > Xs.shape[0]:  # an orthonormal basis Q of the rows' span from the Gram matrix (6-10x faster than a QR here)
        w, V = np.linalg.eigh(Xs @ Xs.T)
        keep = w > 1e-10 * w.max()
        Q = Xs.T @ (V[:, keep] / np.sqrt(w[keep]))
        return Xs @ Q, lambda X: ((X.astype(np.float64) - mu) / sd) @ Q
    return Xs, lambda X: (X.astype(np.float64) - mu) / sd


def fit(Z: np.ndarray, y: np.ndarray, C: float, theta0=None) -> np.ndarray:
    """L2 logistic regression, sklearn's objective divided by C * n (same minimiser): mean log-loss + ||w||^2 / (2 C n)."""
    n, p = Z.shape
    lam = 1.0 / (C * n)
    ys = 2.0 * y - 1.0

    def f(t):
        w, b = t[:p], t[p]
        z = Z @ w + b
        loss = -log_expit(ys * z).mean() + 0.5 * lam * (w @ w)
        r = -ys * expit(-ys * z) / n
        return loss, np.concatenate([Z.T @ r + lam * w, [r.sum()]])

    t0 = np.zeros(p + 1) if theta0 is None else theta0
    res = minimize(f, t0, jac=True, method="L-BFGS-B", options={"maxiter": 5000, "gtol": 1e-7, "ftol": 1e-12})
    return res.x


def pick_C(X, y, groups, seed):
    folds = group_folds(groups, K_INNER, seed)
    score = collections.defaultdict(list)
    for f in sorted(set(folds.tolist())):
        tr, va = folds != f, folds == f
        if len(set(y[tr].tolist())) < 2 or len(set(y[va].tolist())) < 2:
            continue
        Ztr, tf = prep(X[tr])
        Zva, th = tf(X[va]), None
        for C in CS:  # ascending, warm-started
            th = fit(Ztr, y[tr], C, th)
            score[C].append(auc(Zva @ th[:-1] + th[-1], y[va]))
    if not score:
        return 1.0, False
    return max(CS, key=lambda C: (np.mean(score[C]), -C)), True


def cv_scores(X, y, groups):
    folds = group_folds(groups, K_OUTER, 0)
    s, chosen = np.full(len(y), np.nan), []
    for f in sorted(set(folds.tolist())):
        tr, te = folds != f, folds == f
        if len(set(y[tr].tolist())) < 2:
            chosen.append(None)
            continue
        C, inner_ok = pick_C(X[tr], y[tr], groups[tr], 1000 + f)
        Ztr, tf = prep(X[tr])
        th = fit(Ztr, y[tr], C)
        s[te] = tf(X[te]) @ th[:-1] + th[-1]
        chosen.append(C if inner_ok else f"{C} (default: no inner fold with both classes)")
    return s, chosen


# ---- features --------------------------------------------------------------------------------------------------------
def layer_idx(spec):
    return G["band_idx"] if spec == "band" else [G["layers"].index(spec)]


def features(site: str, spec, fs: str, rows: np.ndarray) -> np.ndarray:
    li = layer_idx(spec)
    if fs == "F":
        return G["h"][site][np.ix_(rows, li)].astype(np.float32).mean(1)
    if fs in ALT:
        return G[fs][site][np.ix_(rows, li)].mean(1)
    P = G[fs][site][np.ix_(rows, li)].mean(1)  # [n, m_max], each relation's coordinates first
    X = np.zeros((len(rows), G["m_total"]), dtype=np.float32)
    for k, r in enumerate(rows):
        rel = G["rel"][r]
        o, m = G["offset"][rel], G["m"][rel]
        X[k, o : o + m] = P[k, :m]
    return X


def subset_rows(sub: str) -> np.ndarray:
    return np.array([r for r in G["rows"] if G["word"][r] in SUBSETS[sub]], dtype=int)


def shuffle_within(y: np.ndarray, strata: list, seed: int) -> np.ndarray:
    rng, y2 = random.Random(seed), y.copy()
    for st in sorted(set(strata)):
        idx = [k for k, x in enumerate(strata) if x == st]
        perm = idx[:]
        rng.shuffle(perm)
        y2[idx] = y[perm]
    return y2


def task(t):
    """One probe: (site, layer spec, feature set, subset, shuffle) -> AUC, interval, n, chosen C per outer fold."""
    site, spec, fs, sub, shuf = t
    rows = subset_rows(sub)
    y = G["y"][rows].copy()
    groups = np.array([G["bridge"][r] for r in rows])
    if shuf:
        kind, seed = shuf
        strata = [G["rel"][r] if kind == "rel" else (G["rel"][r], G["word"][r]) for r in rows]
        y = shuffle_within(y, strata, seed)
    X = features(site, spec, fs, rows)
    s, chosen = cv_scores(X, y, groups)
    ok = ~np.isnan(s)
    return t, {"auc": round(auc(s[ok], y[ok]), 4), "ci": auc_ci(s, y, groups), "n_scored": int(ok.sum()), "C": chosen, "dim": int(X.shape[1])}


def z_auc(site, spec, sub):
    rows = subset_rows(sub)
    z = G["Z"][site][np.ix_(rows, layer_idx(spec))].mean(1).astype(np.float64)
    y, groups = G["y"][rows], np.array([G["bridge"][r] for r in rows])
    return {"auc": round(auc(z, y), 4), "ci": auc_ci(z, y, groups), "n_scored": len(rows)}


def reading(c: dict, J="J", R="R") -> str:
    """Amendment 63 addendum: lens vs random."""
    aJ, aR = c[J]["auc"], c[R]["auc"]
    if aJ != aJ or aR != aR:
        return "unclear (an AUC is undefined)"
    if aJ <= aR + 0.05:
        return "lens no better than random"
    if aJ >= aR + 0.10 and c[J]["ci"] and c[R]["ci"] and c[J]["ci"][0] > c[R]["ci"][1]:
        return "lens better"
    return "unclear"


def f_beyond_b(c: dict) -> bool:
    """Amendment 63 addendum: "F adds beyond memory strength"."""
    aF, aB = c["F"]["auc"], c["B"]["auc"]
    return bool(aF == aF and aB == aB and aF >= aB + 0.10 and c["F"]["ci"] and c["B"]["ci"] and c["F"]["ci"][0] > c["B"]["ci"][1])


def b_auc(sub, key="h2_margin"):
    """B: the scene's closed-book named recall (H2) cand2 margin (key h2_margin), or beside it, H2 right = 1 / wrong = 0
    (key h2), as the score for memory (no training)."""
    rows = [r for r in subset_rows(sub) if G[key][r] is not None]
    rows = np.array(rows, dtype=int)
    if not len(rows):
        return {"auc": float("nan"), "ci": None, "n_scored": 0}
    b = np.array([float(G[key][r]) for r in rows])
    y, groups = G["y"][rows], np.array([G["bridge"][r] for r in rows])
    extra = {"share_h2_right": round(100 * float(b.mean()), 1)} if key == "h2" else {"median_margin": round(float(np.median(b)), 3)}
    return {"auc": round(auc(b, y), 4), "ci": auc_ci(b, y, groups), "n_scored": len(rows), **extra}


def time_course(run_dir: Path) -> dict:
    """By lens layer at s3: the share of items whose eventual answer is the J++ top-1 among the relation's values."""
    import torch

    blob = torch.load(run_dir / "s3_ranks.pt", map_location="cpu", weights_only=True)
    lay, rt, rf = blob["layers"], blob["rank_true"].numpy(), blob["rank_false"].numpy()
    out = {}
    for sub in SUBSETS:
        rows = subset_rows(sub)
        rec = {}
        for name, sel in (("all", rows), ("memory items", rows[G["y"][rows] == 1]), ("passage items", rows[G["y"][rows] == 0])):
            if not len(sel):
                continue
            top1 = np.where(G["y"][sel][:, None] == 1, rt[sel] == 1, rf[sel] == 1)  # the eventual answer is the top-1
            share = [round(100 * float(x), 1) for x in top1.mean(0)]
            first = next((la for la, x in zip(lay, share, strict=True) if x >= 50), None)
            rec[name] = {"n": int(len(sel)), "first_layer_ge_50": first, "share_by_layer": dict(zip([f"L{la}" for la in lay], share, strict=True))}
        out[sub] = rec
    return out


# ---- the claim read --------------------------------------------------------------------------------------------------
def claim_read(run_dir: Path, man: dict) -> dict:
    import torch

    from scripts.nn_topk_read import fold

    blob = torch.load(run_dir / "claim_top20.pt", map_location="cpu", weights_only=True)
    top, layers, band = blob["top"].numpy(), blob["layers"], blob["band"]
    vocab = {int(k): v for k, v in json.loads((run_dir / "claim_vocab.json").read_text()).items()}
    idx = [json.loads(line) for line in (run_dir / "claim_index.jsonl").read_text().splitlines()]
    lst, ctl = set(man["claim_list"]), {c["fold"] for c in man["control_tokens"]}
    is_l = {t: fold(s) in lst for t, s in vocab.items()}
    is_c = {t: fold(s) in ctl for t, s in vocab.items()}
    lut_l, lut_c = np.zeros(max(vocab) + 1, dtype=np.int64), np.zeros(max(vocab) + 1, dtype=np.int64)
    for t in vocab:
        lut_l[t], lut_c[t] = is_l[t], is_c[t]
    cnt_l, cnt_c = lut_l[top].sum(-1), lut_c[top].sum(-1)  # [items, layers]: list words / control tokens in the top-20
    bi = [layers.index(la) for la in band]
    by = {(r["word"], r["scene"]): r for r in idx}
    out = {"band": band, "layers": layers, "n_items": dict(collections.Counter(r["word"] for r in idx)), "contrasts": {}, "per_layer": {}}
    for name, pairs in (("CN-TN", PAIRS[:1]), ("DN-TD", PAIRS[1:]), ("pooled", PAIRS)):
        units = []  # (bridge, conflict row, control row)
        for c, t in pairs:
            for (w, sc), r in sorted(by.items()):
                if w == c and (t, sc) in by:
                    units.append((r["bridge"], r["crow"], by[(t, sc)]["crow"]))
        if not units:
            continue
        rec = {"n_pairs": len(units)}
        for what, cnt in (("list", cnt_l), ("control", cnt_c)):
            has = (cnt > 0).astype(float)
            bh, bc = has[:, bi].mean(1), cnt[:, bi].mean(1)  # the band's measure: the mean over its layers
            g = collections.defaultdict(list)
            for b, i, j in units:
                g[b].append((bh[i] - bh[j], bc[i] - bc[j]))
            dh = [x for v in g.values() for x, _ in v]
            dc = [x for v in g.values() for _, x in v]
            rec[what] = {"share_conflict": round(100 * float(np.mean([bh[i] for _, i, _ in units])), 1),
                         "share_true": round(100 * float(np.mean([bh[j] for _, _, j in units])), 1),
                         "contrast_share": round(100 * float(np.mean(dh)), 1),
                         "ci_share": (lambda c: [round(100 * c[0], 1), round(100 * c[1], 1)] if c else None)(boot_ci(g, lambda us: float(np.mean([a for a, _ in us])) if us else float("nan"))),
                         "mean_count_conflict": round(float(np.mean([bc[i] for _, i, _ in units])), 3),
                         "mean_count_true": round(float(np.mean([bc[j] for _, _, j in units])), 3),
                         "contrast_count": round(float(np.mean(dc)), 3),
                         "ci_count": boot_ci(g, lambda us: float(np.mean([b for _, b in us])) if us else float("nan"))}  # fmt: skip
            out["per_layer"].setdefault(name, {})[what] = {f"L{la}": round(100 * float(np.mean([int(cnt[i, k] > 0) - int(cnt[j, k] > 0) for _, i, j in units])), 1)
                                                           for k, la in enumerate(layers)}  # fmt: skip
        L, Cc = rec["list"], rec["control"]
        ci = L["ci_share"]
        if ci and L["contrast_share"] >= 10 and ci[0] > 0 and Cc["contrast_share"] <= L["contrast_share"] / 3:
            rec["reading"] = "conflict seen"
        elif ci and ci[0] <= 0 <= ci[1]:
            rec["reading"] = "not seen"
        else:
            rec["reading"] = "weak"
        out["contrasts"][name] = rec
    # mechanics: CN and DN share the prompt up to s2 (and TN / TD), so their s2 lists should agree up to batch numerics
    same = [np.array_equal(top[by[("CN", sc)]["crow"]], top[by[("DN", sc)]["crow"]]) for (w, sc) in by if w == "CN" and ("DN", sc) in by]
    out["check_CN_DN_same_s2_lists"] = f"{sum(same)} of {len(same)} scenes identical at every layer"
    return out


# ---- main ------------------------------------------------------------------------------------------------------------
def load(run_dir: Path, eligible_only: bool) -> dict:
    import torch

    torch.set_num_threads(1)
    man = json.loads((run_dir / "manifest.json").read_text())
    idx = [json.loads(line) for line in (run_dir / "index.jsonl").read_text().splitlines()]
    G["layers"], G["band"] = man["layers"], man["band"]
    G["band_idx"] = [G["layers"].index(la) for la in G["band"]]
    G["m"] = man["m"]
    rels = man["relations"]
    G["offset"], o = {}, 0
    for r in rels:
        G["offset"][r] = o
        o += G["m"][r]
    G["m_total"] = o
    for k in ("h", "J", "R", "U", *ALT, "Z"):
        G[k] = {}
    for s in SITES:
        blob = torch.load(run_dir / f"site_{s}.pt", map_location="cpu", weights_only=True)
        G["h"][s] = blob["h"].numpy()
        for k in ("J", "R", "U", *ALT, "Z"):
            G[k][s] = blob[k].numpy()
    assert len(idx) == G["h"]["s1"].shape[0]
    G["y"] = np.array([1 if r["label"] == "memory" else 0 for r in idx])
    G["rel"] = [r["rel"] for r in idx]
    G["word"] = [r["word"] for r in idx]
    G["bridge"] = [r["bridge"] for r in idx]
    G["h2"] = [r.get("h2_correct") for r in idx]
    G["h2_margin"] = [r.get("h2_margin") for r in idx]
    G["rows"] = [k for k, r in enumerate(idx) if not eligible_only or r["known"]]
    return man


def main(a) -> None:
    run_dir = Path(a.run) if "/" in a.run else RES / a.run
    t0 = time.time()
    man = load(run_dir, a.eligible_only)
    out: dict = {"run": man["run"], "target": man["target"], "band": G["band"], "eligible_only": a.eligible_only,
                 "probe": {"Cs": CS, "outer_folds": K_OUTER, "inner_folds": K_INNER, "boot": N_BOOT, "perms": N_PERM,
                           "fold_seed": "random.Random(0) outer, random.Random(1000 + fold) inner", "boot_seed": 0,
                           "dims": {"F": int(G["h"]["s1"].shape[-1]), "J/R/U (block layout)": G["m_total"], "per relation m": G["m"],
                                    "union m": int(G["Jall"]["s1"].shape[-1])}},
                 "n": {}, "band_read": {}, "layers_read": {}}  # fmt: skip
    for sub in SUBSETS:
        rows = subset_rows(sub)
        out["n"][sub] = {"memory": int(G["y"][rows].sum()), "passage": int(len(rows) - G["y"][rows].sum()),
                         "bridges": len({G["bridge"][r] for r in rows})}  # fmt: skip
    tasks = [(s, "band", fs, sub, None) for s in SITES for sub in SUBSETS for fs in SETS + ALT]
    tasks += [(s, "band", "F", sub, ("rel", p)) for s in SITES for sub in SUBSETS for p in range(N_PERM)]
    tasks += [(s, "band", "F", "pooled", ("relword", p)) for s in SITES for p in range(N_PERM)]
    if not a.no_layers:
        tasks += [(s, la, fs, sub, None) for la in G["layers"] for s in SITES for sub in SUBSETS for fs in SETS]
    print(f"{len(tasks)} probes, {a.jobs} workers; n {out['n']}", flush=True)
    res = {}
    with ProcessPoolExecutor(max_workers=a.jobs, mp_context=multiprocessing.get_context("fork")) as ex:  # workers inherit G
        for k, (t, r) in enumerate(ex.map(task, tasks, chunksize=1)):
            res[t] = r
            if (k + 1) % 50 == 0:
                print(f"  {k + 1}/{len(tasks)} probes, {time.time() - t0:.0f}s", flush=True)
    for s in SITES:
        for sub in SUBSETS:
            c = {fs: res[(s, "band", fs, sub, None)] for fs in SETS + ALT}
            c["Z"] = z_auc(s, "band", sub)
            perm = [res[(s, "band", "F", sub, ("rel", p))]["auc"] for p in range(N_PERM)]
            c["F_shuffled_within_relation"] = {"aucs": perm, "mean": round(float(np.nanmean(perm)), 4)}
            if sub == "pooled":
                pw = [res[(s, "band", "F", sub, ("relword", p))]["auc"] for p in range(N_PERM)]
                c["F_shuffled_within_relation_word (not pre-registered)"] = {"aucs": pw, "mean": round(float(np.nanmean(pw)), 4)}
            c["B"] = b_auc(sub)
            c["B_correct (H2 right/wrong, beside)"] = b_auc(sub, "h2")
            c["F_adds_beyond_memory_strength"] = f_beyond_b(c)
            if s in ("s1", "s3"):
                c["reading"] = reading(c)
            c["reading_union_basis (not pre-registered)"] = reading(c, "Jall", "Rall")
            out["band_read"].setdefault(s, {})[sub] = c
    if not a.no_layers:
        for la in G["layers"]:
            for s in SITES:
                for sub in SUBSETS:
                    c = {fs: {k: res[(s, la, fs, sub, None)][k] for k in ("auc", "ci")} for fs in SETS}
                    c["Z"] = z_auc(s, la, sub)
                    out["layers_read"].setdefault(f"L{la}", {}).setdefault(s, {})[sub] = c
    tc = {"s3_top1_eventual_answer": time_course(run_dir), "auc_by_layer": {}}
    for s in ("s1", "s3"):
        for sub in SUBSETS:
            tc["auc_by_layer"].setdefault(s, {})[sub] = {f"L{la}": {fs: out["layers_read"][f"L{la}"][s][sub][fs]["auc"] for fs in ("F", "J", "R")}
                                                         for la in G["layers"]} if not a.no_layers else None  # fmt: skip
    out["time_course"] = tc
    out["claim_read"] = claim_read(run_dir, man)
    out["seconds"] = round(time.time() - t0)
    path = run_dir / ("probe_read_eligible.json" if a.eligible_only else "probe_read.json")
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(f"\n{man['run']} ({man['target']}), band L{G['band'][0]}-{G['band'][-1]}; AUC [95% CI over bridges]; n {out['n']}")
    for s in SITES:
        for sub in SUBSETS:
            c = out["band_read"][s][sub]
            f = lambda k: f"{c[k]['auc']:.3f}" + (f" [{c[k]['ci'][0]:.2f},{c[k]['ci'][1]:.2f}]" if c[k]["ci"] else " [-]")  # noqa: E731
            print(f"  {s} {sub:9s} J {f('J')}  R {f('R')}  -> {c.get('reading', 'descriptive')}  |  F {f('F')}  B {f('B')}  F>B+.10 {c['F_adds_beyond_memory_strength']}  Bcorrect {c['B_correct (H2 right/wrong, beside)']['auc']:.3f}"
                  f"  |  U {f('U')}  Z {f('Z')}  shufF {c['F_shuffled_within_relation']['mean']:.3f}  (union basis: J {c['Jall']['auc']:.3f} R {c['Rall']['auc']:.3f})")  # fmt: skip
    for sub, rec in out["time_course"]["s3_top1_eventual_answer"].items():
        print(f"  s3 J++ top-1 = eventual answer, first layer >= 50%: {sub:9s} " + "; ".join(f"{k} (n {v['n']}): {v['first_layer_ge_50']}" for k, v in rec.items()))
    for name, r in out["claim_read"]["contrasts"].items():
        L, C_ = r["list"], r["control"]
        print(f"  claim read {name:7s} n {r['n_pairs']:4d}: list share {L['share_conflict']:.1f} vs {L['share_true']:.1f}, contrast {L['contrast_share']:+.1f} {L['ci_share']}"
              f"; control contrast {C_['contrast_share']:+.1f} -> {r['reading']}")  # fmt: skip
    print("  " + out["claim_read"]["check_CN_DN_same_s2_lists"])
    print(f"written {path} ({out['seconds']}s)")


def claim(runs: list[str], out_path: str | None) -> None:
    """The three models side by side. Note 34's cross-model claim was built on its first rule ("monitor blind"), which the
    amendment 63 addendum dropped without stating a new cross-model rule, so this tabulates and gives no combined verdict."""
    reads = {}
    for r in runs:
        d = Path(r) if "/" in r else RES / r
        reads[r] = json.loads((d / "probe_read.json").read_text())
    out = {"runs": runs, "note": "no pre-registered cross-model rule after the amendment 63 addendum; tabulated only"}
    for sub in SUBSETS:
        out[sub] = {s: {r: {"reading": reads[r]["band_read"][s][sub].get("reading"),
                            "F_adds_beyond_memory_strength": reads[r]["band_read"][s][sub].get("F_adds_beyond_memory_strength"),
                            **{k: reads[r]["band_read"][s][sub][k]["auc"] for k in ("J", "R", "F", "B")}} for r in runs}
                    for s in ("s1", "s3")}  # fmt: skip
        for s in ("s1", "s3"):
            print(f"{sub:9s} {s} " + " | ".join(f"{r}: {v['reading']} (J {v['J']:.3f} R {v['R']:.3f}; F {v['F']:.3f} B {v['B']:.3f})" for r, v in out[sub][s].items()))
    p = Path(out_path) if out_path else RES / "claim_across_models.json"
    p.write_text(json.dumps(out, indent=1) + "\n")
    print(f"written {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", nargs="*")
    ap.add_argument("--claim", action="store_true", help="the three models' readings side by side, from their probe_read.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--eligible-only", action="store_true", help="probe items of note 30's eligible scenes only (descriptive)")
    ap.add_argument("--no-layers", action="store_true", help="skip the descriptive every-4th-layer probes")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    if args.claim:
        assert len(args.run) == 3, "--claim takes the three models' runs"
        claim(args.run, args.out)
    else:
        assert len(args.run) == 1
        main(argparse.Namespace(run=args.run[0], **{k: v for k, v in vars(args).items() if k != "run"}))
