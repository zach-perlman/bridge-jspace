# pointer_swap / d3_absent_entity_27b_smoke

Checks: {"self_noop": {"n": 30, "same_top": 30, "max_abs_dlogit_max": 0.2812}, "layer0_all_reproduces_source": {"n": 30, "same_top": 30, "max_abs_dlogit_max": 0.3945}, "unedited_base_answer_read": {"n": 30, "base_answer": 30}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5f0|last: 50: damage, early: damage, mid: damage, transit: damage
- DL|e5f0|last: 50: damage, early: damage, mid: damage, transit: damage

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5f0 | last | 50 | dissoc | 15 | 20% [7,45] | 0% [-0,20] | 60% [36,80] | 0% [-0,20] | 20% [7,45] | 0% |
| RL | e5f0 | last | 50 | same | 15 | 93% [70,99] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | 7% [1,30] | 0% |
| RL | e5f0 | last | 50 | rand | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| RL | e5f0 | last | 50 | other | 15 | 93% [70,99] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | 7% [1,30] | 0% |
| RL | e5f0 | last | early | dissoc | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| RL | e5f0 | last | early | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| RL | e5f0 | last | mid | dissoc | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| RL | e5f0 | last | mid | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| RL | e5f0 | last | transit | dissoc | 15 | 27% [11,52] | 0% [-0,20] | 27% [11,52] | 47% [25,70] | - | 0% |
| RL | e5f0 | last | transit | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | 50 | dissoc | 15 | 47% [25,70] | 0% [-0,20] | 40% [20,64] | 0% [-0,20] | 13% [4,38] | 0% |
| DL | e5f0 | last | 50 | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | 50 | rand | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | 50 | other | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | early | dissoc | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | early | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | mid | dissoc | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | mid | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | transit | dissoc | 15 | 87% [62,96] | 0% [-0,20] | 13% [4,38] | 0% [-0,20] | - | 0% |
| DL | e5f0 | last | transit | same | 15 | 100% [80,100] | 0% [-0,20] | 0% [-0,20] | 0% [-0,20] | - | 0% |
