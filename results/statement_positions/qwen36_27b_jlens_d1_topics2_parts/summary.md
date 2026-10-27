# statement_positions / qwen36_27b_jlens_d1_topics2_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [32, 36, 40] | 180 | 60% / 64% | 4.9% / 0% | 57% | 1.8% | 0.75 [0.65, 0.87] | 0.24 [0.19, 0.29] | around (outside) |
| PP/context/secondary | [32, 36, 40] | 180 | 60% / 64% | 4.9% / 0% | 57% | 1.8% | 0.75 [0.65, 0.87] | 0.24 [0.19, 0.29] | around (outside) |
| PM/bind_bridge/primary | [32] | 180 | 77% / 78% | 23.6% / 18% | 46% | 2.7% | 1.97 [1.70, 2.25] | 0.15 [0.11, 0.18] | inside (inconclusive) |
| PM/bind_bridge/secondary | [32] | 180 | 77% / 78% | 23.6% / 18% | 46% | 2.7% | 1.97 [1.70, 2.25] | 0.15 [0.11, 0.18] | inside (inconclusive) |
| PM/bridge_word/primary | [32] | 180 | 74% / 74% | 23.3% / 18% | 44% | 2.7% | 1.75 [1.52, 2.00] | 0.15 [0.11, 0.19] | inside (outside) |
| PM/bridge_word/secondary | [32] | 180 | 74% / 74% | 23.3% / 18% | 44% | 2.7% | 1.75 [1.52, 2.00] | 0.15 [0.11, 0.19] | inside (outside) |
| PM/context/primary | [32, 36] | 180 | 66% / 66% | 17.3% / 11% | 50% | 2.4% | 2.47 [2.11, 2.85] | 0.16 [0.12, 0.20] | inside (inside) |
| PM/context/secondary | [32, 36] | 180 | 66% / 66% | 17.3% / 11% | 50% | 2.4% | 2.47 [2.11, 2.85] | 0.16 [0.12, 0.20] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/context": {"layers": [32, 36], "concentration_diff": [1.5872227878844445, 1.2132291919796823, 1.9823233253826256], "same_patch_max_share_diff": 0.0}}
Chance share: 0.0661
