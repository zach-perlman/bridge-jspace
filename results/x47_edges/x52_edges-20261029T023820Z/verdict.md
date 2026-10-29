# 47.6: where is the pointer formed? (edge knock-outs)

Batch 47, test 47.6 (jobs/c3/batch47.yaml; batch 52 C coverage, no prediction: coverage run on an already-scored rule; rule first scored in results/x47_edges/x47_6-20261028T113107Z). Routes C2 scenes with the filler sentence first; L = the layer fixed in advance; cluster bootstrap over bridge items (10000, seed 0); point estimates decide. Part (c) was dropped by Dan (amendment 1) before any run. UNVERIFIED.

**Formation** (block/sentence/all: the pick sentence cannot read the locker sentences at 0..L, both forwards that form the change): does not hold (holds on none).

## qwen3.6-27b (L32, n = 300 items, 32 bridge items)

(b) routes (lookup) and the recall's switch per arm; the routes runs' whole-change position share was 0.34.

| arm | identity | position | value | original | other | recall switch |
|---|---|---|---|---|---|---|
| unedited | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| none | 0.70 [0.65, 0.75] | 0.28 [0.23, 0.33] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.50 [0.41, 0.59] |
| block/sentence/all | 0.41 [0.37, 0.44] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.56 [0.53, 0.60] | 0.00 [0.00, 0.00] | 0.28 [0.20, 0.37] |
| control/sentence/all | 0.70 [0.65, 0.75] | 0.29 [0.24, 0.34] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.49 [0.40, 0.59] |
| block/sentence/attn | 0.51 [0.46, 0.56] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.44 [0.39, 0.49] | 0.00 [0.00, 0.01] | 0.34 [0.25, 0.44] |
| control/sentence/attn | 0.70 [0.66, 0.75] | 0.28 [0.24, 0.33] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.51 [0.42, 0.60] |
| block/bridge/all | 0.41 [0.37, 0.45] | 0.04 [0.02, 0.05] | 0.00 [0.00, 0.00] | 0.55 [0.51, 0.59] | 0.00 [0.00, 0.00] | 0.26 [0.17, 0.35] |
| control/bridge/all | 0.70 [0.65, 0.75] | 0.29 [0.24, 0.34] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.49 [0.40, 0.58] |
| block/bridge/attn | 0.51 [0.45, 0.57] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.45 [0.39, 0.50] | 0.00 [0.00, 0.01] | 0.35 [0.26, 0.44] |
| control/bridge/attn | 0.70 [0.65, 0.75] | 0.28 [0.23, 0.33] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.50 [0.41, 0.59] |

Each arm minus none (paired): position, identity, recall switch.

| arm | position | identity | recall switch |
|---|---|---|---|
| block/sentence/all | -0.25 [-0.30, -0.21] | -0.30 [-0.34, -0.24] | -0.22 [-0.27, -0.17] |
| control/sentence/all | 0.01 [0.00, 0.02] | -0.01 [-0.02, 0.00] | -0.01 [-0.02, 0.00] |
| block/sentence/attn | -0.24 [-0.30, -0.19] | -0.19 [-0.25, -0.13] | -0.16 [-0.21, -0.11] |
| control/sentence/attn | 0.00 [-0.01, 0.01] | 0.00 [-0.01, 0.01] | 0.01 [0.00, 0.02] |
| block/bridge/all | -0.25 [-0.30, -0.20] | -0.29 [-0.34, -0.24] | -0.24 [-0.30, -0.20] |
| control/bridge/all | 0.00 [-0.01, 0.01] | -0.00 [-0.01, 0.01] | -0.01 [-0.02, 0.00] |
| block/bridge/attn | -0.25 [-0.30, -0.20] | -0.19 [-0.26, -0.12] | -0.15 [-0.21, -0.10] |
| control/bridge/attn | 0.00 [-0.01, 0.01] | 0.00 [-0.01, 0.01] | -0.00 [-0.01, 0.01] |

Medians of the change at the bridge word per arm: norm, share in U, cosine with none's.

| arm | norm | share in U | cos with none |
|---|---|---|---|
| none | 55.69 | 0.121 | 1.000 |
| block/sentence/all | 53.97 | 0.004 | 0.404 |
| control/sentence/all | 54.00 | 0.122 | 0.991 |
| block/sentence/attn | 49.81 | 0.005 | 0.484 |
| control/sentence/attn | 55.55 | 0.122 | 0.997 |
| block/bridge/all | 49.69 | 0.004 | 0.428 |
| control/bridge/all | 54.95 | 0.120 | 0.994 |
| block/bridge/attn | 49.79 | 0.005 | 0.493 |
| control/bridge/attn | 55.85 | 0.122 | 0.998 |

Formation clauses: position_fell yes, identity_within no, recall_within no, control_position_within yes, control_identity_within yes, control_recall_within yes -> **does not hold**.

Edges per arm (item 0; every item the same: yes): (b) block/sentence/all 4455; (b) control/sentence/all 4455; (b) block/sentence/attn 1080; (b) control/sentence/attn 1080; (b) block/bridge/all 891; (b) control/bridge/all 891; (b) block/bridge/attn 216; (b) control/bridge/attn 216.

## (a) attention from the last token to the locker sentences (descriptive)

### qwen3.6-27b (L32, n = 300)

| arm | identity | position | value | original | other |
|---|---|---|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| whole | 0.65 [0.60, 0.70] | 0.34 [0.29, 0.39] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] |
| no_U | 0.72 [0.68, 0.77] | 0.06 [0.03, 0.08] | 0.00 [0.00, 0.00] | 0.22 [0.18, 0.25] | 0.00 [0.00, 0.01] |
| no_U_rand | 0.69 [0.64, 0.75] | 0.25 [0.20, 0.31] | 0.00 [0.00, 0.00] | 0.05 [0.03, 0.07] | 0.00 [0.00, 0.01] |
| write1 | 0.19 [0.14, 0.25] | 0.22 [0.17, 0.28] | 0.00 [0.00, 0.00] | 0.58 [0.52, 0.65] | 0.00 [0.00, 0.00] |
| write2 | 0.08 [0.05, 0.11] | 0.08 [0.05, 0.12] | 0.00 [0.00, 0.00] | 0.84 [0.79, 0.89] | 0.00 [0.00, 0.00] |
| rand1 | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] |
| rand2 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |

Heads whose largest locker mass is most often on the answered locker under the whole change, on the items whose answer left A's locker; the same head's rate per arm (chance 1/3):

| layer | head | none | whole | no_U | no_U_rand | write1 | write2 | rand1 | rand2 |
|---|---|---|---|---|---|---|---|---|---|
| 59 | 3 | - | 0.966 | 0.957 | 0.954 | 0.904 | 0.896 | 0.5 | 1.0 |
| 59 | 1 | - | 0.956 | 0.949 | 0.923 | 0.76 | 0.812 | 0.5 | 1.0 |
| 59 | 21 | - | 0.94 | 0.906 | 0.944 | 0.92 | 0.792 | 1.0 | 1.0 |
| 51 | 22 | - | 0.933 | 0.936 | 0.937 | 0.8 | 0.979 | 0.5 | 1.0 |
| 51 | 20 | - | 0.933 | 0.915 | 0.947 | 0.824 | 0.938 | 0.5 | 1.0 |
| 59 | 4 | - | 0.93 | 0.902 | 0.908 | 0.776 | 0.833 | 0.5 | 1.0 |
| 51 | 6 | - | 0.872 | 0.923 | 0.852 | 0.632 | 0.958 | 0.5 | 1.0 |
| 55 | 14 | - | 0.866 | 0.859 | 0.81 | 0.656 | 0.875 | 0.5 | 1.0 |
| 55 | 23 | - | 0.862 | 0.868 | 0.835 | 0.52 | 0.729 | 0.5 | 1.0 |
| 51 | 23 | - | 0.859 | 0.897 | 0.856 | 0.656 | 0.958 | 0.5 | 1.0 |

