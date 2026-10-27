# X0b (exploratory): x0b_v2_ptr_27b

Model qwen3.6-27b (6a9e13bd); set x0b_v2; predicted layer 32; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 49 of 51 cells pass; 1635 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 32, pooled: HOLDS (C = 0.48 [0.42, 0.53])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 32 | PM | 1635 | 61 | 0.68 [0.65, 0.70] | 0.56 [0.51, 0.62] | 0.01 [-0.02, 0.03] | 0.56 [0.50, 0.61] | through | 0.48 [0.42, 0.53] |
| 32 | PP | 1635 | 61 | 0.66 [0.64, 0.68] | 0.07 [0.05, 0.09] | -0.01 [-0.02, -0.00] | 0.08 [0.06, 0.10] | around | 0.48 [0.42, 0.53] |

## The k-curve at layer 32 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.56 [0.51, 0.62] | 0.01 [-0.02, 0.03] | 0.56 [0.50, 0.61] | through |
| 25 | PP | 0.07 [0.05, 0.09] | -0.01 [-0.02, -0.00] | 0.08 [0.06, 0.10] | around |

## Probe (b) at layer 32: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| json | before | 241 | 29 | 9 | 0.80 [0.74, 0.85] | 0.24 [0.17, 0.32] | 0.11 | 0.18 [0.13, 0.23] | 0.19 [0.14, 0.24] | 0.56 [0.48, 0.63] (majority) |
| json | after | 69 | 23 | 9 | 0.13 [0.07, 0.19] | 0.14 [0.07, 0.22] | 0.11 | 0.19 [0.11, 0.27] | 0.12 [0.06, 0.16] | -0.06 [-0.14, 0.02] (structure) |
| prose | before | 715 | 59 | 9 | 0.74 [0.70, 0.77] | 0.35 [0.31, 0.39] | 0.11 | 0.32 [0.28, 0.36] | 0.36 [0.31, 0.41] | 0.37 [0.33, 0.43] (layout) |
| prose | after | 252 | 50 | 9 | 0.28 [0.23, 0.32] | 0.29 [0.24, 0.34] | 0.11 | 0.25 [0.20, 0.30] | 0.32 [0.27, 0.38] | -0.04 [-0.11, 0.01] (layout) |
| table | before | 737 | 60 | 9 | 0.88 [0.85, 0.91] | 0.20 [0.17, 0.23] | 0.11 | 0.19 [0.16, 0.22] | 0.23 [0.19, 0.27] | 0.65 [0.61, 0.69] (layout) |
| table | after | 244 | 51 | 9 | 0.23 [0.18, 0.29] | 0.19 [0.15, 0.24] | 0.11 | 0.29 [0.24, 0.34] | 0.21 [0.16, 0.26] | -0.06 [-0.11, 0.00] (structure) |

## Strata at layer 32 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | json | PP | 233 | 167 | 0.72 [0.66, 0.77] | 0.02 [-0.02, 0.06] | -0.02 [-0.05, 0.01] | 0.04 [0.01, 0.08] | around |
| format | json | PM | 233 | 182 | 0.78 [0.72, 0.83] | 0.46 [0.36, 0.57] | -0.01 [-0.05, 0.04] | 0.47 [0.37, 0.58] | through |
| format | prose | PP | 741 | 443 | 0.60 [0.56, 0.63] | 0.10 [0.06, 0.13] | -0.02 [-0.05, -0.00] | 0.12 [0.08, 0.16] | mixed |
| format | prose | PM | 741 | 466 | 0.63 [0.59, 0.66] | 0.63 [0.57, 0.69] | -0.01 [-0.04, 0.02] | 0.64 [0.57, 0.70] | through |
| format | table | PP | 661 | 472 | 0.71 [0.68, 0.75] | 0.06 [0.04, 0.08] | -0.00 [-0.02, 0.01] | 0.06 [0.04, 0.08] | around |
| format | table | PM | 661 | 459 | 0.69 [0.66, 0.73] | 0.54 [0.47, 0.61] | 0.02 [-0.01, 0.06] | 0.51 [0.45, 0.59] | through |
| level | 0 | PP | 522 | 371 | 0.71 [0.67, 0.75] | 0.02 [0.01, 0.04] | -0.01 [-0.02, 0.01] | 0.03 [0.01, 0.05] | around |
| level | 0 | PM | 522 | 354 | 0.68 [0.64, 0.72] | 0.45 [0.38, 0.52] | 0.02 [-0.02, 0.05] | 0.43 [0.35, 0.51] | through |
| level | 1 | PP | 544 | 339 | 0.62 [0.58, 0.66] | 0.09 [0.06, 0.13] | -0.01 [-0.04, 0.01] | 0.10 [0.06, 0.15] | mixed |
| level | 1 | PM | 544 | 356 | 0.65 [0.61, 0.69] | 0.60 [0.53, 0.68] | -0.02 [-0.05, 0.01] | 0.62 [0.55, 0.69] | through |
| level | 2 | PP | 569 | 372 | 0.65 [0.61, 0.69] | 0.09 [0.06, 0.13] | -0.03 [-0.05, -0.00] | 0.12 [0.08, 0.16] | mixed |
| level | 2 | PM | 569 | 397 | 0.70 [0.66, 0.73] | 0.63 [0.57, 0.70] | 0.02 [-0.01, 0.04] | 0.62 [0.54, 0.69] | through |
| domain | animals | PP | 316 | 218 | 0.69 [0.64, 0.74] | 0.06 [0.03, 0.10] | -0.00 [-0.03, 0.02] | 0.07 [0.03, 0.11] | around |
| domain | animals | PM | 316 | 203 | 0.64 [0.59, 0.69] | 0.54 [0.44, 0.63] | 0.05 [0.00, 0.10] | 0.49 [0.42, 0.57] | through |
| domain | elements | PP | 240 | 156 | 0.65 [0.59, 0.71] | 0.08 [0.03, 0.14] | -0.02 [-0.05, 0.00] | 0.10 [0.04, 0.16] | around |
| domain | elements | PM | 240 | 192 | 0.80 [0.74, 0.85] | 0.62 [0.47, 0.75] | -0.03 [-0.05, -0.02] | 0.66 [0.52, 0.78] | through |
| domain | greek | PP | 360 | 248 | 0.69 [0.64, 0.73] | 0.04 [0.01, 0.06] | -0.02 [-0.04, 0.00] | 0.06 [0.03, 0.08] | around |
| domain | greek | PM | 360 | 280 | 0.78 [0.73, 0.82] | 0.65 [0.54, 0.75] | -0.01 [-0.04, 0.02] | 0.65 [0.56, 0.75] | through |
| domain | instruments | PP | 235 | 138 | 0.59 [0.52, 0.65] | 0.09 [0.04, 0.10] | -0.01 [-0.06, 0.00] | 0.10 [0.04, 0.11] | mixed |
| domain | instruments | PM | 235 | 132 | 0.56 [0.50, 0.62] | 0.56 [0.53, 0.59] | -0.02 [-0.20, 0.00] | 0.58 [0.56, 0.73] | through |
| domain | planets | PP | 160 | 103 | 0.64 [0.57, 0.71] | 0.08 [0.01, 0.15] | -0.03 [-0.08, 0.01] | 0.11 [0.05, 0.18] | mixed |
| domain | planets | PM | 160 | 100 | 0.62 [0.55, 0.70] | 0.52 [0.37, 0.67] | 0.03 [-0.07, 0.12] | 0.49 [0.34, 0.62] | through |
| domain | shapes | PP | 134 | 89 | 0.66 [0.58, 0.74] | 0.11 [0.06, 0.18] | -0.02 [-0.05, 0.00] | 0.13 [0.06, 0.23] | mixed |
| domain | shapes | PM | 134 | 96 | 0.72 [0.63, 0.79] | 0.42 [0.33, 0.51] | -0.03 [-0.04, -0.02] | 0.45 [0.37, 0.53] | through |
| domain | vehicles | PP | 190 | 130 | 0.68 [0.61, 0.75] | 0.07 [0.06, 0.10] | 0.00 [-0.03, 0.02] | 0.07 [0.05, 0.13] | around |
| domain | vehicles | PM | 190 | 104 | 0.55 [0.48, 0.62] | 0.45 [0.38, 0.59] | 0.07 [-0.06, 0.14] | 0.38 [0.31, 0.65] | through |
| order | after | PP | 408 | 20 ⚠ | 0.05 [0.03, 0.07] | 0.45 [0.27, 0.64] | -0.10 [-0.35, 0.08] | 0.55 [0.26, 0.88] | can't tell |
| order | after | PM | 408 | 241 | 0.59 [0.54, 0.64] | 0.82 [0.75, 0.91] | -0.02 [-0.07, 0.03] | 0.84 [0.75, 0.94] | through |
| order | before | PP | 1227 | 1062 | 0.87 [0.85, 0.88] | 0.06 [0.04, 0.08] | -0.01 [-0.02, -0.00] | 0.07 [0.05, 0.10] | around |
| order | before | PM | 1227 | 866 | 0.71 [0.68, 0.73] | 0.49 [0.43, 0.56] | 0.01 [-0.01, 0.03] | 0.48 [0.41, 0.55] | through |
| numbers | digits | PP | 865 | 579 | 0.67 [0.64, 0.70] | 0.07 [0.05, 0.09] | -0.01 [-0.02, 0.01] | 0.08 [0.06, 0.11] | around |
| numbers | digits | PM | 865 | 578 | 0.67 [0.64, 0.70] | 0.58 [0.52, 0.64] | 0.00 [-0.02, 0.03] | 0.58 [0.51, 0.64] | through |
| numbers | words | PP | 770 | 503 | 0.65 [0.62, 0.69] | 0.07 [0.03, 0.10] | -0.02 [-0.04, -0.00] | 0.09 [0.06, 0.12] | around |
| numbers | words | PM | 770 | 529 | 0.69 [0.65, 0.72] | 0.55 [0.49, 0.61] | 0.01 [-0.02, 0.04] | 0.54 [0.48, 0.60] | through |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/json/0 | 18 | 1.00 / 1.00 | True | 16 | 16 |
| animals/json/1 | 36 | 1.00 / 0.92 | True | 33 | 33 |
| animals/json/2 | 31 | 1.00 / 1.00 | True | 27 | 27 |
| animals/prose/0 | 42 | 1.00 / 1.00 | True | 40 | 40 |
| animals/prose/1 | 60 | 1.00 / 0.98 | True | 58 | 40 |
| animals/prose/2 | 56 | 1.00 / 0.96 | True | 53 | 40 |
| animals/table/0 | 51 | 1.00 / 0.96 | True | 45 | 40 |
| animals/table/1 | 57 | 0.98 / 0.96 | True | 52 | 40 |
| animals/table/2 | 55 | 0.98 / 0.95 | True | 48 | 40 |
| elements/prose/0 | 41 | 1.00 / 1.00 | True | 40 | 40 |
| elements/prose/1 | 47 | 1.00 / 1.00 | True | 47 | 40 |
| elements/prose/2 | 41 | 1.00 / 1.00 | True | 41 | 40 |
| elements/table/0 | 41 | 1.00 / 1.00 | True | 41 | 40 |
| elements/table/1 | 49 | 1.00 / 1.00 | True | 48 | 40 |
| elements/table/2 | 46 | 1.00 / 1.00 | True | 46 | 40 |
| greek/json/0 | 61 | 1.00 / 0.97 | True | 54 | 40 |
| greek/json/1 | 62 | 1.00 / 0.94 | True | 50 | 40 |
| greek/json/2 | 65 | 0.98 / 0.94 | True | 55 | 40 |
| greek/prose/0 | 64 | 1.00 / 0.95 | True | 60 | 40 |
| greek/prose/1 | 63 | 1.00 / 0.98 | True | 57 | 40 |
| greek/prose/2 | 63 | 1.00 / 0.89 | True | 49 | 40 |
| greek/table/0 | 63 | 1.00 / 0.95 | True | 57 | 40 |
| greek/table/1 | 65 | 1.00 / 0.88 | True | 52 | 40 |
| greek/table/2 | 64 | 1.00 / 0.97 | True | 61 | 40 |
| instruments/prose/0 | 42 | 1.00 / 1.00 | True | 36 | 36 |
| instruments/prose/1 | 53 | 1.00 / 0.96 | True | 47 | 40 |
| instruments/prose/2 | 63 | 1.00 / 0.95 | True | 58 | 40 |
| instruments/table/0 | 39 | 1.00 / 1.00 | True | 39 | 39 |
| instruments/table/1 | 59 | 1.00 / 0.97 | True | 57 | 40 |
| instruments/table/2 | 59 | 1.00 / 0.98 | True | 54 | 40 |
| planets/prose/0 | 59 | 1.00 / 0.90 | True | 47 | 40 |
| planets/prose/1 | 62 | 1.00 / 0.90 | True | 52 | 40 |
| planets/prose/2 | 64 | 1.00 / 0.89 | True | 53 | 40 |
| planets/table/0 | 66 | 1.00 / 0.83 | True | 44 | 40 |
| planets/table/1 | 62 | 1.00 / 0.74 | False | 33 | 0 |
| planets/table/2 | 56 | 1.00 / 0.71 | False | 31 | 0 |
| shapes/json/0 | 4 | 1.00 / 1.00 | True | 4 | 4 |
| shapes/json/1 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/json/2 | 22 | 1.00 / 1.00 | True | 22 | 22 |
| shapes/prose/0 | 10 | 1.00 / 1.00 | True | 10 | 10 |
| shapes/prose/1 | 14 | 1.00 / 1.00 | True | 14 | 14 |
| shapes/prose/2 | 25 | 1.00 / 1.00 | True | 25 | 25 |
| shapes/table/0 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/table/1 | 15 | 1.00 / 1.00 | True | 15 | 15 |
| shapes/table/2 | 22 | 1.00 / 1.00 | True | 22 | 22 |
| vehicles/prose/0 | 25 | 1.00 / 1.00 | True | 25 | 25 |
| vehicles/prose/1 | 31 | 1.00 / 1.00 | True | 31 | 31 |
| vehicles/prose/2 | 42 | 1.00 / 0.98 | True | 41 | 40 |
| vehicles/table/0 | 21 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/table/1 | 46 | 0.98 / 1.00 | True | 45 | 40 |
| vehicles/table/2 | 34 | 1.00 / 1.00 | True | 33 | 33 |
