# X0b (exploratory): qwen35_9b_x0b_v2_ptr

Model qwen3.5-9b (c2022362); set x0b_v2; predicted layer 12; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 36 of 51 cells pass; 1010 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 12, pooled: HOLDS (C = 0.22 [0.13, 0.31])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 12 | PM | 1010 | 53 | 0.96 [0.95, 0.97] | 0.25 [0.16, 0.36] | 0.02 [0.01, 0.04] | 0.23 [0.15, 0.33] | mixed | 0.22 [0.13, 0.31] |
| 12 | PP | 1010 | 53 | 0.79 [0.76, 0.81] | 0.08 [0.05, 0.09] | 0.06 [0.04, 0.08] | 0.01 [-0.00, 0.03] | around | 0.22 [0.13, 0.31] |

## The k-curve at layer 12 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.25 [0.16, 0.36] | 0.02 [0.01, 0.04] | 0.23 [0.15, 0.33] | mixed |
| 25 | PP | 0.08 [0.05, 0.09] | 0.06 [0.04, 0.08] | 0.01 [-0.00, 0.03] | around |

## Probe (b) at layer 12: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| json | before | 241 | 29 | 9 | 0.70 [0.62, 0.78] | 0.24 [0.17, 0.32] | 0.11 | 0.18 [0.13, 0.23] | 0.19 [0.14, 0.24] | 0.46 [0.39, 0.53] (majority) |
| json | after | 69 | 23 | 9 | 0.13 [0.07, 0.20] | 0.14 [0.07, 0.22] | 0.11 | 0.19 [0.11, 0.27] | 0.12 [0.06, 0.16] | -0.06 [-0.14, 0.02] (structure) |
| prose | before | 715 | 59 | 9 | 0.72 [0.68, 0.76] | 0.35 [0.31, 0.39] | 0.11 | 0.32 [0.28, 0.36] | 0.36 [0.31, 0.41] | 0.36 [0.31, 0.41] (layout) |
| prose | after | 252 | 50 | 9 | 0.27 [0.23, 0.32] | 0.29 [0.24, 0.34] | 0.11 | 0.25 [0.20, 0.30] | 0.32 [0.27, 0.38] | -0.05 [-0.10, 0.00] (layout) |
| table | before | 737 | 60 | 9 | 0.84 [0.80, 0.87] | 0.20 [0.17, 0.23] | 0.11 | 0.19 [0.16, 0.22] | 0.23 [0.19, 0.27] | 0.60 [0.56, 0.64] (layout) |
| table | after | 244 | 51 | 9 | 0.26 [0.20, 0.31] | 0.19 [0.15, 0.24] | 0.11 | 0.29 [0.24, 0.34] | 0.21 [0.16, 0.26] | -0.03 [-0.09, 0.03] (structure) |

## Strata at layer 12 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | json | PP | 113 | 85 | 0.75 [0.67, 0.82] | 0.02 [-0.04, 0.07] | 0.04 [-0.05, 0.10] | -0.01 [-0.06, 0.04] | around |
| format | json | PM | 113 | 99 | 0.88 [0.80, 0.92] | 0.30 [0.22, 0.38] | 0.02 [-0.02, 0.06] | 0.28 [0.20, 0.36] | through |
| format | prose | PP | 465 | 348 | 0.75 [0.71, 0.79] | 0.06 [0.03, 0.08] | 0.05 [0.02, 0.07] | 0.01 [-0.00, 0.03] | around |
| format | prose | PM | 465 | 459 | 0.99 [0.97, 0.99] | 0.26 [0.16, 0.38] | 0.02 [0.01, 0.04] | 0.24 [0.15, 0.35] | mixed |
| format | table | PP | 432 | 363 | 0.84 [0.80, 0.87] | 0.10 [0.07, 0.14] | 0.09 [0.05, 0.12] | 0.02 [-0.01, 0.05] | around |
| format | table | PM | 432 | 415 | 0.96 [0.94, 0.98] | 0.24 [0.13, 0.36] | 0.02 [0.00, 0.05] | 0.21 [0.12, 0.33] | mixed |
| level | 0 | PP | 286 | 217 | 0.76 [0.71, 0.80] | 0.05 [0.02, 0.08] | 0.04 [0.02, 0.07] | 0.00 [-0.02, 0.03] | around |
| level | 0 | PM | 286 | 272 | 0.95 [0.92, 0.97] | 0.20 [0.12, 0.29] | 0.01 [-0.00, 0.03] | 0.19 [0.11, 0.28] | mixed |
| level | 1 | PP | 318 | 253 | 0.80 [0.75, 0.84] | 0.08 [0.04, 0.11] | 0.07 [0.02, 0.11] | 0.00 [-0.03, 0.05] | around |
| level | 1 | PM | 318 | 310 | 0.97 [0.95, 0.99] | 0.24 [0.13, 0.38] | 0.03 [0.00, 0.06] | 0.21 [0.11, 0.34] | mixed |
| level | 2 | PP | 406 | 326 | 0.80 [0.76, 0.84] | 0.10 [0.06, 0.12] | 0.07 [0.05, 0.09] | 0.02 [0.00, 0.04] | around |
| level | 2 | PM | 406 | 391 | 0.96 [0.94, 0.98] | 0.30 [0.20, 0.42] | 0.03 [0.01, 0.05] | 0.28 [0.18, 0.39] | through |
| domain | animals | PP | 235 | 182 | 0.77 [0.72, 0.82] | 0.07 [0.03, 0.11] | 0.05 [0.01, 0.09] | 0.02 [-0.01, 0.05] | around |
| domain | animals | PM | 235 | 219 | 0.93 [0.89, 0.96] | 0.26 [0.20, 0.32] | 0.03 [0.00, 0.05] | 0.23 [0.18, 0.28] | mixed |
| domain | elements | PP | 221 | 173 | 0.78 [0.72, 0.83] | 0.08 [0.05, 0.12] | 0.05 [0.02, 0.07] | 0.03 [0.00, 0.08] | around |
| domain | elements | PM | 221 | 217 | 0.98 [0.95, 0.99] | 0.28 [0.15, 0.41] | -0.00 [-0.02, 0.00] | 0.28 [0.15, 0.43] | mixed |
| domain | greek | PP | 33 | 26 ⚠ | 0.79 [0.62, 0.89] | 0.04 [0.00, 0.12] | 0.08 [0.00, 0.17] | -0.04 [-0.11, 0.00] | can't tell |
| domain | greek | PM | 33 | 27 ⚠ | 0.82 [0.66, 0.91] | 0.41 [0.19, 0.56] | 0.07 [0.00, 0.21] | 0.33 [0.09, 0.50] | can't tell |
| domain | instruments | PP | 231 | 176 | 0.76 [0.70, 0.81] | 0.10 [0.05, 0.12] | 0.08 [0.00, 0.10] | 0.02 [0.00, 0.12] | around |
| domain | instruments | PM | 231 | 228 | 0.99 [0.96, 1.00] | 0.13 [0.00, 0.56] | 0.03 [0.00, 0.14] | 0.10 [0.00, 0.44] | mixed |
| domain | shapes | PP | 115 | 89 | 0.77 [0.69, 0.84] | 0.09 [0.06, 0.12] | 0.10 [0.09, 0.12] | -0.01 [-0.02, 0.00] | around |
| domain | shapes | PM | 115 | 110 | 0.96 [0.90, 0.98] | 0.35 [0.28, 0.44] | 0.02 [0.00, 0.04] | 0.34 [0.28, 0.40] | through |
| domain | vehicles | PP | 175 | 150 | 0.86 [0.80, 0.90] | 0.05 [0.02, 0.10] | 0.05 [0.03, 0.07] | -0.01 [-0.05, 0.03] | around |
| domain | vehicles | PM | 175 | 172 | 0.98 [0.95, 0.99] | 0.30 [0.08, 0.48] | 0.03 [0.00, 0.08] | 0.27 [0.08, 0.44] | mixed |
| order | after | PP | 249 | 94 | 0.38 [0.32, 0.44] | 0.28 [0.18, 0.36] | 0.21 [0.10, 0.31] | 0.06 [-0.02, 0.18] | around |
| order | after | PM | 249 | 239 | 0.96 [0.93, 0.98] | 0.49 [0.31, 0.70] | 0.03 [0.00, 0.08] | 0.46 [0.29, 0.65] | through |
| order | before | PP | 761 | 702 | 0.92 [0.90, 0.94] | 0.05 [0.03, 0.06] | 0.04 [0.03, 0.06] | 0.01 [-0.01, 0.02] | around |
| order | before | PM | 761 | 734 | 0.96 [0.95, 0.98] | 0.18 [0.11, 0.26] | 0.02 [0.00, 0.04] | 0.16 [0.09, 0.23] | mixed |
| numbers | digits | PP | 552 | 440 | 0.80 [0.76, 0.83] | 0.07 [0.04, 0.10] | 0.05 [0.02, 0.08] | 0.02 [0.00, 0.04] | around |
| numbers | digits | PM | 552 | 536 | 0.97 [0.95, 0.98] | 0.25 [0.16, 0.35] | 0.02 [0.01, 0.04] | 0.22 [0.15, 0.32] | mixed |
| numbers | words | PP | 458 | 356 | 0.78 [0.74, 0.81] | 0.08 [0.05, 0.11] | 0.08 [0.05, 0.10] | 0.01 [-0.02, 0.03] | around |
| numbers | words | PM | 458 | 437 | 0.95 [0.93, 0.97] | 0.26 [0.16, 0.39] | 0.02 [0.01, 0.04] | 0.24 [0.14, 0.36] | mixed |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/json/0 | 18 | 0.89 / 0.89 | True | 10 | 10 |
| animals/json/1 | 36 | 0.94 / 0.81 | True | 21 | 21 |
| animals/json/2 | 31 | 0.84 / 0.87 | True | 18 | 18 |
| animals/prose/0 | 42 | 0.95 / 0.83 | True | 33 | 33 |
| animals/prose/1 | 60 | 0.97 / 0.92 | True | 45 | 40 |
| animals/prose/2 | 56 | 0.96 / 0.88 | True | 44 | 40 |
| animals/table/0 | 51 | 0.98 / 0.82 | True | 33 | 33 |
| animals/table/1 | 57 | 0.98 / 0.79 | False | 33 | 0 |
| animals/table/2 | 55 | 0.96 / 0.91 | True | 43 | 40 |
| elements/prose/0 | 41 | 0.98 / 0.93 | True | 36 | 36 |
| elements/prose/1 | 47 | 0.98 / 0.87 | True | 35 | 35 |
| elements/prose/2 | 41 | 0.98 / 1.00 | True | 36 | 36 |
| elements/table/0 | 41 | 0.98 / 1.00 | True | 37 | 37 |
| elements/table/1 | 49 | 0.90 / 0.96 | True | 37 | 37 |
| elements/table/2 | 46 | 0.98 / 1.00 | True | 42 | 40 |
| greek/json/0 | 61 | 0.90 / 0.67 | False | 19 | 0 |
| greek/json/1 | 62 | 0.92 / 0.68 | False | 21 | 0 |
| greek/json/2 | 65 | 0.92 / 0.82 | True | 33 | 33 |
| greek/prose/0 | 64 | 0.95 / 0.80 | False | 36 | 0 |
| greek/prose/1 | 63 | 0.97 / 0.79 | False | 31 | 0 |
| greek/prose/2 | 63 | 0.95 / 0.68 | False | 27 | 0 |
| greek/table/0 | 63 | 1.00 / 0.62 | False | 26 | 0 |
| greek/table/1 | 65 | 0.97 / 0.66 | False | 27 | 0 |
| greek/table/2 | 64 | 0.97 / 0.75 | False | 36 | 0 |
| instruments/prose/0 | 42 | 0.98 / 0.98 | True | 35 | 35 |
| instruments/prose/1 | 53 | 0.96 / 0.96 | True | 48 | 40 |
| instruments/prose/2 | 63 | 0.94 / 0.95 | True | 54 | 40 |
| instruments/table/0 | 39 | 1.00 / 1.00 | True | 36 | 36 |
| instruments/table/1 | 59 | 0.97 / 0.97 | True | 52 | 40 |
| instruments/table/2 | 59 | 0.98 / 1.00 | True | 53 | 40 |
| planets/prose/0 | 59 | 0.97 / 0.63 | False | 25 | 0 |
| planets/prose/1 | 62 | 1.00 / 0.69 | False | 26 | 0 |
| planets/prose/2 | 64 | 0.95 / 0.69 | False | 30 | 0 |
| planets/table/0 | 66 | 0.95 / 0.56 | False | 16 | 0 |
| planets/table/1 | 62 | 0.98 / 0.58 | False | 15 | 0 |
| planets/table/2 | 56 | 0.89 / 0.59 | False | 14 | 0 |
| shapes/json/0 | 4 | 1.00 / 1.00 | True | 3 | 3 |
| shapes/json/1 | 11 | 1.00 / 1.00 | True | 10 | 10 |
| shapes/json/2 | 22 | 0.91 / 1.00 | True | 18 | 18 |
| shapes/prose/0 | 10 | 0.90 / 1.00 | True | 9 | 9 |
| shapes/prose/1 | 14 | 1.00 / 1.00 | True | 13 | 13 |
| shapes/prose/2 | 25 | 0.84 / 1.00 | True | 21 | 21 |
| shapes/table/0 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/table/1 | 15 | 1.00 / 1.00 | True | 13 | 13 |
| shapes/table/2 | 22 | 0.95 / 0.95 | True | 17 | 17 |
| vehicles/prose/0 | 25 | 1.00 / 1.00 | True | 23 | 23 |
| vehicles/prose/1 | 31 | 0.97 / 1.00 | True | 29 | 29 |
| vehicles/prose/2 | 42 | 0.95 / 0.93 | True | 35 | 35 |
| vehicles/table/0 | 21 | 1.00 / 1.00 | True | 20 | 20 |
| vehicles/table/1 | 46 | 0.93 / 1.00 | True | 40 | 40 |
| vehicles/table/2 | 34 | 0.91 / 0.97 | True | 28 | 28 |
