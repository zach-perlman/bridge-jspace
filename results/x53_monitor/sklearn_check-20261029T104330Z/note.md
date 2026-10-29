# 53.2: one probe cell against sklearn (critic_1125)

Run qwen35_9b_x53_monitor (main test), same folds as scripts/x53_monitor.py (5 seeds x 5-fold), C = 1.0, features standardised on the training rows. Ours: multinomial logistic, sklearn's objective, scipy L-BFGS in the training rows' span (gtol 1e-3). sklearn: LogisticRegression (lbfgs, l2, max_iter 20000, tol 1e-8) on the full standardised features (no span reduction). UNVERIFIED.

| cell | rows | held-out acc, ours | held-out acc, sklearn | ours - sklearn | predictions agree |
|---|---|---|---|---|---|
| the check: T, target (c), L20, full | 400 | 0.8985 | 0.8995 | -0.0010 | 0.9990 |
| beside: B, target (b), L16, jpp25 | 400 | 0.6125 | 0.6135 | -0.0010 | 0.9990 |

sklearn 1.9.1, run once with `uv run --with scikit-learn` (not a project dependency).
