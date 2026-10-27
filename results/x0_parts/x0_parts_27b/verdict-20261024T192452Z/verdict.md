# Word, J++ without the word, PCA: x0_parts_27b

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.6-27b, layer 32, the single-change items of x0_single_27b_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 6.0 (range 2-17). PCA: 200 held-out prompts of d1_topics_v4 (13790 tokens), the top 2000 directions hold 0.994 of the residual variance. UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.029 | 0.48 | 0.47 | 0.47 | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | around |
| word only (least squares) | recall | 0.029 | 0.72 | 0.62 | 0.73 | 0.14 [0.08, 0.22] | -0.01 [-0.04, 0.02] | 0.16 [0.08, 0.23] | mixed |
| J++ without the word (k = 25) | lookup | 0.133 | 0.48 | 0.45 | 0.47 | 0.07 [0.03, 0.12] | 0.02 [0.00, 0.05] | 0.05 [0.01, 0.10] | around |
| J++ without the word (k = 25) | recall | 0.133 | 0.72 | 0.28 | 0.73 | 0.61 [0.52, 0.68] | -0.01 [-0.04, 0.02] | 0.63 [0.53, 0.71] | through |
| PCA top 2000 (k = 25) | lookup | 0.340 | 0.48 | 0.22 | 0.40 | 0.54 [0.40, 0.67] | 0.17 [0.11, 0.23] | 0.38 [0.24, 0.49] | through |
| PCA top 2000 (k = 25) | recall | 0.340 | 0.72 | 0.29 | 0.60 | 0.60 [0.45, 0.72] | 0.17 [0.10, 0.22] | 0.43 [0.32, 0.53] | through |
| J++ (k = 25, reference) | lookup | 0.135 | 0.48 | 0.45 | 0.47 | 0.06 [0.02, 0.11] | 0.02 [0.00, 0.05] | 0.04 [0.01, 0.08] | around |
| J++ (k = 25, reference) | recall | 0.135 | 0.72 | 0.28 | 0.73 | 0.62 [0.53, 0.70] | -0.01 [-0.04, 0.02] | 0.63 [0.53, 0.72] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
