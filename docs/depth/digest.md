# Results digest (generated 2026-10-27 08:11 UTC by scripts/results_digest.py)

Every number is read from results/ (jsuite2_score, soft_score, jswap and probe_ceiling summaries). M - K: accuracy drop (points) on
memory finals minus stated-fact finals under the top-10 J++ removal at the band, start all, 95% bootstrap over bridges.
Swaps: transfer (donor - third) on PM. '-' = not run (or not yet).

## Knock-out (test set)

| Model | Band | J++ M - K | n (M) | K drop | rotated | logit lens | by probability | size-matched variance (pcasize) | renderings |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | L32-40 | +51 [46, 55] | 892 | 2.6 | +3 | +2 | +50 [47, 54] | +12 [10, 15] | +49, +50 |
| Qwen3.5-9B | L12-16 | +43 [37, 49] | 563 | 5.0 | +2 | +1 | +35 [31, 40] | +7 [5, 10] | +42, +43 |
| DeepSeek-V4-Flash | L18-23 | +18 [14, 22] | 504 | 2.4 | +5 | +2 | +21 [18, 25] | +9 [5, 13] | - |
| Ministral-3-14B | L32-37 | +23 [19, 28] | 645 | 1.9 | +1 | +4 | +37 [34, 41] | +1 [0, 2] | - |
| Nemotron-3.5-Lightning | L27-33 | +53 [48, 59] | 563 | 3.7 | +4 | +9 | +44 [40, 48] | +8 [6, 11] | +49, +50 |
| Nemotron-3.5-Bolt | L42-53 | +6 [3, 9] | 383 | 0.5 | +0 | +2 | +6 [4, 8] | - | - |
| Muse-Glimmer-30B | L36-42 | +60 [55, 65] | 541 | 1.8 | +3 | +35 | +49 [46, 53] | - | - |
| Qwen3.5-122B | L39-45 | +48 [44, 54] | 778 | 0.8 | +2 | +12 | +2 [0, 4] | - | - |
| OLMo-3-32B (base, Q&A) | L12-20 | +5 [3, 8] | 467 | 0.0 | +2 | +2 | +4 [3, 5] | - | - |

## What the mention carries (swaps) and what the lens reads

| Model | Swap at the band | Swap at mid depth | Cross-relation | Probe readout (J++ / probe above chance) | Probe swap (valid relations) |
|---|---|---|---|---|---|
| Qwen3.6-27B | swap +66 / paste +59 / comp +39 / u +0 (n 338) | - | xrel +88 / srel +89 (ratio 0.99; n 374) | 0.91 on animals, cities, countries, languages | J++ +75 vs probe +8 (n 891) |
| Qwen3.5-9B | swap +69 / paste +45 / comp +18 / u -0 (n 258) | - | xrel +84 / srel +85 (ratio 0.99; n 204) | 1.21 on cities, countries, languages | J++ +80 vs probe +6 (n 456) |
| DeepSeek-V4-Flash | - | swap +12 / paste +20 / comp +17 / u +4 (n 247) | - | 0.96 on cities, countries | J++ +53 vs probe +17 (n 223) |
| Ministral-3-14B | swap +0 / paste +0 / comp +0 / u +0 (n 284) | swap +2 / paste +15 / comp +14 / u +0 (n 284) | - | 1.15 on animals, cities, countries, landmarks, languages, people | J++ +2 vs probe +3 (n 867) |
| Nemotron-3.5-Lightning | swap +46 / paste +13 / comp +8 / u +2 (n 275) | swap +51 / paste +13 / comp +6 / u +2 (n 275) | xrel +61 / srel +62 (ratio 0.98; n 198) | 1.11 on cities, countries, languages | J++ +62 vs probe +2 (n 420) |
| Nemotron-3.5-Bolt | swap +1 / paste +19 / comp +19 / u +1 (n 150) | swap +2 / paste +20 / comp +20 / u +1 (n 292) | - | - | - |
| Muse-Glimmer-30B | - | - | - | - | - |
| Qwen3.5-122B | - | - | - | - | - |
| OLMo-3-32B (base, Q&A) | swap +41 / paste +52 / comp +52 / u +0 (n 227) | - | - | - | - |

## Pointer tests (amendment 51; memory finals pooled, 150 random per word)

Neutral donor: the J-part from one neutral sentence about D. Own / no-own: the J-part's own-word rows alone / without them.
Relations: neutral >= 2/3 of the same-passage swap, of the relations with swap >= 10. Lookup: first layer at the answer
position where the lens reads X's answer (unedited) / D's answer (neutral-donor swap) on >= 50% of items.

| Model | n | J-part swap | neutral donor (ratio) | neutral rot / u | paste_neutral | relations | own name (share) | no-own (share) | lookup |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | 898 | +64 [58, 70] | +70 (1.09) | -1 / +0 | +68 | 8 of 8 | +44 (0.69) | +54 (0.84) | X from L50; D (neutral donor) from L56 |
| Qwen3.5-9B | 624 | +64 [58, 70] | +70 (1.10) | +1 / -0 | +55 | 8 of 8 | +46 (0.73) | +52 (0.83) | X from L23; D (neutral donor) from L24 |
| Nemotron-3.5-Lightning | 654 | +46 [40, 52] | +46 (1.01) | -0 / +1 | +44 | 7 of 7 | +32 (0.69) | +28 (0.62) | X from L32; D (neutral donor) peaks 45% |
| Nemotron-3.5-Bolt | 698 | +41 [35, 48] | +42 (1.01) | -0 / +2 | +28 | 6 of 6 | +34 (0.83) | +18 (0.43) | X from L69; D (neutral donor) peaks 44% |

## Removal size at the knock-out band (median share of the residual norm removed, top 10)

| Model | J++ | logit lens | top principal directions |
|---|---|---|---|
| Qwen3.6-27B | 16% | 10% | 72% |
| Qwen3.5-9B | 13% | 9% | 68% |
| DeepSeek-V4-Flash | 14% | 15% | 50% |
| Ministral-3-14B | 20% | 17% | 73% |
| Nemotron-3.5-Lightning | 18% | 16% | 63% |
| Nemotron-3.5-Bolt | 6% | 11% | - |

## Dose in K (top-K J++ directions; amendments 52, 53)

Knock-out on the test set at the knock-out band; swap pooled over memory finals at the swap band. Size: share of the
residual norm the top-K J++ removal takes there.

| Model | K | size (KO band) | M - K | rotated | logit lens | size (swap band) | J-part swap / paste / comp / rot |
|---|---|---|---|---|---|---|---|
| Nemotron-3.5-Bolt | 10 | L42-53: 6% | +6 [3, 9] | +0 | +2 | L42-53: 6% | +3 [1, 4] / paste +20 / comp +19 / rot +0 (n 698) |
| Nemotron-3.5-Bolt | 30 | L42-53: 10% | +14 [10, 18] | +1 | +3 | L42-53: 10% | +10 [7, 13] / paste +20 / comp +20 / rot +0 (n 698) |
| Nemotron-3.5-Bolt | 100 | L42-53: 18% | +31 [26, 37] | +7 | +2 | L42-53: 18% | +41 [35, 48] / paste +20 / comp +18 / rot -1 (n 698) |
| Ministral-3-14B | 10 | L32-37: 20% | +23 [19, 28] | +1 | +4 | L20-25: 16% | +3 [2, 4] / paste +10 / comp +8 / rot +0 (n 1212) |
| Ministral-3-14B | 30 | L32-37: 22% | +24 [20, 29] | +1 | +3 | L20-25: 19% | +4 [2, 5] / paste +10 / comp +8 / rot +0 (n 1212) |
| Ministral-3-14B | 100 | L32-37: 25% | +19 [15, 23] | +1 | +3 | L20-25: 21% | +5 [3, 6] / paste +10 / comp +8 / rot +0 (n 1212) |
