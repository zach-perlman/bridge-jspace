# Word, J++ without the word, PCA: qwen35_122b_x0b_parts

Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule. Model qwen3.5-122b-a10b, layer 33, the single-change items of qwen35_122b_x0b_v2 (n = 852); each part removed against a random subspace of its own share; bootstrap over bridge entities (10000 resamples). Word variants per item: median 5.0 (range 2-16). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| word only (least squares) | lookup | 0.090 | 0.74 | 0.73 | 0.73 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | -0.00 [-0.01, 0.01] | around |
| word only (least squares) | recall | 0.090 | 0.94 | 0.86 | 0.93 | 0.08 [0.06, 0.10] | 0.01 [-0.00, 0.02] | 0.07 [0.05, 0.09] | around |
| J++ without the word (k = 25) | lookup | 0.203 | 0.74 | 0.71 | 0.71 | 0.03 [0.02, 0.05] | 0.04 [0.02, 0.06] | -0.01 [-0.02, 0.00] | around |
| J++ without the word (k = 25) | recall | 0.203 | 0.94 | 0.76 | 0.89 | 0.19 [0.16, 0.22] | 0.05 [0.03, 0.07] | 0.14 [0.11, 0.17] | mixed |
| J++ (k = 25, reference) | lookup | 0.209 | 0.74 | 0.72 | 0.70 | 0.03 [0.01, 0.04] | 0.05 [0.03, 0.06] | -0.02 [-0.04, -0.01] | around |
| J++ (k = 25, reference) | recall | 0.209 | 0.94 | 0.75 | 0.89 | 0.19 [0.17, 0.23] | 0.05 [0.03, 0.07] | 0.14 [0.11, 0.18] | mixed |

Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with the layer's geometry'.
