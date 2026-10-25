# J++ extra loss by swap and sentence order (descriptive, after the data)

Layer fixed in advance; 25 J++ directions; cluster bootstrap (10000 resamples). UNVERIFIED.

| model | swap | sentence order | n | lookup extra loss | recall extra loss | recall S_whole |
|---|---|---|---|---|---|---|
| qwen3.5-9b | two people swap | all | 200 | -0.03 [-0.08, 0.03] | 0.50 [0.41, 0.57] | 0.98 |
| qwen3.5-9b | two people swap | both locker sentences before the pick | 75 | -0.04 [-0.10, 0.02] | 0.23 [0.14, 0.31] | 1.00 |
| qwen3.5-9b | two people swap | only the original's before | 25 | 0.29 [0.07, 0.57] | 0.72 [0.57, 0.88] | 1.00 |
| qwen3.5-9b | two people swap | the original's after | 100 | -0.21 [-0.43, -0.05] | 0.65 [0.57, 0.73] | 0.97 |
| qwen3.5-9b | only the asked pick | all | 200 | -0.02 [-0.05, 0.02] | 0.37 [0.29, 0.43] | 0.95 |
| qwen3.5-9b | only the asked pick | both locker sentences before the pick | 73 | 0.00 [0.00, 0.00] | 0.06 [0.00, 0.12] | 0.99 |
| qwen3.5-9b | only the asked pick | only the original's before | 27 | 0.00 [0.00, 0.00] | 0.50 [0.33, 0.69] | 0.96 |
| qwen3.5-9b | only the asked pick | the original's after | 100 | -0.11 [-0.29, 0.10] | 0.57 [0.47, 0.67] | 0.93 |
| qwen3.5-9b | only the asked pick (replication, fresh scenes) | all | 200 | -0.01 [-0.02, 0.00] | 0.12 [0.06, 0.19] | 0.96 |
| qwen3.5-9b | only the asked pick (replication, fresh scenes) | both locker sentences before the pick | 200 | -0.01 [-0.02, 0.00] | 0.12 [0.06, 0.19] | 0.96 |
| qwen3.6-27b | two people swap | all | 200 | 0.14 [0.08, 0.20] | 0.74 [0.66, 0.80] | 0.75 |
| qwen3.6-27b | two people swap | both locker sentences before the pick | 69 | 0.14 [0.06, 0.21] | 0.73 [0.61, 0.83] | 0.74 |
| qwen3.6-27b | two people swap | only the original's before | 32 | 0.18 [0.00, 0.45] | 0.54 [0.32, 0.79] | 0.75 |
| qwen3.6-27b | two people swap | the original's after | 99 | 0.11 [0.00, 0.40] | 0.81 [0.71, 0.91] | 0.76 |
| qwen3.6-27b | only the asked pick | all | 200 | 0.05 [0.01, 0.09] | 0.61 [0.51, 0.69] | 0.73 |
| qwen3.6-27b | only the asked pick | both locker sentences before the pick | 70 | 0.00 [0.00, 0.00] | 0.46 [0.34, 0.57] | 0.71 |
| qwen3.6-27b | only the asked pick | only the original's before | 33 | 0.08 [0.00, 0.27] | 0.56 [0.32, 0.80] | 0.76 |
| qwen3.6-27b | only the asked pick | the original's after | 97 | 0.33 [0.10, 0.60] | 0.73 [0.58, 0.86] | 0.73 |
| qwen3.6-27b | only the asked pick (replication, fresh scenes) | all | 200 | 0.01 [0.00, 0.02] | 0.37 [0.28, 0.46] | 0.69 |
| qwen3.6-27b | only the asked pick (replication, fresh scenes) | both locker sentences before the pick | 200 | 0.01 [0.00, 0.02] | 0.37 [0.28, 0.46] | 0.69 |

qwen3.5-9b: the pointer directions' scenes (x0_massmean/qwen35_9b_x0_massmean_lf, n = 73) are the one-pick run's both-before scenes (n = 73; overlap 73).
qwen3.6-27b: the pointer directions' scenes (x0_massmean/x0_massmean_lf_27b, n = 70) are the one-pick run's both-before scenes (n = 70; overlap 70).
