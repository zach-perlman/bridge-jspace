# pointer_swap / qwen3_32b_d3v4_swap_r2_smoke

Checks: {"self_noop": {"n": 6, "same_top": 6, "max_abs_dlogit_max": 0.4297}, "layer0_all_reproduces_source": {"n": 6, "same_top": 6, "max_abs_dlogit_max": 0.75}, "unedited_base_answer_read": {"n": 6, "base_answer": 6}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5f0|last: 40: damage, early: damage, mid: damage, transit: damage

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5f0 | last | 40 | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | 40 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | 40 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | 40 | other | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5f0 | last | transit | dissoc | 6 | 0% [0,39] | 0% [0,39] | 17% [3,56] | 83% [44,97] | - | 0% |
| RL | e5f0 | last | transit | same | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | 17% [3,56] | 0% |
