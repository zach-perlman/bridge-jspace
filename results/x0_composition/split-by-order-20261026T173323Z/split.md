# The split by sentence order (descriptive, after the data)

J++ extra loss per reader and the gap (recall minus lookup, paired resamples) at the layer fixed in advance, by where the original bridge's locker sentence sits relative to the asked pick. Fresh scenes are the README's matched scenes (both locker sentences before the pick by construction). The pre-registered numbers are the main test's 'all' rows. Cluster bootstrap over bridge entities (10000 resamples, seed 0). Lookup switch: the share of lookups the whole change switches (the lookup's extra loss is a share of those switches, so it is measurable only where they are many). UNVERIFIED.

| model | design | locker vs pick | n | lookup switch | lookup extra loss | recall extra loss | gap |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | two people swap | all | 200 | 0.53 | -0.03 [-0.08, 0.03] | 0.50 [0.41, 0.57] | 0.53 [0.42, 0.61] |
| qwen3.5-9b | two people swap | before | 100 | 0.86 | 0.01 [-0.04, 0.07] | 0.35 [0.26, 0.43] | 0.34 [0.23, 0.43] |
| qwen3.5-9b | two people swap | after | 100 | 0.19 | -0.21 [-0.43, -0.05] | 0.65 [0.57, 0.73] | 0.86 [0.67, 1.10] |
| qwen3.5-9b | only the asked pick | all | 200 | 0.53 | -0.02 [-0.05, 0.02] | 0.37 [0.29, 0.43] | 0.39 [0.30, 0.46] |
| qwen3.5-9b | only the asked pick | before | 100 | 0.87 | 0.00 [0.00, 0.00] | 0.17 [0.11, 0.23] | 0.17 [0.11, 0.23] |
| qwen3.5-9b | only the asked pick | after | 100 | 0.19 | -0.11 [-0.29, 0.10] | 0.57 [0.47, 0.67] | 0.68 [0.45, 0.88] |
| qwen3.5-9b | only the asked pick (replication, fresh scenes) | all | 200 | 0.99 | -0.01 [-0.02, 0.00] | 0.12 [0.06, 0.19] | 0.13 [0.07, 0.19] |
| qwen3.5-9b | only the asked pick (replication, fresh scenes) | before | 200 | 0.99 | -0.01 [-0.02, 0.00] | 0.12 [0.06, 0.19] | 0.13 [0.07, 0.19] |
| qwen3.6-27b | two people swap | all | 200 | 0.43 | 0.14 [0.08, 0.20] | 0.74 [0.66, 0.80] | 0.60 [0.50, 0.69] |
| qwen3.6-27b | two people swap | before | 101 | 0.76 | 0.14 [0.07, 0.22] | 0.67 [0.58, 0.76] | 0.52 [0.40, 0.65] |
| qwen3.6-27b | two people swap | after | 99 | 0.09 | 0.11 [0.00, 0.40] | 0.81 [0.71, 0.91] | 0.70 [0.40, 0.88] |
| qwen3.6-27b | only the asked pick | all | 200 | 0.47 | 0.05 [0.01, 0.09] | 0.61 [0.51, 0.69] | 0.56 [0.45, 0.65] |
| qwen3.6-27b | only the asked pick | before | 103 | 0.81 | 0.01 [0.00, 0.04] | 0.49 [0.39, 0.60] | 0.48 [0.37, 0.59] |
| qwen3.6-27b | only the asked pick | after | 97 | 0.12 | 0.33 [0.10, 0.60] | 0.73 [0.58, 0.86] | 0.40 [0.05, 0.68] |
| qwen3.6-27b | only the asked pick (replication, fresh scenes) | all | 200 | 0.99 | 0.01 [0.00, 0.02] | 0.37 [0.28, 0.46] | 0.37 [0.27, 0.46] |
| qwen3.6-27b | only the asked pick (replication, fresh scenes) | before | 200 | 0.99 | 0.01 [0.00, 0.02] | 0.37 [0.28, 0.46] | 0.37 [0.27, 0.46] |
| qwen3.5-122b-a10b | two people swap | all | 200 | 0.45 | 0.00 [-0.06, 0.06] | 0.32 [0.22, 0.41] | 0.32 [0.20, 0.43] |
| qwen3.5-122b-a10b | two people swap | before | 85 | 0.89 | -0.01 [-0.08, 0.06] | 0.20 [0.10, 0.30] | 0.21 [0.10, 0.33] |
| qwen3.5-122b-a10b | two people swap | after | 115 | 0.11 | 0.08 [0.00, 0.23] | 0.41 [0.26, 0.54] | 0.33 [0.09, 0.53] |
| qwen3.5-122b-a10b | only the asked pick | all | 200 | 0.47 | -0.01 [-0.06, 0.04] | 0.27 [0.16, 0.36] | 0.28 [0.15, 0.39] |
| qwen3.5-122b-a10b | only the asked pick | before | 85 | 0.94 | -0.01 [-0.07, 0.04] | 0.10 [0.03, 0.17] | 0.11 [0.02, 0.20] |
| qwen3.5-122b-a10b | only the asked pick | after | 115 | 0.12 | 0.00 [0.00, 0.00] | 0.40 [0.25, 0.54] | 0.40 [0.25, 0.54] |
| qwen3.5-122b-a10b | only the asked pick (replication, fresh scenes) | all | 200 | 1.00 | 0.00 [0.00, 0.00] | 0.06 [0.03, 0.09] | 0.06 [0.03, 0.09] |
| qwen3.5-122b-a10b | only the asked pick (replication, fresh scenes) | before | 200 | 1.00 | 0.00 [0.00, 0.00] | 0.06 [0.03, 0.09] | 0.06 [0.03, 0.09] |
| muse-glimmer-30b | two people swap | all | 200 | 0.35 | -0.10 [-0.15, -0.04] | 0.75 [0.61, 0.87] | 0.85 [0.68, 0.98] |
| muse-glimmer-30b | two people swap | before | 92 | 0.65 | -0.07 [-0.12, -0.02] | 0.68 [0.46, 0.88] | 0.75 [0.51, 0.95] |
| muse-glimmer-30b | two people swap | after | 108 | 0.09 | -0.30 [-0.44, 0.00] | 0.80 [0.65, 0.92] | 1.10 [0.83, 1.30] |
| muse-glimmer-30b | only the asked pick | all | 200 | 0.43 | -0.01 [-0.04, 0.00] | 0.66 [0.53, 0.78] | 0.67 [0.53, 0.80] |
| muse-glimmer-30b | only the asked pick | before | 95 | 0.80 | 0.00 [0.00, 0.00] | 0.54 [0.32, 0.75] | 0.54 [0.32, 0.75] |
| muse-glimmer-30b | only the asked pick | after | 105 | 0.10 | -0.10 [-0.29, 0.00] | 0.76 [0.64, 0.87] | 0.86 [0.65, 1.10] |
| muse-glimmer-30b | only the asked pick (replication, fresh scenes) | all | 200 | 0.94 | -0.01 [-0.03, 0.02] | 0.31 [0.16, 0.45] | 0.32 [0.15, 0.46] |
| muse-glimmer-30b | only the asked pick (replication, fresh scenes) | before | 200 | 0.94 | -0.01 [-0.03, 0.02] | 0.31 [0.16, 0.45] | 0.32 [0.15, 0.46] |
