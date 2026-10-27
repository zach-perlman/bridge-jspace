# pointer_fit

Verdict: **the slot direction steers the lookup where the lens push does not**

Checks: {"a_lower_bound_ge_0.30": true, "b_20_points_above_lens_and_random": true, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 48, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 42% [38, 45] (n=729) |
| lens | 0% [-0, 1] (n=729) |
| random | 0% [-0, 1] (n=729) |
| shuffled | 1% [1, 2] (n=729) |
| rr_slot | 0% [0, 3] (n=200) |
| span_only | 27% [24, 31] (n=729) |
| rest_only | 7% [5, 9] (n=729) |
| held_out_entities | 46% [41, 51] (n=371) |
| seen_entities | 37% [32, 42] (n=358) |
| patch | 31% [27, 34] (n=729) |
| sub4 | 38% [35, 42] (n=729) |

slot - lens +42 [+38, +45] pts; slot - random +42 [+38, +45] pts
