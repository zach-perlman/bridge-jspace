# pointer_fit

Verdict: **the slot direction steers the lookup where the lens push does not**

Checks: {"a_lower_bound_ge_0.30": true, "b_20_points_above_lens_and_random": true, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 48, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 37% [30, 45] (n=175) |
| lens | 0% [0, 2] (n=175) |
| random | 0% [0, 2] (n=175) |
| shuffled | 1% [0, 4] (n=175) |
| rr_slot | 1% [0, 5] (n=100) |
| span_only | 26% [20, 33] (n=175) |
| rest_only | 6% [4, 11] (n=175) |
| held_out_entities | 35% [26, 46] (n=88) |
| seen_entities | 39% [30, 50] (n=87) |
| patch | 34% [28, 42] (n=175) |
| sub1 | 21% [16, 28] (n=175) |
| sub2 | 22% [16, 28] (n=175) |
| sub4 | 37% [30, 44] (n=175) |
| sub8 | 41% [34, 49] (n=175) |
| sub16 | 38% [31, 46] (n=175) |

slot - lens +37 [+30, +45] pts; slot - random +37 [+30, +45] pts
