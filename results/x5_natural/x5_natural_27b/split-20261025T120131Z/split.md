# x5_natural_27b: J++ extra loss by where the answer's fact sentence sits (descriptive, after the data)

Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| split | group | n | lookup switches (whole change) | lookup extra loss | recall switches | recall extra loss |
|---|---|---|---|---|---|---|
| all | all | 137 | 60 | 0.32 [0.20, 0.45] | 126 | 0.59 [0.50, 0.67] |
| original's fact sentence vs the bridge's mention | after | 62 | 5 | 0.40 [0.00, 1.50] | 56 | 0.66 [0.54, 0.77] |
| original's fact sentence vs the bridge's mention | before | 75 | 55 | 0.31 [0.18, 0.46] | 70 | 0.53 [0.41, 0.65] |
| both fact sentences | both fact sentences before | 46 | 36 | 0.28 [0.12, 0.45] | 43 | 0.44 [0.30, 0.59] |
| both fact sentences | only the original's before | 29 | 19 | 0.37 [0.15, 0.64] | 27 | 0.67 [0.46, 0.84] |
| both fact sentences | the original's fact sentence after the bridge's mention | 62 | 5 | 0.40 [0.00, 1.50] | 56 | 0.66 [0.54, 0.77] |

Extra loss is a share of the whole change's switches; where the lookup switches only a few times, its interval is wide and can leave [-1, 1].
