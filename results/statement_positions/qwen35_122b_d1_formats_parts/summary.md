# statement_positions / qwen35_122b_d1_formats_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inside"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside", "context": "inside"}, "jspace_half": "H-loc"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [24, 27, 30] | 180 | 86% / 88% | 29.0% / 25% | 24% | 1.6% | 1.23 [1.07, 1.40] | 0.00 [-0.03, 0.04] | inconclusive (inconclusive) |
| PP/bind_bridge/secondary | [24, 27, 30] | 180 | 86% / 88% | 29.0% / 25% | 24% | 1.6% | 1.23 [1.07, 1.40] | 0.00 [-0.03, 0.04] | inconclusive (inconclusive) |
| PP/bridge_word/primary | [24, 27, 30] | 180 | 74% / 74% | 26.5% / 23% | 22% | 1.2% | 1.13 [0.98, 1.29] | 0.01 [-0.03, 0.05] | inconclusive (inconclusive) |
| PP/bridge_word/secondary | [24, 27, 30] | 180 | 74% / 74% | 26.5% / 23% | 22% | 1.2% | 1.13 [0.98, 1.29] | 0.01 [-0.03, 0.05] | inconclusive (inconclusive) |
| PP/context/primary | [24, 27, 30] | 180 | 100% / 100% | 50.9% / 49% | 52% | 2.6% | 2.15 [2.00, 2.31] | 0.02 [-0.02, 0.05] | inside (inside) |
| PP/context/secondary | [24, 27, 30] | 180 | 100% / 100% | 50.9% / 49% | 52% | 2.6% | 2.15 [2.00, 2.31] | 0.02 [-0.02, 0.05] | inside (inside) |
| PM/bind_bridge/primary | [24, 27, 30] | 180 | 95% / 96% | 45.5% / 43% | 39% | 6.4% | 1.74 [1.61, 1.89] | 0.13 [0.07, 0.19] | inside (inconclusive) |
| PM/bind_bridge/secondary | [24, 27, 30] | 180 | 95% / 96% | 45.5% / 43% | 39% | 6.4% | 1.74 [1.61, 1.89] | 0.13 [0.07, 0.19] | inside (inconclusive) |
| PM/bridge_word/primary | [24, 27, 30] | 180 | 91% / 94% | 45.0% / 43% | 38% | 6.7% | 1.57 [1.45, 1.70] | 0.14 [0.08, 0.20] | inside (inconclusive) |
| PM/bridge_word/secondary | [24, 27, 30] | 180 | 91% / 94% | 45.0% / 43% | 38% | 6.7% | 1.57 [1.45, 1.70] | 0.14 [0.08, 0.20] | inside (inconclusive) |
| PM/context/primary | [24, 27, 30] | 180 | 99% / 99% | 52.0% / 51% | 49% | 6.7% | 2.22 [2.07, 2.38] | 0.13 [0.08, 0.19] | inside (inside) |
| PM/context/secondary | [24, 27, 30] | 180 | 99% / 99% | 52.0% / 51% | 49% | 6.7% | 2.22 [2.07, 2.38] | 0.13 [0.08, 0.19] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [24, 27, 30], "concentration_diff": [0.5134257416499985, 0.35838261348656747, 0.6641803007840317], "same_patch_max_share_diff": 0.015899999999999997}, "PM-PP/bridge_word": {"layers": [24, 27, 30], "concentration_diff": [0.43441870526986404, 0.29591623493842395, 0.5761593671110984], "same_patch_max_share_diff": 0.01050000000000001}, "PM-PP/context": {"layers": [24, 27, 30], "concentration_diff": [0.06240420595699936, -0.0642006470393753, 0.18791261678910895], "same_patch_max_share_diff": 0.010499999999999982}}
Chance share: 0.088
