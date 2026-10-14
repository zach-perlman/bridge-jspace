# exp02_swaps / gate

Items: eligible 66, clean_wrong 16, multi_token_answer 7, no_probe:June 1

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 16-32 | raw_jlens |  | 66 | 20% [12, 31] | 77% [66, 86] | 3% | 0.006 | 0 |
| 16-32 | full_probe |  | 66 | 3% [1, 10] | 58% [46, 69] | 39% | 0.099 | 0 |
| 24-40 | raw_jlens |  | 66 | 47% [35, 59] | 47% [35, 59] | 6% | 0.009 | 0 |
| 24-40 | full_probe |  | 66 | 11% [5, 20] | 73% [61, 82] | 17% | 0.080 | 0 |
| 32-48 | raw_jlens |  | 66 | 55% [43, 66] | 38% [27, 50] | 8% | 0.008 | 0 |
| 32-48 | full_probe |  | 66 | 17% [10, 27] | 67% [55, 77] | 17% | 0.068 | 0 |
| 24-48 | raw_jlens |  | 66 | 55% [43, 66] | 41% [30, 53] | 5% | 0.007 | 0 |
| 24-48 | full_probe |  | 66 | 17% [10, 27] | 58% [46, 69] | 26% | 0.068 | 0 |

Gate: band 32-48, full-probe flip rate 17% (threshold 30%): STOP and debug.
