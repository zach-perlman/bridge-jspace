# muse30b_x5_natural_pcfnat: the pointer directions: extra loss by where the answer's fact sentence sits (descriptive, after the data)

Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| split | group | n | lookup switches (whole change) | lookup extra loss | recall switches | recall extra loss |
|---|---|---|---|---|---|---|
| all | all | 60 | 10 | 0.20 [0.00, 0.50] | 53 | 0.00 [0.00, 0.00] |
| original's fact sentence vs the bridge's mention | after | 32 | 2 | 0.00 [0.00, 0.00] | 28 | 0.00 [0.00, 0.00] |
| original's fact sentence vs the bridge's mention | before | 28 | 8 | 0.25 [0.00, 0.67] | 25 | 0.00 [0.00, 0.00] |
| both fact sentences | both fact sentences before | 16 | 6 | 0.33 [0.00, 0.75] | 13 | 0.00 [0.00, 0.00] |
| both fact sentences | only the original's before | 12 | 2 | 0.00 [0.00, 0.00] | 12 | 0.00 [0.00, 0.00] |
| both fact sentences | the original's fact sentence after the bridge's mention | 32 | 2 | 0.00 [0.00, 0.00] | 28 | 0.00 [0.00, 0.00] |

Extra loss is a share of the whole change's switches; where the lookup switches only a few times, its interval is wide and can leave [-1, 1].
