# Probe (b) by locker-sentence index: qwen35_9b_x0_probe (layer 12, locker-before)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Out-of-fold predictions of x0_probe's (b) probe (5 folds by bridge entity); accuracy per true index with a cluster bootstrap over entities (10000 resamples, seed 0); the rest of each row is the share of that index's items predicted as each index. UNVERIFIED.

## X0 items (n = 100)

| true index | n | accuracy | predicted 0 | predicted 1 | predicted 2 | predicted 3 | predicted 4 |
|---|---|---|---|---|---|---|---|
| 0 | 31 | 1.00 [1.00, 1.00] | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 22 | 0.82 [0.67, 0.95] | 0.00 | 0.82 | 0.18 | 0.00 | 0.00 |
| 2 | 28 | 0.89 [0.72, 1.00] | 0.00 | 0.04 | 0.89 | 0.04 | 0.04 |
| 3 | 11 | 0.27 [0.00, 0.60] | 0.00 | 0.09 | 0.45 | 0.27 | 0.18 |
| 4 | 8 | 0.62 [0.25, 0.88] | 0.00 | 0.00 | 0.00 | 0.38 | 0.62 |

## every scene (n = 301)

| true index | n | accuracy | predicted 0 | predicted 1 | predicted 2 | predicted 3 | predicted 4 |
|---|---|---|---|---|---|---|---|
| 0 | 92 | 1.00 [1.00, 1.00] | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 90 | 1.00 [1.00, 1.00] | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 2 | 65 | 0.78 [0.67, 0.89] | 0.00 | 0.08 | 0.78 | 0.14 | 0.00 |
| 3 | 29 | 0.45 [0.23, 0.66] | 0.00 | 0.03 | 0.41 | 0.45 | 0.10 |
| 4 | 25 | 0.92 [0.82, 1.00] | 0.00 | 0.00 | 0.00 | 0.08 | 0.92 |

## Probe (c)'s split

Probe (c) (bridge identity) uses 5 folds over items; each item is one scene, so the split is by scene. Every entity is spread over the folds (an entity-held-out fold has no seen class): entities by the number of folds they span: {1: 2, 2: 1, 3: 6, 4: 2, 5: 35}.

