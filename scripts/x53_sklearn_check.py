"""53.2 (Dan's critic_1125: "Check one cell against sklearn."): one probe cell of scripts/x53_monitor.py refit with
sklearn's LogisticRegression on the same folds, C = 1.0, standardised features, in the full feature space (no
training-span reduction), against x53_monitor's scipy L-BFGS fit in the training span. sklearn is not a project
dependency: a one-off run with

uv run --with scikit-learn python scripts/x53_sklearn_check.py --states-root <dir with the pulled states>

Cell: the 9B, main test, the last token of the lookup's prompt (T), target (c) the lookup's answer digit (held-out
entities), layer 20, the full residual; beside: (b) the slot at the bridge word, layer 16, the J++ part k = 25. Every
fold of every seed (5 x 5), as the probe stage runs them. Writes results/x53_monitor/sklearn_check-<UTC>/{note.md,
check.json}.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x53_monitor as M

RUN = "qwen35_9b_x53_monitor"
CELLS = (("T", "c", 20, "full"), ("B", "b", 16, "jpp25"))  # the first is the check; the second beside


def cell(run_dir: Path, s: str, pos: str, target: str, layer: int, feature: str) -> dict:
    import sklearn
    from sklearn.linear_model import LogisticRegression

    layers = json.loads((run_dir / "manifest.json").read_text())["layers"]
    li = layers.index(layer)
    rows = M.row_table(M.X.read_jsonl(run_dir / f"cases_{s}.jsonl"))
    n = len(rows["entity"])
    m = M.ROW_OF[(pos, target)]
    arr = np.load(run_dir / f"states_{s}_{'h' if feature == 'full' else feature}.npy", mmap_mode="r")
    x = np.asarray(arr[li][:, :, m], dtype=np.float64).reshape(n, -1)
    y = rows[f"y_{target}"]
    groups = rows[M.GROUP_BY[target]]
    ours, theirs = np.zeros((M.N_SEEDS, n), bool), np.zeros((M.N_SEEDS, n), bool)
    agree = np.zeros((M.N_SEEDS, n), bool)
    for seed in range(M.N_SEEDS):
        folds = M.fold_ids(groups, seed)
        for f in range(M.N_FOLDS):
            te = folds == f
            tr = ~te
            ztr, zte = M.standardize(x[tr], x[te])
            ctr, cte = M.span_coords(ztr, zte)
            p_ours = M.logistic(ctr, y[tr], cte)
            clf = LogisticRegression(C=M.C_REG, max_iter=20000, tol=1e-8)
            clf.fit(ztr, y[tr])
            p_sk = clf.predict(zte)
            ours[seed, te], theirs[seed, te] = p_ours == y[te], p_sk == y[te]
            agree[seed, te] = p_ours == p_sk
    return {"set": s, "position": pos, "target": target, "layer": layer, "feature": feature, "rows": n,
            "acc_scipy_span": float(ours.mean()), "acc_sklearn_full": float(theirs.mean()),
            "diff": float(ours.mean() - theirs.mean()), "predictions_agree": float(agree.mean()),
            "per_seed_scipy": [float(v) for v in ours.mean(1)], "per_seed_sklearn": [float(v) for v in theirs.mean(1)],
            "sklearn": sklearn.__version__, "sklearn_settings": {"C": M.C_REG, "max_iter": 20000, "tol": 1e-8,
                                                                 "solver": "lbfgs (default)", "penalty": "l2"}}  # fmt: skip


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--states-root", type=Path, default=M.RESULTS)
    a = ap.parse_args()
    t0 = time.time()
    res = [cell(a.states_root / RUN, "main", *c) for c in CELLS]
    out = M.RESULTS / f"sklearn_check-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    blob = {"what": "53.2's probe (scipy L-BFGS in the training span) vs sklearn LogisticRegression (full space), "
            "same folds (5 seeds x 5-fold), C = 1.0, standardised features", "run": RUN, "cells": res,
            "seconds": round(time.time() - t0, 1)}  # fmt: skip
    (out / "check.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = ["# 53.2: one probe cell against sklearn (critic_1125)", "",
             f"Run {RUN} (main test), same folds as scripts/x53_monitor.py (5 seeds x 5-fold), C = {M.C_REG}, features "
             "standardised on the training rows. Ours: multinomial logistic, sklearn's objective, scipy L-BFGS in the "
             "training rows' span (gtol 1e-3). sklearn: LogisticRegression (lbfgs, l2, max_iter 20000, tol 1e-8) on "
             "the full standardised features (no span reduction). UNVERIFIED.", "",
             "| cell | rows | held-out acc, ours | held-out acc, sklearn | ours - sklearn | predictions agree |",
             "|---|---|---|---|---|---|"]  # fmt: skip
    for i, r in enumerate(res):
        tag = "the check" if i == 0 else "beside"
        lines.append(f"| {tag}: {r['position']}, target ({r['target']}), L{r['layer']}, {r['feature']} | {r['rows']} | "
                     f"{r['acc_scipy_span']:.4f} | {r['acc_sklearn_full']:.4f} | {r['diff']:+.4f} | "
                     f"{r['predictions_agree']:.4f} |")  # fmt: skip
    lines += [
        "",
        f"sklearn {res[0]['sklearn']}, run once with `uv run --with scikit-learn` (not a project dependency).",
        "",
    ]
    (out / "note.md").write_text("\n".join(lines))
    print("\n".join(lines))
    print("wrote", out)


if __name__ == "__main__":
    main()
