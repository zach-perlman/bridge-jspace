# exp02_swaps / main_v4_jpp_32-48

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 32-48 | raw_jlens |  | 77 | 55% [43, 65] | 38% [28, 49] | 8% | 0.010 | 0 |
| 32-48 | raw_jlens | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.048 | 0 |
| 32-48 | full_probe |  | 77 | 25% [16, 35] | 57% [46, 68] | 18% | 0.064 | 0 |
| 32-48 | full_probe | yes | 77 | 0% [0, 5] | 74% [63, 83] | 26% | 0.167 | 0 |
| 32-48 | jpart |  | 77 | 44% [34, 55] | 47% [36, 58] | 9% | 0.018 | 0 |
| 32-48 | jpart | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.053 | 0 |
| 32-48 | remainder |  | 77 | 10% [5, 19] | 77% [66, 85] | 13% | 0.069 | 0 |
| 32-48 | remainder | yes | 77 | 4% [1, 11] | 75% [65, 84] | 21% | 0.169 | 0 |
| 32-48 | remainder_clamped |  | 77 | 3% [1, 9] | 88% [79, 94] | 9% | 0.084 | 0 |
| 32-48 | remainder_clamped | yes | 77 | 1% [0, 7] | 71% [61, 80] | 27% | 0.172 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +34 pts [+22, +44]
- remainder - remainder_clamped: +8 pts [+1, +16]

Labels: J-mediated 33, non-J 1, both 1, neither 42
