# pointer_swap / d3_absent_entity_27b_r2

Checks: {"self_noop": {"n": 1528, "same_top": 1528, "max_abs_dlogit_max": 1.6562}, "layer0_all_reproduces_source": {"n": 1528, "same_top": 1528, "max_abs_dlogit_max": 0.9688}, "unedited_base_answer_read": {"n": 1528, "base_answer": 1528}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5f0|last: 50: position, early: none, mid: none, transit: value
- DL|e5f0|last: 50: position, early: none, mid: none, transit: none

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5f0 | last | 50 | dissoc | 764 | 21% [18,24] | 0% [0,0] | 57% [54,61] | 0% [0,0] | 22% [19,25] | 0% |
| RL | e5f0 | last | 50 | same | 764 | 99% [99,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | 1% [0,1] | 0% |
| RL | e5f0 | last | 50 | rand | 764 | 100% [99,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | 0% [0,1] | 0% |
| RL | e5f0 | last | 50 | other | 764 | 66% [63,70] | 0% [0,0] | 25% [22,28] | 0% [0,0] | 9% [7,11] | 0% |
| RL | e5f0 | last | early | dissoc | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | early | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | mid | dissoc | 764 | 100% [99,100] | 0% [0,0] | 0% [0,1] | 0% [0,0] | 0% [0,1] | 0% |
| RL | e5f0 | last | mid | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | transit | dissoc | 764 | 27% [24,30] | 0% [0,0] | 26% [23,30] | 44% [40,47] | 3% [2,4] | 0% |
| RL | e5f0 | last | transit | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | 50 | dissoc | 764 | 58% [54,61] | 0% [0,0] | 34% [31,38] | 0% [0,0] | 8% [6,10] | 0% |
| DL | e5f0 | last | 50 | same | 764 | 100% [99,100] | 0% [0,0] | 0% [0,1] | 0% [0,0] | 0% [0,1] | 0% |
| DL | e5f0 | last | 50 | rand | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | 50 | other | 764 | 99% [98,99] | 0% [0,0] | 1% [0,2] | 0% [0,0] | 0% [0,1] | 0% |
| DL | e5f0 | last | early | dissoc | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | early | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | mid | dissoc | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | mid | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | transit | dissoc | 764 | 85% [83,88] | 0% [0,0] | 10% [8,13] | 3% [2,5] | 1% [1,2] | 0% |
| DL | e5f0 | last | transit | same | 764 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
