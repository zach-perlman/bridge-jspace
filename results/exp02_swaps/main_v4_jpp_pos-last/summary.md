# exp02_swaps / main_v4_jpp_pos-last

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 1% [0, 7] | 97% [91, 99] | 1% | 0.010 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.035 | 0 |
| 24-40 | full_probe |  | 77 | 8% [4, 16] | 87% [78, 93] | 5% | 0.073 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.149 | 0 |
| 24-40 | jpart |  | 77 | 8% [4, 16] | 91% [82, 96] | 1% | 0.018 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.044 | 0 |
| 24-40 | remainder |  | 77 | 3% [1, 9] | 94% [86, 97] | 4% | 0.077 | 0 |
| 24-40 | remainder | yes | 77 | 0% [0, 5] | 96% [89, 99] | 4% | 0.150 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 95% [87, 98] | 4% | 0.089 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 0% [0, 5] | 90% [81, 95] | 10% | 0.171 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +5 pts [+0, +12]
- remainder - remainder_clamped: +1 pts [+0, +4]

Labels: J-mediated 5, non-J 0, both 1, neither 71
