# Word, J++ without the word, PCA: qwen35_122b_x0_parts

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-122b-a10b, layer 33, the single-change items of qwen35_122b_x0_single (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 6.0 (range 2-17). PCA at J++'s share (Dan, ~21:50): atoms per item median 8.5 (range 2-51). PCA: 200 held-out prompts of d1_topics_v4 (13790 tokens), the top 2000 directions hold 0.998 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.092 | 0.46 | 0.44 | 0.43 | 0.03 [-0.01, 0.09] | 0.04 [0.00, 0.10] | -0.01 [-0.05, 0.02] | around |
| word only (least squares) | recall | 0.092 | 0.91 | 0.76 | 0.88 | 0.17 [0.10, 0.24] | 0.03 [0.01, 0.07] | 0.14 [0.08, 0.20] | mixed |
| J++ without the word, orthogonal to the word (k = 25) | lookup | 0.139 | 0.46 | 0.45 | 0.43 | 0.02 [-0.03, 0.08] | 0.05 [0.01, 0.11] | -0.03 [-0.07, 0.00] | around |
| J++ without the word, orthogonal to the word (k = 25) | recall | 0.139 | 0.91 | 0.86 | 0.90 | 0.05 [0.03, 0.09] | 0.02 [-0.01, 0.04] | 0.04 [0.00, 0.08] | around |
| PCA top 2000 at J++'s share (k per item) | lookup | 0.215 | 0.46 | 0.39 | 0.43 | 0.14 [0.06, 0.23] | 0.05 [0.00, 0.12] | 0.09 [0.02, 0.15] | around |
| PCA top 2000 at J++'s share (k per item) | recall | 0.215 | 0.91 | 0.64 | 0.83 | 0.30 [0.21, 0.39] | 0.09 [0.05, 0.13] | 0.21 [0.13, 0.30] | through |
| J++ (k = 25, reference) | lookup | 0.211 | 0.46 | 0.43 | 0.43 | 0.04 [0.00, 0.10] | 0.05 [0.00, 0.12] | -0.01 [-0.06, 0.04] | around |
| J++ (k = 25, reference) | recall | 0.211 | 0.91 | 0.61 | 0.85 | 0.33 [0.22, 0.43] | 0.07 [0.03, 0.11] | 0.26 [0.16, 0.36] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.

Reading for PCA at J++'s share (Dan, ~21:50, before the run): recall-specific like J++ -> 'J++-specific' means 'aligned with the layer's main directions'; hurts both readers -> J++ is the only dictionary that separates the readers; inert -> J++ is special at equal share. Branches (Q30.1, committed before the run): recall-specific = lookup excess <= 0.10, recall excess >= 0.20 with lower CI > 0; hurts both = lookup excess >= 0.10 and both readers' lower CI > 0; inert = both readers' upper CI < 0.10. This run: lookup 0.09 [0.02, 0.15], recall 0.21 [0.13, 0.30] -> recall-specific like J++.

Reading for the word-orthogonal part (Dan, ~22:05; no prediction committed before the run): recall still loses >= 0.20 with the word intact -> 'recall needs J++ components beyond the word'; <= 0.10 -> 'the word and the other J++ components are redundant: either suffices'. 'Loses' (set by the agent before the run): the point estimate of the recall's excess. This run: 0.04 [0.00, 0.08] -> the word and the other J++ components are redundant: either suffices.

## Each part pasted alone (Dan, 25 Oct ~00:20): its switches as a share of the whole change's, against the random part of its share alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ without the word, orthogonal to the word (k = 25) | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| J++ without the word, orthogonal to the word (k = 25) | recall | 200 | 0.02 [0.00, 0.04] | 0.01 [0.00, 0.03] | 0.01 [-0.02, 0.03] |
| word only (least squares) | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| word only (least squares) | recall | 200 | 0.07 [0.04, 0.11] | 0.00 [0.00, 0.00] | 0.07 [0.04, 0.11] |
