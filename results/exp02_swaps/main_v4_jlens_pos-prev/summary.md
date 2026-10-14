# exp02_swaps / main_v4_jlens_pos-prev

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 3% [1, 9] | 97% [91, 99] | 0% | 0.011 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.060 | 0 |
| 24-40 | full_probe |  | 77 | 5% [2, 13] | 92% [84, 96] | 3% | 0.069 | 0 |
| 24-40 | full_probe | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.159 | 0 |
| 24-40 | jpart |  | 77 | 3% [1, 9] | 96% [89, 99] | 1% | 0.017 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.055 | 0 |
| 24-40 | remainder |  | 77 | 1% [0, 7] | 95% [87, 98] | 4% | 0.073 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 96% [89, 99] | 3% | 0.161 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 96% [89, 99] | 3% | 0.082 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.171 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +1 pts [+0, +4]
- remainder - remainder_clamped: +0 pts [+0, +0]

Labels: J-mediated 1, non-J 0, both 1, neither 75
