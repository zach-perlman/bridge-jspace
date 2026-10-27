# X0b (exploratory): qwen35_122b_x0b_v2_ptr

Model qwen3.5-122b-a10b (a099dee7); set x0b_v2; predicted layer 33; J++ k = 25 signed, the random part of its share; the alt built here (single change). UNVERIFIED.

Gate per cell: 48 of 51 cells pass; 1552 eligible scenes used (at most 40 per cell).

## X0b's rule at layer 33, pooled: MIXED (C = 0.15 [0.12, 0.18])

Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1.

| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |
|---|---|---|---|---|---|---|---|---|---|
| 33 | PM | 1552 | 61 | 0.92 [0.91, 0.94] | 0.20 [0.17, 0.23] | 0.06 [0.04, 0.08] | 0.14 [0.11, 0.17] | mixed | 0.15 [0.12, 0.18] |
| 33 | PP | 1552 | 61 | 0.76 [0.74, 0.78] | 0.03 [0.02, 0.05] | 0.05 [0.03, 0.06] | -0.01 [-0.02, -0.00] | around | 0.15 [0.12, 0.18] |

## The k-curve at layer 33 (descriptive)

| k | reader | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|
| 25 | PM | 0.20 [0.17, 0.23] | 0.06 [0.04, 0.08] | 0.14 [0.11, 0.17] | mixed |
| 25 | PP | 0.03 [0.02, 0.05] | 0.05 [0.03, 0.06] | -0.01 [-0.02, -0.00] | around |

## Probe (b) at layer 33: the bridge's locker row ordinal (descriptive)

Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the most frequent ordinal given how many locker statements precede the asked pick, of how many.

| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| json | before | 241 | 29 | 9 | 0.75 [0.68, 0.82] | 0.24 [0.17, 0.32] | 0.11 | 0.18 [0.13, 0.23] | 0.19 [0.14, 0.24] | 0.51 [0.44, 0.57] (majority) |
| json | after | 69 | 23 | 9 | 0.12 [0.05, 0.19] | 0.14 [0.07, 0.22] | 0.11 | 0.19 [0.11, 0.27] | 0.12 [0.06, 0.16] | -0.07 [-0.18, 0.03] (structure) |
| prose | before | 715 | 59 | 9 | 0.69 [0.65, 0.72] | 0.35 [0.31, 0.39] | 0.11 | 0.32 [0.28, 0.36] | 0.36 [0.31, 0.41] | 0.32 [0.28, 0.37] (layout) |
| prose | after | 252 | 50 | 9 | 0.28 [0.23, 0.33] | 0.29 [0.24, 0.34] | 0.11 | 0.25 [0.20, 0.30] | 0.32 [0.27, 0.38] | -0.04 [-0.09, 0.01] (layout) |
| table | before | 737 | 60 | 9 | 0.82 [0.79, 0.86] | 0.20 [0.17, 0.23] | 0.11 | 0.19 [0.16, 0.22] | 0.23 [0.19, 0.27] | 0.59 [0.55, 0.63] (layout) |
| table | after | 244 | 51 | 9 | 0.27 [0.21, 0.32] | 0.19 [0.15, 0.24] | 0.11 | 0.29 [0.24, 0.34] | 0.21 [0.16, 0.26] | -0.02 [-0.08, 0.03] (structure) |

## Strata at layer 33 (descriptive)

⚠ = fewer than 30 switched by the whole edit.

| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| format | json | PP | 221 | 173 | 0.78 [0.72, 0.83] | 0.03 [0.00, 0.08] | 0.04 [0.00, 0.09] | -0.01 [-0.04, 0.03] | around |
| format | json | PM | 221 | 193 | 0.87 [0.82, 0.91] | 0.15 [0.08, 0.22] | 0.05 [-0.01, 0.11] | 0.10 [0.05, 0.16] | mixed |
| format | prose | PP | 691 | 512 | 0.74 [0.71, 0.77] | 0.04 [0.02, 0.07] | 0.05 [0.03, 0.07] | -0.01 [-0.03, 0.01] | around |
| format | prose | PM | 691 | 649 | 0.94 [0.92, 0.95] | 0.20 [0.16, 0.26] | 0.04 [0.02, 0.07] | 0.16 [0.13, 0.21] | mixed |
| format | table | PP | 640 | 496 | 0.78 [0.74, 0.81] | 0.02 [0.01, 0.04] | 0.05 [0.03, 0.07] | -0.02 [-0.04, -0.01] | around |
| format | table | PM | 640 | 593 | 0.93 [0.90, 0.94] | 0.20 [0.17, 0.24] | 0.08 [0.05, 0.11] | 0.12 [0.09, 0.17] | mixed |
| level | 0 | PP | 425 | 329 | 0.77 [0.73, 0.81] | 0.01 [0.00, 0.02] | 0.03 [0.01, 0.06] | -0.02 [-0.04, -0.01] | around |
| level | 0 | PM | 425 | 391 | 0.92 [0.89, 0.94] | 0.16 [0.13, 0.20] | 0.03 [0.01, 0.06] | 0.13 [0.09, 0.17] | mixed |
| level | 1 | PP | 565 | 413 | 0.73 [0.69, 0.77] | 0.04 [0.02, 0.07] | 0.06 [0.03, 0.08] | -0.02 [-0.03, -0.00] | around |
| level | 1 | PM | 565 | 530 | 0.94 [0.92, 0.96] | 0.20 [0.16, 0.24] | 0.06 [0.04, 0.08] | 0.14 [0.11, 0.18] | mixed |
| level | 2 | PP | 562 | 439 | 0.78 [0.75, 0.81] | 0.04 [0.02, 0.07] | 0.05 [0.02, 0.07] | -0.00 [-0.02, 0.02] | around |
| level | 2 | PM | 562 | 514 | 0.91 [0.89, 0.94] | 0.22 [0.19, 0.27] | 0.08 [0.05, 0.11] | 0.15 [0.11, 0.18] | mixed |
| domain | animals | PP | 260 | 194 | 0.75 [0.69, 0.80] | 0.06 [0.03, 0.09] | 0.07 [0.04, 0.10] | -0.01 [-0.04, 0.01] | around |
| domain | animals | PM | 260 | 207 | 0.80 [0.74, 0.84] | 0.27 [0.19, 0.34] | 0.13 [0.07, 0.18] | 0.14 [0.08, 0.19] | mixed |
| domain | elements | PP | 232 | 167 | 0.72 [0.66, 0.77] | 0.03 [-0.01, 0.06] | 0.04 [0.00, 0.10] | -0.01 [-0.04, 0.01] | around |
| domain | elements | PM | 232 | 224 | 0.97 [0.93, 0.98] | 0.23 [0.18, 0.32] | 0.00 [-0.01, 0.02] | 0.23 [0.17, 0.32] | mixed |
| domain | greek | PP | 360 | 278 | 0.77 [0.73, 0.81] | 0.02 [0.00, 0.05] | 0.02 [-0.01, 0.06] | 0.00 [-0.02, 0.02] | around |
| domain | greek | PM | 360 | 334 | 0.93 [0.90, 0.95] | 0.17 [0.11, 0.22] | 0.06 [0.03, 0.09] | 0.11 [0.07, 0.15] | mixed |
| domain | instruments | PP | 229 | 177 | 0.77 [0.71, 0.82] | 0.06 [0.03, 0.07] | 0.07 [0.06, 0.07] | -0.01 [-0.03, 0.00] | around |
| domain | instruments | PM | 229 | 224 | 0.98 [0.95, 0.99] | 0.18 [0.15, 0.33] | 0.06 [0.00, 0.10] | 0.12 [0.08, 0.33] | mixed |
| domain | planets | PP | 152 | 113 | 0.74 [0.67, 0.81] | 0.01 [0.00, 0.02] | 0.04 [0.01, 0.09] | -0.04 [-0.08, 0.00] | around |
| domain | planets | PM | 152 | 141 | 0.93 [0.88, 0.96] | 0.23 [0.13, 0.31] | 0.06 [0.01, 0.12] | 0.16 [0.11, 0.22] | mixed |
| domain | shapes | PP | 130 | 99 | 0.76 [0.68, 0.83] | -0.01 [-0.02, 0.00] | 0.02 [0.02, 0.02] | -0.03 [-0.04, -0.02] | around |
| domain | shapes | PM | 130 | 127 | 0.98 [0.93, 0.99] | 0.17 [0.16, 0.18] | 0.02 [0.00, 0.03] | 0.16 [0.15, 0.16] | mixed |
| domain | vehicles | PP | 189 | 153 | 0.81 [0.75, 0.86] | 0.04 [0.00, 0.10] | 0.07 [0.00, 0.13] | -0.03 [-0.04, 0.00] | around |
| domain | vehicles | PM | 189 | 178 | 0.94 [0.90, 0.97] | 0.14 [0.13, 0.16] | 0.07 [0.05, 0.10] | 0.07 [0.04, 0.09] | around |
| order | after | PP | 409 | 97 | 0.24 [0.20, 0.28] | 0.32 [0.21, 0.42] | 0.39 [0.26, 0.51] | -0.07 [-0.16, 0.02] | can't tell |
| order | after | PM | 409 | 363 | 0.89 [0.85, 0.91] | 0.50 [0.43, 0.59] | 0.09 [0.05, 0.13] | 0.41 [0.33, 0.50] | through |
| order | before | PP | 1143 | 1084 | 0.95 [0.93, 0.96] | 0.01 [-0.00, 0.02] | 0.02 [0.01, 0.03] | -0.01 [-0.02, 0.00] | around |
| order | before | PM | 1143 | 1072 | 0.94 [0.92, 0.95] | 0.09 [0.07, 0.12] | 0.05 [0.03, 0.07] | 0.05 [0.03, 0.07] | around |
| numbers | digits | PP | 827 | 620 | 0.75 [0.72, 0.78] | 0.03 [0.01, 0.05] | 0.05 [0.02, 0.07] | -0.01 [-0.03, 0.00] | around |
| numbers | digits | PM | 827 | 765 | 0.93 [0.91, 0.94] | 0.20 [0.17, 0.23] | 0.06 [0.04, 0.08] | 0.13 [0.10, 0.16] | mixed |
| numbers | words | PP | 725 | 561 | 0.77 [0.74, 0.80] | 0.03 [0.01, 0.05] | 0.05 [0.03, 0.07] | -0.01 [-0.03, 0.00] | around |
| numbers | words | PM | 725 | 670 | 0.92 [0.90, 0.94] | 0.20 [0.16, 0.24] | 0.05 [0.03, 0.08] | 0.15 [0.11, 0.19] | mixed |

## Gate per cell

| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |
|---|---|---|---|---|---|
| animals/json/0 | 18 | 1.00 / 1.00 | True | 15 | 15 |
| animals/json/1 | 36 | 0.94 / 0.92 | True | 28 | 28 |
| animals/json/2 | 31 | 0.97 / 0.90 | True | 23 | 23 |
| animals/prose/0 | 42 | 1.00 / 0.79 | False | 26 | 0 |
| animals/prose/1 | 60 | 0.98 / 0.80 | True | 44 | 40 |
| animals/prose/2 | 56 | 0.98 / 0.86 | True | 43 | 40 |
| animals/table/0 | 51 | 0.96 / 0.96 | True | 38 | 38 |
| animals/table/1 | 57 | 0.98 / 0.84 | True | 36 | 36 |
| animals/table/2 | 55 | 0.98 / 0.91 | True | 40 | 40 |
| elements/prose/0 | 41 | 0.98 / 0.88 | True | 35 | 35 |
| elements/prose/1 | 47 | 1.00 / 0.98 | True | 45 | 40 |
| elements/prose/2 | 41 | 1.00 / 1.00 | True | 41 | 40 |
| elements/table/0 | 41 | 1.00 / 0.90 | True | 37 | 37 |
| elements/table/1 | 49 | 0.98 / 0.94 | True | 41 | 40 |
| elements/table/2 | 46 | 1.00 / 0.98 | True | 42 | 40 |
| greek/json/0 | 61 | 1.00 / 0.92 | True | 43 | 40 |
| greek/json/1 | 62 | 0.95 / 0.89 | True | 45 | 40 |
| greek/json/2 | 65 | 0.98 / 0.92 | True | 51 | 40 |
| greek/prose/0 | 64 | 0.98 / 0.92 | True | 47 | 40 |
| greek/prose/1 | 63 | 1.00 / 0.87 | True | 40 | 40 |
| greek/prose/2 | 63 | 1.00 / 0.89 | True | 48 | 40 |
| greek/table/0 | 63 | 0.97 / 0.94 | True | 50 | 40 |
| greek/table/1 | 65 | 0.97 / 0.88 | True | 49 | 40 |
| greek/table/2 | 64 | 0.95 / 0.89 | True | 44 | 40 |
| instruments/prose/0 | 42 | 0.98 / 0.88 | True | 32 | 32 |
| instruments/prose/1 | 53 | 1.00 / 0.81 | True | 42 | 40 |
| instruments/prose/2 | 63 | 0.98 / 0.89 | True | 51 | 40 |
| instruments/table/0 | 39 | 1.00 / 1.00 | True | 37 | 37 |
| instruments/table/1 | 59 | 0.98 / 1.00 | True | 56 | 40 |
| instruments/table/2 | 59 | 0.98 / 0.98 | True | 56 | 40 |
| planets/prose/0 | 59 | 1.00 / 0.93 | True | 53 | 40 |
| planets/prose/1 | 62 | 1.00 / 0.95 | True | 58 | 40 |
| planets/prose/2 | 64 | 0.98 / 0.97 | True | 57 | 40 |
| planets/table/0 | 66 | 0.95 / 0.71 | False | 38 | 0 |
| planets/table/1 | 62 | 0.97 / 0.87 | True | 32 | 32 |
| planets/table/2 | 56 | 0.98 / 0.77 | False | 25 | 0 |
| shapes/json/0 | 4 | 1.00 / 1.00 | True | 4 | 4 |
| shapes/json/1 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/json/2 | 22 | 0.95 / 1.00 | True | 20 | 20 |
| shapes/prose/0 | 10 | 1.00 / 1.00 | True | 10 | 10 |
| shapes/prose/1 | 14 | 1.00 / 1.00 | True | 14 | 14 |
| shapes/prose/2 | 25 | 1.00 / 1.00 | True | 25 | 25 |
| shapes/table/0 | 11 | 1.00 / 1.00 | True | 11 | 11 |
| shapes/table/1 | 15 | 1.00 / 1.00 | True | 14 | 14 |
| shapes/table/2 | 22 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/prose/0 | 25 | 1.00 / 1.00 | True | 25 | 25 |
| vehicles/prose/1 | 31 | 1.00 / 1.00 | True | 30 | 30 |
| vehicles/prose/2 | 42 | 0.98 / 0.98 | True | 41 | 40 |
| vehicles/table/0 | 21 | 1.00 / 1.00 | True | 21 | 21 |
| vehicles/table/1 | 46 | 1.00 / 1.00 | True | 46 | 40 |
| vehicles/table/2 | 34 | 1.00 / 1.00 | True | 33 | 33 |
