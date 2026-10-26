# Word, J++ without the word, PCA: x0_jppother100_27b

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.6-27b, layer 32, the alt cf items of x0_necessity_27b_chat (n = 200); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ atoms fitted to another scene's change (k = 100) | lookup | 0.047 | 0.42 | 0.42 | 0.42 | 0.00 [-0.03, 0.03] | 0.01 [0.00, 0.04] | -0.01 [-0.04, 0.00] | around |
| J++ atoms fitted to another scene's change (k = 100) | recall | 0.047 | 0.75 | 0.73 | 0.75 | 0.03 [0.01, 0.05] | 0.00 [-0.02, 0.02] | 0.03 [0.01, 0.05] | around |
| J++ (k = 25, reference) | lookup | 0.155 | 0.42 | 0.35 | 0.41 | 0.16 [0.09, 0.24] | 0.02 [0.00, 0.06] | 0.14 [0.08, 0.21] | mixed |
| J++ (k = 25, reference) | recall | 0.155 | 0.75 | 0.18 | 0.72 | 0.76 [0.66, 0.84] | 0.03 [-0.01, 0.07] | 0.73 [0.64, 0.80] | through |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
