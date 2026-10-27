# Word, J++ without the word, PCA: x0b_parts_27b

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.6-27b, layer 32, the single-change items of x0b_v2_27b (n = 1635); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 7 (range 2-17). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.037 | 0.66 | 0.66 | 0.66 | 0.01 [-0.00, 0.01] | -0.00 [-0.01, 0.01] | 0.01 [0.00, 0.02] | around |
| word only (least squares) | recall | 0.037 | 0.68 | 0.60 | 0.68 | 0.11 [0.08, 0.15] | -0.00 [-0.01, 0.01] | 0.12 [0.08, 0.15] | mixed |
| J++ without the word (k = 25) | lookup | 0.143 | 0.66 | 0.62 | 0.67 | 0.07 [0.05, 0.09] | -0.01 [-0.02, -0.00] | 0.08 [0.06, 0.10] | around |
| J++ without the word (k = 25) | recall | 0.143 | 0.68 | 0.30 | 0.67 | 0.55 [0.50, 0.61] | 0.01 [-0.02, 0.03] | 0.55 [0.49, 0.60] | through |
| J++ (k = 25, reference) | lookup | 0.145 | 0.66 | 0.62 | 0.67 | 0.07 [0.05, 0.09] | -0.01 [-0.02, -0.00] | 0.08 [0.06, 0.10] | around |
| J++ (k = 25, reference) | recall | 0.145 | 0.68 | 0.30 | 0.67 | 0.56 [0.51, 0.62] | 0.00 [-0.02, 0.03] | 0.56 [0.50, 0.62] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
