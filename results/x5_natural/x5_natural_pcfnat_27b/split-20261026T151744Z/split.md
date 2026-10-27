# x5_natural_pcfnat_27b: the pointer directions: extra loss by where the answer's fact sentence sits (descriptive, after the data)

Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| split | group | n | lookup switches (whole change) | lookup extra loss | recall switches | recall extra loss |
|---|---|---|---|---|---|---|
| all | all | 137 | 59 | 0.08 [0.00, 0.18] | 126 | 0.02 [-0.03, 0.07] |
| original's fact sentence vs the bridge's mention | after | 62 | 5 | 0.20 [0.00, 0.67] | 56 | 0.00 [0.00, 0.00] |
| original's fact sentence vs the bridge's mention | before | 75 | 54 | 0.07 [0.00, 0.17] | 70 | 0.04 [-0.05, 0.12] |
| both fact sentences | both fact sentences before | 46 | 36 | 0.11 [0.02, 0.24] | 43 | 0.07 [-0.07, 0.20] |
| both fact sentences | only the original's before | 29 | 18 | 0.00 [-0.18, 0.15] | 27 | 0.00 [0.00, 0.00] |
| both fact sentences | the original's fact sentence after the bridge's mention | 62 | 5 | 0.20 [0.00, 0.67] | 56 | 0.00 [0.00, 0.00] |

Extra loss is a share of the whole change's switches; where the lookup switches only a few times, its interval is wide and can leave [-1, 1].
