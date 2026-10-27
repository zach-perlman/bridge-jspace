# X4 verdict: qwen35_122b_x4_patch (qwen3.5-122b-a10b, layer 33)

jobs/c3/X4.md section 2. J++ k = 25 against a random part of its share; bootstrap over bridge entities (10000 resamples, seed 0), the same draws for both forms of a domain. UNVERIFIED.

## Gate (unedited org accuracy, decisive read, >= 0.80 per form and reader)

| form / reader | cases | accuracy | pass | eligible |
|---|---|---|---|---|
| animals/same/PP | 400 | 0.99 | True | 396 |
| animals/same/PM | 400 | 0.96 | True | 178 |
| animals/xlang/PP | 400 | 0.99 | True | 394 |
| animals/xlang/PM | 400 | 0.98 | True | 179 |
| elements/same/PP | 400 | 1.00 | True | 400 |
| elements/same/PM | 400 | 1.00 | True | 400 |
| elements/syn/PP | 400 | 0.98 | True | 381 |
| elements/syn/PM | 400 | 0.99 | True | 394 |

## Cells per form and reader (each reader on its own eligible items; the recall's rows are a stability check, X4.md)

| form | reader | n | S_whole | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|
| animals/same | recall | 178 | 0.99 [0.96, 1.00] | 0.13 [0.01, 0.23] | 0.06 [0.01, 0.11] | 0.07 [0.01, 0.13] | around |
| animals/same | lookup | 396 | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 0.00 [-0.01, 0.01] | around |
| animals/xlang | recall | 179 | 0.99 [0.97, 1.00] | 0.25 [0.10, 0.36] | 0.04 [-0.00, 0.08] | 0.20 [0.08, 0.28] | mixed |
| animals/xlang | lookup | 394 | 0.99 [0.98, 1.00] | 0.01 [-0.00, 0.02] | 0.01 [0.00, 0.02] | -0.00 [-0.01, 0.00] | around |
| elements/same | recall | 400 | 1.00 [0.99, 1.00] | 0.03 [0.01, 0.06] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.06] | around |
| elements/same | lookup | 400 | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| elements/syn | recall | 394 | 0.99 [0.98, 1.00] | 0.54 [0.38, 0.71] | -0.00 [-0.01, 0.00] | 0.54 [0.39, 0.71] | through |
| elements/syn | lookup | 381 | 0.99 [0.97, 1.00] | 0.08 [0.06, 0.11] | 0.06 [0.04, 0.09] | 0.02 [-0.01, 0.07] | around |

## The graded rules (lookup)

| domain | difference | value | reading |
|---|---|---|---|
| animals | excess (xlang) - excess (same) | -0.00 [-0.01, 0.00] | does not need a verbatim match |
| elements | excess (syn) - excess (same) | 0.02 [-0.01, 0.07] | fails: the method may not see a lookup that needs J++ |

## Every entity (the unit; X4.md)

| domain | entity | n verbatim | n alias | excess verbatim | excess alias | D |
|---|---|---|---|---|---|---|
| animals | cat | 49 | 50 | 0.00 | 0.00 | 0.00 |
| animals | chicken | 45 | 46 | 0.00 | -0.02 | -0.02 |
| animals | cow | 46 | 47 | 0.00 | 0.00 | 0.00 |
| animals | dog | 41 | 39 | 0.02 | 0.00 | -0.02 |
| animals | duck | 49 | 49 | 0.00 | 0.00 | 0.00 |
| animals | horse | 56 | 57 | -0.02 | 0.00 | 0.02 |
| animals | mouse | 48 | 46 | 0.00 | 0.00 | 0.00 |
| animals | pig | 62 | 60 | 0.00 | 0.00 | 0.00 |
| elements | carbon | 65 | 64 | 0.00 | 0.14 | 0.14 |
| elements | helium | 75 | 68 | 0.00 | -0.03 | -0.03 |
| elements | hydrogen | 52 | 47 | 0.00 | 0.00 | 0.00 |
| elements | lithium | 68 | 64 | 0.00 | 0.00 | 0.00 |
| elements | nitrogen | 64 | 62 | 0.00 | 0.00 | 0.00 |
| elements | oxygen | 76 | 76 | 0.00 | 0.03 | 0.03 |

- animals: D > 0 for 1 of 8 entities; the entity-bootstrap interval -0.00 [-0.01, 0.00] is unreliable with 8 clusters (fewer than 10); a bootstrap over scenes, within these entities only: -0.00 [-0.02, 0.01].
- elements: D > 0 for 2 of 6 entities; the entity-bootstrap interval 0.02 [-0.01, 0.07] is unreliable with 6 clusters (fewer than 10); a bootstrap over scenes, within these entities only: 0.02 [-0.00, 0.05].

## C = recall excess - lookup excess, on items eligible for both readers

| form | n | C |
|---|---|---|
| animals/same | 177 | 0.07 [0.01, 0.13] |
| animals/xlang | 178 | 0.21 [0.08, 0.30] |
| elements/same | 400 | 0.03 [0.01, 0.06] |
| elements/syn | 375 | 0.51 [0.39, 0.64] |
