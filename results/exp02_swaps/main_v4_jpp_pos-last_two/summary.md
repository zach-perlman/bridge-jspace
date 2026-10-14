# exp02_swaps / main_v4_jpp_pos-last_two

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 16% [9, 25] | 82% [72, 89] | 3% | 0.010 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.035 | 0 |
| 24-40 | full_probe |  | 77 | 17% [10, 27] | 77% [66, 85] | 6% | 0.073 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.154 | 0 |
| 24-40 | jpart |  | 77 | 17% [10, 27] | 79% [69, 87] | 4% | 0.017 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.043 | 0 |
| 24-40 | remainder |  | 77 | 1% [0, 7] | 91% [82, 96] | 8% | 0.077 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 91% [82, 96] | 8% | 0.151 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 92% [84, 96] | 6% | 0.090 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 1% [0, 7] | 88% [79, 94] | 10% | 0.171 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +16 pts [+8, +23]
- remainder - remainder_clamped: +0 pts [+0, +0]

Labels: J-mediated 12, non-J 0, both 1, neither 64
