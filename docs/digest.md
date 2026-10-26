# Results digest (generated 2026-10-26 02:30 UTC by scripts/results_digest.py)

Every number is read from results/ (jsuite2_score, soft_score, jswap and probe_ceiling summaries). M - K: points lost on
memory finals minus stated-fact finals under the top-10 J++ removal at the band, start all, 95% bootstrap over bridges.
Swaps: transfer (donor - third) on PM. '-' = not run (or not yet).

## Knock-out (test set)

| Model | Band | J++ M - K | n (M) | K lost | rotated | logit lens | by probability | size-matched variance (pcasize) | renderings |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | L32-40 | +51 [46, 55] | 892 | 2.6 | +3 | +2 | +50 [47, 54] | +12 [10, 15] | -, - |
| Qwen3.5-9B | L12-16 | +43 [37, 49] | 563 | 5.0 | +2 | +1 | +35 [31, 40] | +7 [5, 10] | +42, +43 |
| DeepSeek-V4-Flash | L18-23 | +18 [14, 22] | 504 | 2.4 | +5 | +2 | +21 [18, 25] | +9 [5, 13] | - |
| Ministral-3-14B | L32-37 | +23 [19, 28] | 645 | 1.9 | +1 | +4 | +37 [34, 41] | +1 [0, 2] | - |
| Nemotron-3.5-Lightning | L27-33 | +53 [48, 59] | 563 | 3.7 | +4 | +9 | +44 [40, 48] | - | - |
| Nemotron-3.5-Bolt | (dev pick) | - | - | - | - | - | - | - | - |
| Muse-Glimmer-30B | (v2 band) | +60 [55, 65] | 541 | 1.8 | +3 | +35 | +49 [46, 53] | - | - |
| Qwen3.5-122B | (v2 band) | +48 [44, 54] | 778 | 0.8 | +2 | +12 | +2 [0, 4] | - | - |
| OLMo-3-32B (base, Q&A) | L12-20 | +5 [3, 8] | 467 | 0.0 | +2 | +2 | +4 [3, 5] | - | - |

## What the mention carries (swaps) and what the lens reads

| Model | Swap at the band | Swap at mid depth | Cross-relation | Probe readout (J++ / probe above chance) | Probe swap (valid relations) |
|---|---|---|---|---|---|
| Qwen3.6-27B | swap +66 / paste +59 / comp +39 / u +0 (n 338) | - | xrel +88 / srel +89 (ratio 0.99; n 374) | 0.91 on animals, cities, countries, languages | J++ +75 vs probe +8 (n 891) |
| Qwen3.5-9B | swap +69 / paste +45 / comp +18 / u -0 (n 258) | - | xrel +84 / srel +85 (ratio 0.99; n 204) | 1.21 on cities, countries, languages | J++ +80 vs probe +6 (n 456) |
| DeepSeek-V4-Flash | - | swap +12 / paste +20 / comp +17 / u +4 (n 247) | - | 0.96 on cities, countries | J++ +53 vs probe +17 (n 223) |
| Ministral-3-14B | swap +0 / paste +0 / comp +0 / u +0 (n 284) | swap +2 / paste +15 / comp +14 / u +0 (n 284) | - | 1.15 on animals, cities, countries, landmarks, languages, people | J++ +2 vs probe +3 (n 867) |
| Nemotron-3.5-Lightning | swap +46 / paste +13 / comp +8 / u +2 (n 275) | swap +51 / paste +13 / comp +6 / u +2 (n 275) | - | - | - |
| Nemotron-3.5-Bolt | - | - | - | - | - |
| Muse-Glimmer-30B | - | - | - | - | - |
| Qwen3.5-122B | - | - | - | - | - |
| OLMo-3-32B (base, Q&A) | swap +41 / paste +52 / comp +52 / u +0 (n 227) | - | - | - | - |
