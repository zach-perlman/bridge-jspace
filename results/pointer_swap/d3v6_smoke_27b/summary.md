# pointer_swap / d3v6_smoke_27b

Checks: {"self_noop": {"n": 24, "same_top": 24, "max_abs_dlogit_max": 0.3125}, "layer0_all_reproduces_source": {"n": 12, "same_top": 12, "max_abs_dlogit_max": 0.4375}, "unedited_base_answer_read": {"n": 24, "base_answer": 24}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5-still|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e5-abs|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e5-rel|last: 50: damage, early: damage, mid: damage, transit: damage
- RL|e5-long|last: 50: damage, early: damage, mid: damage, transit: damage

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5-still | last | 50 | dissoc | 6 | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% |
| RL | e5-still | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | 50 | other | 6 | 83% [44,97] | 0% [0,39] | 17% [3,56] | 0% [0,39] | - | 0% |
| RL | e5-still | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-still | last | transit | dissoc | 6 | 17% [3,56] | 0% [0,39] | 0% [0,39] | 67% [30,90] | 17% [3,56] | 0% |
| RL | e5-still | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | 50 | dissoc | 6 | 67% [30,90] | 17% [3,56] | 0% [0,39] | 0% [0,39] | 17% [3,56] | 0% |
| RL | e5-abs | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | 50 | other | 6 | 50% [19,81] | 0% [0,39] | 33% [10,70] | 0% [0,39] | 17% [3,56] | 0% |
| RL | e5-abs | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-abs | last | transit | dissoc | 6 | 17% [3,56] | 0% [0,39] | 0% [0,39] | 83% [44,97] | - | 0% |
| RL | e5-abs | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | 50 | dissoc | 6 | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% |
| RL | e5-rel | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | 50 | other | 6 | 83% [44,97] | 0% [0,39] | 17% [3,56] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-rel | last | transit | dissoc | 6 | 33% [10,70] | 0% [0,39] | 0% [0,39] | 67% [30,90] | - | 0% |
| RL | e5-rel | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | 50 | dissoc | 6 | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% [0,39] | 33% [10,70] | 0% |
| RL | e5-long | last | 50 | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | 50 | rand | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | 50 | other | 6 | 67% [30,90] | 0% [0,39] | 33% [10,70] | 0% [0,39] | - | 0% |
| RL | e5-long | last | early | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | early | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | mid | dissoc | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | mid | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
| RL | e5-long | last | transit | dissoc | 6 | 17% [3,56] | 0% [0,39] | 0% [0,39] | 67% [30,90] | 17% [3,56] | 0% |
| RL | e5-long | last | transit | same | 6 | 100% [61,100] | 0% [0,39] | 0% [0,39] | 0% [0,39] | - | 0% |
