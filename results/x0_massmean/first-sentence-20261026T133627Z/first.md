# Does the pointer result rest on the first sentence? (after the data, descriptive)

The main test's pointer removal on its one-change items, the items the whole change switches, by where the original and the changed bridge's locker sentences sit. Extra loss without the pointer directions (vs their random part) and the switch rate with only the pointer part; cluster bootstrap over bridge entities. UNVERIFIED.

| model | reader | group | n | extra loss without the pointer | only the pointer part: switch rate |
|---|---|---|---|---|---|
| qwen3.5-9b | lookup | (a) first sentence | 41 | 0.66 [0.53, 0.79] | 0.56 [0.41, 0.72] |
| qwen3.5-9b | lookup | (b) first locker, not first sentence | 22 | 0.23 [0.05, 0.45] | 0.14 [0.00, 0.27] |
| qwen3.5-9b | lookup | (c) neither | 9 | 0.33 [0.00, 0.75] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | lookup | **(a) − (b)**, paired | | 0.43 [0.18, 0.65] | 0.42 [0.25, 0.62] |
| qwen3.5-9b | lookup | **(a) − (b, c)**, paired | | 0.40 [0.18, 0.60] | 0.46 [0.31, 0.64] |
| qwen3.5-9b | recall | (a) first sentence | 41 | 0.17 [0.07, 0.29] | 0.12 [0.03, 0.21] |
| qwen3.5-9b | recall | (b) first locker, not first sentence | 22 | 0.05 [0.00, 0.14] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | recall | (c) neither | 9 | 0.11 [0.00, 0.38] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | recall | **(a) − (b)**, paired | | 0.13 [0.01, 0.25] | 0.12 [0.03, 0.21] |
| qwen3.5-9b | recall | **(a) − (b, c)**, paired | | 0.11 [-0.02, 0.24] | 0.12 [0.03, 0.22] |
| qwen3.6-27b | lookup | (a) first sentence | 37 | 0.24 [0.12, 0.36] | 0.16 [0.05, 0.30] |
| qwen3.6-27b | lookup | (b) first locker, not first sentence | 20 | 0.05 [0.00, 0.17] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | lookup | (c) neither | 13 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | lookup | **(a) − (b)**, paired | | 0.19 [0.00, 0.35] | 0.16 [0.05, 0.30] |
| qwen3.6-27b | lookup | **(a) − (b, c)**, paired | | 0.21 [0.05, 0.35] | 0.16 [0.04, 0.31] |
| qwen3.6-27b | recall | (a) first sentence | 25 | 0.24 [0.04, 0.46] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | recall | (b) first locker, not first sentence | 15 | 0.07 [0.00, 0.19] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | recall | (c) neither | 9 | 0.11 [0.00, 0.27] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | recall | **(a) − (b)**, paired | | 0.17 [-0.08, 0.43] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | recall | **(a) − (b, c)**, paired | | 0.16 [-0.08, 0.40] | 0.00 [0.00, 0.00] |
| qwen3.5-122b-a10b | lookup | (a) first sentence | 25 | 0.52 [0.36, 0.68] | 0.28 [0.11, 0.46] |
| qwen3.5-122b-a10b | lookup | (b) first locker, not first sentence | 19 | 0.21 [0.05, 0.39] | 0.32 [0.12, 0.47] |
| qwen3.5-122b-a10b | lookup | (c) neither | 10 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.5-122b-a10b | lookup | **(a) − (b)**, paired | | 0.31 [0.10, 0.53] | -0.04 [-0.31, 0.26] |
| qwen3.5-122b-a10b | lookup | **(a) − (b, c)**, paired | | 0.38 [0.21, 0.56] | 0.07 [-0.16, 0.32] |
| qwen3.5-122b-a10b | recall | (a) first sentence | 24 | 0.17 [0.00, 0.39] | 0.08 [0.00, 0.21] |
| qwen3.5-122b-a10b | recall | (b) first locker, not first sentence | 19 | 0.16 [0.00, 0.33] | 0.11 [0.00, 0.28] |
| qwen3.5-122b-a10b | recall | (c) neither | 9 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.5-122b-a10b | recall | **(a) − (b)**, paired | | 0.01 [-0.22, 0.25] | -0.02 [-0.23, 0.16] |
| qwen3.5-122b-a10b | recall | **(a) − (b, c)**, paired | | 0.06 [-0.15, 0.29] | 0.01 [-0.14, 0.17] |
| muse-glimmer-30b | lookup | (a) first sentence | 39 | 0.51 [0.37, 0.67] | 0.33 [0.20, 0.49] |
| muse-glimmer-30b | lookup | (b) first locker, not first sentence | 21 | 0.14 [0.00, 0.29] | 0.14 [0.00, 0.26] |
| muse-glimmer-30b | lookup | (c) neither | 7 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | lookup | **(a) − (b)**, paired | | 0.37 [0.20, 0.56] | 0.19 [0.03, 0.37] |
| muse-glimmer-30b | lookup | **(a) − (b, c)**, paired | | 0.41 [0.25, 0.59] | 0.23 [0.09, 0.39] |
| muse-glimmer-30b | recall | (a) first sentence | 23 | 0.17 [0.00, 0.41] | 0.09 [0.00, 0.22] |
| muse-glimmer-30b | recall | (b) first locker, not first sentence | 12 | 0.08 [0.00, 0.23] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | recall | (c) neither | 3 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | recall | **(a) − (b)**, paired | | 0.09 [-0.15, 0.37] | 0.09 [0.00, 0.22] |
| muse-glimmer-30b | recall | **(a) − (b, c)**, paired | | 0.11 [-0.10, 0.37] | 0.09 [0.00, 0.22] |
