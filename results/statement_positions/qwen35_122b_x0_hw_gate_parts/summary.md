# statement_positions / qwen35_122b_x0_hw_gate_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around"}, "positive_control": {"bind_bridge": "inside"}, "jspace_half": "H-around"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [33] | 180 | 49% / 51% | 1.2% / 0% | 42% | 1.6% | 0.13 [0.04, 0.22] | 0.08 [-0.07, 0.22] | around (outside) |
| PP/bind_bridge/secondary | [33] | 180 | 49% / 51% | 1.2% / 0% | 42% | 1.6% | 0.13 [0.04, 0.22] | 0.08 [-0.07, 0.22] | around (outside) |
| PM/bind_bridge/primary | [33] | 180 | 97% / 94% | 31.8% / 26% | 59% | 6.2% | 1.50 [1.33, 1.67] | 0.16 [0.08, 0.23] | inside (outside) |
| PM/bind_bridge/secondary | [33] | 180 | 97% / 94% | 31.8% / 26% | 59% | 6.2% | 1.50 [1.33, 1.67] | 0.16 [0.08, 0.23] | inside (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [33], "concentration_diff": [1.374146689789629, 1.1868495033266762, 1.5530541278762484], "same_patch_max_share_diff": 0.018199999999999994}}
Chance share: 0.1028
