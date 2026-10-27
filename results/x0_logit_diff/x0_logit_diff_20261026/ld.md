# Batch 39: the split on the logit difference (x0_logit_diff_20261026)

The main test (two people swap picks), chat, each model's layer fixed in advance, J++ (25, signed) against its random part. Fraction of the whole change's ld shift lost; extra loss = without J++ minus without random; gap = recall minus lookup. Cluster bootstrap over bridge entities (10000 resamples, seed 0). UNVERIFIED.

| model | layer | n | lookup extra loss (ld) | recall extra loss (ld) | gap (ld) | median whole shift, lookup / recall |
|---|---|---|---|---|---|---|
| 9B | 12 | 200 | -0.05 [-0.07, -0.03] | 0.43 [0.37, 0.48] | 0.48 [0.42, 0.53] | 3.38 / 7.12 |
| 27B | 32 | 200 | 0.13 [0.11, 0.16] | 0.60 [0.54, 0.65] | 0.47 [0.42, 0.51] | 5.41 / 9.56 |
| 122B | 33 | 200 | -0.02 [-0.05, -0.00] | 0.31 [0.26, 0.34] | 0.33 [0.29, 0.38] | 3.25 / 8.50 |
| Muse | 26 | 200 | -0.03 [-0.05, -0.02] | 0.58 [0.49, 0.65] | 0.61 [0.52, 0.68] | 1.50 / 6.81 |

Q39.1: gap >= 0.2 on 4 of 4 models: (a) all four.

Q39.2 (the 27B; cut points 4.88, 10.62 on the pooled whole shift): 1 terciles count (each reader >= 30 switched): can't tell.

| tercile | counts | lookup n / switched / extra loss | recall n / switched / extra loss | gap (switches) |
|---|---|---|---|---|
| 1 | no | 98 / 2 / 0.00 [0.00, 0.00] | 35 / 2 / 2.00 [1.00, 5.00] | 2.00 |
| 2 | no | 41 / 24 / 0.21 [0.07, 0.38] | 91 / 75 / 0.68 [0.56, 0.78] | 0.47 |
| 3 | yes | 61 / 60 / 0.12 [0.05, 0.20] | 74 / 73 / 0.77 [0.67, 0.86] | 0.65 |
