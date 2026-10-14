# exp02_swaps / main_v4_jlens

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 40% [30, 51] | 55% [43, 65] | 5% | 0.008 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.042 | 0 |
| 24-40 | full_probe |  | 77 | 27% [19, 38] | 55% [43, 65] | 18% | 0.074 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 88% [79, 94] | 10% | 0.161 | 0 |
| 24-40 | jpart |  | 77 | 35% [25, 46] | 58% [47, 69] | 6% | 0.014 | 0 |
| 24-40 | jpart | yes | 77 | 1% [0, 7] | 96% [89, 99] | 3% | 0.045 | 0 |
| 24-40 | remainder |  | 77 | 12% [6, 21] | 71% [61, 80] | 17% | 0.077 | 0 |
| 24-40 | remainder | yes | 77 | 3% [1, 9] | 86% [76, 92] | 12% | 0.160 | 0 |
| 24-40 | remainder_clamped |  | 77 | 4% [1, 11] | 84% [75, 91] | 12% | 0.085 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 0% [0, 5] | 84% [75, 91] | 16% | 0.182 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +23 pts [+13, +35]
- remainder - remainder_clamped: +8 pts [+3, +14]

Labels: J-mediated 25, non-J 1, both 2, neither 49
