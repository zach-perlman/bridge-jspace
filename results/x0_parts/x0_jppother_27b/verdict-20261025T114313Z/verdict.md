# Word, J++ without the word, PCA: x0_jppother_27b

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.6-27b, layer 32, the single-change items of x0_single_27b_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ atoms fitted to another scene's change (k = 25) | lookup | 0.011 | 0.47 | 0.47 | 0.47 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| J++ atoms fitted to another scene's change (k = 25) | recall | 0.011 | 0.73 | 0.72 | 0.74 | 0.01 [-0.02, 0.03] | -0.01 [-0.03, 0.00] | 0.02 [-0.01, 0.05] | around |
| J++ (k = 25, reference) | lookup | 0.135 | 0.47 | 0.45 | 0.47 | 0.05 [0.01, 0.09] | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] | around |
| J++ (k = 25, reference) | recall | 0.135 | 0.73 | 0.28 | 0.73 | 0.61 [0.52, 0.69] | 0.00 [-0.03, 0.03] | 0.61 [0.51, 0.69] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
