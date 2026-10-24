# Word, J++ without the word, PCA: qwen35_9b_x0_pcaeq

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-9b, layer 12, the single-change items of qwen35_9b_x0_single_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). PCA at J++'s share (Dan, ~21:50): atoms per item median 8.0 (range 3-54). PCA: 200 held-out prompts of d1_topics_v4 (13790 tokens), the top 2000 directions hold 0.997 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| PCA top 2000 at J++'s share (k per item) | lookup | 0.189 | 0.53 | 0.43 | 0.48 | 0.18 [0.10, 0.26] | 0.09 [0.03, 0.16] | 0.08 [0.02, 0.15] | around |
| PCA top 2000 at J++'s share (k per item) | recall | 0.189 | 0.95 | 0.79 | 0.92 | 0.17 [0.10, 0.24] | 0.04 [0.02, 0.07] | 0.13 [0.06, 0.19] | mixed |
| J++ without the word, orthogonal to the word (k = 25) | lookup | 0.158 | 0.53 | 0.47 | 0.47 | 0.11 [0.06, 0.17] | 0.11 [0.06, 0.16] | 0.00 [-0.03, 0.02] | around |
| J++ without the word, orthogonal to the word (k = 25) | recall | 0.158 | 0.95 | 0.83 | 0.94 | 0.13 [0.06, 0.21] | 0.02 [-0.01, 0.04] | 0.12 [0.06, 0.18] | mixed |
| J++ (k = 25, reference) | lookup | 0.186 | 0.53 | 0.48 | 0.47 | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.17] | -0.02 [-0.05, 0.02] | around |
| J++ (k = 25, reference) | recall | 0.186 | 0.95 | 0.56 | 0.92 | 0.41 [0.34, 0.48] | 0.04 [0.02, 0.07] | 0.37 [0.29, 0.43] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.

Reading for PCA at J++'s share (Dan, ~21:50, before the run): recall-specific like J++ -> 'J++-specific' means 'aligned with the layer's main directions'; hurts both readers -> J++ is the only dictionary that separates the readers; inert -> J++ is special at equal share. Branches (Q30.1, committed before the run): recall-specific = lookup excess <= 0.10, recall excess >= 0.20 with lower CI > 0; hurts both = lookup excess >= 0.10 and both readers' lower CI > 0; inert = both readers' upper CI < 0.10. This run: lookup 0.08 [0.02, 0.15], recall 0.13 [0.06, 0.19] -> none of the three branches.

Reading for the word-orthogonal part (Dan, ~22:05; no prediction committed before the run): recall still loses >= 0.20 with the word intact -> 'recall needs J++ components beyond the word'; <= 0.10 -> 'the word and the other J++ components are redundant: either suffices'. 'Loses' (set by the agent before the run): the point estimate of the recall's excess. This run: 0.12 [0.06, 0.18] -> neither branch (between 0.10 and 0.20).
