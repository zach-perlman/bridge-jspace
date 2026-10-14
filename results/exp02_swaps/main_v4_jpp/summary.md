# exp02_swaps / main_v4_jpp

Items: eligible 77, clean_wrong 13

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 24-40 | raw_jlens |  | 77 | 49% [38, 60] | 40% [30, 51] | 10% | 0.009 | 0 |
| 24-40 | raw_jlens | yes | 77 | 0% [0, 5] | 97% [91, 99] | 3% | 0.034 | 0 |
| 24-40 | full_probe |  | 77 | 27% [19, 38] | 55% [43, 65] | 18% | 0.074 | 0 |
| 24-40 | full_probe | yes | 77 | 1% [0, 7] | 88% [79, 94] | 10% | 0.161 | 0 |
| 24-40 | jpart |  | 77 | 52% [41, 63] | 39% [29, 50] | 9% | 0.016 | 0 |
| 24-40 | jpart | yes | 77 | 0% [0, 5] | 100% [95, 100] | 0% | 0.044 | 0 |
| 24-40 | remainder |  | 77 | 8% [4, 16] | 78% [67, 86] | 14% | 0.078 | 0 |
| 24-40 | remainder | yes | 77 | 1% [0, 7] | 87% [78, 93] | 12% | 0.154 | 0 |
| 24-40 | remainder_clamped |  | 77 | 1% [0, 7] | 87% [78, 93] | 12% | 0.090 | 0 |
| 24-40 | remainder_clamped | yes | 77 | 0% [0, 5] | 84% [75, 91] | 16% | 0.179 | 0 |

Paired bootstrap differences in flip rate:
- jpart - remainder: +44 pts [+32, +56]
- remainder - remainder_clamped: +6 pts [+1, +13]

Labels: J-mediated 39, non-J 0, both 1, neither 37
