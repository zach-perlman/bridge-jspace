# pointer_swap / d3v4_seed3_swap_27b

Checks: {"self_noop": {"n": 1532, "same_top": 1532, "max_abs_dlogit_max": 1.6562}, "layer0_all_reproduces_source": {"n": 1532, "same_top": 1532, "max_abs_dlogit_max": 1.9688}, "unedited_base_answer_read": {"n": 1532, "base_answer": 1532}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5f0|last: 50: position, early: none, mid: none, transit: value
- DL|e5f0|last: 50: position, early: none, mid: none, transit: none

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5f0 | last | 50 | dissoc | 766 | 16% [14,19] | 22% [20,25] | 52% [49,56] | 0% [-0,0] | 9% [7,11] | 0% |
| RL | e5f0 | last | 50 | same | 766 | 99% [99,100] | 0% [0,1] | 0% [-0,0] | 0% [-0,0] | 0% [0,1] | 0% |
| RL | e5f0 | last | 50 | rand | 766 | 100% [99,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | 0% [0,1] | 0% |
| RL | e5f0 | last | 50 | other | 766 | 67% [63,70] | 0% [-0,0] | 26% [23,29] | 0% [-0,0] | 7% [6,10] | 0% |
| RL | e5f0 | last | early | dissoc | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| RL | e5f0 | last | early | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| RL | e5f0 | last | mid | dissoc | 766 | 100% [99,100] | 0% [-0,0] | 0% [0,1] | 0% [-0,0] | - | 0% |
| RL | e5f0 | last | mid | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| RL | e5f0 | last | transit | dissoc | 766 | 26% [23,29] | 5% [3,6] | 26% [23,29] | 42% [38,45] | 1% [1,2] | 0% |
| RL | e5f0 | last | transit | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | 50 | dissoc | 766 | 53% [49,56] | 11% [9,14] | 33% [30,36] | 0% [-0,0] | 3% [2,4] | 0% |
| DL | e5f0 | last | 50 | same | 766 | 100% [99,100] | 0% [-0,0] | 0% [0,1] | 0% [-0,0] | 0% [0,1] | 0% |
| DL | e5f0 | last | 50 | rand | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | 50 | other | 766 | 98% [97,99] | 0% [-0,0] | 1% [0,2] | 0% [-0,0] | 1% [0,2] | 0% |
| DL | e5f0 | last | early | dissoc | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | early | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | mid | dissoc | 766 | 100% [99,100] | 0% [-0,0] | 0% [0,1] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | mid | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
| DL | e5f0 | last | transit | dissoc | 766 | 83% [81,86] | 2% [1,3] | 10% [8,13] | 4% [3,6] | 1% [0,2] | 0% |
| DL | e5f0 | last | transit | same | 766 | 100% [100,100] | 0% [-0,0] | 0% [-0,0] | 0% [-0,0] | - | 0% |
