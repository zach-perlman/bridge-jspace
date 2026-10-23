# statement_positions / qwen35_122b_d1_topics2_parts

Claims (J-space half): {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inside"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside", "context": "inside"}, "jspace_half": "H-loc"}}

| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | rand-dict null | verdict (strict) |
|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [24, 27, 30] | 180 | 80% / 84% | 26.3% / 25% | 30% | 2.8% | 1.27 [1.08, 1.45] | 0.07 [0.00, 0.13] | inconclusive (outside) |
| PP/bind_bridge/secondary | [24, 27, 30] | 180 | 80% / 84% | 26.3% / 25% | 30% | 2.8% | 1.27 [1.08, 1.45] | 0.07 [0.00, 0.13] | inconclusive (outside) |
| PP/bridge_word/primary | [24, 27, 30] | 180 | 75% / 79% | 25.8% / 25% | 29% | 2.3% | 1.19 [1.02, 1.36] | 0.08 [0.03, 0.14] | inconclusive (inconclusive) |
| PP/bridge_word/secondary | [24, 27, 30] | 180 | 75% / 79% | 25.8% / 25% | 29% | 2.3% | 1.19 [1.02, 1.36] | 0.08 [0.03, 0.14] | inconclusive (inconclusive) |
| PP/context/primary | [24, 27, 30] | 180 | 99% / 99% | 37.1% / 35% | 68% | 4.2% | 1.90 [1.70, 2.10] | 0.08 [0.03, 0.13] | inside (inconclusive) |
| PP/context/secondary | [24, 27, 30] | 180 | 99% / 99% | 37.1% / 35% | 68% | 4.2% | 1.90 [1.70, 2.10] | 0.08 [0.03, 0.13] | inside (inconclusive) |
| PM/bind_bridge/primary | [24, 27, 30] | 180 | 99% / 95% | 51.9% / 50% | 42% | 6.6% | 2.02 [1.86, 2.18] | 0.12 [0.07, 0.18] | inside (inconclusive) |
| PM/bind_bridge/secondary | [24, 27, 30] | 180 | 99% / 95% | 51.9% / 50% | 42% | 6.6% | 2.02 [1.86, 2.18] | 0.12 [0.07, 0.18] | inside (inconclusive) |
| PM/bridge_word/primary | [24, 27, 30] | 180 | 98% / 94% | 51.8% / 50% | 42% | 6.8% | 1.84 [1.70, 1.98] | 0.13 [0.07, 0.19] | inside (inconclusive) |
| PM/bridge_word/secondary | [24, 27, 30] | 180 | 98% / 94% | 51.8% / 50% | 42% | 6.8% | 1.84 [1.70, 1.98] | 0.13 [0.07, 0.19] | inside (inconclusive) |
| PM/context/primary | [24, 27, 30] | 180 | 99% / 97% | 47.1% / 47% | 47% | 6.9% | 2.43 [2.21, 2.62] | 0.12 [0.04, 0.19] | inside (inside) |
| PM/context/secondary | [24, 27, 30] | 180 | 99% / 97% | 47.1% / 47% | 47% | 6.9% | 2.43 [2.21, 2.62] | 0.12 [0.04, 0.19] | inside (inside) |

Paired readers (concentration difference, recall-used minus lookup-used): {"PM-PP/bind_bridge": {"layers": [24, 27, 30], "concentration_diff": [0.7551569947177863, 0.5946872341998325, 0.9110402173010955], "same_patch_max_share_diff": 0.010399999999999993}, "PM-PP/bridge_word": {"layers": [24, 27, 30], "concentration_diff": [0.6514577408078472, 0.5118777184951832, 0.7935962443869805], "same_patch_max_share_diff": 0.013099999999999973}, "PM-PP/context": {"layers": [24, 27, 30], "concentration_diff": [0.5244594298450256, 0.29737360413882163, 0.7354244887579392], "same_patch_max_share_diff": 0.005500000000000005}}
Chance share: 0.088
