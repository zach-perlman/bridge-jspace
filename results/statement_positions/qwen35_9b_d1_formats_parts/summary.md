# statement_positions / qwen35_9b_d1_formats_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [16, 18] | 180 | 59% / 59% | 4.1% / 0% | 57% | 10.8% | 0.41 [0.35, 0.46] | 0.92 [0.84, 1.01] | around (outside) |
| PP/context/secondary | [16, 18] | 180 | 59% / 59% | 4.1% / 0% | 57% | 10.8% | 0.41 [0.35, 0.46] | 0.92 [0.84, 1.01] | around (outside) |
| PM/bind_bridge/primary | [16, 18] | 180 | 73% / 72% | 56.5% / 59% | 26% | 17.6% | 2.73 [2.58, 2.89] | 0.42 [0.36, 0.49] | inside (inside) |
| PM/bind_bridge/secondary | [16, 18] | 180 | 73% / 72% | 56.5% / 59% | 26% | 17.6% | 2.73 [2.58, 2.89] | 0.42 [0.36, 0.49] | inside (inside) |
| PM/bridge_word/primary | [16, 18] | 180 | 73% / 73% | 56.2% / 59% | 25% | 17.4% | 2.27 [2.17, 2.38] | 0.43 [0.36, 0.50] | inside (inside) |
| PM/bridge_word/secondary | [16, 18] | 180 | 73% / 73% | 56.2% / 59% | 25% | 17.4% | 2.27 [2.17, 2.38] | 0.43 [0.36, 0.50] | inside (inside) |
| PM/context/primary | [16, 18] | 180 | 64% / 65% | 52.7% / 57% | 28% | 16.5% | 4.80 [4.51, 5.10] | 0.50 [0.42, 0.58] | inside (inside) |
| PM/context/secondary | [16, 18] | 180 | 64% / 65% | 52.7% / 57% | 28% | 16.5% | 4.80 [4.51, 5.10] | 0.50 [0.42, 0.58] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/context": {"layers": [16, 18], "concentration_diff": [4.393496481267489, 4.104858046335907, 4.689443718506161], "same_patch_max_share_diff": 0.004499999999999976}}
Chance share: 0.08745
