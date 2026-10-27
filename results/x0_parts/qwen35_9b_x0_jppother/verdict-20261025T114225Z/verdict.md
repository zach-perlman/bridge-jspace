# Word, J++ without the word, PCA: qwen35_9b_x0_jppother

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-9b, layer 12, the single-change items of qwen35_9b_x0_single_r2 (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ atoms fitted to another scene's change (k = 25) | lookup | 0.018 | 0.53 | 0.52 | 0.52 | 0.02 [0.00, 0.05] | 0.03 [0.00, 0.06] | -0.01 [-0.03, 0.00] | around |
| J++ atoms fitted to another scene's change (k = 25) | recall | 0.018 | 0.95 | 0.95 | 0.95 | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | -0.01 [-0.02, 0.00] | around |
| J++ (k = 25, reference) | lookup | 0.186 | 0.53 | 0.48 | 0.47 | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.17] | -0.02 [-0.05, 0.02] | around |
| J++ (k = 25, reference) | recall | 0.186 | 0.95 | 0.56 | 0.92 | 0.41 [0.34, 0.48] | 0.04 [0.02, 0.07] | 0.37 [0.29, 0.43] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
