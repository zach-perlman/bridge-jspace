# X4 verdict: qwen35_9b_x4_patch (qwen3.5-9b, layer 12)

jobs/c3/X4.md section 2. J++ k = 25 against a random part of its share; bootstrap over bridge entities (10000 resamples, seed 0), the same draws for both forms of a domain. UNVERIFIED.

## Gate (unedited org accuracy, decisive read, >= 0.80 per form and reader)

| form / reader | cases | accuracy | pass | eligible |
|---|---|---|---|---|
| animals/same/PP | 400 | 1.00 | True | 400 |
| animals/same/PM | 400 | 0.98 | True | 179 |
| animals/xlang/PP | 400 | 0.97 | True | 377 |
| animals/xlang/PM | 400 | 1.00 | True | 180 |
| elements/same/PP | 400 | 1.00 | True | 398 |
| elements/same/PM | 400 | 1.00 | True | 400 |
| elements/syn/PP | 400 | 0.94 | True | 341 |
| elements/syn/PM | 400 | 0.99 | True | 395 |

## Cells per form and reader (each reader on its own eligible items; the recall's rows are a stability check, X4.md)

| form | reader | n | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|
| animals/same | recall | 179 | 1.00 [0.98, 1.00] | 0.05 [0.00, 0.11] | 0.01 [0.00, 0.01] | 0.04 [0.00, 0.09] | around |
| animals/same | lookup | 400 | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.01] | -0.01 [-0.01, -0.00] | around |
| animals/xlang | recall | 180 | 0.99 [0.97, 1.00] | 0.21 [0.11, 0.36] | 0.01 [-0.02, 0.03] | 0.20 [0.11, 0.34] | mixed |
| animals/xlang | lookup | 377 | 0.99 [0.97, 0.99] | 0.01 [-0.01, 0.02] | 0.03 [0.01, 0.07] | -0.03 [-0.06, -0.01] | around |
| elements/same | recall | 400 | 0.99 [0.98, 1.00] | 0.23 [0.08, 0.37] | 0.01 [0.00, 0.01] | 0.23 [0.08, 0.37] | mixed |
| elements/same | lookup | 398 | 0.99 [0.98, 1.00] | 0.00 [-0.01, 0.01] | 0.02 [0.01, 0.04] | -0.02 [-0.03, -0.01] | around |
| elements/syn | recall | 395 | 0.99 [0.98, 1.00] | 0.72 [0.53, 0.89] | 0.00 [-0.01, 0.01] | 0.72 [0.54, 0.89] | through |
| elements/syn | lookup | 341 | 0.99 [0.98, 1.00] | 0.01 [-0.01, 0.03] | 0.08 [0.05, 0.10] | -0.07 [-0.09, -0.05] | around |

## The graded rules (lookup)

| domain | difference | value | reading |
|---|---|---|---|
| animals | excess (xlang) - excess (same) | -0.02 [-0.05, -0.00] | does not need a verbatim match |
| elements | excess (syn) - excess (same) | -0.05 [-0.08, -0.02] | fails: the method may not see a lookup that needs J++ |

## Every entity (the unit; X4.md)

| domain | entity | n verbatim | n alias | excess verbatim | excess alias | D |
|---|---|---|---|---|---|---|
| animals | cat | 50 | 48 | 0.00 | -0.02 | -0.02 |
| animals | chicken | 46 | 44 | 0.00 | -0.02 | -0.02 |
| animals | cow | 47 | 44 | 0.00 | -0.11 | -0.11 |
| animals | dog | 41 | 39 | 0.00 | -0.03 | -0.03 |
| animals | duck | 49 | 45 | 0.00 | -0.02 | -0.02 |
| animals | horse | 57 | 53 | -0.02 | -0.04 | -0.02 |
| animals | mouse | 48 | 45 | -0.02 | 0.00 | 0.02 |
| animals | pig | 62 | 59 | -0.02 | 0.00 | 0.02 |
| elements | carbon | 65 | 62 | -0.03 | -0.05 | -0.02 |
| elements | helium | 75 | 60 | -0.03 | -0.08 | -0.06 |
| elements | hydrogen | 51 | 40 | 0.00 | -0.12 | -0.12 |
| elements | lithium | 67 | 59 | 0.00 | -0.04 | -0.04 |
| elements | nitrogen | 64 | 57 | -0.02 | -0.09 | -0.07 |
| elements | oxygen | 76 | 63 | -0.04 | -0.05 | -0.01 |

- animals: D > 0 for 2 of 8 entities; the entity-bootstrap interval -0.02 [-0.05, -0.00] is unreliable with 8 clusters (fewer than 10); a bootstrap over scenes, within these entities only: -0.02 [-0.04, -0.00].
- elements: D > 0 for 0 of 6 entities; the entity-bootstrap interval -0.05 [-0.08, -0.02] is unreliable with 6 clusters (fewer than 10); a bootstrap over scenes, within these entities only: -0.05 [-0.08, -0.02].

## C = recall excess - lookup excess, on items eligible for both readers

| form | n | C |
|---|---|---|
| animals/same | 179 | 0.05 [0.01, 0.10] |
| animals/xlang | 167 | 0.24 [0.14, 0.38] |
| elements/same | 398 | 0.25 [0.09, 0.40] |
| elements/syn | 340 | 0.78 [0.59, 0.95] |
