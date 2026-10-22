# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": true, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 44, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 31% [25, 39] (n=175) |
| lens | 1% [0, 3] (n=175) |
| random | 0% [0, 2] (n=175) |
| shuffled | 1% [0, 4] (n=175) |
| rr_slot | 2% [1, 4] (n=198) |
| span_only | 14% [9, 20] (n=175) |
| rest_only | 7% [4, 12] (n=175) |
| held_out_entities | 24% [16, 34] (n=88) |
| seen_entities | 39% [30, 50] (n=87) |
| patch | 22% [17, 29] (n=175) |
| sub4 | 25% [19, 31] (n=175) |

slot - lens +31 [+25, +38] pts; slot - random +31 [+25, +38] pts
