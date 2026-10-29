# X0b (exploratory): nem35l_x52_x0b

Model nemotron-3.5-lightning (a9904d24); set x0b_v2; predicted layer 14; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 42 of 57 cells pass; 1105 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 14, pooled: HOLDS (C = 0.24 [0.17, 0.32])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 14 | PM | 1105 | 61 | 0.98 [0.97, 0.98] | 0.28 [0.22, 0.36] | 0.02 [0.01, 0.03] | 0.26 [0.20, 0.34] | mixed | 0.24 [0.17, 0.32] |
| 14 | PP | 1105 | 61 | 0.74 [0.71, 0.76] | 0.12 [0.09, 0.15] | 0.10 [0.08, 0.12] | 0.03 [0.00, 0.05] | around | 0.24 [0.17, 0.32] |

## The k-curve at layer 14 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.28 [0.22, 0.36] | 0.02 [0.01, 0.03] | 0.26 [0.20, 0.34] | mixed |
| 25 | PP | 0.12 [0.09, 0.15] | 0.10 [0.08, 0.12] | 0.03 [0.00, 0.05] | around |
| 50 | PM | 0.55 [0.49, 0.63] | 0.09 [0.06, 0.12] | 0.47 [0.40, 0.54] | through |
| 50 | PP | 0.23 [0.19, 0.28] | 0.23 [0.19, 0.26] | 0.01 [-0.02, 0.03] | around |
| 100 | PM | 0.74 [0.68, 0.79] | 0.35 [0.29, 0.41] | 0.39 [0.33, 0.45] | through |
| 100 | PP | 0.42 [0.37, 0.47] | 0.51 [0.47, 0.56] | -0.09 [-0.13, -0.06] | around |

## Probe (b) at layer 14: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| json | before | 325 | 28 | 9 | 0.72 [0.65, 0.78] | 0.23 [0.17, 0.29] | 0.11 | 0.19 [0.16, 0.22] | 0.17 [0.13, 0.22] | 0.49 [0.42, 0.55] (majority) |
| json | after | 90 | 21 | 9 | 0.18 [0.10, 0.27] | 0.21 [0.14, 0.29] | 0.11 | 0.18 [0.11, 0.26] | 0.20 [0.12, 0.28] | -0.03 [-0.10, 0.03] (majority) |
| prose | before | 751 | 60 | 9 | 0.68 [0.65, 0.71] | 0.35 [0.31, 0.39] | 0.11 | 0.33 [0.28, 0.37] | 0.36 [0.31, 0.40] | 0.32 [0.27, 0.37] (layout) |
| prose | after | 268 | 50 | 9 | 0.27 [0.22, 0.31] | 0.29 [0.24, 0.33] | 0.11 | 0.25 [0.20, 0.29] | 0.35 [0.30, 0.40] | -0.08 [-0.13, -0.03] (layout) |
| table | before | 772 | 61 | 9 | 0.74 [0.70, 0.78] | 0.17 [0.14, 0.20] | 0.11 | 0.19 [0.16, 0.22] | 0.22 [0.18, 0.26] | 0.52 [0.48, 0.56] (layout) |
| table | after | 259 | 52 | 9 | 0.24 [0.19, 0.28] | 0.21 [0.16, 0.27] | 0.11 | 0.25 [0.20, 0.30] | 0.25 [0.19, 0.30] | -0.02 [-0.08, 0.05] (structure) |

## Strata at layer 14 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | json | PP | 197 | 147 | 0.75 [0.68, 0.80] | 0.14 [0.08, 0.20] | 0.14 [0.09, 0.20] | 0.00 [-0.05, 0.05] | around |
| format | json | PM | 197 | 193 | 0.98 [0.95, 0.99] | 0.37 [0.27, 0.50] | 0.03 [0.01, 0.05] | 0.35 [0.24, 0.48] | through |
| format | prose | PP | 425 | 306 | 0.72 [0.68, 0.76] | 0.09 [0.05, 0.13] | 0.07 [0.04, 0.10] | 0.02 [-0.01, 0.05] | around |
| format | prose | PM | 425 | 413 | 0.97 [0.95, 0.98] | 0.21 [0.15, 0.29] | 0.01 [-0.01, 0.03] | 0.20 [0.14, 0.28] | mixed |
| format | table | PP | 483 | 364 | 0.75 [0.71, 0.79] | 0.14 [0.10, 0.18] | 0.10 [0.07, 0.14] | 0.04 [0.01, 0.07] | around |
| format | table | PM | 483 | 474 | 0.98 [0.96, 0.99] | 0.31 [0.23, 0.39] | 0.02 [0.00, 0.04] | 0.29 [0.21, 0.37] | through |
| level | 0 | PP | 417 | 304 | 0.73 [0.68, 0.77] | 0.08 [0.05, 0.11] | 0.08 [0.05, 0.11] | 0.00 [-0.02, 0.03] | around |
| level | 0 | PM | 417 | 402 | 0.96 [0.94, 0.98] | 0.21 [0.16, 0.27] | 0.01 [-0.00, 0.03] | 0.20 [0.14, 0.26] | mixed |
| level | 1 | PP | 347 | 251 | 0.72 [0.67, 0.77] | 0.14 [0.09, 0.19] | 0.10 [0.07, 0.14] | 0.04 [0.00, 0.07] | around |
| level | 1 | PM | 347 | 343 | 0.99 [0.97, 1.00] | 0.30 [0.21, 0.41] | 0.02 [0.00, 0.03] | 0.28 [0.19, 0.39] | mixed |
| level | 2 | PP | 341 | 262 | 0.77 [0.72, 0.81] | 0.16 [0.11, 0.22] | 0.12 [0.07, 0.18] | 0.04 [0.00, 0.07] | around |
| level | 2 | PM | 341 | 335 | 0.98 [0.96, 0.99] | 0.35 [0.26, 0.45] | 0.02 [0.00, 0.05] | 0.33 [0.25, 0.42] | through |
| domain | animals | PP | 183 | 140 | 0.77 [0.70, 0.82] | 0.11 [0.06, 0.16] | 0.11 [0.05, 0.17] | 0.00 [-0.04, 0.05] | around |
| domain | animals | PM | 183 | 176 | 0.96 [0.92, 0.98] | 0.26 [0.18, 0.34] | 0.01 [-0.02, 0.03] | 0.25 [0.18, 0.31] | mixed |
| domain | elements | PP | 188 | 137 | 0.73 [0.66, 0.79] | 0.18 [0.11, 0.25] | 0.17 [0.14, 0.21] | 0.01 [-0.04, 0.05] | around |
| domain | elements | PM | 188 | 184 | 0.98 [0.95, 0.99] | 0.43 [0.29, 0.58] | -0.01 [-0.03, 0.02] | 0.43 [0.30, 0.58] | through |
| domain | greek | PP | 113 | 81 | 0.72 [0.63, 0.79] | 0.06 [0.02, 0.11] | 0.07 [0.02, 0.13] | -0.01 [-0.04, 0.00] | around |
| domain | greek | PM | 113 | 110 | 0.97 [0.92, 0.99] | 0.30 [0.24, 0.37] | 0.04 [0.01, 0.06] | 0.26 [0.19, 0.36] | through |
| domain | instruments | PP | 234 | 172 | 0.73 [0.68, 0.79] | 0.12 [0.02, 0.15] | 0.07 [0.02, 0.11] | 0.05 [0.00, 0.07] | around |
| domain | instruments | PM | 234 | 231 | 0.99 [0.96, 1.00] | 0.13 [0.09, 0.20] | 0.02 [0.00, 0.05] | 0.11 [0.08, 0.17] | mixed |
| domain | planets | PP | 117 | 79 | 0.68 [0.59, 0.75] | 0.09 [0.06, 0.13] | 0.10 [0.08, 0.13] | -0.01 [-0.05, 0.03] | around |
| domain | planets | PM | 117 | 114 | 0.97 [0.93, 0.99] | 0.28 [0.16, 0.44] | 0.04 [0.02, 0.07] | 0.24 [0.11, 0.40] | mixed |
| domain | shapes | PP | 108 | 85 | 0.79 [0.70, 0.85] | 0.22 [0.17, 0.27] | 0.11 [0.05, 0.16] | 0.12 [0.11, 0.12] | mixed |
| domain | shapes | PM | 108 | 107 | 0.99 [0.95, 1.00] | 0.45 [0.31, 0.58] | 0.01 [0.00, 0.02] | 0.44 [0.31, 0.57] | through |
| domain | vehicles | PP | 162 | 123 | 0.76 [0.69, 0.82] | 0.09 [0.03, 0.12] | 0.06 [0.00, 0.11] | 0.03 [0.00, 0.09] | around |
| domain | vehicles | PM | 162 | 158 | 0.98 [0.94, 0.99] | 0.24 [0.05, 0.39] | 0.03 [0.00, 0.06] | 0.21 [0.05, 0.33] | mixed |
| order | after | PP | 318 | 79 | 0.25 [0.20, 0.30] | 0.42 [0.29, 0.54] | 0.32 [0.21, 0.43] | 0.10 [0.00, 0.20] | can't tell |
| order | after | PM | 318 | 306 | 0.96 [0.94, 0.98] | 0.49 [0.40, 0.58] | 0.04 [0.02, 0.05] | 0.45 [0.37, 0.55] | through |
| order | before | PP | 787 | 738 | 0.94 [0.92, 0.95] | 0.09 [0.06, 0.12] | 0.07 [0.05, 0.10] | 0.02 [-0.01, 0.04] | around |
| order | before | PM | 787 | 774 | 0.98 [0.97, 0.99] | 0.20 [0.14, 0.28] | 0.01 [0.00, 0.02] | 0.19 [0.13, 0.26] | mixed |
| numbers | digits | PP | 553 | 420 | 0.76 [0.72, 0.79] | 0.11 [0.07, 0.15] | 0.09 [0.06, 0.12] | 0.02 [-0.01, 0.05] | around |
| numbers | digits | PM | 553 | 542 | 0.98 [0.96, 0.99] | 0.26 [0.20, 0.34] | 0.01 [0.00, 0.03] | 0.25 [0.18, 0.32] | mixed |
| numbers | words | PP | 552 | 397 | 0.72 [0.68, 0.76] | 0.14 [0.11, 0.17] | 0.11 [0.08, 0.14] | 0.03 [0.00, 0.06] | around |
| numbers | words | PM | 552 | 538 | 0.97 [0.96, 0.98] | 0.30 [0.23, 0.38] | 0.02 [0.00, 0.04] | 0.28 [0.21, 0.36] | through |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/json/0 | 12 | 1.00 / 0.92 | True | 9 | 9 |
| animals/json/1 | 19 | 0.95 / 0.68 | False | 11 | 0 |
| animals/json/2 | 21 | 0.95 / 0.81 | True | 12 | 12 |
| animals/prose/0 | 36 | 0.94 / 0.94 | True | 28 | 28 |
| animals/prose/1 | 55 | 1.00 / 0.84 | True | 37 | 37 |
| animals/prose/2 | 52 | 0.98 / 0.90 | True | 42 | 40 |
| animals/table/0 | 46 | 1.00 / 0.83 | True | 26 | 26 |
| animals/table/1 | 51 | 0.94 / 0.75 | False | 24 | 0 |
| animals/table/2 | 50 | 0.94 / 0.84 | True | 31 | 31 |
| elements/json/0 | 17 | 1.00 / 1.00 | True | 15 | 15 |
| elements/json/1 | 37 | 0.92 / 0.97 | True | 27 | 27 |
| elements/json/2 | 35 | 0.91 / 1.00 | True | 26 | 26 |
| elements/prose/0 | 60 | 0.97 / 0.72 | False | 25 | 0 |
| elements/prose/1 | 62 | 0.97 / 0.68 | False | 35 | 0 |
| elements/prose/2 | 57 | 1.00 / 0.63 | False | 30 | 0 |
| elements/table/0 | 63 | 0.98 / 0.81 | True | 41 | 40 |
| elements/table/1 | 64 | 0.94 / 0.98 | True | 44 | 40 |
| elements/table/2 | 63 | 0.89 / 0.98 | True | 49 | 40 |
| greek/json/0 | 70 | 0.91 / 0.81 | True | 40 | 40 |
| greek/json/1 | 70 | 0.90 / 0.80 | True | 33 | 33 |
| greek/json/2 | 70 | 0.91 / 0.79 | False | 33 | 0 |
| greek/prose/0 | 63 | 0.89 / 0.94 | True | 46 | 40 |
| greek/prose/1 | 58 | 0.97 / 0.71 | False | 24 | 0 |
| greek/prose/2 | 64 | 0.97 / 0.61 | False | 22 | 0 |
| greek/table/0 | 63 | 0.97 / 0.48 | False | 14 | 0 |
| greek/table/1 | 61 | 0.97 / 0.49 | False | 18 | 0 |
| greek/table/2 | 57 | 0.98 / 0.65 | False | 21 | 0 |
| instruments/prose/0 | 52 | 0.98 / 0.81 | True | 34 | 34 |
| instruments/prose/1 | 62 | 0.98 / 0.92 | True | 54 | 40 |
| instruments/prose/2 | 66 | 1.00 / 0.97 | True | 62 | 40 |
| instruments/table/0 | 49 | 0.96 / 0.96 | True | 44 | 40 |
| instruments/table/1 | 66 | 0.97 / 0.97 | True | 57 | 40 |
| instruments/table/2 | 65 | 0.95 / 0.98 | True | 54 | 40 |
| planets/json/0 | 5 | 1.00 / 1.00 | True | 4 | 4 |
| planets/json/1 | 8 | 0.88 / 1.00 | True | 5 | 5 |
| planets/json/2 | 14 | 0.79 / 0.93 | False | 6 | 0 |
| planets/prose/0 | 59 | 1.00 / 0.88 | True | 43 | 40 |
| planets/prose/1 | 62 | 0.97 / 0.76 | False | 41 | 0 |
| planets/prose/2 | 64 | 0.98 / 0.72 | False | 34 | 0 |
| planets/table/0 | 66 | 0.97 / 0.82 | True | 39 | 39 |
| planets/table/1 | 62 | 0.94 / 0.84 | True | 29 | 29 |
| planets/table/2 | 56 | 0.91 / 0.79 | False | 27 | 0 |
| shapes/json/0 | 4 | 1.00 / 1.00 | True | 4 | 4 |
| shapes/json/1 | 11 | 0.91 / 1.00 | True | 7 | 7 |
| shapes/json/2 | 22 | 1.00 / 0.86 | True | 15 | 15 |
| shapes/prose/0 | 10 | 1.00 / 0.90 | True | 9 | 9 |
| shapes/prose/1 | 14 | 1.00 / 1.00 | True | 14 | 14 |
| shapes/prose/2 | 25 | 0.96 / 1.00 | True | 23 | 23 |
| shapes/table/0 | 11 | 1.00 / 0.91 | True | 10 | 10 |
| shapes/table/1 | 15 | 1.00 / 0.93 | True | 12 | 12 |
| shapes/table/2 | 22 | 1.00 / 0.95 | True | 14 | 14 |
| vehicles/prose/0 | 25 | 1.00 / 0.92 | True | 20 | 20 |
| vehicles/prose/1 | 31 | 1.00 / 0.94 | True | 27 | 27 |
| vehicles/prose/2 | 42 | 0.93 / 0.98 | True | 33 | 33 |
| vehicles/table/0 | 21 | 1.00 / 0.90 | True | 19 | 19 |
| vehicles/table/1 | 46 | 0.96 / 0.91 | True | 36 | 36 |
| vehicles/table/2 | 34 | 1.00 / 0.88 | True | 27 | 27 |
