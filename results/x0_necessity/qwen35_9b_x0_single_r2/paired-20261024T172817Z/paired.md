# Two-change vs single-change edit at layer 12: qwen35_9b_x0_necessity vs qwen35_9b_x0_single_r2

Descriptive, added after data (Dan, 24 Oct ~18:45, item 1); not part of X0's rule. J++ k = 25 signed; bootstrap over bridge entities, 10000 resamples, seed 0. UNVERIFIED.

| reader | items | n | entities | S_whole | Jdep | Rdep | excess |
|---|---|---|---|---|---|---|---|
| lookup | two-change, all | 200 | 40 | 0.53 [0.46, 0.59] | 0.22 [0.14, 0.29] | 0.25 [0.16, 0.33] | -0.03 [-0.08, 0.03] |
| lookup | two-change, shared | 186 | 38 | 0.53 [0.46, 0.60] | 0.21 [0.13, 0.29] | 0.24 [0.15, 0.32] | -0.03 [-0.08, 0.03] |
| lookup | single, shared | 186 | 38 | 0.54 [0.47, 0.61] | 0.09 [0.04, 0.14] | 0.11 [0.05, 0.17] | -0.02 [-0.06, 0.02] |
| lookup | single, all | 200 | 39 | 0.53 [0.46, 0.60] | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.17] | -0.02 [-0.05, 0.02] |
| recall | two-change, all | 200 | 40 | 0.98 [0.96, 0.99] | 0.53 [0.45, 0.61] | 0.04 [0.01, 0.07] | 0.50 [0.41, 0.57] |
| recall | two-change, shared | 186 | 38 | 0.98 [0.95, 0.99] | 0.54 [0.45, 0.62] | 0.04 [0.01, 0.07] | 0.50 [0.42, 0.58] |
| recall | single, shared | 186 | 38 | 0.96 [0.92, 0.98] | 0.41 [0.33, 0.48] | 0.04 [0.01, 0.07] | 0.37 [0.29, 0.44] |
| recall | single, all | 200 | 39 | 0.95 [0.92, 0.98] | 0.41 [0.34, 0.48] | 0.04 [0.02, 0.07] | 0.37 [0.29, 0.43] |

Paired differences on the shared items (single - two-change):

| reader | n | S_whole | Jdep | Rdep | excess |
|---|---|---|---|---|---|
| lookup | 186 | 0.01 [-0.03, 0.04] | -0.12 [-0.19, -0.05] | -0.13 [-0.21, -0.05] | 0.01 [-0.07, 0.08] |
| recall | 186 | -0.03 [-0.06, -0.01] | -0.13 [-0.20, -0.07] | 0.00 [-0.03, 0.03] | -0.13 [-0.19, -0.08] |
