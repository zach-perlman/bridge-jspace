# exp02_swaps / main_v4_jlens_pos-earlier

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 26% [17, 37] | 70% [59, 79] | 4% | 0.008 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.042 | 0 |
| 24-40 | full_probe |  | 77 | 16% [9, 25] | 75% [65, 84] | 9% | 0.064 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 94% [86, 97] | 5% | 0.144 | 0 |
| 24-40 | jpart |  | 77 | 23% [15, 34] | 74% [63, 83] | 3% | 0.015 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.038 | 0 |
| 24-40 | remainder |  | 77 | 4% [1, 11] | 87% [78, 93] | 9% | 0.067 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 92% [84, 96] | 6% | 0.145 | 0 |
| 24-40 | remainder_clamped |  | 77 | 3% [1, 9] | 92% [84, 96] | 5% | 0.074 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 3% [1, 9] | 91% [82, 96] | 6% | 0.159 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +19 pts [+9, +30]
- remainder - remainder_clamped: +1 pts [+0, +4]

Labels: J-mediated 18, non-J 2, both 0, neither 57
