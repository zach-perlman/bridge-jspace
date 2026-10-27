# pointer_swap / d3v5_smoke_27b

Checks: {"self_noop": {"n": 24, "same_top": 23, "max_abs_dlogit_max": 0.5625}, "layer0_all_reproduces_source": {"n": 24, "same_top": 24, "max_abs_dlogit_max": 0.4219}, "unedited_base_answer_read": {"n": 24, "base_answer": 20}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5-digit|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e5-word|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e8-digit|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e8-word|last: 50: damage, early: damage, mid: damage, transit: damage

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5-digit | last | 50 | dissoc | 6 | 33% [10,70] | 0% [0,39] | 17% [3,56] | 0% [0,39] | 50% [19,81] | 0% |
| RL | e5-digit | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | 50 | other | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-digit | last | transit | dissoc | 6 | 17% [3,56] | 0% [0,39] | 0% [0,39] | 83% [44,97] | - | 0% |
| RL | e5-digit | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-word | last | 50 | dissoc | 6 | 33% [10,70] | 0% [0,39] | 17% [3,56] | 0% [0,39] | 17% [3,56] | 33% |
| RL | e5-word | last | 50 | same | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | 50 | rand | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | 50 | other | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e5-word | last | early | dissoc | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | early | same | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | mid | dissoc | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | mid | same | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e5-word | last | transit | dissoc | 6 | 67% [30,90] | 17% [3,56] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e5-word | last | transit | same | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 50% |
| RL | e8-digit | last | 50 | dissoc | 6 | 0% [0,39] | 50% [19,81] | 33% [10,70] | 0% [0,39] | 17% [3,56] | 0% |
| RL | e8-digit | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | 50 | other | 6 | 67% [30,90] | 0% [0,39] | 0% [0,39] | 17% [3,56] | 17% [3,56] | 0% |
| RL | e8-digit | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-digit | last | transit | dissoc | 6 | 0% [0,39] | 33% [10,70] | 0% [0,39] | 67% [30,90] | - | 0% |
| RL | e8-digit | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e8-word | last | 50 | dissoc | 6 | 33% [10,70] | 33% [10,70] | 0% [0,39] | 0% [0,39] | 33% [10,70] | 0% |
| RL | e8-word | last | 50 | same | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e8-word | last | 50 | rand | 6 | 67% [30,90] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 33% |
| RL | e8-word | last | 50 | other | 6 | 50% [19,81] | 0% [0,39] | 0% [0,39] | 0% [0,39] | 50% [19,81] | 0% |
| RL | e8-word | last | early | dissoc | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e8-word | last | early | same | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e8-word | last | mid | dissoc | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e8-word | last | mid | same | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 17% |
| RL | e8-word | last | transit | dissoc | 6 | 83% [44,97] | 0% [0,39] | 0% [0,39] | 0% [0,39] | 17% [3,56] | 0% |
| RL | e8-word | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
