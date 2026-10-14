# exp02_swaps / main_v4_jpp_pos-earlier

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 31% [22, 42] | 66% [55, 76] | 3% | 0.010 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.038 | 0 |
| 24-40 | full_probe |  | 77 | 16% [9, 25] | 75% [65, 84] | 9% | 0.064 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.144 | 0 |
| 24-40 | jpart |  | 77 | 35% [25, 46] | 61% [50, 71] | 4% | 0.018 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.039 | 0 |
| 24-40 | remainder |  | 77 | 1% [0, 7] | 88% [79, 94] | 10% | 0.068 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.146 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 95% [87, 98] | 4% | 0.079 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 1% [0, 7] | 92% [84, 96] | 6% | 0.157 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +34 pts [+23, +45]
- remainder - remainder_clamped: +0 pts [-4, +4]

Labels: J-mediated 27, non-J 1, both 0, neither 49
