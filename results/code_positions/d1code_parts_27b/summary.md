# code_positions / d1code_parts_27b

Claims (J-space half): {"KL": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| KL/bind_bridge/primary | [32, 36, 40] | 80 | 87% / 99% | 2.4% / 0% | 83% | 0.9% | 0.15 [0.13, 0.17] | 0.05 [0.03, 0.06] | around (outside) |
| KL/bind_bridge/secondary | [28, 32, 36, 40] | 80 | 90% / 99% | 2.8% / 0% | 86% | 0.9% | 0.15 [0.14, 0.17] | 0.04 [0.03, 0.06] | around (outside) |
| KL/bridge_word/primary | [32, 36, 40] | 80 | 87% / 99% | 2.4% / 0% | 82% | 0.9% | 0.15 [0.13, 0.16] | 0.05 [0.03, 0.06] | around (outside) |
| KL/bridge_word/secondary | [28, 32, 36, 40] | 80 | 90% / 99% | 2.8% / 0% | 86% | 0.9% | 0.15 [0.13, 0.17] | 0.04 [0.02, 0.05] | around (outside) |
| KL/context/primary | [32, 36, 40] | 80 | 87% / 99% | 2.4% / 0% | 83% | 0.9% | 0.16 [0.14, 0.18] | 0.05 [0.03, 0.06] | around (outside) |
| KL/context/secondary | [28, 32, 36, 40] | 80 | 91% / 99% | 2.8% / 0% | 86% | 0.9% | 0.16 [0.14, 0.18] | 0.04 [0.02, 0.05] | around (outside) |
| KR/bind_bridge/primary | [32, 36, 40] | 80 | 76% / 83% | 16.7% / 7% | 56% | 3.6% | 1.18 [1.06, 1.31] | 0.19 [0.15, 0.24] | inconclusive (outside) |
| KR/bind_bridge/secondary | [28, 32, 36, 40] | 80 | 82% / 88% | 18.9% / 8% | 61% | 3.8% | 1.14 [1.02, 1.27] | 0.17 [0.13, 0.21] | inconclusive (outside) |
| KR/bridge_word/primary | [32, 36, 40] | 80 | 76% / 82% | 16.7% / 6% | 56% | 3.6% | 1.16 [1.04, 1.29] | 0.18 [0.14, 0.23] | inconclusive (outside) |
| KR/bridge_word/secondary | [28, 32, 36, 40] | 80 | 81% / 87% | 18.9% / 8% | 61% | 3.8% | 1.12 [1.00, 1.24] | 0.16 [0.12, 0.20] | inconclusive (outside) |
| KR/context/primary | [32, 36, 40] | 80 | 76% / 84% | 16.7% / 7% | 56% | 3.7% | 1.25 [1.12, 1.39] | 0.19 [0.14, 0.23] | inconclusive (outside) |
| KR/context/secondary | [28, 32, 36, 40] | 80 | 82% / 88% | 18.9% / 8% | 61% | 3.8% | 1.22 [1.08, 1.36] | 0.16 [0.13, 0.21] | inconclusive (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"KR-KL/bind_bridge": {"layers": [32, 36, 40], "concentration_diff": [1.0283535323889408, 0.9038850032318946, 1.1612295863423292], "same_patch_max_share_diff": 0.002899999999999958}, "KR-KL/bridge_word": {"layers": [32, 36, 40], "concentration_diff": [1.0149051752770404, 0.8943245158642171, 1.1447478603598606], "same_patch_max_share_diff": 0.002799999999999997}, "KR-KL/context": {"layers": [32, 36, 40], "concentration_diff": [1.092364415627298, 0.9559520054135656, 1.2393830995041968], "same_patch_max_share_diff": 0.002599999999999991}}
Chance share: 0.0685
