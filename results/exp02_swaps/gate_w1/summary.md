# exp02_swaps / gate_w1

Items: eligible 66, clean_wrong 16, multi_token_answer 7, no_probe:June 1

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 16-32 | raw_jlens |  | 66 | 20% [12, 31] | 77% [66, 86] | 3% | 0.006 | 0 |
| 16-32 | full_probe |  | 66 | 2% [0, 8] | 97% [90, 99] | 2% | 0.015 | 0 |
| 24-40 | raw_jlens |  | 66 | 47% [35, 59] | 47% [35, 59] | 6% | 0.009 | 0 |
| 24-40 | full_probe |  | 66 | 6% [2, 15] | 92% [83, 97] | 2% | 0.017 | 0 |
| 32-48 | raw_jlens |  | 66 | 55% [43, 66] | 38% [27, 50] | 8% | 0.008 | 0 |
| 32-48 | full_probe |  | 66 | 5% [2, 13] | 95% [87, 98] | 0% | 0.016 | 0 |
| 24-48 | raw_jlens |  | 66 | 55% [43, 66] | 41% [30, 53] | 5% | 0.007 | 0 |
| 24-48 | full_probe |  | 66 | 8% [3, 17] | 94% [85, 98] | -2% | 0.015 | 0 |

Gate: band 24-48, full-probe flip rate 8% (threshold 30%): STOP and debug.
