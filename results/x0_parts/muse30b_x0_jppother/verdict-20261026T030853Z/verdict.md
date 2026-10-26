# Word, J++ without the word, PCA: muse30b_x0_jppother

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model muse-glimmer-30b, layer 26, the single-change items of muse30b_x0_single (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ atoms fitted to another scene's change (k = 25) | lookup | 0.013 | 0.43 | 0.43 | 0.43 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| J++ atoms fitted to another scene's change (k = 25) | recall | 0.013 | 0.57 | 0.56 | 0.58 | 0.02 [0.00, 0.04] | -0.03 [-0.08, 0.01] | 0.04 [0.01, 0.09] | around |
| J++ (k = 25, reference) | lookup | 0.117 | 0.43 | 0.42 | 0.42 | 0.01 [-0.03, 0.05] | 0.01 [0.00, 0.04] | 0.00 [-0.03, 0.03] | around |
| J++ (k = 25, reference) | recall | 0.117 | 0.57 | 0.21 | 0.59 | 0.62 [0.50, 0.73] | -0.04 [-0.10, 0.02] | 0.66 [0.53, 0.77] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
