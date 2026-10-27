# X4 verdict: x4_patch_27b (qwen3.6-27b, layer 32)

jobs/c3/X4.md section 2. J++ k = 25 against a random part of its share; bootstrap over bridge entities (10000 resamples, seed 0), the same draws for both forms of a domain. UNVERIFIED.

## Gate (unedited org accuracy, decisive read, >= 0.80 per form and reader)

| form / reader | cases | accuracy | pass | eligible |
|---|---|---|---|---|
| animals/same/PP | 400 | 0.99 | True | 395 |
| animals/same/PM | 400 | 1.00 | True | 181 |
| animals/xlang/PP | 400 | 0.99 | True | 394 |
| animals/xlang/PM | 400 | 1.00 | True | 181 |
| elements/same/PP | 400 | 1.00 | True | 400 |
| elements/same/PM | 400 | 1.00 | True | 400 |
| elements/syn/PP | 400 | 0.97 | True | 374 |
| elements/syn/PM | 400 | 1.00 | True | 400 |

## Cells per form and reader (each reader on its own eligible items; the recall's rows are a stability check, X4.md)

| form | reader | n | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|
| animals/same | recall | 181 | 0.55 [0.48, 0.62] | 0.61 [0.52, 0.72] | 0.18 [0.09, 0.30] | 0.43 [0.33, 0.52] | through |
| animals/same | lookup | 395 | 0.87 [0.83, 0.90] | -0.06 [-0.09, -0.04] | -0.07 [-0.09, -0.05] | 0.01 [-0.01, 0.03] | around |
| animals/xlang | recall | 181 | 0.71 [0.64, 0.77] | 0.66 [0.52, 0.80] | 0.09 [0.01, 0.17] | 0.56 [0.49, 0.63] | through |
| animals/xlang | lookup | 394 | 0.95 [0.92, 0.97] | -0.01 [-0.02, 0.01] | -0.02 [-0.04, -0.00] | 0.02 [0.00, 0.03] | around |
| elements/same | recall | 400 | 0.85 [0.81, 0.88] | 0.70 [0.59, 0.81] | -0.01 [-0.03, 0.00] | 0.71 [0.60, 0.83] | through |
| elements/same | lookup | 400 | 0.92 [0.89, 0.94] | -0.04 [-0.06, -0.02] | -0.04 [-0.06, -0.03] | 0.00 [-0.01, 0.01] | around |
| elements/syn | recall | 400 | 0.93 [0.90, 0.95] | 0.95 [0.88, 0.99] | -0.03 [-0.05, -0.01] | 0.98 [0.91, 1.03] | through |
| elements/syn | lookup | 374 | 0.84 [0.80, 0.88] | 0.10 [0.06, 0.13] | -0.05 [-0.08, -0.03] | 0.15 [0.11, 0.19] | mixed |

## The graded rules (lookup)

| domain | difference | value | reading |
|---|---|---|---|
| animals | excess (xlang) - excess (same) | 0.01 [-0.01, 0.04] | does not need a verbatim match |
| elements | excess (syn) - excess (same) | 0.15 [0.10, 0.19] | fails: the method may not see a lookup that needs J++ |

## Every entity (the unit; X4.md)

| domain | entity | n verbatim | n alias | excess verbatim | excess alias | D |
|---|---|---|---|---|---|---|
| animals | cat | 50 | 50 | 0.02 | 0.02 | -0.00 |
| animals | chicken | 45 | 46 | -0.02 | 0.07 | 0.09 |
| animals | cow | 47 | 46 | 0.05 | 0.02 | -0.03 |
| animals | dog | 40 | 39 | 0.00 | 0.00 | 0.00 |
| animals | duck | 49 | 49 | -0.02 | -0.02 | 0.00 |
| animals | horse | 55 | 56 | 0.04 | 0.02 | -0.02 |
| animals | mouse | 48 | 48 | 0.00 | 0.00 | 0.00 |
| animals | pig | 61 | 60 | -0.02 | 0.02 | 0.04 |
| elements | carbon | 65 | 65 | -0.02 | 0.14 | 0.15 |
| elements | helium | 75 | 67 | 0.02 | 0.23 | 0.22 |
| elements | hydrogen | 52 | 45 | 0.02 | 0.16 | 0.14 |
| elements | lithium | 68 | 62 | -0.02 | 0.20 | 0.21 |
| elements | nitrogen | 64 | 62 | 0.00 | 0.11 | 0.11 |
| elements | oxygen | 76 | 73 | 0.01 | 0.08 | 0.07 |

- animals: D > 0 for 3 of 8 entities; the entity-bootstrap interval 0.01 [-0.01, 0.04] is unreliable with 8 clusters (fewer than 10); a bootstrap over scenes, within these entities only: 0.01 [-0.01, 0.03].
- elements: D > 0 for 6 of 6 entities; the entity-bootstrap interval 0.15 [0.10, 0.19] is unreliable with 6 clusters (fewer than 10); a bootstrap over scenes, within these entities only: 0.15 [0.10, 0.19].

## C = recall excess - lookup excess, on items eligible for both readers

| form | n | C |
|---|---|---|
| animals/same | 180 | 0.43 [0.32, 0.53] |
| animals/xlang | 180 | 0.54 [0.46, 0.59] |
| elements/same | 400 | 0.71 [0.59, 0.83] |
| elements/syn | 374 | 0.83 [0.71, 0.92] |
