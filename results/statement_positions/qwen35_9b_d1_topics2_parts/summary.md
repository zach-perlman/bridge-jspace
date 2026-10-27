# statement_positions / qwen35_9b_d1_topics2_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [16, 18] | 180 | 54% / 54% | 3.5% / 0% | 51% | 7.4% | 0.41 [0.33, 0.50] | 0.77 [0.67, 0.88] | around (outside) |
| PP/context/secondary | [16, 18] | 180 | 54% / 54% | 3.5% / 0% | 51% | 7.4% | 0.41 [0.33, 0.50] | 0.77 [0.67, 0.88] | around (outside) |
| PM/bind_bridge/primary | [16, 18] | 180 | 63% / 61% | 55.7% / 52% | 18% | 10.6% | 3.17 [2.95, 3.43] | 0.29 [0.23, 0.35] | inside (inside) |
| PM/bind_bridge/secondary | [16, 18] | 180 | 63% / 61% | 55.7% / 52% | 18% | 10.6% | 3.17 [2.95, 3.43] | 0.29 [0.23, 0.35] | inside (inside) |
| PM/bridge_word/primary | [16, 18] | 180 | 62% / 60% | 55.5% / 52% | 18% | 10.5% | 2.82 [2.62, 3.04] | 0.29 [0.23, 0.36] | inside (inside) |
| PM/bridge_word/secondary | [16, 18] | 180 | 62% / 60% | 55.5% / 52% | 18% | 10.5% | 2.82 [2.62, 3.04] | 0.29 [0.23, 0.36] | inside (inside) |
| PM/context/primary | [16, 18] | 180 | 62% / 63% | 53.0% / 51% | 25% | 10.6% | 5.49 [5.06, 5.96] | 0.32 [0.26, 0.39] | inside (inside) |
| PM/context/secondary | [16, 18] | 180 | 62% / 63% | 53.0% / 51% | 25% | 10.6% | 5.49 [5.06, 5.96] | 0.32 [0.26, 0.39] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/context": {"layers": [16, 18], "concentration_diff": [5.082942492402322, 4.641139903077955, 5.556948183951761], "same_patch_max_share_diff": 0.0}}
Chance share: 0.08745
