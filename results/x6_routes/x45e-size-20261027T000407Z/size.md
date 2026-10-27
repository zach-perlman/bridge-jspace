# 45e size check (Dan 27 Oct ~01:00; descriptive, after the data)

Conditions (i) and (ii) of 45e (x6_routes.identity_control_flags, unchanged) on all scenes and on the scenes where the wrong-pair control holds at least 0.9 of identity outside J++'s share. Lookup; cluster bootstrap over bridge entities, 10000 resamples, seed 0. n = scenes (bridge entities).

| model | scenes | (i) C0: left without idout + J++ + pointer vs wrong pair + J++ + pointer (n) | (i) holds | (ii) C2: idout's cut minus the wrong pair's (n) | (ii) holds | both |
|---|---|---|---|---|---|---|
| qwen3.5-9b | all | 0.07 [0.04, 0.10] vs 0.15 [0.11, 0.20] (n 300) | yes | 0.06 [0.02, 0.10] (n 300) | no | no |
| qwen3.5-9b | control >= 0.9 | 0.06 [0.03, 0.10] vs 0.16 [0.11, 0.21] (n 241 (31)) | yes | 0.08 [0.03, 0.12] (n 244 (31)) | no | no |
| qwen3.6-27b | all | 0.18 [0.13, 0.23] vs 0.39 [0.34, 0.44] (n 300) | yes | 0.12 [0.08, 0.16] (n 300) | no | no |
| qwen3.6-27b | control >= 0.9 | 0.18 [0.12, 0.24] vs 0.38 [0.32, 0.45] (n 226 (31)) | yes | 0.14 [0.09, 0.21] (n 215 (32)) | no | no |
| muse-glimmer-30b | all | 0.52 [0.47, 0.58] vs 0.57 [0.51, 0.64] (n 290) | no | 0.04 [0.01, 0.07] (n 290) | no | no |
| muse-glimmer-30b | control >= 0.9 | 0.54 [0.48, 0.61] vs 0.59 [0.53, 0.66] (n 237 (31)) | no | 0.05 [0.01, 0.08] (n 231 (31)) | no | no |

Rule (fixed in advance): (i) the first number at most half the second; (ii) at least 0.15; both on at least 2 of 3 models. Q45.7's score stays as computed on all scenes.

## Why the control took zero directions

wrong_pair_basis keeps the number of directions whose share is closest to idout's share, so it takes none exactly when one wrong-pair direction already holds at least twice that share (or the pool has fewer than two entities).

| model | condition | scenes | zero directions | pool sizes (all scenes) | domains (zero-direction scenes) | idout's share, median: zero-direction scenes vs all |
|---|---|---|---|---|---|---|
| qwen3.5-9b | C0 | 300 | 0 | 30 | – | – |
| qwen3.5-9b | C2 | 300 | 1 | 30 | animals | 0.0166 vs 0.1360 |
| qwen3.6-27b | C0 | 300 | 23 | 30 | animals | 0.0037 vs 0.0569 |
| qwen3.6-27b | C2 | 300 | 28 | 30 | animals | 0.0009 vs 0.0591 |
| muse-glimmer-30b | C0 | 290 | 2 | 29 | animals | 0.0004 vs 0.0790 |
| muse-glimmer-30b | C2 | 290 | 5 | 29 | animals | 0.0044 vs 0.0783 |
