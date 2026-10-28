# 47.6: where is the pointer formed? (edge knock-outs)

Batch 47, test 47.6 (jobs/c3/batch47.yaml; Q47.6, Dan: yes · 60%; no · 40%). Routes C2 scenes with the filler sentence first; L = the layer fixed in advance; cluster bootstrap over bridge items (10000, seed 0); point estimates decide. Part (c) was dropped by Dan (amendment 1) before any run. UNVERIFIED.

**Formation** (block/sentence/all: the pick sentence cannot read the locker sentences at 0..L, both forwards that form the change): does not hold (holds on none).

## muse-glimmer-30b (L26, n = 300 items, 32 bridge items)

(b) routes (lookup) and the recall's switch per arm; the routes runs' whole-change position share was 0.54.

| arm | identity | position | value | original | other | recall switch |
|---|---|---|---|---|---|---|
| unedited | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| none | 0.41 [0.37, 0.46] | 0.56 [0.51, 0.61] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.40 [0.34, 0.46] |
| block/sentence/all | 0.16 [0.13, 0.20] | 0.17 [0.13, 0.21] | 0.00 [0.00, 0.00] | 0.67 [0.62, 0.71] | 0.00 [0.00, 0.00] | 0.26 [0.20, 0.33] |
| control/sentence/all | 0.42 [0.37, 0.46] | 0.56 [0.52, 0.61] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.38 [0.32, 0.44] |
| block/bridge/all | 0.18 [0.14, 0.23] | 0.17 [0.13, 0.21] | 0.00 [0.00, 0.00] | 0.65 [0.59, 0.70] | 0.00 [0.00, 0.00] | 0.25 [0.19, 0.33] |
| control/bridge/all | 0.42 [0.38, 0.47] | 0.56 [0.51, 0.60] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.37 [0.31, 0.43] |

Each arm minus none (paired): position, identity, recall switch.

| arm | position | identity | recall switch |
|---|---|---|---|
| block/sentence/all | -0.39 [-0.44, -0.33] | -0.25 [-0.31, -0.19] | -0.15 [-0.20, -0.09] |
| control/sentence/all | 0.00 [-0.01, 0.02] | 0.00 [-0.01, 0.02] | -0.02 [-0.04, -0.01] |
| block/bridge/all | -0.39 [-0.44, -0.34] | -0.23 [-0.29, -0.17] | -0.15 [-0.20, -0.09] |
| control/bridge/all | -0.00 [-0.02, 0.01] | 0.01 [0.00, 0.02] | -0.04 [-0.06, -0.02] |

Medians of the change at the bridge word per arm: norm, share in U, cosine with none's.

| arm | norm | share in U | cos with none |
|---|---|---|---|
| none | 165.14 | 0.095 | 1.000 |
| block/sentence/all | 192.78 | 0.010 | 0.475 |
| control/sentence/all | 163.62 | 0.095 | 0.995 |
| block/bridge/all | 198.55 | 0.012 | 0.481 |
| control/bridge/all | 164.02 | 0.096 | 0.997 |

Formation clauses: position_fell no, identity_within no, recall_within no, control_position_within yes, control_identity_within yes, control_recall_within yes -> **does not hold**.

Edges per arm (item 0; every item the same: yes): (b) block/sentence/all 3645; (b) control/sentence/all 3645; (b) block/bridge/all 729; (b) control/bridge/all 729.

## qwen3.5-9b (L12, n = 300 items, 31 bridge items)

(b) routes (lookup) and the recall's switch per arm; the routes runs' whole-change position share was 0.51.

| arm | identity | position | value | original | other | recall switch |
|---|---|---|---|---|---|---|
| unedited | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| none | 0.53 [0.48, 0.58] | 0.44 [0.38, 0.49] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.05] | 0.01 [0.00, 0.02] | 0.92 [0.88, 0.95] |
| block/sentence/all | 0.21 [0.17, 0.25] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.78 [0.73, 0.82] | 0.00 [0.00, 0.00] | 0.68 [0.61, 0.76] |
| control/sentence/all | 0.52 [0.47, 0.56] | 0.45 [0.40, 0.51] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.01 [0.00, 0.02] | 0.93 [0.89, 0.96] |
| block/sentence/attn | 0.26 [0.21, 0.32] | 0.05 [0.02, 0.07] | 0.00 [0.00, 0.00] | 0.68 [0.63, 0.74] | 0.01 [0.00, 0.02] | 0.75 [0.68, 0.82] |
| control/sentence/attn | 0.51 [0.46, 0.56] | 0.45 [0.39, 0.50] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.05] | 0.01 [0.00, 0.03] | 0.92 [0.89, 0.95] |
| block/bridge/all | 0.21 [0.17, 0.25] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.78 [0.74, 0.82] | 0.00 [0.00, 0.00] | 0.68 [0.61, 0.75] |
| control/bridge/all | 0.52 [0.47, 0.57] | 0.45 [0.39, 0.50] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.05] | 0.01 [0.00, 0.02] | 0.92 [0.89, 0.96] |
| block/bridge/attn | 0.27 [0.21, 0.32] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.68 [0.62, 0.75] | 0.01 [0.00, 0.02] | 0.75 [0.68, 0.82] |
| control/bridge/attn | 0.52 [0.47, 0.57] | 0.45 [0.39, 0.50] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.05] | 0.01 [0.00, 0.02] | 0.92 [0.88, 0.95] |

Each arm minus none (paired): position, identity, recall switch.

| arm | position | identity | recall switch |
|---|---|---|---|
| block/sentence/all | -0.43 [-0.48, -0.37] | -0.32 [-0.37, -0.27] | -0.23 [-0.29, -0.18] |
| control/sentence/all | 0.01 [0.00, 0.03] | -0.01 [-0.03, 0.00] | 0.01 [-0.00, 0.02] |
| block/sentence/attn | -0.39 [-0.45, -0.33] | -0.26 [-0.33, -0.19] | -0.17 [-0.23, -0.12] |
| control/sentence/attn | 0.01 [-0.01, 0.03] | -0.02 [-0.03, -0.00] | 0.00 [-0.01, 0.01] |
| block/bridge/all | -0.43 [-0.48, -0.37] | -0.32 [-0.37, -0.27] | -0.24 [-0.30, -0.18] |
| control/bridge/all | 0.01 [-0.01, 0.02] | -0.01 [-0.02, 0.01] | 0.01 [-0.01, 0.02] |
| block/bridge/attn | -0.40 [-0.46, -0.34] | -0.26 [-0.33, -0.19] | -0.17 [-0.23, -0.11] |
| control/bridge/attn | 0.01 [-0.01, 0.02] | -0.01 [-0.02, 0.01] | 0.00 [-0.01, 0.01] |

Medians of the change at the bridge word per arm: norm, share in U, cosine with none's.

| arm | norm | share in U | cos with none |
|---|---|---|---|
| none | 17.49 | 0.109 | 1.000 |
| block/sentence/all | 20.88 | 0.010 | 0.578 |
| control/sentence/all | 17.02 | 0.112 | 0.990 |
| block/sentence/attn | 20.23 | 0.013 | 0.621 |
| control/sentence/attn | 17.32 | 0.111 | 0.997 |
| block/bridge/all | 20.58 | 0.011 | 0.587 |
| control/bridge/all | 17.31 | 0.110 | 0.993 |
| block/bridge/attn | 20.13 | 0.014 | 0.624 |
| control/bridge/attn | 17.50 | 0.109 | 0.998 |

Formation clauses: position_fell yes, identity_within no, recall_within no, control_position_within yes, control_identity_within yes, control_recall_within yes -> **does not hold**.

Edges per arm (item 0; every item the same: yes): (b) block/sentence/all 1755; (b) control/sentence/all 1755; (b) block/sentence/attn 405; (b) control/sentence/attn 405; (b) block/bridge/all 351; (b) control/bridge/all 351; (b) block/bridge/attn 81; (b) control/bridge/attn 81.

## (a) attention from the last token to the locker sentences (descriptive)

muse-glimmer-30b: pending.

qwen3.5-9b: pending.

