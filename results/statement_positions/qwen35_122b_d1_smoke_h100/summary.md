# statement_positions / qwen35_122b_d1_smoke_h100

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "inconclusive", "context": "inconclusive"}, "positive_control": {"bind_bridge": "inside", "context": "inside"}, "jspace_half": "mixed / inconclusive"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [30] | 180 | 74% / 79% | 16.7% / 15% | 39% | 3.5% | 0.87 [0.69, 1.06] | 0.09 [0.01, 0.17] | inconclusive (outside) |
| PP/bind_bridge/secondary | [30] | 180 | 74% / 79% | 16.7% / 15% | 39% | 3.5% | 0.87 [0.69, 1.06] | 0.09 [0.01, 0.17] | inconclusive (outside) |
| PP/context/primary | [30] | 180 | 98% / 98% | 22.2% / 16% | 82% | 6.2% | 1.14 [0.96, 1.33] | 0.11 [0.04, 0.19] | inconclusive (outside) |
| PP/context/secondary | [30] | 180 | 98% / 98% | 22.2% / 16% | 82% | 6.2% | 1.14 [0.96, 1.33] | 0.11 [0.04, 0.19] | inconclusive (outside) |
| PM/bind_bridge/primary | [30] | 180 | 97% / 94% | 43.0% / 37% | 53% | 7.5% | 1.67 [1.50, 1.85] | 0.13 [0.05, 0.21] | inside (outside) |
| PM/bind_bridge/secondary | [30] | 180 | 97% / 94% | 43.0% / 37% | 53% | 7.5% | 1.67 [1.50, 1.85] | 0.13 [0.05, 0.21] | inside (outside) |
| PM/context/primary | [30] | 180 | 98% / 97% | 36.2% / 29% | 59% | 8.2% | 1.86 [1.63, 2.09] | 0.10 [0.02, 0.17] | inside (inconclusive) |
| PM/context/secondary | [30] | 180 | 98% / 97% | 36.2% / 29% | 59% | 8.2% | 1.86 [1.63, 2.09] | 0.10 [0.02, 0.17] | inside (inconclusive) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [30], "concentration_diff": [0.7970098307274752, 0.6265670872827892, 0.9724333646030417], "same_patch_max_share_diff": 0.02300000000000002}, "PM-PP/context": {"layers": [30], "concentration_diff": [0.7181958137457831, 0.46567856786757955, 0.9585063841724539], "same_patch_max_share_diff": 0.005800000000000027}}
Chance share: 0.0972
