# Batch 45g: two routes for the recall? (scored against the rules fixed in advance)

| run | model | scene set | reader | order | n | without J++ | without the pointer | without both | both − larger single | both − J++ |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | lookup | all | 200 | -0.05 [-0.09, 0.00] | 0.47 [0.37, 0.56] | 0.18 [0.07, 0.28] | -0.29 [-0.39, -0.18] (Alf) | 0.23 [0.11, 0.33] |
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | lookup | before | 100 | -0.01 [-0.05, 0.03] | 0.55 [0.45, 0.64] | 0.21 [0.10, 0.32] | -0.34 [-0.44, -0.22] (Alf) | 0.22 [0.11, 0.33] |
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | lookup | after | 100 | -0.20 [-0.40, -0.05] | 0.15 [-0.09, 0.39] | 0.05 [-0.13, 0.20] | -0.10 [-0.33, 0.14] (Alf) | 0.25 [0.08, 0.42] |
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | recall | all | 200 | 0.50 [0.41, 0.57] | 0.05 [0.02, 0.09] | 0.55 [0.47, 0.61] | 0.05 [-0.01, 0.11] (jpp) | 0.05 [-0.01, 0.11] |
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | recall | before | 100 | 0.35 [0.26, 0.43] | 0.10 [0.04, 0.16] | 0.38 [0.29, 0.46] | 0.03 [-0.08, 0.13] (jpp) | 0.03 [-0.08, 0.13] |
| qwen35_9b_x45g_swap_r2 | qwen3.5-9b | two people swap | recall | after | 100 | 0.65 [0.57, 0.73] | 0.00 [0.00, 0.00] | 0.72 [0.62, 0.82] | 0.07 [0.01, 0.14] (jpp) | 0.07 [0.01, 0.14] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | lookup | all | 200 | -0.02 [-0.05, 0.02] | 0.42 [0.33, 0.49] | 0.39 [0.30, 0.47] | -0.03 [-0.12, 0.07] (Alf) | 0.41 [0.31, 0.50] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | lookup | before | 100 | 0.00 [0.00, 0.00] | 0.46 [0.36, 0.56] | 0.44 [0.34, 0.53] | -0.02 [-0.13, 0.08] (Alf) | 0.44 [0.34, 0.53] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | lookup | after | 100 | -0.11 [-0.29, 0.10] | 0.21 [0.05, 0.39] | 0.16 [0.00, 0.32] | -0.05 [-0.24, 0.12] (Alf) | 0.26 [0.00, 0.50] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | recall | all | 200 | 0.37 [0.29, 0.43] | 0.05 [0.02, 0.09] | 0.59 [0.51, 0.66] | 0.23 [0.17, 0.28] (jpp) | 0.23 [0.17, 0.28] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | recall | before | 100 | 0.17 [0.11, 0.23] | 0.09 [0.04, 0.16] | 0.51 [0.41, 0.61] | 0.34 [0.22, 0.45] (jpp) | 0.34 [0.22, 0.45] |
| qwen35_9b_x45g_one_r2 | qwen3.5-9b | only the asked pick | recall | after | 100 | 0.57 [0.47, 0.67] | 0.01 [0.00, 0.04] | 0.68 [0.57, 0.78] | 0.11 [0.04, 0.19] (jpp) | 0.11 [0.04, 0.19] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | lookup | all | 200 | 0.14 [0.08, 0.20] | 0.14 [0.04, 0.24] | 0.33 [0.23, 0.43] | 0.19 [0.06, 0.33] (Alf) | 0.19 [0.06, 0.31] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | lookup | before | 101 | 0.14 [0.07, 0.22] | 0.13 [0.01, 0.24] | 0.32 [0.21, 0.44] | 0.18 [0.04, 0.33] (jpp) | 0.18 [0.04, 0.33] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | lookup | after | 99 | 0.11 [0.00, 0.40] | 0.22 [0.00, 0.50] | 0.33 [0.00, 0.62] | 0.11 [-0.00, 0.40] (Alf) | 0.22 [-0.25, 0.60] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | recall | all | 200 | 0.74 [0.66, 0.80] | -0.05 [-0.11, 0.01] | 0.59 [0.50, 0.67] | -0.15 [-0.23, -0.08] (jpp) | -0.15 [-0.23, -0.08] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | recall | before | 101 | 0.67 [0.58, 0.76] | -0.09 [-0.21, 0.00] | 0.31 [0.19, 0.43] | -0.36 [-0.48, -0.24] (jpp) | -0.36 [-0.48, -0.24] |
| x45g_swap_27b_r2 | qwen3.6-27b | two people swap | recall | after | 99 | 0.81 [0.71, 0.91] | 0.00 [-0.04, 0.04] | 0.87 [0.76, 0.97] | 0.05 [0.01, 0.11] (jpp) | 0.05 [0.01, 0.11] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | lookup | all | 200 | 0.05 [0.01, 0.09] | 0.19 [0.11, 0.26] | 0.47 [0.35, 0.58] | 0.28 [0.15, 0.41] (Alf) | 0.42 [0.29, 0.54] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | lookup | before | 103 | 0.01 [0.00, 0.04] | 0.18 [0.10, 0.26] | 0.49 [0.36, 0.63] | 0.31 [0.17, 0.46] (Alf) | 0.48 [0.34, 0.62] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | lookup | after | 97 | 0.31 [0.08, 0.56] | 0.23 [0.00, 0.45] | 0.31 [0.08, 0.56] | -0.00 [-0.33, 0.33] (jpp) | -0.00 [-0.33, 0.33] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | recall | all | 200 | 0.61 [0.51, 0.69] | 0.03 [-0.03, 0.08] | 0.73 [0.62, 0.81] | 0.12 [0.04, 0.19] (jpp) | 0.12 [0.04, 0.19] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | recall | before | 103 | 0.49 [0.39, 0.60] | 0.07 [-0.05, 0.16] | 0.67 [0.52, 0.80] | 0.17 [0.03, 0.32] (jpp) | 0.17 [0.03, 0.32] |
| x45g_one_27b_r2 | qwen3.6-27b | only the asked pick | recall | after | 97 | 0.73 [0.58, 0.86] | -0.01 [-0.05, 0.00] | 0.79 [0.65, 0.90] | 0.06 [0.01, 0.11] (jpp) | 0.06 [0.01, 0.11] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | lookup | all | 200 | -0.10 [-0.15, -0.04] | 0.51 [0.41, 0.63] | 0.39 [0.26, 0.51] | -0.13 [-0.21, -0.04] (Alf) | 0.49 [0.34, 0.62] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | lookup | before | 92 | -0.07 [-0.12, -0.02] | 0.57 [0.44, 0.69] | 0.45 [0.31, 0.59] | -0.12 [-0.20, -0.02] (Alf) | 0.52 [0.38, 0.66] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | lookup | after | 108 | -0.30 [-0.44, 0.00] | 0.20 [0.00, 0.50] | 0.00 [-0.40, 0.22] | -0.20 [-0.50, 0.00] (Alf) | 0.30 [-0.29, 0.57] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | recall | all | 200 | 0.76 [0.62, 0.88] | 0.02 [-0.04, 0.09] | 0.79 [0.68, 0.89] | 0.03 [-0.04, 0.11] (jpp) | 0.03 [-0.04, 0.11] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | recall | before | 92 | 0.70 [0.49, 0.91] | 0.04 [-0.10, 0.18] | 0.70 [0.55, 0.87] | -0.00 [-0.15, 0.18] (jpp) | -0.00 [-0.15, 0.18] |
| muse30b_x45g_swap | muse-glimmer-30b | two people swap | recall | after | 108 | 0.80 [0.65, 0.92] | 0.00 [-0.07, 0.07] | 0.85 [0.69, 0.97] | 0.04 [-0.03, 0.12] (jpp) | 0.04 [-0.03, 0.12] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | lookup | all | 200 | -0.01 [-0.04, 0.00] | 0.33 [0.23, 0.42] | 0.38 [0.29, 0.49] | 0.06 [-0.01, 0.13] (Alf) | 0.40 [0.30, 0.49] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | lookup | before | 95 | 0.00 [0.00, 0.00] | 0.34 [0.25, 0.44] | 0.41 [0.31, 0.51] | 0.07 [0.00, 0.13] (Alf) | 0.41 [0.31, 0.51] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | lookup | after | 105 | -0.10 [-0.29, 0.00] | 0.20 [0.00, 0.40] | 0.20 [0.00, 0.50] | -0.00 [-0.25, 0.38] (Alf) | 0.30 [0.00, 0.57] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | recall | all | 200 | 0.68 [0.55, 0.79] | -0.01 [-0.08, 0.07] | 0.76 [0.65, 0.87] | 0.09 [0.01, 0.17] (jpp) | 0.09 [0.01, 0.17] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | recall | before | 95 | 0.57 [0.36, 0.78] | 0.00 [-0.15, 0.15] | 0.69 [0.49, 0.89] | 0.12 [-0.02, 0.29] (jpp) | 0.12 [-0.02, 0.29] |
| muse30b_x45g_one | muse-glimmer-30b | only the asked pick | recall | after | 105 | 0.76 [0.64, 0.87] | -0.02 [-0.07, 0.04] | 0.83 [0.70, 0.93] | 0.06 [-0.00, 0.13] (jpp) | 0.06 [-0.00, 0.13] |

Rule (a) holds on a scene set if at least 3 of 4 models meet its clause; rule (b)'s count of models is reported (the brief does not say how many models it needs).

- two people swap: (a) 0 of 3 models -> does not hold; (b) 3 of 3 models.
- only the asked pick: (a) 1 of 3 models -> does not hold; (b) 2 of 3 models.
