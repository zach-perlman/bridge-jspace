# Word, J++ without the word, PCA: muse30b_x0_parts

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model muse-glimmer-30b, layer 26, the single-change items of muse30b_x0_single (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 7.0 (range 3-16). PCA at J++'s share (Dan, ~21:50): atoms per item median 6.0 (range 2-59). PCA: 200 held-out prompts of d1_topics_v4 (20865 tokens), the top 2000 directions hold 0.993 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.043 | 0.43 | 0.42 | 0.43 | 0.02 [0.00, 0.05] | -0.01 [-0.04, 0.00] | 0.03 [0.00, 0.07] | around |
| word only (least squares) | recall | 0.043 | 0.56 | 0.46 | 0.57 | 0.18 [0.08, 0.26] | -0.03 [-0.09, 0.02] | 0.21 [0.12, 0.29] | mixed |
| J++ without the word, orthogonal to the word (k = 25) | lookup | 0.085 | 0.43 | 0.43 | 0.43 | 0.00 [-0.04, 0.03] | 0.00 [-0.04, 0.03] | 0.00 [-0.03, 0.03] | around |
| J++ without the word, orthogonal to the word (k = 25) | recall | 0.085 | 0.56 | 0.54 | 0.57 | 0.04 [-0.01, 0.10] | -0.03 [-0.07, 0.03] | 0.07 [0.00, 0.13] | around |
| PCA top 2000 at J++'s share (k per item) | lookup | 0.118 | 0.43 | 0.39 | 0.42 | 0.09 [0.03, 0.15] | 0.02 [-0.02, 0.06] | 0.07 [0.02, 0.12] | around |
| PCA top 2000 at J++'s share (k per item) | recall | 0.118 | 0.56 | 0.49 | 0.59 | 0.12 [0.01, 0.20] | -0.06 [-0.13, 0.00] | 0.18 [0.08, 0.26] | mixed |
| J++ (k = 25, reference) | lookup | 0.117 | 0.43 | 0.42 | 0.41 | 0.02 [-0.03, 0.06] | 0.03 [-0.02, 0.07] | -0.01 [-0.04, 0.00] | around |
| J++ (k = 25, reference) | recall | 0.117 | 0.56 | 0.21 | 0.58 | 0.62 [0.50, 0.73] | -0.04 [-0.10, 0.02] | 0.66 [0.53, 0.78] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.

Reading for PCA at J++'s share (Dan, ~21:50, before the run): recall-specific like J++ -> 'J++-specific' means 'aligned with the layer's main directions'; hurts both readers -> J++ is the only dictionary that separates the readers; inert -> J++ is special at equal share. Branches (Q30.1, committed before the run): recall-specific = lookup excess <= 0.10, recall excess >= 0.20 with lower CI > 0; hurts both = lookup excess >= 0.10 and both readers' lower CI > 0; inert = both readers' upper CI < 0.10. This run: lookup 0.07 [0.02, 0.12], recall 0.18 [0.08, 0.26] -> none of the three branches.

Reading for the word-orthogonal part (Dan, ~22:05; no prediction committed before the run): recall still loses >= 0.20 with the word intact -> 'recall needs J++ components beyond the word'; <= 0.10 -> 'the word and the other J++ components are redundant: either suffices'. 'Loses' (set by the agent before the run): the point estimate of the recall's excess. This run: 0.07 [0.00, 0.13] -> the word and the other J++ components are redundant: either suffices.

## Each part pasted alone (Dan, 25 Oct ~00:20): its switches as a share of the whole change's, against the random part of its share alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ without the word, orthogonal to the word (k = 25) | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| J++ without the word, orthogonal to the word (k = 25) | recall | 200 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] |
| word only (least squares) | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| word only (least squares) | recall | 200 | 0.04 [0.01, 0.11] | 0.00 [0.00, 0.00] | 0.04 [0.01, 0.11] |
