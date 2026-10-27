# Duplicate check: the other person's pick of the changed item before or after the asked pick

Dan 26 Oct ~21:45; descriptive, after the data. One-pick runs only. Extra loss = (switches without the random part - switches without the part) / whole-change switches, per group; before - after on the same cluster-bootstrap draws over bridge entities (10000, seed 0). 'no difference' = |diff| < 0.1 and the CI covering 0. UNVERIFIED.

| model | run | measure | n before / after (none) | before | after | before - after | no difference |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | x0_necessity/qwen35_9b_x0_single_r2 | jpp_lookup | 105 / 95 (0) | −0.01 [−0.06, 0.03] | −0.03 [−0.11, 0.00] | 0.02 [−0.05, 0.11] | yes |
| qwen3.5-9b | x0_necessity/qwen35_9b_x0_single_r2 | jpp_recall | 105 / 95 (0) | 0.14 [0.08, 0.21] | 0.61 [0.49, 0.70] | −0.47 [−0.58, −0.33] | **no** |
| qwen3.5-9b | x0_necessity/qwen35_9b_x0_single_r2 | gap | 105 / 95 (0) | 0.15 [0.07, 0.24] | 0.64 [0.52, 0.74] | −0.49 [−0.63, −0.33] | **no** |
| qwen3.5-9b | x0_massmean/qwen35_9b_x45g_one_r2 | pointer_lookup | 105 / 95 (0) | 0.41 [0.30, 0.52] | 0.42 [0.23, 0.64] | −0.01 [−0.29, 0.24] | yes |
| qwen3.5-9b | x0_massmean/qwen35_9b_x0_massmean_lf | pointer_lookup | 58 / 15 (0) | 0.44 [0.32, 0.56] | 0.67 [0.38, 0.90] | −0.23 [−0.50, 0.09] | **no** |
| qwen3.6-27b | x0_necessity/x0_single_27b_r2 | jpp_lookup | 94 / 106 (0) | 0.04 [0.00, 0.09] | 0.08 [0.00, 0.20] | −0.04 [−0.17, 0.07] | yes |
| qwen3.6-27b | x0_necessity/x0_single_27b_r2 | jpp_recall | 94 / 106 (0) | 0.44 [0.29, 0.56] | 0.75 [0.62, 0.86] | −0.31 [−0.50, −0.13] | **no** |
| qwen3.6-27b | x0_necessity/x0_single_27b_r2 | gap | 94 / 106 (0) | 0.40 [0.25, 0.53] | 0.67 [0.52, 0.80] | −0.27 [−0.47, −0.09] | **no** |
| qwen3.6-27b | x0_massmean/x45g_one_27b_r2 | pointer_lookup | 94 / 106 (0) | 0.14 [0.06, 0.22] | 0.31 [0.15, 0.47] | −0.16 [−0.33, −0.01] | **no** |
| qwen3.6-27b | x0_massmean/x0_massmean_lf_27b | pointer_lookup | 53 / 17 (0) | 0.09 [0.02, 0.17] | 0.29 [0.09, 0.50] | −0.20 [−0.42, 0.01] | **no** |
| qwen3.5-122b-a10b | x0_necessity/qwen35_122b_x0_single | jpp_lookup | 85 / 115 (0) | 0.00 [0.00, 0.00] | −0.03 [−0.14, 0.10] | 0.03 [−0.10, 0.14] | yes |
| qwen3.5-122b-a10b | x0_necessity/qwen35_122b_x0_single | jpp_recall | 85 / 115 (0) | 0.14 [0.05, 0.22] | 0.36 [0.22, 0.50] | −0.22 [−0.36, −0.10] | **no** |
| qwen3.5-122b-a10b | x0_necessity/qwen35_122b_x0_single | gap | 85 / 115 (0) | 0.14 [0.05, 0.22] | 0.39 [0.18, 0.58] | −0.25 [−0.45, −0.06] | **no** |
| qwen3.5-122b-a10b | x0_massmean/qwen35_122b_x0_massmean_grid | pointer_lookup | 42 / 12 (0) | 0.21 [0.09, 0.34] | 0.67 [0.38, 0.92] | −0.45 [−0.74, −0.14] | **no** |
| qwen3.5-122b-a10b | x0_massmean/qwen35_122b_x45g_one | pointer_lookup | not run yet | | | | |
| muse-glimmer-30b | x0_necessity/muse30b_x0_single | jpp_lookup | 99 / 101 (0) | 0.02 [0.00, 0.04] | −0.10 [−0.24, 0.00] | 0.12 [0.00, 0.27] | **no** |
| muse-glimmer-30b | x0_necessity/muse30b_x0_single | jpp_recall | 99 / 101 (0) | 0.54 [0.38, 0.74] | 0.77 [0.60, 0.91] | −0.23 [−0.45, 0.03] | **no** |
| muse-glimmer-30b | x0_necessity/muse30b_x0_single | gap | 99 / 101 (0) | 0.52 [0.37, 0.72] | 0.87 [0.62, 1.09] | −0.34 [−0.59, −0.06] | **no** |
| muse-glimmer-30b | x0_massmean/muse30b_x45g_one | pointer_lookup | 99 / 101 (0) | 0.30 [0.20, 0.40] | 0.40 [0.19, 0.62] | −0.10 [−0.34, 0.13] | yes |
| muse-glimmer-30b | x0_massmean/muse30b_x0_massmean_grid | pointer_lookup | 53 / 15 (0) | 0.32 [0.21, 0.44] | 0.43 [0.17, 0.73] | −0.11 [−0.43, 0.19] | **no** |

## Beside the split (agent, after the data): within each place of the changed item's locker sentence

A duplicate before the asked pick also names the changed item before the bridge word. Within 'its locker sentence before the pick' the item is named earlier in both groups; within 'after', only the duplicate names it earlier. x0 single runs, J++ k = 25.

| model | changed item's locker sentence | measure | n before / after | before | after | before - after |
|---|---|---|---|---|---|---|
| qwen3.5-9b | before the pick | jpp_lookup | 78 / 29 | −0.02 [−0.05, 0.00] | −0.04 [−0.13, 0.00] | 0.03 [−0.04, 0.12] |
| qwen3.5-9b | before the pick | jpp_recall | 78 / 29 | 0.08 [0.03, 0.13] | 0.31 [0.12, 0.50] | −0.23 [−0.44, −0.02] |
| qwen3.5-9b | before the pick | gap | 78 / 29 | 0.10 [0.04, 0.15] | 0.35 [0.13, 0.57] | −0.25 [−0.47, −0.04] |
| qwen3.5-9b | after the pick | jpp_lookup | 27 / 66 | 0.00 [−0.18, 0.27] | 0.00 [0.00, 0.00] | 0.00 [−0.18, 0.27] |
| qwen3.5-9b | after the pick | jpp_recall | 27 / 66 | 0.32 [0.09, 0.58] | 0.75 [0.62, 0.84] | −0.43 [−0.67, −0.15] |
| qwen3.5-9b | after the pick | gap | 27 / 66 | 0.32 [−0.07, 0.70] | 0.75 [0.62, 0.84] | −0.43 [−0.83, −0.02] |
| qwen3.6-27b | before the pick | jpp_lookup | 72 / 35 | 0.02 [0.00, 0.05] | 0.05 [0.00, 0.16] | −0.03 [−0.14, 0.04] |
| qwen3.6-27b | before the pick | jpp_recall | 72 / 35 | 0.39 [0.23, 0.54] | 0.74 [0.44, 1.00] | −0.35 [−0.69, 0.00] |
| qwen3.6-27b | before the pick | gap | 72 / 35 | 0.37 [0.22, 0.51] | 0.69 [0.41, 0.94] | −0.32 [−0.62, 0.01] |
| qwen3.6-27b | after the pick | jpp_lookup | 22 / 71 | 0.17 [0.00, 0.38] | 0.33 [0.00, 1.00] | −0.17 [−0.89, 0.31] |
| qwen3.6-27b | after the pick | jpp_recall | 22 / 71 | 0.55 [0.33, 0.77] | 0.75 [0.66, 0.86] | −0.20 [−0.45, 0.03] |
| qwen3.6-27b | after the pick | gap | 22 / 71 | 0.38 [0.06, 0.71] | 0.42 [−0.28, 0.84] | −0.04 [−0.62, 0.70] |
| qwen3.5-122b-a10b | before the pick | jpp_lookup | 57 / 34 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.5-122b-a10b | before the pick | jpp_recall | 57 / 34 | 0.08 [0.00, 0.16] | 0.19 [0.03, 0.41] | −0.11 [−0.35, 0.07] |
| qwen3.5-122b-a10b | before the pick | gap | 57 / 34 | 0.08 [0.00, 0.16] | 0.19 [0.03, 0.41] | −0.11 [−0.35, 0.07] |
| qwen3.5-122b-a10b | after the pick | jpp_lookup | 28 / 81 | 0.00 [0.00, 0.00] | −0.07 [−0.32, 0.29] | 0.07 [−0.29, 0.32] |
| qwen3.5-122b-a10b | after the pick | jpp_recall | 28 / 81 | 0.25 [0.10, 0.40] | 0.44 [0.25, 0.63] | −0.19 [−0.41, −0.00] |
| qwen3.5-122b-a10b | after the pick | gap | 28 / 81 | 0.25 [0.10, 0.40] | 0.51 [0.14, 0.82] | −0.26 [−0.60, 0.13] |
| muse-glimmer-30b | before the pick | jpp_lookup | 73 / 34 | 0.02 [0.00, 0.05] | −0.11 [−0.25, 0.00] | 0.13 [0.00, 0.28] |
| muse-glimmer-30b | before the pick | jpp_recall | 73 / 34 | 0.46 [0.30, 0.68] | 0.63 [0.33, 0.95] | −0.17 [−0.56, 0.21] |
| muse-glimmer-30b | before the pick | gap | 73 / 34 | 0.45 [0.29, 0.66] | 0.74 [0.36, 1.12] | −0.30 [−0.72, 0.15] |
| muse-glimmer-30b | after the pick | jpp_lookup | 26 / 67 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | after the pick | jpp_recall | 26 / 67 | 0.82 [0.33, 1.50] | 0.83 [0.68, 0.98] | −0.01 [−0.53, 0.73] |
| muse-glimmer-30b | after the pick | gap | 26 / 67 | 0.82 [0.33, 1.50] | 0.83 [0.67, 0.97] | −0.01 [−0.52, 0.76] |
