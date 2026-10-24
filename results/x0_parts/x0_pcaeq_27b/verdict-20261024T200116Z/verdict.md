# Word, J++ without the word, PCA: x0_pcaeq_27b

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.6-27b, layer 32, the single-change items of x0_single_27b_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). PCA at J++'s share (Dan, ~21:50): atoms per item median 5.0 (range 1-95). PCA: 200 held-out prompts of d1_topics_v4 (13790 tokens), the top 2000 directions hold 0.994 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| PCA top 2000 at J++'s share (k per item) | lookup | 0.138 | 0.48 | 0.47 | 0.47 | 0.03 [0.00, 0.06] | 0.01 [0.00, 0.04] | 0.02 [0.00, 0.05] | around |
| PCA top 2000 at J++'s share (k per item) | recall | 0.138 | 0.73 | 0.61 | 0.73 | 0.16 [0.08, 0.22] | 0.00 [-0.03, 0.03] | 0.16 [0.08, 0.23] | mixed |
| J++ without the word, orthogonal to the word (k = 25) | lookup | 0.111 | 0.48 | 0.46 | 0.47 | 0.04 [0.01, 0.09] | 0.01 [0.00, 0.04] | 0.03 [0.00, 0.07] | around |
| J++ without the word, orthogonal to the word (k = 25) | recall | 0.111 | 0.73 | 0.59 | 0.74 | 0.18 [0.09, 0.28] | -0.01 [-0.04, 0.02] | 0.20 [0.10, 0.29] | mixed |
| J++ (k = 25, reference) | lookup | 0.135 | 0.48 | 0.45 | 0.47 | 0.06 [0.02, 0.11] | 0.01 [0.00, 0.04] | 0.05 [0.01, 0.09] | around |
| J++ (k = 25, reference) | recall | 0.135 | 0.73 | 0.28 | 0.73 | 0.61 [0.52, 0.69] | 0.00 [-0.03, 0.03] | 0.61 [0.51, 0.69] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.

Reading for PCA at J++'s share (Dan, ~21:50, before the run): recall-specific like J++ -> 'J++-specific' means 'aligned with the layer's main directions'; hurts both readers -> J++ is the only dictionary that separates the readers; inert -> J++ is special at equal share. Branches (Q30.1, committed before the run): recall-specific = lookup excess <= 0.10, recall excess >= 0.20 with lower CI > 0; hurts both = lookup excess >= 0.10 and both readers' lower CI > 0; inert = both readers' upper CI < 0.10. This run: lookup 0.02 [0.00, 0.05], recall 0.16 [0.08, 0.23] -> none of the three branches.

Reading for the word-orthogonal part (Dan, ~22:05; no prediction committed before the run): recall still loses >= 0.20 with the word intact -> 'recall needs J++ components beyond the word'; <= 0.10 -> 'the word and the other J++ components are redundant: either suffices'. 'Loses' (set by the agent before the run): the point estimate of the recall's excess. This run: 0.20 [0.10, 0.29] -> neither branch (between 0.10 and 0.20).
