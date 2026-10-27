# X0b (exploratory): muse30b_x0b_v2_ptr

Model muse-glimmer-30b (cec94fcf); set x0b_v2; predicted layer 26; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 44 of 57 cells pass; 1389 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 26, pooled: HOLDS (C = 0.50 [0.39, 0.62])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 26 | PM | 1389 | 60 | 0.40 [0.37, 0.42] | 0.54 [0.46, 0.62] | -0.03 [-0.08, 0.03] | 0.56 [0.48, 0.67] | through | 0.50 [0.39, 0.62] |
| 26 | PP | 1389 | 60 | 0.36 [0.34, 0.39] | -0.05 [-0.08, -0.01] | -0.11 [-0.15, -0.07] | 0.06 [0.03, 0.10] | around | 0.50 [0.39, 0.62] |

## The k-curve at layer 26 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.54 [0.46, 0.62] | -0.03 [-0.08, 0.03] | 0.56 [0.48, 0.67] | through |
| 25 | PP | -0.05 [-0.08, -0.01] | -0.11 [-0.15, -0.07] | 0.06 [0.03, 0.10] | around |

## Probe (b) at layer 26: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| json | before | 301 | 32 | 9 | 0.72 [0.66, 0.79] | 0.19 [0.14, 0.25] | 0.11 | 0.18 [0.13, 0.23] | 0.16 [0.12, 0.20] | 0.53 [0.48, 0.59] (majority) |
| json | after | 87 | 25 | 9 | 0.20 [0.11, 0.28] | 0.20 [0.12, 0.27] | 0.11 | 0.15 [0.07, 0.23] | 0.09 [0.04, 0.15] | 0.00 [-0.08, 0.08] (majority) |
| prose | before | 783 | 63 | 9 | 0.71 [0.68, 0.74] | 0.35 [0.31, 0.39] | 0.11 | 0.31 [0.27, 0.34] | 0.38 [0.33, 0.42] | 0.34 [0.30, 0.37] (layout) |
| prose | after | 282 | 53 | 9 | 0.34 [0.28, 0.39] | 0.29 [0.24, 0.34] | 0.11 | 0.27 [0.23, 0.32] | 0.35 [0.30, 0.41] | -0.01 [-0.08, 0.05] (layout) |
| table | before | 797 | 64 | 9 | 0.82 [0.79, 0.85] | 0.19 [0.16, 0.22] | 0.11 | 0.18 [0.16, 0.20] | 0.20 [0.17, 0.24] | 0.62 [0.58, 0.66] (layout) |
| table | after | 285 | 54 | 9 | 0.22 [0.17, 0.27] | 0.19 [0.14, 0.24] | 0.11 | 0.22 [0.16, 0.28] | 0.25 [0.20, 0.31] | -0.03 [-0.11, 0.04] (layout) |

## Strata at layer 26 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | json | PP | 220 | 56 | 0.25 [0.20, 0.32] | -0.04 [-0.14, 0.05] | -0.23 [-0.44, -0.11] | 0.20 [0.08, 0.38] | can't tell |
| format | json | PM | 220 | 32 | 0.15 [0.10, 0.20] | 0.59 [0.44, 0.77] | -0.12 [-0.43, 0.16] | 0.72 [0.52, 0.97] | can't tell |
| format | prose | PP | 540 | 234 | 0.43 [0.39, 0.48] | -0.05 [-0.09, -0.00] | -0.09 [-0.15, -0.03] | 0.04 [-0.00, 0.09] | around |
| format | prose | PM | 540 | 307 | 0.57 [0.53, 0.61] | 0.51 [0.42, 0.59] | -0.04 [-0.08, 0.01] | 0.54 [0.46, 0.64] | through |
| format | table | PP | 629 | 212 | 0.34 [0.30, 0.37] | -0.04 [-0.09, 0.01] | -0.10 [-0.16, -0.04] | 0.06 [0.02, 0.09] | around |
| format | table | PM | 629 | 212 | 0.34 [0.30, 0.37] | 0.57 [0.46, 0.70] | -0.00 [-0.08, 0.08] | 0.57 [0.42, 0.74] | through |
| level | 0 | PP | 350 | 200 | 0.57 [0.52, 0.62] | 0.01 [-0.03, 0.05] | -0.05 [-0.09, -0.01] | 0.06 [0.02, 0.09] | around |
| level | 0 | PM | 350 | 156 | 0.45 [0.39, 0.50] | 0.47 [0.36, 0.60] | -0.02 [-0.12, 0.06] | 0.49 [0.35, 0.67] | through |
| level | 1 | PP | 530 | 151 | 0.28 [0.25, 0.32] | -0.07 [-0.13, -0.01] | -0.13 [-0.23, -0.05] | 0.06 [0.00, 0.13] | can't tell |
| level | 1 | PM | 530 | 202 | 0.38 [0.34, 0.42] | 0.54 [0.45, 0.64] | 0.00 [-0.05, 0.05] | 0.54 [0.45, 0.64] | through |
| level | 2 | PP | 509 | 151 | 0.30 [0.26, 0.34] | -0.10 [-0.16, -0.04] | -0.17 [-0.27, -0.10] | 0.07 [0.01, 0.17] | can't tell |
| level | 2 | PM | 509 | 193 | 0.38 [0.34, 0.42] | 0.58 [0.49, 0.66] | -0.07 [-0.16, 0.00] | 0.64 [0.54, 0.77] | through |
| domain | animals | PP | 283 | 115 | 0.41 [0.35, 0.46] | 0.00 [-0.04, 0.03] | -0.10 [-0.17, -0.03] | 0.10 [0.03, 0.17] | around |
| domain | animals | PM | 283 | 101 | 0.36 [0.30, 0.41] | 0.52 [0.38, 0.64] | 0.02 [-0.06, 0.10] | 0.50 [0.39, 0.62] | through |
| domain | elements | PP | 301 | 113 | 0.38 [0.32, 0.43] | 0.00 [-0.06, 0.07] | -0.04 [-0.14, 0.02] | 0.04 [-0.03, 0.16] | around |
| domain | elements | PM | 301 | 133 | 0.44 [0.39, 0.50] | 0.69 [0.55, 0.81] | -0.08 [-0.16, -0.02] | 0.77 [0.63, 0.90] | through |
| domain | greek | PP | 115 | 27 ⚠ | 0.23 [0.17, 0.32] | -0.15 [-0.43, -0.02] | -0.30 [-0.73, -0.08] | 0.15 [0.03, 0.33] | can't tell |
| domain | greek | PM | 115 | 19 ⚠ | 0.17 [0.11, 0.24] | 0.63 [0.47, 0.83] | 0.11 [0.00, 0.28] | 0.53 [0.33, 0.73] | can't tell |
| domain | instruments | PP | 234 | 76 | 0.32 [0.27, 0.39] | -0.04 [-0.08, 0.09] | -0.17 [-0.21, 0.00] | 0.13 [0.09, 0.18] | mixed |
| domain | instruments | PM | 234 | 103 | 0.44 [0.38, 0.50] | 0.39 [0.10, 0.49] | 0.09 [-0.18, 0.15] | 0.30 [0.10, 0.45] | mixed |
| domain | planets | PP | 20 | 9 ⚠ | 0.45 [0.26, 0.66] | -0.11 [-0.20, 0.00] | -0.11 [-0.20, 0.00] | 0.00 [0.00, 0.00] | can't tell |
| domain | planets | PM | 20 | 5 ⚠ | 0.25 [0.11, 0.47] | 0.40 [0.25, 1.00] | -0.40 [-0.50, 0.00] | 0.80 [0.75, 1.00] | can't tell |
| domain | shapes | PP | 251 | 84 | 0.33 [0.28, 0.40] | -0.12 [-0.18, -0.05] | -0.15 [-0.25, -0.05] | 0.04 [0.00, 0.08] | around |
| domain | shapes | PM | 251 | 122 | 0.49 [0.42, 0.55] | 0.45 [0.29, 0.64] | -0.11 [-0.18, -0.07] | 0.57 [0.44, 0.78] | through |
| domain | vehicles | PP | 185 | 78 | 0.42 [0.35, 0.49] | -0.06 [-0.17, 0.04] | -0.05 [-0.13, 0.00] | -0.01 [-0.05, 0.04] | around |
| domain | vehicles | PM | 185 | 68 | 0.37 [0.30, 0.44] | 0.60 [0.29, 0.80] | -0.04 [-0.10, 0.00] | 0.65 [0.29, 0.90] | through |
| order | after | PP | 354 | 21 ⚠ | 0.06 [0.04, 0.09] | -0.10 [-0.29, 0.00] | 0.05 [-0.12, 0.21] | -0.14 [-0.33, 0.00] | can't tell |
| order | after | PM | 354 | 212 | 0.60 [0.55, 0.65] | 0.75 [0.67, 0.84] | 0.01 [-0.07, 0.10] | 0.74 [0.62, 0.88] | through |
| order | before | PP | 1035 | 481 | 0.46 [0.43, 0.50] | -0.04 [-0.08, -0.01] | -0.12 [-0.16, -0.07] | 0.07 [0.04, 0.11] | around |
| order | before | PM | 1035 | 339 | 0.33 [0.30, 0.36] | 0.40 [0.30, 0.51] | -0.06 [-0.10, -0.01] | 0.45 [0.36, 0.57] | through |
| numbers | digits | PP | 705 | 263 | 0.37 [0.34, 0.41] | -0.02 [-0.06, 0.02] | -0.11 [-0.17, -0.05] | 0.08 [0.04, 0.13] | around |
| numbers | digits | PM | 705 | 275 | 0.39 [0.35, 0.43] | 0.59 [0.50, 0.67] | -0.03 [-0.08, 0.01] | 0.62 [0.53, 0.72] | through |
| numbers | words | PP | 684 | 239 | 0.35 [0.31, 0.39] | -0.07 [-0.11, -0.03] | -0.11 [-0.18, -0.06] | 0.04 [-0.01, 0.11] | around |
| numbers | words | PM | 684 | 276 | 0.40 [0.37, 0.44] | 0.48 [0.41, 0.57] | -0.03 [-0.11, 0.06] | 0.51 [0.40, 0.64] | through |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/json/0 | 18 | 1.00 / 0.83 | True | 14 | 14 |
| animals/json/1 | 34 | 0.97 / 0.82 | True | 26 | 26 |
| animals/json/2 | 28 | 1.00 / 0.93 | True | 22 | 22 |
| animals/prose/0 | 38 | 0.97 / 0.87 | True | 28 | 28 |
| animals/prose/1 | 58 | 0.98 / 0.90 | True | 48 | 40 |
| animals/prose/2 | 54 | 0.98 / 0.94 | True | 49 | 40 |
| animals/table/0 | 47 | 1.00 / 0.83 | True | 33 | 33 |
| animals/table/1 | 53 | 0.98 / 0.89 | True | 40 | 40 |
| animals/table/2 | 54 | 1.00 / 0.96 | True | 45 | 40 |
| elements/json/0 | 9 | 1.00 / 1.00 | True | 9 | 9 |
| elements/json/1 | 26 | 1.00 / 1.00 | True | 26 | 26 |
| elements/json/2 | 26 | 1.00 / 1.00 | True | 26 | 26 |
| elements/prose/0 | 60 | 0.97 / 0.95 | True | 52 | 40 |
| elements/prose/1 | 62 | 0.98 / 1.00 | True | 61 | 40 |
| elements/prose/2 | 57 | 0.96 / 0.91 | True | 49 | 40 |
| elements/table/0 | 63 | 1.00 / 1.00 | True | 63 | 40 |
| elements/table/1 | 64 | 0.98 / 1.00 | True | 63 | 40 |
| elements/table/2 | 63 | 0.98 / 1.00 | True | 60 | 40 |
| greek/json/0 | 64 | 1.00 / 0.80 | False | 43 | 0 |
| greek/json/1 | 60 | 1.00 / 0.92 | True | 43 | 40 |
| greek/json/2 | 59 | 0.97 / 0.78 | False | 38 | 0 |
| greek/prose/0 | 63 | 0.95 / 0.71 | False | 30 | 0 |
| greek/prose/1 | 58 | 0.97 / 0.48 | False | 17 | 0 |
| greek/prose/2 | 64 | 0.98 / 0.67 | False | 26 | 0 |
| greek/table/0 | 63 | 1.00 / 0.70 | False | 35 | 0 |
| greek/table/1 | 61 | 0.97 / 0.82 | True | 38 | 38 |
| greek/table/2 | 57 | 1.00 / 0.81 | True | 37 | 37 |
| instruments/prose/0 | 42 | 1.00 / 0.95 | True | 36 | 36 |
| instruments/prose/1 | 53 | 1.00 / 1.00 | True | 50 | 40 |
| instruments/prose/2 | 63 | 0.97 / 0.97 | True | 55 | 40 |
| instruments/table/0 | 39 | 1.00 / 1.00 | True | 38 | 38 |
| instruments/table/1 | 59 | 1.00 / 1.00 | True | 59 | 40 |
| instruments/table/2 | 59 | 1.00 / 1.00 | True | 57 | 40 |
| planets/json/0 | 5 | 1.00 / 0.60 | False | 1 | 0 |
| planets/json/1 | 8 | 1.00 / 0.88 | True | 7 | 7 |
| planets/json/2 | 14 | 1.00 / 0.93 | True | 13 | 13 |
| planets/prose/0 | 59 | 1.00 / 0.20 | False | 8 | 0 |
| planets/prose/1 | 62 | 1.00 / 0.40 | False | 19 | 0 |
| planets/prose/2 | 64 | 0.95 / 0.55 | False | 20 | 0 |
| planets/table/0 | 66 | 1.00 / 0.47 | False | 15 | 0 |
| planets/table/1 | 62 | 1.00 / 0.56 | False | 20 | 0 |
| planets/table/2 | 56 | 1.00 / 0.59 | False | 23 | 0 |
| shapes/json/0 | 4 | 1.00 / 1.00 | True | 4 | 4 |
| shapes/json/1 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/json/2 | 22 | 1.00 / 1.00 | True | 22 | 22 |
| shapes/prose/0 | 37 | 0.97 / 0.95 | True | 32 | 32 |
| shapes/prose/1 | 35 | 1.00 / 1.00 | True | 34 | 34 |
| shapes/prose/2 | 38 | 1.00 / 1.00 | True | 38 | 38 |
| shapes/table/0 | 37 | 1.00 / 0.97 | True | 34 | 34 |
| shapes/table/1 | 39 | 0.97 / 1.00 | True | 37 | 37 |
| shapes/table/2 | 39 | 1.00 / 1.00 | True | 39 | 39 |
| vehicles/prose/0 | 25 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/prose/1 | 31 | 1.00 / 1.00 | True | 31 | 31 |
| vehicles/prose/2 | 42 | 0.95 / 1.00 | True | 40 | 40 |
| vehicles/table/0 | 21 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/table/1 | 46 | 1.00 / 0.98 | True | 45 | 40 |
| vehicles/table/2 | 34 | 1.00 / 1.00 | True | 32 | 32 |
