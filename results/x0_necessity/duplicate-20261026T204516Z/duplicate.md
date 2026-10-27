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
