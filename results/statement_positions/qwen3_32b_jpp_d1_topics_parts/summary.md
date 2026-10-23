# statement_positions / qwen3_32b_jpp_d1_topics_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36] | 120 | 72% / 71% | 1.8% / 1% | 47% | 0.1% | 0.15 [0.07, 0.27] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bind_bridge/secondary | [32, 36] | 120 | 72% / 71% | 1.8% / 1% | 47% | 0.1% | 0.15 [0.07, 0.27] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bridge_word/primary | [32] | 120 | 87% / 89% | 3.2% / 2% | 55% | 0.4% | 0.19 [0.07, 0.35] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bridge_word/secondary | [32] | 120 | 87% / 89% | 3.2% / 2% | 55% | 0.4% | 0.19 [0.07, 0.35] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/context/primary | [32, 36, 40] | 120 | 99% / 100% | 3.0% / 2% | 94% | 0.3% | 0.26 [0.14, 0.40] | 0.01 [-0.03, 0.04] | around (outside) |
| PP/context/secondary | [32, 36, 40] | 120 | 99% / 100% | 3.0% / 2% | 94% | 0.3% | 0.26 [0.14, 0.40] | 0.01 [-0.03, 0.04] | around (outside) |
| PM/bind_bridge/primary | [32, 36, 40] | 120 | 86% / 83% | 11.0% / 8% | 66% | 2.3% | 0.86 [0.59, 1.16] | 0.12 [0.04, 0.22] | inconclusive (outside) |
| PM/bind_bridge/secondary | [32, 36, 40] | 120 | 86% / 83% | 11.0% / 8% | 66% | 2.3% | 0.86 [0.59, 1.16] | 0.12 [0.04, 0.22] | inconclusive (outside) |
| PM/bridge_word/primary | [32, 36, 40] | 120 | 84% / 81% | 11.0% / 8% | 65% | 2.1% | 0.78 [0.53, 1.04] | 0.14 [0.06, 0.24] | inconclusive (outside) |
| PM/bridge_word/secondary | [32, 36, 40] | 120 | 84% / 81% | 11.0% / 8% | 65% | 2.1% | 0.78 [0.53, 1.04] | 0.14 [0.06, 0.24] | inconclusive (outside) |
| PM/context/primary | [32, 36, 40] | 120 | 100% / 98% | 11.3% / 8% | 86% | 2.6% | 0.96 [0.67, 1.29] | 0.12 [0.04, 0.23] | inconclusive (outside) |
| PM/context/secondary | [32, 36, 40] | 120 | 100% / 98% | 11.3% / 8% | 86% | 2.6% | 0.96 [0.67, 1.29] | 0.12 [0.04, 0.23] | inconclusive (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [32, 36], "concentration_diff": [0.7671490320409506, 0.47655219086808753, 1.0608215679342061], "same_patch_max_share_diff": 0.0063}, "PM-PP/bridge_word": {"layers": [32], "concentration_diff": [0.48480878425397805, 0.24592810705756904, 0.7360218946997718], "same_patch_max_share_diff": 0.0068000000000000005}, "PM-PP/context": {"layers": [32, 36, 40], "concentration_diff": [0.7057005298685212, 0.40215251583465644, 1.041917647975649], "same_patch_max_share_diff": 0.005700000000000011}}
Chance share: 0.0626
