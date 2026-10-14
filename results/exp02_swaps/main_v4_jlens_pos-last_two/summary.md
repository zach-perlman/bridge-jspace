# exp02_swaps / main_v4_jlens_pos-last_two

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 12% [6, 21] | 86% [76, 92] | 3% | 0.010 | 0 |
| 24-40 | raw_jlens | yes | 77 | 1% [0, 7] | 99% [93, 100] | 0% | 0.044 | 0 |
| 24-40 | full_probe |  | 77 | 17% [10, 27] | 77% [66, 85] | 6% | 0.073 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.154 | 0 |
| 24-40 | jpart |  | 77 | 10% [5, 19] | 87% [78, 93] | 3% | 0.015 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.045 | 0 |
| 24-40 | remainder |  | 77 | 5% [2, 13] | 87% [78, 93] | 8% | 0.076 | 0 |
| 24-40 | remainder | yes | 77 | 3% [1, 9] | 91% [82, 96] | 6% | 0.157 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.084 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 1% [0, 7] | 88% [79, 94] | 10% | 0.176 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +5 pts [-1, +12]
- remainder - remainder_clamped: +4 pts [+0, +9]

Labels: J-mediated 7, non-J 0, both 1, neither 69
