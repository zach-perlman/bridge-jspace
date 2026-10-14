# exp02_swaps / gate_v3

Items: eligible 67, clean_wrong 16, multi_token_answer 7

| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | items with skipped layers |
|---|---|---|---|---|---|---|---|---|
| 16-32 | raw_jlens |  | 67 | 19% [12, 30] | 76% [65, 85] | 4% | 0.006 | 0 |
| 16-32 | full_probe |  | 67 | 19% [12, 30] | 46% [35, 58] | 34% | 0.091 | 0 |
| 24-40 | raw_jlens |  | 67 | 46% [35, 58] | 46% [35, 58] | 7% | 0.009 | 0 |
| 24-40 | full_probe |  | 67 | 25% [16, 37] | 52% [40, 64] | 22% | 0.071 | 0 |
| 32-48 | raw_jlens |  | 67 | 51% [39, 62] | 36% [25, 48] | 13% | 0.008 | 0 |
| 32-48 | full_probe |  | 67 | 27% [18, 39] | 51% [39, 62] | 22% | 0.063 | 0 |
| 24-48 | raw_jlens |  | 67 | 52% [40, 64] | 39% [28, 51] | 9% | 0.007 | 0 |
| 24-48 | full_probe |  | 67 | 24% [15, 35] | 48% [36, 60] | 28% | 0.064 | 0 |

Gate: band 32-48, full-probe flip rate 27% (threshold 30%): STOP and debug.
