# The address swap: share of recalls changed, all rows vs rows where the target item's legs differ from the original item's (post hoc)

Rule: max |non-colliding - reported| = 0.0441 (bar 0.05): caveat line only

## qwen3.5-9b (qwen35_9b_x8_write); README reports 0.2150 (write, s = 2); all-rows share equals it: True

| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |
|---|---|---|---|---|---|
| write|1 | 600 | 0.155 (93) | 0.040 [0.022, 0.062] | 507 | 0.045 [0.024, 0.072] |
| write|2 | 600 | 0.155 (93) | 0.215 [0.165, 0.276] | 507 | 0.243 [0.182, 0.322] |
| write|4 | 600 | 0.155 (93) | 0.427 [0.374, 0.480] | 507 | 0.477 [0.413, 0.548] |
| random|1 | 600 | 0.155 (93) | 0.005 [0.000, 0.016] | 507 | 0.004 [0.000, 0.013] |
| random|4 | 600 | 0.155 (93) | 0.030 [0.011, 0.055] | 507 | 0.022 [0.006, 0.044] |

C2-0047 (write, s = 2): [{'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'bee', 'legs_j': 6, 'legs_k': 6, 'changed': 0, 'collision': True}, {'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'chicken', 'legs_j': 6, 'legs_k': 2, 'changed': 0, 'collision': False}]

## qwen3.6-27b (x8_write_27b); README reports 0.0433 (write, s = 2); all-rows share equals it: True

| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |
|---|---|---|---|---|---|
| write|1 | 600 | 0.158 (95) | 0.007 [0.000, 0.015] | 505 | 0.008 [0.000, 0.018] |
| write|2 | 600 | 0.158 (95) | 0.043 [0.015, 0.082] | 505 | 0.045 [0.017, 0.084] |
| write|4 | 600 | 0.158 (95) | 0.113 [0.066, 0.172] | 505 | 0.127 [0.075, 0.191] |
| random|1 | 600 | 0.158 (95) | 0.000 [0.000, 0.000] | 505 | 0.000 [0.000, 0.000] |
| random|4 | 600 | 0.158 (95) | 0.005 [0.000, 0.013] | 505 | 0.006 [0.000, 0.015] |

C2-0047 (write, s = 2): [{'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'bee', 'legs_j': 6, 'legs_k': 6, 'changed': 0, 'collision': True}, {'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'chicken', 'legs_j': 6, 'legs_k': 2, 'changed': 0, 'collision': False}]

## muse-glimmer-30b (muse30b_x8_write); README reports 0.0583 (write, s = 2); all-rows share equals it: True

| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |
|---|---|---|---|---|---|
| write|1 | 600 | 0.203 (122) | 0.007 [0.000, 0.022] | 478 | 0.008 [0.000, 0.028] |
| write|2 | 600 | 0.203 (122) | 0.058 [0.029, 0.098] | 478 | 0.061 [0.028, 0.104] |
| write|4 | 600 | 0.203 (122) | 0.107 [0.064, 0.160] | 478 | 0.109 [0.060, 0.174] |
| random|1 | 600 | 0.203 (122) | 0.003 [0.000, 0.009] | 478 | 0.004 [0.000, 0.011] |
| random|4 | 600 | 0.203 (122) | 0.010 [0.000, 0.026] | 478 | 0.011 [0.000, 0.030] |

C2-0047 (write, s = 2): []

## nemotron-3.5-lightning (nem35l_x52_write); README reports 0.2733 (write, s = 2); all-rows share equals it: True

| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |
|---|---|---|---|---|---|
| write|1 | 600 | 0.165 (99) | 0.020 [0.004, 0.041] | 501 | 0.022 [0.005, 0.043] |
| write|2 | 600 | 0.165 (99) | 0.273 [0.217, 0.329] | 501 | 0.317 [0.254, 0.380] |
| write|4 | 600 | 0.165 (99) | 0.398 [0.318, 0.473] | 501 | 0.469 [0.383, 0.549] |
| random|1 | 600 | 0.165 (99) | 0.002 [0.000, 0.005] | 501 | 0.000 [0.000, 0.000] |
| random|4 | 600 | 0.165 (99) | 0.013 [0.004, 0.024] | 501 | 0.014 [0.005, 0.025] |

C2-0047 (write, s = 2): []

## qwen3.5-122b-a10b (qwen35_122b_x8_write_g75); README reports 0.2267 (write, s = 2); all-rows share equals it: True

| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |
|---|---|---|---|---|---|
| write|1 | 600 | 0.157 (94) | 0.032 [0.017, 0.051] | 506 | 0.034 [0.018, 0.055] |
| write|2 | 600 | 0.157 (94) | 0.227 [0.175, 0.291] | 506 | 0.249 [0.186, 0.336] |
| write|4 | 600 | 0.157 (94) | 0.447 [0.375, 0.526] | 506 | 0.490 [0.402, 0.596] |
| random|1 | 600 | 0.157 (94) | 0.017 [0.004, 0.033] | 506 | 0.014 [0.003, 0.029] |
| random|4 | 600 | 0.157 (94) | 0.032 [0.015, 0.053] | 506 | 0.028 [0.011, 0.051] |

C2-0047 (write, s = 2): [{'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'bee', 'legs_j': 6, 'legs_k': 6, 'changed': 0, 'collision': True}, {'scene': 'C2-0047', 'j_item': 'butterfly', 'k_item': 'chicken', 'legs_j': 6, 'legs_k': 2, 'changed': 0, 'collision': False}]

