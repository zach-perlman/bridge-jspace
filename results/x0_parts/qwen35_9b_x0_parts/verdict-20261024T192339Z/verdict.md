# Word, J++ without the word, PCA: qwen35_9b_x0_parts

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-9b, layer 12, the single-change items of qwen35_9b_x0_single_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 6.0 (range 2-16). PCA: 200 held-out prompts of d1_topics_v4 (13790 tokens), the top 2000 directions hold 0.997 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.041 | 0.53 | 0.52 | 0.52 | 0.02 [0.00, 0.05] | 0.02 [0.00, 0.05] | 0.00 [-0.03, 0.03] | around |
| word only (least squares) | recall | 0.041 | 0.95 | 0.93 | 0.95 | 0.03 [0.00, 0.06] | 0.01 [-0.01, 0.02] | 0.02 [-0.00, 0.06] | around |
| J++ without the word (k = 25) | lookup | 0.187 | 0.53 | 0.48 | 0.47 | 0.09 [0.02, 0.15] | 0.10 [0.05, 0.16] | -0.02 [-0.07, 0.03] | around |
| J++ without the word (k = 25) | recall | 0.187 | 0.95 | 0.57 | 0.93 | 0.40 [0.33, 0.48] | 0.03 [0.01, 0.06] | 0.37 [0.30, 0.43] | through |
| PCA top 2000 (k = 25) | lookup | 0.387 | 0.53 | 0.17 | 0.36 | 0.69 [0.60, 0.77] | 0.30 [0.21, 0.40] | 0.38 [0.29, 0.48] | through |
| PCA top 2000 (k = 25) | recall | 0.387 | 0.95 | 0.29 | 0.74 | 0.69 [0.58, 0.79] | 0.22 [0.15, 0.29] | 0.47 [0.38, 0.55] | through |
| J++ (k = 25, reference) | lookup | 0.186 | 0.53 | 0.47 | 0.47 | 0.10 [0.05, 0.14] | 0.10 [0.05, 0.16] | -0.01 [-0.04, 0.02] | around |
| J++ (k = 25, reference) | recall | 0.186 | 0.95 | 0.57 | 0.92 | 0.40 [0.33, 0.47] | 0.04 [0.02, 0.07] | 0.36 [0.29, 0.42] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
