# exp02_swaps / main

Items: eligible 67, clean_wrong 16, multi_token_answer 7

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 32-48 | raw_jlens |  | 67 | 51% [39, 62] | 36% [25, 48] | 13% | 0.008 | 0 |
| 32-48 | raw_jlens | yes | 67 | 1% [0, 8] | 97% [90, 99] | 1% | 0.056 | 0 |
| 32-48 | full_probe |  | 67 | 27% [18, 39] | 51% [39, 62] | 22% | 0.063 | 0 |
| 32-48 | full_probe | yes | 67 | 0% [0, 5] | 67% [55, 77] | 33% | 0.160 | 0 |
| 32-48 | jpart |  | 67 | 39% [28, 51] | 52% [40, 64] | 9% | 0.014 | 0 |
| 32-48 | jpart | yes | 67 | 0% [0, 5] | 99% [92, 100] | 1% | 0.054 | 0 |
| 32-48 | remainder |  | 67 | 13% [7, 24] | 66% [54, 76] | 21% | 0.068 | 0 |
| 32-48 | remainder | yes | 67 | 0% [0, 5] | 72% [60, 81] | 28% | 0.169 | 0 |
| 32-48 | remainder_clamped |  | 67 | 3% [1, 10] | 82% [71, 89] | 15% | 0.079 | 0 |
| 32-48 | remainder_clamped | yes | 67 | 1% [0, 8] | 64% [52, 75] | 34% | 0.185 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +25 pts [+13, +37]
- remainder - remainder_clamped: +10 pts [+3, +19]

Labels: J-mediated 25, non-J 1, both 1, neither 40
