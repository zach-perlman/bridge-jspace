# X0b (exploratory): qwen35_122b_x0b_v2

Model qwen3.5-122b-a10b (a099dee7); set x0b_v2; predicted layer 33; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 26 of 28 cells pass; 852 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 33, pooled: MIXED (C = 0.15 [0.12, 0.18])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 33 | PM | 852 | 60 | 0.94 [0.92, 0.95] | 0.19 [0.16, 0.22] | 0.06 [0.03, 0.08] | 0.13 [0.11, 0.16] | mixed | 0.15 [0.12, 0.18] |
| 33 | PP | 852 | 60 | 0.74 [0.71, 0.77] | 0.03 [0.01, 0.04] | 0.04 [0.03, 0.06] | -0.02 [-0.03, -0.00] | around | 0.15 [0.12, 0.18] |

## The k-curve at layer 33 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.19 [0.16, 0.22] | 0.06 [0.03, 0.08] | 0.13 [0.11, 0.16] | mixed |
| 25 | PP | 0.03 [0.01, 0.04] | 0.04 [0.03, 0.06] | -0.02 [-0.03, -0.00] | around |

## Probe (b) at layer 33: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| prose | before | 451 | 56 | 6 | 0.78 [0.75, 0.82] | 0.42 [0.37, 0.48] | 0.17 | 0.38 [0.34, 0.43] | 0.40 [0.36, 0.45] | 0.36 [0.31, 0.42] (majority) |
| prose | after | 162 | 45 | 6 | 0.33 [0.27, 0.40] | 0.36 [0.30, 0.44] | 0.17 | 0.30 [0.22, 0.39] | 0.36 [0.29, 0.44] | -0.03 [-0.08, 0.00] (majority) |
| table | before | 469 | 58 | 6 | 0.88 [0.85, 0.91] | 0.27 [0.23, 0.31] | 0.17 | 0.19 [0.16, 0.22] | 0.25 [0.21, 0.29] | 0.61 [0.57, 0.65] (majority) |
| table | after | 176 | 45 | 6 | 0.27 [0.21, 0.33] | 0.24 [0.17, 0.31] | 0.17 | 0.23 [0.18, 0.28] | 0.28 [0.23, 0.34] | -0.01 [-0.10, 0.07] (layout) |

## Strata at layer 33 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | prose | PP | 426 | 307 | 0.72 [0.68, 0.76] | 0.03 [0.01, 0.05] | 0.04 [0.02, 0.06] | -0.01 [-0.03, 0.00] | around |
| format | prose | PM | 426 | 401 | 0.94 [0.91, 0.96] | 0.18 [0.13, 0.24] | 0.04 [0.01, 0.08] | 0.14 [0.10, 0.18] | mixed |
| format | table | PP | 426 | 322 | 0.76 [0.71, 0.79] | 0.02 [0.00, 0.04] | 0.04 [0.02, 0.06] | -0.02 [-0.03, -0.01] | around |
| format | table | PM | 426 | 397 | 0.93 [0.90, 0.95] | 0.20 [0.16, 0.24] | 0.07 [0.03, 0.11] | 0.13 [0.09, 0.17] | mixed |
| level | 0 | PP | 366 | 274 | 0.75 [0.70, 0.79] | 0.00 [-0.01, 0.01] | 0.02 [0.00, 0.03] | -0.02 [-0.04, -0.00] | around |
| level | 0 | PM | 366 | 339 | 0.93 [0.89, 0.95] | 0.17 [0.13, 0.21] | 0.04 [0.02, 0.07] | 0.13 [0.09, 0.17] | mixed |
| level | 1 | PP | 486 | 355 | 0.73 [0.69, 0.77] | 0.05 [0.02, 0.07] | 0.06 [0.03, 0.08] | -0.01 [-0.03, 0.00] | around |
| level | 1 | PM | 486 | 459 | 0.94 [0.92, 0.96] | 0.20 [0.17, 0.25] | 0.07 [0.04, 0.09] | 0.14 [0.11, 0.17] | mixed |
| domain | animals | PP | 114 | 86 | 0.75 [0.67, 0.82] | 0.03 [0.00, 0.08] | 0.05 [0.01, 0.09] | -0.01 [-0.03, 0.00] | around |
| domain | animals | PM | 114 | 93 | 0.82 [0.73, 0.88] | 0.26 [0.14, 0.38] | 0.13 [0.04, 0.23] | 0.13 [0.06, 0.20] | mixed |
| domain | elements | PP | 152 | 108 | 0.71 [0.63, 0.78] | 0.06 [0.03, 0.09] | 0.05 [0.02, 0.08] | 0.01 [0.00, 0.03] | around |
| domain | elements | PM | 152 | 147 | 0.97 [0.93, 0.99] | 0.22 [0.17, 0.29] | 0.01 [0.00, 0.02] | 0.21 [0.16, 0.28] | mixed |
| domain | greek | PP | 160 | 113 | 0.71 [0.63, 0.77] | 0.00 [0.00, 0.00] | 0.03 [0.00, 0.06] | -0.03 [-0.06, 0.00] | around |
| domain | greek | PM | 160 | 152 | 0.95 [0.90, 0.97] | 0.16 [0.12, 0.22] | 0.04 [-0.01, 0.09] | 0.12 [0.08, 0.18] | mixed |
| domain | instruments | PP | 149 | 111 | 0.74 [0.67, 0.81] | 0.06 [0.00, 0.08] | 0.05 [0.00, 0.06] | 0.01 [0.00, 0.01] | around |
| domain | instruments | PM | 149 | 144 | 0.97 [0.92, 0.99] | 0.15 [0.14, 0.22] | 0.07 [0.00, 0.13] | 0.08 [0.07, 0.17] | around |
| domain | planets | PP | 112 | 81 | 0.72 [0.63, 0.80] | -0.01 [-0.05, 0.00] | 0.04 [-0.03, 0.08] | -0.05 [-0.09, -0.01] | around |
| domain | planets | PM | 112 | 102 | 0.91 [0.84, 0.95] | 0.21 [0.11, 0.29] | 0.08 [0.00, 0.15] | 0.13 [0.07, 0.19] | mixed |
| domain | shapes | PP | 49 | 37 | 0.76 [0.62, 0.85] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| domain | shapes | PM | 49 | 49 | 1.00 [0.93, 1.00] | 0.16 [0.15, 0.17] | 0.00 [0.00, 0.00] | 0.16 [0.15, 0.17] | mixed |
| domain | vehicles | PP | 116 | 93 | 0.80 [0.72, 0.86] | 0.01 [0.00, 0.04] | 0.05 [0.00, 0.12] | -0.04 [-0.08, 0.00] | around |
| domain | vehicles | PM | 116 | 111 | 0.96 [0.90, 0.98] | 0.17 [0.14, 0.20] | 0.07 [0.04, 0.10] | 0.10 [0.10, 0.10] | around |
| order | after | PP | 236 | 42 | 0.18 [0.13, 0.23] | 0.21 [0.09, 0.32] | 0.36 [0.21, 0.48] | -0.14 [-0.25, -0.05] | can't tell |
| order | after | PM | 236 | 213 | 0.90 [0.86, 0.93] | 0.51 [0.43, 0.61] | 0.11 [0.06, 0.17] | 0.39 [0.31, 0.49] | through |
| order | before | PP | 616 | 587 | 0.95 [0.93, 0.97] | 0.01 [-0.00, 0.02] | 0.02 [0.01, 0.03] | -0.01 [-0.02, 0.00] | around |
| order | before | PM | 616 | 585 | 0.95 [0.93, 0.96] | 0.07 [0.05, 0.10] | 0.04 [0.02, 0.06] | 0.04 [0.02, 0.06] | around |
| numbers | digits | PP | 463 | 336 | 0.73 [0.68, 0.76] | 0.02 [-0.01, 0.04] | 0.03 [0.01, 0.06] | -0.01 [-0.03, -0.00] | around |
| numbers | digits | PM | 463 | 429 | 0.93 [0.90, 0.95] | 0.19 [0.15, 0.23] | 0.07 [0.04, 0.10] | 0.13 [0.09, 0.17] | mixed |
| numbers | words | PP | 389 | 293 | 0.75 [0.71, 0.79] | 0.03 [0.02, 0.05] | 0.05 [0.03, 0.08] | -0.02 [-0.04, 0.01] | around |
| numbers | words | PM | 389 | 369 | 0.95 [0.92, 0.97] | 0.19 [0.14, 0.24] | 0.05 [0.02, 0.07] | 0.14 [0.10, 0.18] | mixed |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/prose/0 | 42 | 1.00 / 0.79 | False | 26 | 0 |
| animals/prose/1 | 60 | 0.98 / 0.80 | True | 44 | 40 |
| animals/table/0 | 51 | 0.96 / 0.96 | True | 38 | 38 |
| animals/table/1 | 57 | 0.98 / 0.84 | True | 36 | 36 |
| elements/prose/0 | 41 | 0.98 / 0.88 | True | 35 | 35 |
| elements/prose/1 | 47 | 1.00 / 0.98 | True | 45 | 40 |
| elements/table/0 | 41 | 1.00 / 0.90 | True | 37 | 37 |
| elements/table/1 | 49 | 0.98 / 0.94 | True | 41 | 40 |
| greek/prose/0 | 64 | 0.98 / 0.92 | True | 47 | 40 |
| greek/prose/1 | 63 | 1.00 / 0.87 | True | 40 | 40 |
| greek/table/0 | 63 | 0.97 / 0.94 | True | 50 | 40 |
| greek/table/1 | 65 | 0.97 / 0.88 | True | 49 | 40 |
| instruments/prose/0 | 42 | 0.98 / 0.88 | True | 32 | 32 |
| instruments/prose/1 | 53 | 1.00 / 0.81 | True | 42 | 40 |
| instruments/table/0 | 39 | 1.00 / 1.00 | True | 37 | 37 |
| instruments/table/1 | 59 | 0.98 / 1.00 | True | 56 | 40 |
| planets/prose/0 | 59 | 1.00 / 0.93 | True | 53 | 40 |
| planets/prose/1 | 62 | 1.00 / 0.95 | True | 58 | 40 |
| planets/table/0 | 66 | 0.95 / 0.71 | False | 38 | 0 |
| planets/table/1 | 62 | 0.97 / 0.87 | True | 32 | 32 |
| shapes/prose/0 | 10 | 1.00 / 1.00 | True | 10 | 10 |
| shapes/prose/1 | 14 | 1.00 / 1.00 | True | 14 | 14 |
| shapes/table/0 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/table/1 | 15 | 1.00 / 1.00 | True | 14 | 14 |
| vehicles/prose/0 | 25 | 1.00 / 1.00 | True | 25 | 25 |
| vehicles/prose/1 | 31 | 1.00 / 1.00 | True | 30 | 30 |
| vehicles/table/0 | 21 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/table/1 | 46 | 1.00 / 1.00 | True | 46 | 40 |
