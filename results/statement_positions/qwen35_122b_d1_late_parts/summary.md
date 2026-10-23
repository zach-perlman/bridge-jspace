# statement_positions / qwen35_122b_d1_late_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around", "context": "inconclusive"}, "positive_control": {"bind_bridge": "inside", "context": "inside"}, "jspace_half": "mixed / inconclusive"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [30, 33, 36] | 180 | 52% / 55% | 6.1% / 5% | 38% | 2.5% | 0.57 [0.45, 0.68] | 0.14 [0.03, 0.24] | around (outside) |
| PP/bind_bridge/secondary | [30, 33, 36] | 180 | 52% / 55% | 6.1% / 5% | 38% | 2.5% | 0.57 [0.45, 0.68] | 0.14 [0.03, 0.24] | around (outside) |
| PP/context/primary | [24, 30, 33, 36] | 180 | 91% / 92% | 14.6% / 13% | 79% | 3.7% | 0.95 [0.82, 1.07] | 0.14 [0.08, 0.20] | inconclusive (outside) |
| PP/context/secondary | [24, 30, 33, 36] | 180 | 91% / 92% | 14.6% / 13% | 79% | 3.7% | 0.95 [0.82, 1.07] | 0.14 [0.08, 0.20] | inconclusive (outside) |
| PM/bind_bridge/primary | [30, 33, 36] | 180 | 92% / 91% | 31.8% / 25% | 55% | 6.5% | 1.53 [1.37, 1.68] | 0.17 [0.09, 0.24] | inside (outside) |
| PM/bind_bridge/secondary | [30, 33, 36] | 180 | 92% / 91% | 31.8% / 25% | 55% | 6.5% | 1.53 [1.37, 1.68] | 0.17 [0.09, 0.24] | inside (outside) |
| PM/context/primary | [24, 30, 33, 36] | 180 | 91% / 92% | 30.7% / 24% | 58% | 5.6% | 1.97 [1.76, 2.17] | 0.15 [0.07, 0.22] | inside (inconclusive) |
| PM/context/secondary | [24, 30, 33, 36] | 180 | 91% / 92% | 30.7% / 24% | 58% | 5.6% | 1.97 [1.76, 2.17] | 0.15 [0.07, 0.22] | inside (inconclusive) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [30, 33, 36], "concentration_diff": [0.9625292003921786, 0.7912005283766902, 1.1260641674851057], "same_patch_max_share_diff": 0.02300000000000002}, "PM-PP/context": {"layers": [24, 30, 33, 36], "concentration_diff": [1.0213841320560284, 0.7922879797133289, 1.2521959818038757], "same_patch_max_share_diff": 0.011799999999999977}}
Chance share: 0.1
