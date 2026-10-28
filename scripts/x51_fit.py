"""x51_fit (batch 51; CPU item 5, and the fit of 51.1's figure): a reader's switch on the two gains of the change,

    logit P(switch) = a·α + b·β (+ c·αβ)            (as written in the brief: no intercept, so P = 0.5 at α = β = 0)
    logit P(switch) = a0 + a·α + b·β (+ c·αβ)       (with an intercept: P at the unedited prompt is free)

fit by maximum likelihood on item-level 0/1 rows, aggregated without loss to successes / trials per (cluster, α, β)
cell. "c is needed" = the likelihood-ratio test of the model with c against the one without (df 1) at p < 0.05; the
test treats rows as independent, so it is anti-conservative under clustering, and the cluster-bootstrap interval of c
stands beside it. Cluster bootstrap: whole clusters drawn with replacement, the draws of x0_necessity.resampled_rates
(sorted cluster keys, numpy default_rng(seed).integers), every fit of a resample on the same draw.

Pure numpy / scipy (no new dependency). Import from another script:

    from scripts import x51_fit as F
    g = F.grid_counts(rows)                      # rows: {"arm": "J(α,β)", "switched": 0/1, "entity": ...}
    fit = F.fit_gain(g["alpha"], g["beta"], g["succ"].sum(0), g["trials"].sum(0), interaction=False, intercept=True)
    fit["predict"](alpha, beta)                  # fitted P(switch)
"""

from __future__ import annotations

import math
import re
from typing import Any

import numpy as np
from scipy import stats

ARM_RE = re.compile(r"^J\(([0-9.]+),([0-9.]+)\)$")
C_ALPHA = 0.05  # "c is needed" at p < 0.05 (likelihood-ratio test, df 1)
MAX_ITER, TOL, COEF_MAX = 200, 1e-9, 40.0  # a coefficient beyond COEF_MAX marks a separated (non-converged) fit


def parse_arm(name: str) -> tuple[float, float] | None:
    """(α, β) of a grid arm 'J(α,β)'; None for any other arm (random corners, the no-U arms, J100)."""
    m = ARM_RE.match(name)
    return (float(m.group(1)), float(m.group(2))) if m else None


def names(interaction: bool, intercept: bool) -> list[str]:
    return [*(["a0"] if intercept else []), "a", "b", *(["c"] if interaction else [])]


def design(alpha: np.ndarray, beta: np.ndarray, interaction: bool, intercept: bool) -> np.ndarray:
    alpha, beta = np.asarray(alpha, float), np.asarray(beta, float)
    cols = [*([np.ones_like(alpha)] if intercept else []), alpha, beta, *([alpha * beta] if interaction else [])]
    return np.stack(cols, axis=1)


def loglik(x: np.ndarray, coef: np.ndarray, succ: np.ndarray, trials: np.ndarray) -> float:
    """Binomial log-likelihood without the combinatorial constant (it cancels in every comparison here)."""
    eta = x @ coef
    return float(-(succ * np.logaddexp(0.0, -eta) + (trials - succ) * np.logaddexp(0.0, eta)).sum())


def fit_binomial(x: np.ndarray, succ: np.ndarray, trials: np.ndarray) -> dict[str, Any]:
    """Newton-Raphson (IRLS) with step halving from zero; converged = the step fell under TOL with every coefficient
    within COEF_MAX (else the data are (quasi-)separated along some direction and the MLE is infinite)."""
    succ, trials = np.asarray(succ, float), np.asarray(trials, float)
    keep = trials > 0
    x, succ, trials = x[keep], succ[keep], trials[keep]
    coef = np.zeros(x.shape[1])
    ll = loglik(x, coef, succ, trials)
    converged = False
    for _ in range(MAX_ITER):
        p = 1.0 / (1.0 + np.exp(-(x @ coef)))
        grad = x.T @ (succ - trials * p)
        hess = x.T @ (x * (trials * p * (1 - p))[:, None])
        try:
            step = np.linalg.solve(hess + 1e-10 * np.eye(len(coef)), grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(hess, grad, rcond=None)[0]
        t = 1.0
        while t > 1e-6:
            new = coef + t * step
            ll_new = loglik(x, new, succ, trials)
            if ll_new >= ll - 1e-12:
                break
            t /= 2
        coef, ll = new, ll_new
        if np.max(np.abs(t * step)) < TOL:
            converged = True
            break
        if np.max(np.abs(coef)) > COEF_MAX:
            break
    converged = converged and bool(np.max(np.abs(coef)) <= COEF_MAX)
    return {"coef": coef, "loglik": ll, "converged": converged}


def fit_gain(alpha, beta, succ, trials, interaction: bool, intercept: bool) -> dict[str, Any]:
    """One fit on the (α, β) cells: the named coefficients, b/a, the log-likelihood, convergence and a predictor."""
    f = fit_binomial(design(alpha, beta, interaction, intercept), succ, trials)
    co = dict(zip(names(interaction, intercept), (float(v) for v in f["coef"]), strict=True))
    coef = f["coef"]

    def predict(a, b):
        return 1.0 / (1.0 + np.exp(-(design(np.atleast_1d(a), np.atleast_1d(b), interaction, intercept) @ coef)))

    return {**co, "b_over_a": co["b"] / co["a"] if co["a"] != 0 else math.nan, "loglik": f["loglik"],
            "converged": f["converged"], "predict": predict}  # fmt: skip


def lr_test(alpha, beta, succ, trials, intercept: bool) -> dict[str, Any]:
    """The model with c against the one without: 2 (ll1 - ll0) ~ chi2(1); c needed iff p < C_ALPHA."""
    f0 = fit_gain(alpha, beta, succ, trials, False, intercept)
    f1 = fit_gain(alpha, beta, succ, trials, True, intercept)
    stat = max(0.0, 2.0 * (f1["loglik"] - f0["loglik"]))
    p = float(stats.chi2.sf(stat, 1))
    return {
        "stat": stat,
        "p": p,
        "df": 1,
        "c_needed": bool(p < C_ALPHA),
        "converged": f0["converged"] and f1["converged"],
    }


def grid_counts(rows: list[dict], cluster: str = "entity") -> dict[str, Any]:
    """The grid arms' rows as successes / trials [clusters, cells] (clusters sorted, cells in (α, β) order)."""
    cells: dict[tuple[float, float], int] = {}
    for r in rows:
        ab = parse_arm(r["arm"])
        if ab is not None:
            cells.setdefault(ab, 0)
    cell_list = sorted(cells)
    ci = {ab: i for i, ab in enumerate(cell_list)}
    keys = sorted({r[cluster] for r in rows if parse_arm(r["arm"]) is not None})
    ki = {k: i for i, k in enumerate(keys)}
    succ = np.zeros((len(keys), len(cell_list)))
    trials = np.zeros_like(succ)
    for r in rows:
        ab = parse_arm(r["arm"])
        if ab is None:
            continue
        succ[ki[r[cluster]], ci[ab]] += int(r["switched"])
        trials[ki[r[cluster]], ci[ab]] += 1
    return {"alpha": np.array([a for a, _ in cell_list]), "beta": np.array([b for _, b in cell_list]),
            "succ": succ, "trials": trials, "clusters": keys, "rows": int(trials.sum())}  # fmt: skip


def resample_weights(n_clusters: int, n_boot: int, seed: int) -> np.ndarray:
    """[n_boot, n_clusters] counts of each cluster per resample (x0_necessity.resampled_rates' draws)."""
    pick = np.random.default_rng(seed).integers(0, n_clusters, size=(n_boot, n_clusters))
    return np.stack([np.bincount(p, minlength=n_clusters) for p in pick]).astype(float)


def interval(x: np.ndarray) -> list[float]:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        return [math.nan, math.nan]
    lo, hi = np.percentile(x, [2.5, 97.5])
    return [float(lo), float(hi)]


def gain_fit(rows: list[dict], n_boot: int, seed: int, intercept: bool, cluster: str = "entity") -> dict[str, Any]:
    """One reader's rows: the additive fit (a, b, b/a), the fit with c, the likelihood-ratio test, each coefficient's
    cluster-bootstrap interval (non-converged resamples dropped and counted), the observed and fitted cell shares."""
    g = grid_counts(rows, cluster)
    al, be, s, n = g["alpha"], g["beta"], g["succ"].sum(0), g["trials"].sum(0)
    f0 = fit_gain(al, be, s, n, False, intercept)
    f1 = fit_gain(al, be, s, n, True, intercept)
    lrt = lr_test(al, be, s, n, intercept)
    w = resample_weights(len(g["clusters"]), n_boot, seed)
    draws: dict[str, list[float]] = {k: [] for k in ("a", "b", "b_over_a", "c", "c_b_over_a")}
    bad = {"additive": 0, "with_c": 0}
    for wi in w:
        sb, nb = wi @ g["succ"], wi @ g["trials"]
        b0 = fit_gain(al, be, sb, nb, False, intercept)
        b1 = fit_gain(al, be, sb, nb, True, intercept)
        ok0, ok1 = b0["converged"], b1["converged"]
        bad["additive"] += not ok0
        bad["with_c"] += not ok1
        for k in ("a", "b", "b_over_a"):
            draws[k].append(b0[k] if ok0 else math.nan)
        draws["c"].append(b1["c"] if ok1 else math.nan)
        draws["c_b_over_a"].append(b1["b_over_a"] if ok1 else math.nan)
    shares = np.where(w @ g["trials"] > 0, (w @ g["succ"]) / np.maximum(w @ g["trials"], 1), np.nan)
    out = {"intercept": intercept, "n_rows": g["rows"], "n_clusters": len(g["clusters"]), "n_boot": n_boot,
           "additive": {k: v for k, v in f0.items() if k != "predict"},
           "with_c": {k: v for k, v in f1.items() if k != "predict"}, "lrt": lrt,
           "ci": {k: interval(np.array(v)) for k, v in draws.items()}, "nonconverged_resamples": bad,
           "cells": [{"alpha": float(a), "beta": float(b), "n": int(nn), "share": float(ss / nn) if nn else math.nan,
                      "share_ci": interval(shares[:, i]), "fit_additive": float(f0["predict"](a, b)[0]),
                      "fit_with_c": float(f1["predict"](a, b)[0])}
                     for i, (a, b, ss, nn) in enumerate(zip(al, be, s, n, strict=True))]}  # fmt: skip
    return out
