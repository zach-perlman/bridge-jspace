# exp02 edit size: edit_size_v1

Runs: {'jpp': 'main_v4_jpp', 'jlens': 'main_v4_jlens'}. Edit size = `edit_ratio`: |edit| / |h| at the final position, mean over the band's layers.

## 1. Flip rate and edit size per condition

| lens | condition | null | n | flip [95% CI] | edit ratio (median) |
|---|---|---|---|---|---|
| jpp | raw_jlens |  | 77 | 49% [38, 60] | 0.0085 |
| jpp | raw_jlens | yes | 77 | 0% [0, 5] | 0.0338 |
| jpp | jpart |  | 77 | 52% [41, 63] | 0.0159 |
| jpp | jpart | yes | 77 | 0% [0, 5] | 0.0437 |
| jpp | full_probe |  | 77 | 27% [19, 38] | 0.0736 |
| jpp | full_probe | yes | 77 | 1% [0, 7] | 0.1611 |
| jpp | remainder |  | 77 | 8% [4, 16] | 0.0777 |
| jpp | remainder | yes | 77 | 1% [0, 7] | 0.1541 |
| jpp | remainder_clamped |  | 77 | 1% [0, 7] | 0.0897 |
| jpp | remainder_clamped | yes | 77 | 0% [0, 5] | 0.1792 |
| jlens | raw_jlens |  | 77 | 40% [30, 51] | 0.0084 |
| jlens | raw_jlens | yes | 77 | 0% [0, 5] | 0.0419 |
| jlens | jpart |  | 77 | 35% [25, 46] | 0.0141 |
| jlens | jpart | yes | 77 | 1% [0, 7] | 0.0448 |
| jlens | full_probe |  | 77 | 27% [19, 38] | 0.0736 |
| jlens | full_probe | yes | 77 | 1% [0, 7] | 0.1611 |
| jlens | remainder |  | 77 | 12% [6, 21] | 0.0768 |
| jlens | remainder | yes | 77 | 3% [1, 9] | 0.1596 |
| jlens | remainder_clamped |  | 77 | 4% [1, 11] | 0.0850 |
| jlens | remainder_clamped | yes | 77 | 0% [0, 5] | 0.1818 |

## 2. Within each lens: does the J-part edit's size predict a flip?

| lens | flipped: n, median edit | kept: n, median edit | AUC |
|---|---|---|---|
| jpp | 40, 0.0154 | 37, 0.0167 | 0.48 |
| jlens | 27, 0.0139 | 50, 0.0144 | 0.49 |

## 3. J++ against the J-lens at matched edit size (J-part swap)

| edit quartile | edit range | J++ flips | J-lens flips |
|---|---|---|---|
| 1 | 0.0073-0.0123 | 6/11 (55% [28, 79]) | 11/27 (41% [25, 59]) |
| 2 | 0.0125-0.0151 | 11/21 (52% [32, 72]) | 5/18 (28% [12, 51]) |
| 3 | 0.0152-0.0194 | 11/22 (50% [31, 69]) | 6/17 (35% [17, 59]) |
| 4 | 0.0194-0.0404 | 12/23 (52% [33, 71]) | 5/15 (33% [15, 58]) |

Paired over 77 questions: flipped by J++ only 13, by the J-lens only 0 (exact McNemar p = 0.00024).
J++'s J-part edit over the J-lens's, per question: median 1.21 (quartiles 1.06, 1.36).
Questions where J++'s edit is no bigger than the J-lens's: 14; flips there: J++ 4, J-lens 3.
