# exp02_swaps / main_v4_jlens_pos-last

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 1% [0, 7] | 97% [91, 99] | 1% | 0.010 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.044 | 0 |
| 24-40 | full_probe |  | 77 | 8% [4, 16] | 87% [78, 93] | 5% | 0.073 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.149 | 0 |
| 24-40 | jpart |  | 77 | 4% [1, 11] | 96% [89, 99] | 0% | 0.015 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 99% [93, 100] | 1% | 0.045 | 0 |
| 24-40 | remainder |  | 77 | 1% [0, 7] | 92% [84, 96] | 6% | 0.076 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 95% [87, 98] | 4% | 0.155 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.083 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 0% [0, 5] | 90% [81, 95] | 10% | 0.177 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +3 pts [-3, +8]
- remainder - remainder_clamped: +0 pts [-4, +4]

Labels: J-mediated 3, non-J 1, both 0, neither 73
