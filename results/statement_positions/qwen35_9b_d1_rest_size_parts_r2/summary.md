# statement_positions / qwen35_9b_d1_rest_size_parts_r2

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"context": "around", "bind_bridge": "around"}, "positive_control": {"context": "inside", "bind_bridge": "inside"}, "jspace_half": "H-around"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [16, 18] | 180 | 54% / 55% | 3.5% / 0% | 51% | 7.5% | 0.41 [0.33, 0.50] | 0.76 [0.66, 0.87] | around (outside) |
| PP/context/secondary | [16, 18] | 180 | 54% / 55% | 3.5% / 0% | 51% | 7.5% | 0.41 [0.33, 0.50] | 0.76 [0.66, 0.87] | around (outside) |
| PP/bind_bridge/primary | [16] | 180 | 24% / 19% | 2.3% / 0% | 23% | 4.8% | 0.52 [0.38, 0.65] | 0.82 [0.66, 1.00] | around (outside) |
| PP/bind_bridge/secondary | [16] | 180 | 24% / 19% | 2.3% / 0% | 23% | 4.8% | 0.52 [0.38, 0.65] | 0.82 [0.66, 1.00] | around (outside) |
| PM/context/primary | [16, 18] | 180 | 62% / 63% | 53.0% / 51% | 25% | 10.6% | 5.49 [5.07, 5.96] | 0.32 [0.26, 0.39] | inside (inside) |
| PM/context/secondary | [16, 18] | 180 | 62% / 63% | 53.0% / 51% | 25% | 10.6% | 5.49 [5.07, 5.96] | 0.32 [0.26, 0.39] | inside (inside) |
| PM/bind_bridge/primary | [16] | 180 | 66% / 64% | 60.8% / 57% | 17% | 8.6% | 3.67 [3.41, 3.99] | 0.24 [0.19, 0.30] | inside (inside) |
| PM/bind_bridge/secondary | [16] | 180 | 66% / 64% | 60.8% / 57% | 17% | 8.6% | 3.67 [3.41, 3.99] | 0.24 [0.19, 0.30] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [16], "concentration_diff": [3.1528414386832844, 2.859503516961881, 3.48305064924196], "same_patch_max_share_diff": 0.0}, "PM-PP/context": {"layers": [16, 18], "concentration_diff": [5.079582617304121, 4.639376910695487, 5.549878598631459], "same_patch_max_share_diff": 0.0}}
Chance share: 0.08745
