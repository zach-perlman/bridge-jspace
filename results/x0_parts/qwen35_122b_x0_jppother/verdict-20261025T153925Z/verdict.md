# Word, J++ without the word, PCA: qwen35_122b_x0_jppother

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-122b-a10b, layer 33, the single-change items of qwen35_122b_x0_single (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ atoms fitted to another scene's change (k = 25) | lookup | 0.022 | 0.47 | 0.46 | 0.47 | 0.02 [0.00, 0.05] | 0.01 [-0.03, 0.05] | 0.01 [-0.02, 0.05] | around |
| J++ atoms fitted to another scene's change (k = 25) | recall | 0.022 | 0.90 | 0.91 | 0.90 | -0.02 [-0.05, 0.01] | -0.01 [-0.03, 0.01] | -0.01 [-0.03, 0.00] | around |
| J++ (k = 25, reference) | lookup | 0.211 | 0.47 | 0.43 | 0.41 | 0.07 [0.02, 0.14] | 0.12 [0.04, 0.21] | -0.04 [-0.11, 0.01] | around |
| J++ (k = 25, reference) | recall | 0.211 | 0.90 | 0.62 | 0.84 | 0.31 [0.20, 0.41] | 0.06 [0.02, 0.10] | 0.25 [0.15, 0.34] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
