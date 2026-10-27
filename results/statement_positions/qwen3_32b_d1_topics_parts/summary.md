# statement_positions / qwen3_32b_d1_topics_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "jspace_half": "H-around but positive control fails (not interpretable)"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36] | 120 | 72% / 71% | 1.5% / 1% | 50% | 0.2% | 0.12 [0.07, 0.17] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bind_bridge/secondary | [32, 36] | 120 | 72% / 71% | 1.5% / 1% | 50% | 0.2% | 0.12 [0.07, 0.17] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bridge_word/primary | [32] | 120 | 87% / 89% | 2.4% / 1% | 56% | 0.5% | 0.13 [0.07, 0.20] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/bridge_word/secondary | [32] | 120 | 87% / 89% | 2.4% / 1% | 56% | 0.5% | 0.13 [0.07, 0.20] | -0.01 [-0.04, 0.02] | around (outside) |
| PP/context/primary | [32, 36, 40] | 120 | 99% / 100% | 1.9% / 1% | 97% | 0.4% | 0.15 [0.07, 0.24] | 0.01 [-0.03, 0.04] | around (outside) |
| PP/context/secondary | [32, 36, 40] | 120 | 99% / 100% | 1.9% / 1% | 97% | 0.4% | 0.15 [0.07, 0.24] | 0.01 [-0.03, 0.04] | around (outside) |
| PM/bind_bridge/primary | [32, 36, 40] | 120 | 86% / 83% | 8.1% / 5% | 72% | 2.7% | 0.58 [0.35, 0.85] | 0.12 [0.04, 0.22] | around (outside) |
| PM/bind_bridge/secondary | [32, 36, 40] | 120 | 86% / 83% | 8.1% / 5% | 72% | 2.7% | 0.58 [0.35, 0.85] | 0.12 [0.04, 0.22] | around (outside) |
| PM/bridge_word/primary | [32, 36, 40] | 120 | 84% / 81% | 8.1% / 5% | 71% | 2.5% | 0.52 [0.31, 0.75] | 0.14 [0.06, 0.24] | around (outside) |
| PM/bridge_word/secondary | [32, 36, 40] | 120 | 84% / 81% | 8.1% / 5% | 71% | 2.5% | 0.52 [0.31, 0.75] | 0.14 [0.06, 0.24] | around (outside) |
| PM/context/primary | [32, 36, 40] | 120 | 100% / 98% | 8.0% / 5% | 92% | 3.1% | 0.65 [0.39, 0.95] | 0.12 [0.04, 0.23] | around (outside) |
| PM/context/secondary | [32, 36, 40] | 120 | 100% / 98% | 8.0% / 5% | 92% | 3.1% | 0.65 [0.39, 0.95] | 0.12 [0.04, 0.23] | around (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [32, 36], "concentration_diff": [0.4420322685781217, 0.2302854747727496, 0.6848019107329159], "same_patch_max_share_diff": 0.008099999999999996}, "PM-PP/bridge_word": {"layers": [32], "concentration_diff": [0.2887993417242718, 0.11411157004516065, 0.4847581671005817], "same_patch_max_share_diff": 0.008799999999999975}, "PM-PP/context": {"layers": [32, 36, 40], "concentration_diff": [0.49467812518404075, 0.24306411447589715, 0.7908506810477602], "same_patch_max_share_diff": 0.005299999999999971}}
Chance share: 0.0531
