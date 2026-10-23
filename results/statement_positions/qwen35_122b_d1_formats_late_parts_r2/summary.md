# statement_positions / qwen35_122b_d1_formats_late_parts_r2

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around", "context": "inconclusive"}, "positive_control": {"bind_bridge": "inconclusive", "context": "inside"}, "jspace_half": "mixed / inconclusive"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [30, 33, 36] | 180 | 57% / 58% | 7.2% / 6% | 40% | 2.1% | 0.55 [0.45, 0.66] | 0.08 [-0.00, 0.16] | around (outside) |
| PP/bind_bridge/secondary | [30, 33, 36] | 180 | 57% / 58% | 7.2% / 6% | 40% | 2.1% | 0.55 [0.45, 0.66] | 0.08 [-0.00, 0.16] | around (outside) |
| PP/context/primary | [24, 30, 33, 36] | 180 | 93% / 94% | 19.7% / 18% | 76% | 2.9% | 1.07 [0.95, 1.19] | 0.09 [0.05, 0.14] | inconclusive (outside) |
| PP/context/secondary | [24, 30, 33, 36] | 180 | 93% / 94% | 19.7% / 18% | 76% | 2.9% | 1.07 [0.95, 1.19] | 0.09 [0.05, 0.14] | inconclusive (outside) |
| PM/bind_bridge/primary | [30, 33, 36] | 180 | 89% / 92% | 27.9% / 22% | 54% | 6.7% | 1.32 [1.18, 1.46] | 0.12 [0.08, 0.17] | inconclusive (outside) |
| PM/bind_bridge/secondary | [30, 33, 36] | 180 | 89% / 92% | 27.9% / 22% | 54% | 6.7% | 1.32 [1.18, 1.46] | 0.12 [0.08, 0.17] | inconclusive (outside) |
| PM/context/primary | [24, 30, 33, 36] | 180 | 93% / 94% | 32.1% / 27% | 62% | 6.1% | 1.75 [1.59, 1.92] | 0.12 [0.08, 0.17] | inside (outside) |
| PM/context/secondary | [24, 30, 33, 36] | 180 | 93% / 94% | 32.1% / 27% | 62% | 6.1% | 1.75 [1.59, 1.92] | 0.12 [0.08, 0.17] | inside (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [30, 33, 36], "concentration_diff": [0.7664200376790288, 0.6130405493998187, 0.9217735739270613], "same_patch_max_share_diff": 0.01419999999999999}, "PM-PP/context": {"layers": [24, 30, 33, 36], "concentration_diff": [0.6843989790272489, 0.5284410850290173, 0.8369923700539633], "same_patch_max_share_diff": 0.04199999999999998}}
Chance share: 0.1
