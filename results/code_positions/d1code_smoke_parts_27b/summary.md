# code_positions / d1code_smoke_parts_27b

Claims (J-space half): {"KL": {"statement_verdicts": {"bind_bridge": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| KL/bind_bridge/primary | [32] | 2 | 99% / 100% | 6.8% / 0% | 96% | 0.5% | 0.31 [0.04, 0.55] | -0.05 [-0.15, 0.04] | around (outside) |
| KL/bind_bridge/secondary | [32] | 2 | 99% / 100% | 6.8% / 0% | 96% | 0.5% | 0.31 [0.04, 0.55] | -0.05 [-0.15, 0.04] | around (outside) |
| KL/context/primary | [32] | 2 | 99% / 100% | 6.6% / 0% | 95% | 0.3% | 0.39 [0.03, 0.61] | -0.02 [-0.05, 0.00] | around (outside) |
| KL/context/secondary | [32] | 2 | 99% / 100% | 6.6% / 0% | 95% | 0.3% | 0.39 [0.03, 0.61] | -0.02 [-0.05, 0.00] | around (outside) |
| KR/bind_bridge/primary | [32] | 2 | 99% / 100% | 15.5% / 0% | 77% | 1.8% | 0.72 [0.69, 0.75] | 0.07 [0.07, 0.08] | around (outside) |
| KR/bind_bridge/secondary | [32] | 2 | 99% / 100% | 15.5% / 0% | 77% | 1.8% | 0.72 [0.69, 0.75] | 0.07 [0.07, 0.08] | around (outside) |
| KR/context/primary | [32] | 2 | 100% / 100% | 14.9% / 0% | 77% | 3.0% | 0.87 [0.75, 1.07] | 0.09 [0.08, 0.10] | inconclusive (outside) |
| KR/context/secondary | [32] | 2 | 100% / 100% | 14.9% / 0% | 77% | 3.0% | 0.87 [0.75, 1.07] | 0.09 [0.08, 0.10] | inconclusive (outside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"KR-KL/bind_bridge": {"layers": [32], "concentration_diff": [0.4022398706895177, 0.14222673403055508, 0.7098910270647087], "same_patch_max_share_diff": 0.0}, "KR-KL/context": {"layers": [32], "concentration_diff": [0.4870452515672429, 0.1444064915079465, 1.043845696293732], "same_patch_max_share_diff": 0.0}}
Chance share: 0.066
