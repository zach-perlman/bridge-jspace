# qwen35_122b_x5_natural_pcfnat: the pointer directions: extra loss by where the answer's fact sentence sits (descriptive, after the data)

Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| split | group | n | lookup switches (whole change) | lookup extra loss | recall switches | recall extra loss |
|---|---|---|---|---|---|---|
| all | all | 114 | 56 | 0.09 [-0.02, 0.19] | 105 | 0.01 [-0.03, 0.05] |
| original's fact sentence vs the bridge's mention | after | 57 | 10 | 0.10 [0.00, 0.33] | 49 | -0.02 [-0.10, 0.04] |
| original's fact sentence vs the bridge's mention | before | 57 | 46 | 0.09 [-0.02, 0.21] | 56 | 0.04 [0.00, 0.09] |
| both fact sentences | both fact sentences before | 34 | 29 | 0.21 [0.07, 0.39] | 33 | 0.06 [0.00, 0.16] |
| both fact sentences | only the original's before | 23 | 17 | -0.12 [-0.31, 0.00] | 23 | 0.00 [0.00, 0.00] |
| both fact sentences | the original's fact sentence after the bridge's mention | 57 | 10 | 0.10 [0.00, 0.33] | 49 | -0.02 [-0.10, 0.04] |

Extra loss is a share of the whole change's switches; where the lookup switches only a few times, its interval is wide and can leave [-1, 1].
