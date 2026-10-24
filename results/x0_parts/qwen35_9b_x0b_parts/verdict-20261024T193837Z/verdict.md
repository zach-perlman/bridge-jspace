# Word, J++ without the word, PCA: qwen35_9b_x0b_parts

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-9b, layer 12, the single-change items of qwen35_9b_x0b_v2 (n = 1010); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 6.0 (range 2-17). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.048 | 0.79 | 0.78 | 0.79 | 0.01 [0.00, 0.02] | 0.00 [-0.01, 0.01] | 0.01 [-0.00, 0.02] | around |
| word only (least squares) | recall | 0.048 | 0.96 | 0.91 | 0.96 | 0.05 [0.03, 0.09] | 0.00 [-0.00, 0.00] | 0.05 [0.03, 0.09] | around |
| J++ without the word (k = 25) | lookup | 0.198 | 0.79 | 0.73 | 0.74 | 0.08 [0.06, 0.09] | 0.06 [0.04, 0.07] | 0.02 [0.00, 0.03] | around |
| J++ without the word (k = 25) | recall | 0.198 | 0.96 | 0.71 | 0.95 | 0.26 [0.17, 0.36] | 0.02 [0.01, 0.03] | 0.24 [0.16, 0.34] | mixed |
| J++ (k = 25, reference) | lookup | 0.203 | 0.79 | 0.73 | 0.74 | 0.08 [0.05, 0.09] | 0.06 [0.04, 0.08] | 0.01 [-0.00, 0.03] | around |
| J++ (k = 25, reference) | recall | 0.203 | 0.96 | 0.72 | 0.94 | 0.25 [0.16, 0.36] | 0.02 [0.01, 0.04] | 0.23 [0.15, 0.33] | mixed |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
