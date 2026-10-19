# exp02_swaps / own_chat_stmt_h200

Items: eligible 76, clean_wrong 14

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 32-48 | raw_jlens |  | 76 | 59% [48, 70] | 34% [25, 45] | 7% | 0.007 | 0 |
| 32-48 | raw_jlens | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.015 | 0 |
| 32-48 | jpart |  | 76 | 50% [39, 61] | 42% [32, 53] | 8% | 0.011 | 0 |
| 32-48 | jpart | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.018 | 0 |
| 32-48 | jpart_minus_own |  | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.013 | 0 |
| 32-48 | jpart_minus_own | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.017 | 0 |
| 32-48 | jpart_matched |  | 76 | 11% [5, 19] | 84% [74, 91] | 5% | 0.044 | 0 |
| 32-48 | jpart_matched | yes | 76 | 0% [0, 5] | 100% [95, 100] | 0% | 0.055 | 0 |

Paired bootstrap differences in flip rate:
- jpart - jpart_matched: +39 pts [+29, +50]
- jpart - jpart_minus_own: +50 pts [+38, +61]
- jpart_minus_own - jpart_matched: -11 pts [-18, -4]
- raw_jlens - jpart_minus_own: +59 pts [+47, +70]

Labels: J-mediated 0, non-J 0, both 0, neither 0
