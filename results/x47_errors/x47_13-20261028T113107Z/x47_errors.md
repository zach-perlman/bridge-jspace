# 47.13: does the address probe predict the lookup's errors?

Batch 47, test 47.13 (jobs/c3/batch47.yaml, amendment 4; Q47.13, Dan: 65%). Unedited scenes where the lookup answers wrong, from the varied-scene runs (x0b_v2; the d1 sets hold almost no lookup errors, see the script's docstring); the slot probe trained on the scenes the lookup gets right (per format and locker order, the wrong item's entity held out) against the slot of the wrong answer; the lens's top item at the bridge word from the gpu stage. Cluster bootstrap over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): "The address predicts the error" if the probe's slot matches the wrong answer's slot in >= 0.5 of wrong items (chance ~ 0.33 with three lockers; the layout baseline beside), and the lens's top item at the bridge word is still the right item in >= 0.8 of those.

| model | run | status | wrong items (with a slot / with a probe; entities) | chance | probe matches the wrong slot | majority | layout | structure | probe = gold slot | lens top item right: matched / all | holds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x47_errors | scored | 100 (91 / 100; 40) | 0.20 | 0.07 [0.02, 0.12] | 0.23 [0.16, 0.30] | 0.16 [0.08, 0.24] | 0.18 [0.10, 0.26] | 0.61 [0.52, 0.69] | 1.00 [1.00, 1.00] / 0.97 [0.93, 1.00] | no () |
| qwen3.6-27b | x47_errors_27b | not tested | 5 (5 / 5; 5) | 0.14 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.20 [0.00, 0.60] | - / 1.00 [1.00, 1.00] | no (5 wrong items, fewer than 30) |
| muse-glimmer-30b | muse30_x47_errors | pending | 32 (32 / 32; 25) | 0.20 | 0.06 [0.00, 0.16] | 0.16 [0.03, 0.29] | 0.03 [0.00, 0.09] | 0.03 [0.00, 0.10] | 0.50 [0.33, 0.65] | - | no (no lens row (the gpu stage has not landed, or no matched item has one)) |

Over the wrong items that have a slot (a locker statement states the answered digit):

| model | n | probe | majority | layout | structure |
|---|---|---|---|---|---|
| qwen3.5-9b | 91 | 0.08 [0.02, 0.14] | 0.25 [0.17, 0.33] | 0.18 [0.09, 0.26] | 0.20 [0.11, 0.29] |
| qwen3.6-27b | 5 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 32 | 0.06 [0.00, 0.16] | 0.16 [0.03, 0.29] | 0.03 [0.00, 0.09] | 0.03 [0.00, 0.10] |

By format and by locker order (descriptive):

| model | split | n | probe matches the wrong slot | majority | layout | probe = gold slot |
|---|---|---|---|---|---|---|
| qwen3.5-9b | json | 29 | 0.03 [0.00, 0.11] | 0.34 [0.14, 0.54] | 0.38 [0.15, 0.59] | 0.69 [0.56, 0.83] |
| qwen3.5-9b | prose | 35 | 0.03 [0.00, 0.10] | 0.03 [0.00, 0.10] | 0.03 [0.00, 0.10] | 0.60 [0.41, 0.76] |
| qwen3.5-9b | table | 36 | 0.14 [0.05, 0.26] | 0.33 [0.21, 0.46] | 0.11 [0.00, 0.23] | 0.56 [0.37, 0.72] |
| qwen3.5-9b | after | 46 | 0.15 [0.04, 0.29] | 0.13 [0.05, 0.22] | 0.09 [0.02, 0.17] | 0.30 [0.16, 0.46] |
| qwen3.5-9b | before | 54 | 0.00 [0.00, 0.00] | 0.31 [0.19, 0.45] | 0.22 [0.10, 0.35] | 0.87 [0.80, 0.94] |
| qwen3.6-27b | json | 2 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | table | 3 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.33 [0.00, 1.00] |
| qwen3.6-27b | after | 1 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | before | 4 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.25 [0.00, 0.75] |
| muse-glimmer-30b | json | 3 | 0.00 [0.00, 0.00] | 0.67 [0.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | prose | 22 | 0.05 [0.00, 0.13] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.50 [0.32, 0.68] |
| muse-glimmer-30b | table | 7 | 0.14 [0.00, 0.50] | 0.43 [0.14, 0.71] | 0.14 [0.00, 0.50] | 0.71 [0.33, 1.00] |
| muse-glimmer-30b | after | 16 | 0.06 [0.00, 0.20] | 0.06 [0.00, 0.20] | 0.00 [0.00, 0.00] | 0.31 [0.12, 0.53] |
| muse-glimmer-30b | before | 16 | 0.06 [0.00, 0.22] | 0.25 [0.00, 0.45] | 0.06 [0.00, 0.16] | 0.69 [0.43, 0.88] |

The probe on the right scenes (entity-held-out CV accuracy per group; descriptive):

| model | format | order | right scenes | entities | wrong items | probe | CV accuracy | majority share |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | json | after | 61 | 21 | 8 | yes | 0.05 | 0.16 |
| qwen3.5-9b | json | before | 220 | 29 | 21 | yes | 0.72 | 0.26 |
| qwen3.5-9b | prose | after | 234 | 48 | 17 | yes | 0.32 | 0.29 |
| qwen3.5-9b | prose | before | 696 | 59 | 18 | yes | 0.70 | 0.34 |
| qwen3.5-9b | table | after | 222 | 51 | 21 | yes | 0.30 | 0.25 |
| qwen3.5-9b | table | before | 722 | 60 | 15 | yes | 0.81 | 0.22 |
| qwen3.6-27b | json | before | 239 | 29 | 2 | yes | 0.79 | 0.24 |
| qwen3.6-27b | table | after | 243 | 51 | 1 | yes | 0.21 | 0.25 |
| qwen3.6-27b | table | before | 735 | 60 | 2 | yes | 0.89 | 0.22 |
| muse-glimmer-30b | json | after | 86 | 25 | 1 | yes | 0.20 | 0.20 |
| muse-glimmer-30b | json | before | 299 | 32 | 2 | yes | 0.73 | 0.23 |
| muse-glimmer-30b | prose | after | 266 | 53 | 15 | yes | 0.30 | 0.30 |
| muse-glimmer-30b | prose | before | 776 | 63 | 7 | yes | 0.71 | 0.35 |
| muse-glimmer-30b | table | before | 790 | 63 | 7 | yes | 0.82 | 0.22 |
