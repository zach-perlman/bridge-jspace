# Two-change vs single-change edit at layer 32: x0_necessity_27b_chat vs x0_single_27b_r2

Descriptive, added after data (Dan, 24 Oct ~18:45, item 1); not part of X0's rule. J++ k = 25 signed; bootstrap over bridge entities, 10000 resamples, seed 0. UNVERIFIED.

| reader | items | n | entities | S_whole | Jdep | Rdep | excess |
|---|---|---|---|---|---|---|---|
| lookup | two-change, all | 200 | 44 | 0.43 [0.36, 0.50] | 0.17 [0.10, 0.25] | 0.03 [0.00, 0.08] | 0.14 [0.08, 0.20] |
| lookup | two-change, shared | 195 | 44 | 0.44 [0.37, 0.51] | 0.16 [0.09, 0.24] | 0.04 [0.00, 0.08] | 0.13 [0.07, 0.19] |
| lookup | single, shared | 195 | 44 | 0.48 [0.41, 0.55] | 0.05 [0.01, 0.09] | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] |
| lookup | single, all | 200 | 44 | 0.47 [0.41, 0.54] | 0.05 [0.01, 0.09] | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] |
| recall | two-change, all | 200 | 44 | 0.75 [0.69, 0.80] | 0.77 [0.67, 0.84] | 0.03 [-0.02, 0.06] | 0.74 [0.66, 0.80] |
| recall | two-change, shared | 195 | 44 | 0.75 [0.69, 0.81] | 0.77 [0.67, 0.85] | 0.02 [-0.02, 0.06] | 0.75 [0.67, 0.81] |
| recall | single, shared | 195 | 44 | 0.73 [0.67, 0.79] | 0.60 [0.51, 0.68] | 0.00 [-0.03, 0.03] | 0.60 [0.50, 0.69] |
| recall | single, all | 200 | 44 | 0.73 [0.66, 0.79] | 0.61 [0.52, 0.69] | 0.00 [-0.03, 0.03] | 0.61 [0.51, 0.69] |

Paired differences on the shared items (single - two-change):

| reader | n | S_whole | Jdep | Rdep | excess |
|---|---|---|---|---|---|
| lookup | 195 | 0.04 [0.01, 0.07] | -0.11 [-0.20, -0.03] | -0.04 [-0.08, 0.00] | -0.08 [-0.16, 0.00] |
| recall | 195 | -0.02 [-0.05, 0.01] | -0.17 [-0.23, -0.10] | -0.02 [-0.06, 0.02] | -0.15 [-0.22, -0.08] |
