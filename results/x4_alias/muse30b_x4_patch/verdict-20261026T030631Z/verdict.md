# X4 verdict: muse30b_x4_patch (muse-glimmer-30b, layer 26)

jobs/c3/X4.md section 2. J++ k = 25 against a random part of its share; bootstrap over bridge entities (10000 resamples, seed 0), the same draws for both forms of a domain. UNVERIFIED.

## Gate (unedited org accuracy, decisive read, >= 0.80 per form and reader)

| form / reader | cases | accuracy | pass | eligible |
|---|---|---|---|---|
| animals/same/PP | 400 | 0.98 | True | 388 |
| animals/same/PM | 400 | 1.00 | True | 180 |
| animals/xlang/PP | 400 | 0.97 | True | 378 |
| animals/xlang/PM | 400 | 0.99 | True | 180 |
| elements/same/PP | 400 | 0.99 | True | 395 |
| elements/same/PM | 400 | 1.00 | True | 400 |
| elements/syn/PP | 400 | 0.97 | True | 380 |
| elements/syn/PM | 400 | 1.00 | True | 398 |

## Cells per form and reader (each reader on its own eligible items; the recall's rows are a stability check, X4.md)

| form | reader | n | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|
| animals/same | recall | 180 | 0.38 [0.31, 0.45] | 0.44 [0.19, 0.66] | -0.03 [-0.14, 0.06] | 0.47 [0.30, 0.61] | through |
| animals/same | lookup | 388 | 0.61 [0.56, 0.66] | -0.08 [-0.10, -0.05] | -0.20 [-0.24, -0.16] | 0.13 [0.10, 0.16] | mixed |
| animals/xlang | recall | 180 | 0.48 [0.41, 0.55] | 0.52 [0.28, 0.75] | 0.07 [-0.09, 0.17] | 0.45 [0.28, 0.64] | through |
| animals/xlang | lookup | 378 | 0.78 [0.74, 0.82] | -0.04 [-0.07, -0.01] | -0.11 [-0.15, -0.07] | 0.07 [0.04, 0.10] | around |
| elements/same | recall | 400 | 0.46 [0.41, 0.51] | 0.59 [0.43, 0.74] | -0.04 [-0.08, 0.02] | 0.63 [0.46, 0.80] | through |
| elements/same | lookup | 395 | 0.54 [0.49, 0.59] | -0.07 [-0.10, -0.04] | -0.13 [-0.17, -0.08] | 0.06 [0.01, 0.10] | around |
| elements/syn | recall | 398 | 0.83 [0.79, 0.87] | 0.80 [0.55, 0.97] | -0.08 [-0.11, -0.05] | 0.88 [0.63, 1.07] | through |
| elements/syn | lookup | 380 | 0.62 [0.57, 0.67] | -0.01 [-0.03, 0.01] | -0.11 [-0.16, -0.07] | 0.11 [0.06, 0.15] | mixed |

## The graded rules (lookup)

| domain | difference | value | reading |
|---|---|---|---|
| animals | excess (xlang) - excess (same) | -0.06 [-0.08, -0.04] | does not need a verbatim match |
| elements | excess (syn) - excess (same) | 0.05 [-0.01, 0.10] | fails: the method may not see a lookup that needs J++ |

## Every entity (the unit; X4.md)

| domain | entity | n verbatim | n alias | excess verbatim | excess alias | D |
|---|---|---|---|---|---|---|
| animals | cat | 49 | 47 | 0.09 | 0.03 | -0.07 |
| animals | chicken | 46 | 44 | 0.09 | 0.05 | -0.04 |
| animals | cow | 46 | 42 | 0.22 | 0.16 | -0.07 |
| animals | dog | 40 | 37 | 0.14 | 0.07 | -0.07 |
| animals | duck | 49 | 49 | 0.06 | 0.03 | -0.03 |
| animals | horse | 56 | 55 | 0.11 | 0.06 | -0.04 |
| animals | mouse | 43 | 46 | 0.20 | 0.12 | -0.07 |
| animals | pig | 59 | 58 | 0.15 | 0.05 | -0.10 |
| elements | carbon | 65 | 62 | 0.15 | 0.15 | 0.01 |
| elements | helium | 75 | 71 | 0.11 | 0.04 | -0.07 |
| elements | hydrogen | 52 | 47 | -0.07 | 0.03 | 0.10 |
| elements | lithium | 66 | 66 | 0.05 | 0.18 | 0.13 |
| elements | nitrogen | 62 | 60 | 0.03 | 0.06 | 0.03 |
| elements | oxygen | 75 | 74 | 0.05 | 0.17 | 0.13 |

- animals: D > 0 for 0 of 8 entities; the entity-bootstrap interval -0.06 [-0.08, -0.04] is unreliable with 8 clusters (fewer than 10); a bootstrap over scenes, within these entities only: -0.06 [-0.12, 0.00].
- elements: D > 0 for 5 of 6 entities; the entity-bootstrap interval 0.05 [-0.01, 0.10] is unreliable with 6 clusters (fewer than 10); a bootstrap over scenes, within these entities only: 0.05 [-0.02, 0.12].

## C = recall excess - lookup excess, on items eligible for both readers

| form | n | C |
|---|---|---|
| animals/same | 176 | 0.35 [0.13, 0.51] |
| animals/xlang | 168 | 0.36 [0.20, 0.52] |
| elements/same | 395 | 0.57 [0.38, 0.72] |
| elements/syn | 378 | 0.76 [0.54, 0.96] |
