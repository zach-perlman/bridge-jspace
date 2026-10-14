# exp02_swaps / main_v4_jlens_32-48

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 32-48 | raw_jlens |  | 77 | 48% [37, 59] | 42% [31, 53] | 10% | 0.008 | 0 |
| 32-48 | raw_jlens | yes | 77 | 1% [0, 7] | 99% [93, 100] | 0% | 0.056 | 0 |
| 32-48 | full_probe |  | 77 | 25% [16, 35] | 57% [46, 68] | 18% | 0.064 | 0 |
| 32-48 | full_probe | yes | 77 | 0% [0, 5] | 74% [63, 83] | 26% | 0.167 | 0 |
| 32-48 | jpart |  | 77 | 34% [24, 45] | 57% [46, 68] | 9% | 0.014 | 0 |
| 32-48 | jpart | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.058 | 0 |
| 32-48 | remainder |  | 77 | 12% [6, 21] | 74% [63, 83] | 14% | 0.070 | 0 |
| 32-48 | remainder | yes | 77 | 3% [1, 9] | 75% [65, 84] | 22% | 0.175 | 0 |
| 32-48 | remainder_clamped |  | 77 | 1% [0, 7] | 91% [82, 96] | 8% | 0.081 | 0 |
| 32-48 | remainder_clamped | yes | 77 | 3% [1, 9] | 68% [56, 77] | 30% | 0.173 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +22 pts [+12, +32]
- remainder - remainder_clamped: +10 pts [+4, +18]

Labels: J-mediated 25, non-J 0, both 1, neither 51
