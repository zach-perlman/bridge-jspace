# exp02_swaps / main_chat_stmt_h200

Items: eligible 76, clean_wrong 14

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 32-48 | raw_jlens |  | 76 | 59% [48, 70] | 34% [25, 45] | 7% | 0.007 | 0 |
| 32-48 | raw_jlens | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.015 | 0 |
| 32-48 | full_probe |  | 76 | 29% [20, 40] | 61% [49, 71] | 11% | 0.066 | 0 |
| 32-48 | full_probe | yes | 76 | 1% [0, 7] | 87% [77, 93] | 12% | 0.159 | 0 |
| 32-48 | jpart |  | 76 | 50% [39, 61] | 42% [32, 53] | 8% | 0.011 | 0 |
| 32-48 | jpart | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.018 | 0 |
| 32-48 | remainder |  | 76 | 7% [3, 14] | 84% [74, 91] | 9% | 0.068 | 0 |
| 32-48 | remainder | yes | 76 | 0% [0, 5] | 91% [82, 95] | 9% | 0.171 | 0 |
| 32-48 | remainder_clamped |  | 76 | 3% [1, 9] | 91% [82, 95] | 7% | 0.086 | 0 |
| 32-48 | remainder_clamped | yes | 76 | 0% [0, 5] | 83% [73, 90] | 17% | 0.182 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +43 pts [+32, +54]
- remainder - remainder_clamped: +4 pts [+0, +9]

Labels: J-mediated 36, non-J 0, both 2, neither 38
