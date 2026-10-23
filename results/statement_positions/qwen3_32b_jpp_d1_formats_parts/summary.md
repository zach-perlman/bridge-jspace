# statement_positions / qwen3_32b_jpp_d1_formats_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "jspace_half": "H-around but positive control fails (not interpretable)"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36, 40] | 180 | 70% / 71% | 2.5% / 1% | 45% | 0.5% | 0.21 [0.13, 0.30] | 0.03 [0.01, 0.06] | around (outside) |
| PP/bind_bridge/secondary | [32, 36, 40] | 180 | 70% / 71% | 2.5% / 1% | 45% | 0.5% | 0.21 [0.13, 0.30] | 0.03 [0.01, 0.06] | around (outside) |
| PP/bridge_word/primary | [32, 36] | 180 | 77% / 78% | 3.5% / 2% | 43% | 0.5% | 0.21 [0.13, 0.31] | 0.01 [-0.01, 0.04] | around (outside) |
| PP/bridge_word/secondary | [32, 36] | 180 | 77% / 78% | 3.5% / 2% | 43% | 0.5% | 0.21 [0.13, 0.31] | 0.01 [-0.01, 0.04] | around (outside) |
| PP/context/primary | [32, 36, 40] | 180 | 100% / 100% | 4.2% / 2% | 95% | 0.7% | 0.28 [0.20, 0.37] | 0.04 [0.02, 0.06] | around (outside) |
| PP/context/secondary | [32, 36, 40] | 180 | 100% / 100% | 4.2% / 2% | 95% | 0.7% | 0.28 [0.20, 0.37] | 0.04 [0.02, 0.06] | around (outside) |
| PM/bind_bridge/primary | [32, 36, 40] | 180 | 92% / 90% | 8.8% / 7% | 67% | 1.3% | 0.57 [0.44, 0.71] | 0.06 [0.03, 0.10] | around (outside) |
| PM/bind_bridge/secondary | [32, 36, 40] | 180 | 92% / 90% | 8.8% / 7% | 67% | 1.3% | 0.57 [0.44, 0.71] | 0.06 [0.03, 0.10] | around (outside) |
| PM/bridge_word/primary | [32, 36, 40] | 180 | 91% / 89% | 8.7% / 7% | 66% | 1.5% | 0.51 [0.39, 0.63] | 0.06 [0.03, 0.11] | around (outside) |
| PM/bridge_word/secondary | [32, 36, 40] | 180 | 91% / 89% | 8.7% / 7% | 66% | 1.5% | 0.51 [0.39, 0.63] | 0.06 [0.03, 0.11] | around (outside) |
| PM/context/primary | [32, 36, 40] | 180 | 100% / 100% | 9.7% / 7% | 90% | 1.3% | 0.64 [0.50, 0.79] | 0.05 [0.02, 0.08] | around (outside) |
| PM/context/secondary | [32, 36, 40] | 180 | 100% / 100% | 9.7% / 7% | 90% | 1.3% | 0.64 [0.50, 0.79] | 0.05 [0.02, 0.08] | around (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [32, 36, 40], "concentration_diff": [0.36530776611859184, 0.24773574047432959, 0.4920400080260276], "same_patch_max_share_diff": 0.005399999999999988}, "PM-PP/bridge_word": {"layers": [32, 36], "concentration_diff": [0.3740229032943254, 0.2557056903489468, 0.4976801417441563], "same_patch_max_share_diff": 0.005500000000000005}, "PM-PP/context": {"layers": [32, 36, 40], "concentration_diff": [0.36402578737374836, 0.23657040438547974, 0.4933221371684058], "same_patch_max_share_diff": 0.0032000000000000084}}
Chance share: 0.0626
